# Limitações e Auto-auditoria Adversarial

Documento de honestidade metodológica. Registra limitações conhecidas e submete
o trabalho a uma crítica adversarial — "o que um avaliador cético diria?" — com
as mitigações efetivamente adotadas (ou a ausência delas).

## 1. Limitações por fase

### Coleta (Fase 1)
- **Janela de 6 meses** (21/12/2025–21/06/2026): dezembro/2025 e junho/2026 estão
  **parciais**; comparações mensais nesses extremos são enviesadas para baixo.
- **Autoria não recuperável:** a WP REST API retorna apenas o `id` do autor; a
  autoria individual não foi resolvida (conteúdo institucional, raramente
  assinado). O campo `autoria` guarda `author_id:<n>`.
- **Conteúdo é alvo móvel:** matérias podem ter sido editadas após a publicação
  (`modified` registrado). O snapshot versionado no git congela a análise.
- **Categorias-fonte genéricas:** 2–3 rótulos cobrem quase tudo — úteis como
  motivação, inúteis como *ground truth* fino.

### Pré-processamento (Fase 2)
- **Dedup semântico leve (MinHash, Jaccard≥0,85):** removeu apenas 2 quase-
  duplicatas. O limiar é conservador; republicações com edição moderada podem ter
  escapado. Não houve avaliação formal de recall do deduplicador.
- **Filtro de idioma** roda sobre os 1.500 primeiros caracteres; textos curtos ou
  mistos podem ser mal classificados (1 `es` removido — não auditado exaustivamente).
- **Remoção de boilerplate** é baseada em regras (marcadores de crédito); pode
  cortar conteúdo legítimo que use "Fonte:"/"Texto:" no terço final, ou deixar
  passar assinaturas não catalogadas (ex.: siglas de Ascom de tribunais).

### Modelagem de tópicos (Fase 4)
- **Corpus homogêneo** (cosseno médio ≈0,69): o resultado é **sensível a
  hiperparâmetros**. A escolha `n_neighbors=10` + `cluster_selection_method="leaf"`
  foi necessária para evitar o colapso em 2 tópicos, mas é uma decisão que
  **infla outliers (29%)** e não é a única configuração defensável.
- **UMAP com `random_state` fixo** garante reprodutibilidade, porém desativa o
  paralelismo e representa **uma única realização** estocástica.
- **Seleção por máximo c_v** favorece soluções com **menos tópicos** (mais
  grossos). O modelo final (10 tópicos) mistura subtemas: T0 funde "itinerância",
  "cidadania" e "população em situação de rua"; T3 mistura "Corte IDH",
  "direitos humanos" e parte de "corregedoria ética". Configurações mais
  granulares (12 tópicos, c_v=0,72) existem e foram reportadas.
- **`reduce_outliers`** reatribui 29% dos documentos ao tópico mais próximo,
  inflando contagens com itens de baixa confiança — por isso a análise temporal
  usa os rótulos **brutos**. O efeito colateral é **viés de seleção**: ao
  descartar os 29% de outliers, descartam-se justamente os itens ambíguos/raros,
  que poderiam conter pauta emergente ainda não consolidada.

### Deriva temporal (Fase 5)
- **Cruzamento pico↔evento é correlacional, não causal.** Picos coincidirem com
  eventos não prova que o evento causou a pauta.
- **Circularidade parcial dos eventos:** vários "eventos" de `eventos_cnj.csv`
  são **inferidos das próprias notícias** que formam o pico (evidência interna,
  não fonte externa independente). Apenas as **observâncias de calendário**
  (8/3, 18/5, 5/6) são externas e verificáveis.
- **Sem fontes externas auditáveis** (números de resolução, datas oficiais): o
  *conhecimento do assistente tem corte em jan/2026*, anterior à maior parte da
  janela. Optou-se por **não inventar** referências externas — limitação assumida.
- **Detecção de picos frágil:** z-score sobre série semanal curta (26 semanas);
  o limiar 1,5 é arbitrário e tópicos pequenos têm alta variância (picos de n=4–5).

### Classificação supervisionada (Fase 6 — núcleo)
- **Anotador humano único** (a dupla/trio do trabalho). **Não há concordância
  inter-anotador** independente; o kappa reportado é predição×gold humano, não
  humano×humano. Risco de o anotador, ciente da taxonomia do modelo,
  **alinhar-se inconscientemente** a ela.
- **Gold pequeno (173 rótulos + 22 'indefinido')**, anotado contra os 10 rótulos
  da taxonomia da Fase 4.
- **Rótulos de TREINO são fracos:** vêm do BERTopic (`topic_raw`), não de humano.
  Mede-se se classificadores de features independentes (TF-IDF / embeddings
  BERTimbau) **reproduzem** a taxonomia e **concordam com o humano** — não a
  verdade absoluta. As features (TF-IDF lexical; embeddings BERTimbau) são um
  espaço distinto do UMAP/HDBSCAN que gerou os clusters, reduzindo circularidade.
- **Métricas honestas, sem vazamento:** ao contrário da validação antiga
  (`src/supervised.py`, kappa ≈ 0,91, que treinava com o gold dentro do conjunto),
  a Fase 6 **remove o gold do treino** (162/173 também eram rótulo fraco). O
  resultado cai para **kappa ≈ 0,77–0,79** (MLP/BERTimbau) — *concordância
  substancial*, e a leitura correta da independência.
- **NB falha em classes pequenas:** F1=0,0 em "Precatórios" (28 docs de treino) —
  baseline insuficiente; documentado, não mascarado.
- **`indefinido` excluído das métricas:** 22 casos (~11%) — justamente os
  ambíguos/difíceis. Incluí-los reduziria os números reportados.
- **Resultado negativo do Dropout:** em features TF-IDF esparsas com poucos
  dados, o Dropout **não corrigiu** o overfit (piorou `val_loss`); quem controla
  é o **L2 moderado** e o **EarlyStopping**. Reportado como achado, não escondido.

## 2. Auto-auditoria adversarial

> *"Um avaliador cético diria…"* — seguido da resposta honesta.

- **"Os 10 tópicos são poucos; você escondeu granularidade para inflar o c_v."**
  Procede em parte. O critério (máx. c_v) foi declarado *a priori* e as três
  configurações estão em `topic_eval.csv`. A de 12 tópicos é reportada no
  notebook 02. Não há cherry-picking oculto, mas a métrica escolhida tem viés
  conhecido para soluções grossas.

- **"A 'pauta não óbvia' (justiça itinerante/PopRua em alta) não é descoberta —
  está nos títulos."** Parcialmente justo: os títulos contêm o sinal. O valor
  está em **quantificar** o deslocamento (+7,2pp) e mostrá-lo invisível na
  taxonomia editorial (tudo era "Agência CNJ de Notícias"). Não se alega
  descoberta de algo semanticamente oculto.

- **"Os 'eventos verificáveis' são circulares — você lê o pico e nomeia o
  evento."** Procede para os eventos institucionais (assumido explicitamente). As
  observâncias de calendário são exceção genuína (externas). O cruzamento deve ser
  lido como **interpretativo**, não como teste causal.

- **"O gold set foi rotulado pela mesma entidade que rodou o modelo → kappa
  inflado."** Limitação real e assumida. Mitigação parcial: rotulação por leitura
  de título/lead, com correção de erros do modelo — o que mostra independência de
  julgamento em casos concretos, mas não substitui um segundo anotador humano.

- **"Você treinou no gold e testou no gold → métrica inflada."** Não nesta versão.
  O gold é **removido do treino** (162/173 também eram rótulo fraco). Por isso o
  kappa caiu de ~0,91 (validação antiga, com vazamento) para ~0,79 — é a versão
  honesta.

- **"Dropout não ajudou, então a MLP está errada?"** Não — o achado é legítimo:
  em features TF-IDF esparsas com amostra pequena, Dropout pode prejudicar. A
  análise mostra L2 moderado controlando o overfit e L2 forte gerando underfit
  (trade-off viés-variância). O modelo final usa Dropout + EarlyStopping conforme
  a arquitetura pedida no curso; o resultado é reportado como é.

- **"Tudo isso generaliza?"** Não. É um estudo de caso de 6 meses de **um** órgão.
  Não se afirma validade externa para outros períodos ou instituições.

## 2b. Respostas diretas à auto-auditoria exigida

- **O gold é humano e independente?** **Humano, sim** (anotação manual contra a
  taxonomia). **Independente, parcialmente:** anotador único, sem segundo
  anotador; mas é **removido do treino** (sem vazamento) e as features dos
  classificadores são distintas do espaço que gerou os rótulos fracos.
- **Outliers/indefinidos foram excluídos das métricas?** **Sim, e está
  declarado.** Treino usa rótulos fracos de alta confiança (`topic_raw != -1`);
  os 22 `indefinido` do gold são excluídos. A taxa bruta de outliers (29,42%) é
  reportada honestamente em `topic_eval.csv`.
- **Overfit foi observado e tratado?** **Sim.** `train_acc=1,0` vs `val_acc≈0,80`
  e subida de `val_loss` evidenciam overfit; tratado por **EarlyStopping** (modelo
  principal) e estudado com Dropout (não ajudou) e L2 (ajudou). Figuras 14 e 14b.
- **Por que classificação supervisionada e não só topic modeling?** Porque a
  **avaliação formal** do curso exige aprendizado supervisionado com técnicas
  específicas (TF-IDF, Naive Bayes, redes densas, Dropout, transformers) e medição
  contra **gold humano**. O BERTopic permanece como **descoberta exploratória**
  que *deriva a taxonomia*; ele não é avaliável contra verdade humana por si só.
- **Quais técnicas do curso foram usadas e onde?** Ver o *mapa de cobertura* no
  notebook `04_supervised_classification.ipynb` (seção 7) e no README: BoW/TF-IDF
  (Modelos A/B), Naive Bayes (A), rede densa Keras/ReLU/softmax/Adam (B),
  overfit/underfit + regularização Dropout/L2 (B), BERTimbau/Transformers (C +
  NER), embeddings (Fase 4 + C), split treino/val/teste estratificado (Fase 6).

- **O NER é confiável? A saída foi limpa ou maquiada?** **Reduzida, não
  perfeita — e medida.** A saída crua do modelo pt-BR é ruidosa: 11.971 spans
  brutos com fragmentos de subpalavra ("##J"), preposições penduradas
  ("Tribunal de Justiça **do**"), substantivos comuns tageados como entidade
  ("Judiciário", "Brasil", "Federal") e **nenhum corte de confiança** (score
  mínimo bruto 0,19). Aplicamos um funil explícito e auditável (`src/ner.py`,
  listas canônicas em `src/text_utils.py`): corte de score ≥0,90 → limpeza de
  bordas funcionais → filtro de fragmento → filtro de genérico, restando **4.136
  entidades finais** (34,6% do bruto; o corte de score sozinho descarta 62,5%).
  A **taxa de fragmento residual é 0,77%** (32 chaves ≤4 chars não-sigla) e
  consiste majoritariamente em entidades **legítimas** curtas (Acre, Rio, EUA,
  Haia, USP, TJRN), não em lixo de tokenizer — o resíduo de subpalavra "##"
  caiu a zero. Limitações que **permanecem**: (i) o rótulo de tipo
  (PER/ORG/LOC) do modelo é ruidoso e é tratado como informativo, não
  autoritativo; (ii) processamos só título + lead (≤1.500 chars do corpo), então
  entidades que só aparecem no fim de notícias longas escapam; (iii) o corte de
  0,90 troca recall por precisão — entidades reais de baixa confiança são
  perdidas. As contagens do NER devem ser lidas como **ordens de grandeza da
  saliência**, não como um censo exato de entidades.

## 3. LGPD / ética

- O acervo é jornalístico, público e institucional. Há **nomes de magistrados**
  em notícias disciplinares (T8) — dados pessoais em contexto de publicidade
  oficial e interesse público. O uso aqui é analítico/agregado; recomenda-se
  cautela em qualquer reuso que isole indivíduos.
- Coleta respeitou robots.txt, rate limit (≥1,2 s) e backoff (ver `coleta.md`).

## 4. Trabalhos futuros

- Segundo anotador humano + concordância inter-anotador (kappa de Cohen real) e
  rotulação do `reports/gold_template.csv` por mais de um anotador.
- Janela de 12+ meses para separar sazonalidade de tendência estrutural.
- **Fine-tuning** do BERTimbau (em vez de embeddings congelados + LogReg) para a
  classificação, comparando com a MLP sobre TF-IDF.
- Fontes externas auditáveis de eventos (DOU, atos normativos do CNJ) para
  cruzamento causal mais forte.
- Análise de subtópicos hierárquica para os tópicos largos (T0, T3, T9).
