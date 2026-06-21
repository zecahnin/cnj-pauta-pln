"""
Fase 5 — Deriva temporal da pauta.

A partir das atribuições de tópico por documento (Fase 4), analisa como a pauta
se distribui e se desloca no tempo:
- matriz tópico × semana (contagens e participação relativa);
- detecção de picos por tópico (scipy.signal.find_peaks sobre z-score);
- evidência de cada pico: manchetes reais daquela semana naquele tópico;
- cruzamento com eventos verificáveis (`reports/eventos_cnj.csv`).

Princípio de honestidade: os "eventos" usados para anotação são, sempre que
possível, **ancorados nas próprias notícias** (cujas URLs são verificáveis),
e não em conhecimento externo não auditável.

Artefatos:
- `data/processed/topic_week_counts.csv`   matriz tópico × semana
- `data/processed/topic_peaks.csv`         picos + manchetes de evidência

Uso:
    python src/drift.py
    python src/drift.py --freq W --z 1.5
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROC = PROJECT_ROOT / "data" / "processed"

# Rótulos dos tópicos = taxonomia temática da Fase 4. Reusa a fonte canônica
# (src/topics.py::TAXONOMY) para garantir que rótulos da deriva temporal e da
# classificação supervisionada nunca divirjam.
sys.path.insert(0, str(PROJECT_ROOT / "src"))
from topics import TAXONOMY as TOPIC_LABELS  # noqa: E402


def load_doc_topics(use_reduced: bool = False) -> pd.DataFrame:
    """Carrega atribuições de tópico.

    Por padrão usa as atribuições BRUTAS do HDBSCAN (`topic_raw`), removendo
    outliers (-1): são os membros de cluster de alta confiança, o que torna os
    picos e suas manchetes de evidência fiéis ao tema. Com `use_reduced=True`,
    usa as atribuições pós-`reduce_outliers` (cobertura total, porém com ruído).
    """
    df = pd.read_parquet(PROC / "doc_topics.parquet")
    df["data_publicacao"] = pd.to_datetime(df["data_publicacao"])
    col = "topic" if use_reduced else "topic_raw"
    df["topic"] = df[col]
    if not use_reduced:
        df = df[df["topic"] != -1].copy()
    df["label"] = df["topic"].map(TOPIC_LABELS).fillna(df["topic"].astype(str))
    return df


def topic_time_matrix(df: pd.DataFrame, freq: str = "W") -> pd.DataFrame:
    """Contagens tópico × período (linhas=período, colunas=tópico)."""
    g = (df.assign(per=df["data_publicacao"].dt.to_period(freq))
           .groupby(["per", "topic"]).size().unstack(fill_value=0).sort_index())
    g.index = g.index.to_timestamp()
    return g


def detect_peaks(mat: pd.DataFrame, z_thresh: float = 1.5,
                 min_count: int = 4) -> pd.DataFrame:
    """Picos por tópico via z-score; exige contagem mínima absoluta."""
    from scipy.signal import find_peaks

    rows = []
    for topic in mat.columns:
        s = mat[topic].astype(float)
        if s.sum() < min_count:
            continue
        mu, sd = s.mean(), s.std(ddof=0)
        if sd == 0:
            continue
        z = (s - mu) / sd
        idx, _ = find_peaks(s.values, height=max(min_count, mu + z_thresh * sd),
                            distance=2)
        for i in idx:
            rows.append({
                "topic": int(topic),
                "label": TOPIC_LABELS.get(int(topic), str(topic)),
                "periodo": mat.index[i].date().isoformat(),
                "contagem": int(s.values[i]),
                "z": round(float(z.values[i]), 2),
            })
    return pd.DataFrame(rows).sort_values(["topic", "periodo"])


def peak_evidence(df: pd.DataFrame, peaks: pd.DataFrame, freq: str = "W",
                  k: int = 3) -> pd.DataFrame:
    """Anexa manchetes reais (evidência) de cada pico."""
    ev = []
    for _, p in peaks.iterrows():
        per = pd.Period(p["periodo"], freq=freq)
        mask = ((df["topic"] == p["topic"]) &
                (df["data_publicacao"].dt.to_period(freq) == per))
        titles = df.loc[mask, "titulo"].head(k).tolist()
        ev.append(" | ".join(titles))
    out = peaks.copy()
    out["manchetes_evidencia"] = ev
    return out


def run(freq: str, z: float, use_reduced: bool = False) -> None:
    df = load_doc_topics(use_reduced=use_reduced)
    mat = topic_time_matrix(df, freq=freq)
    mat.to_csv(PROC / "topic_week_counts.csv")
    print(f"[drift] matriz {mat.shape[0]} períodos × {mat.shape[1]} tópicos "
          f"(freq={freq})")

    peaks = detect_peaks(mat, z_thresh=z)
    peaks = peak_evidence(df, peaks, freq=freq)
    peaks.to_csv(PROC / "topic_peaks.csv", index=False)
    print(f"[drift] {len(peaks)} picos detectados (z>={z})")
    for _, p in peaks.iterrows():
        print(f"  T{p['topic']} [{p['label']}] {p['periodo']} "
              f"n={p['contagem']} z={p['z']}")
        print(f"      ev: {p['manchetes_evidencia'][:140]}")


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Análise de deriva temporal.")
    ap.add_argument("--freq", default="W", help="Frequência pandas (W, M).")
    ap.add_argument("--z", type=float, default=1.5, help="Limiar de z-score.")
    ap.add_argument("--use-reduced", action="store_true",
                    help="Usa tópicos pós-reduce_outliers (default: brutos).")
    return ap.parse_args()


if __name__ == "__main__":
    a = parse_args()
    run(a.freq, a.z, use_reduced=a.use_reduced)
