"""
Fase 1 — Coleta de notícias da Agência CNJ via WordPress REST API.

Fonte: https://www.cnj.jus.br/wp-json/wp/v2/posts

Princípios:
- Respeita robots.txt (verificado: /wp-json/ é permitido para User-agent: *).
- Rate limit >= 1s entre requisições.
- Backoff exponencial em respostas 429 e 5xx.
- Idempotente: deduplica por `id` e por `link`; reexecuções não duplicam.
- Persistência incremental em JSON Lines (data/raw/noticias.jsonl).

Campos extraídos por notícia:
    id, data_publicacao, url, titulo, categoria_fonte, corpo_html,
    corpo_texto, autoria

Uso:
    python src/collect.py --after 2025-12-21 --before 2026-06-21
    python src/collect.py --months 6          # janela relativa a hoje
    python src/collect.py --dry-run           # só conta, não baixa

Resultado e limitações são documentados em docs/coleta.md.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.robotparser
from datetime import datetime, timedelta, timezone
from html import unescape
from pathlib import Path

import requests
from bs4 import BeautifulSoup

# --------------------------------------------------------------------------
# Configuração
# --------------------------------------------------------------------------

BASE_URL = "https://www.cnj.jus.br"
API_POSTS = f"{BASE_URL}/wp-json/wp/v2/posts"
API_CATEGORIES = f"{BASE_URL}/wp-json/wp/v2/categories"
ROBOTS_URL = f"{BASE_URL}/robots.txt"

# User-agent identificável e honesto (pesquisa acadêmica, contato no projeto).
USER_AGENT = (
    "cnj-pauta-pln/1.0 (pesquisa academica de PLN; "
    "+https://github.com/; contato via repositorio)"
)

PER_PAGE = 100              # máximo aceito pela WP REST API
RATE_LIMIT_SECONDS = 1.2    # >= 1s exigido; folga para não pressionar o servidor
MAX_RETRIES = 5
BACKOFF_BASE = 2.0          # segundos: 2, 4, 8, 16, 32
REQUEST_TIMEOUT = 60        # segundos

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = PROJECT_ROOT / "data" / "raw" / "noticias.jsonl"


# --------------------------------------------------------------------------
# robots.txt
# --------------------------------------------------------------------------

def check_robots(url: str) -> bool:
    """Verifica se a coleta da URL é permitida pelo robots.txt para nosso UA."""
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(ROBOTS_URL)
    try:
        rp.read()
    except Exception as exc:  # noqa: BLE001
        print(f"[robots] Não foi possível ler robots.txt ({exc}). "
              f"Abortando por precaução.", file=sys.stderr)
        return False
    allowed = rp.can_fetch(USER_AGENT, url)
    allowed_generic = rp.can_fetch("*", url)
    print(f"[robots] can_fetch({url}) -> UA={allowed} | '*'={allowed_generic}")
    return allowed and allowed_generic


# --------------------------------------------------------------------------
# HTTP com retry/backoff
# --------------------------------------------------------------------------

def request_with_backoff(session: requests.Session, url: str,
                         params: dict | None = None) -> requests.Response | None:
    """GET com backoff exponencial em 429/5xx. Retorna Response ou None."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = session.get(url, params=params, timeout=REQUEST_TIMEOUT)
        except requests.RequestException as exc:
            wait = BACKOFF_BASE ** attempt
            print(f"[http] erro de rede ({exc}); tentativa {attempt}/"
                  f"{MAX_RETRIES}; aguardando {wait:.0f}s", file=sys.stderr)
            time.sleep(wait)
            continue

        if resp.status_code == 200:
            return resp

        if resp.status_code == 429 or 500 <= resp.status_code < 600:
            # Respeita Retry-After se presente; senão backoff exponencial.
            retry_after = resp.headers.get("Retry-After")
            if retry_after and retry_after.isdigit():
                wait = float(retry_after)
            else:
                wait = BACKOFF_BASE ** attempt
            print(f"[http] {resp.status_code} em {url}; tentativa {attempt}/"
                  f"{MAX_RETRIES}; aguardando {wait:.0f}s", file=sys.stderr)
            time.sleep(wait)
            continue

        # 4xx que não 429: não adianta repetir.
        print(f"[http] {resp.status_code} definitivo em {url}: "
              f"{resp.text[:200]}", file=sys.stderr)
        return None

    print(f"[http] esgotadas {MAX_RETRIES} tentativas para {url}",
          file=sys.stderr)
    return None


# --------------------------------------------------------------------------
# Categorias (id -> nome)
# --------------------------------------------------------------------------

def fetch_category_map(session: requests.Session) -> dict[int, str]:
    """Baixa todas as categorias e devolve mapeamento id -> nome."""
    cat_map: dict[int, str] = {}
    page = 1
    while True:
        params = {"per_page": PER_PAGE, "page": page, "_fields": "id,name"}
        resp = request_with_backoff(session, API_CATEGORIES, params)
        if resp is None:
            break
        batch = resp.json()
        if not batch:
            break
        for c in batch:
            cat_map[c["id"]] = c["name"]
        total_pages = int(resp.headers.get("X-WP-TotalPages", page))
        if page >= total_pages:
            break
        page += 1
        time.sleep(RATE_LIMIT_SECONDS)
    print(f"[cats] {len(cat_map)} categorias mapeadas")
    return cat_map


# --------------------------------------------------------------------------
# Extração de texto
# --------------------------------------------------------------------------

def html_to_text(html: str) -> str:
    """Converte HTML do corpo em texto limpo (limpeza leve; o pesado fica na Fase 2)."""
    if not html:
        return ""
    soup = BeautifulSoup(html, "lxml")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    text = soup.get_text(separator=" ")
    return " ".join(unescape(text).split())


def extract_record(post: dict, cat_map: dict[int, str]) -> dict:
    """Mapeia um post da API para o registro canônico do projeto."""
    cat_ids = post.get("categories", []) or []
    cat_names = [cat_map.get(cid, str(cid)) for cid in cat_ids]
    corpo_html = (post.get("content") or {}).get("rendered", "") or ""
    titulo_html = (post.get("title") or {}).get("rendered", "") or ""
    return {
        "id": post.get("id"),
        "data_publicacao": post.get("date"),           # horário local do site
        "data_publicacao_gmt": post.get("date_gmt"),
        "url": post.get("link"),
        "titulo": " ".join(unescape(BeautifulSoup(titulo_html, "lxml")
                                    .get_text()).split()),
        "categoria_fonte_ids": cat_ids,
        "categoria_fonte": cat_names,
        "corpo_html": corpo_html,
        "corpo_texto": html_to_text(corpo_html),
        "autoria": _extract_author(post),
        "slug": post.get("slug"),
        "modified": post.get("modified"),
        "_coletado_em": datetime.now(timezone.utc).isoformat(),
    }


def _extract_author(post: dict) -> str | None:
    """Tenta extrair nome de autor; a WP REST embute só o id por padrão.

    A Agência CNJ raramente expõe autoria individual (conteúdo institucional);
    registramos o id quando presente e deixamos o nome a resolver na Fase 2
    se houver _embed. Mantido como campo para fidelidade ao schema pedido.
    """
    emb = post.get("_embedded", {})
    authors = emb.get("author") if isinstance(emb, dict) else None
    if authors and isinstance(authors, list) and authors:
        name = authors[0].get("name")
        if name:
            return name
    aid = post.get("author")
    return f"author_id:{aid}" if aid not in (None, 0) else None


# --------------------------------------------------------------------------
# Idempotência
# --------------------------------------------------------------------------

def load_existing(path: Path) -> tuple[set[int], set[str]]:
    """Carrega ids e urls já coletados para evitar duplicação."""
    ids: set[int] = set()
    urls: set[str] = set()
    if not path.exists():
        return ids, urls
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if rec.get("id") is not None:
                ids.add(rec["id"])
            if rec.get("url"):
                urls.add(rec["url"])
    print(f"[dedup] {len(ids)} registros já existentes em {path.name}")
    return ids, urls


# --------------------------------------------------------------------------
# Coleta principal
# --------------------------------------------------------------------------

def collect(after: str, before: str, dry_run: bool = False) -> int:
    """Coleta posts no intervalo [after, before]. Retorna nº de novos registros."""
    sample_url = f"{API_POSTS}?per_page=1"
    if not check_robots(sample_url):
        print("[robots] coleta NÃO permitida; abortando.", file=sys.stderr)
        return 0

    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT,
                            "Accept": "application/json"})

    after_iso = f"{after}T00:00:00"
    before_iso = f"{before}T23:59:59"

    # Sondagem: total de posts na janela.
    probe = request_with_backoff(
        session, API_POSTS,
        {"per_page": 1, "after": after_iso, "before": before_iso,
         "_fields": "id"},
    )
    if probe is None:
        print("[coleta] falha na sondagem inicial; abortando.", file=sys.stderr)
        return 0
    total = int(probe.headers.get("X-WP-Total", 0))
    total_pages = int(probe.headers.get("X-WP-TotalPages", 0))
    print(f"[coleta] janela {after} -> {before}: {total} posts, "
          f"{(total + PER_PAGE - 1) // PER_PAGE} páginas a {PER_PAGE}/pág")

    if dry_run:
        print("[coleta] dry-run: nada baixado.")
        return total

    if total == 0:
        print("[coleta] nenhum post na janela.", file=sys.stderr)
        return 0

    cat_map = fetch_category_map(session)
    seen_ids, seen_urls = load_existing(OUTPUT_PATH)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    new_count = 0
    n_pages = (total + PER_PAGE - 1) // PER_PAGE

    with OUTPUT_PATH.open("a", encoding="utf-8") as out:
        for page in range(1, n_pages + 1):
            params = {
                "per_page": PER_PAGE,
                "page": page,
                "after": after_iso,
                "before": before_iso,
                "orderby": "date",
                "order": "desc",
            }
            resp = request_with_backoff(session, API_POSTS, params)
            if resp is None:
                print(f"[coleta] página {page} falhou; seguindo.",
                      file=sys.stderr)
                time.sleep(RATE_LIMIT_SECONDS)
                continue

            batch = resp.json()
            if not batch:
                break

            page_new = 0
            for post in batch:
                pid = post.get("id")
                purl = post.get("link")
                if pid in seen_ids or (purl and purl in seen_urls):
                    continue
                rec = extract_record(post, cat_map)
                out.write(json.dumps(rec, ensure_ascii=False) + "\n")
                seen_ids.add(pid)
                if purl:
                    seen_urls.add(purl)
                new_count += 1
                page_new += 1

            out.flush()
            print(f"[coleta] página {page}/{n_pages}: "
                  f"{len(batch)} recebidos, {page_new} novos "
                  f"(total novos: {new_count})")
            time.sleep(RATE_LIMIT_SECONDS)

    print(f"[coleta] CONCLUÍDO: {new_count} novos registros em {OUTPUT_PATH}")
    return new_count


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Coleta de notícias da Agência CNJ.")
    p.add_argument("--after", help="Data inicial YYYY-MM-DD (inclusive).")
    p.add_argument("--before", help="Data final YYYY-MM-DD (inclusive).")
    p.add_argument("--months", type=int, default=6,
                   help="Janela em meses a partir de hoje (se --after ausente).")
    p.add_argument("--dry-run", action="store_true",
                   help="Apenas conta os posts da janela, sem baixar.")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.after:
        after = args.after
    else:
        after_dt = datetime.now(timezone.utc) - timedelta(days=30 * args.months)
        after = after_dt.strftime("%Y-%m-%d")
    before = args.before or datetime.now(timezone.utc).strftime("%Y-%m-%d")

    n = collect(after, before, dry_run=args.dry_run)
    return 0 if (n > 0 or args.dry_run) else 1


if __name__ == "__main__":
    raise SystemExit(main())
