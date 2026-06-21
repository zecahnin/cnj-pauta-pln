"""
Fase 6 — Validação supervisionada.

Pergunta de validação: os **rótulos fracos** do BERTopic (atribuições brutas do
HDBSCAN) são consistentes o bastante para (a) serem aprendidos por um
classificador a partir de features lexicais independentes e (b) concordarem com
um **gold set anotado manualmente** por leitura dos textos?

- **Features:** TF-IDF (1-2 gramas) sobre `título + corpo_norm`. Espaço lexical,
  DISTINTO do espaço de embeddings/UMAP que gerou os clusters — reduz
  circularidade da avaliação.
- **Rótulos fracos:** `topic_raw` (exclui outliers -1).
- **Classificadores:** Regressão Logística e LinearSVM.
- **Avaliação intrínseca:** F1-macro em split de teste dos rótulos fracos.
- **Avaliação contra gold:** F1-macro e Cohen's kappa entre predição e gold;
  também kappa rótulo-fraco × gold (concordância dos rótulos fracos com o humano).
  Matriz de confusão (gold × predito).

Gold set: `reports/gold_labels.csv` (~195 notícias; anotação por leitura de
título/lead contra a taxonomia de 10 tópicos da Fase 4; "indefinido" para casos
ambíguos, excluídos das métricas).

Artefatos:
- `data/processed/supervised_metrics.json`
- `reports/figures/13_confusion_matrix.png`

Uso:
    python src/supervised.py
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
INTERIM = PROJECT_ROOT / "data" / "interim" / "noticias_limpo.parquet"
PROC = PROJECT_ROOT / "data" / "processed"
FIG = PROJECT_ROOT / "reports" / "figures"
GOLD = PROJECT_ROOT / "reports" / "gold_labels.csv"
SEED = 42

import sys
sys.path.insert(0, str(PROJECT_ROOT / "src"))
from drift import TOPIC_LABELS  # noqa: E402
from topics import get_stopwords  # noqa: E402


def load_dataset() -> pd.DataFrame:
    dt = pd.read_parquet(PROC / "doc_topics.parquet")[["id", "topic_raw"]]
    txt = pd.read_parquet(INTERIM)[["id", "titulo", "corpo_norm"]]
    df = dt.merge(txt, on="id")
    df["text"] = (df["titulo"].fillna("").str.lower() + " "
                  + df["corpo_norm"].fillna(""))
    return df


def main() -> None:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.svm import LinearSVC
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import (f1_score, accuracy_score, cohen_kappa_score,
                                 confusion_matrix, classification_report)

    df = load_dataset()
    weak = df[df["topic_raw"] != -1].copy()
    print(f"[sup] {len(df)} docs | {len(weak)} com rótulo fraco "
          f"(exclui {len(df) - len(weak)} outliers)")

    stop_words = get_stopwords()
    vec = TfidfVectorizer(stop_words=stop_words, ngram_range=(1, 2),
                          min_df=3, max_features=20000, sublinear_tf=True)

    X_all = vec.fit_transform(weak["text"])
    y_all = weak["topic_raw"].to_numpy()

    # --- Avaliação intrínseca (aprendizagem dos rótulos fracos) ---
    Xtr, Xte, ytr, yte = train_test_split(
        X_all, y_all, test_size=0.25, random_state=SEED, stratify=y_all)

    results = {}
    classifiers = {
        "logreg": LogisticRegression(max_iter=2000, C=10.0,
                                     class_weight="balanced"),
        "linsvm": LinearSVC(C=1.0, class_weight="balanced"),
    }
    for name, clf in classifiers.items():
        clf.fit(Xtr, ytr)
        pred = clf.predict(Xte)
        results[name] = {
            "intrinsic_f1_macro": round(float(f1_score(yte, pred,
                                        average="macro")), 4),
            "intrinsic_accuracy": round(float(accuracy_score(yte, pred)), 4),
        }
        print(f"[sup] {name}: F1-macro(teste fraco)="
              f"{results[name]['intrinsic_f1_macro']} "
              f"acc={results[name]['intrinsic_accuracy']}")

    # --- Avaliação contra o gold set ---
    gold = pd.read_csv(GOLD, dtype={"gold": str})
    gold = gold[gold["gold"] != "indefinido"].copy()
    gold["gold"] = gold["gold"].astype(int)
    n_indef = pd.read_csv(GOLD)["gold"].eq("indefinido").sum()
    gdf = gold.merge(df[["id", "text", "topic_raw"]], on="id")
    print(f"[sup] gold: {len(gold)} rotulados (+{n_indef} 'indefinido' "
          f"excluídos)")

    # Treina classificador final em TODOS os rótulos fracos; prediz no gold.
    best_name = max(results, key=lambda k: results[k]["intrinsic_f1_macro"])
    final_clf = classifiers[best_name]
    final_clf.fit(X_all, y_all)
    Xg = vec.transform(gdf["text"])
    gpred = final_clf.predict(Xg)

    f1_gold = float(f1_score(gdf["gold"], gpred, average="macro"))
    kappa_pred_gold = float(cohen_kappa_score(gdf["gold"], gpred))

    # Concordância rótulo-fraco × gold (só onde o doc tinha rótulo fraco != -1)
    mask = gdf["topic_raw"] != -1
    kappa_weak_gold = float(cohen_kappa_score(
        gdf.loc[mask, "gold"], gdf.loc[mask, "topic_raw"]))
    acc_weak_gold = float(accuracy_score(
        gdf.loc[mask, "gold"], gdf.loc[mask, "topic_raw"]))

    print(f"[sup] === contra GOLD (classificador {best_name}) ===")
    print(f"[sup] F1-macro(pred×gold)={f1_gold:.4f}")
    print(f"[sup] kappa(pred×gold)={kappa_pred_gold:.4f}")
    print(f"[sup] kappa(rótulo_fraco×gold)={kappa_weak_gold:.4f} "
          f"(n={int(mask.sum())}) acc={acc_weak_gold:.4f}")

    print("\n[sup] classification_report (pred × gold):")
    labels = sorted(set(gdf["gold"]) | set(gpred))
    target_names = [f"T{l}:{TOPIC_LABELS.get(l, l)[:18]}" for l in labels]
    print(classification_report(gdf["gold"], gpred, labels=labels,
                                target_names=target_names, zero_division=0))

    # Matriz de confusão
    _plot_confusion(gdf["gold"].to_numpy(), gpred, labels)

    metrics = {
        "n_docs": int(len(df)),
        "n_weak_labeled": int(len(weak)),
        "n_outliers": int(len(df) - len(weak)),
        "classifiers_intrinsic": results,
        "best_classifier": best_name,
        "gold": {
            "n_labeled": int(len(gold)),
            "n_indefinido_excluded": int(n_indef),
            "f1_macro_pred_vs_gold": round(f1_gold, 4),
            "kappa_pred_vs_gold": round(kappa_pred_gold, 4),
            "kappa_weak_vs_gold": round(kappa_weak_gold, 4),
            "accuracy_weak_vs_gold": round(acc_weak_gold, 4),
            "n_weak_in_gold": int(mask.sum()),
        },
    }
    PROC.mkdir(parents=True, exist_ok=True)
    with (PROC / "supervised_metrics.json").open("w", encoding="utf-8") as fh:
        json.dump(metrics, fh, ensure_ascii=False, indent=2)
    print(f"\n[sup] métricas salvas em {PROC / 'supervised_metrics.json'}")


def _plot_confusion(y_true, y_pred, labels) -> None:
    import matplotlib.pyplot as plt
    from sklearn.metrics import confusion_matrix

    cm = confusion_matrix(y_true, y_pred, labels=labels)
    fig, ax = plt.subplots(figsize=(8, 7))
    im = ax.imshow(cm, cmap="Blues")
    ax.set_xticks(range(len(labels)), [f"T{l}" for l in labels])
    ax.set_yticks(range(len(labels)), [f"T{l}" for l in labels])
    ax.set_xlabel("Predito (classificador)")
    ax.set_ylabel("Gold (anotação manual)")
    ax.set_title("Matriz de confusão — predição × gold")
    thr = cm.max() / 2 if cm.max() else 0
    for i in range(len(labels)):
        for j in range(len(labels)):
            ax.text(j, i, cm[i, j], ha="center", va="center",
                    color="white" if cm[i, j] > thr else "black", fontsize=9)
    fig.colorbar(im, fraction=0.046, pad=0.04)
    plt.tight_layout()
    FIG.mkdir(parents=True, exist_ok=True)
    plt.savefig(FIG / "13_confusion_matrix.png")
    plt.close()
    print(f"[sup] matriz de confusão -> {FIG / '13_confusion_matrix.png'}")


if __name__ == "__main__":
    main()
