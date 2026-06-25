"""
Fase 6 (ataque aos outliers) — amostragem ATIVA de outliers do BERTopic para
rotulação humana.

Motivação (medida nos dados): 56% do corpus (e 56% do gold) são *outliers* do
BERTopic — docs que ele não conseguiu agrupar (topic_raw == -1). O pool de treino
NÃO contém nenhum doc desse tipo, e por isso o MLP cai de F1 0.70 (docs
clusterizados) para 0.58 (outliers). Rotular à mão ~150 outliers e injetá-los no
treino é a alavanca de maior retorno (sugestão #2). Este script SELECIONA quais
rotular; a rotulação em si é humana.

Estratégia de seleção (estratificada por classe + informativa):
1. Espaço semântico = embeddings BERTimbau (cache, MESMAS features do Modelo C),
   CENTRALIZADOS pela média global e L2-normalizados (produto interno = cosseno).
   A centralização remove a anisotropia do mean-pooling do BERT (sem ela todos os
   cossenos colam em ~0.95 e a classe mais próxima fica pouco discriminativa); é o
   mesmo espírito do StandardScaler usado na cabeça do Modelo C.
2. Centroide de cada classe (0-29) = média dos embeddings (normalizados) dos docs
   CLUSTERIZADOS (topic_raw != -1) daquela classe.
3. Para cada outlier (topic_raw == -1 e FORA do gold): similaridade a todos os 30
   centroides -> classe mais próxima (sim1), 2ª mais próxima (sim2) e
   margem = sim1 - sim2 (baixa margem = ambíguo entre dois temas).
4. Estratificação: cada outlier é alocado à sua classe mais próxima; a cota total
   (~N) é distribuída entre as classes proporcional à população de outliers de
   cada uma, com PISO por classe presente — garante cobertura de todos os temas
   (e não só dos dominantes, como Gestão).
5. Informatividade DENTRO da classe: em vez de pegar só os mais prototípicos
   (fáceis/redundantes), seleciona por espaçamento uniforme ao longo da lista
   ordenada por sim1 — cobre o intervalo do mais prototípico ao mais ambíguo,
   que é o que de fato agrega sinal novo ao treino.

Saídas:
- reports/outliers_template.csv : id, titulo, trecho (400 chars), classe (VAZIA)
  -> rotulação humana CEGA (0-29, 'Outros' ou 'indefinido'). NÃO expõe a classe
     sugerida, para evitar viés de ancoragem (mesmo protocolo do gold_template).
- reports/outliers_diagnostico.csv : id, classe_sugerida, sim1, sim2, margem
  -> APENAS para auditoria/reprodutibilidade. NÃO deve ser usado na rotulação.

Uso:
    python src/sample_outliers.py            # ~150 outliers
    python src/sample_outliers.py --n 200
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))
from text_utils import TAXONOMY  # noqa: E402

INTERIM = PROJECT_ROOT / "data" / "interim" / "noticias_limpo.parquet"
PROC = PROJECT_ROOT / "data" / "processed"
GOLD = PROJECT_ROOT / "reports" / "gold_labels.csv"
TEMPLATE = PROJECT_ROOT / "reports" / "outliers_template.csv"
DIAG = PROJECT_ROOT / "reports" / "outliers_diagnostico.csv"

SEED = 42
N_CLASSES = len(TAXONOMY)
TRECHO_CHARS = 400
FLOOR_PER_CLASS = 2  # piso de docs por classe presente (cobertura temática)


def center_and_normalize(mat: np.ndarray) -> np.ndarray:
    """Centraliza pela média global (remove anisotropia do BERT) e L2-normaliza,
    de modo que o produto interno entre dois vetores seja o cosseno."""
    mat = mat - mat.mean(axis=0, keepdims=True)
    norms = np.linalg.norm(mat, axis=1, keepdims=True)
    return mat / np.clip(norms, 1e-9, None)


def class_centroids(emb_unit: np.ndarray, id2row: dict, clustered: pd.DataFrame
                    ) -> np.ndarray:
    """Centroide (vetor unitário) de cada classe 0-29 a partir dos docs
    clusterizados. Classes sem docs recebem vetor nulo (sim=0 sempre)."""
    cent = np.zeros((N_CLASSES, emb_unit.shape[1]), dtype="float32")
    for c in range(N_CLASSES):
        ids = clustered.loc[clustered["classe_id"] == c, "id"]
        rows = [id2row[int(i)] for i in ids if int(i) in id2row]
        if rows:
            v = emb_unit[rows].mean(axis=0)
            cent[c] = v / max(np.linalg.norm(v), 1e-9)
    return cent


def allocate_quota(nearest: np.ndarray, n_target: int) -> dict[int, int]:
    """Distribui ~n_target vagas entre as classes presentes: piso por classe +
    resto proporcional à população de outliers (largest remainder)."""
    counts = Counter(int(c) for c in nearest)
    present = sorted(counts)
    quota = {c: min(FLOOR_PER_CLASS, counts[c]) for c in present}
    remaining = n_target - sum(quota.values())
    if remaining > 0:
        tot = sum(counts[c] for c in present)
        frac = {c: remaining * counts[c] / tot for c in present}
        base = {c: int(frac[c]) for c in present}
        for c in present:
            quota[c] += base[c]
        leftover = remaining - sum(base.values())
        for c in sorted(present, key=lambda c: frac[c] - int(frac[c]),
                        reverse=True)[:leftover]:
            quota[c] += 1
    # respeita a disponibilidade real de cada classe
    return {c: min(quota[c], counts[c]) for c in present}


def pick_spread(rows_sorted: list[int], k: int) -> list[int]:
    """Seleciona k índices espaçados uniformemente ao longo da lista já ordenada
    por sim1 (do mais prototípico ao mais ambíguo)."""
    if k >= len(rows_sorted):
        return rows_sorted
    sel = np.unique(np.linspace(0, len(rows_sorted) - 1, k).round().astype(int))
    return [rows_sorted[j] for j in sel]


def main() -> None:
    ap = argparse.ArgumentParser(description="Amostragem ativa de outliers do "
                                             "BERTopic para rotulação humana.")
    ap.add_argument("--n", type=int, default=150, help="Nº alvo de outliers (~150).")
    ap.add_argument("--seed", type=int, default=SEED)
    args = ap.parse_args()
    rng = np.random.RandomState(args.seed)

    # --- dados ---
    dt = pd.read_parquet(PROC / "doc_topics.parquet")[["id", "topic_raw", "classe_id"]]
    txt = pd.read_parquet(INTERIM)[["id", "titulo", "corpo_texto"]]
    gold_ids = set(pd.read_csv(GOLD)["id"])
    emb = np.load(PROC / "bertimbau_embeddings.npy")
    emb_ids = np.load(PROC / "bertimbau_ids.npy")
    id2row = {int(i): r for r, i in enumerate(emb_ids)}
    emb_unit = center_and_normalize(emb)

    clustered = dt[dt["topic_raw"] != -1]
    cent = class_centroids(emb_unit, id2row, clustered)

    # outliers fora do gold e com embedding
    outliers = dt[(dt["topic_raw"] == -1) & (~dt["id"].isin(gold_ids))].copy()
    outliers = outliers[outliers["id"].isin(id2row.keys())].reset_index(drop=True)
    rows = np.array([id2row[int(i)] for i in outliers["id"]])
    sims = emb_unit[rows] @ cent.T                       # (n_out, 30) cosseno
    order = np.argsort(-sims, axis=1)
    nearest = order[:, 0]
    sim1 = sims[np.arange(len(sims)), order[:, 0]]
    sim2 = sims[np.arange(len(sims)), order[:, 1]]
    outliers["nearest"] = nearest
    outliers["sim1"] = sim1
    outliers["sim2"] = sim2
    outliers["margem"] = sim1 - sim2

    print(f"[out] outliers amostráveis (fora do gold): {len(outliers)} | "
          f"alvo N={args.n}")

    # --- estratificação + seleção informativa ---
    quota = allocate_quota(nearest, args.n)
    chosen_idx: list[int] = []
    for c in sorted(quota):
        sub = outliers.index[outliers["nearest"] == c].tolist()
        sub_sorted = sorted(sub, key=lambda i: outliers.at[i, "sim1"], reverse=True)
        chosen_idx.extend(pick_spread(sub_sorted, quota[c]))

    sample = outliers.loc[chosen_idx].merge(txt, on="id")
    sample = sample.sample(frac=1, random_state=rng)     # embaralha (anti-ancoragem)

    # --- template CEGO (4 colunas, classe vazia) ---
    template = pd.DataFrame({
        "id": sample["id"].to_numpy(),
        "titulo": sample["titulo"].to_numpy(),
        "trecho": sample["corpo_texto"].fillna("").str[:TRECHO_CHARS].to_numpy(),
        "classe": "",   # <-- VAZIA: rotular à mão (0-29, 'Outros' ou 'indefinido')
    })
    template.to_csv(TEMPLATE, index=False)

    # --- diagnóstico (auditoria; NÃO usar na rotulação) ---
    diag = pd.DataFrame({
        "id": sample["id"].to_numpy(),
        "classe_sugerida_id": sample["nearest"].to_numpy(),
        "classe_sugerida": [TAXONOMY[int(c)] for c in sample["nearest"]],
        "sim1": sample["sim1"].round(4).to_numpy(),
        "sim2": sample["sim2"].round(4).to_numpy(),
        "margem": sample["margem"].round(4).to_numpy(),
    }).sort_values("classe_sugerida_id")
    diag.to_csv(DIAG, index=False)

    # --- resumo ---
    dist = Counter(int(c) for c in sample["nearest"])
    print(f"[out] selecionados: {len(template)} (cobrindo {len(dist)}/30 classes)")
    print(f"[out] template CEGO -> {TEMPLATE}")
    print(f"[out] diagnóstico   -> {DIAG}")
    print("[out] distribuição por classe sugerida (classe: n | sim1 médio):")
    for c in sorted(dist):
        m = sample.loc[sample["nearest"] == c, "sim1"].mean()
        print(f"      {c:>2} {TAXONOMY[c][:34]:<34} n={dist[c]:>2} | sim1~{m:.3f}")


if __name__ == "__main__":
    main()
