"""
Fase 6b — Reconhecimento de Entidades Nomeadas (NER).

Usa o modelo de NER em português indicado pelo professor
(`rhaymison/ner-portuguese-br-bert-cased`, baseado em BERT) para extrair
entidades das notícias (pessoas, organizações/tribunais, locais, etc.) e analisar
*quem e o quê* domina a comunicação institucional do CNJ, inclusive por classe
temática (cruzando com os rótulos da Fase 4).

Roda só com PyTorch/transformers (sem TensorFlow) — processo independente, sem
conflito de runtime. Por limite de 512 subtokens do modelo, processa
**título + início do corpo** (a maioria das entidades de uma notícia aparece no
lead); a limitação é declarada honestamente.

Limpeza da saída do NER (a saída crua é ruidosa — fragmentos de subpalavra,
preposições penduradas nas bordas do span, substantivos comuns tageados como
entidade, sem corte de confiança). Funil aplicado, nesta ordem, com contagem
real reportada a cada etapa:

    bruto -> após score (>= --min-score) -> após edge-clean (bordas funcionais)
          -> após filtro de fragmento -> após filtro de genérico = final

As listas canônicas (GENERIC_ENTITY_STOP, ENTITY_SELF_REF,
ENTITY_ACRONYM_WHITELIST, ENTITY_EDGE_WORDS) vêm da fonte única TF-free
`src/text_utils.py`. O campo `tipo` (entity_group) do modelo é ruidoso: é tratado
como informativo, não autoritativo.

Artefatos:
- data/processed/entidades.parquet        (uma linha por entidade encontrada)
- data/processed/entidades_top.csv        top entidades agregadas
- data/processed/entidades_por_classe.csv top entidades por classe temática
                                          (auto-referências do CNJ excluídas)
- reports/figures/16_top_entidades.png

Uso:
    python src/ner.py --min-score 0.90
    python src/ner.py --min-score 0.90 --max-chars 1500
"""

from __future__ import annotations

import argparse
import sys
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
INTERIM = PROJECT_ROOT / "data" / "interim" / "noticias_limpo.parquet"
PROC = PROJECT_ROOT / "data" / "processed"
FIG = PROJECT_ROOT / "reports" / "figures"
MODEL_NAME = "rhaymison/ner-portuguese-br-bert-cased"

# Listas canônicas de limpeza vêm da fonte única TF-free (text_utils), mesma
# origem da taxonomia e das stopwords — nunca redefinir aqui.
sys.path.insert(0, str(PROJECT_ROOT / "src"))
from text_utils import (  # noqa: E402
    ENTITY_ACRONYM_WHITELIST,
    ENTITY_EDGE_WORDS,
    ENTITY_SELF_REF,
    GENERIC_ENTITY_STOP,
)


def _norm_key(s: str) -> str:
    """Chave de agregação: minúsculas, sem acento, espaços colapsados."""
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return " ".join(s.lower().split())


def _clean_span(surface: str) -> str:
    """Remove palavras funcionais penduradas no início/fim do span e colapsa
    espaços ("Tribunal de Justiça do" -> "Tribunal de Justiça"). Nunca toca no
    miolo do span — só nas bordas."""
    toks = surface.split()
    while toks and _norm_key(toks[0]) in ENTITY_EDGE_WORDS:
        toks.pop(0)
    while toks and _norm_key(toks[-1]) in ENTITY_EDGE_WORDS:
        toks.pop()
    return " ".join(toks)


def _is_fragment(surface: str, tipo: str, key: str) -> bool:
    """True se o span parece ruído de tokenizer/agregação e não uma entidade:
    - resíduo de subpalavra ("##J", "##dor");
    - curto demais (< 3 chars normalizados);
    - sem nenhuma letra;
    - curto (<= 4) e PER/ORG fora da whitelist de siglas (ex.: "Corre", "Def").
      LOC curto é mantido (siglas de UF, etc.); a whitelist protege CNJ/STF/...
    """
    if "##" in surface:
        return True
    if len(key) < 3:
        return True
    if not any(ch.isalpha() for ch in surface):
        return True
    if len(key) <= 4 and tipo in ("PER", "ORG") \
            and key not in ENTITY_ACRONYM_WHITELIST:
        return True
    return False


def extract_entities(max_chars: int, min_score: float) -> pd.DataFrame:
    import torch
    from transformers import pipeline

    df = pd.read_parquet(INTERIM)[["id", "titulo", "corpo_texto"]]
    cls = pd.read_parquet(PROC / "doc_topics.parquet")[
        ["id", "classe_id", "classe_tematica"]]
    df = df.merge(cls, on="id")
    texts = (df["titulo"].fillna("") + ". "
             + df["corpo_texto"].fillna("").str[:max_chars]).tolist()

    device = 0 if torch.cuda.is_available() else -1
    print(f"[ner] {len(texts)} documentos | modelo {MODEL_NAME} | "
          f"device={'cuda' if device == 0 else 'cpu'} | max_chars={max_chars} "
          f"| min_score={min_score}")
    # aggregation_strategy="max": remonta melhor entidades multi-token que a
    # estratégia "simple", reduzindo fragmentos na origem.
    ner = pipeline("ner", model=MODEL_NAME, aggregation_strategy="max",
                   device=device)

    # Funil de limpeza — contagem real em cada etapa.
    funnel = {"bruto": 0, "score": 0, "edge": 0, "frag": 0, "final": 0}
    rows = []
    bs = 16
    for i in range(0, len(texts), bs):
        batch = texts[i:i + bs]
        results = ner(batch, batch_size=bs)
        if isinstance(results, dict):           # caso de 1 elemento
            results = [results]
        for local, ents in enumerate(results):
            r = df.iloc[i + local]
            for e in ents:
                funnel["bruto"] += 1
                score = float(e["score"])
                if score < min_score:
                    continue
                funnel["score"] += 1
                surface = _clean_span(str(e["word"]).strip())
                if not surface:                 # span era só palavra funcional
                    continue
                funnel["edge"] += 1
                tipo = e["entity_group"]
                key = _norm_key(surface)
                if _is_fragment(surface, tipo, key):
                    continue
                funnel["frag"] += 1
                if key in GENERIC_ENTITY_STOP:
                    continue
                funnel["final"] += 1
                rows.append({
                    "id": int(r["id"]),
                    "classe_id": int(r["classe_id"]),
                    "classe_tematica": r["classe_tematica"],
                    "entidade": surface,
                    "entidade_key": key,
                    "tipo": tipo,
                    "score": round(score, 4),
                })
        print(f"[ner]   {min(i + bs, len(texts))}/{len(texts)}", end="\r")
    print()

    _report_funnel(funnel)
    ent = pd.DataFrame(rows)
    print(f"[ner] {len(ent)} entidades finais | tipos (informativo, não "
          f"autoritativo): {ent['tipo'].value_counts().to_dict()}")
    _report_residual_fragments(ent)
    return ent


def _report_funnel(f: dict) -> None:
    """Imprime o funil de limpeza com contagens absolutas e % retido vs bruto."""
    b = max(f["bruto"], 1)
    print("[ner] funil de limpeza (contagem real):")
    print(f"[ner]   bruto                 : {f['bruto']:6d} (100,0%)")
    print(f"[ner]   após score (>=min)    : {f['score']:6d} "
          f"({100 * f['score'] / b:5.1f}%)")
    print(f"[ner]   após edge-clean       : {f['edge']:6d} "
          f"({100 * f['edge'] / b:5.1f}%)")
    print(f"[ner]   após filtro fragmento : {f['frag']:6d} "
          f"({100 * f['frag'] / b:5.1f}%)")
    print(f"[ner]   após filtro genérico  : {f['final']:6d} "
          f"({100 * f['final'] / b:5.1f}%)  <- FINAL")


def _report_residual_fragments(ent: pd.DataFrame) -> None:
    """Honestidade sobre o resíduo: mede a taxa de fragmento residual — chaves
    curtas (<= 4 chars) que NÃO são siglas conhecidas e que sobreviveram aos
    filtros (sobretudo LOC curto, que o filtro de fragmento deixa passar)."""
    if ent.empty:
        print("[ner] taxa de fragmento residual: n/d (sem entidades)")
        return
    suspect = ent[(ent["entidade_key"].str.len() <= 4)
                  & (~ent["entidade_key"].isin(ENTITY_ACRONYM_WHITELIST))]
    n, tot = len(suspect), len(ent)
    print(f"[ner] taxa de fragmento residual: {n}/{tot} = "
          f"{100 * n / tot:.2f}% (chaves <=4 chars não-sigla)")
    if n:
        amostra = suspect["entidade_key"].value_counts().head(10).to_dict()
        print(f"[ner]   amostra de resíduo: {amostra}")


def aggregate(ent: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    # Top entidades por nº de DOCUMENTOS distintos (evita inflar por repetição).
    # Auto-referências do CNJ permanecem aqui (são entidades de fato).
    top = (ent.groupby(["entidade_key", "tipo"])
              .agg(docs=("id", "nunique"),
                   ocorrencias=("id", "size"),
                   exemplo=("entidade", "first"))
              .reset_index()
              .sort_values("docs", ascending=False))

    # Top entidade por classe temática (análise diferencial): aqui as
    # auto-referências do CNJ são EXCLUÍDAS — não distinguem classe alguma.
    ent_diff = ent[~ent["entidade_key"].isin(ENTITY_SELF_REF)]
    by_class = (ent_diff.groupby(["classe_tematica", "entidade_key"])
                   .agg(docs=("id", "nunique"), exemplo=("entidade", "first"))
                   .reset_index())
    by_class = (by_class.sort_values(["classe_tematica", "docs"],
                                     ascending=[True, False])
                        .groupby("classe_tematica").head(8))
    return top, by_class


def plot_top(top: pd.DataFrame, k: int = 20) -> None:
    import matplotlib.pyplot as plt
    sub = top.head(k).iloc[::-1]
    palette = {t: c for t, c in zip(
        sorted(top["tipo"].unique()),
        ["#2c6fbb", "#3a9a6d", "#bb5d2c", "#8a5dbb", "#bb2c4f", "#777777",
         "#5d8abb", "#bb8a5d", "#5dbb8a", "#8abb5d"])}
    colors = [palette.get(t, "#777777") for t in sub["tipo"]]
    fig, ax = plt.subplots(figsize=(9, 8))
    ax.barh(sub["exemplo"], sub["docs"], color=colors)
    ax.set_xlabel("Nº de notícias (documentos distintos)")
    ax.set_title(f"Top {k} entidades nomeadas na comunicação do CNJ")
    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in palette.values()]
    ax.legend(handles, palette.keys(), title="tipo", loc="lower right")
    for i, v in enumerate(sub["docs"]):
        ax.text(v + 0.3, i, str(int(v)), va="center", fontsize=8)
    plt.tight_layout()
    FIG.mkdir(parents=True, exist_ok=True)
    plt.savefig(FIG / "16_top_entidades.png")
    plt.close()
    print(f"[ner] figura -> {FIG / '16_top_entidades.png'}")


def main() -> None:
    ap = argparse.ArgumentParser(description="NER das notícias do CNJ.")
    ap.add_argument("--max-chars", type=int, default=1500,
                    help="Caracteres do corpo usados por documento (lead).")
    ap.add_argument("--min-score", type=float, default=0.90,
                    help="Corte de confiança: descarta entidades com score < "
                         "min-score (default 0.90).")
    args = ap.parse_args()

    ent = extract_entities(args.max_chars, args.min_score)
    PROC.mkdir(parents=True, exist_ok=True)
    ent.to_parquet(PROC / "entidades.parquet", index=False)
    print(f"[ner] salvo -> {PROC / 'entidades.parquet'}")

    top, by_class = aggregate(ent)
    top.to_csv(PROC / "entidades_top.csv", index=False)
    by_class.to_csv(PROC / "entidades_por_classe.csv", index=False)
    plot_top(top)

    print("\n[ner] TOP 20 entidades (por nº de notícias):")
    for _, r in top.head(20).iterrows():
        print(f"  {int(r['docs']):3d} docs | {r['tipo']:6} | {r['exemplo']}")


if __name__ == "__main__":
    main()
