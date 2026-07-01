"""
CNJ Pauta PLN — Demo ao vivo
Classificação temática (10 classes, MLP + TF-IDF) + NER (BERT-pt cased)

Isolamento TF/torch: TF roda no processo principal (classificação);
torch roda em subprocess isolado via src/ner_single.py (mesma estratégia
do embed_bertimbau.py — evita segfault TF+torch no mesmo processo).
"""

import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ.setdefault("TF_FORCE_GPU_ALLOW_GROWTH", "true")

import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from text_utils import TAXONOMY_10  # noqa: E402
from preprocess import normalize_text  # noqa: E402

MODEL_DIR = PROJECT_ROOT / "data" / "processed" / "model_10"
NER_SCRIPT = PROJECT_ROOT / "src" / "ner_single.py"

EXAMPLES = [
    (
        "Tecnologia / IA",
        "CNJ lança plataforma de inteligência artificial para triagem de processos\n\n"
        "O Conselho Nacional de Justiça apresentou o projeto Juízo 4.0, plataforma de "
        "inteligência artificial desenvolvida para auxiliar magistrados na triagem e "
        "classificação automática de processos judiciais. A ferramenta utiliza algoritmos "
        "de aprendizado de máquina para identificar temas recorrentes e sugerir precedentes "
        "aplicáveis, reduzindo o tempo de análise inicial em até 60%. O presidente do CNJ "
        "destacou que a tecnologia não substitui o raciocínio jurídico, mas agiliza tarefas "
        "repetitivas. O sistema será implantado em tribunais estaduais como parte da "
        "estratégia de digitalização da Justiça brasileira.",
    ),
    (
        "Violência doméstica",
        "CNJ amplia rede de proteção a mulheres vítimas de violência doméstica\n\n"
        "O Conselho Nacional de Justiça lançou o programa Mulher Protegida, que integra "
        "varas especializadas em violência doméstica com centros de atendimento psicossocial "
        "em todo o Brasil. A iniciativa inclui monitoramento eletrônico para agressores em "
        "regime de medida protetiva e criação de casas-abrigo em municípios que ainda não "
        "dispõem do serviço. A ministra destacou que os feminicídios aumentaram no último "
        "ano, reforçando a urgência de políticas públicas de prevenção e a aplicação "
        "rigorosa da Lei Maria da Penha nos tribunais.",
    ),
    (
        "Sistema prisional",
        "CNJ conclui mutirão carcerário e determina interdição de presídios superlotados\n\n"
        "O Conselho Nacional de Justiça encerrou inspeção em unidades penitenciárias de "
        "quatro estados, identificando superlotação carcerária de até 300% da capacidade "
        "em algumas instalações. A inspeção revelou falta de assistência jurídica, ausência "
        "de atividades de ressocialização e número elevado de presos provisórios além do "
        "prazo legal. O plenário determinou a liberação imediata de presos com penas "
        "cumpridas e a interdição parcial de duas unidades em estado crítico. O programa "
        "Fazendo Justiça prevê construção de novas unidades e fortalecimento das defensorias.",
    ),
]


# --------------------------------------------------------------------------- #
# Carregamento dos modelos (cacheado — carrega apenas na primeira chamada)
# --------------------------------------------------------------------------- #

@st.cache_resource(show_spinner="Carregando classificador (TF-IDF + MLP)...")
def load_classifier():
    """Carrega vectorizer + MLP Keras do esquema 10."""
    import json
    import joblib
    import tensorflow as tf  # TF antes do torch — ordem importa para coexistência

    if not MODEL_DIR.exists() or not (MODEL_DIR / "mlp.keras").exists():
        return None, None, None

    vec = joblib.load(MODEL_DIR / "vectorizer.joblib")
    model = tf.keras.models.load_model(MODEL_DIR / "mlp.keras")
    with (MODEL_DIR / "meta.json").open(encoding="utf-8") as f:
        meta = json.load(f)
    return vec, model, meta


def _run_ner_subprocess(text: str) -> list[dict]:
    """NER via subprocess isolado (torch, sem TF) — evita segfault TF+torch."""
    python = Path(sys.executable)
    try:
        result = subprocess.run(
            [str(python), str(NER_SCRIPT)],
            input=text,
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode != 0:
            st.warning(f"NER subprocess falhou (código {result.returncode}). "
                       "Entidades indisponíveis.")
            return []
        return json.loads(result.stdout)
    except Exception as exc:
        st.warning(f"NER subprocess erro: {exc}. Entidades indisponíveis.")
        return []


# --------------------------------------------------------------------------- #
# Inferência
# --------------------------------------------------------------------------- #

def classify_and_extract(text: str) -> dict:
    """Classifica o texto e extrai entidades nomeadas com modelos reais.

    Classificação: TF-IDF → MLP Keras (processo principal, TF).
    NER: rhaymison/ner-portuguese-br-bert-cased via subprocess isolado (torch).

    Returns:
        dict com: class_name, class_id, confidence, top3, entities.
        Retorna {} e exibe aviso se os artefatos não forem encontrados.
    """
    vec, model, meta = load_classifier()
    if vec is None:
        st.error(
            "Artefatos não encontrados em `data/processed/model_10/`.  \n"
            "Execute:  \n`python src/classify.py --scheme 10 --save-model`"
        )
        return {}

    # Classificação: TF-IDF → MLP → softmax
    feat = normalize_text(text)
    X = vec.transform([feat]).toarray().astype("float32")
    probs = model.predict(X, verbose=0)[0]  # shape (10,)

    class_names = meta["class_names"]  # {"0": "...", "9": "..."}
    top3_idx = np.argsort(probs)[::-1][:3]
    top3 = [
        {"name": class_names[str(int(i))], "id": int(i), "prob": float(probs[i])}
        for i in top3_idx
    ]

    # NER: subprocess isolado (torch separado do TF)
    entities = _run_ner_subprocess(text)

    return {
        "class_name": top3[0]["name"],
        "class_id": top3[0]["id"],
        "confidence": top3[0]["prob"],
        "top3": top3,
        "entities": entities,
    }


# --------------------------------------------------------------------------- #
# Layout Streamlit
# --------------------------------------------------------------------------- #

st.set_page_config(
    page_title="CNJ Pauta PLN",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

with st.sidebar:
    st.title("⚖️ CNJ Pauta PLN")
    st.markdown("**Classificador temático de notícias do CNJ**")
    st.divider()
    st.markdown(
        "| Parâmetro | Valor |\n"
        "|---|---|\n"
        "| Modelo | MLP + TF-IDF |\n"
        "| Features | 5.000 |\n"
        "| Classes | 10 |\n"
        "| F1-macro (gold) | **0.705** |\n"
        "| NER | BERT-pt cased |"
    )
    st.divider()
    st.markdown("**Taxonomia temática (10 classes)**")
    for cid, cname in TAXONOMY_10.items():
        st.markdown(f"**{cid}** — {cname}")

st.title("CNJ Pauta PLN — Demo ao vivo")
st.caption(
    "Classificação temática (10 classes) + NER de notícias do CNJ. "
    "Modelo MLP + TF-IDF treinado sobre ~4.400 notícias (F1-macro 0.705 vs gold humano)."
)

# Inicializa session state
if "demo_text" not in st.session_state:
    st.session_state["demo_text"] = ""


def _set_example(txt: str) -> None:
    st.session_state["demo_text"] = txt


# Botões de exemplo
st.markdown("##### Exemplos prontos")
ex_cols = st.columns(len(EXAMPLES))
for col, (i, (label, txt)) in zip(ex_cols, enumerate(EXAMPLES)):
    with col:
        st.button(
            f"📰 {label}",
            key=f"btn_ex{i}",
            on_click=_set_example,
            args=(txt,),
            use_container_width=True,
        )

st.divider()

# Área de texto
user_text = st.text_area(
    "Texto da notícia (título + corpo):",
    key="demo_text",
    height=220,
    placeholder="Cole aqui o título e o corpo da notícia...",
)

col_btn, _ = st.columns([1, 5])
with col_btn:
    classify_clicked = st.button(
        "▶ Classificar",
        type="primary",
        disabled=not (user_text or "").strip(),
        use_container_width=True,
    )

if classify_clicked and (user_text or "").strip():
    with st.spinner("Classificando e extraindo entidades..."):
        result = classify_and_extract((user_text or "").strip())
    if result:
        st.session_state["last_result"] = result

# Exibe resultado persistido
result = st.session_state.get("last_result")
if result:
    st.divider()
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("### Classificação")
        st.metric(
            label=f"Classe {result['class_id']}",
            value=result["class_name"],
            delta=f"confiança: {result['confidence']:.1%}",
        )

    with col_right:
        st.markdown("### Top-3 classes")
        for entry in result["top3"]:
            pct = entry["prob"]
            st.markdown(f"**{entry['id']} — {entry['name']}**  `{pct:.1%}`")
            st.progress(float(pct))

    st.divider()
    st.markdown("### Entidades nomeadas")
    if result["entities"]:
        import pandas as pd
        st.dataframe(
            pd.DataFrame(result["entities"]).rename(
                columns={"text": "Entidade", "type": "Tipo", "score": "Score"}
            ),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("Nenhuma entidade detectada com score ≥ 0.90 após filtros de limpeza.")
