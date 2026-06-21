"""Impede o import de TensorFlow em processos do stack torch + numba.

Por que isto existe
-------------------
`umap.parametric_umap` faz ``import tensorflow`` de forma incondicional sempre
que o TensorFlow está instalado (ver ``umap/__init__.py``, que envolve o import
em ``try/except ImportError``). O TensorFlow só foi instalado para a MLP Keras
(Modelo B, Fase 6). Acontece que carregar **TensorFlow + PyTorch + numba** no
MESMO processo provoca *segmentation fault* (conflito de runtime OpenMP entre
as bibliotecas) — exatamente o caso da `src/topics.py`, que usa BERTopic
(numba via UMAP/HDBSCAN + torch via sentence-transformers).

Como o BERTopic/NER/BERTimbau não precisam de TensorFlow, basta importar este
módulo ANTES de `bertopic`/`umap`: ao colocar ``None`` em
``sys.modules["tensorflow"]``, qualquer ``import tensorflow`` subsequente
levanta ``ImportError``; o UMAP captura e simplesmente não expõe o
``ParametricUMAP`` (que não usamos). A MLP Keras roda em processo próprio
(`src/classify.py`), sem importar este guard, e portanto tem o TF disponível.
"""

from __future__ import annotations

import sys


def block_tensorflow() -> None:
    """Faz ``import tensorflow`` levantar ImportError (se ainda não importado)."""
    if "tensorflow" not in sys.modules:
        sys.modules["tensorflow"] = None  # type: ignore[assignment]


block_tensorflow()
