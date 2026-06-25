# Deriva de Pauta nas Notícias do CNJ — Guia de Execução

> **Para quem é este guia.** Você precisa (1) **rodar o projeto do zero**,
> (2) **confirmar que cada etapa funcionou** e (3) **entender o que cada etapa faz
> e por quê**. Cada termo técnico é explicado na primeira vez que aparece. Para o
> relatório técnico completo (hiperparâmetros, arquiteturas, métricas por esquema,
> decisões de design e resultados negativos), veja **`reports/RESUMO_FINAL.md`**.

---

## A. Visão de 1 minuto

Projeto acadêmico de **PLN** (Processamento de Linguagem Natural). Ele pega
**4.394 notícias** publicadas pela Agência CNJ de Notícias ao longo de
**~24 meses** (21/06/2024 a 19/06/2026) e responde três perguntas:

1. **Sobre o que o CNJ comunica?** O código *descobre* sozinho os temas
   (não-supervisionado, BERTopic) e os organiza numa **taxonomia de 30 classes**.
2. **Dá para classificar uma notícia nova automaticamente?** Treinamos três
   modelos e medimos a concordância com um **gold set humano de 300 notícias**.
   A taxonomia pode ser usada em **três granularidades** — 30, 12 ou 10 classes.
3. **A pauta muda no tempo? Quem domina a comunicação?** Detectamos *picos* de
   assunto ao longo das semanas e as *entidades* mais citadas (NER).

### Fluxo do projeto (da notícia bruta ao resultado)

```
 coleta → limpeza →  EDA  → embeddings → BERTopic → consolidação → deriva → classificação → NER
(baixar)(faxinar)(explorar)(virar nº)  (46 temas)  (46→30 classes)(no tempo)(3 modelos×3 esq.)(entidades)
 Fase 1  Fase 2   Fase 3    Fase 4a     Fase 4b       Fase 4c       Fase 5      Fase 6        Fase 6b
```

Cada caixa é um script em `src/`. Cada uma lê o arquivo que a anterior produziu e
grava um novo. Rodando na ordem, os números deste guia se reproduzem (seed=42).

---

## B. Glossário rápido

| Termo | Em 1-2 frases |
|---|---|
| **PLN** | Técnicas para o computador ler, organizar e classificar texto. |
| **Corpus** | O conjunto de textos analisados. Aqui: as 4.394 notícias limpas. |
| **Embedding** | Texto → vetor de números, de modo que textos de significado parecido fiquem com vetores próximos. |
| **TF-IDF** | Texto → números contando palavras, com peso maior nas raras-no-geral-mas-frequentes-no-texto. |
| **BERTopic** | Agrupa textos por assunto **sem rótulos prontos** (não-supervisionado) e descreve cada grupo por palavras típicas. |
| **UMAP / HDBSCAN** | UMAP comprime os embeddings (768→5 dims); HDBSCAN acha os grupos e marca como *outlier* (-1) o que não encaixa. |
| **Rótulo fraco vs. gold** | **Fraco** = classe que a máquina atribuiu (barato, ruidoso). **Gold** = classe de um humano (caro, confiável). A prova real é a máquina vs. o gold. |
| **Outlier (BERTopic)** | Notícia que o HDBSCAN não conseguiu agrupar (tópico -1). **56% do corpus** caem aqui — fato central deste projeto. |
| **F1-macro** | Nota 0–1 que combina precisão e abrangência **dando peso igual a cada classe**. |
| **Kappa (Cohen)** | Concordância entre dois anotadores **descontando a sorte**. ~0,6 já é "substancial". |
| **Esquema de classes** | A mesma taxonomia em 3 granularidades: **30** (consolidada), **12** e **10** (fusões temáticas). Escolhido por `--scheme`. |

---

## C. Setup do ambiente

### C.1 Pré-requisitos
- **Python 3.12**; **Linux/macOS** recomendado; ~3 GB livres; internet (1ª execução baixa modelos ~1–2 GB).
- **GPU opcional** (acelera BERTimbau; o projeto roda em CPU).

### C.2 Ambiente virtual
```bash
cd cnj-pauta-pln
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt   # inclui tensorflow (MLP) e torch (BERTopic/BERTimbau)
```
> Reative com `source .venv/bin/activate` a cada novo terminal.

### C.3 Stopwords (NLTK, automático)
O código baixa sozinho (`nltk.download("stopwords")`). Para adiantar:
`python -c "import nltk; nltk.download('stopwords')"`.

### C.4 Pré-requisito de dados: o *gold set* humano
**`reports/gold_labels.csv`** já vem versionado — a classificação feita **à mão**.
Colunas: `id` e `gold` (um número **0–29** da taxonomia, ou `indefinido`).
São **300 notícias anotadas** (0 marcadas `indefinido` na versão atual). É
**entrada obrigatória da Fase 6**. Não apague nem regenere — é trabalho humano.
> Não confunda com `gold_template.csv` (molde vazio para futuras anotações).

### C.5 Runtime: TensorFlow × PyTorch (importante)
- **TensorFlow/Keras** → MLP (Fase 6, Modelo B). **PyTorch** → BERTopic/BERTimbau/NER.
- Carregar os dois no mesmo processo causa *segmentation fault*. Contornos:
  `src/tf_guard.py` bloqueia o TF nos scripts PyTorch; o BERTimbau roda em
  **processo separado** (`embed_bertimbau.py`) e o `classify.py` só **lê o cache**.
- Basta rodar os scripts **na ordem** da Seção E.

### C.6 Artefatos pesados não versionados (regenerados pelo pipeline)
`data/processed/embeddings.npy`, `bertopic_model/`, `bertimbau_embeddings.npy`.
Já o snapshot dos dados e o gold set estão versionados.

### C.7 Smoke test
```bash
python -c "import pandas, numpy, sklearn, bertopic, torch, tensorflow; print('OK libs')"
head -2 reports/gold_labels.csv    # cabeçalho 'id,gold' + 1 linha
```

---

## D. As etapas, uma a uma

Molde: **Objetivo · Comando · Por baixo · Gerado · Testar**.

### Fase 1 — Coleta
- **Objetivo.** Baixar as notícias da Agência CNJ de forma respeitosa e reproduzível.
- **Comando.** `python src/collect.py --after 2024-06-21 --before 2026-06-21`
  (`--dry-run` só conta; `--months N` usa janela relativa).
- **Por baixo.** Conversa com a WordPress REST API; lê `robots.txt`, respeita
  ~1,2 s entre requisições e *backoff*. **Idempotente** (não duplica).
- **Gerado.** `data/raw/noticias.jsonl` (uma notícia por linha).
- **Testar.** `wc -l data/raw/noticias.jsonl` (o snapshot já vem versionado).

### Fase 2 — Pré-processamento
- **Objetivo.** Texto bruto → corpus limpo, sem duplicatas.
- **Comando.** `python src/preprocess.py` (`--min-chars 250`, `--jaccard 0.85`).
- **Por baixo.** Remove rodapé editorial; mantém só português; remove duplicatas
  e quase-duplicatas (MinHash); cria campos derivados e texto normalizado.
- **Gerado.** `data/interim/noticias_limpo.parquet`.
- **Testar.**
  ```bash
  python -c "import pandas as pd; d=pd.read_parquet('data/interim/noticias_limpo.parquet'); print(len(d))"
  ```
  Esperado: **4394**.

### Fase 3 — EDA
- **Objetivo.** Olhar o corpus antes de modelar (volume/mês, comprimento, termos).
- **Comando.** `jupyter nbconvert --to notebook --execute --inplace notebooks/01_eda.ipynb`
- **Gerado.** Figuras `01`–`06` em `reports/figures/`.

### Fase 4a — Embeddings
- **Objetivo.** Cada notícia → vetor de 768 números (significado).
- **Comando.** `python src/embed.py` (`--model`, `--batch-size 32`).
- **Por baixo.** *Sentence-transformer*
  **`paraphrase-multilingual-mpnet-base-v2`** lê "título + corpo" → vetor 768d,
  normalizado. Roda em CPU.
- **Gerado.** `data/processed/embeddings.npy` + `ids.npy`.
- **Testar.** `python -c "import numpy as np; print(np.load('data/processed/embeddings.npy').shape)"` → **`(4394, 768)`**.

### Fase 4b — BERTopic (descoberta de temas)
- **Objetivo.** Descobrir **sem rótulos** os assuntos do corpus.
- **Comando.** `python src/topics.py --sizes 10 15 20`
- **Por baixo.** UMAP (`n_neighbors=10, n_components=5, min_dist=0.0, cosine`) →
  HDBSCAN (`min_cluster_size=min_topic_size, euclidean, leaf`) → c-TF-IDF
  (`CountVectorizer ngram=(1,2), min_df=3`). Varre `min_topic_size ∈ {10,15,20}`
  e escolhe pela coerência c_v + diversidade.
- **Gerado.** `bertopic_model/`, `topic_info.csv`, `topic_eval.csv`,
  e o **rótulo fraco** `doc_topics.parquet` (`topic_raw` 0–45, `classe_id` 0–29).
- **Testar.** `cat data/processed/topic_eval.csv`. Vencedor: **`min_topic_size=20`
  → 46 tópicos, c_v 0,681, diversidade 0,885, 55,5% de outliers.**

| min_topic_size | nº tópicos | c_v | diversidade | % outliers |
|---|---|---|---|---|
| 10 | 94 | 0,629 | 0,866 | 44,1% |
| 15 | 66 | 0,669 | 0,870 | 51,6% |
| **20** | **46** | **0,681** | **0,885** | **55,5%** |

### Fase 4c — Consolidação da taxonomia (46 → 30 classes)
- **Objetivo.** Os 46 tópicos brutos do BERTopic são fragmentados; um **mapa de
  consolidação** (`reports/taxonomia_map.csv`, decisão do dono) os agrupa em
  **30 classes temáticas** nomeadas (`27 fundir`, `19 manter`).
- **Por baixo.** `text_utils.topic_to_class_id` traduz `topic_raw → classe_id`
  (0–29). É a **fonte de verdade** dos rótulos; validada por palavras-âncora.
- **Esquemas mais grossos (opt-in, Fase 6):** `MERGE_MAP` funde 30→**12** e
  `MERGE_MAP_10` funde 30→**10**, escolhidos por coesão temática + matriz de
  confusão vs. gold. Ver `reports/RESUMO_FINAL.md`.

### Fase 5 — Deriva temporal
- **Comando.** `python src/drift.py --freq W --z 1.5`
- **Por baixo.** Matriz tópico×semana → z-score por tópico → marca picos acima do
  limiar, anexando as manchetes reais como evidência.
- **Gerado.** `topic_week_counts.csv`, `topic_peaks.csv` (+ figuras 10–12).
- **Testar.** `tail -n +2 data/processed/topic_peaks.csv | wc -l` → **63 picos**.

### Fase 6 (pré) — Embeddings BERTimbau
- **Comando.** `python src/embed_bertimbau.py`
- **Por baixo.** Processo **só PyTorch**. **`neuralmind/bert-base-portuguese-cased`**
  lê "título + corpo" (cased: preserva caixa/acentos), **mean-pooling** da última
  camada → vetor 768d, truncado em 512 subtokens.
- **Gerado.** `bertimbau_embeddings.npy` + `bertimbau_ids.npy`.
- **Testar.** shape **`(4394, 768)`**. (Se faltar, o `classify.py` o gera sozinho.)

### Fase 6 — Classificação supervisionada (núcleo avaliado)
- **Objetivo.** Treinar modelos para prever a classe e **medir a concordância com
  o gold humano (300 notícias)**.
- **Comando.**
  ```bash
  python src/classify.py --scheme 10 --epochs 50     # 10 classes (recomendado)
  python src/classify.py --scheme 12                 # 12 classes
  python src/classify.py                              # 30 classes (default)
  ```
  `--skip-bert` pula o Modelo C; `--scheme {full,12,10}` escolhe a granularidade.
- **Protocolo (sem vazamento).**
  - **Rótulo fraco** = `classe_id` consolidado (remapeado p/ 12/10 via MERGE_MAP),
    no MESMO espaço do gold. **Outliers (topic_raw=-1) ficam fora do pool.**
  - **Pool de treino** = docs com rótulo fraco e **fora do gold** = **1.821**;
    split estratificado treino/val/teste = **1164 / 292 / 365**.
  - **Gold (300)** é removido do treino e usado só na avaliação externa.
- **Os três modelos.**
  - **A. Naive Bayes** — `TfidfVectorizer(ngram=(1,2), min_df=3, max_features=5000,
    sublinear_tf)` + `MultinomialNB`.
  - **B. MLP Keras** — TF-IDF → `Dense(256,relu) → Dropout(0.3) → Dense(128,relu)
    → Dropout(0.3) → Dense(N,softmax)`; Adam; `sparse_categorical_crossentropy`;
    batch 32; *early stopping* (val_loss, paciência 5). Treinada **com e sem
    Dropout + variantes L2** para o **estudo de overfit**.
  - **C. BERTimbau** — embeddings (pré-passo) + `StandardScaler` +
    `LogisticRegression(C=1, max_iter=2000)`.
- **Gerado** (sufixo por esquema: `''`/`_merged`/`_merged10`).
  `classify_metrics*.json`, `classify_gold_preds*.json`, figuras
  `14_overfit_mlp*`, `14b_regularizacao*`, `15_confusion_gold*`.

#### Resultados reais (régua externa, vs. gold de 300) — melhor modelo: **MLP**

| Esquema | Modelo | acurácia | F1-macro | kappa |
|---|---|---|---|---|
| **30** | NB | 0,400 | 0,359 | 0,354 |
|  | MLP | 0,503 | 0,492 | 0,480 |
|  | BERTimbau | 0,473 | 0,469 | 0,451 |
| **12** | NB | 0,533 | 0,472 | 0,475 |
|  | MLP | 0,637 | 0,657 | 0,592 |
|  | BERTimbau | 0,583 | 0,607 | 0,535 |
| **10** | NB | 0,613 | 0,562 | 0,542 |
|  | **MLP** | **0,670** | **0,705** | **0,615** |
|  | BERTimbau | 0,627 | 0,650 | 0,566 |

Fundir classes **sobe a métrica** (menos confusão entre vizinhos + mais suporte
por classe), mas **parte do ganho é mecânica** (remove classes minúsculas): o
kappa sobe menos que o F1. O **teto humano** (re-anotação vs. gold) é **~0,81**
em 10 classes — o MLP (0,705) já opera perto desse limite.

### Fase 6b — NER (entidades nomeadas)
- **Comando.** `python src/ner.py --min-score 0.90`
- **Por baixo.** NER em português + funil de limpeza (confiança → preposições de
  borda → fragmentos de subpalavra → genéricos), agregando por nº de notícias.
- **Gerado.** `entidades_top.csv`, `entidades_por_classe.csv`, figura `16`.
- **Testar.** `head -6 data/processed/entidades_top.csv`. Top atual: **CNJ**
  (409 docs), **Edson Fachin** (129), **Brasília** (68), **PNUD** (40),
  **Mauro Campbell Marques** (39).

---

## E. Rodar tudo de uma vez

```bash
source .venv/bin/activate
python src/collect.py --after 2024-06-21 --before 2026-06-21   # Fase 1 (já versionado)
python src/preprocess.py                                       # Fase 2
python src/embed.py                                            # Fase 4a
python src/topics.py --sizes 10 15 20                          # Fase 4b (+ consolidação)
python src/drift.py --freq W --z 1.5                           # Fase 5
python src/embed_bertimbau.py                                  # Fase 6 (pré)
python src/classify.py --scheme 10 --epochs 50                 # Fase 6 (núcleo)
python src/ner.py --min-score 0.90                             # Fase 6b
# Notebooks: figuras 01-13
jupyter nbconvert --to notebook --execute --inplace notebooks/01_eda.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/02_topic_modeling.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/03_temporal_drift.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/04_supervised_classification.ipynb
```
> **Ordem importa** (C.5): `topics.py` bloqueia o TF; `classify.py` usa TF; o
> BERTimbau roda à parte.

---

## F. Mapa de arquivos

### `src/` — pipeline
| Arquivo | O que faz |
|---|---|
| `collect.py` | Fase 1: baixa as notícias (robots.txt, rate limit, idempotente). |
| `preprocess.py` | Fase 2: limpa, filtra português, remove duplicatas (MinHash). |
| `embed.py` | Fase 4a: embeddings multilíngues (mpnet, 768d). |
| `topics.py` | Fase 4b: BERTopic + sweep de `min_topic_size`. |
| `text_utils.py` | Fonte única (sem libs pesadas): taxonomia 30/12/10, `MERGE_MAP`/`MERGE_MAP_10`, stopwords, consolidação. |
| `drift.py` | Fase 5: série temporal por tópico + detecção de picos. |
| `embed_bertimbau.py` | Fase 6 (pré): embeddings BERTimbau (processo separado). |
| `classify.py` | Fase 6: NB/MLP/BERTimbau × esquemas 30/12/10; avalia vs. gold. |
| `ner.py` | Fase 6b: extrai e limpa entidades. |
| `sample_outliers.py` | Amostra ativa de outliers para rotulação (centroides + estratificação). |
| `exp_outliers.py` | Experimento sem vazamento: rotular outliers ajuda? (CV nos 167). |
| `adjudicate.py` | Adjudicação gold × re-anotação → consenso + F1. |
| `tf_guard.py` | Bloqueia o TF nos processos PyTorch (anti-segfault). |

### `notebooks/` | `01_eda` (fig 01–06) · `02_topic_modeling` (07–09) · `03_temporal_drift` (10–12) · `04_supervised_classification` (13).

---

## G. O que os resultados significam

1. **A categoria oficial não revela a pauta** → foi preciso *descobrir* os temas:
   BERTopic recuperou **46 tópicos** consolidados em **30 classes**.
2. **Dá para classificar — a MLP é a melhor.** Em 10 classes: **F1 0,705 /
   kappa 0,615** vs. o gold humano (concordância substancial). NB fica atrás
   (F1 0,562); o BERTimbau não supera a MLP (F1 0,650).
3. **Overfit é honesto.** Sem regularização a MLP chega a 100% no treino e
   estaciona na validação. Resultado **não óbvio**: em TF-IDF esparso o **Dropout
   não ajudou** e o L2 forte levou a *underfit*; o modelo final usa Dropout
   moderado + *early stopping* (figuras 14/14b).
4. **O teto é o rótulo, não o modelo.** 56% do corpus são outliers do BERTopic;
   o rótulo fraco concorda com o gold ~0,75 (F1); duas anotações humanas concordam
   só ~0,81 (10 classes). O MLP (0,705) já está perto do **teto humano**.
5. **A pauta tem sazonalidade.** **63 picos** semanais casados com eventos
   (infância em maio, Pauta Verde em junho, Mês da Mulher em março).
6. **A comunicação gira em torno do CNJ** (NER: CNJ 409 docs, Fachin 129).

### Limitações honestas
- **Gold de 300** — classes raras têm F1 instável (1 erro zera a classe).
- **56% outliers** — o pool de treino não os representa; o MLP cai de F1 0,70
  (clusterizados) p/ 0,58 (outliers). Rotular outliers ajuda **pouco** (+0,05 só
  no MLP) — o limite é a ambiguidade da taxonomia, não a falta de dados.
- **Rótulo fraco na origem** — o alvo de treino vem do clustering, não de humanos;
  o gold mede o quanto isso se sustenta. Validações antigas que treinavam *com* o
  gold dentro reportavam kappa inflado — abandonadas.

Detalhamento completo: **`reports/RESUMO_FINAL.md`**. Limitações/auto-auditoria:
`docs/limitacoes.md`; referências: `docs/referencias.md`; coleta: `docs/coleta.md`.
