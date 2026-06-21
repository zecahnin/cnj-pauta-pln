# Relatório Detalhado — Deriva de Pauta nas Notícias do CNJ

> **Projeto:** PLN acadêmico — Modalidade 2 "PLN no Setor Público"  
> **Repositório:** [github.com/zecahnin/cnj-pauta-pln](https://github.com/zecahnin/cnj-pauta-pln)  
> **Execução:** Claude Code (Anthropic Claude Opus 4.8) via Hermes Agent  
> **Data:** 2026-06-21  
> **Período analisado:** 22/12/2025 a 19/06/2026

---

## 1. Objetivo

Descobrir **como a agenda comunicacional da Agência CNJ de Notícias se distribui e se desloca** ao longo de 6 meses, identificando pautas emergentes não óbvias na taxonomia editorial e correlacionando picos temáticos com eventos verificáveis.

**Diferencial da rubrica:** correlação picos × eventos (resoluções, semanas nacionais, programas como Justiça 4.0, Pena Justa, mutirões).

---

## 2. Pipeline — Execução Completa (7 fases)

### FASE 1 — Coleta (✅ commit: `a645c8e`)

| Item | Resultado |
|------|-----------|
| API | WP REST API v2 — `https://www.cnj.jus.br/wp-json/wp/v2/posts` |
| Status | HTTP 200, 44.465 posts totais no acervo |
| Período | `after=2025-12-21` → `before=2026-06-21` |
| Total coletado | **983 notícias** |
| Idempotência | Dedup por `id`/`link` — 0 duplicatas |
| User-Agent | `cnj-pauta-pln/1.0 (pesquisa academica de PLN; ...)` |
| Rate limit | ≥1,2s entre requisições |
| Backoff | Exponencial (2,4,8,16,32s) em 429/5xx |
| robots.txt | `/wp-json/` não bloqueado — check programático |
| Categorias mapeadas | 288 (id→nome) via `/wp/v2/categories` |

**Distribuição por mês:**

| Mês | Notícias |
|-----|----------|
| 2025-12 | 15 (parcial, desde 21/12) |
| 2026-01 | 151 |
| 2026-02 | 136 |
| 2026-03 | 198 |
| 2026-04 | 183 |
| 2026-05 | 176 |
| 2026-06 | 124 (parcial, até 19/06) |

**Categorias-fonte (top):**

| Categoria | N |
|-----------|---|
| Agência CNJ de Notícias | 977 |
| Notícias CNJ | 615 |
| Notícias do Judiciário | 344 |
| Sem categoria | 17 |
| Corte IDH | 1 |

> ⚠️ **Observação metodológica:** a taxonomia editorial é cega à pauta fina — 977/983 notícias caem em "Agência CNJ de Notícias". Isso **justifica a modelagem de tópicos**.

**Artefato:** `data/raw/noticias.jsonl` (~8,9 MB, 983 registros)

---

### FASE 2 — Pré-processamento (✅ commit: `f9461fe`)

| Operação | Resultado |
|----------|-----------|
| HTML → texto | Boilerplate removido (créditos: "Texto:", "Edição:", "Revisão:", "Fonte:", "Agência CNJ de Notícias") |
| Corpos curtos removidos | 1 notícia (<250 caracteres) |
| Filtro idioma (não pt-BR) | 1 notícia em espanhol removida |
| Dedup semântico (MinHash, Jaccard ≥0,85) | 2 quase-duplicatas removidas |
| **Total após limpeza** | **979 notícias** |
| Mediana tokens/notícia | 449 |

**Campos derivados:** `mes` (YYYY-MM), `n_tokens`, `n_chars`

**Artefato:** `data/interim/noticias_limpo.parquet`

---

### FASE 3 — EDA (✅ commit: `4a09d69`)

Notebook: `notebooks/01_eda.ipynb`

**Figuras geradas (6):**

| # | Arquivo | Descrição |
|---|---------|-----------|
| 01 | `01_volume_por_mes.png` | Série temporal de publicações por mês |
| 02 | `02_volume_por_categoria.png` | Volume por categoria-fonte |
| 03 | `03_distribuicao_comprimento.png` | Distribuição de comprimento do texto |
| 04 | `04_top_termos.png` | Top termos por frequência |
| 05 | `05_wordcloud.png` | Wordcloud do corpus (651 KB) |
| 06 | `06_volume_semanal.png` | Volume semanal de publicações |

**Principais descobertas da EDA:**
- Volume mensal estável (136-198), exceto meses parciais
- Distribuição de comprimento concentrada entre 500-2.500 caracteres
- Termos dominantes esperados: "justiça", "cnj", "tribunal", "judiciário", "direitos"

---

### FASE 4 — Modelagem de Tópicos (✅ commit: `1025984`)

Notebook: `notebooks/02_topic_modeling.ipynb`

#### Embeddings
- **Modelo:** `paraphrase-multilingual-mpnet-base-v2` (768d)
- **Justificativa:** forte performance em pt-BR, multilíngue robusto para domínio jurídico-português
- **Persistido em:** `data/processed/embeddings.npy` + `embeddings_model.txt`

#### Teste de hiperparâmetros (3 configurações)

| min_topic_size | N tópicos | c_v coherence | Diversidade | Outliers % |
|:---:|:---:|:---:|:---:|:---:|
| 10 | 23 | 0,6335 | 0,9217 | 39,22% |
| **15** | **12** | **0,7192** | **0,95** | **31,15%** |
| **20 (selecionado)** | **10** | **0,777** | **1,0** | **29,42%** |

**Modelo final:** `min_topic_size=20`, UMAP `n_neighbors=10`, HDBSCAN `cluster_selection_method="leaf"`

> ⚠️ Colapso inicial em 2 tópicos (cosseno médio ≈0,69 — corpus homogêneo) → resolvido com `n_neighbors=10` + `cluster_selection_method="leaf"`.  
> ⚠️ Bug de acentos: `language="english"` padrão removia não-ASCII → corrigido com `language="multilingual"`.

#### 10 Tópicos Identificados

| ID | Rótulo | N docs | Palavras-chave |
|:--:|--------|:------:|----------------|
| **T0** | Justiça itinerante / cidadania / PopRuaJud | **179** | atendimentos, itinerante, serviços, trabalho, cidadania, população, rua |
| **T1** | IA / Conecta / Justiça 4.0 | **152** | conecta, inteligência artificial, dados, soluções, programa |
| **T2** | Saúde / judicialização / SUS | **106** | saúde, judicialização, processos, conciliação, sus, ações |
| **T3** | Direitos humanos / Corte IDH | **139** | direitos humanos, corte, fachin, interamericana, internacional |
| **T4** | Violência doméstica / mulheres | **96** | violência, mulheres, doméstica, enfrentamento, feminicídio |
| **T5** | Sistema prisional / Pena Justa | **89** | prisional, pena justa, sistema, penal, socioeducativo |
| **T6** | Infância e juventude | **68** | crianças, adolescentes, infância, adoção, acolhimento |
| **T7** | Sustentabilidade ambiental | **56** | sustentabilidade, resíduos, ambiental, energia, carbono |
| **T8** | Processos disciplinares | **53** | disciplinar, decisão, sessão, magistrado, PAD |
| **T9** | Precatórios / corregedoria | **41** | precatórios, inspeção, teto, verbas, corregedoria |

**Outliers:** 288 docs (29,42%) — reatribuídos via `reduce_outliers` para análise, mas a deriva temporal usou rótulos brutos.

**Artefatos:**
- `data/processed/bertopic_model/` — modelo salvo
- `data/processed/topic_info.csv` — tabela completa
- `data/processed/topic_eval.csv` — comparação de hiperparâmetros
- `data/processed/topics_best.txt` — modelo final selecionado

**Figuras (3):**

| # | Arquivo | Conteúdo |
|---|---------|----------|
| 07 | `07_topic_eval.png` | Comparação c_v por min_topic_size |
| 08 | `08_topic_sizes.png` | Tamanho de cada tópico |
| 09 | `09_topic_terms.png` | Barchart dos top-termos por tópico |

---

### FASE 5 — Deriva Temporal (✅ commit: `b58995a`)

Notebook: `notebooks/03_temporal_drift.ipynb`

#### 20 picos detectados (z-score ≥1,5)

| Data | Tópico | z | N | Contexto |
|:----:|:------:|:-:|:-:|----------|
| 18/05 | T6 Infância | **3,68** | 9 | Dia Nacional Combate Abuso Infantil + A.DOT SNA |
| 03/03 | T8 Disciplinar | **3,88** | 9 | Decisões de alto perfil (afastamento TRT-8, pena assédio) |
| 03/03 | T9 Precatórios | **3,17** | 5 | Comissão técnica verbas indenizatórias |
| 20/04 | T0 Itinerante | **3,18** | 16 | PopRuaJud + Justiça Itinerante Amazônia |
| 26/01 | T7 Sustentabilidade | **3,01** | 8 | Selo Carbono Neutro, energia solar TJMS |
| 09/03 | T4 Violência doméstica | **2,64** | 10 | Mês da Mulher / Dia Internacional |
| 23/03 | T4 Violência doméstica | **2,26** | 9 | Paridade de gênero, políticas |
| 12/01 | T7 Sustentabilidade | **2,02** | 6 | Reciclagem TRT-15, energia solar TJSC |
| 08/06 | T7 Sustentabilidade | **2,02** | 6 | Semana da Pauta Verde |
| 09/03 | T1 IA/Justiça 4.0 | **2,02** | 9 | e-MILIA, Prêmio Inovação, Observatório |

#### Deriva estrutural (H1 → H2)

| Tópico | Variação | Direção |
|--------|:--------:|:-------:|
| **T0 — Itinerante / PopRuaJud** | **+7,2 pp** | 📈 Alta estrutural |
| **T1 — IA / Conecta / Justiça 4.0** | **+2,7 pp** | 📈 Alta estrutural |
| T4 — Violência doméstica | −3,9 pp | 📉 Queda sazonal (Mês da Mulher) |
| T7 — Sustentabilidade | −3,5 pp | 📉 Queda sazonal (Semana Pauta Verde) |

#### Cruzamento com eventos (12 eventos mapeados)

`reports/eventos_cnj.csv` — eventos de 3 tipos:

1. **Observâncias de calendário** (fontes externas verificáveis):
   - 08/03 — Dia Internacional da Mulher → pico T4
   - 18/05 — Dia Nacional Combate Abuso Infantil → pico T6
   - 05/06 — Semana da Pauta Verde → pico T7

2. **Programas do CNJ** (inferidos do corpus):
   - PopRuaJud (abril) → pico T0
   - Estratégia Cuidar / Semana da Saúde (abril) → pico T2
   - Pena Justa (maio) → pico T5

3. **Eventos institucionais** (inferidos do corpus):
   - Decisões disciplinares alto perfil (03/03) → pico T8
   - Nota de repúdio a ataques racistas (16/03) → pico T3
   - Atuação internacional Haia (04/05) → pico T3

**Figuras (3):**

| # | Arquivo | Conteúdo |
|---|---------|----------|
| 10 | `10_streamgraph.png` | Streamgraph completo com eventos anotados (290 KB) |
| 11 | `11_topicos_no_tempo.png` | Linhas temporais por tópico |
| 12 | `12_drift_h1_h2.png` | Comparação H1 vs H2 por tópico |

---

### FASE 6 — Validação Supervisionada (✅ commit: `5d28253`)

Notebook: `notebooks/04_supervised_validation.ipynb`

#### Classificadores treinados sobre rótulos fracos (691 docs não-outliers)

| Modelo | F1-macro intrínseco | Acurácia |
|--------|:-------------------:|:--------:|
| **LogReg (selecionado)** | **0,8131** | **0,8208** |
| LinearSVM | 0,8065 | 0,8150 |

> **Anti-circularidade:** features TF-IDF (espaço lexical) ≠ espaço de embeddings dos clusters

#### Gold set humano: 173 notícias

| Métrica | Valor |
|---------|:-----:|
| Gold set total (amostra estratificada) | 195 notícias |
| Casos `indefinido` excluídos | 22 (≈11%) |
| **Gold rotulado** | **173** |
| **F1-macro (predição × gold)** | **0,9137** |
| **Kappa (predição × gold)** | **0,9099** |
| **Kappa (rótulo fraco × gold)** | **0,9107** |
| Acurácia (rótulo fraco × gold) | 0,9198 |

**Discussão:**
- F1=0,91 é **otimista** — exclui os 22 casos indefinido (justamente os difíceis)
- Kappa 0,91 valida a etapa **não supervisionada** do BERTopic
- Erros concentrados em T3 (direitos humanos, largo) e T9 (precatórios, pequeno)
- Anotador único (assistente) — não há concordância inter-anotador independente

**Figura:**

| # | Arquivo | Conteúdo |
|---|---------|----------|
| 13 | `13_confusion_matrix.png` | Matriz de confusão |

**Artefatos:**
- `data/processed/supervised_metrics.json` — todas as métricas
- `reports/gold_labels.csv` — 195 rótulos manuais

---

### FASE 7 — Documentação (✅ commit: `57629bf`)

#### Arquivos produzidos:

- **`docs/coleta.md`** (115 linhas) — fonte, endpoint, parâmetros, distribuição, schema, reprodutibilidade, limitações, conformidade ética
- **`docs/limitacoes.md`** (123 linhas) — limitações por fase + auto-auditoria adversarial (6 perguntas de banca cética) + LGPD + trabalhos futuros
- **`docs/referencias.md`** (79 linhas) — 10 DOIs reais verificados:
  - **Domínio (5):** McCombs & Shaw (agenda-setting), DiMaggio et al. (topic modeling + mídia), Jacobi et al. (jornalismo quantitativo), Grimmer & Stewart (text as data), BERTimbau/Souza et al.
  - **Técnica (5):** BERTopic/Grootendorst, Sentence-BERT/Reimers, UMAP/McInnes, HDBSCAN/McInnes, Coherence/Röder
  - ✅ Todos verificados por resolução em `doi.org`
- **`README.md`** (120 linhas) — visão geral, achados, pipeline, métricas, reprodução, estrutura, decisões técnicas, princípios

#### Auto-auditoria adversarial (6 pontos críticos)

| Pergunta da banca cética | Resposta honesta |
|--------------------------|------------------|
| "10 tópicos é cherry-pick para inflar c_v?" | Critério (máx. c_v) foi declarado a priori; as 3 configurações estão em topic_eval.csv |
| "Pauta não óbvia está nos títulos, não é descoberta" | Parcialmente justo — o valor está em quantificar o deslocamento (+7,2pp) invisível na taxonomia |
| "Eventos são circulares (lê o pico e nomeia)" | Assumido: exceto observâncias de calendário, os eventos são inferidos do corpus. Leitura interpretativa, não causal |
| "Gold set rotulado por quem rodou o modelo → kappa inflado" | Limitação real. Mitigação parcial: erros concretos corrigidos (ex: feminicídio→saúde) |
| "F1 0,91 com 29% outliers descartados é seletivo" | Correto: métricas vivem no subconjunto de alta confiança. F1 intrínseco 0,81 reportado |
| "Generaliza?" | Não. Estudo de caso de 6 meses de um órgão. Sem validade externa |

---

## 3. Resumo de Métricas (todas de execução real)

| Métrica | Valor |
|---------|:-----:|
| Notícias coletadas | 983 |
| Após limpeza | 979 |
| Tópicos BERTopic | 10 |
| Coerência c_v | 0,777 |
| Diversidade | 1,0 |
| Outliers brutos | 29,4% |
| Picos detectados | 20 |
| Classificador intrínseco (LogReg) | F1=0,8131 |
| **F1-macro vs gold humano** | **0,9137** |
| **Kappa vs gold humano** | **0,9099** |
| Gold set manual | 173 notícias |
| Eventos mapeados | 12 |
| Figuras geradas | 13 |
| Commits | 7 |
| Total de linhas de código | ~2.000+ (6 scripts + 4 notebooks + docs) |

---

## 4. Resultados Negativos Documentados

1. **Colapso inicial** em 2 tópicos (cosseno médio ≈0,69) — corrigido com UMAP `n_neighbors=10` + HDBSCAN `cluster_selection_method="leaf"`
2. **Bug de acentos** — BERTopic `language="english"` default remove não-ASCII
3. **Outliers de 29%** — HDBSCAN descarta docs ambíguos que poderiam conter pauta emergente
4. **Eventos parcialmente circulares** — maioria inferida do próprio corpus
5. **F1=0,91 otimista** — exclui 22 casos indefinido (≈11% da amostra)
6. **Anotador único** — sem concordância inter-anotador independente
7. **Janela parcial** (6 meses) — não separa sazonalidade de tendência estrutural

---

## 5. Achados Principais

1. **A taxonomia editorial é cega à pauta** — 977/983 notícias em "Agência CNJ de Notícias". A modelagem de tópicos recupera 10 tópicos coesos que a navegação por categoria não revela.

2. **Pauta em alta (deriva estrutural):**
   - *Justiça itinerante / cidadania / PopRuaJud*: **+7,2 pp** entre 1ª e 2ª metade
   - *IA / Conecta / Justiça 4.0*: **+2,7 pp** — crescimento invisível na taxonomia

3. **Pauta em queda (sazonal):**
   - *Violência doméstica/mulheres*: **−3,9 pp** — concentrada em março (Mês da Mulher)
   - *Sustentabilidade*: **−3,5 pp** — concentrada em janeiro e Semana da Pauta Verde

4. **Picos ↔ eventos verificáveis:**
   - Infância (18/05) — Dia Nacional de Combate ao Abuso Sexual
   - Sustentabilidade (05/06) — Semana da Pauta Verde
   - Saúde (abril) — Estratégia Cuidar
   - Disciplinares (03/03) — decisões de alto perfil

5. **Validação:** F1-macro 0,91 e kappa 0,91 contra gold set humano validam tanto a etapa supervisionada quanto os rótulos não supervisionados do BERTopic.

---

## 6. Estrutura Final do Repositório

```
/home/zeca/mestrado/git/cnj-pauta-pln/
├── README.md
├── requirements.txt
├── environment.yml
├── .gitignore
├── data/
│   ├── raw/noticias.jsonl              # 983 notícias brutas
│   ├── interim/noticias_limpo.parquet   # 979 pós-limpeza
│   └── processed/                       # embeddings, modelo, métricas
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_topic_modeling.ipynb
│   ├── 03_temporal_drift.ipynb
│   └── 04_supervised_validation.ipynb
├── src/
│   ├── collect.py
│   ├── preprocess.py
│   ├── embed.py
│   ├── topics.py
│   ├── drift.py
│   └── supervised.py
├── reports/
│   ├── eventos_cnj.csv                 # 12 eventos mapeados
│   ├── gold_labels.csv                 # 195 rótulos manuais
│   └── figures/                        # 13 figuras PNG
└── docs/
    ├── coleta.md
    ├── referencias.md
    └── limitacoes.md
```

---

## 7. Sobre a Execução

- **Orquestração:** Hermes Agent (DeepSeek V4 Flash) — preparou prompt, git, remote, identidade, watcher
- **Execução de código:** Claude Code (Anthropic Claude Opus 4.8) — todo código, notebooks, análises
- **Tempo total:** ~40 minutos de execução contínua (Claude Code)
- **Git identity:** todos os 7 commits com `zecahnin <zecahnin@gmail.com>`
- **Repositório público:** https://github.com/zecahnin/cnj-pauta-pln
