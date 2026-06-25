"""Constantes e utilidades de texto compartilhadas (SEM dependências pesadas).

Este módulo NÃO importa bertopic/umap/torch/tensorflow — pode ser importado com
segurança tanto pelo pipeline BERTopic (que bloqueia TF via `tf_guard`) quanto
pela classificação supervisionada da Fase 6 (que USA TensorFlow/Keras). É a
fonte canônica única da taxonomia temática e da lista de stopwords, para que a
descoberta (Fase 4), a deriva (Fase 5) e a classificação (Fase 6) nunca
divirjam nos rótulos ou no vocabulário.
"""

from __future__ import annotations

import csv
from pathlib import Path

# --- Taxonomia temática (corpus de 2 anos, 4.394 notícias) --------------------
# Consolidada a partir de 46 tópicos brutos do BERTopic em 30 classes
# interpretáveis, decididas pelo dono do projeto (ver reports/taxonomia_map.csv).
TAXONOMY = {
    0: "Processos disciplinares",
    1: "Equidade racial",
    2: "Violência doméstica / mulheres",
    3: "Conciliação e mediação",
    4: "IA / Justiça 4.0",
    5: "Corregedoria / Inspeção",
    6: "Justiça Itinerante / cidadania",
    7: "Socioeducativo",
    8: "Participação feminina",
    9: "Direitos humanos / Corte IDH",
    10: "Institucional / Gestão",
    11: "Precatórios",
    12: "Transparência",
    13: "LGBTQIA+",
    14: "Sistema prisional",
    15: "Inclusão PCDs",
    16: "Inovação",
    17: "Regularização fundiária",
    18: "Domicílio Judicial Eletrônico",
    19: "Justiça Eleitoral",
    20: "Linguagem simples",
    21: "Saúde / judicialização",
    22: "ENAC / Exame de cartórios",
    23: "Sustentabilidade / Pauta verde",
    24: "Execuções fiscais",
    25: "PopRuaJud",
    26: "Trabalho escravo / tráfico",
    27: "Litigância / ações coletivas",
    28: "Infância e juventude",
    29: "Conflitos fundiários",
}

# Inverso da TAXONOMY: nome de classe consolidada -> id (0..29). Usado para
# traduzir o `classe_final` (texto) do mapa de consolidação no id numérico.
CLASS_NAME_TO_ID = {name: cid for cid, name in TAXONOMY.items()}

# --------------------------------------------------------------------------- #
# Fusão para 12 classes (decisão do dono, 24/06/2026).
#
# Motivação (medida nos dados, não no chute): a taxonomia de 30 classes tem 4
# classes SEM nenhum gold (3 Conciliação, 11 Precatórios, 12 Transparência, 26
# Trabalho escravo) e várias com n<6, o que torna o macro-F1 instável e infla a
# confusão entre vizinhos temáticos. As fusões abaixo absorvem 35 dos 149 erros
# do MLP vs gold (acc 0.503 -> ~0.62 sem nem retreinar) e sobem o suporte médio
# de ~10 para ~25 docs/classe. Critérios por fusão: (1) coesão temática,
# (2) pares que mais se confundem na matriz vs gold, (3) suporte final >= ~15.
#
# A TAXONOMY de 30 classes permanece INTACTA (drift/topics/ner dependem dela);
# o esquema fundido é OPT-IN via `classify.py --merged`.
# --------------------------------------------------------------------------- #
TAXONOMY_MERGED = {
    0: "Gestão institucional e transparência",
    1: "Corregedoria, disciplina e cartórios",
    2: "Tecnologia, inovação e Justiça 4.0",
    3: "Direitos humanos, igualdade e diversidade",
    4: "Violência doméstica e proteção à mulher",
    5: "Acesso à justiça, cidadania e conciliação",
    6: "Questões fundiárias",
    7: "Infância, juventude e socioeducativo",
    8: "Sistema prisional",
    9: "Judicialização, execução fiscal e precatórios",
    10: "Sustentabilidade / Pauta verde",
    11: "Justiça Eleitoral",
}

# Classe fundida (0-11) -> lista de classes consolidadas (0-29) que a compõem.
# Deve cobrir as 30 classes EXATAMENTE uma vez (validado no import).
MERGE_GROUPS = {
    0: [10, 12],            # Institucional + Transparência
    1: [5, 0, 22],          # Corregedoria + Proc. disciplinares + ENAC/cartórios
    2: [4, 16, 18],         # IA + Inovação + Domicílio Judicial Eletrônico
    3: [1, 8, 9, 13, 26, 15],  # Equidade racial+fem.+DH/IDH+LGBTQIA++trab.escravo+PCD
    4: [2],                 # Violência doméstica (isolada: sinal limpo, F1 0.84)
    5: [6, 25, 20, 3],      # Itinerante + PopRua + Linguagem simples + Conciliação
    6: [17, 29],            # Regularização + Conflitos fundiários
    7: [28, 7],             # Infância e juventude + Socioeducativo
    8: [14],                # Sistema prisional (isolado)
    9: [21, 24, 11, 27],    # Saúde/judic. + Exec. fiscal + Precatórios + Litigância
    10: [23],               # Sustentabilidade (isolada)
    11: [19],               # Justiça Eleitoral (isolada)
}
MERGE_MAP = {old: new for new, olds in MERGE_GROUPS.items() for old in olds}
assert sorted(MERGE_MAP) == list(range(len(TAXONOMY))), (
    "MERGE_MAP deve cobrir as 30 classes da TAXONOMY exatamente uma vez")


def merge_class_id(classe_id: int) -> int:
    """Classe consolidada (0-29) -> classe fundida (0-11). Preserva -1 (outlier)."""
    if classe_id == -1:
        return -1
    return MERGE_MAP[int(classe_id)]


# --------------------------------------------------------------------------- #
# Fusão para 10 classes (decisão do dono, 25/06/2026).
#
# É o esquema de 12 classes + DUAS fusões, escolhidas por dados (análise pós-hoc
# da matriz de confusão das 12 classes vs gold, 3 modelos):
#   12cls 0 Gestão  + 1 Corregedoria  -> "Gestão, governança e corregedoria"
#       (2ª maior confusão, 34x; tematicamente coeso = administração interna do
#        Judiciário. Preferido a Gestão+DH, que daria balde incoerente de n=97.)
#   12cls 5 Acesso  + 11 Justiça Eleitoral -> "Acesso à justiça, cidadania e
#        Justiça Eleitoral" (Eleitoral é a classe mais fraca: n=8, F1 0.36; cabe
#        em cidadania/participação democrática.)
# Ganho estimado (pós-hoc, sem retreino): F1-macro do MLP ~0.71.
#
# Definido direto em espaço 30->10 (e renumerado 0-9) para ficar inspecionável.
# --------------------------------------------------------------------------- #
TAXONOMY_10 = {
    0: "Gestão, governança e corregedoria",
    1: "Tecnologia, inovação e Justiça 4.0",
    2: "Direitos humanos, igualdade e diversidade",
    3: "Violência doméstica e proteção à mulher",
    4: "Acesso à justiça, cidadania e Justiça Eleitoral",
    5: "Questões fundiárias",
    6: "Infância, juventude e socioeducativo",
    7: "Sistema prisional",
    8: "Judicialização, execução fiscal e precatórios",
    9: "Sustentabilidade / Pauta verde",
}

# Classe fundida (0-9) -> classes consolidadas (0-29) que a compõem.
MERGE_GROUPS_10 = {
    0: [10, 12, 5, 0, 22],     # (12cls 0 Gestão) + (12cls 1 Corregedoria/cartórios)
    1: [4, 16, 18],            # Tecnologia / Justiça 4.0
    2: [1, 8, 9, 13, 26, 15],  # Direitos humanos, igualdade e diversidade
    3: [2],                    # Violência doméstica (isolada)
    4: [6, 25, 20, 3, 19],     # (12cls 5 Acesso) + (12cls 11 Justiça Eleitoral)
    5: [17, 29],               # Questões fundiárias
    6: [28, 7],                # Infância e juventude + Socioeducativo
    7: [14],                   # Sistema prisional (isolado)
    8: [21, 24, 11, 27],       # Judicialização + Exec. fiscal + Precatórios + Litig.
    9: [23],                   # Sustentabilidade (isolada)
}
MERGE_MAP_10 = {old: new for new, olds in MERGE_GROUPS_10.items() for old in olds}
assert sorted(MERGE_MAP_10) == list(range(len(TAXONOMY))), (
    "MERGE_MAP_10 deve cobrir as 30 classes da TAXONOMY exatamente uma vez")
# Consistência: o esquema de 10 deve ser um agrupamento (coarsening) do de 12.
assert all(len({MERGE_MAP[o] for o in olds}) >= 1 for olds in MERGE_GROUPS_10.values())

# Mapa de consolidação (decisão do dono): tópico bruto do BERTopic -> classe
# consolidada. É a FONTE DE VERDADE para rotular cada tópico por classe; NÃO se
# assume que a numeração do BERTopic (por tamanho) case com a taxonomia.
_PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONSOLIDATION_MAP_CSV = _PROJECT_ROOT / "reports" / "taxonomia_map.csv"


def load_consolidation_map(path: str | Path | None = None) -> dict[int, str]:
    """Lê reports/taxonomia_map.csv -> {tópico_bruto: nome_da_classe_final}.

    Valida que todo `classe_final` existe na TAXONOMY (senão a inversão para id
    falharia silenciosamente). Levanta ValueError em rótulo desconhecido.
    """
    path = Path(path) if path is not None else CONSOLIDATION_MAP_CSV
    mapping: dict[int, str] = {}
    with path.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            raw = int(row["topico_id"])
            name = row["classe_final"].strip()
            if name not in CLASS_NAME_TO_ID:
                raise ValueError(
                    f"classe_final '{name}' (tópico {raw}) não está na TAXONOMY")
            mapping[raw] = name
    return mapping


def topic_to_class_id(raw_topic: int, consolidation_map: dict[int, str]) -> int:
    """Tópico bruto/reduzido -> id de classe consolidada (0..29).

    Outlier (-1) é mantido como -1. KeyError se o tópico não estiver no mapa
    (sinaliza que a numeração do BERTopic mudou — condição de PARADA).
    """
    if raw_topic == -1:
        return -1
    return CLASS_NAME_TO_ID[consolidation_map[raw_topic]]


# Regra do dono (registrada para o futuro): numa janela recente, classe com
# menos de MIN_CLASS_DOCS_RECENT documentos não tem massa suficiente para
# classificar/avaliar com segurança e deve ser colapsada em 'Outros'. Em
# 21/06/2026 nenhuma dispara na janela de 18 meses (mínimo ~34, ENAC), mas a
# regra fica viva: se a janela ou o corpus mudar, as classes pequenas colapsam
# automaticamente. Ver reports/diagnostico_janela.csv.
MIN_CLASS_DOCS_RECENT = 30
OUTROS_LABEL = "Outros"


def small_classes_for_window(
        window_counts: dict[int, int],
        min_docs: int = MIN_CLASS_DOCS_RECENT) -> set[int]:
    """Ids de classe que colapsam em 'Outros' por terem < min_docs na janela.

    `window_counts` é {classe_id: nº de docs na janela}; classe ausente conta
    como 0 (também colapsa). Retorna o conjunto (vazio quando todas têm massa).
    """
    return {cid for cid in TAXONOMY if window_counts.get(cid, 0) < min_docs}


TAXONOMY_ANCHORS = {
    0: "disciplinar",
    1: "racial",
    2: "violência",
    3: "conciliação",
    4: "inteligência artificial",
    5: "inspeção",
    6: "itinerante",
    7: "socioeducativo",
    8: "feminina",
    9: "humanos",
    10: "encontro",
    11: "precatórios",
    12: "transparência",
    13: "lgbtqia",
    14: "prisional",
    15: "deficiência",
    16: "inovação",
    17: "fundiária",
    18: "domicílio",
    19: "eleitoral",
    20: "linguagem",
    21: "saúde",
    22: "enac",
    23: "sustentabilidade",
    24: "fiscais",
    25: "popruajud",
    26: "escravo",
    27: "litigância",
    28: "crianças",
    29: "fundiários",
}

# Stopwords institucionais/onipresentes (espelham as da EDA) — não discriminam
# pauta e poluiriam tanto a representação c-TF-IDF (Fase 4) quanto as features
# TF-IDF dos classificadores (Fase 6).
DOMAIN_STOP = {
    "cnj", "conselho", "nacional", "justica", "justiça", "judiciario",
    "judiciário", "tribunal", "tribunais", "poder", "brasil", "brasileiro",
    "brasileira", "país", "pais", "ainda", "sobre", "durante", "ser", "após",
    "apos", "todos", "todas", "além", "alem", "dia", "dias", "ano", "anos",
    "mês", "mes", "meses", "secao", "seção", "presidente", "ministro",
    "ministra", "federal", "estado", "estadual", "geral", "primeira",
    "segundo", "segunda", "número", "numero", "parte", "forma", "meio",
    "grande", "maior", "novo", "nova", "novos", "novas", "três", "tres",
    "dois", "duas", "feira", "terça", "terca", "quarta", "quinta", "sexta",
    "auxiliar", "presidência", "presidencia",
    # Ruído de fragmentos de número de processo (ex.: 0007147-67.2024.2.00.0000)
    "0000", "00",
}


def get_stopwords() -> list[str]:
    """Stopwords pt-BR (NLTK) unidas às institucionais do domínio."""
    import nltk
    nltk.download("stopwords", quiet=True)
    from nltk.corpus import stopwords
    return sorted(set(stopwords.words("portuguese")) | DOMAIN_STOP)


# --- Listas canônicas para limpeza de NER (Fase 6b) ----------------------------
# Fonte canônica única, no mesmo espírito de DOMAIN_STOP: chaves normalizadas
# (minúsculas, sem acento, espaços colapsados — ver _norm_key em src/ner.py).
# O NER pt-BR tagueia muito substantivo comum/adjetivo institucional como
# entidade; estas listas separam "entidade nomeada informativa" de ruído.

# Substantivos comuns / adjetivos genéricos que o NER marca como entidade mas
# que não são entidades nomeadas informativas (poluem o Top N). Descartados.
GENERIC_ENTITY_STOP = {
    "judiciario", "brasil", "federal", "nacional", "publico", "justica",
    "poder", "governo", "estado", "uniao", "ministerio", "conselho", "pais",
    "republica", "regiao", "sul", "norte", "nordeste", "sudeste",
    "centro-oeste", "tribunal", "ministro", "juiz", "juiza", "desembargador",
    "presidente", "poder judiciario",
}

# Auto-referências do próprio CNJ: ficam no parquet (são entidades de fato), mas
# são excluídas da análise diferencial por classe (entidades_por_classe.csv),
# onde só interessa o que distingue uma classe das demais.
ENTITY_SELF_REF = {
    "conselho nacional de justica", "cnj",
}

# Siglas curtas legítimas: escapam do filtro de fragmento (len curto + PER/ORG),
# porque são entidades nomeadas reais apesar de poucos caracteres.
ENTITY_ACRONYM_WHITELIST = {
    "cnj", "stf", "stj", "tst", "tse", "trf", "oab", "mp", "mpf", "dpu",
    "cnmp", "sus", "idh", "onu", "pnud", "ipea", "ibge",
}

# Palavras funcionais (preposições, artigos, conjunções) penduradas nas bordas
# de um span do NER ("tribunal de justica do" -> "tribunal de justica"). São
# removidas apenas do início e do fim, nunca do miolo do span.
ENTITY_EDGE_WORDS = {
    "de", "do", "da", "dos", "das", "no", "na", "nos", "nas", "e", "o", "a",
    "os", "as", "em", "para", "por", "com", "ao", "à",
}
