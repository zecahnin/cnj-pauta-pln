"""
Helper script de NER para uso em subprocess isolado (torch only, sem TF).
Lê o texto de stdin, imprime JSON de entidades para stdout.
Uso: echo "<texto>" | python src/ner_single.py
"""

from __future__ import annotations

import json
import sys
import unicodedata
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_NAME = "rhaymison/ner-portuguese-br-bert-cased"
MIN_SCORE = 0.90
MAX_CHARS = 2000

sys.path.insert(0, str(PROJECT_ROOT / "src"))
from text_utils import (  # noqa: E402
    ENTITY_ACRONYM_WHITELIST,
    ENTITY_EDGE_WORDS,
    ENTITY_SELF_REF,
    GENERIC_ENTITY_STOP,
)


def _norm_key(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return " ".join(s.lower().split())


def _clean_span(surface: str) -> str:
    toks = surface.split()
    while toks and _norm_key(toks[0]) in ENTITY_EDGE_WORDS:
        toks.pop(0)
    while toks and _norm_key(toks[-1]) in ENTITY_EDGE_WORDS:
        toks.pop()
    return " ".join(toks)


def _is_fragment(surface: str, tipo: str, key: str) -> bool:
    if "##" in surface:
        return True
    if len(key) < 3:
        return True
    if not any(ch.isalpha() for ch in surface):
        return True
    if len(key) <= 4 and tipo in ("PER", "ORG") \
            and key not in ENTITY_ACRONYM_WHITELIST:
        return True
    return False


def run_ner(text: str) -> list[dict]:
    import torch
    from transformers import pipeline

    device = 0 if torch.cuda.is_available() else -1
    ner = pipeline("ner", model=MODEL_NAME, aggregation_strategy="max", device=device)
    raw = ner(text[:MAX_CHARS])
    if isinstance(raw, dict):
        raw = [raw]

    seen: set[str] = set()
    out = []
    for e in raw:
        if float(e["score"]) < MIN_SCORE:
            continue
        surface = _clean_span(str(e["word"]).strip())
        if not surface:
            continue
        tipo = e["entity_group"]
        key = _norm_key(surface)
        if _is_fragment(surface, tipo, key):
            continue
        if key in GENERIC_ENTITY_STOP:
            continue
        if key in seen:
            continue
        seen.add(key)
        out.append({"text": surface, "type": tipo, "score": round(float(e["score"]), 4)})
    return out


if __name__ == "__main__":
    text = sys.stdin.read()
    entities = run_ner(text)
    print(json.dumps(entities, ensure_ascii=False))
