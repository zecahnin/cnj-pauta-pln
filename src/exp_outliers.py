"""
Experimento #2 (versão SEM VAZAMENTO) — os outliers rotulados pelo dono em
reports/gold_reanotacao.csv coincidem 300/300 com o gold. Mesclá-los ao treino e
avaliar no gold seria treino-no-teste. Aqui medimos o MESMO efeito de forma
válida, por validação cruzada sobre os 167 outliers genuínos (topic_raw == -1):

- Conjunto de teste = os 167 outliers, sempre avaliados com o rótulo GOLD.
- ANTES : modelo treinado só no pool (sem nenhum outlier) prediz os 167.
- DEPOIS: KFold(5) sobre os 167; cada fold é predito por um modelo treinado em
          pool + (outliers dos DEMAIS folds, com o rótulo do DONO). Acumula a
          predição de cada outlier quando ele cai no fold de teste.

Como o teste (gold) nunca aparece no treino do seu próprio fold, não há
vazamento; e o conjunto avaliado é idêntico em ANTES e DEPOIS -> comparável.
Responde diretamente: rotular outliers e injetá-los no treino melhora a
classificação de OUTROS outliers? Esquema de 10 classes.

Uso:
    python src/exp_outliers.py --epochs 40
"""

from __future__ import annotations

import argparse
import sys
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))
import classify as C  # noqa: E402
from text_utils import TAXONOMY, MERGE_MAP_10  # noqa: E402

PROC = PROJECT_ROOT / "data" / "processed"
REANOT = PROJECT_ROOT / "reports" / "gold_reanotacao.csv"
SEED = 42
N_SPLITS = 5


def norm_name(s: str) -> str:
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    return " ".join(s.lower().replace("/", " / ").split())


def owner_labels_10() -> pd.DataFrame:
    """Lê a re-anotação do dono (nomes das 30 classes) -> id de 10 classes."""
    name2id = {norm_name(n): i for i, n in TAXONOMY.items()}
    df = pd.read_csv(REANOT)
    df["cid30"] = df["classe"].map(lambda v: name2id.get(norm_name(v)))
    if df["cid30"].isna().any():
        bad = df.loc[df["cid30"].isna(), "classe"].unique()
        raise ValueError(f"nomes não mapeados: {bad}")
    df["owner10"] = df["cid30"].astype(int).map(MERGE_MAP_10)
    return df[["id", "owner10"]]


def fit_predict_nb(tr_text, tr_y, ev_text):
    from sklearn.naive_bayes import MultinomialNB
    vec = C.build_vectorizer()
    Xtr = vec.fit_transform(tr_text)
    clf = MultinomialNB().fit(Xtr, tr_y)
    return clf.predict(vec.transform(ev_text))


def fit_predict_mlp(tr_text, tr_y, ev_text, epochs):
    from sklearn.model_selection import train_test_split
    vec = C.build_vectorizer()
    Xtr_all = vec.fit_transform(tr_text).toarray().astype("float32")
    Xev = vec.transform(ev_text).toarray().astype("float32")
    a, b = train_test_split(np.arange(len(tr_y)), test_size=0.15,
                            random_state=SEED, stratify=tr_y)
    m = C.build_mlp(Xtr_all.shape[1], dropout=0.3)
    C.train_mlp(m, Xtr_all[a], tr_y[a], Xtr_all[b], tr_y[b],
                epochs=epochs, early_stop=True)
    return m.predict(Xev, verbose=0).argmax(1)


def fit_predict_bert(tr_ids, tr_y, ev_ids, emb, id2row):
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler
    from sklearn.pipeline import make_pipeline
    E = lambda ids: emb[[id2row[int(i)] for i in ids]]
    clf = make_pipeline(StandardScaler(),
                        LogisticRegression(max_iter=2000, C=1.0))
    clf.fit(E(tr_ids), tr_y)
    return clf.predict(E(ev_ids))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--epochs", type=int, default=40)
    args = ap.parse_args()
    C.set_seeds()
    C.apply_scheme("10")
    from sklearn.model_selection import KFold

    # --- pool (sem outliers, sem gold) e gold_df (300, com texto), em 10 classes
    # gold_df já carrega `topic_raw` (vem de load_data); basta juntar o rótulo dono.
    pool, gold_df, _, _ = C.load_data()
    gdf = gold_df.merge(owner_labels_10(), on="id")
    out = gdf[gdf["topic_raw"] == -1].reset_index(drop=True)        # 167 outliers
    print(f"[exp] pool={len(pool)} | outliers genuínos no gold={len(out)} "
          f"(eval) | esquema=10 classes")

    emb, id2row = C.load_bertimbau_embeddings()
    pool_text = pool["text_tfidf"].to_numpy()
    pool_y = pool["y"].to_numpy()
    pool_ids = pool["id"].to_numpy()
    o_text = out["text_tfidf"].to_numpy()
    o_ids = out["id"].to_numpy()
    o_gold = out["gold"].to_numpy()        # rótulo GOLD (avaliação)
    o_owner = out["owner10"].to_numpy()    # rótulo DONO (treino, no DEPOIS)

    def metrics(pred):
        return C.score(o_gold, pred, with_kappa=True)

    results = {}
    # ---------------- ANTES: treina só no pool, prediz os 167 ----------------
    print("[exp] ANTES (treino = pool; eval = 167 outliers, rótulo gold)...")
    antes = {
        "NB": fit_predict_nb(pool_text, pool_y, o_text),
        "MLP": fit_predict_mlp(pool_text, pool_y, o_text, args.epochs),
        "BERTimbau": fit_predict_bert(pool_ids, pool_y, o_ids, emb, id2row),
    }
    # ---------------- DEPOIS: KFold, treino = pool + outliers-dono ------------
    print(f"[exp] DEPOIS ({N_SPLITS}-fold; treino = pool + outliers do dono)...")
    kf = KFold(n_splits=N_SPLITS, shuffle=True, random_state=SEED)
    pred_dep = {k: np.empty(len(out), dtype=int) for k in antes}
    for fold, (tr_idx, te_idx) in enumerate(kf.split(np.arange(len(out))), 1):
        tr_text = np.concatenate([pool_text, o_text[tr_idx]])
        tr_y = np.concatenate([pool_y, o_owner[tr_idx]])
        tr_ids = np.concatenate([pool_ids, o_ids[tr_idx]])
        pred_dep["NB"][te_idx] = fit_predict_nb(tr_text, tr_y, o_text[te_idx])
        pred_dep["MLP"][te_idx] = fit_predict_mlp(tr_text, tr_y, o_text[te_idx],
                                                  args.epochs)
        pred_dep["BERTimbau"][te_idx] = fit_predict_bert(
            tr_ids, tr_y, o_ids[te_idx], emb, id2row)
        print(f"[exp]   fold {fold}/{N_SPLITS} ok")

    # ---------------- tabela ----------------
    print("\n[exp] ===== ANTES vs DEPOIS (eval = 167 outliers held-out, gold) =====")
    hdr = f"{'modelo':<12} {'acc_antes':>9} {'acc_depois':>10} {'f1_antes':>9} {'f1_depois':>10} {'kappa_antes':>11} {'kappa_depois':>12}"
    print(hdr)
    for k in antes:
        a, d = metrics(antes[k]), metrics(pred_dep[k])
        results[k] = {"antes": a, "depois": d}
        print(f"{k:<12} {a['accuracy']:>9} {d['accuracy']:>10} "
              f"{a['f1_macro']:>9} {d['f1_macro']:>10} "
              f"{a['kappa']:>11} {d['kappa']:>12}")
    import json
    outp = PROC / "exp_outliers_results.json"
    with outp.open("w", encoding="utf-8") as fh:
        json.dump({"n_eval": int(len(out)), "n_pool": int(len(pool)),
                   "results": results}, fh, ensure_ascii=False, indent=2)
    print(f"\n[exp] resultados -> {outp}")


if __name__ == "__main__":
    main()
