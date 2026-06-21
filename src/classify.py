"""
Fase 6 — NÚCLEO: classificação temática supervisionada.

Objetivo (avaliação formal do projeto): aprender a **taxonomia temática** da
Fase 4 a partir de features lexicais/semânticas INDEPENDENTES e medir a
concordância com um **gold set anotado à mão**. Três modelos, todos cobrindo
técnicas do curso:

    A. Naive Bayes      — TF-IDF (BoW ponderado) + MultinomialNB        (baseline)
    B. MLP (Keras)      — TF-IDF -> Dense/ReLU/Dropout/softmax + Adam   (DL, núcleo)
    C. BERTimbau        — embeddings BERT-pt (mean-pooling) + LogReg    (transformer)

Protocolo de avaliação (sem vazamento):
- **Rótulo fraco** = `topic_raw` do BERTopic (alta confiança; exclui outliers -1).
- O **gold humano** (`reports/gold_labels.csv`) é REMOVIDO do conjunto de treino,
  pois 162/173 documentos do gold também têm rótulo fraco — treinar neles
  inflaria a métrica externa.
- **Regime interno** (aprende o rótulo fraco): split estratificado
  treino/validação/teste sobre a "pool" (529 docs com rótulo fraco e fora do
  gold). Mede se o modelo aprende a taxonomia a partir de features independentes.
- **Regime externo** (vs gold humano): cada modelo é treinado na pool INTEIRA e
  prediz os 173 documentos do gold; reporta accuracy, F1-macro, Cohen's kappa e
  matriz de confusão contra a anotação humana. Esta é a validação de cabeçalho.

Análise de overfit/underfit (peça central do Módulo 2): a MLP é treinada em duas
variantes — COM e SEM Dropout — e as curvas de perda/acurácia treino×validação
são plotadas lado a lado para demonstrar o overfitting e como o Dropout o atenua.

Gera também `reports/gold_template.csv`: amostra estratificada por classe
(~8-10/classe) restrita à janela recente (default 18 meses, Parada 1), com a
coluna `classe` VAZIA, para anotação manual cega (protocolo reprodutível).
`--template-only` gera só o template e para (não roda a classificação).

Artefatos:
- reports/gold_template.csv
- data/processed/classify_metrics.json
- data/processed/bertimbau_embeddings.npy (+ ids)
- reports/figures/14_overfit_mlp.png
- reports/figures/15_confusion_gold.png

Uso:
    python src/classify.py
    python src/classify.py --epochs 60 --skip-bert
"""

from __future__ import annotations

import argparse
import json
import os
import random
import sys
from pathlib import Path

import numpy as np
import pandas as pd

# NÃO importar topics/drift aqui: eles ativam o tf_guard (bloqueiam TensorFlow).
# A MLP (Modelo B) PRECISA do TF; este script roda em processo próprio com TF
# disponível. A taxonomia e as stopwords vêm do módulo TF-free text_utils.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))
from text_utils import (  # noqa: E402
    MIN_CLASS_DOCS_RECENT, OUTROS_LABEL, TAXONOMY, get_stopwords,
    small_classes_for_window)

INTERIM = PROJECT_ROOT / "data" / "interim" / "noticias_limpo.parquet"
PROC = PROJECT_ROOT / "data" / "processed"
FIG = PROJECT_ROOT / "reports" / "figures"
GOLD = PROJECT_ROOT / "reports" / "gold_labels.csv"
GOLD_TEMPLATE = PROJECT_ROOT / "reports" / "gold_template.csv"

SEED = 42
MAX_FEATURES = 5000
N_CLASSES = len(TAXONOMY)
CLASS_NAMES = [TAXONOMY[i] for i in range(N_CLASSES)]


def set_seeds() -> None:
    os.environ["PYTHONHASHSEED"] = str(SEED)
    random.seed(SEED)
    np.random.seed(SEED)


# --------------------------------------------------------------------------- #
# Dados
# --------------------------------------------------------------------------- #
def load_data() -> tuple[pd.DataFrame, pd.DataFrame, set[int], int]:
    """Retorna (pool, gold_df, gold_ids, n_indefinido).

    pool: docs com rótulo fraco (topic_raw != -1) e FORA do gold.
    gold_df: docs do gold com rótulo humano inteiro (exclui 'indefinido').
    """
    dt = pd.read_parquet(PROC / "doc_topics.parquet")[["id", "topic_raw"]]
    txt = pd.read_parquet(INTERIM)[["id", "titulo", "corpo_texto", "corpo_norm"]]
    df = dt.merge(txt, on="id")
    # Features TF-IDF: título + corpo normalizado (espaço lexical).
    df["text_tfidf"] = (df["titulo"].fillna("").str.lower() + " "
                        + df["corpo_norm"].fillna(""))
    # Features BERTimbau: título + corpo ORIGINAL (modelo cased usa caixa/acentos).
    df["text_bert"] = (df["titulo"].fillna("") + ". "
                       + df["corpo_texto"].fillna(""))

    gold_raw = pd.read_csv(GOLD, dtype={"gold": str})
    n_indef = int((gold_raw["gold"] == "indefinido").sum())
    gold_ok = gold_raw[gold_raw["gold"] != "indefinido"].copy()
    gold_ok["gold"] = gold_ok["gold"].astype(int)
    gold_ids = set(gold_ok["id"])
    gold_df = gold_ok.merge(df, on="id")

    weak = df[df["topic_raw"] != -1].copy()
    pool = weak[~weak["id"].isin(gold_ids)].copy()
    pool = pool.rename(columns={"topic_raw": "y"})
    print(f"[clf] pool de treino (rótulo fraco, fora do gold): {len(pool)} docs "
          f"| gold humano: {len(gold_df)} (+{n_indef} 'indefinido' excluídos)")
    return pool, gold_df, gold_ids, n_indef


def make_splits(pool: pd.DataFrame):
    """Split estratificado treino/validação/teste (≈64/16/20)."""
    from sklearn.model_selection import train_test_split
    idx = np.arange(len(pool))
    y = pool["y"].to_numpy()
    tr_full, te = train_test_split(idx, test_size=0.20, random_state=SEED,
                                   stratify=y)
    tr, va = train_test_split(tr_full, test_size=0.20, random_state=SEED,
                              stratify=y[tr_full])
    print(f"[clf] split interno: treino={len(tr)} val={len(va)} teste={len(te)}")
    return tr, va, te


# --------------------------------------------------------------------------- #
# Gold template (6.1) — NÃO rotula; só gera o CSV vazio para anotação humana
# --------------------------------------------------------------------------- #
def write_gold_template(recent_months: int = 18, n_per_class: int = 10) -> None:
    """Template de gold: amostra ALEATÓRIA ESTRATIFICADA por classe, restrita à
    JANELA RECENTE, com a coluna `classe` VAZIA para anotação humana CEGA.

    - `recent_months`: usa só docs cujos `data_publicacao` caem nos N meses mais
      recentes do corpus (decisão da Parada 1: 18 meses).
    - `n_per_class`: ~8-10 docs por classe (default 10), limitado pela
      disponibilidade da classe na janela.
    - Colunas: id, titulo, trecho, classe (VAZIA). NÃO incluímos o rótulo fraco
      candidato de propósito — anotação às cegas evita viés de ancoragem.
    - Regra do dono (registrada): classe com < MIN_CLASS_DOCS_RECENT docs na
      janela colapsa em 'Outros'. Hoje nenhuma dispara; o log confirma.
    """
    dt = pd.read_parquet(PROC / "doc_topics.parquet")[
        ["id", "classe_id", "classe_tematica", "data_publicacao"]]
    dt["data_publicacao"] = pd.to_datetime(dt["data_publicacao"])

    # Janela recente (mesma referência do diagnóstico: última publicação).
    ref = dt["data_publicacao"].max()
    start = ref - pd.DateOffset(months=recent_months)
    recent = dt[dt["data_publicacao"] > start].copy()
    counts = recent["classe_id"].value_counts().to_dict()

    # Regra <30 docs/janela -> 'Outros' (hoje no-op; viva para o futuro).
    collapsed = small_classes_for_window(counts)
    if collapsed:
        nomes = ", ".join(f"{c}:{TAXONOMY[c]} ({counts.get(c, 0)})"
                          for c in sorted(collapsed))
        print(f"[clf] regra <{MIN_CLASS_DOCS_RECENT} docs/{recent_months}m -> "
              f"'{OUTROS_LABEL}': colapsando {nomes}")
        recent["strata"] = recent["classe_id"].apply(
            lambda c: OUTROS_LABEL if c in collapsed else TAXONOMY[c])
    else:
        print(f"[clf] regra <{MIN_CLASS_DOCS_RECENT} docs/{recent_months}m -> "
              f"'{OUTROS_LABEL}': nenhuma classe dispara (mínimo "
              f"{min(counts.values())} docs); espaço de rótulos = 30 classes.")
        recent["strata"] = recent["classe_tematica"]

    txt = pd.read_parquet(INTERIM)[["id", "titulo", "corpo_texto"]]
    df = recent.merge(txt, on="id")
    rng = np.random.RandomState(SEED)
    parts = []
    for _, g in df.groupby("strata"):
        take = min(n_per_class, len(g))
        parts.append(g.sample(n=take, random_state=rng))
    sample = pd.concat(parts).sample(frac=1, random_state=rng)  # embaralha
    out = pd.DataFrame({
        "id": sample["id"].to_numpy(),
        "titulo": sample["titulo"].to_numpy(),
        "trecho": sample["corpo_texto"].fillna("").str[:400].to_numpy(),
        "classe": "",  # <-- VAZIA: rotular à mão (0-29, 'Outros' ou 'indefinido')
    })
    GOLD_TEMPLATE.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(GOLD_TEMPLATE, index=False)
    print(f"[clf] gold_template.csv: {len(out)} linhas ({sample['strata'].nunique()} "
          f"estratos x ~{n_per_class}/classe, janela {recent_months}m, "
          f"{len(recent)} docs candidatos) -> {GOLD_TEMPLATE}")


# --------------------------------------------------------------------------- #
# Métricas
# --------------------------------------------------------------------------- #
def score(y_true, y_pred, with_kappa: bool = False) -> dict:
    from sklearn.metrics import (accuracy_score, f1_score, cohen_kappa_score)
    out = {
        "accuracy": round(float(accuracy_score(y_true, y_pred)), 4),
        "f1_macro": round(float(f1_score(y_true, y_pred, average="macro",
                                         zero_division=0)), 4),
    }
    if with_kappa:
        out["kappa"] = round(float(cohen_kappa_score(y_true, y_pred)), 4)
    return out


def per_class_f1(y_true, y_pred) -> dict:
    from sklearn.metrics import f1_score
    labels = list(range(N_CLASSES))
    f1s = f1_score(y_true, y_pred, average=None, labels=labels, zero_division=0)
    return {TAXONOMY[i]: round(float(f1s[i]), 4) for i in labels}


# --------------------------------------------------------------------------- #
# Modelo A — Naive Bayes
# --------------------------------------------------------------------------- #
def build_vectorizer():
    from sklearn.feature_extraction.text import TfidfVectorizer
    return TfidfVectorizer(stop_words=get_stopwords(), ngram_range=(1, 2),
                           min_df=3, max_features=MAX_FEATURES, sublinear_tf=True)


def run_naive_bayes(pool, tr, va, te, gold_df) -> dict:
    from sklearn.naive_bayes import MultinomialNB
    print("\n[clf] === Modelo A: Naive Bayes (TF-IDF + MultinomialNB) ===")
    trva = np.concatenate([tr, va])

    # Interno: vetorizador ajustado só no treino (treino+val); avalia no teste.
    vec = build_vectorizer()
    Xtr = vec.fit_transform(pool.iloc[trva]["text_tfidf"])
    Xte = vec.transform(pool.iloc[te]["text_tfidf"])
    clf = MultinomialNB()
    clf.fit(Xtr, pool.iloc[trva]["y"])
    internal = score(pool.iloc[te]["y"], clf.predict(Xte))
    print(f"[clf]   interno (teste): acc={internal['accuracy']} "
          f"f1_macro={internal['f1_macro']}")

    # Externo: ajusta na pool inteira; prediz o gold humano.
    vec_g = build_vectorizer()
    Xpool = vec_g.fit_transform(pool["text_tfidf"])
    Xg = vec_g.transform(gold_df["text_tfidf"])
    clf_g = MultinomialNB().fit(Xpool, pool["y"])
    gpred = clf_g.predict(Xg)
    ext = score(gold_df["gold"], gpred, with_kappa=True)
    print(f"[clf]   externo (gold): acc={ext['accuracy']} "
          f"f1_macro={ext['f1_macro']} kappa={ext['kappa']}")
    return {"internal": internal, "external": ext,
            "external_per_class_f1": per_class_f1(gold_df["gold"], gpred),
            "_gold_pred": gpred.tolist()}


# --------------------------------------------------------------------------- #
# Modelo B — MLP Keras (com análise de overfit/underfit e Dropout)
# --------------------------------------------------------------------------- #
def build_mlp(n_features: int, dropout: float, l2: float = 0.0):
    import tensorflow as tf
    from tensorflow.keras import Sequential, regularizers
    from tensorflow.keras.layers import Dense, Dropout, Input
    tf.keras.utils.set_random_seed(SEED)
    reg = regularizers.l2(l2) if l2 > 0 else None
    layers = [Input(shape=(n_features,)),
              Dense(256, activation="relu", kernel_regularizer=reg)]
    if dropout > 0:
        layers.append(Dropout(dropout))
    layers.append(Dense(128, activation="relu", kernel_regularizer=reg))
    if dropout > 0:
        layers.append(Dropout(dropout))
    layers.append(Dense(N_CLASSES, activation="softmax"))
    model = Sequential(layers)
    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy",
                  metrics=["accuracy"])
    return model


def train_mlp(model, Xtr, ytr, Xva, yva, epochs: int, patience: int = 5,
              early_stop: bool = True):
    from tensorflow.keras.callbacks import EarlyStopping
    cbs = []
    if early_stop:
        cbs.append(EarlyStopping(monitor="val_loss", patience=patience,
                                 restore_best_weights=True))
    hist = model.fit(Xtr, ytr, validation_data=(Xva, yva), epochs=epochs,
                     batch_size=32, callbacks=cbs, verbose=0)
    return hist


def run_mlp(pool, tr, va, te, gold_df, epochs: int) -> dict:
    print("\n[clf] === Modelo B: MLP Keras (TF-IDF -> Dense/Dropout/softmax) ===")
    vec = build_vectorizer()
    Xtr = vec.fit_transform(pool.iloc[tr]["text_tfidf"]).toarray().astype("float32")
    Xva = vec.transform(pool.iloc[va]["text_tfidf"]).toarray().astype("float32")
    Xte = vec.transform(pool.iloc[te]["text_tfidf"]).toarray().astype("float32")
    ytr = pool.iloc[tr]["y"].to_numpy()
    yva = pool.iloc[va]["y"].to_numpy()
    yte = pool.iloc[te]["y"].to_numpy()
    nfeat = Xtr.shape[1]

    # --- DEMONSTRAÇÃO de overfit: AMBAS as variantes treinam o MESMO nº de
    #     épocas SEM early stopping, para que as curvas sejam comparáveis.
    #     Sem Dropout: overfit forte (val_loss sobe). Com Dropout: regularizado.
    m_no = build_mlp(nfeat, dropout=0.0)
    h_no = train_mlp(m_no, Xtr, ytr, Xva, yva, epochs=epochs, early_stop=False)
    m_do = build_mlp(nfeat, dropout=0.3)
    h_do = train_mlp(m_do, Xtr, ytr, Xva, yva, epochs=epochs, early_stop=False)
    plot_overfit(h_no.history, h_do.history)

    # --- Estudo de regularização (Dropout x L2) e do trade-off viés-variância.
    #     Resultado honesto: em features TF-IDF esparsas com poucos dados, o
    #     Dropout NÃO ajuda; o L2 moderado controla a subida de val_loss; L2
    #     forte leva a UNDERFIT. Curvas comparadas em 14b. ---
    reg_variants = [
        ("Sem regularização", dict(dropout=0.0, l2=0.0)),
        ("Dropout 0.3", dict(dropout=0.3, l2=0.0)),
        ("L2 1e-3", dict(dropout=0.0, l2=1e-3)),
        ("L2 1e-2 (forte)", dict(dropout=0.0, l2=1e-2)),
    ]
    reg_study = {}
    reg_curves = {}
    for label, kw in reg_variants:
        h = train_mlp(build_mlp(nfeat, **kw), Xtr, ytr, Xva, yva,
                      epochs=epochs, early_stop=False).history
        reg_curves[label] = h["val_loss"]
        reg_study[label] = {
            "train_acc_final": round(float(h["accuracy"][-1]), 4),
            "val_acc_best": round(float(max(h["val_accuracy"])), 4),
            "val_loss_min": round(float(min(h["val_loss"])), 4),
            "val_loss_final": round(float(h["val_loss"][-1]), 4),
            "val_loss_rise": round(float(h["val_loss"][-1] - min(h["val_loss"])), 4),
        }
    plot_regularization(reg_curves)

    # --- MODELO PRINCIPAL (para a métrica de teste): Dropout + early stopping
    #     (restaura os melhores pesos por val_loss — boa prática). ---
    m_main = build_mlp(nfeat, dropout=0.3)
    h_main = train_mlp(m_main, Xtr, ytr, Xva, yva, epochs=epochs, early_stop=True)
    pred_te = m_main.predict(Xte, verbose=0).argmax(1)
    internal = score(yte, pred_te)

    # Sinais de overfit (val_loss MÍNIMO = melhor ponto antes de degradar).
    overfit_gap = {
        "sem_dropout_train_acc_final": round(float(h_no.history["accuracy"][-1]), 4),
        "sem_dropout_val_acc_final": round(float(h_no.history["val_accuracy"][-1]), 4),
        "sem_dropout_val_loss_min": round(float(min(h_no.history["val_loss"])), 4),
        "sem_dropout_val_loss_final": round(float(h_no.history["val_loss"][-1]), 4),
        "com_dropout_train_acc_final": round(float(h_do.history["accuracy"][-1]), 4),
        "com_dropout_val_acc_final": round(float(h_do.history["val_accuracy"][-1]), 4),
        "com_dropout_val_loss_min": round(float(min(h_do.history["val_loss"])), 4),
        "com_dropout_val_loss_final": round(float(h_do.history["val_loss"][-1]), 4),
        "modelo_principal_epochs": len(h_main.history["loss"]),
        "epochs_demo": epochs,
        "regularizacao_estudo": reg_study,
    }
    print(f"[clf]   interno (teste, modelo principal c/ Dropout+ES): "
          f"acc={internal['accuracy']} f1_macro={internal['f1_macro']}")
    print(f"[clf]   overfit (demo {epochs} épocas, s/ ES): "
          f"SEM Dropout val_loss min={overfit_gap['sem_dropout_val_loss_min']} "
          f"final={overfit_gap['sem_dropout_val_loss_final']} | "
          f"COM Dropout val_loss min={overfit_gap['com_dropout_val_loss_min']} "
          f"final={overfit_gap['com_dropout_val_loss_final']}")

    # Externo (gold): treina MLP c/ Dropout na pool (val carved p/ early stopping).
    from sklearn.model_selection import train_test_split
    vec_g = build_vectorizer()
    Xpool_all = vec_g.fit_transform(pool["text_tfidf"]).toarray().astype("float32")
    ypool = pool["y"].to_numpy()
    p_tr, p_va = train_test_split(np.arange(len(pool)), test_size=0.15,
                                  random_state=SEED, stratify=ypool)
    Xg = vec_g.transform(gold_df["text_tfidf"]).toarray().astype("float32")
    m_g = build_mlp(Xpool_all.shape[1], dropout=0.3)
    train_mlp(m_g, Xpool_all[p_tr], ypool[p_tr], Xpool_all[p_va], ypool[p_va],
              epochs=epochs, early_stop=True)
    gpred = m_g.predict(Xg, verbose=0).argmax(1)
    ext = score(gold_df["gold"], gpred, with_kappa=True)
    print(f"[clf]   externo (gold): acc={ext['accuracy']} "
          f"f1_macro={ext['f1_macro']} kappa={ext['kappa']}")
    return {"internal": internal, "external": ext,
            "external_per_class_f1": per_class_f1(gold_df["gold"], gpred),
            "overfit_analysis": overfit_gap, "_gold_pred": gpred.tolist()}


def plot_overfit(h_no: dict, h_do: dict) -> None:
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    for col, (h, titulo) in enumerate([(h_no, "SEM Dropout (overfit)"),
                                       (h_do, "COM Dropout (regularizado)")]):
        ep = range(1, len(h["loss"]) + 1)
        axes[0, col].plot(ep, h["loss"], "o-", label="treino", color="#2c6fbb")
        axes[0, col].plot(ep, h["val_loss"], "s--", label="validação",
                          color="#bb2c4f")
        axes[0, col].set_title(f"Perda — {titulo}")
        axes[0, col].set_xlabel("época"); axes[0, col].set_ylabel("loss")
        axes[0, col].legend()
        axes[1, col].plot(ep, h["accuracy"], "o-", label="treino", color="#2c6fbb")
        axes[1, col].plot(ep, h["val_accuracy"], "s--", label="validação",
                          color="#bb2c4f")
        axes[1, col].set_title(f"Acurácia — {titulo}")
        axes[1, col].set_xlabel("época"); axes[1, col].set_ylabel("accuracy")
        axes[1, col].legend()
    fig.suptitle("MLP — análise de overfit/underfit (trade-off viés-variância)",
                 fontsize=13)
    plt.tight_layout()
    FIG.mkdir(parents=True, exist_ok=True)
    plt.savefig(FIG / "14_overfit_mlp.png")
    plt.close()
    print(f"[clf]   curvas de overfit -> {FIG / '14_overfit_mlp.png'}")


def plot_regularization(curves: dict) -> None:
    """Sobrepõe val_loss de cada regime de regularização (overfit→underfit)."""
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(9, 5.5))
    styles = ["o-", "s--", "^-.", "d:"]
    for (label, vl), st in zip(curves.items(), styles):
        ax.plot(range(1, len(vl) + 1), vl, st, label=label, markersize=3)
    ax.set_title("Regularização e trade-off viés-variância (val_loss por época)")
    ax.set_xlabel("época"); ax.set_ylabel("val_loss")
    ax.legend()
    plt.tight_layout()
    FIG.mkdir(parents=True, exist_ok=True)
    plt.savefig(FIG / "14b_regularizacao.png")
    plt.close()
    print(f"[clf]   curvas de regularização -> {FIG / '14b_regularizacao.png'}")


# --------------------------------------------------------------------------- #
# Modelo C — BERTimbau (embeddings BERT-pt mean-pooling + LogReg)
# --------------------------------------------------------------------------- #
def load_bertimbau_embeddings() -> tuple[np.ndarray, dict]:
    """Carrega o cache de embeddings BERTimbau (computado em processo separado
    por src/embed_bertimbau.py, para evitar segfault TF+torch). Se faltar, roda
    o script como subprocesso. Este processo NÃO importa torch."""
    import subprocess
    cache = PROC / "bertimbau_embeddings.npy"
    cache_ids = PROC / "bertimbau_ids.npy"
    if not (cache.exists() and cache_ids.exists()):
        print("[clf]   cache BERTimbau ausente — rodando src/embed_bertimbau.py "
              "(processo separado, somente torch)...")
        subprocess.run([sys.executable, str(PROJECT_ROOT / "src" / "embed_bertimbau.py")],
                       check=True)
    emb = np.load(cache)
    ids = np.load(cache_ids)
    id2row = {int(i): r for r, i in enumerate(ids)}
    print(f"[clf]   embeddings BERTimbau carregados {emb.shape}")
    return emb, id2row


def run_bertimbau(pool, tr, va, te, gold_df) -> dict:
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler
    from sklearn.pipeline import make_pipeline
    print("\n[clf] === Modelo C: BERTimbau (mean-pooling) + LogReg ===")

    emb, id2row = load_bertimbau_embeddings()

    def E(ids):
        return emb[[id2row[int(i)] for i in ids]]

    pool_ids = pool["id"].to_numpy()
    trva = np.concatenate([tr, va])
    clf = make_pipeline(StandardScaler(),
                        LogisticRegression(max_iter=2000, C=1.0))
    clf.fit(E(pool_ids[trva]), pool.iloc[trva]["y"])
    internal = score(pool.iloc[te]["y"], clf.predict(E(pool_ids[te])))
    print(f"[clf]   interno (teste): acc={internal['accuracy']} "
          f"f1_macro={internal['f1_macro']}")

    clf_g = make_pipeline(StandardScaler(),
                          LogisticRegression(max_iter=2000, C=1.0))
    clf_g.fit(E(pool_ids), pool["y"])
    gpred = clf_g.predict(E(gold_df["id"].to_numpy()))
    ext = score(gold_df["gold"], gpred, with_kappa=True)
    print(f"[clf]   externo (gold): acc={ext['accuracy']} "
          f"f1_macro={ext['f1_macro']} kappa={ext['kappa']}")
    return {"internal": internal, "external": ext,
            "external_per_class_f1": per_class_f1(gold_df["gold"], gpred),
            "_gold_pred": gpred.tolist()}


# --------------------------------------------------------------------------- #
# Matriz de confusão dos três modelos vs gold
# --------------------------------------------------------------------------- #
def plot_confusions(gold_y, preds: dict) -> None:
    import matplotlib.pyplot as plt
    from sklearn.metrics import confusion_matrix
    labels = list(range(N_CLASSES))
    n = len(preds)
    fig, axes = plt.subplots(1, n, figsize=(7 * n, 6))
    if n == 1:
        axes = [axes]
    for ax, (name, pred) in zip(axes, preds.items()):
        cm = confusion_matrix(gold_y, pred, labels=labels)
        im = ax.imshow(cm, cmap="Blues")
        ax.set_xticks(labels); ax.set_yticks(labels)
        ax.set_xlabel("Predito"); ax.set_ylabel("Gold (humano)")
        ax.set_title(f"{name} — confusão vs gold")
        thr = cm.max() / 2 if cm.max() else 0
        for i in labels:
            for j in labels:
                ax.text(j, i, cm[i, j], ha="center", va="center", fontsize=8,
                        color="white" if cm[i, j] > thr else "black")
    plt.tight_layout()
    FIG.mkdir(parents=True, exist_ok=True)
    plt.savefig(FIG / "15_confusion_gold.png")
    plt.close()
    print(f"[clf] matrizes de confusão -> {FIG / '15_confusion_gold.png'}")


# --------------------------------------------------------------------------- #
def main() -> None:
    ap = argparse.ArgumentParser(description="Classificação supervisionada (Fase 6).")
    ap.add_argument("--epochs", type=int, default=50)
    ap.add_argument("--skip-bert", action="store_true",
                    help="Pula o Modelo C (BERTimbau) — útil p/ iteração rápida.")
    ap.add_argument("--recent-months", type=int, default=18,
                    help="Janela recente (meses) p/ gold/classificação (Parada 1).")
    ap.add_argument("--per-class", type=int, default=10,
                    help="Docs por classe no gold_template (~8-10).")
    ap.add_argument("--template-only", action="store_true",
                    help="Só gera o gold_template e para (não roda classificação).")
    args = ap.parse_args()

    set_seeds()
    write_gold_template(recent_months=args.recent_months,
                        n_per_class=args.per_class)
    if args.template_only:
        print("[clf] --template-only: parando após o template (gold a rotular "
              "à mão; classificação NÃO executada).")
        return
    pool, gold_df, gold_ids, n_indef = load_data()
    tr, va, te = make_splits(pool)

    results = {}
    results["naive_bayes"] = run_naive_bayes(pool, tr, va, te, gold_df)
    results["mlp_keras"] = run_mlp(pool, tr, va, te, gold_df, epochs=args.epochs)
    if not args.skip_bert:
        results["bertimbau"] = run_bertimbau(pool, tr, va, te, gold_df)

    # Matriz de confusão vs gold (todos os modelos)
    preds = {"NB": results["naive_bayes"]["_gold_pred"],
             "MLP": results["mlp_keras"]["_gold_pred"]}
    if "bertimbau" in results:
        preds["BERTimbau"] = results["bertimbau"]["_gold_pred"]
    plot_confusions(gold_df["gold"].to_numpy(), preds)

    # Tabela-resumo
    print("\n[clf] ===== COMPARAÇÃO DOS MODELOS =====")
    header = f"{'modelo':<12} {'int_acc':>8} {'int_f1':>8} {'gold_acc':>9} {'gold_f1':>8} {'kappa':>7}"
    print(header)
    for name, r in results.items():
        print(f"{name:<12} {r['internal']['accuracy']:>8} "
              f"{r['internal']['f1_macro']:>8} {r['external']['accuracy']:>9} "
              f"{r['external']['f1_macro']:>8} {r['external']['kappa']:>7}")

    # Persiste métricas (remove preds brutas do JSON principal por concisão)
    metrics = {
        "protocol": {
            "pool_size": int(len(pool)),
            "gold_labeled": int(len(gold_df)),
            "gold_indefinido_excluded": int(n_indef),
            "n_classes": N_CLASSES,
            "max_features_tfidf": MAX_FEATURES,
            "split": {"treino": int(len(tr)), "val": int(len(va)),
                      "teste": int(len(te))},
            "seed": SEED,
            "leakage_note": "gold removido do treino (162/173 também eram rótulo fraco)",
        },
        "models": {k: {kk: vv for kk, vv in v.items() if not kk.startswith("_")}
                   for k, v in results.items()},
        "class_names": {i: TAXONOMY[i] for i in range(N_CLASSES)},
    }
    PROC.mkdir(parents=True, exist_ok=True)
    with (PROC / "classify_metrics.json").open("w", encoding="utf-8") as fh:
        json.dump(metrics, fh, ensure_ascii=False, indent=2)
    print(f"\n[clf] métricas -> {PROC / 'classify_metrics.json'}")
    print("[clf] LEMBRETE: reports/gold_template.csv tem a coluna 'classe' VAZIA "
          "— deve ser rotulada à mão. A avaliação aqui usa o gold humano já "
          "existente em reports/gold_labels.csv.")


if __name__ == "__main__":
    main()
