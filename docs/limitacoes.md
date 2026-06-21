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

### Validação supervisionada (Fase 6)
- **Anotador único** (o assistente). **Não há concordância inter-anotador**
  independente; o kappa reportado é predição×gold e rótulo-fraco×gold, não
  humano×humano. Risco de o anotador, ciente da taxonomia do modelo, **alinhar-se
  inconscientemente** a ele.
- **Gold pequeno (173 rótulos)** e estratificado pelos próprios rótulos fracos,
  o que pode **superrepresentar** casos "fáceis" de cada tópico.
- **Independência apenas parcial:** TF-IDF é um espaço distinto do de embeddings,
  mas os *rótulos* de treino vêm do BERTopic (derivado de embeddings). A validação
  mede consistência, não verdade externa absoluta.
- **F1=0,91 é otimista:** exclui 22 casos `indefinido` (~11% da amostra) —
  justamente os difíceis. Incluí-los reduziria as métricas.

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
  de título/lead, com correção de erros do modelo (ex.: feminicídio→saúde) — o que
  mostra independência de julgamento em casos concretos, mas não substitui um
  segundo anotador humano.

- **"F1 0,91 com 29% de outliers descartados é seletivo."** Correto: as métricas
  vivem no subconjunto de alta confiança. O texto reporta ambos (F1 intrínseco
  0,81 no espaço completo de rótulos fracos; 0,91 contra gold limpo).

- **"Tudo isso generaliza?"** Não. É um estudo de caso de 6 meses de **um** órgão.
  Não se afirma validade externa para outros períodos ou instituições.

## 3. LGPD / ética

- O acervo é jornalístico, público e institucional. Há **nomes de magistrados**
  em notícias disciplinares (T8) — dados pessoais em contexto de publicidade
  oficial e interesse público. O uso aqui é analítico/agregado; recomenda-se
  cautela em qualquer reuso que isole indivíduos.
- Coleta respeitou robots.txt, rate limit (≥1,2 s) e backoff (ver `coleta.md`).

## 4. Trabalhos futuros

- Segundo anotador humano + concordância inter-anotador (kappa de Cohen real).
- Janela de 12+ meses para separar sazonalidade de tendência estrutural.
- Modelo de embeddings pt-BR nativo (BERTimbau) como comparação ao multilíngue.
- Fontes externas auditáveis de eventos (DOU, atos normativos do CNJ) para
  cruzamento causal mais forte.
- Análise de subtópicos hierárquica para os tópicos largos (T0, T3, T9).
