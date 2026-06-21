"""Constantes e utilidades de texto compartilhadas (SEM dependências pesadas).

Este módulo NÃO importa bertopic/umap/torch/tensorflow — pode ser importado com
segurança tanto pelo pipeline BERTopic (que bloqueia TF via `tf_guard`) quanto
pela classificação supervisionada da Fase 6 (que USA TensorFlow/Keras). É a
fonte canônica única da taxonomia temática e da lista de stopwords, para que a
descoberta (Fase 4), a deriva (Fase 5) e a classificação (Fase 6) nunca
divirjam nos rótulos ou no vocabulário.
"""

from __future__ import annotations

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
