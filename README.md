# Deriva de Pauta nas Notícias do CNJ

Projeto acadêmico de PLN que **descobre como a agenda comunicacional da Agência
CNJ de Notícias se distribui e se desloca** ao longo de 6 meses e, sobre essa
base, **classifica supervisionadamente** as notícias por tema. A narrativa é:

> **Descoberta** (BERTopic, não-supervisionado → taxonomia de 10 classes) →
> **Classificação supervisionada** (Naive Bayes · MLP Keras · BERTimbau, avaliada
> contra *gold set* humano) → **NER** (entidades dominantes na comunicação) →
> **Deriva temporal** (picos e deslocamentos de pauta).

A classificação supervisionada é o **núcleo avaliado**, cobrindo as técnicas do
curso (TF-IDF/BoW, Naive Bayes, redes densas, ReLU/softmax, Adam, overfit/underfit,
Dropout/L2, BERTimbau/Transformers). O BERTopic passa a ser **descoberta
exploratória** que *deriva a taxonomia* — não a avaliação formal.

**Período analisado:** 22/12/2025 a 19/06/2026 · **Corpus:** 979 notícias.

---

## Principais achados (todos de execução real)

- A **taxonomia editorial é cega à pauta**: 973 das notícias caem em "Agência CNJ
  de Notícias" e 2–3 rótulos genéricos. A descoberta não-supervisionada recupera
  **10 tópicos coesos** (c_v=0,777; diversidade=1,0), consolidados em 10 classes
  temáticas nomeadas.
- **Classificação supervisionada (vs gold humano, sem vazamento):** a **MLP Keras**
  atinge **F1-macro 0,80 / kappa 0,79** e o **BERTimbau** **0,79 / 0,77** —
  *concordância substancial* com humanos; o **Naive Bayes** (baseline) fica em
  F1 0,50 / kappa 0,49.
- **NER:** após limpeza da saída crua (corte de score ≥0,90 + remoção de bordas
  funcionais + filtros de fragmento e genérico; funil 11.971 → 4.136 entidades),
  a comunicação é dominada por **Conselho Nacional de Justiça** (409 notícias),
  **Edson Fachin** (129), o **PNUD** (40) e tribunais/estados (Brasília, Maranhão,
  Rio de Janeiro); cada classe temática tem entidades características.
- **Pauta em alta (deriva estrutural):** *Justiça itinerante / cidadania /
  PopRuaJud* e *IA / Conecta / Justiça 4.0* — crescimento invisível na taxonomia
  de origem. **Em queda (sazonal):** *violência doméstica* (março/Mês da Mulher) e
  *sustentabilidade* (janeiro).
- **Picos correlacionados a eventos verificáveis:** infância (18/05), sustentabili-
  dade (Semana da Pauta Verde / 5 jun), saúde (Estratégia Cuidar), disciplinares
  (decisões de alto perfil em 02/03).

> **Honestidade metodológica.** A validação *antiga* (`src/supervised.py`)
> reportava kappa ≈ 0,91 **treinando com o gold dentro do conjunto** (vazamento).
> A Fase 6 atual **remove o gold do treino** (162/173 também eram rótulo fraco):
> os números caem para ~0,79 e passam a ser defensáveis. Resultados negativos
> (Dropout que não ajuda; classe "Precatórios" com F1 baixo no NB) são reportados,
> não mascarados.

---

## Pipeline e status

| Fase | Descrição | Artefato principal | Status |
|---|---|---|---|
| 1. Coleta | WP REST API, robots.txt/rate limit/backoff | `data/raw/noticias.jsonl` | ✅ |
| 2. Pré-processamento | limpeza, dedup MinHash, filtro pt-BR | `data/interim/noticias_limpo.parquet` | ✅ |
| 3. EDA | volume, comprimento, termos, wordcloud | `notebooks/01_eda.ipynb` | ✅ |
| 4. Descoberta (BERTopic) | embeddings + UMAP/HDBSCAN/c-TF-IDF → taxonomia | `notebooks/02_topic_modeling.ipynb` | ✅ |
| 5. Deriva temporal | picos, eventos, streamgraph | `notebooks/03_temporal_drift.ipynb` | ✅ |
| **6. Classificação supervisionada** | **NB · MLP Keras · BERTimbau vs gold humano** | `notebooks/04_supervised_classification.ipynb` | ✅ |
| 6b. NER | entidades nomeadas (modelo pt-BR) | `data/processed/entidades.parquet` | ✅ |
| 7. Documentação | docs, referências, auto-auditoria | `docs/`, `README.md` | ✅ |

### Métricas reais por fase

| Fase | Métrica | Valor |
|---|---|---|
| 2 | Após limpeza (curtos+não-pt+dups) | 979 |
| 4 | Tópicos (modelo selecionado) | 10 |
| 4 | Coerência c_v / diversidade | 0,777 / 1,0 |
| 4 | Outliers brutos (HDBSCAN) | 29,42% |
| 5 | Picos detectados (z≥1,5) | 20 |
| 6 | Pool de treino (rótulo fraco, fora do gold) | 529 |
| 6 | Gold humano avaliado | 173 (+22 'indefinido') |
| 6 | **MLP** — gold acc / F1-macro / kappa | 0,809 / 0,798 / 0,788 |
| 6 | **BERTimbau** — gold acc / F1-macro / kappa | 0,792 / 0,787 / 0,769 |
| 6 | **Naive Bayes** — gold acc / F1-macro / kappa | 0,543 / 0,496 / 0,490 |
| 6b | Entidades NER (bruto → final após funil de limpeza) | 11.971 → 4.136 |
| 6b | Fragmento residual (chaves ≤4 chars não-sigla) | 0,77% |

> Detalhamento e **resultados negativos** (colapso inicial em 2 tópicos, Dropout
> sem ganho, classe com F1 baixo) em `docs/` e nos notebooks.

---

## Reprodução

```bash
# 1. Ambiente
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt            # inclui tensorflow (MLP Keras)

# 2. Pipeline completo
python src/collect.py --after 2025-12-21 --before 2026-06-21   # Fase 1
python src/preprocess.py                                       # Fase 2
python src/embed.py                                            # Fase 4a (embeddings)
python src/topics.py --sizes 10 15 20                          # Fase 4b (descoberta)
python src/drift.py --freq W --z 1.5                           # Fase 5
python src/embed_bertimbau.py                                  # Fase 6 (embeddings BERTimbau)
python src/classify.py --epochs 50                             # Fase 6 (NB/MLP/BERTimbau)
python src/ner.py                                              # Fase 6b (NER)

# 3. Notebooks (geram as figuras em reports/figures/)
jupyter nbconvert --to notebook --execute --inplace notebooks/*.ipynb
```

> **Nota de ambiente (importante).** `umap.parametric_umap` importa TensorFlow
> incondicionalmente quando ele está instalado, e **TF + PyTorch + numba no mesmo
> processo causa segfault**. Por isso: (i) o pipeline BERTopic bloqueia o TF via
> `src/tf_guard.py`; (ii) os embeddings BERTimbau rodam em processo separado
> (`src/embed_bertimbau.py`), e `classify.py` apenas lê o cache. Rode os scripts
> na ordem acima.

A coleta é **idempotente** e o snapshot de dados está versionado, de modo que as
fases 2–6 reproduzem os números deste README sem nova coleta. Artefatos pesados e
regeneráveis (`embeddings.npy`, `bertopic_model/`, `bertimbau_embeddings.npy`) não
são versionados.

---

## Estrutura

```
data/{raw,interim,processed}/   dados por estágio
src/                            collect · preprocess · embed · topics · drift ·
                                text_utils · tf_guard · classify · embed_bertimbau ·
                                ner   (+ supervised.py, validação antiga/legada)
notebooks/                      01_eda · 02_topic_modeling · 03_temporal_drift ·
                                04_supervised_classification
reports/figures/                18 figuras geradas
reports/eventos_cnj.csv         eventos para cruzamento (ancorados em evidência)
reports/gold_labels.csv         gold set HUMANO (195 linhas: 173 rotuladas + 22 'indefinido')
reports/gold_template.csv       template de anotação (classe VAZIA, ~200, estratificado)
docs/                           coleta · limitacoes · referencias
```

## Decisões técnicas notáveis

- **Taxonomia canônica única:** `src/text_utils.py` (TF-free) centraliza as 10
  classes e as stopwords; descoberta, deriva e classificação nunca divergem.
- **Avaliação sem vazamento:** o gold humano é removido do treino; features dos
  classificadores (TF-IDF lexical; embeddings BERTimbau) são espaço distinto do
  UMAP/HDBSCAN que gerou os rótulos fracos.
- **Overfit/regularização (resultado honesto):** Dropout **não** corrige o overfit
  em TF-IDF esparso; L2 moderado corrige; L2 forte gera underfit. Modelo final usa
  Dropout + EarlyStopping (figuras 14, 14b).
- **Corpus homogêneo / acentos:** `n_neighbors=10` + `cluster_selection_method=
  "leaf"` evitam colapso em 2 tópicos; `BERTopic(language="multilingual")` evita
  remoção ASCII de acentos.

## Princípios

Reprodutibilidade · **sem métricas fabricadas** (todo número vem de execução
real) · **resultados negativos documentados** · **gold set 100% humano** ·
conformidade com robots.txt, rate limit e LGPD. Código em inglês; documentação e
análise em pt-BR. Ver `docs/limitacoes.md` para a **auto-auditoria adversarial**
e `docs/referencias.md` para os DOIs verificados.
