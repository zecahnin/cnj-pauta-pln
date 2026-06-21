"""
Fase 4 (parte 1) — Geração de embeddings das notícias.

Escolha do modelo
-----------------
`sentence-transformers/paraphrase-multilingual-mpnet-base-v2`.

Justificativa:
- **Multilíngue com forte suporte ao português**: treinado em pares
  paralelos de 50+ idiomas, é um dos modelos sentence-transformers com melhor
  desempenho em similaridade semântica em pt-BR sem fine-tuning.
- **Qualidade > velocidade aqui**: o corpus tem ~1k documentos, então o custo
  de embedding (base, 768 dim) é irrelevante em CPU, mas a separabilidade dos
  clusters melhora frente ao MiniLM (384 dim).
- **Embeddings normalizados** (cosine) combinam com UMAP/HDBSCAN na Fase 4.

O que é embeddado: `titulo + ". " + corpo_texto`. O título carrega forte sinal
de pauta; o corpo é truncado pelo `max_seq_length` do modelo (estendido para
256 tokens para capturar o lead da matéria).

Saída: `data/processed/embeddings.npy` (float32, alinhado a `ids.npy`).

Uso:
    python src/embed.py
    python src/embed.py --model sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = PROJECT_ROOT / "data" / "interim" / "noticias_limpo.parquet"
PROC_DIR = PROJECT_ROOT / "data" / "processed"

DEFAULT_MODEL = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
MAX_SEQ_LENGTH = 256
SEED = 42


def build_documents(df: pd.DataFrame) -> list[str]:
    """Concatena título e corpo para embedding (título reforça a pauta)."""
    return [
        f"{t}. {b}".strip()
        for t, b in zip(df["titulo"].fillna(""), df["corpo_texto"].fillna(""))
    ]


def compute_embeddings(docs: list[str], model_name: str = DEFAULT_MODEL,
                       batch_size: int = 32) -> np.ndarray:
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer(model_name)
    model.max_seq_length = MAX_SEQ_LENGTH
    emb = model.encode(
        docs,
        batch_size=batch_size,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True,   # cosine via produto interno
    )
    return emb.astype(np.float32)


def main() -> None:
    ap = argparse.ArgumentParser(description="Gera embeddings das notícias.")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--batch-size", type=int, default=32)
    args = ap.parse_args()

    df = pd.read_parquet(INPUT_PATH)
    docs = build_documents(df)
    print(f"[embed] {len(docs)} documentos | modelo: {args.model}")

    emb = compute_embeddings(docs, args.model, args.batch_size)
    print(f"[embed] shape: {emb.shape}")

    PROC_DIR.mkdir(parents=True, exist_ok=True)
    np.save(PROC_DIR / "embeddings.npy", emb)
    np.save(PROC_DIR / "ids.npy", df["id"].to_numpy())
    with (PROC_DIR / "embeddings_model.txt").open("w") as fh:
        fh.write(f"{args.model}\nmax_seq_length={MAX_SEQ_LENGTH}\n"
                 f"shape={emb.shape}\nnormalized=True\n")
    print(f"[embed] salvo em {PROC_DIR / 'embeddings.npy'}")


if __name__ == "__main__":
    main()
