"""Constantes e utilidades de texto compartilhadas (SEM dependências pesadas).

Este módulo NÃO importa bertopic/umap/torch/tensorflow — pode ser importado com
segurança tanto pelo pipeline BERTopic (que bloqueia TF via `tf_guard`) quanto
pela classificação supervisionada da Fase 6 (que USA TensorFlow/Keras). É a
fonte canônica única da taxonomia temática e da lista de stopwords, para que a
descoberta (Fase 4), a deriva (Fase 5) e a classificação (Fase 6) nunca
divirjam nos rótulos ou no vocabulário.
"""

from __future__ import annotations

# --- Taxonomia temática (Fase 4: consolidação dos tópicos do BERTopic) ---------
# tópico/classe id -> nome interpretável. Mantida em 10 classes (faixa 6-10),
# porque cada tópico é semanticamente distinto e o gold humano já foi anotado
# contra estes rótulos.
TAXONOMY = {
    0: "Justiça itinerante / cidadania",
    1: "IA / Conecta / Justiça 4.0",
    2: "Saúde / judicialização / SUS",
    3: "Direitos humanos / Corte IDH",
    4: "Violência doméstica / mulheres",
    5: "Sistema prisional / Pena Justa",
    6: "Infância e juventude",
    7: "Sustentabilidade ambiental",
    8: "Processos disciplinares / sessões",
    9: "Precatórios / corregedoria",
}

# Palavras-âncora esperadas em cada tópico (id -> termo que DEVE aparecer na
# representação c-TF-IDF). Permitem verificar, após cada execução do BERTopic,
# que a numeração dos tópicos não mudou e a TAXONOMY continua válida.
TAXONOMY_ANCHORS = {
    0: "itinerante",
    1: "inteligência artificial",
    2: "saúde",
    3: "humanos",
    4: "violência",
    5: "prisional",
    6: "crianças",
    7: "sustentabilidade",
    8: "disciplinar",
    9: "precatórios",
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
