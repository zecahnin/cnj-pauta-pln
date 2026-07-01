# SPEC — Deriva de Pauta e Classificação Temática das Notícias do CNJ

> Documento de referência do estado **real** do projeto (o que está construído e commitado).
> Serve para orientar o time, a documentação da colega e a visão geral da banca. Não é plano
> futuro — é fotografia do que existe. Última sincronização: commit `c4130b4`.

---

## 1. Identidade do projeto

- **Disciplina / modalidade:** PLN no Setor Público — Modalidade 2 (dupla/trio).
- **Problema:** a taxonomia editorial da Agência CNJ de Notícias é genérica (a maioria das
  notícias cai num rótulo único); o projeto usa PLN para **descobrir a pauta fina** e
  **classificá-la automaticamente**, além de mapear **entidades** e a **deriva temporal** das
  pautas.
- **Aderência ao edital (3 dos exemplos):** categorização automática (classificação supervisionada),
  extração de entidades (NER) e análise de temas recorrentes no tempo (tópicos + deriva).
  Análise de sentimento foi **deliberadamente descartada** (fonte institucional de tom uniforme).
- **Repositório:** github.com/zecahnin/cnj-pauta-pln · **Execução:** Hermes + Claude Code · seed=42.

---

## 2. Estratégia de design (decisões-chave já tomadas)

- **Tempo separado:** descoberta de tópicos e deriva usam o **corpus cheio (24 meses)**;
  a classificação supervisionada e o gold usam a **janela recente (18 meses)** — para reduzir
  não-estacionariedade e limitar a carga de rotulagem.
- **Taxonomia construída por humano:** 46 tópicos crus do BERTopic → **30 classes** consolidadas
  por decisão humana (fusões e nomeação), registradas em `reports/taxonomia_map.csv`.
- **Esquemas de granularidade:** a classificação foi avaliada em **30 / 12 / 10 classes**
  (`MERGE_MAP`), porque 30 classes têm muitas categorias minoritárias.
- **Gold 100% humano:** 300 notícias rotuladas à mão pelo dono, com re-anotação e adjudicação de
  divergências. Sem rótulo de máquina no gold.

---

## 3. Pipeline (estado real)

| # | Fase | Script | Entra | Sai | Status |
|---|---|---|---|---|---|
| 1 | Coleta | `collect.py` | WP REST API | `data/raw/noticias.jsonl` | ✅ |
| 2 | Limpeza | `preprocess.py` | jsonl | `noticias_limpo.parquet` (**4.394**) | ✅ |
| 3 | EDA | `01_eda.ipynb` | parquet | figuras 01–06 | ✅ |
| 4a | Embeddings | `embed.py` | parquet | `embeddings.npy` (4394×768) | ✅ |
| 4b | BERTopic | `topics.py` | embeddings | 46 tópicos, `doc_topics.parquet` | ✅ |
| 4c | Consolidação | `text_utils` + `taxonomia_map.csv` | 46 tópicos | 30 classes | ✅ |
| 5 | Deriva | `drift.py` | doc_topics | `topic_peaks.csv` (63 picos) | ✅ |
| 6-pré | Embeddings PT | `embed_bertimbau.py` | parquet | `bertimbau_embeddings.npy` | ✅ |
| 6 | Classificação | `classify.py` | pool 18m + gold | métricas, figs 14/14b/15 | ✅ |
| 6b | NER | `ner.py` | parquet | `entidades_top.csv`, fig 16 | ✅ |
| — | Demo | `app_demo.py` (Streamlit) | texto | classe + entidades | 🔶 protótipo (mock) |

**Scripts de apoio:** `taxonomy_review.py` (material de revisão), `sample_outliers.py` +
`exp_outliers.py` (efeito de rotular outliers, sem vazamento), `adjudicate.py` (gold × re-anotação
→ consenso), `tf_guard.py` (isola TensorFlow do BERTopic), `text_utils.py` (taxonomia, stopwords,
listas de entidades — fonte canônica).

---

## 4. Dados

- **Corpus:** 4.394 notícias limpas, 21/06/2024 → 19/06/2026 (~24 meses).
- **Coleta:** WP REST API; robots.txt respeitado; ~1,2 s/req; idempotente.
- **Limpeza:** remoção de rodapé editorial; filtro pt; dedup exato + MinHash (Jaccard 0,85);
  `--min-chars 250`.
- **Janela de classificação (18 meses):** ~3.210 notícias. Classes minoritárias no recorte
  (30–50 docs): ENAC (34), Linguagem simples (38), Justiça Eleitoral (39), Litigância (42),
  Conflitos fundiários (43), Execuções fiscais (46), LGBTQIA+ (48), Trabalho escravo (49).
- **Gold:** `reports/gold_labels.csv` — 300 notícias, 26 classes presentes, 0 `indefinido`.

---

## 5. Taxonomia (30 classes)

0 Processos disciplinares · 1 Equidade racial · 2 Violência doméstica/mulheres ·
3 Conciliação e mediação · 4 IA/Justiça 4.0 · 5 Corregedoria/Inspeção ·
6 Justiça Itinerante/cidadania · 7 Socioeducativo · 8 Participação feminina ·
9 Direitos humanos/Corte IDH · 10 Institucional/Gestão · 11 Precatórios · 12 Transparência ·
13 LGBTQIA+ · 14 Sistema prisional · 15 Inclusão PCDs · 16 Inovação · 17 Regularização fundiária ·
18 Domicílio Judicial Eletrônico · 19 Justiça Eleitoral · 20 Linguagem simples ·
21 Saúde/judicialização · 22 ENAC/Exame de cartórios · 23 Sustentabilidade/Pauta verde ·
24 Execuções fiscais · 25 PopRuaJud · 26 Trabalho escravo/tráfico · 27 Litigância/ações coletivas ·
28 Infância e juventude · 29 Conflitos fundiários.

Avaliada também consolidada em **12** e **10** classes via `MERGE_MAP`.

---

## 6. Modelos e resultados reais

**Descoberta (BERTopic, sweep de `min_topic_size`):**

| min_topic_size | tópicos | c_v | diversidade | outliers |
|:-:|:-:|:-:|:-:|:-:|
| 20 (usado) | 46 | 0,681 | 0,885 | 55,5% |
| 15 | 66 | 0,669 | 0,870 | 51,6% |
| 10 | 94 | 0,629 | 0,866 | 44,1% |

**Classificação (3 modelos × 3 esquemas, contra gold humano):**
Técnicas do curso — **Naive Bayes** (TF-IDF), **MLP Keras** (Dense+ReLU+Dropout+softmax, Adam;
estudo de overfit/regularização), **BERTimbau** (embeddings + cabeça). Melhor resultado registrado:
**MLP Keras, esquema de 10 classes — F1-macro 0,705 / acurácia 0,670 / kappa 0,615** (concordância
substancial vs gold).

**NER (Fase 6b):** `rhaymison/ner-portuguese-br-bert-cased`, com pós-filtro (agregação `max`,
corte de score, stop-list de genéricos, whitelist de siglas, limpeza de borda).

---

## 7. Integridade metodológica (o que protege a nota)

- **Sem vazamento:** gold removido do treino; avaliação externa contra rótulo humano independente.
- **Gold cego e adjudicado:** re-anotação + consenso mediram concordância entre humanos.
- **Overfit tratado:** estudo controlado (sem reg / Dropout / L2) documentado, com achado negativo
  honesto (Dropout não ajudou em TF-IDF esparso; L2 moderado controlou).
- **Resultados negativos registrados** e limitações assumidas (classes minoritárias fracas,
  ~55% outliers do HDBSCAN, taxonomia é interpretação humana, estudo de caso de um órgão).

---

## 8. Pendências / próximos passos

- 🔶 **Demo Streamlit:** protótipo com inferência **mockada** (`app_demo.py`). Trocar a função
  `classify_and_extract()` pelos modelos reais (MLP/BERTimbau + NER) — layout já é final.
- Fechar a escolha do **esquema-título** (10/12/30) para relatório e demo.
- Slides + apresentação (10 min).
- Seção de **aderência ao edital** (mapear os 3 exemplos cobertos + justificar não-sentiment).

---

## 9. Pontos que exigem decisão humana (nunca da máquina)

1. **Nomear/validar a taxonomia** (feito — 30 classes).
2. **Rotular o gold à mão** (feito — 300 notícias).
3. **Escolher a janela recente** (feito — 18 meses).
4. **Conferir cruzamentos pico↔evento** da deriva.
5. **Escrever interpretação crítica e limitações.**

Regra permanente: onde há *significado, julgamento ou verdade externa*, decide o humano; o resto é
transformação determinística de dados.
