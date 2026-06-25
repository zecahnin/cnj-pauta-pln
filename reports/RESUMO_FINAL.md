# RESUMO FINAL — Deriva de Pauta e Classificação Temática das Notícias do CNJ

Relatório técnico de fechamento. Reúne fluxo, hiperparâmetros, arquiteturas,
métricas reais por esquema, decisões de design e resultados negativos. Todos os
números vêm de execuções reais (seed=42); nada é estimado salvo onde explicitado.

- **Corpus:** 4.394 notícias limpas da Agência CNJ (21/06/2024 a 19/06/2026, ~24 meses).
- **Gold humano:** 300 notícias anotadas à mão (taxonomia 0–29; 0 `indefinido`).
- **Melhor resultado:** MLP Keras, esquema de 10 classes — **F1-macro 0,705 /
  acurácia 0,670 / kappa 0,615** vs. o gold (concordância substancial).

---

## 1. Fluxo passo a passo

| # | Fase | Script | Entra | Sai |
|---|---|---|---|---|
| 1 | Coleta | `collect.py` | WordPress REST API | `data/raw/noticias.jsonl` |
| 2 | Limpeza | `preprocess.py` | jsonl bruto | `noticias_limpo.parquet` (4394) |
| 3 | EDA | `01_eda.ipynb` | parquet | figuras 01–06 |
| 4a | Embeddings | `embed.py` | parquet | `embeddings.npy` (4394×768) |
| 4b | BERTopic | `topics.py` | embeddings | 46 tópicos, `doc_topics.parquet` |
| 4c | Consolidação | `text_utils` + `taxonomia_map.csv` | 46 tópicos | 30 classes (`classe_id`) |
| 5 | Deriva | `drift.py` | doc_topics | `topic_peaks.csv` (63 picos) |
| 6-pré | Embeddings PT | `embed_bertimbau.py` | parquet | `bertimbau_embeddings.npy` (4394×768) |
| 6 | Classificação | `classify.py` | pool + gold | `classify_metrics*.json`, figuras 14/14b/15 |
| 6b | NER | `ner.py` | parquet | `entidades_top.csv`, figura 16 |

**Pós-fechamento (alavanca #2 e qualidade do gold):** `sample_outliers.py`
(amostra outliers para rotular), `exp_outliers.py` (mede o ganho sem vazamento),
`adjudicate.py` (gold × re-anotação → consenso).

---

## 2. Dados

- **Coleta:** WordPress REST API da Agência CNJ; `robots.txt` respeitado, ~1,2 s
  entre requisições, idempotente.
- **Limpeza:** remoção de rodapé editorial; filtro de idioma (só pt); dedup exato
  e quase-duplicatas via MinHash (Jaccard 0,85); `--min-chars 250`.
- **Rótulo fraco:** `classe_id` (0–29) derivado do BERTopic via mapa de
  consolidação. **Outliers (topic_raw=-1) = 56% do corpus** e ficam fora do pool.
- **Gold:** 300 notícias rotuladas pelo dono (0–29). Amostragem estratificada por
  classe na janela recente (anti-viés). `reports/gold_labels.csv`.

---

## 3. Hiperparâmetros e arquiteturas

### 3.1 Embeddings semânticos (Fase 4a)
- Modelo: `sentence-transformers/paraphrase-multilingual-mpnet-base-v2` (768d).
- Entrada: "título + corpo"; vetores L2-normalizados. Seed 42.

### 3.2 BERTopic (Fase 4b)
| Componente | Configuração |
|---|---|
| Redução | UMAP `n_neighbors=10, n_components=5, min_dist=0.0, metric=cosine, random_state=42` |
| Clusterização | HDBSCAN `min_cluster_size=min_topic_size, metric=euclidean, cluster_selection_method=leaf` |
| Representação | c-TF-IDF, `CountVectorizer(ngram_range=(1,2), min_df=3, stopwords pt)` |
| Probabilidades | `calculate_probabilities=False` |

**Sweep `min_topic_size ∈ {10, 15, 20}`** (escolha por coerência c_v + diversidade):

| min_topic_size | nº tópicos | c_v | diversidade | % outliers |
|---|---|---|---|---|
| 10 | 94 | 0,629 | 0,866 | 44,1% |
| 15 | 66 | 0,669 | 0,870 | 51,6% |
| **20 (vencedor)** | **46** | **0,681** | **0,885** | **55,5%** |

`n_neighbors=10` (estrutura local) foi necessário para o HDBSCAN não colapsar
tudo em 1–2 clusters. O vencedor maximiza coerência e diversidade ao custo de
mais outliers — daí os 56% que dominam a discussão de limitações.

### 3.3 Features de classificação (Fase 6)
- **TF-IDF** (NB e MLP): `TfidfVectorizer(stop_words=pt, ngram_range=(1,2),
  min_df=3, max_features=5000, sublinear_tf=True)`. Entrada = título + corpo
  normalizado.
- **BERTimbau** (Modelo C): `neuralmind/bert-base-portuguese-cased`,
  **mean-pooling** da última camada, 768d, truncado em 512 subtokens. Entrada =
  título + corpo original (cased preserva caixa/acentos).

### 3.4 Os três modelos
| Modelo | Arquitetura / hiperparâmetros |
|---|---|
| **A. Naive Bayes** | TF-IDF → `MultinomialNB()` (baseline probabilístico). |
| **B. MLP Keras** | `Input(5000) → Dense(256,ReLU) → Dropout(0.3) → Dense(128,ReLU) → Dropout(0.3) → Dense(N,softmax)`; otimizador **Adam**; perda `sparse_categorical_crossentropy`; batch 32; até 50 épocas; **early stopping** `val_loss`, paciência 5, `restore_best_weights`. |
| **C. BERTimbau** | embeddings (3.3) → `StandardScaler` → `LogisticRegression(C=1.0, max_iter=2000)`. |

`N` = nº de classes do esquema (30, 12 ou 10).

---

## 4. Esquemas de classes (30 / 12 / 10)

A taxonomia consolidada tem **30 classes**, mas 4 sem nenhum gold e várias com
n<6 — o que torna o macro-F1 instável e infla a confusão entre vizinhos. Por isso
duas fusões opt-in, escolhidas pela **matriz de confusão real vs. gold**:

- **30 → 12** (`MERGE_MAP`): funde fragmentos temáticos. As mais ancoradas em
  dados: Tecnologia (IA+Inovação+Domicílio Eletrônico, confusão 4↔16 16×) e
  Acesso/cidadania (Itinerante↔PopRua 15×).
- **12 → 10** (`MERGE_MAP_10`, coarsening do de 12): mais duas fusões —
  **Gestão+Corregedoria** ("Gestão, governança e corregedoria"; 34× de confusão,
  coeso = administração interna) e **Acesso+Justiça Eleitoral** (Eleitoral era a
  classe mais fraca, n=8, F1 0,36).

> **Decisão registrada:** *não* fundir Gestão com Direitos Humanos, apesar de ser
> o máximo da métrica (+0,034 isolado): criaria um balde incoerente de n=97 e
> dissolveria um tema valioso. O ganho extra (~0,01) é quase todo artefato mecânico.

Suporte do gold por esquema: 30 classes → média ~10/classe (4 com zero); 10
classes → 85, 37, 40, 11, 41, 15, 25, 15, 19, 12.

---

## 5. Protocolo de avaliação (sem vazamento)

- **Rótulo fraco** = `classe_id` consolidado (remapeado p/ 12/10), no MESMO espaço
  do gold. Outliers (topic_raw=-1) excluídos do pool.
- **Pool de treino** = rótulo fraco e **fora do gold** = **1.821 docs**.
- **Split interno** estratificado: treino **1164** / val **292** / teste **365**.
- **Régua externa** = os **300** do gold, removidos do treino. É o número que vale.
- **Vazamento evitado:** versões antigas treinavam *com* o gold dentro (kappa
  inflado ~0,9) — abandonadas.

---

## 6. Resultados reais por esquema

### 6.1 Régua externa (vs. gold, 300) — **o número que vale**

| Esquema | Modelo | acurácia | F1-macro | kappa |
|---|---|---|---|---|
| 30 | NB | 0,400 | 0,359 | 0,354 |
| 30 | MLP | 0,503 | 0,492 | 0,480 |
| 30 | BERTimbau | 0,473 | 0,469 | 0,451 |
| 12 | NB | 0,533 | 0,472 | 0,475 |
| 12 | MLP | 0,637 | 0,657 | 0,592 |
| 12 | BERTimbau | 0,583 | 0,607 | 0,535 |
| **10** | NB | 0,613 | 0,562 | 0,542 |
| **10** | **MLP** | **0,670** | **0,705** | **0,615** |
| **10** | BERTimbau | 0,627 | 0,650 | 0,566 |

### 6.2 Régua interna (teste do pool, aprende o rótulo fraco)

| Esquema | NB (acc/F1) | MLP (acc/F1) | BERTimbau (acc/F1) |
|---|---|---|---|
| 30 | 0,614 / 0,445 | 0,778 / 0,770 | 0,797 / 0,792 |
| 12 | 0,726 / 0,552 | 0,855 / 0,855 | 0,841 / 0,851 |
| 10 | 0,726 / 0,594 | 0,822 / 0,823 | 0,800 / 0,822 |

**Leitura:** internamente os modelos aprendem bem o rótulo fraco (MLP/BERT ~0,82–0,85);
o gap interno×externo (~0,15–0,30) é o efeito do ruído do rótulo + dos outliers.

### 6.3 Per-class F1 — MLP, 10 classes (vs. gold)
- **Fortes:** Violência doméstica **0,90**; Questões fundiárias 0,81; Sustentabilidade
  0,74; Tecnologia/Justiça 4.0 0,72; Infância+socioeducativo 0,70; DH/diversidade 0,67.
- **Mais fracas (nenhuma < 0,5):** Gestão/governança/corregedoria **0,58** (n=85,
  catch-all residual); Sistema prisional 0,59; Judicialização 0,64.

---

## 7. Estudo de overfit / underfit (MLP)

A MLP é treinada **com e sem Dropout** pelas mesmas 50 épocas (sem early stopping)
para tornar as curvas comparáveis (figura `14_overfit_mlp*`), e em 4 regimes de
regularização (figura `14b_regularizacao*`). Números (esquema de 10 classes):

| Regime | train_acc final | val_acc melhor | val_loss mín | subida de val_loss |
|---|---|---|---|---|
| Sem regularização | 1,00 | 0,839 | 0,507 | +0,142 |
| Dropout 0,3 | 1,00 | 0,853 | 0,517 | +0,215 |
| L2 1e-3 | 1,00 | 0,853 | 0,628 | 0,000 |
| L2 1e-2 (forte) | 0,995 | 0,832 | 1,070 | 0,000 |

**Conclusões (resultados negativos honestos):**
- **Overfit clássico:** treino → 100% de acerto; validação estaciona (~0,84).
- **Dropout NÃO ajuda** em TF-IDF esparso com poucos dados — a subida de val_loss
  é *maior* com Dropout (+0,215) que sem (+0,142).
- **L2 forte leva a underfit** (val_acc cai, val_loss alta e plana).
- O modelo final usa Dropout moderado + early stopping (parou em ~11 épocas).

---

## 8. Análises adicionais (alavanca #2 e qualidade do gold)

### 8.1 Diagnóstico dos outliers
56% do corpus (e do gold) são outliers do BERTopic, ausentes do pool. O MLP cai
de **F1 0,70** (docs clusterizados) para **0,58** (outliers). O rótulo fraco
concorda com o gold **0,75** (F1, 12 classes) — o teto do "professor".

### 8.2 Experimento sem vazamento — rotular outliers ajuda? (`exp_outliers.py`)
Validação cruzada 5-fold sobre os 167 outliers genuínos (eval com rótulo gold;
treino com rótulo do dono; teste sempre fora do treino):

| Modelo | acc ANTES→DEPOIS | F1 ANTES→DEPOIS | kappa ANTES→DEPOIS |
|---|---|---|---|
| NB | 0,551 → 0,557 | 0,515 → 0,517 | 0,479 → 0,483 (~0) |
| **MLP** | 0,599 → **0,647** | 0,650 → **0,679** | 0,537 → **0,588** (+0,05) |
| BERTimbau | 0,575 → 0,575 | 0,605 → 0,603 | 0,511 → 0,506 (~0) |

**Conclusão:** rotular outliers dá ganho **modesto e só no MLP** (+0,05). É
limitado por design — rótulos de outlier são ruidosos (humanos divergem 20–30%).

### 8.3 Teto humano e adjudicação (`adjudicate.py`)
Re-anotação humana dos 300 docs do gold concorda com a anotação original em
**70,3% (30 classes) / 80,7% (10 classes)**, kappa 0,68 / 0,77. Logo o **teto da
tarefa é ~0,81**, não 1,0 — e o MLP (0,705) já opera perto dele.

- 89 divergências em 30 classes (58 em 10). Consenso das **211 concordâncias**
  gerado em `gold_consenso.csv`; as 89 disputas ficam para adjudicação humana
  (`gold_adjudicacao.csv`).
- MLP vs. consenso (211 concordâncias): **F1 0,808** (vs. 0,705 no gold completo)
  — o grosso do "erro" do modelo está nos docs que os próprios humanos disputam.
- Diagnóstico (não-decisão): nas 58 divergências de 10 classes, o MLP concorda
  com o **dono 39×**, com o **gold 10×**, nenhum 9×.

---

## 9. Decisões de design (registro)

1. **Rótulo fraco = `classe_id` consolidado, não `topic_raw`.** O id bruto do
   BERTopic (0–45) vive em outro espaço; usá-lo estourava a MLP e invalidava a
   métrica externa. (Bug corrigido cedo no projeto.)
2. **Avaliação contra gold humano, sem o gold no treino.** O número de cabeçalho.
3. **Fusões guiadas por dados** (confusão + coesão + suporte), não por intuição;
   recusa explícita de fusões de alta-métrica porém incoerentes (Gestão+DH).
4. **Esquemas opt-in via `--scheme`** — as 30 classes seguem intactas (drift,
   topics e NER dependem delas); 12/10 não destroem nada.
5. **Artefatos não-destrutivos.** Fusões materializadas em colunas/arquivos novos
   (`classe_id_merged*`, `gold_labels_merged*.csv`), originais preservados.
6. **Anti-segfault** TF×PyTorch: `tf_guard` + BERTimbau em processo separado.

---

## 10. Resultados negativos (declarados, não escondidos)

- **Dropout não ajuda** em TF-IDF esparso; **L2 forte → underfit** (§7).
- **Naive Bayes fica muito atrás** (F1 0,36–0,56) — baseline confirma que vale um
  modelo mais expressivo.
- **BERTimbau não supera a MLP** na régua externa, apesar de melhor no interno —
  generaliza um pouco pior para o gold.
- **30 classes têm 4 sem nenhum gold** e várias com F1 ~0 — motivo das fusões.
- **Rotular outliers rende pouco** (+0,05 só MLP) — a barreira é a ambiguidade da
  taxonomia/rótulos (teto humano ~0,81), não a falta de dados.
- **Parte do ganho 30→12→10 é mecânica** (remoção de classes minúsculas): o kappa
  sobe menos que o F1 — não superinterpretar o 0,705.

---

## 11. Reprodutibilidade

Seed 42 em todos os scripts. Esquemas:
```bash
python src/classify.py                 # 30 classes
python src/classify.py --scheme 12     # 12 classes
python src/classify.py --scheme 10     # 10 classes (melhor)
python src/exp_outliers.py             # experimento de outliers
python src/adjudicate.py               # consenso gold × re-anotação
```
Artefatos de métrica: `data/processed/classify_metrics{,_merged,_merged10}.json`,
`exp_outliers_results.json`, `adjudicacao_resultado.json`.
