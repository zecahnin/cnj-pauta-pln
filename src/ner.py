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

Artefatos:
- data/processed/entidades.parquet        (uma linha por entidade encontrada)
- data/processed/entidades_top.csv        top entidades agregadas
- data/processed/entidades_por_classe.csv top entidades por classe temática
- reports/figures/16_top_entidades.png

Uso:
    python src/ner.py
    python src/ner.py --max-chars 1500
"""

from __future__ import annotations

import argparse
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
INTERIM = PROJECT_ROOT / "data" / "interim" / "noticias_limpo.parquet"
PROC = PROJECT_ROOT / "data" / "processed"
FIG = PROJECT_ROOT / "reports" / "figures"
MODEL_NAME = "rhaymison/ner-portuguese-br-bert-cased"


def _norm_key(s: str) -> str:
    """Chave de agregação: minúsculas, sem acento, espaços colapsados."""
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return " ".join(s.lower().split())


def extract_entities(max_chars: int) -> pd.DataFrame:
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
          f"device={'cuda' if device == 0 else 'cpu'} | max_chars={max_chars}")
    ner = pipeline("ner", model=MODEL_NAME, aggregation_strategy="simple",
                   device=device)

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
                surface = str(e["word"]).strip()
                # Descarta fragmentos de subpalavra mal mesclados ("##J",
                # "##dor"), curtos demais ou sem letra (ruído do tokenizer).
                if "##" in surface or len(_norm_key(surface)) < 3:
                    continue
                if not any(ch.isalpha() for ch in surface):
                    continue
                rows.append({
                    "id": int(r["id"]),
                    "classe_id": int(r["classe_id"]),
                    "classe_tematica": r["classe_tematica"],
                    "entidade": surface,
                    "entidade_key": _norm_key(surface),
                    "tipo": e["entity_group"],
                    "score": round(float(e["score"]), 4),
                })
        print(f"[ner]   {min(i + bs, len(texts))}/{len(texts)}", end="\r")
    print()
    ent = pd.DataFrame(rows)
    print(f"[ner] {len(ent)} entidades extraídas | tipos: "
          f"{ent['tipo'].value_counts().to_dict()}")
    return ent


def aggregate(ent: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    # Top entidades por nº de DOCUMENTOS distintos (evita inflar por repetição).
    top = (ent.groupby(["entidade_key", "tipo"])
              .agg(docs=("id", "nunique"),
                   ocorrencias=("id", "size"),
                   exemplo=("entidade", "first"))
              .reset_index()
              .sort_values("docs", ascending=False))

    # Top entidade por classe temática
    by_class = (ent.groupby(["classe_tematica", "entidade_key"])
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
        ["#2c6fbb", "#3a9a6d", "#bb5d2c", "#8a5dbb", "#bb2c4f", "#777777"])}
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
    args = ap.parse_args()

    ent = extract_entities(args.max_chars)
    PROC.mkdir(parents=True, exist_ok=True)
    ent.to_parquet(PROC / "entidades.parquet", index=False)
    print(f"[ner] salvo -> {PROC / 'entidades.parquet'}")

    top, by_class = aggregate(ent)
    top.to_csv(PROC / "entidades_top.csv", index=False)
    by_class.to_csv(PROC / "entidades_por_classe.csv", index=False)
    plot_top(top)

    print("\n[ner] TOP 15 entidades (por nº de notícias):")
    for _, r in top.head(15).iterrows():
        print(f"  {int(r['docs']):3d} docs | {r['tipo']:6} | {r['exemplo']}")


if __name__ == "__main__":
    main()
