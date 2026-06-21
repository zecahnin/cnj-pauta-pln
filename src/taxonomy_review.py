"""
Etapa 5 (recoleta 2 anos) — Material CRU para revisão humana da taxonomia.

NÃO nomeia classes nem reescreve TAXONOMY/TAXONOMY_ANCHORS. Apenas expõe, para
cada tópico descoberto pelo BERTopic, o material que o dono precisa para decidir
os rótulos: termos c-TF-IDF, títulos representativos e (quando óbvia) a
correspondência com a taxonomia antiga de 6 meses.

Gera, para os tamanhos pedidos (default 10 e 15, conforme a parada da Etapa 5):
- reports/taxonomia_2anos_REVISAR.md
- reports/figures/08b_classes_2anos.png   (distribuição por tópico do melhor mts)

Reprodutível: mesmo SEED e mesma configuração de make_model() da Fase 4. Re-ajusta
o BERTopic (não toca nos artefatos persistidos por topics.py).

Uso:
    python src/taxonomy_review.py --sizes 10 15
"""

from __future__ import annotations

import tf_guard  # noqa: F401  (bloqueia TF antes de bertopic/umap)

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from topics import build_documents, make_model, evaluate  # reusa Fase 4
from text_utils import TAXONOMY, TAXONOMY_ANCHORS, get_stopwords

PROJECT_ROOT = Path(__file__).resolve().parents[1]
INTERIM = PROJECT_ROOT / "data" / "interim" / "noticias_limpo.parquet"
PROC = PROJECT_ROOT / "data" / "processed"
REPORTS = PROJECT_ROOT / "reports"
FIG = REPORTS / "figures"
SEED = 42
TOPN_TERMS = 15
N_TITLES = 5


def load_data() -> tuple[pd.DataFrame, np.ndarray]:
    df = pd.read_parquet(INTERIM)
    emb = np.load(PROC / "embeddings.npy")
    ids = np.load(PROC / "ids.npy")
    assert np.array_equal(ids, df["id"].to_numpy()), "ordem emb != parquet"
    assert emb.shape[0] == len(df), "n emb != n docs"
    return df, emb


def top_terms_ctfidf(model, topic: int, n: int) -> list[str]:
    """Top-n termos do tópico direto da matriz c-TF-IDF (garante n termos; o
    model.get_topic() trunca em top_n_words=10 e não propaga override)."""
    ctfidf = model.c_tf_idf_
    words = model.vectorizer_model.get_feature_names_out()
    labels = sorted(model.get_topics().keys())
    row = labels.index(topic)
    arr = np.asarray(ctfidf[row].todense()).ravel()
    top = arr.argsort()[::-1][:n]
    return [words[i] for i in top if arr[i] > 0]


def representative_titles(emb: np.ndarray, mask: np.ndarray,
                          titles: list[str], k: int) -> list[str]:
    """k títulos mais próximos do centróide do tópico (emb normalizados -> cosseno
    = produto interno). Critério honesto e reprodutível, sem conhecimento externo."""
    idx = np.where(mask)[0]
    if len(idx) == 0:
        return []
    centroid = emb[idx].mean(axis=0)
    centroid = centroid / (np.linalg.norm(centroid) + 1e-12)
    sims = emb[idx] @ centroid
    order = idx[np.argsort(-sims)]
    seen, out = set(), []
    for i in order:
        t = titles[i].strip()
        if t and t not in seen:
            seen.add(t)
            out.append(t)
        if len(out) >= k:
            break
    return out


def old_taxonomy_match(terms: list[str]) -> str | None:
    """Correspondência ÓBVIA com a taxonomia antiga (6 meses): só quando uma
    palavra-âncora antiga aparece entre os termos top do tópico novo."""
    joined = " ".join(terms).lower()
    hits = []
    for old_id, anchor in TAXONOMY_ANCHORS.items():
        if anchor.lower() in joined:
            hits.append(f"{TAXONOMY[old_id]} (âncora '{anchor}')")
    return "; ".join(hits) if hits else None


def fit_size(df, emb, docs, stop_words, size):
    np.random.seed(SEED)
    model = make_model(size, stop_words)
    model.top_n_words = TOPN_TERMS
    topics, _ = model.fit_transform(docs, embeddings=emb)
    metrics = evaluate(model, docs, topics)
    raw_outliers = sum(1 for t in topics if t == -1)
    topics_red = model.reduce_outliers(docs, topics, strategy="c-tf-idf")
    model.update_topics(docs, topics=topics_red,
                        vectorizer_model=model.vectorizer_model,
                        ctfidf_model=model.ctfidf_model)
    return model, np.array(topics_red), metrics, raw_outliers


def section_for_size(df, emb, docs, titles, stop_words, size) -> tuple[str, dict]:
    model, topics_red, metrics, raw_out = fit_size(df, emb, docs, stop_words, size)
    topic_ids = sorted(t for t in set(topics_red.tolist()) if t != -1)

    lines = []
    lines.append(f"## min_topic_size = {size}\n")
    lines.append(
        f"- Tópicos: **{metrics['n_topics']}** | coerência c_v: "
        f"**{metrics['coherence_cv']}** | diversidade: {metrics['diversity']} "
        f"| outliers brutos: {metrics['outlier_pct']}% "
        f"({raw_out} docs, reatribuídos por c-TF-IDF para a contagem abaixo)\n")

    for t in topic_ids:
        mask = topics_red == t
        count = int(mask.sum())
        terms = top_terms_ctfidf(model, t, TOPN_TERMS)
        reps = representative_titles(emb, mask, titles, N_TITLES)
        match = old_taxonomy_match(terms)

        lines.append(f"### Tópico {t} — {count} documentos\n")
        lines.append(f"**Top-{len(terms)} termos c-TF-IDF:** {', '.join(terms)}\n")
        lines.append("**Títulos mais representativos:**\n")
        for r in reps:
            lines.append(f"- {r}")
        lines.append("")
        if match:
            lines.append(f"**Correspondência com taxonomia antiga (6 meses):** {match}\n")
        else:
            lines.append("**Correspondência com taxonomia antiga (6 meses):** "
                         "_nenhuma óbvia — decidir do zero._\n")
        lines.append("")

    return "\n".join(lines), {"size": size, **metrics}


def make_figure_from_persisted() -> str:
    """Figura 08b a partir do doc_topics.parquet persistido por topics.py (melhor
    mts). Rotula por ID + top termos (os NOMES são decisão humana, não os invento)."""
    dt = pd.read_parquet(PROC / "doc_topics.parquet")
    info = pd.read_csv(PROC / "topic_info.csv")
    best = (PROC / "topics_best.txt").read_text()

    counts = dt["topic"].value_counts().sort_values(ascending=True)
    term_map = {}
    for _, row in info.iterrows():
        rep = str(row["Representation"])
        rep = rep.strip("[]").replace("'", "")
        top3 = ", ".join([w.strip() for w in rep.split(",")[:3]])
        term_map[int(row["Topic"])] = top3

    labels = [f"T{t}: {term_map.get(t, '')}" for t in counts.index]
    fig, ax = plt.subplots(figsize=(11, max(4, 0.5 * len(counts))))
    ax.barh(labels, counts.values, color="#6a3d9a")
    for i, v in enumerate(counts.values):
        ax.text(v + max(counts.values) * 0.01, i, str(v), va="center", fontsize=9)
    ax.set_xlabel("Nº de documentos")
    ax.set_title("Tópicos descobertos — corpus de 2 anos (rótulos a definir pelo humano)")
    plt.tight_layout()
    FIG.mkdir(parents=True, exist_ok=True)
    out = FIG / "08b_classes_2anos.png"
    plt.savefig(out, dpi=130)
    plt.close()
    return best.strip().replace("\n", " | ")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sizes", type=int, nargs="+", default=[10, 15])
    args = ap.parse_args()

    df, emb = load_data()
    docs = build_documents(df)
    titles = df["titulo"].fillna("").tolist()
    stop_words = get_stopwords()
    print(f"[revisar] {len(docs)} docs | sizes={args.sizes}")

    header = [
        "# Taxonomia — corpus de 2 anos (MATERIAL PARA REVISÃO HUMANA)\n",
        "Gerado por `src/taxonomy_review.py` a partir de execução real do BERTopic "
        "(mesma config da Fase 4, SEED=42). **Nada aqui é nomeado pela máquina.** "
        "Os tópicos abaixo são clusters não-supervisionados; cabe ao dono decidir "
        "(1) o nome de cada classe, (2) o número de classes (fundir/dividir), "
        "(3) a palavra-âncora de cada uma.\n",
        f"Corpus: **{len(docs)}** notícias, janela 2024-06 a 2026-06.\n",
        "A taxonomia antiga (6 meses, 10 classes) está apenas como pista de "
        "correspondência — ela vai desalinhar e isso é esperado.\n",
        "---\n",
    ]

    summaries = []
    body = []
    for size in args.sizes:
        print(f"[revisar] ajustando min_topic_size={size}...")
        sec, summ = section_for_size(df, emb, docs, titles, stop_words, size)
        body.append(sec)
        body.append("---\n")
        summaries.append(summ)

    print("[revisar] gerando figura 08b_classes_2anos.png...")
    best = make_figure_from_persisted()
    header.append(f"Figura `reports/figures/08b_classes_2anos.png` gerada do modelo "
                  f"persistido por topics.py ({best}).\n")

    REPORTS.mkdir(parents=True, exist_ok=True)
    out_md = REPORTS / "taxonomia_2anos_REVISAR.md"
    out_md.write_text("\n".join(header) + "\n" + "\n".join(body), encoding="utf-8")
    print(f"[revisar] salvo: {out_md}")
    print("[revisar] resumo por tamanho:")
    for s in summaries:
        print(f"  mts={s['size']}: n_topics={s['n_topics']} "
              f"c_v={s['coherence_cv']} outliers={s['outlier_pct']}%")


if __name__ == "__main__":
    main()
