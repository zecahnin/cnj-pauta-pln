# Deriva de Pauta nas Notícias do CNJ

Projeto acadêmico de PLN que **descobre como a agenda comunicacional da Agência
CNJ de Notícias se distribui e se desloca** ao longo de 6 meses, identifica
pautas emergentes não óbvias na taxonomia editorial e correlaciona picos
temáticos com eventos verificáveis. Pipeline reprodutível, com modelagem de
tópicos não supervisionada validada contra um *gold set* anotado manualmente.

**Período analisado:** 22/12/2025 a 19/06/2026 · **Corpus:** 979 notícias.

---

## Principais achados (todos de execução real)

- A **taxonomia editorial é cega à pauta**: 977 das 983 notícias caem em
  "Agência CNJ de Notícias" e 2–3 rótulos genéricos. A modelagem de tópicos
  recupera **10 tópicos coesos** (c_v=0,78; diversidade=1,0).
- **Pauta em alta (deriva estrutural):** *Justiça itinerante / cidadania /
  PopRuaJud* (+7,2 pp entre 1ª e 2ª metade do período) e *IA / Conecta /
  Justiça 4.0* (+2,7 pp) — crescimento invisível na taxonomia de origem.
- **Pauta em queda (sazonal):** *violência doméstica/mulheres* (−3,9 pp,
  concentrada em março/Mês da Mulher) e *sustentabilidade* (−3,5 pp, concentrada
  em janeiro).
- **Picos correlacionados a eventos verificáveis:** infância (18/05, Dia Nacional
  de Combate ao Abuso Sexual de Crianças), sustentabilidade (Semana da Pauta
  Verde / 5 de junho), saúde (Estratégia Cuidar), disciplinares (decisões de
  alto perfil em 02/03).
- **Validação:** classificador sobre rótulos fracos atinge **F1-macro 0,91** e
  **kappa 0,91** contra o gold set; os próprios rótulos não supervisionados
  concordam com a leitura humana (kappa 0,91), validando a etapa do BERTopic.

---

## Pipeline e status

| Fase | Descrição | Artefato principal | Status |
|---|---|---|---|
| 1. Coleta | WP REST API, robots.txt/rate limit/backoff | `data/raw/noticias.jsonl` | ✅ |
| 2. Pré-processamento | limpeza, dedup MinHash, filtro pt-BR | `data/interim/noticias_limpo.parquet` | ✅ |
| 3. EDA | volume, comprimento, termos, wordcloud | `notebooks/01_eda.ipynb` | ✅ |
| 4. Tópicos | embeddings + BERTopic (UMAP/HDBSCAN/c-TF-IDF) | `notebooks/02_topic_modeling.ipynb` | ✅ |
| 5. Deriva temporal | picos, eventos, streamgraph | `notebooks/03_temporal_drift.ipynb` | ✅ |
| 6. Validação | rótulos fracos + classificador + gold set | `notebooks/04_supervised_validation.ipynb` | ✅ |
| 7. Documentação | docs, referências, auto-auditoria | `docs/`, `README.md` | ✅ |

### Métricas reais por fase

| Fase | Métrica | Valor |
|---|---|---|
| 1 | Notícias coletadas / únicas | 983 / 983 |
| 2 | Após limpeza (curtos+não-pt+dups) | 979 |
| 4 | Tópicos (modelo selecionado) | 10 |
| 4 | Coerência c_v / diversidade | 0,78 / 1,0 |
| 4 | Outliers brutos (HDBSCAN) | 29,4% |
| 5 | Picos detectados (z≥1,5) | 20 |
| 6 | F1-macro intrínseco (rótulos fracos) | 0,81 |
| 6 | F1-macro / kappa (predição × gold) | 0,91 / 0,91 |
| 6 | kappa (rótulo fraco × gold) | 0,91 |

> Detalhamento e **resultados negativos** (colapso inicial em 2 tópicos, bug de
> acentos, erros de classe) em `docs/` e nos notebooks.

---

## Reprodução

```bash
# 1. Ambiente
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt            # ou: conda env create -f environment.yml

# 2. Pipeline completo
python src/collect.py --after 2025-12-21 --before 2026-06-21   # Fase 1
python src/preprocess.py                                       # Fase 2
python src/embed.py                                            # Fase 4a (embeddings)
python src/topics.py --sizes 10 15 20                          # Fase 4b (tópicos)
python src/drift.py --freq W --z 1.5                           # Fase 5
python src/supervised.py                                       # Fase 6

# 3. Notebooks (geram as figuras em reports/figures/)
jupyter nbconvert --to notebook --execute --inplace notebooks/*.ipynb
```

A coleta é **idempotente** e o snapshot de dados está versionado, de modo que as
fases 2–6 reproduzem os números exatos deste README sem nova coleta.

> Os artefatos pesados e regeneráveis (`embeddings.npy`, `bertopic_model/`) não
> são versionados; rode `embed.py` e `topics.py` para recriá-los.

---

## Estrutura

```
data/{raw,interim,processed}/   dados por estágio
src/                            collect, preprocess, embed, topics, drift, supervised
notebooks/                      01_eda · 02_topic_modeling · 03_temporal_drift · 04_supervised_validation
reports/figures/                13 figuras geradas
reports/eventos_cnj.csv         eventos para cruzamento (ancorados em evidência)
reports/gold_labels.csv         gold set anotado manualmente (195 notícias)
docs/                           coleta · limitacoes · referencias
```

## Decisões técnicas notáveis

- **Embeddings:** `paraphrase-multilingual-mpnet-base-v2` (768d, forte em pt-BR);
  ver justificativa em `src/embed.py`.
- **Corpus homogêneo:** cosseno médio ≈0,69 colapsava o HDBSCAN em 2 tópicos;
  resolvido com `n_neighbors=10` + `cluster_selection_method="leaf"`.
- **Acentos:** `BERTopic(language="multilingual")` evita a remoção ASCII que o
  default (`"english"`) aplica ao português.
- **Anti-circularidade na validação:** features TF-IDF (espaço lexical) distintas
  do espaço de embeddings que gerou os clusters.

## Princípios

Reprodutibilidade · **sem métricas fabricadas** (todo número vem de execução
real) · **resultados negativos documentados** · conformidade com robots.txt,
rate limit e LGPD. Código em inglês; documentação e análise em pt-BR.
Ver `docs/limitacoes.md` para a **auto-auditoria adversarial**.
