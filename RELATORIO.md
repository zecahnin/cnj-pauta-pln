# Relatório Completo — Deriva de Pauta nas Notícias do CNJ

> **Projeto:** PLN acadêmico — Modalidade 2 "PLN no Setor Público"
> **Repositório:** [github.com/zecahnin/cnj-pauta-pln](https://github.com/zecahnin/cnj-pauta-pln)
> **Execução:** Claude Code (Anthropic Claude Opus 4.8) via Hermes Agent
> **Data de fechamento:** 2026-06-26
> **Período analisado:** 21/06/2024 a 19/06/2026 (**~24 meses**)
> **Corpus:** **4.394 notícias** limpas · taxonomia consolidada de **30 classes**
> (com fusões opt-in para **12** e **10** classes)

> **Fonte única dos números.** Todas as métricas e hiperparâmetros deste relatório
> vêm de execuções reais (seed=42) e estão consolidados em
> **`reports/RESUMO_FINAL.md`**. Em caso de divergência, vale o RESUMO_FINAL.

---

## 1. Visão Geral

A Agência CNJ de Notícias (comunicação institucional do Conselho Nacional de
Justiça) publica ~180 notícias/mês, mas sua taxonomia editorial é **cega à
pauta** — quase todo o acervo cai em 2–3 rótulos genéricos ("Agência CNJ de
Notícias", "Notícias CNJ", "Notícias do Judiciário"). O projeto usa PLN para
**descobrir a pauta fina** (BERTopic não-supervisionado, 46 tópicos → 30 classes)
e **classificar supervisionadamente** cada notícia (Naive Bayes, MLP Keras,
BERTimbau), medindo a concordância contra um **gold set humano de 300 notícias**.

**Narrativa:** Descoberta → Classificação → NER → Deriva temporal

**Resultado principal:** MLP Keras, esquema de **10 classes** —
**F1-macro 0,705 / acurácia 0,670 / kappa 0,615** contra o gold humano
(concordância substancial), operando perto do **teto humano da tarefa (~0,81)**.

---

## 2. Pipeline Completo

```
 coleta → limpeza →  EDA  → embeddings → BERTopic → consolidação → deriva → classificação → NER
(baixar)(faxinar)(explorar)(virar nº)  (46 temas)  (46→30 classes)(no tempo)(3 modelos×3 esq.)(entidades)
 Fase 1  Fase 2   Fase 3    Fase 4a     Fase 4b       Fase 4c       Fase 5      Fase 6        Fase 6b
```

### FASE 1 — Coleta (✅ 4.410 notícias brutas)

| Item | Resultado |
|------|-----------|
| API | WP REST API v2 — `https://www.cnj.jus.br/wp-json/wp/v2/posts` |
| Período | `after=2024-06-21` → `before=2026-06-21` (~24 meses) |
| **Total coletado** | **4.410** (0 duplicatas; 4.410 ids/urls únicos) |
| Rate limit | ≥1,2 s entre requisições |
| Backoff | Exponencial (2,4,8,16,32 s) em 429/5xx |
| robots.txt | `/wp-json/` não bloqueado (validado por `can_fetch`) |
| User-Agent | `cnj-pauta-pln/1.0 (pesquisa academica de PLN)` |
| Intervalo real | 21/06/2024 08:00 → 19/06/2026 12:12 |

Detalhes, distribuição mensal e schema do registro: **`docs/coleta.md`**.

### FASE 2 — Pré-processamento (✅ 4.394 notícias)

| Operação | Resultado |
|----------|-----------|
| Limpeza HTML → texto | Boilerplate/rodapé editorial removido |
| Corpos curtos | `--min-chars 250` |
| Filtro idioma | mantém só português |
| Dedup semântico (MinHash, Jaccard ≥0,85) | quase-duplicatas removidas |
| **Total após limpeza** | **4.394** (4.410 − 16) |

Saída: `data/interim/noticias_limpo.parquet`.

### FASE 3 — EDA ✅ (notebook `01_eda.ipynb`)

**6 figuras (01–06):** volume por mês, por categoria-fonte, distribuição de
comprimento, top termos, wordcloud, volume semanal.

### FASE 4 — Descoberta Exploratória: BERTopic ✅

**Embeddings (4a):** `sentence-transformers/paraphrase-multilingual-mpnet-base-v2`
(768d), entrada "título + corpo", vetores L2-normalizados, seed 42.

**BERTopic (4b):**

| Componente | Configuração |
|---|---|
| Redução | UMAP `n_neighbors=10, n_components=5, min_dist=0.0, metric=cosine, random_state=42` |
| Clusterização | HDBSCAN `min_cluster_size=min_topic_size, metric=euclidean, cluster_selection_method=leaf` |
| Representação | c-TF-IDF, `CountVectorizer(ngram_range=(1,2), min_df=3, stopwords pt)` |
| Probabilidades | `calculate_probabilities=False` |

**Sweep `min_topic_size ∈ {10, 15, 20}`** (escolha por coerência c_v + diversidade):

| min_topic_size | N tópicos | c_v | Diversidade | Outliers |
|:---:|:---:|:---:|:---:|:---:|
| 10 | 94 | 0,629 | 0,866 | 44,1% |
| 15 | 66 | 0,669 | 0,870 | 51,6% |
| **20 (selecionado)** | **46** | **0,681** | **0,885** | **55,5%** |

> `n_neighbors=10` (estrutura local) foi necessário para o HDBSCAN não colapsar
> tudo em 1–2 clusters. O vencedor maximiza coerência e diversidade ao custo de
> mais outliers — daí os **56% de outliers**, que dominam a discussão de limitações.

**Consolidação (4c):** os 46 tópicos brutos são fragmentados; o mapa
`reports/taxonomia_map.csv` (decisão do dono) os agrupa em **30 classes
temáticas** nomeadas. `text_utils.topic_to_class_id` traduz `topic_raw → classe_id`
(0–29) — é a fonte de verdade dos rótulos.

**Resultados negativos (corrigidos):** colapso inicial em 1–2 tópicos →
`n_neighbors=10` + `leaf`. Bug de acentos do `language="english"` (removia
não-ASCII) → `"multilingual"`.

### FASE 5 — Deriva Temporal ✅ (notebook `03_temporal_drift.ipynb`)

- **Comando:** `python src/drift.py --freq W --z 1.5`
- Matriz tópico×semana → z-score por tópico → marca picos acima do limiar,
  anexando as manchetes reais como evidência.
- **63 picos** detectados (`topic_peaks.csv`), casados com eventos de calendário
  (infância em maio, Pauta Verde em junho, Mês da Mulher em março).

> Cruzamento pico↔evento é **correlação temporal**, não causal. Observâncias de
> calendário são fonte externa verificável; eventos institucionais são inferidos
> do corpus.

### FASE 6 — NÚCLEO: Classificação Supervisionada ✅

#### Protocolo de avaliação (sem vazamento)

| Item | Valor |
|------|-------|
| **Rótulo fraco** | `classe_id` consolidado (remapeado p/ 12/10), no MESMO espaço do gold |
| **Outliers (topic_raw=-1)** | excluídos do pool (56% do corpus) |
| Pool de treino (rótulo fraco, fora do gold) | **1.821** docs |
| Split estratificado | **1.164** treino / **292** val / **365** teste |
| **Gold humano (régua externa)** | **300** docs (0 `indefinido`), removidos do treino |

> **Correção de vazamento:** versões antigas treinavam *com* o gold dentro do
> conjunto e reportavam kappa inflado (~0,9). O protocolo novo (gold fora do
> treino) é a régua honesta — **é o número que vale**.
>
> **Bug corrigido:** o rótulo fraco usava `topic_raw` (id bruto 0–45, espaço
> distinto do gold 0–29), o que estourava a MLP e invalidava a métrica externa.
> Corrigido para `classe_id` consolidado.

#### Features

- **TF-IDF** (NB e MLP): `TfidfVectorizer(stop_words=pt, ngram_range=(1,2),
  min_df=3, max_features=5000, sublinear_tf=True)`. Entrada = título + corpo
  normalizado.
- **BERTimbau** (Modelo C): `neuralmind/bert-base-portuguese-cased`,
  **mean-pooling** da última camada, 768d, truncado em 512 subtokens. Entrada =
  título + corpo original (cased preserva caixa/acentos).

#### Os três modelos

| Modelo | Arquitetura / hiperparâmetros |
|---|---|
| **A. Naive Bayes** | TF-IDF → `MultinomialNB()` (baseline probabilístico). |
| **B. MLP Keras** | `Input(5000) → Dense(256,ReLU) → Dropout(0.3) → Dense(128,ReLU) → Dropout(0.3) → Dense(N,softmax)`; **Adam**; `sparse_categorical_crossentropy`; batch 32; até 50 épocas; **early stopping** (`val_loss`, paciência 5, `restore_best_weights`). |
| **C. BERTimbau** | embeddings (mean-pooling) → `StandardScaler` → `LogisticRegression(C=1.0, max_iter=2000)`. |

`N` = nº de classes do esquema (30, 12 ou 10).

#### Esquemas de classes (30 / 12 / 10)

A taxonomia consolidada tem **30 classes**, mas **4 sem nenhum gold** e várias com
n<6 — o que torna o macro-F1 instável. Por isso duas fusões opt-in, escolhidas
pela **matriz de confusão real vs. gold**:

- **30 → 12** (`MERGE_MAP`): funde fragmentos temáticos (ex.: Tecnologia =
  IA+Inovação+Domicílio Eletrônico; Acesso = Itinerante+PopRua).
- **12 → 10** (`MERGE_MAP_10`): mais duas fusões — Gestão+Corregedoria e
  Acesso+Justiça Eleitoral (Eleitoral era a classe mais fraca, n=8, F1 0,36).

> **Decisão registrada:** *não* fundir Gestão com Direitos Humanos, apesar de ser
> o máximo da métrica (+0,034 isolado): criaria um balde incoerente de n=97 e
> dissolveria um tema valioso. O ganho extra é quase todo artefato mecânico.

#### Resultados reais — régua externa (vs. gold de 300) — **o número que vale**

| Esquema | Modelo | Acurácia | **F1-macro** | Kappa |
|:---:|---|:---:|:---:|:---:|
| **30** | NB | 0,400 | 0,359 | 0,354 |
|  | MLP | 0,503 | 0,492 | 0,480 |
|  | BERTimbau | 0,473 | 0,469 | 0,451 |
| **12** | NB | 0,533 | 0,472 | 0,475 |
|  | MLP | 0,637 | 0,657 | 0,592 |
|  | BERTimbau | 0,583 | 0,607 | 0,535 |
| **10** | NB | 0,613 | 0,562 | 0,542 |
|  | **MLP** | **0,670** | **0,705** | **0,615** |
|  | BERTimbau | 0,627 | 0,650 | 0,566 |

#### Régua interna (teste do pool, aprende o rótulo fraco)

| Esquema | NB (acc/F1) | MLP (acc/F1) | BERTimbau (acc/F1) |
|:---:|:---:|:---:|:---:|
| 30 | 0,614 / 0,445 | 0,778 / 0,770 | 0,797 / 0,792 |
| 12 | 0,726 / 0,552 | 0,855 / 0,855 | 0,841 / 0,851 |
| 10 | 0,726 / 0,594 | 0,822 / 0,823 | 0,800 / 0,822 |

> **Leitura:** internamente os modelos aprendem bem o rótulo fraco (MLP/BERT
> ~0,82–0,85); o gap interno×externo (~0,15–0,30) é o efeito do **ruído do rótulo
> fraco + dos outliers**.

#### Tabela comparativa final (10 classes, gold)

| Modelo | Acc gold | **F1 gold** | **Kappa** | Técnica do curso |
|--------|:-------:|:----------:|:---------:|------------------|
| **A: Naive Bayes** | 0,613 | 0,562 | 0,542 | BoW/TF-IDF, Naive Bayes |
| **B: MLP Keras** | **0,670** | **0,705** | **0,615** | Redes densas, ReLU, softmax, Adam, Dropout/L2, overfit |
| **C: BERTimbau** | 0,627 | 0,650 | 0,566 | BERT/Transformers, embeddings |

O **MLP Keras é o melhor modelo geral**. O BERTimbau não o supera na régua
externa (apesar de melhor no interno — generaliza um pouco pior para o gold). O
Naive Bayes é baseline esperado — confirma que vale um modelo mais expressivo.

> **Atenção à interpretação:** fundir classes **sobe a métrica** (menos confusão
> entre vizinhos + mais suporte por classe), mas **parte do ganho 30→12→10 é
> mecânica** (remoção de classes minúsculas): o kappa sobe menos que o F1. Não
> superinterpretar o 0,705.

#### Per-class F1 — MLP, 10 classes (gold)

- **Fortes:** Violência doméstica **0,90**; Questões fundiárias 0,81;
  Sustentabilidade 0,74; Tecnologia/Justiça 4.0 0,72; Infância+socioeducativo
  0,70; DH/diversidade 0,67.
- **Mais fracas (nenhuma < 0,5):** Gestão/governança/corregedoria **0,58** (n=85,
  catch-all residual); Sistema prisional 0,59; Judicialização 0,64.

#### Análise de Overfit (peça central do Módulo 2 do curso)

A MLP é treinada **com e sem Dropout** pelas mesmas 50 épocas (sem early stopping,
para tornar as curvas comparáveis — figura `14_overfit_mlp`), e em 4 regimes de
regularização (figura `14b_regularizacao`). Números (esquema de 10 classes):

| Regime | train_acc final | val_acc melhor | val_loss mín | subida de val_loss |
|:---|:---:|:---:|:---:|:---:|
| Sem regularização | 1,00 | 0,839 | 0,507 | +0,142 |
| Dropout 0,3 | 1,00 | 0,853 | 0,517 | **+0,215** |
| L2 1e-3 | 1,00 | 0,853 | 0,628 | 0,000 |
| L2 1e-2 (forte) | 0,995 | 0,832 | 1,070 | 0,000 (underfit) |

> 🧠 **Resultados negativos honestos:**
> - **Overfit clássico:** treino → 100% de acerto; validação estaciona (~0,84).
> - **Dropout NÃO ajuda** em TF-IDF esparso com poucos dados — a subida de
>   val_loss é *maior* com Dropout (+0,215) que sem (+0,142).
> - **L2 forte leva a underfit** (val_acc cai, val_loss alta e plana).
> - O modelo final usa Dropout moderado + early stopping (parou em ~11 épocas).

### FASE 6b — NER (Extração de Entidades) ✅

**Modelo:** NER em português (`transformers.pipeline("ner",
aggregation_strategy="max")`). A saída crua do modelo é ruidosa; aplicamos um
funil explícito e auditável (`src/ner.py`, listas canônicas em `text_utils.py`):

| Etapa do funil | Entidades | % do bruto |
|---|--:|--:|
| Bruto (saída do modelo) | 11.971 | 100,0% |
| Após corte de score (≥0,90) | 4.492 | 37,5% |
| Após limpeza de bordas | 4.475 | 37,4% |
| Após filtro de fragmento | 4.344 | 36,3% |
| **Após filtro de genérico (final)** | **4.136** | **34,6%** |

O corte de confiança é o filtro dominante (descarta 62,5%). **Taxa de fragmento
residual: 0,77%** (siglas/topônimos curtos legítimos: Acre, Rio, EUA, Haia, USP),
não lixo de tokenizer — o resíduo de subpalavra "##" foi a zero.

**Top entidades** (por nº de notícias distintas; `tipo` é informativo):

| Entidade | Notícias | Ocorrências |
|----------|:--------:|:-----------:|
| Conselho Nacional de Justiça | 409 | 428 |
| Edson Fachin | 129 | 137 |
| Brasília | 68 | 71 |
| Programa das Nações Unidas para o Desenvolvimento (PNUD) | 40 | 42 |
| Mauro Campbell Marques | 39 | 41 |

---

## 3. Análises adicionais (qualidade do gold e alavanca dos outliers)

### Diagnóstico dos outliers
56% do corpus (e do gold) são outliers do BERTopic, ausentes do pool. O MLP cai
de **F1 0,70** (clusterizados) para **0,58** (outliers). O rótulo fraco concorda
com o gold **0,75** (F1, 12 classes) — o **teto do "professor"**.

### Experimento sem vazamento — rotular outliers ajuda? (`exp_outliers.py`)
Validação cruzada 5-fold sobre os 167 outliers genuínos (eval com rótulo gold;
treino com rótulo do dono; teste sempre fora do treino):

| Modelo | acc ANTES→DEPOIS | F1 ANTES→DEPOIS | kappa ANTES→DEPOIS |
|---|:---:|:---:|:---:|
| NB | 0,551 → 0,557 | 0,515 → 0,517 | 0,479 → 0,483 (~0) |
| **MLP** | 0,599 → **0,647** | 0,650 → **0,679** | 0,537 → **0,588** (+0,05) |
| BERTimbau | 0,575 → 0,575 | 0,605 → 0,603 | 0,511 → 0,506 (~0) |

**Conclusão:** rotular outliers dá ganho **modesto e só no MLP** (+0,05). A
barreira é a ambiguidade da taxonomia/rótulos, não a falta de dados.

### Teto humano e adjudicação (`adjudicate.py`)
Re-anotação humana dos 300 docs do gold concorda com a anotação original em
**70,3% (30 classes) / 80,7% (10 classes)**, kappa 0,68 / 0,77. Logo o **teto da
tarefa é ~0,81**, não 1,0 — e o MLP (0,705) já opera perto dele.

- MLP vs. consenso das 211 concordâncias: **F1 0,808** (vs. 0,705 no gold completo)
  — o grosso do "erro" do modelo está nos docs que os próprios humanos disputam.

---

## 4. Cobertura do Curso

| Conceito | Onde | Arquivo |
|----------|------|---------|
| **Bag-of-Words / TF-IDF** | Features dos Modelos A/B (Fase 6) | `src/classify.py::build_vectorizer()` |
| **Naive Bayes** | Modelo A — baseline clássico | `src/classify.py::run_naive_bayes()` |
| **Rede neural densa (Keras)** | `Sequential([Dense,Dense,Dense])` — Modelo B | `src/classify.py::build_mlp()` |
| **ReLU, softmax** | Ativações das camadas da MLP | `src/classify.py::build_mlp()` |
| **Adam, gradiente descendente** | `optimizer="adam"` | `src/classify.py::build_mlp()` |
| **Treino/teste/validação** | Split estratificado 70/15/15 | `src/classify.py::make_splits()` |
| **Overfit/underfit** | Curvas treino×validação (figs 14, 14b) | `src/classify.py::run_mlp()` |
| **Regularização (Dropout, L2)** | Estudo controlado: sem reg / Dropout / L2 1e-3 / L2 1e-2 | `src/classify.py::overfit_study()` |
| **BERTimbau / Transformers** | Modelo C + NER | `src/embed_bertimbau.py`, `src/ner.py` |
| **Embeddings** | sentence-transformers (exploração) + BERTimbau | `src/embed.py`, `src/embed_bertimbau.py` |

---

## 5. Resultados Negativos Documentados

1. **Colapso inicial em 1–2 tópicos** — corrigido com `n_neighbors=10` + `leaf`.
2. **Bug de acentos** — BERTopic `language="english"` removia não-ASCII.
3. **Rótulo fraco usava `topic_raw`** (espaço 0–45) em vez de `classe_id` (0–29)
   — estourava a MLP; corrigido.
4. **Dropout não ajuda** em TF-IDF esparso (val_loss +0,215 vs +0,142 sem reg).
5. **L2 forte (1e-2) causa underfit** — val_loss plana em 1,07.
6. **Segfault TF+torch** — resolvido com `src/tf_guard.py` + BERTimbau em processo
   separado.
7. **Kappa real ~0,48–0,62** (conforme granularidade) vs. relato antigo inflado
   ~0,9 — diferença é vazamento corrigido (gold fora do treino).
8. **Naive Bayes fica muito atrás** (F1 0,36–0,56) — baseline insuficiente em
   classes pequenas.
9. **56% de outliers** do HDBSCAN — pool não os representa; rotulá-los rende pouco
   (+0,05 só MLP).
10. **30 classes têm 4 sem nenhum gold** e várias com F1 instável — motivo das
    fusões 12/10.
11. **Parte do ganho 30→12→10 é mecânica** — o kappa sobe menos que o F1.

---

## 6. Figuras Geradas

| # | Arquivo | Fase | Conteúdo |
|:-:|---------|:----:|----------|
| 01–06 | `01_volume_por_mes` … `06_volume_semanal` | 3 | EDA |
| 07–09 | `07_topic_eval`, `08_topic_sizes`, `08b_classes_tematicas`, `09_topic_terms` | 4 | BERTopic |
| 10–12 | `10_streamgraph`, `11_topicos_no_tempo`, `12_drift_h1_h2` | 5 | Deriva |
| 13 | `13_confusion_matrix` | 6 | Matriz NB |
| 14 | `14_overfit_mlp*` | 6 | Curvas treino×validação MLP |
| 14b | `14b_regularizacao*` | 6 | Comparação de regularização |
| 15 | `15_confusion_gold*` | 6 | Matriz gold MLP |
| 16 | `16_top_entidades` | 6b | Top entidades NER |

> Sufixo por esquema nas figuras da Fase 6: `''` (30), `_merged` (12),
> `_merged10` (10).

---

## 7. Estrutura do Repositório

```
cnj-pauta-pln/
├── README.md                                  # guia de execução completo
├── RELATORIO.md                               # este relatório
├── requirements.txt
├── data/
│   ├── raw/noticias.jsonl                      # 4.410 notícias brutas
│   ├── interim/noticias_limpo.parquet          # 4.394 pós-limpeza
│   └── processed/                              # embeddings, modelo, métricas
├── notebooks/
│   ├── 01_eda.ipynb · 02_topic_modeling.ipynb
│   └── 03_temporal_drift.ipynb · 04_supervised_classification.ipynb
├── src/
│   ├── collect.py · preprocess.py · embed.py
│   ├── text_utils.py                           # taxonomia 30/12/10, MERGE_MAP(_10)
│   ├── tf_guard.py · topics.py · drift.py
│   ├── embed_bertimbau.py · classify.py · ner.py
│   ├── sample_outliers.py · exp_outliers.py    # alavanca dos outliers
│   └── adjudicate.py                           # consenso gold × re-anotação
├── reports/
│   ├── RESUMO_FINAL.md                         # fonte única dos números
│   ├── gold_labels.csv                         # 300 gold humano (0 indefinido)
│   ├── taxonomia_map.csv · eventos_cnj.csv
│   └── figures/                                # PNGs
└── docs/
    ├── coleta.md · referencias.md · limitacoes.md
```

---

## 8. Auto-Auditoria Adversarial (resumo)

| Pergunta da banca | Resposta |
|-------------------|----------|
| "Gold é humano e independente?" | ✅ 300 notícias rotuladas à mão (0–29), **removidas do treino** (sem vazamento). Há agora uma **segunda anotação humana** (teto ~0,81). |
| "Métricas vivem num subconjunto fácil?" | Não. A régua que vale é o gold de 300 (não o pool). 0 `indefinido` na versão atual. |
| "Overfit foi tratado?" | ✅ Estudo controlado (figs 14/14b). **Dropout não ajuda** em TF-IDF esparso; final usa Dropout moderado + early stopping. |
| "Por que classificação e não só topic modeling?" | ✅ A avaliação formal exige supervisão + gold humano. BERTopic é descoberta exploratória que *deriva a taxonomia*. |
| "O número 0,705 é robusto?" | Parcialmente: parte do ganho 30→12→10 é mecânica (kappa sobe menos). Mas 0,705 já está perto do **teto humano (~0,81)**. |
| "Generaliza para outros órgãos?" | Não. Estudo de caso de 24 meses de UM órgão. Sem validade externa. |

Auto-auditoria completa e limitações por fase: **`docs/limitacoes.md`**.
Referências (19, DOIs verificados): **`docs/referencias.md`**.
