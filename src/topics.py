"""
Fase 4 (parte 2) — Modelagem de tópicos com BERTopic.

Pipeline BERTopic:
    embeddings (Fase 1/embed.py) -> UMAP (redução) -> HDBSCAN (clusterização)
    -> c-TF-IDF (representação dos tópicos por termos).

Avaliação (números reais, sem fabricação):
- **Coerência c_v** (gensim CoherenceModel) — média sobre os tópicos.
- **Diversidade de tópicos** — fração de termos únicos entre os top-N de todos
  os tópicos (Dieng et al., 2020).
- **% de outliers** — proporção de documentos no tópico -1 (ruído do HDBSCAN).

Varre 3 valores de `min_topic_size` (10, 15, 20) e escolhe o melhor por
coerência c_v (com a % de outliers reportada para contexto).

Artefatos salvos em `data/processed/`:
- `bertopic_model/`           modelo BERTopic (pickle)
- `topic_info.csv`            tópico -> tamanho -> termos
- `doc_topics.parquet`        id, data, tópico atribuído por documento
- `topic_eval.csv`            métricas por min_topic_size

Uso:
    python src/topics.py
    python src/topics.py --sizes 10 15 20
"""

from __future__ import annotations

# Bloqueia TensorFlow ANTES de importar bertopic/umap (evita segfault
# TF+torch+numba; ver src/tf_guard.py). Deve vir antes de qualquer import pesado.
import tf_guard  # noqa: F401  (efeito colateral no import)

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
INTERIM = PROJECT_ROOT / "data" / "interim" / "noticias_limpo.parquet"
PROC = PROJECT_ROOT / "data" / "processed"
SEED = 42

# Taxonomia, âncoras e stopwords vêm da fonte canônica TF-free (text_utils), para
# que descoberta (Fase 4), deriva (Fase 5) e classificação (Fase 6) compartilhem
# exatamente os mesmos rótulos e vocabulário. A atribuição de classe por
# documento gravada aqui é um RÓTULO FRACO (vem do clustering, não de humano);
# a avaliação formal é a Fase 6, contra o gold humano.
from text_utils import (  # noqa: E402
    DOMAIN_STOP, TAXONOMY, TAXONOMY_ANCHORS, get_stopwords)


def load_data() -> tuple[pd.DataFrame, np.ndarray]:
    df = pd.read_parquet(INTERIM)
    emb = np.load(PROC / "embeddings.npy")
    ids = np.load(PROC / "ids.npy")
    assert np.array_equal(ids, df["id"].to_numpy()), \
        "ordem de embeddings != ordem do parquet"
    assert emb.shape[0] == len(df), "nº de embeddings != nº de documentos"
    return df, emb


def build_documents(df: pd.DataFrame) -> list[str]:
    return [f"{t}. {b}".strip()
            for t, b in zip(df["titulo"].fillna(""), df["corpo_texto"].fillna(""))]


def make_model(min_topic_size: int, stop_words: list[str]):
    from bertopic import BERTopic
    from bertopic.vectorizers import ClassTfidfTransformer
    from hdbscan import HDBSCAN
    from sklearn.feature_extraction.text import CountVectorizer
    from umap import UMAP

    # n_neighbors=10 enfatiza estrutura LOCAL: o corpus é semanticamente
    # homogêneo (registro institucional; cosseno médio ~0.69), então vizinhança
    # menor é necessária para o HDBSCAN não colapsar tudo em 1-2 clusters.
    umap_model = UMAP(n_neighbors=10, n_components=5, min_dist=0.0,
                      metric="cosine", random_state=SEED)
    # cluster_selection_method="leaf": com corpus homogêneo, "eom" (excess of
    # mass) seleciona pouquíssimos clusters gigantes; "leaf" recupera os
    # subtópicos finos da pauta (custo: mais outliers, tratados depois).
    hdbscan_model = HDBSCAN(min_cluster_size=min_topic_size,
                            metric="euclidean", cluster_selection_method="leaf",
                            prediction_data=True)
    vectorizer_model = CountVectorizer(stop_words=stop_words,
                                       ngram_range=(1, 2), min_df=3)
    ctfidf_model = ClassTfidfTransformer(reduce_frequent_words=True)

    return BERTopic(
        embedding_model=None,            # usamos embeddings pré-computados
        language="multilingual",         # NÃO remove acentos (default "english" sim)
        umap_model=umap_model,
        hdbscan_model=hdbscan_model,
        vectorizer_model=vectorizer_model,
        ctfidf_model=ctfidf_model,
        calculate_probabilities=False,
        verbose=False,
    )


def evaluate(model, docs: list[str], topics: list[int],
             topn: int = 10) -> dict:
    """Coerência c_v, diversidade e % outliers — todos sobre execução real."""
    from gensim.corpora import Dictionary
    from gensim.models import CoherenceModel

    # Tokeniza com o MESMO analyzer do vectorizer (inclui bigramas), para que os
    # termos dos tópicos (que podem ser bigramas) casem com os tokens dos textos.
    analyzer = model.vectorizer_model.build_analyzer()
    tokens = [analyzer(d) for d in docs]
    dictionary = Dictionary(tokens)

    topic_ids = sorted(t for t in set(topics) if t != -1)
    topic_words = []
    for t in topic_ids:
        words = [w for w, _ in model.get_topic(t)][:topn]
        words = [w for w in words if w]  # remove vazios
        if words:
            topic_words.append(words)

    if len(topic_words) < 2:
        coherence = float("nan")
    else:
        cm = CoherenceModel(topics=topic_words, texts=tokens,
                            dictionary=dictionary, coherence="c_v", topn=topn)
        coherence = float(cm.get_coherence())

    # Diversidade: termos únicos / total entre os top-N de todos os tópicos.
    all_words = [w for ws in topic_words for w in ws]
    diversity = len(set(all_words)) / len(all_words) if all_words else float("nan")

    outlier_pct = 100.0 * sum(1 for t in topics if t == -1) / len(topics)

    return {
        "n_topics": len(topic_ids),
        "coherence_cv": round(coherence, 4),
        "diversity": round(diversity, 4),
        "outlier_pct": round(outlier_pct, 2),
    }


def run_sweep(sizes: list[int]) -> None:
    df, emb = load_data()
    docs = build_documents(df)
    stop_words = get_stopwords()
    print(f"[topics] {len(docs)} docs | {len(stop_words)} stopwords | "
          f"sizes={sizes}")

    results = []
    fitted = {}
    for mts in sizes:
        np.random.seed(SEED)
        model = make_model(mts, stop_words)
        topics, _ = model.fit_transform(docs, embeddings=emb)
        metrics = evaluate(model, docs, topics)
        metrics["min_topic_size"] = mts
        results.append(metrics)
        fitted[mts] = (model, topics)
        print(f"[topics] min_topic_size={mts}: "
              f"n_topics={metrics['n_topics']} "
              f"c_v={metrics['coherence_cv']} "
              f"diversity={metrics['diversity']} "
              f"outliers={metrics['outlier_pct']}%")

    eval_df = pd.DataFrame(results)[
        ["min_topic_size", "n_topics", "coherence_cv", "diversity", "outlier_pct"]]
    PROC.mkdir(parents=True, exist_ok=True)
    eval_df.to_csv(PROC / "topic_eval.csv", index=False)
    print("\n[topics] tabela de avaliação:")
    print(eval_df.to_string(index=False))

    # Seleção: maior coerência c_v (desempate: menor % outliers).
    eval_df_valid = eval_df.dropna(subset=["coherence_cv"])
    best_row = eval_df_valid.sort_values(
        ["coherence_cv", "outlier_pct"], ascending=[False, True]).iloc[0]
    best_mts = int(best_row["min_topic_size"])
    print(f"\n[topics] MELHOR min_topic_size = {best_mts} "
          f"(c_v={best_row['coherence_cv']}, "
          f"outliers={best_row['outlier_pct']}%)")

    model, topics = fitted[best_mts]
    docs = build_documents(df)
    _persist(df, docs, model, topics, best_mts)


def verify_taxonomy(model, topic_ids) -> bool:
    """Confere que a ordem dos tópicos casa com TAXONOMY_ANCHORS.

    O BERTopic numera os tópicos por tamanho; com SEED fixo a ordem é estável,
    mas mudanças de versão de UMAP/HDBSCAN poderiam reordená-los. Sem esta
    checagem, gravaríamos rótulos temáticos trocados. Retorna True se todas as
    âncoras casarem; caso contrário imprime os desvios e retorna False.
    """
    ok = True
    for tid in topic_ids:
        if tid == -1 or tid not in TAXONOMY_ANCHORS:
            continue
        terms = " ".join(w for w, _ in model.get_topic(tid)).lower()
        anchor = TAXONOMY_ANCHORS[tid].lower()
        if anchor not in terms:
            ok = False
            print(f"[topics][AVISO] tópico {tid} não contém a âncora "
                  f"'{anchor}' — TAXONOMY pode estar desalinhada. "
                  f"Termos: {terms[:80]}")
    if ok:
        print("[topics] taxonomia verificada: ordem dos tópicos casa com "
              "as âncoras esperadas.")
    return ok


def _persist(df, docs, model, topics, best_mts: int) -> None:
    # Redução de outliers para a análise temporal (Fase 5): reatribui os
    # documentos do tópico -1 ao tópico mais próximo via c-TF-IDF. A taxa BRUTA
    # de outliers (qualidade do clustering) já foi reportada em topic_eval.csv.
    raw_outliers = sum(1 for t in topics if t == -1)
    topics_reduced = model.reduce_outliers(docs, topics, strategy="c-tf-idf")
    model.update_topics(docs, topics=topics_reduced,
                        vectorizer_model=model.vectorizer_model,
                        ctfidf_model=model.ctfidf_model)
    red_outliers = sum(1 for t in topics_reduced if t == -1)
    print(f"[topics] outliers: {raw_outliers} brutos -> {red_outliers} "
          f"após reduce_outliers (c-TF-IDF)")

    # Tabela tópico -> tamanho -> termos
    info = model.get_topic_info()
    info.to_csv(PROC / "topic_info.csv", index=False)

    # Verifica que a numeração dos tópicos casa com a TAXONOMY antes de gravar
    # os rótulos temáticos (evita gravar classe errada se a ordem mudar).
    verify_taxonomy(model, sorted(set(topics_reduced)))

    # Atribuição por documento (tópico bruto, reduzido e classe temática nomeada).
    # `classe_tematica` é o RÓTULO FRACO usado como alvo no treino supervisionado
    # da Fase 6 (consolidação não-supervisionada -> espaço de rótulos).
    doc_topics = pd.DataFrame({
        "id": df["id"].to_numpy(),
        "data_publicacao": df["data_publicacao"].to_numpy(),
        "mes": df["mes"].to_numpy(),
        "titulo": df["titulo"].to_numpy(),
        "topic_raw": topics,
        "topic": topics_reduced,
        "classe_id": topics_reduced,
        "classe_tematica": [TAXONOMY.get(t, "Outros") for t in topics_reduced],
    })
    doc_topics.to_parquet(PROC / "doc_topics.parquet", index=False)
    print("[topics] distribuição de classes temáticas (rótulo fraco):")
    print(doc_topics["classe_tematica"].value_counts().to_string())

    # Modelo (pickle, sem o embedding model pesado)
    model_dir = PROC / "bertopic_model"
    model.save(str(model_dir), serialization="pickle",
               save_embedding_model=False)

    with (PROC / "topics_best.txt").open("w") as fh:
        fh.write(f"best_min_topic_size={best_mts}\n"
                 f"n_topics={len([t for t in set(topics) if t != -1])}\n")

    print(f"[topics] salvos: topic_info.csv, doc_topics.parquet, "
          f"bertopic_model/ (min_topic_size={best_mts})")


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Modelagem de tópicos BERTopic.")
    ap.add_argument("--sizes", type=int, nargs="+", default=[10, 15, 20])
    return ap.parse_args()


if __name__ == "__main__":
    a = parse_args()
    run_sweep(a.sizes)
