"""
Adjudicação das divergências entre a anotação original (reports/gold_labels.csv)
e a re-anotação do dono (reports/gold_reanotacao.csv).

ADJUDICAÇÃO É DECISÃO HUMANA. Para cada doc em que as duas anotações discordam,
alguém de domínio (o dono) precisa escolher o rótulo final — este script NÃO
inventa essas decisões. Ele:

  1. Identifica as divergências (espaço de 30 classes) e gera uma WORKLIST para
     resolver à mão: reports/gold_adjudicacao.csv
     (colunas: id, titulo, trecho, classe_dono, classe_gold, decisao=VAZIA).
  2. Monta o consenso JÁ resolvido = docs onde as duas anotações concordam (não
     exigem julgamento) -> reports/gold_consenso.csv (id, classe_consenso 0-29,
     classe_nome, origem). Disputas ficam como 'pendente' até serem decididas.
  3. Com --decisions <csv preenchido>, incorpora as decisões humanas, reporta
     quantas foram a favor do DONO vs do GOLD original, e finaliza o consenso.
  4. Mede o F1-macro do MLP (10 classes) contra o consenso DISPONÍVEL e compara
     com o gold completo (300). Também mostra, como DIAGNÓSTICO (não decisão),
     para que lado o MLP pende nas divergências.

Uso:
    python src/adjudicate.py
    python src/adjudicate.py --decisions reports/gold_adjudicacao.csv
"""

from __future__ import annotations

import argparse
import json
import sys
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))
from text_utils import TAXONOMY, MERGE_MAP_10  # noqa: E402

REPORTS = PROJECT_ROOT / "reports"
PROC = PROJECT_ROOT / "data" / "processed"
GOLD = REPORTS / "gold_labels.csv"
REANOT = REPORTS / "gold_reanotacao.csv"
WORKLIST = REPORTS / "gold_adjudicacao.csv"
CONSENSO = REPORTS / "gold_consenso.csv"
MLP_PREDS = PROC / "classify_gold_preds_merged10.json"
RESULT = PROC / "adjudicacao_resultado.json"


def norm_name(s: str) -> str:
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    return " ".join(s.lower().replace("/", " / ").split())


def load_pair() -> pd.DataFrame:
    """Junta gold original e re-anotação do dono num id->(gold30, dono30, texto)."""
    name2id = {norm_name(n): i for i, n in TAXONOMY.items()}
    gold = pd.read_csv(GOLD).rename(columns={"gold": "gold30"})
    re = pd.read_csv(REANOT)
    re["dono30"] = re["classe"].map(lambda v: name2id.get(norm_name(v)))
    if re["dono30"].isna().any():
        raise ValueError(f"nomes não mapeados: {re.loc[re['dono30'].isna(),'classe'].unique()}")
    re["dono30"] = re["dono30"].astype(int)
    df = re.merge(gold, on="id")
    df["gold10"] = df["gold30"].map(MERGE_MAP_10)
    df["dono10"] = df["dono30"].map(MERGE_MAP_10)
    return df


def write_worklist(div: pd.DataFrame) -> None:
    out = pd.DataFrame({
        "id": div["id"].to_numpy(),
        "titulo": div["titulo"].to_numpy(),
        "trecho": div["trecho"].fillna("").str[:400].to_numpy(),
        "classe_dono": [TAXONOMY[c] for c in div["dono30"]],
        "classe_gold": [TAXONOMY[c] for c in div["gold30"]],
        "decisao": "",   # <-- VAZIA: rotular à mão ('dono', 'gold' ou um nome de classe)
    })
    out.to_csv(WORKLIST, index=False)
    print(f"[adj] worklist das {len(out)} divergências -> {WORKLIST}")


def apply_decisions(df: pd.DataFrame, path: Path) -> tuple[pd.DataFrame, dict]:
    """Lê decisões humanas (coluna 'decisao': 'dono'/'gold'/nome de classe) e
    devolve a coluna de consenso resolvida para as divergências + contagem."""
    name2id = {norm_name(n): i for i, n in TAXONOMY.items()}
    dec = pd.read_csv(path)
    dmap, favor = {}, {"dono": 0, "gold": 0, "outro": 0}
    by_id = df.set_index("id")
    for _, r in dec.iterrows():
        v = str(r.get("decisao", "")).strip()
        if not v or v.lower() == "nan":
            continue
        i = int(r["id"])
        if v.lower() == "dono":
            dmap[i] = int(by_id.at[i, "dono30"]); favor["dono"] += 1
        elif v.lower() == "gold":
            dmap[i] = int(by_id.at[i, "gold30"]); favor["gold"] += 1
        elif norm_name(v) in name2id:
            cid = name2id[norm_name(v)]; dmap[i] = cid
            favor["dono" if cid == by_id.at[i, "dono30"]
                  else "gold" if cid == by_id.at[i, "gold30"] else "outro"] += 1
    return dmap, favor


def mlp_f1_against(consenso10: dict) -> dict:
    """F1-macro/acc/kappa do MLP (10 cls) restrito aos ids com consenso definido."""
    from sklearn.metrics import f1_score, accuracy_score, cohen_kappa_score
    d = json.load(open(MLP_PREDS))
    pred = {int(i): int(p) for i, p in zip(d["gold_ids"], d["preds"]["MLP"])}
    ids = [i for i in consenso10 if i in pred]
    y = [consenso10[i] for i in ids]
    yp = [pred[i] for i in ids]
    return {
        "n": len(ids),
        "accuracy": round(accuracy_score(y, yp), 4),
        "f1_macro": round(f1_score(y, yp, average="macro", zero_division=0), 4),
        "kappa": round(cohen_kappa_score(y, yp), 4),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--decisions", type=str, default=None,
                    help="CSV de adjudicação preenchido (coluna 'decisao').")
    args = ap.parse_args()

    df = load_pair()
    agree = df["dono30"] == df["gold30"]
    div = df[~agree].copy()
    print(f"[adj] docs={len(df)} | concordância={agree.sum()} | "
          f"divergências (30 cls)={len(div)}")
    print(f"[adj] em 10 classes: divergências={(df['dono10'] != df['gold10']).sum()} "
          f"(as demais colapsam no mesmo rótulo fundido)")

    write_worklist(div)

    # consenso: concordâncias (resolvidas) + adjudicadas (se houver decisões)
    consenso30: dict[int, int] = {int(r.id): int(r.gold30)
                                  for r in df[agree].itertuples()}
    favor = {"dono": 0, "gold": 0, "outro": 0}
    if args.decisions:
        dmap, favor = apply_decisions(df, Path(args.decisions))
        consenso30.update(dmap)
        print(f"[adj] decisões aplicadas: {sum(favor.values())}/{len(div)} | "
              f"a favor do DONO={favor['dono']} | do GOLD={favor['gold']} | "
              f"outro rótulo={favor['outro']}")
    else:
        print(f"[adj] (sem --decisions) {len(div)} divergências PENDENTES — "
              f"preencha {WORKLIST.name} e rode com --decisions.")

    # escreve gold_consenso.csv (300 linhas; disputas pendentes ficam vazias)
    rows = []
    for r in df.itertuples():
        cid = consenso30.get(int(r.id))
        origem = ("concordancia" if agree[r.Index]
                  else "adjudicado" if cid is not None else "pendente")
        rows.append({"id": int(r.id),
                     "classe_consenso": "" if cid is None else cid,
                     "classe_nome": "" if cid is None else TAXONOMY[cid],
                     "origem": origem})
    pd.DataFrame(rows).to_csv(CONSENSO, index=False)
    n_res = sum(v is not None for v in (consenso30.get(int(r.id)) for r in df.itertuples()))
    print(f"[adj] consenso -> {CONSENSO} ({n_res}/{len(df)} resolvidos, "
          f"{len(df)-n_res} pendentes)")

    # F1 do MLP contra o consenso disponível (10 classes) + baseline no gold
    consenso10 = {i: MERGE_MAP_10[c] for i, c in consenso30.items()}
    gold10_all = {int(r.id): int(r.gold10) for r in df.itertuples()}
    mlp_cons = mlp_f1_against(consenso10)
    mlp_gold = mlp_f1_against(gold10_all)
    print(f"\n[adj] === MLP (10 classes) ===")
    print(f"  vs gold completo (n={mlp_gold['n']}):  acc={mlp_gold['accuracy']} "
          f"f1={mlp_gold['f1_macro']} kappa={mlp_gold['kappa']}")
    print(f"  vs CONSENSO       (n={mlp_cons['n']}):  acc={mlp_cons['accuracy']} "
          f"f1={mlp_cons['f1_macro']} kappa={mlp_cons['kappa']}")

    # DIAGNÓSTICO (não é decisão): nas divergências de 10 cls, p/ que lado o MLP pende
    d = json.load(open(MLP_PREDS))
    pred = {int(i): int(p) for i, p in zip(d["gold_ids"], d["preds"]["MLP"])}
    div10 = df[df["dono10"] != df["gold10"]]
    lean = {"concorda_dono": 0, "concorda_gold": 0, "nenhum": 0}
    for r in div10.itertuples():
        p = pred.get(int(r.id))
        lean["concorda_dono" if p == r.dono10 else
             "concorda_gold" if p == r.gold10 else "nenhum"] += 1
    print(f"\n[adj] DIAGNÓSTICO (não-decisão) nas {len(div10)} divergências de 10 cls — "
          f"para que lado o MLP pende:")
    print(f"  concorda c/ DONO={lean['concorda_dono']} | c/ GOLD={lean['concorda_gold']} "
          f"| nenhum dos dois={lean['nenhum']}")

    json.dump({"n_docs": len(df), "n_concordancia": int(agree.sum()),
               "n_divergencia_30": int(len(div)),
               "n_divergencia_10": int((df['dono10'] != df['gold10']).sum()),
               "favor": favor, "mlp_vs_consenso": mlp_cons,
               "mlp_vs_gold": mlp_gold, "mlp_lean_divergencias": lean},
              open(RESULT, "w"), ensure_ascii=False, indent=2)
    print(f"\n[adj] resultado -> {RESULT}")


if __name__ == "__main__":
    main()
