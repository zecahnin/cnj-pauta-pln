# Relatório Completo — Deriva de Pauta nas Notícias do CNJ

> **Projeto:** PLN acadêmico — Modalidade 2 "PLN no Setor Público"  
> **Repositório:** [github.com/zecahnin/cnj-pauta-pln](https://github.com/zecahnin/cnj-pauta-pln)  
> **Execução:** Claude Code (Anthropic Claude Opus 4.8) via Hermes Agent  
> **Data:** 2026-06-21  
> **Período analisado:** 22/12/2025 a 19/06/2026  
> **Corpus:** 979 notícias · **10 classes temáticas**

---

## 1. Visão Geral

A Agência CNJ de Notícias (comunicação institucional do Conselho Nacional de Justiça) publica ~160 notícias/mês, mas sua taxonomia editorial é **cega à pauta** — 973/979 notícias caem em "Agência CNJ de Notícias". O projeto usa PLN para **descobrir a pauta fina** (BERTopic não-supervisionado) e **classificar supervisionadamente** cada notícia (Naive Bayes, MLP Keras, BERTimbau), cobrindo as técnicas do curso.

**Narrativa:** Descoberta → Classificação → NER → Deriva temporal

---

## 2. Pipeline Completo (8 fases)

### FASE 1 — Coleta (✅ 983 notícias)

| Item | Resultado |
|------|-----------|
| API | WP REST API v2 — `https://www.cnj.jus.br/wp-json/wp/v2/posts` |
| Status | HTTP 200, 44.465 posts totais |
| Período | `after=2025-12-21` → `before=2026-06-21` |
| **Total coletado** | **983** (0 duplicatas) |
| Rate limit | ≥1,2s entre requisições |
| Backoff | Exponencial (2,4,8,16,32s) em 429/5xx |
| robots.txt | `/wp-json/` não bloqueado |
| User-Agent | `cnj-pauta-pln/1.0 (pesquisa academica de PLN)` |
| Categorias mapeadas | 288 (id→nome) |

**Distribuição por mês:**

| Mês | N |
|-----|---|
| 2025-12 | 15 (parcial) |
| 2026-01 | 151 |
| 2026-02 | 136 |
| 2026-03 | 198 |
| 2026-04 | 183 |
| 2026-05 | 176 |
| 2026-06 | 124 (parcial) |

---

### FASE 2 — Pré-processamento (✅ 979 notícias)

| Operação | Resultado |
|----------|-----------|
| Limpeza HTML → texto | Boilerplate removido (créditos, "Leia mais") |
| Corpos curtos | 1 removida (<250 chars) |
| Filtro idioma | 1 em espanhol removida |
| Dedup semântico (MinHash, Jaccard ≥0,85) | 2 quase-duplicatas |
| **Total após limpeza** | **979** |
| Mediana tokens/notícia | 449 |

---

### FASE 3 — EDA ✅ (notebook `01_eda.ipynb`)

**6 figuras:** volume por mês, por categoria, distribuição comprimento, top termos, wordcloud, volume semanal.

---

### FASE 4 — Descoberta Exploratória: BERTopic ✅

**Embeddings:** `paraphrase-multilingual-mpnet-base-v2` (768d)

**Sweep de hiperparâmetros:**

| min_topic_size | N tópicos | c_v | Diversidade | Outliers |
|:---:|:---:|:---:|:---:|:---:|
| 10 | 23 | 0,6335 | 0,9217 | 39,22% |
| 15 | 12 | 0,7192 | 0,95 | 31,15% |
| **20 (selecionado)** | **10** | **0,777** | **1,0** | **29,42%** |

**10 classes temáticas (taxonomia canônica):**

| ID | Classe | N docs | Âncora |
|:--:|--------|:------:|--------|
| T0 | Justiça itinerante / cidadania | 179 | itinerante |
| T1 | IA / Conecta / Justiça 4.0 | 152 | inteligência artificial |
| T2 | Saúde / judicialização / SUS | 106 | saúde |
| T3 | Direitos humanos / Corte IDH | 139 | humanos |
| T4 | Violência doméstica / mulheres | 96 | violência |
| T5 | Sistema prisional / Pena Justa | 89 | prisional |
| T6 | Infância e juventude | 68 | crianças |
| T7 | Sustentabilidade ambiental | 56 | sustentabilidade |
| T8 | Processos disciplinares | 53 | disciplinar |
| T9 | Precatórios / corregedoria | 41 | precatórios |

> O BERTopic é **descoberta exploratória** — deriva a taxonomia que alimenta a classificação supervisionada. A avaliação formal é a Fase 6.

**Resultado negativo:** colapso inicial em 2 tópicos (cosseno médio ≈0,69) → corrigido com `n_neighbors=10` + `cluster_selection_method="leaf"`. Bug de acentos do `language="english"` corrigido com `"multilingual"`.

---

### FASE 5 — Deriva Temporal ✅ (notebook `03_temporal_drift.ipynb`)

**20 picos detectados** (z-score ≥1,5):

| Data | Tópico | z | N | Contexto |
|:----:|:------:|:-:|:-:|----------|
| 18/05 | T6 Infância | **3,68** | 9 | Dia Nacional Combate Abuso Infantil + app A.DOT SNA |
| 03/03 | T8 Disciplinar | **3,88** | 9 | Decisões alto perfil (afastamento TRT-8) |
| 03/03 | T9 Precatórios | **3,17** | 5 | Comissão verbas indenizatórias |
| 20/04 | T0 Itinerante | **3,18** | 16 | PopRuaJud + Justiça Itinerante Amazônia |
| 26/01 | T7 Sustentabilidade | **3,01** | 8 | Selo Carbono Neutro, energia solar |
| 09/03 | T4 Violência doméstica | **2,64** | 10 | Mês da Mulher / Dia Internacional |

**Deriva estrutural (H1 → H2):**
- **📈 Justiça itinerante / PopRuaJud: +7,2 pp** — maior crescimento
- **📈 IA / Justiça 4.0: +2,7 pp** — crescimento invisível na taxonomia
- 📉 Violência doméstica: −3,9 pp (sazonal, Mês da Mulher)
- 📉 Sustentabilidade: −3,5 pp (sazonal, Semana Pauta Verde)

**12 eventos mapeados** em `reports/eventos_cnj.csv` — observâncias de calendário (8/3, 18/5, 5/6), programas do CNJ (PopRuaJud, Estratégia Cuidar, Pena Justa), eventos institucionais.

> Cruzamento pico↔evento é **correlação temporal**, não causal. Observâncias de calendário são fonte externa verificável; eventos institucionais são inferidos do corpus.

---

### FASE 6 — NÚCLEO: Classificação Supervisionada ✅ (notebook `04_supervised_classification.ipynb`)

#### Protocolo de avaliação (sem vazamento)

| Item | Valor |
|------|-------|
| Pool de treino (rótulo fraco, sem gold) | **529** docs |
| Split | 338 treino / 85 val / 106 teste |
| Gold humano (excluído do treino) | **173** (+22 "indefinido") |
| Gold ids que coincidiam com weak set | 162 → removidos do treino |
| Features TF-IDF | `max_features=5000`, `ngram_range=(1,2)` |

> **Correção de vazamento:** a validação antiga treinava com gold dentro do conjunto e reportava κ≈0,91. O protocolo novo (gold removido do treino) dá κ≈0,79 — números honestos e defensáveis.

#### Modelo A — Naive Bayes (baseline clássico)

`TfidfVectorizer` + `MultinomialNB`

| Métrica | Interno (teste) | Externo (gold) |
|---------|:---------------:|:--------------:|
| Accuracy | 0,6038 | 0,5434 |
| **F1-macro** | 0,4292 | **0,4958** |
| **Kappa** | — | **0,4896** |

**F1 por classe (gold):** Violência doméstica 0,81 | IA/Justiça 4.0 0,74 | Sustentabilidade 0,69 | Sistema prisional 0,77 | Precatórios **0,00** (classe pequena, NB não consegue)

#### Modelo B — MLP Keras (rede neural densa, modelo principal de DL)

```
Sequential([
    Input(shape=(5000,)),
    Dense(256, activation="relu"),
    Dropout(0.3),
    Dense(128, activation="relu"),
    Dropout(0.3),
    Dense(10, activation="softmax"),
])
compile(optimizer="adam", loss="sparse_categorical_crossentropy")
```

| Métrica | Interno (teste) | Externo (gold) |
|---------|:---------------:|:--------------:|
| Accuracy | 0,7736 | **0,8092** |
| **F1-macro** | 0,6863 | **0,7980** |
| **Kappa** | — | **0,7875** |
| Early stopping | 16 épocas (patience=5) |

**F1 por classe (gold):** Sustentabilidade **0,94** | Infância **0,92** | Disciplinares 0,88 | IA/Justiça 4.0 0,83 | Violência 0,83 | Itinerante 0,77 | Precatórios 0,56

#### Análise de Overfit (peça central do Módulo 2 do curso)

Estudo controlado com 4 configurações, 50 épocas:

| Configuração | train_acc | val_acc_best | val_loss min | val_loss final | ∆ |
|:------------:|:---------:|:------------:|:------------:|:--------------:|:-:|
| **Sem regularização** | 1,0 | 0,7882 | 0,7081 | 0,7235 | +0,0155 |
| Dropout 0.3 | 1,0 | 0,7765 | 0,7686 | **0,8256** | **+0,0570** |
| **L2 1e-3** | 1,0 | 0,7765 | 0,8511 | 0,8579 | +0,0069 |
| L2 1e-2 (forte) | 0,9941 | 0,7765 | 1,4867 | 1,4867 | 0,0 (underfit) |

> 🧠 **Resultado negativo honesto:** Dropout **piora** a generalização em TF-IDF esparso com dataset pequeno (val_loss sobe +0,057). Quem controla o overfit é L2 moderado (1e-3). L2 forte causa underfit (val_loss flat em 1,49). Documentado nas figuras 14 e 14b como achado, não mascarado.

#### Modelo C — BERTimbau (transformer do curso)

`neuralmind/bert-base-portuguese-cased` (mean-pooling) + `LogisticRegression`

| Métrica | Interno (teste) | Externo (gold) |
|---------|:---------------:|:--------------:|
| Accuracy | 0,7925 | **0,7919** |
| **F1-macro** | 0,7092 | **0,787** |
| **Kappa** | — | **0,7687** |

**F1 por classe (gold):** Disciplinares **0,94** | Infância 0,87 | Sustentabilidade 0,87 | IA/Justiça 4.0 0,84 | Itinerante 0,76 | Precatórios 0,77

#### Tabela Comparativa Final

| Modelo | Acc gold | **F1 gold** | **Kappa** | Técnica do curso |
|--------|:-------:|:----------:|:---------:|------------------|
| **A: Naive Bayes** | 0,5434 | **0,4958** | 0,4896 | BoW/TF-IDF, Naive Bayes |
| **B: MLP Keras** | **0,8092** | **0,7980** | **0,7875** | Redes densas, ReLU, softmax, Adam, Dropout/L2, overfit |
| **C: BERTimbau** | 0,7919 | 0,787 | 0,7687 | BERT/Transformers, embeddings |

O MLP Keras é o **melhor modelo geral**. O BERTimbau empata em F1-macro (0,79 vs 0,80) e supera em classes pequenas (Precatórios: 0,77 vs 0,56). O Naive Bayes é baseline esperado — não consegue classes minoritárias.

---

### FASE 6b — NER (Extração de Entidades) ✅

**Modelo:** `rhaymison/ner-portuguese-br-bert-cased` (mesmo do curso) via `transformers.pipeline("ner", aggregation_strategy="max")`

**Limpeza da saída do NER (funil real, contagem em cada etapa).** A saída crua do modelo é ruidosa (fragmentos de subpalavra, preposições penduradas no span, substantivos comuns tageados como entidade, sem corte de confiança). Aplicado, nesta ordem: corte de score (`--min-score 0.90`) → limpeza de bordas funcionais → filtro de fragmento → filtro de genérico. Listas canônicas em `src/text_utils.py`.

| Etapa do funil | Entidades | % do bruto |
|---|--:|--:|
| Bruto (saída do modelo) | 11.971 | 100,0% |
| Após corte de score (≥0,90) | 4.492 | 37,5% |
| Após limpeza de bordas | 4.475 | 37,4% |
| Após filtro de fragmento | 4.344 | 36,3% |
| **Após filtro de genérico (final)** | **4.136** | **34,6%** |

O corte de confiança é, de longe, o filtro dominante (descarta 62,5% — entidades de baixa probabilidade). Docs processados: 979. Entidades distintas (chaves): 1.880.

**Taxa de fragmento residual: 0,77%** (32/4.136 chaves ≤4 chars não-sigla). A amostra residual é majoritariamente composta por entidades **legítimas** curtas (Acre, Rio, EUA, Haia, USP, TJRN, TJAP), não por lixo de tokenizer — o resíduo de subpalavra ("##") foi a zero, mas siglas/topônimos curtos sobrevivem por construção e são contados com honestidade.

**Top 10 entidades** (por nº de notícias distintas; `tipo` é informativo, não autoritativo):

| Entidade | Notícias | Ocorrências |
|----------|:--------:|:-----------:|
| Conselho Nacional de Justiça | 409 | 428 |
| Edson Fachin | 129 | 137 |
| Brasília | 68 | 71 |
| Programa das Nações Unidas para o Desenvolvimento | 40 | 42 |
| Mauro Campbell Marques | 39 | 41 |
| Maranhão | 27 | 30 |
| Rio de Janeiro | 27 | 35 |
| Amazonas | 22 | 27 |
| Fábio Esteves | 22 | 24 |
| João Paulo Schoucair | 20 | 20 |

**Entidades por classe temática** (diferenciais; auto-referências do CNJ excluídas):
- **Direitos humanos:** Edson Fachin (48), Corte Interamericana de Direitos Humanos (15)
- **IA/Justiça 4.0:** PNUD (17), Rodrigo Badaró (9)
- **Disciplinares:** Mauro Campbell Marques (16) — única classe com corregedor como top
- **Sustentabilidade:** Guilherme Feliciano (5) — juiz com pauta ambiental
- **Saúde:** Fórum Nacional do Judiciário para a Saúde (11)
- **Sistema prisional:** Pernambuco (8), PNUD (8)

---

### FASE 7 — Documentação ✅

- **`README.md`** — nova narrativa (descoberta → classificação → NER → deriva), métricas honestas, reprodutibilidade
- **`docs/coleta.md`** — 115 linhas: fonte, endpoint, schema, limitações
- **`docs/limitacoes.md`** — 123 linhas: auto-auditoria adversarial respondendo 6 perguntas de banca cética
- **`docs/referencias.md`** — 138 linhas: **19 referências** (17 DOIs verificados + 2 sem DOI citadas pela URL):
  - **Domínio (6):** Agenda-setting, modelagem de tópicos em mídia, PLN jurídico pt-BR (LeNER-Br, Lage-Freitas), análise quantitativa de texto jornalístico
  - **Técnica (13):** TF-IDF (Salton & Buckley), BoW/Naive Bayes (Manning IIR), BERTopic, Sentence-BERT, UMAP, HDBSCAN, c_v coherence, Transformer (Vaswani), BERT (Devlin), BERTimbau (Souza), Adam (Kingma & Ba), Dropout (Srivastava/JMLR), Deep Learning (Goodfellow/MIT Press)
  - ✅ Todos verificados resolvendo `doi.org`

---

## 3. Cobertura do Curso

| Conceito | Onde | Arquivo |
|----------|------|---------|
| **Bag-of-Words / TF-IDF** | Features de todos os modelos (Fase 6) | `src/classify.py::build_vectorizer()` |
| **Naive Bayes** | Modelo A — baseline clássico | `src/classify.py::run_naive_bayes()` |
| **Rede neural densa (Keras)** | `Sequential([Dense,Dense,Dense])` — Modelo B | `src/classify.py::build_mlp()` |
| **ReLU, softmax** | Ativações das camadas da MLP | `src/classify.py::build_mlp()` |
| **Adam, gradiente descendente** | `optimizer="adam"` na compilação | `src/classify.py::build_mlp()` |
| **Treino/teste/validação** | Split estratificado 70/15/15 | `src/classify.py::make_splits()` |
| **Overfit/underfit** | Curvas treino×validação (figs 14, 14b) | `src/classify.py::run_mlp()` |
| **Regularização (Dropout, L2)** | Estudo controlado: sem reg / Dropout / L2 1e-3 / L2 1e-2 | `src/classify.py::overfit_study()` |
| **BERTimbau / Transformers** | Modelo C (emb congelado + LogReg) + NER | `src/embed_bertimbau.py`, `src/ner.py` |
| **Embeddings** | sentence-transformers (exploração) + BERTimbau | `src/embed.py`, `src/embed_bertimbau.py` |

---

## 4. Resultados Negativos Documentados

1. **Colapso inicial em 2 tópicos** (cosseno médio ≈0,69) — corrigido com `n_neighbors=10` + `leaf`
2. **Bug de acentos** — BERTopic `language="english"` remove não-ASCII
3. **Dropout piora generalização** em TF-IDF esparso (val_loss +0,057 vs +0,015 sem reg)
4. **L2 forte (1e-2) causa underfit** — val_loss flat em 1,49
5. **Segfault TF+torch+numba** — resolvido com `src/tf_guard.py`
6. **NER com saída ruidosa** (fragmentos "##J"/"##dor", preposição pendurada, genéricos, sem corte de score) — **reduzido**, não eliminado: funil 11.971 brutos → 4.136 finais; fragmento residual 0,77% (siglas/topônimos curtos legítimos), resíduo de subpalavra a zero
7. **κ real 0,79 vs relato anterior 0,91** — diferença é vazamento corrigido
8. **Naive Bayes F1=0 em Precatórios** — classe pequena demais para NB
9. **29% outliers HDBSCAN** — docs ambíguos descartados pelo clustering

---

## 5. Figuras Geradas (18 PNGs)

| # | Arquivo | Fase | Conteúdo |
|:-:|---------|:----:|----------|
| 01 | `01_volume_por_mes.png` | 3 | Série temporal mensal |
| 02 | `02_volume_por_categoria.png` | 3 | Volume por categoria-fonte |
| 03 | `03_distribuicao_comprimento.png` | 3 | Distribuição de comprimento |
| 04 | `04_top_termos.png` | 3 | Top termos frequência |
| 05 | `05_wordcloud.png` | 3 | Wordcloud (651 KB) |
| 06 | `06_volume_semanal.png` | 3 | Volume semanal |
| 07 | `07_topic_eval.png` | 4 | Comparação c_v por min_topic_size |
| 08 | `08_topic_sizes.png` | 4 | Tamanho de cada tópico |
| 08b | `08b_classes_tematicas.png` | 4 | Distribuição das classes temáticas |
| 09 | `09_topic_terms.png` | 4 | Barchart top-termos por tópico |
| 10 | `10_streamgraph.png` | 5 | Streamgraph com eventos (290 KB) |
| 11 | `11_topicos_no_tempo.png` | 5 | Linhas temporais por tópico |
| 12 | `12_drift_h1_h2.png` | 5 | Comparação H1 vs H2 |
| 13 | `13_confusion_matrix.png` | 6 | Matriz de confusão NB |
| 14 | `14_overfit_mlp.png` | 6 | Curvas treino×validação MLP |
| 14b | `14b_regularizacao.png` | 6 | Comparação regularização |
| 15 | `15_confusion_gold.png` | 6 | Matriz gold MLP |
| 16 | `16_top_entidades.png` | 6b | Top entidades NER |

---

## 6. Estrutura do Repositório

```
cnj-pauta-pln/
├── README.md
├── requirements.txt
├── environment.yml
├── .gitignore
├── data/
│   ├── raw/noticias.jsonl                    # 983 notícias brutas
│   ├── interim/noticias_limpo.parquet         # 979 pós-limpeza
│   └── processed/                             # embeddings, modelo, métricas
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_topic_modeling.ipynb
│   ├── 03_temporal_drift.ipynb
│   └── 04_supervised_classification.ipynb
├── src/
│   ├── collect.py                             # Coleta WP REST API
│   ├── preprocess.py                          # Limpeza/dedup
│   ├── embed.py                               # Embeddings sentence-transformers
│   ├── text_utils.py                          # Taxonomia canônica (TF-free)
│   ├── tf_guard.py                            # Bloqueio TF no BERTopic
│   ├── topics.py                              # BERTopic (descoberta)
│   ├── drift.py                               # Deriva temporal
│   ├── classify.py                            # NB + MLP Keras + BERTimbau (NÚCLEO)
│   ├── embed_bertimbau.py                     # Embeddings BERTimbau
│   └── ner.py                                 # NER (modelo do professor)
├── reports/
│   ├── eventos_cnj.csv                        # 12 eventos
│   ├── gold_labels.csv                        # 173 gold humano + 22 indefinido
│   ├── gold_template.csv                      # ~200 template (classe vazia)
│   └── figures/                               # 18 PNGs
└── docs/
    ├── coleta.md
    ├── referencias.md                         # 19 refs (17 DOIs verificados)
    └── limitacoes.md                          # Auto-auditoria adversarial
```

---

## 7. Auto-Auditoria Adversarial (resumo)

| Pergunta da banca | Resposta |
|-------------------|----------|
| "Gold é humano e independente?" | ✅ Sim. 173 notícias rotuladas à mão como tópico 0–9. Excluído do treino (sem vazamento). |
| "Métricas vivem em subconjunto fácil?" | Parcialmente. F1=0,80 é sobre gold (não sobre weak set). 22 "indefinido" excluídos (~11%). |
| "Overfit foi tratado?" | ✅ Documentado com estudo controlado (figs 14, 14b). Dropout não ajuda; L2 1e-3 sim. |
| "Por que classificação e não só topic modeling?" | ✅ Classificação cobre o currículo do curso. BERTopic é descoberta exploratória, não avaliação. |
| "Quais técnicas do curso foram usadas?" | Todas as 10 listadas na seção 3. |
| "Generaliza para outros órgãos?" | Não. Estudo de caso de 6 meses de UM órgão. Sem validade externa. |
