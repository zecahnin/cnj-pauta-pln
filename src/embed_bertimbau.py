"""
Fase 6 (Modelo C) — embeddings BERTimbau, em PROCESSO SEPARADO.

Por que processo separado: o `classify.py` usa TensorFlow/Keras (Modelo B). O
BERTimbau usa PyTorch. Carregar TensorFlow + PyTorch no MESMO processo, depois
de o TF já ter treinado a MLP, provoca *segmentation fault* (conflito de runtime
nativo). Solução: este script (somente torch/transformers) computa os embeddings
de TODO o corpus e os salva em cache; o `classify.py` apenas LÊ o cache (sklearn,
sem torch) para a cabeça classificadora.

Embedding = mean-pooling da última camada de `neuralmind/bert-base-portuguese-cased`
(BERTimbau base; Souza et al., 2020) sobre `título + corpo` originais (modelo
cased: preserva caixa e acentos). Trunca em 512 subtokens.

Artefatos:
- data/processed/bertimbau_embeddings.npy   (N, 768) float32
- data/processed/bertimbau_ids.npy          ids alinhados às linhas

Uso:
    python src/embed_bertimbau.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
INTERIM = PROJECT_ROOT / "data" / "interim" / "noticias_limpo.parquet"
PROC = PROJECT_ROOT / "data" / "processed"
MODEL_NAME = "neuralmind/bert-base-portuguese-cased"


def main() -> None:
    import torch
    from transformers import AutoTokenizer, AutoModel

    df = pd.read_parquet(INTERIM)[["id", "titulo", "corpo_texto"]].sort_values("id")
    df = df.reset_index(drop=True)
    texts = (df["titulo"].fillna("") + ". " + df["corpo_texto"].fillna("")).tolist()
    ids = df["id"].to_numpy()
    print(f"[bert] {len(texts)} documentos | modelo {MODEL_NAME}")

    tok = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModel.from_pretrained(MODEL_NAME)
    model.eval()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    print(f"[bert] device={device}")

    embs = []
    bs = 16
    with torch.no_grad():
        for i in range(0, len(texts), bs):
            batch = texts[i:i + bs]
            enc = tok(batch, padding=True, truncation=True, max_length=512,
                      return_tensors="pt").to(device)
            out = model(**enc).last_hidden_state            # (B, T, H)
            mask = enc["attention_mask"].unsqueeze(-1).float()
            pooled = (out * mask).sum(1) / mask.sum(1).clamp(min=1e-9)
            embs.append(pooled.cpu().numpy())
            print(f"[bert]   {min(i + bs, len(texts))}/{len(texts)}", end="\r")
    embs = np.vstack(embs).astype("float32")
    print()

    PROC.mkdir(parents=True, exist_ok=True)
    np.save(PROC / "bertimbau_embeddings.npy", embs)
    np.save(PROC / "bertimbau_ids.npy", ids)
    print(f"[bert] salvo {embs.shape} -> {PROC / 'bertimbau_embeddings.npy'}")


if __name__ == "__main__":
    main()
