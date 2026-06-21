"""
Fase 2 — Pré-processamento das notícias coletadas.

Entrada:  data/raw/noticias.jsonl        (Fase 1)
Saída:    data/interim/noticias_limpo.parquet

Etapas:
1. Limpeza de texto e remoção de boilerplate (bloco de créditos editoriais ao
   final: "Texto:", "Edição:", "Revisão:", "Fonte:", "Agência CNJ de Notícias",
   siglas de Ascom/tribunais).
2. Filtro de idioma (mantém apenas pt-BR via langdetect, determinístico).
3. Deduplicação semântica leve via MinHash (Jaccard de shingles de palavras),
   sem dependências pesadas — captura republicações quase idênticas.
4. Normalização (gera `corpo_norm` para c-TF-IDF/wordcloud; mantém o original
   `corpo_texto` limpo para embeddings).
5. Campos derivados: `mes`, `n_tokens`, `n_chars`.

Uso:
    python src/preprocess.py
    python src/preprocess.py --min-chars 250 --jaccard 0.85
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

import pandas as pd
from langdetect import DetectorFactory, LangDetectException, detect

# Torna o langdetect determinístico (reprodutibilidade).
DetectorFactory.seed = 42

PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = PROJECT_ROOT / "data" / "raw" / "noticias.jsonl"
OUTPUT_PATH = PROJECT_ROOT / "data" / "interim" / "noticias_limpo.parquet"

# Marcadores do bloco de créditos editoriais que aparece ao final das matérias.
CREDIT_MARKERS = [
    "Texto:", "Edição:", "Edicao:", "Revisão:", "Revisao:",
    "Fotos:", "Foto:", "Fonte:", "Colaborou:", "Colaboração:",
    "Com informações", "Com informacoes", "Arte:", "Vídeo:", "Video:",
]

# Assinaturas institucionais que aparecem soltas no fim do corpo.
TRAILING_SIGNATURES = [
    "Agência CNJ de Notícias",
    "Agencia CNJ de Noticias",
]


# --------------------------------------------------------------------------
# Limpeza / boilerplate
# --------------------------------------------------------------------------

def normalize_whitespace(text: str) -> str:
    return " ".join((text or "").split())


def remove_boilerplate(text: str) -> str:
    """Remove o bloco de créditos ao final e assinaturas institucionais soltas.

    Estratégia conservadora: só corta créditos quando aparecem no terço final
    do texto, para não destruir conteúdo legítimo que mencione "Fonte:" no meio.
    """
    text = normalize_whitespace(text)
    if not text:
        return text

    # 1) Remove assinaturas institucionais ao final.
    for sig in TRAILING_SIGNATURES:
        if text.endswith(sig):
            text = text[: -len(sig)].strip()

    # 2) Procura o primeiro marcador de crédito que ocorra no terço final.
    tail_start = int(len(text) * 0.66)
    cut_at = None
    for marker in CREDIT_MARKERS:
        idx = text.find(marker, tail_start)
        if idx != -1 and (cut_at is None or idx < cut_at):
            cut_at = idx
    if cut_at is not None:
        text = text[:cut_at].strip()

    # 3) Nova passada de assinatura (pode ter ficado exposta após o corte).
    for sig in TRAILING_SIGNATURES:
        if text.endswith(sig):
            text = text[: -len(sig)].strip()

    return text.strip(" .;:-—")


def normalize_text(text: str) -> str:
    """Versão normalizada para c-TF-IDF/wordcloud: minúsculas, sem pontuação
    nem dígitos; acentos preservados (relevante para português)."""
    text = (text or "").lower()
    text = re.sub(r"https?://\S+", " ", text)
    # remove tudo que não for letra (inclui acentuadas) ou espaço
    text = re.sub(r"[^a-záàâãéêíóôõúüç\s]", " ", text)
    return normalize_whitespace(text)


# --------------------------------------------------------------------------
# Idioma
# --------------------------------------------------------------------------

def detect_lang(text: str) -> str:
    sample = text[:1500]
    if len(sample) < 20:
        return "unknown"
    try:
        return detect(sample)
    except LangDetectException:
        return "unknown"


# --------------------------------------------------------------------------
# MinHash para dedup semântico leve (sem dependências externas)
# --------------------------------------------------------------------------

NUM_HASHES = 64
_MERSENNE = (1 << 61) - 1  # primo grande para hashing universal


def _hash_coeffs(n: int) -> list[tuple[int, int]]:
    """Coeficientes (a, b) determinísticos para n funções de hash universais."""
    coeffs = []
    for i in range(n):
        a = int(hashlib.md5(f"a{i}".encode()).hexdigest(), 16) % _MERSENNE or 1
        b = int(hashlib.md5(f"b{i}".encode()).hexdigest(), 16) % _MERSENNE
        coeffs.append((a, b))
    return coeffs


_COEFFS = _hash_coeffs(NUM_HASHES)


def shingles(text: str, k: int = 5) -> set[int]:
    """Conjunto de hashes de k-gramas de palavras do texto normalizado."""
    words = normalize_text(text).split()
    if len(words) < k:
        return {hash(" ".join(words))} if words else set()
    out = set()
    for i in range(len(words) - k + 1):
        gram = " ".join(words[i : i + k])
        out.add(int(hashlib.md5(gram.encode()).hexdigest(), 16) % _MERSENNE)
    return out


def minhash_signature(sh: set[int]) -> tuple[int, ...]:
    if not sh:
        return tuple([_MERSENNE] * NUM_HASHES)
    sig = []
    for a, b in _COEFFS:
        sig.append(min(((a * x + b) % _MERSENNE) for x in sh))
    return tuple(sig)


def estimate_jaccard(sig1: tuple[int, ...], sig2: tuple[int, ...]) -> float:
    equal = sum(1 for x, y in zip(sig1, sig2) if x == y)
    return equal / len(sig1)


def find_near_duplicates(df: pd.DataFrame, threshold: float) -> list[int]:
    """Retorna índices a remover (mantém o mais antigo de cada grupo de quase-dups)."""
    sigs = [minhash_signature(shingles(t)) for t in df["corpo_limpo"]]
    n = len(sigs)
    # ordena por data crescente: mantemos a publicação mais antiga.
    order = df["data_publicacao"].argsort().to_list()
    removed: set[int] = set()
    for ii in range(n):
        i = order[ii]
        if i in removed:
            continue
        for jj in range(ii + 1, n):
            j = order[jj]
            if j in removed:
                continue
            if estimate_jaccard(sigs[i], sigs[j]) >= threshold:
                removed.add(j)
    return sorted(removed)


# --------------------------------------------------------------------------
# Pipeline
# --------------------------------------------------------------------------

def run(min_chars: int, jaccard: float) -> None:
    if not INPUT_PATH.exists():
        print(f"[erro] entrada não encontrada: {INPUT_PATH}", file=sys.stderr)
        raise SystemExit(1)

    rows = [json.loads(l) for l in INPUT_PATH.open(encoding="utf-8") if l.strip()]
    df = pd.DataFrame(rows)
    n0 = len(df)
    print(f"[pre] carregados {n0} registros")

    # 1) Limpeza + boilerplate
    df["corpo_limpo"] = df["corpo_texto"].map(remove_boilerplate)
    df["titulo"] = df["titulo"].map(normalize_whitespace)

    # 2) Filtro de comprimento mínimo (corpos curtos demais para modelar)
    df["n_chars"] = df["corpo_limpo"].str.len()
    n_curtos = int((df["n_chars"] < min_chars).sum())
    df = df[df["n_chars"] >= min_chars].copy()
    print(f"[pre] removidos {n_curtos} corpos com < {min_chars} chars "
          f"-> {len(df)} restantes")

    # 3) Filtro de idioma
    df["idioma"] = df["corpo_limpo"].map(detect_lang)
    lang_counts = df["idioma"].value_counts().to_dict()
    n_nao_pt = int((df["idioma"] != "pt").sum())
    df = df[df["idioma"] == "pt"].copy()
    print(f"[pre] idiomas detectados: {lang_counts}")
    print(f"[pre] removidos {n_nao_pt} não-pt -> {len(df)} restantes")

    # 4) Dedup exato por assinatura de texto normalizado
    df["_sig_exata"] = df["corpo_limpo"].map(
        lambda t: hashlib.md5(normalize_text(t).encode()).hexdigest())
    n_antes = len(df)
    df = df.drop_duplicates(subset="_sig_exata", keep="first").copy()
    n_exatos = n_antes - len(df)
    print(f"[pre] removidas {n_exatos} duplicatas exatas -> {len(df)} restantes")

    # 5) Dedup semântico leve (MinHash)
    df = df.reset_index(drop=True)
    dup_idx = find_near_duplicates(df, threshold=jaccard)
    if dup_idx:
        print(f"[pre] quase-duplicatas (Jaccard>={jaccard}) removidas: "
              f"{len(dup_idx)}")
        for i in dup_idx[:10]:
            print(f"       - drop id={df.loc[i,'id']} | {df.loc[i,'titulo'][:60]}")
    else:
        print(f"[pre] nenhuma quase-duplicata (Jaccard>={jaccard})")
    df = df.drop(index=dup_idx).reset_index(drop=True)

    # 6) Normalização + campos derivados
    df["corpo_norm"] = df["corpo_limpo"].map(normalize_text)
    df["corpo_texto"] = df["corpo_limpo"]  # corpo_texto passa a ser o limpo
    df["data_publicacao"] = pd.to_datetime(df["data_publicacao"])
    df["mes"] = df["data_publicacao"].dt.to_period("M").astype(str)
    df["n_chars"] = df["corpo_texto"].str.len()
    df["n_tokens"] = df["corpo_norm"].str.split().map(len)

    cols = [
        "id", "data_publicacao", "mes", "url", "titulo",
        "categoria_fonte", "categoria_fonte_ids",
        "corpo_texto", "corpo_norm", "corpo_html",
        "autoria", "idioma", "n_chars", "n_tokens", "slug",
    ]
    df = df[[c for c in cols if c in df.columns]]

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUTPUT_PATH, index=False)

    print("-" * 60)
    print(f"[pre] CONCLUÍDO: {n0} -> {len(df)} notícias")
    print(f"[pre] tokens: min {df['n_tokens'].min()} | "
          f"mediana {int(df['n_tokens'].median())} | max {df['n_tokens'].max()}")
    print(f"[pre] salvo em {OUTPUT_PATH}")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Pré-processamento das notícias do CNJ.")
    p.add_argument("--min-chars", type=int, default=250,
                   help="Comprimento mínimo do corpo limpo (default 250).")
    p.add_argument("--jaccard", type=float, default=0.85,
                   help="Limiar de Jaccard p/ quase-duplicatas (default 0.85).")
    return p.parse_args()


if __name__ == "__main__":
    a = parse_args()
    run(min_chars=a.min_chars, jaccard=a.jaccard)
