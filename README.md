# Deriva de Pauta nas Notícias do CNJ — Guia de Execução

> **Para quem é este guia.** Você não escreveu este código, mas precisa
> (1) **rodar o projeto do zero**, (2) **confirmar que cada etapa funcionou** e
> (3) **entender o que cada etapa faz e por quê** para documentar o trabalho.
> Cada termo técnico é explicado na primeira vez que aparece. Siga as seções na
> ordem; não é preciso conhecer BERTopic, NER, *embeddings* ou Keras de antemão.

---

## A. Visão de 1 minuto

Este é um projeto acadêmico de **PLN** (Processamento de Linguagem Natural — a
área que ensina o computador a ler e organizar texto em linguagem humana). Ele
pega **979 notícias** publicadas pela Agência CNJ de Notícias ao longo de 6 meses
(22/12/2025 a 19/06/2026) e responde três perguntas:

1. **Sobre o que o CNJ comunica?** O código *descobre* sozinho os temas das
   notícias (sem ninguém dizer quais são) e os organiza em **10 classes**.
2. **Dá para classificar uma notícia nova automaticamente?** Treinamos modelos
   que aprendem esses 10 temas e medimos o quanto eles concordam com uma pessoa
   que classificou as notícias à mão.
3. **A pauta muda no tempo? Quem domina a comunicação?** Detectamos *picos* de
   assuntos ao longo das semanas e as *entidades* (pessoas, órgãos, lugares)
   mais citadas.

### Fluxo do projeto (da notícia bruta ao resultado)

```
  coleta  →  limpeza  →   EDA   →  embeddings  →  BERTopic  →   deriva   →  classificação  →   NER
 (baixar) (faxinar)  (explorar) (virar números) (achar temas) (ver no tempo) (treinar modelos) (entidades)
  Fase 1    Fase 2     Fase 3      Fase 4a        Fase 4b        Fase 5         Fase 6           Fase 6b
```

Cada caixa é um script em `src/` (ou um notebook em `notebooks/`). Cada uma lê o
arquivo que a anterior produziu e grava um arquivo novo. É uma esteira: rodando
na ordem, os números deste guia se reproduzem.

---

## B. Glossário rápido

Leia uma vez; volte aqui sempre que um termo aparecer adiante.

| Termo | Em 1-2 frases |
|---|---|
| **PLN** | Processamento de Linguagem Natural: técnicas para o computador ler, organizar e classificar texto. |
| **Corpus** | O conjunto de textos que estamos analisando. Aqui: as 979 notícias limpas. |
| **Embedding** | Transformar um texto em uma lista de números (um vetor) de modo que textos com *significado parecido* fiquem com vetores *próximos*. É como dar coordenadas a cada notícia. |
| **TF-IDF** | Forma clássica de transformar texto em números contando palavras, dando peso maior às palavras que são *raras no geral mas frequentes naquele texto* (portanto, características dele). |
| **Modelagem de tópicos / BERTopic** | Técnica que agrupa textos por assunto **sem rótulos prontos** (não-supervisionada) e descreve cada grupo por suas palavras típicas. BERTopic é a ferramenta usada aqui. |
| **Clustering (UMAP / HDBSCAN)** | "Clusterizar" = juntar itens parecidos em grupos. **UMAP** comprime os *embeddings* de 768 números para poucos, preservando vizinhanças; **HDBSCAN** encontra os grupos (e marca como "ruído" o que não encaixa). |
| **Classificação supervisionada** | Ensinar um modelo a prever um rótulo **a partir de exemplos já rotulados**. Diferente da modelagem de tópicos, aqui os rótulos existem de antemão. |
| **Rótulo fraco vs. gold set** | **Rótulo fraco** = classe que a *própria máquina* atribuiu (barato, mas pode errar). **Gold set** = classe atribuída por um *humano* (caro, mas confiável). Comparar a máquina contra o gold é a prova real. |
| **NER** | *Named Entity Recognition* (Reconhecimento de Entidades Nomeadas): achar no texto nomes próprios — pessoas, órgãos, lugares. |
| **Overfit / underfit** | **Overfit**: o modelo decorou os exemplos de treino e vai mal em dados novos. **Underfit**: o modelo é simples demais e vai mal até no treino. O alvo é o meio-termo. |
| **F1-macro** | Nota de 0 a 1 que combina precisão e abrangência **dando o mesmo peso a cada classe** (não deixa as classes grandes mascararem as pequenas). Quanto maior, melhor. |
| **Kappa (Cohen)** | Mede a concordância entre dois "anotadores" (aqui: o modelo vs. o humano) **descontando a sorte**. ~0,8 já é "concordância substancial". |

---

## C. Setup do ambiente (passo a passo testável)

### C.1 Pré-requisitos

- **Python 3.12** (o projeto fixa versões compatíveis com essa série).
- **Linux ou macOS** recomendado (o projeto foi executado em Linux).
- ~3 GB livres em disco e conexão à internet (na 1ª execução baixam-se modelos
  de ~1–2 GB de PLN).
- **Git** para clonar o repositório.

### C.2 Criar o ambiente virtual e instalar dependências

Um *ambiente virtual* (`venv`) é uma pasta isolada com as bibliotecas do projeto,
para não bagunçar o Python do seu sistema.

```bash
cd cnj-pauta-pln
python3 -m venv .venv            # cria a pasta .venv/
source .venv/bin/activate        # ATIVA o ambiente (o prompt passa a mostrar "(.venv)")
pip install --upgrade pip
pip install -r requirements.txt  # instala tudo, inclusive tensorflow (para a MLP)
```

> Toda vez que abrir um terminal novo para trabalhar no projeto, rode de novo
> `source .venv/bin/activate`. Sem isso, os comandos `python src/...` usam o
> Python errado.

### C.3 Downloads do NLTK (automático)

O **NLTK** é uma biblioteca de PLN; usamos dela a lista de *stopwords* em
português (palavras muito comuns como "de", "que", "para", que não ajudam a
distinguir assuntos). **Você não precisa baixar nada à mão**: o próprio código
(`src/text_utils.py`) chama `nltk.download("stopwords")` na primeira vez. Se
quiser adiantar:

```bash
python -c "import nltk; nltk.download('stopwords')"
```

### C.4 Pré-requisito de dados: o *gold set* humano

O arquivo **`reports/gold_labels.csv`** já vem versionado no repositório. Ele é o
**gold set** — a classificação feita **à mão por uma pessoa**, contra a qual os
modelos serão avaliados. Tem duas colunas:

- `id` — o identificador da notícia;
- `gold` — a classe atribuída pelo humano: um número de **0 a 9** (ver a tabela
  das 10 classes na Fase 5/Fase 6) **ou** a palavra `indefinido` quando a notícia
  não cabia em nenhuma classe.

São **195 notícias anotadas**: 173 com classe 0–9 e 22 marcadas `indefinido`
(estas últimas são excluídas da avaliação). Esse arquivo é **entrada obrigatória
da Fase 6** (classificação). Não o apague nem o regenere — ele representa trabalho
humano e não é reproduzível por código.

> Não confunda com `reports/gold_template.csv`, que é apenas um *molde vazio*
> gerado pelo código para uma futura rodada de anotação (coluna `classe` em
> branco). A avaliação usa o `gold_labels.csv`, que já está preenchido.

### C.5 Aviso de runtime: TensorFlow × PyTorch (importante)

Duas bibliotecas de *deep learning* convivem no projeto:

- **TensorFlow/Keras** — usado pela rede neural MLP (Fase 6, Modelo B).
- **PyTorch** — usado pelo BERTopic, pelo BERTimbau e pelo NER.

Carregar **TensorFlow + PyTorch + numba no mesmo processo causa *segmentation
fault*** (um travamento de baixo nível). O projeto contorna isso de duas formas,
e por isso **a ordem dos scripts importa**:

1. `src/tf_guard.py` **bloqueia o TensorFlow** nos scripts que usam PyTorch
   (`topics.py`), para o UMAP não importá-lo por acidente.
2. Os *embeddings* do BERTimbau rodam em **processo separado**
   (`src/embed_bertimbau.py`); o `classify.py` só **lê** o resultado em cache.

Você não precisa fazer nada além de **rodar os scripts na ordem da Seção E**.

### C.6 Artefatos pesados não versionados (precisam ser regenerados)

Arquivos grandes e que dá para recriar **não estão no Git** e serão gerados quando
você rodar o pipeline:

- `data/processed/embeddings.npy` (embeddings das notícias);
- `data/processed/bertopic_model/` (o modelo de tópicos treinado);
- `data/processed/bertimbau_embeddings.npy` (embeddings do BERTimbau).

Já o **snapshot dos dados coletados** (`data/raw/noticias.jsonl`) e o
**gold set** estão versionados, então você pode reproduzir as Fases 2–6 sem
coletar de novo.

### C.7 Smoke test de setup

"Smoke test" = um teste rápido só para ver se "sai fumaça", isto é, se o básico
funciona antes de investir tempo. Rode:

```bash
# 1) o ambiente está ativo e as libs principais importam?
python -c "import pandas, numpy, sklearn, bertopic, torch, tensorflow; print('OK libs')"

# 2) os dados de entrada e o gold existem?
wc -l data/raw/noticias.jsonl      # esperado: 983
head -2 reports/gold_labels.csv    # esperado: cabeçalho 'id,gold' + 1 linha
```

Se as três linhas responderem sem erro (`OK libs`, `983 ...`, e o cabeçalho),
o ambiente está pronto.

---

## D. As etapas, uma a uma

Cada fase segue o mesmo molde: **Objetivo · Comando · O que acontece por baixo ·
O que é gerado · Como testar**. Os comandos foram conferidos no `argparse` real
de cada script — todos aceitam `-h` (ex.: `python src/collect.py -h`) para listar
as opções.

---

### Fase 1 — Coleta

- **Objetivo.** Baixar as notícias da Agência CNJ direto do site, de forma
  respeitosa e reproduzível.
- **Comando.**
  ```bash
  python src/collect.py --after 2025-12-21 --before 2026-06-21
  ```
  Opções: `--after`/`--before` (datas `YYYY-MM-DD`, inclusive); `--months N`
  (janela relativa a hoje, usada se você omitir `--after`); `--dry-run` (só
  **conta** quantas notícias há na janela, sem baixar — bom para testar).
- **O que acontece por baixo.** O script conversa com a *API* do site (uma porta
  de entrada para dados, a WordPress REST API). Antes, ele **lê o `robots.txt`**
  (as regras de quem pode acessar o quê) e respeita um **intervalo de ~1,2 s entre
  requisições** e *backoff* (espera crescente) se o servidor pedir calma. É
  **idempotente**: rodar de novo não duplica — ele pula o que já baixou.
- **O que é gerado.** `data/raw/noticias.jsonl` — um arquivo *JSON Lines* (uma
  notícia por linha), cada uma com id, data, URL, título, corpo e categoria.
- **Como testar.**
  ```bash
  wc -l data/raw/noticias.jsonl     # ~983 linhas
  ```
  Como o snapshot já vem no repositório, esse número aparece mesmo sem recoletar.

---

### Fase 2 — Pré-processamento (limpeza)

- **Objetivo.** Transformar o texto bruto em um *corpus* limpo e sem repetições,
  pronto para análise.
- **Comando.**
  ```bash
  python src/preprocess.py
  ```
  Opções: `--min-chars 250` (descarta corpos curtos demais para modelar);
  `--jaccard 0.85` (limiar de semelhança para considerar duas notícias
  "quase iguais").
- **O que acontece por baixo.** Quatro faxinas: (1) remove o rodapé de créditos
  editoriais ("Texto:", "Edição:", "Agência CNJ de Notícias"); (2) mantém só
  o que está **em português** (detecção automática de idioma); (3) remove
  **duplicatas exatas** e **quase-duplicatas** (republicações) usando *MinHash*,
  um jeito rápido de estimar o quanto dois textos se sobrepõem; (4) cria campos
  derivados (mês, nº de palavras) e uma versão normalizada do texto.
- **O que é gerado.** `data/interim/noticias_limpo.parquet` — tabela em formato
  *Parquet* (eficiente para colunas) com as notícias limpas.
- **Como testar.**
  ```bash
  python -c "import pandas as pd; d=pd.read_parquet('data/interim/noticias_limpo.parquet'); \
print('linhas:', len(d)); print('idiomas:', d['idioma'].unique())"
  ```
  Esperado: **979 linhas** e idioma `['pt']` apenas. (983 brutas → 979 após
  remover curtas, não-pt e duplicatas.)

---

### Fase 3 — EDA (Análise Exploratória de Dados)

- **Objetivo.** Olhar o corpus antes de modelar: volume por mês, tamanho das
  notícias, palavras mais frequentes. *EDA* = explorar para criar intuição.
- **Comando.** É um *notebook* (documento interativo de código + gráficos).
  Abra no Jupyter **ou** execute-o de ponta a ponta sem abrir:
  ```bash
  jupyter nbconvert --to notebook --execute --inplace notebooks/01_eda.ipynb
  ```
- **O que acontece por baixo.** O notebook lê o Parquet da Fase 2, conta notícias
  por mês e categoria, mede o comprimento dos textos, lista os termos mais comuns
  e desenha uma *nuvem de palavras* (wordcloud).
- **O que é gerado.** Seis figuras em `reports/figures/`:
  `01_volume_por_mes.png`, `02_volume_por_categoria.png`,
  `03_distribuicao_comprimento.png`, `04_top_termos.png`,
  `05_wordcloud.png`, `06_volume_semanal.png`.
- **Como testar.**
  ```bash
  ls -1 reports/figures/0[1-6]_*.png    # devem aparecer as 6 figuras
  ```

---

### Fase 4a — Embeddings

- **Objetivo.** Converter cada notícia em um vetor de números que captura seu
  *significado* (não só as palavras), para a máquina poder medir semelhança.
- **Comando.**
  ```bash
  python src/embed.py
  ```
  Opções: `--model` (qual modelo de *embedding* usar; o padrão é multilíngue com
  bom português) e `--batch-size 32` (quantas notícias processar por vez).
- **O que acontece por baixo.** Um modelo *sentence-transformer* lê
  "título + corpo" de cada notícia e devolve um vetor de **768 números**. Vetores
  são normalizados para que a proximidade entre eles signifique proximidade de
  tema. Roda em CPU sem problema (são ~1.000 notícias).
- **O que é gerado.** `data/processed/embeddings.npy` (a matriz de vetores) e
  `data/processed/ids.npy` (os ids, na mesma ordem, para alinhamento).
- **Como testar.**
  ```bash
  python -c "import numpy as np; print(np.load('data/processed/embeddings.npy').shape)"
  ```
  Esperado: **`(979, 768)`** — 979 notícias, 768 números cada.

---

### Fase 4b — BERTopic (descoberta de temas)

- **Objetivo.** Descobrir, **sem rótulos prontos**, quais assuntos existem no
  corpus e consolidá-los em **10 classes temáticas** nomeadas.
- **Comando.**
  ```bash
  python src/topics.py --sizes 10 15 20
  ```
  `--sizes` lista os tamanhos mínimos de grupo a testar (o script escolhe o
  melhor automaticamente).
- **O que acontece por baixo.** O BERTopic pega os *embeddings* da Fase 4a,
  **reduz** sua dimensão com UMAP, **agrupa** com HDBSCAN e **descreve** cada
  grupo por suas palavras típicas (c-TF-IDF). Para cada `--size` ele mede a
  **coerência c_v** (o quanto as palavras de um tópico "combinam") e a
  **diversidade** (o quanto os tópicos não se repetem) e escolhe o melhor. As
  notícias que sobram como "ruído" são reatribuídas ao tópico mais próximo.
- **O que é gerado.** Em `data/processed/`: `bertopic_model/` (o modelo),
  `topic_info.csv` (tópico → tamanho → termos), `topic_eval.csv` (as métricas de
  cada `--size`) e **`doc_topics.parquet`** (a classe atribuída a cada notícia —
  este é o **rótulo fraco** que a Fase 6 vai tentar aprender).
- **Como testar.**
  ```bash
  cat data/processed/topic_eval.csv
  ```
  Esperado: a linha vencedora é `min_topic_size=20` → **10 tópicos**,
  **c_v ≈ 0,777**, diversidade **1,0**, ~29% de ruído bruto. (Os tamanhos 10 e 15
  dão tópicos demais e menos coerentes — por isso 20 vence.)

---

### Fase 5 — Deriva temporal

- **Objetivo.** Ver **como a pauta se move no tempo**: detectar semanas em que um
  tema disparou ("picos") e cruzar com eventos verificáveis.
- **Comando.**
  ```bash
  python src/drift.py --freq W --z 1.5
  ```
  Opções: `--freq` (agrupamento temporal — `W` = semanal, `M` = mensal);
  `--z 1.5` (quão "fora do normal" uma semana precisa estar, em desvios-padrão,
  para contar como pico); `--use-reduced` (usa todas as notícias em vez de só as
  de alta confiança — padrão é só as de alta confiança).
- **O que acontece por baixo.** Monta uma matriz **tópico × semana**, calcula um
  *z-score* (quantos desvios-padrão acima da média) por tópico e marca como pico
  as semanas que ultrapassam o limiar. Para cada pico, anexa as **manchetes reais**
  daquela semana (evidência) e cruza com `reports/eventos_cnj.csv`.
- **O que é gerado.** `data/processed/topic_week_counts.csv` (a matriz) e
  `data/processed/topic_peaks.csv` (os picos + manchetes). Os gráficos
  (streamgraph, tópicos no tempo) são desenhados pelo notebook
  `03_temporal_drift.ipynb` → figuras `10`, `11`, `12`.
- **Como testar.**
  ```bash
  tail -n +2 data/processed/topic_peaks.csv | wc -l    # esperado: 20 picos
  ```
  Abra o CSV: cada linha traz tópico, semana, contagem, z-score e as manchetes
  que comprovam o pico.

---

### Fase 6 (pré-passo) — Embeddings BERTimbau

- **Objetivo.** Gerar um **segundo tipo de embedding**, agora com o **BERTimbau**
  (um BERT treinado em português), para alimentar o terceiro classificador da
  Fase 6.
- **Comando.**
  ```bash
  python src/embed_bertimbau.py
  ```
  (Sem opções — processa o corpus inteiro.)
- **O que acontece por baixo.** Roda em **processo separado, só com PyTorch**
  (lembre da Seção C.5: TF e PyTorch juntos travam). O BERTimbau lê
  "título + corpo" e produz um vetor de 768 números por notícia, salvo em cache.
- **O que é gerado.** `data/processed/bertimbau_embeddings.npy` e
  `bertimbau_ids.npy`.
- **Como testar.**
  ```bash
  python -c "import numpy as np; print(np.load('data/processed/bertimbau_embeddings.npy').shape)"
  ```
  Esperado: **`(979, 768)`**. (Se você esquecer este passo, o `classify.py` o
  executa sozinho como subprocesso — mas rodar antes deixa tudo explícito.)

---

### Fase 6 — Classificação supervisionada (o núcleo avaliado)

- **Objetivo.** Treinar modelos para prever as 10 classes e **medir a
  concordância com o gold humano**. Esta é a entrega central do projeto.
- **Comando.**
  ```bash
  python src/classify.py --epochs 50
  ```
  Opções: `--epochs 50` (quantas passadas de treino a rede neural faz);
  `--skip-bert` (pula o Modelo C/BERTimbau, útil para iterar rápido).
- **Pré-requisito.** **`reports/gold_labels.csv`** (Seção C.4) precisa existir —
  é contra ele que a avaliação acontece. O script também **remove o gold do
  treino** para não "colar" (sem isso, a nota seria inflada artificialmente).
- **O que acontece por baixo.** Treina **três modelos** sobre features
  *independentes* do clustering que gerou os rótulos:
  - **A. Naive Bayes** (baseline): TF-IDF + um classificador probabilístico
    simples.
  - **B. MLP Keras** (o foco do curso): uma rede neural densa (camadas
    Dense/ReLU/softmax, otimizador Adam). É treinada **com e sem Dropout** para
    **demonstrar overfit** (a rede decora o treino) e como a regularização ajuda.
  - **C. BERTimbau**: usa os embeddings do pré-passo + uma regressão logística.

  Cada modelo é avaliado **contra o gold humano** (régua externa) e também num
  teste interno. Gera ainda o molde vazio `gold_template.csv` para futuras
  anotações.
- **O que é gerado.** `data/processed/classify_metrics.json` (todas as métricas);
  figuras `14_overfit_mlp.png` (curvas de overfit com/sem Dropout),
  `14b_regularizacao.png` (Dropout vs. L2) e `15_confusion_gold.png` (matrizes
  de confusão vs. gold). A figura `13_confusion_matrix.png` vem do notebook
  `04_supervised_classification.ipynb`.
- **Como testar.** O script imprime uma tabela comparando os modelos. Confira:
  ```bash
  python -c "import json; m=json.load(open('data/processed/classify_metrics.json')); \
[print(k, m['models'][k]['external']) for k in m['models']]"
  ```
  Valores esperados (régua externa, vs. gold):

  | Modelo | acurácia | F1-macro | kappa |
  |---|---|---|---|
  | Naive Bayes (baseline) | 0,543 | 0,496 | 0,490 |
  | **MLP Keras** | **0,809** | **0,798** | **0,788** |
  | BERTimbau | 0,792 | 0,787 | 0,769 |

  E as figuras `14`, `14b`, `15` devem existir em `reports/figures/`.

---

### Fase 6b — NER (entidades nomeadas)

- **Objetivo.** Descobrir **quem e o quê** dominam a comunicação: extrair nomes
  de pessoas, órgãos e lugares e ranqueá-los.
- **Comando.**
  ```bash
  python src/ner.py --min-score 0.90
  ```
  Opções: `--min-score 0.90` (confiança mínima: descarta entidades em que o
  modelo tem menos de 90% de certeza); `--max-chars 1500` (quantos caracteres do
  corpo ler por notícia — a maioria das entidades aparece no início).
- **O que acontece por baixo.** Um modelo de **NER** em português lê
  "título + início do corpo" e aponta as entidades. A saída crua é ruidosa, então
  passa por um **funil de limpeza** com contagem real em cada etapa: corte por
  confiança → remoção de preposições nas bordas → remoção de fragmentos de
  subpalavra → remoção de termos genéricos ("governo", "tribunal"). Depois agrega
  por **número de notícias distintas** e também **por classe temática**.
- **O que é gerado.** `data/processed/entidades.parquet` (uma linha por entidade),
  `entidades_top.csv` (ranking geral), `entidades_por_classe.csv` (ranking por
  tema) e a figura `16_top_entidades.png`.
- **Como testar.** O script imprime o funil e o Top 20. Confira o ranking e a
  taxa de resíduo:
  ```bash
  head -6 data/processed/entidades_top.csv
  ```
  Esperado (Top com nomes reais): **Conselho Nacional de Justiça** (409 notícias),
  **Edson Fachin** (129), **Brasília** (68), **PNUD** (40), **Mauro Campbell
  Marques** (39)… O funil reduz de **11.971 → 4.136** entidades, com apenas
  **0,77%** de fragmento residual. A figura `16` deve existir.

---

## E. Rodar tudo de uma vez

Com o ambiente ativo (`source .venv/bin/activate`), execute na ordem. Cada linha
depende da anterior:

```bash
# Fase 1 — coleta (idempotente; já há snapshot versionado, pode pular)
python src/collect.py --after 2025-12-21 --before 2026-06-21

# Fase 2 — limpeza  ->  data/interim/noticias_limpo.parquet
python src/preprocess.py

# Fase 4a — embeddings das notícias  ->  data/processed/embeddings.npy
python src/embed.py

# Fase 4b — descoberta de temas (BERTopic)  ->  doc_topics.parquet
python src/topics.py --sizes 10 15 20

# Fase 5 — deriva temporal  ->  topic_peaks.csv
python src/drift.py --freq W --z 1.5

# Fase 6 (pré) — embeddings BERTimbau (processo separado, só PyTorch)
python src/embed_bertimbau.py

# Fase 6 — classificação supervisionada (núcleo)  ->  classify_metrics.json
python src/classify.py --epochs 50

# Fase 6b — NER  ->  entidades_top.csv + figura 16
python src/ner.py --min-score 0.90

# Notebooks — geram as figuras 01-12 em reports/figures/
jupyter nbconvert --to notebook --execute --inplace notebooks/01_eda.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/02_topic_modeling.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/03_temporal_drift.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/04_supervised_classification.ipynb
```

> **Ordem importa** (Seção C.5): `topics.py` bloqueia o TensorFlow; `classify.py`
> usa o TensorFlow; o BERTimbau roda à parte. Rodar nesta sequência evita o
> *segfault*.

---

## F. Mapa de arquivos

### `src/` — scripts do pipeline

| Arquivo | O que faz |
|---|---|
| `collect.py` | Fase 1: baixa as notícias da API do CNJ (robots.txt, rate limit, idempotente). |
| `preprocess.py` | Fase 2: limpa, filtra português e remove duplicatas (MinHash). |
| `embed.py` | Fase 4a: gera os embeddings multilíngues das notícias. |
| `topics.py` | Fase 4b: roda o BERTopic e consolida a taxonomia de 10 classes. |
| `drift.py` | Fase 5: monta a série temporal por tópico e detecta picos. |
| `embed_bertimbau.py` | Fase 6 (pré): gera embeddings BERTimbau em processo separado. |
| `classify.py` | Fase 6: treina NB/MLP/BERTimbau e avalia contra o gold. |
| `ner.py` | Fase 6b: extrai e limpa as entidades nomeadas. |
| `text_utils.py` | Fonte única (sem libs pesadas) da taxonomia, stopwords e listas de limpeza do NER — garante que todas as fases usem os mesmos rótulos. |
| `tf_guard.py` | Bloqueia o TensorFlow nos processos PyTorch para evitar o segfault. |

### `notebooks/` — exploração e figuras

| Notebook | O que faz |
|---|---|
| `01_eda.ipynb` | Análise exploratória; figuras 01–06. |
| `02_topic_modeling.ipynb` | Visualiza os tópicos do BERTopic; figuras 07–09. |
| `03_temporal_drift.ipynb` | Visualiza a deriva no tempo; figuras 10–12. |
| `04_supervised_classification.ipynb` | Visualiza a classificação e a confusão; figura 13. |

---

## G. O que os resultados significam

**1. A categoria oficial do site não revela a pauta.** Quase todas as notícias
caem no rótulo editorial "Agência CNJ de Notícias". Foi por isso que precisamos
*descobrir* os temas: o BERTopic recuperou **10 tópicos coesos** (coerência
c_v ≈ 0,78; diversidade 1,0) que a categorização de origem não expunha.

**2. Dá para classificar automaticamente — e a MLP é a melhor.** Contra o gold
humano, a **MLP Keras** atinge **F1-macro 0,80 / kappa 0,79** e o **BERTimbau**
**0,79 / 0,77** — *concordância substancial* com a pessoa que anotou à mão. O
**Naive Bayes** (baseline simples) fica bem atrás (F1 0,50), o que mostra que vale
a pena usar um modelo mais expressivo.

**3. A análise de overfit é honesta.** Sem regularização, a rede chega a 100% de
acerto no treino mas estaciona na validação — o retrato clássico de *overfit*. O
estudo mostra um resultado **não óbvio**: em features TF-IDF esparsas com poucos
dados, o **Dropout não ajudou** e o L2 forte levou a *underfit*; o modelo final
usa Dropout moderado + parada antecipada (figuras 14 e 14b).

**4. A pauta tem sazonalidade clara.** Foram detectados **20 picos** semanais,
casados com eventos verificáveis: infância (maio), sustentabilidade (Semana da
Pauta Verde, junho), violência doméstica (Mês da Mulher, março), saúde
(Estratégia Cuidar). Temas como *justiça itinerante* e *IA / Justiça 4.0* crescem
de forma estrutural.

**5. A comunicação gira em torno do próprio CNJ.** O NER confirma que **Conselho
Nacional de Justiça** (409 notícias) e o presidente **Edson Fachin** (129)
dominam, seguidos de parceiros (**PNUD**) e tribunais/estados.

### Limitações honestas (leia antes de citar números)

- **Gold pequeno (173 notícias).** As métricas têm margem de incerteza; classes
  raras (ex.: "Precatórios", F1 baixo) são pouco representadas.
- **NER trunca o corpo** (~1.500 caracteres): entidades citadas só no fim da
  matéria escapam. A taxa de fragmento residual (0,77%) é declarada, não escondida.
- **Os "tópicos" são uma leitura do corpus, não a verdade absoluta** — outra
  semente ou outro `--size` poderia reorganizá-los. Por isso a taxonomia é fixada
  e verificada por palavras-âncora a cada execução.
- **Avaliação sem vazamento, mas com rótulo fraco na origem.** O alvo de treino
  vem do clustering (máquina), não de humanos; o gold serve justamente para medir
  o quanto isso se sustenta. Validações antigas que treinavam *com* o gold dentro
  reportavam kappa ~0,91 — número **inflado** e abandonado.

Para o detalhamento metodológico e a auto-auditoria adversarial, ver
`docs/limitacoes.md`; para as referências com DOIs, `docs/referencias.md`; para a
coleta, `docs/coleta.md`.
