# Taxonomia — corpus de 2 anos (MATERIAL PARA REVISÃO HUMANA)

Gerado por `src/taxonomy_review.py` a partir de execução real do BERTopic (mesma config da Fase 4, SEED=42). **Nada aqui é nomeado pela máquina.** Os tópicos abaixo são clusters não-supervisionados; cabe ao dono decidir (1) o nome de cada classe, (2) o número de classes (fundir/dividir), (3) a palavra-âncora de cada uma.

Corpus: **4394** notícias, janela 2024-06 a 2026-06.

A taxonomia antiga (6 meses, 10 classes) está apenas como pista de correspondência — ela vai desalinhar e isso é esperado.

---

Figura `reports/figures/08b_classes_2anos.png` gerada do modelo persistido por topics.py (best_min_topic_size=20 | n_topics=46).

## min_topic_size = 20

- Tópicos: **46** | coerência c_v: **0.6805** | diversidade: 0.8848 | outliers brutos: 55.53% (2440 docs, reatribuídos por c-TF-IDF para a contagem abaixo)

### Tópico 0 — 190 documentos

**Top-15 termos c-TF-IDF:** disciplinar, 0000, 00 0000, relator, 00, decisão, pad, magistrado, sessão, afastamento, sessão ordinária, ordinária, voto, plenário, administrativo disciplinar

**Títulos mais representativos:**

- Juíza que nomeou peritos sem formação contábil será investigada pelo CNJ
- Juiz do Mato Grosso do Sul responderá a PAD por suspeita de venda de decisões
- Mutirão do TJCE para revisão de prisões no semiaberto tem legalidade confirmada pelo CNJ
- CNJ aplica pena de remoção a juiz que depreciou magistrados e membros do MPF
- Desembargador mineiro acusado de conceder vantagem indevida é punido com pena de disponibilidade

**Correspondência com taxonomia antiga (6 meses):** Processos disciplinares / sessões (âncora 'disciplinar')


### Tópico 1 — 165 documentos

**Top-15 termos c-TF-IDF:** racial, racismo, equidade, equidade racial, negra, negras, plural, negros, racismo estrutural, programa plural, pessoas negras, raciais, memória, diversidade, estrutural

**Títulos mais representativos:**

- Mutirão Racial 2026 mobiliza tribunais para julgamento de processos em novembro
- Curso aborda aplicação do Protocolo para Julgamento com Perspectiva Racial no Judiciário
- Mutirão Racial e Mês Nacional do Júri são destaques da agenda do CNJ em novembro
- Tribunal do PI abre Semana da Consciência Negra com lançamento de cartilha sobre crimes raciais
- Tribunais concentram esforços para movimentar processos com temática racial no Mês da Consciência Negra

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 2 — 217 documentos

**Top-15 termos c-TF-IDF:** violência, mulher, doméstica, violência doméstica, mulheres, contra, contra mulher, doméstica familiar, violência contra, maria penha, penha, paz casa, maria, familiar, meninas

**Títulos mais representativos:**

- Judiciário baiano realiza mobilização em Eunápolis e Porto Seguro contra a violência de gênero
- Celeridade processual e mobilização da sociedade marcam a 32ª Semana Justiça pela Paz em Casa
- Sertão de Pernambuco recebe “Ação Meninas e Mulheres” do CNJ nos dias 4 e 5 agosto
- Justiça pela Paz em Casa: 27.ª edição da ação começa nesta segunda (19/8)
- Justiça do Ceará agenda 353 audiências em ação voltada ao combate da violência contra a mulher

**Correspondência com taxonomia antiga (6 meses):** Violência doméstica / mulheres (âncora 'violência')


### Tópico 3 — 195 documentos

**Top-15 termos c-TF-IDF:** conciliação, acordos, semana conciliação, pagamento, cejusc, trabalhista, semana, milhões, audiências, precatórios, beneficiários, trt, rpvs, nupemec, partes

**Títulos mais representativos:**

- 8ª edição do Mutirão de Precatórios de tribunal do Mato Grosso do Sul movimenta R$ 1,1 milhão
- Justiça do Trabalho do Paraná ajusta acordos em R$ 61,4 mi durante a Semana da Conciliação
- Justiça Federal no Tocantins teve 80% de aproveitamento das audiências de conciliação marcadas em 2025
- Tribunal conquista medalha de prata na 10ª Semana Nacional da Conciliação Trabalhista
- TRT-2 realiza 119 mediações coletivas e fecha quase 48% de acordos em 2025

**Correspondência com taxonomia antiga (6 meses):** Precatórios / corregedoria (âncora 'precatórios')


### Tópico 4 — 159 documentos

**Top-15 termos c-TF-IDF:** ia, artificial, inteligência artificial, inteligência, uso, uso ia, generativa, tecnologia, ferramentas, proteção dados, ferramenta, ia generativa, uso inteligência, dados, artificial ia

**Títulos mais representativos:**

- CNJ inicia coleta de informações sobre uso de inteligência artificial por tribunais
- Tribunal do Pará apresenta uso da IA na análise de documentos processuais
- Primeiro dia de audiência pública sobre IA na Justiça aborda controle e capacitação
- Webinário apresenta pesquisa sobre o uso de IA no Judiciário
- Corte do DF encerra o 1.º Encontro Nacional dos Tribunais Usuários do PJe sobre IA

**Correspondência com taxonomia antiga (6 meses):** IA / Conecta / Justiça 4.0 (âncora 'inteligência artificial')


### Tópico 5 — 102 documentos

**Top-15 termos c-TF-IDF:** inspeção, corregedoria, trabalhos, administrativos judiciais, setores administrativos, equipe corregedoria, inspeções, prazos processuais, extrajudiciais, equipe, administrativos, litigância abusiva, abusiva, prazos, litigância

**Títulos mais representativos:**

- Corregedoria Nacional inicia inspeção ordinária no Tribunal de Justiça do Espírito Santo
- Tribunal receberá comitiva da Corregedoria Nacional de Justiça para inspeção em março
- Inspeção da Corregedoria Nacional no TJRS é encerrada após semana de trabalhos
- Corregedoria Nacional abre trabalhos de inspeção em tribunal alagoano
- TJPI recebe inspeção ordinária da Corregedoria Nacional até quarta-feira (25/9)

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 6 — 115 documentos

**Top-15 termos c-TF-IDF:** amazonas, amazônia, am, amazônia legal, indígenas, tjam, manaus, povos, indígena, itinerante, legal, povos indígenas, boca acre, boca, itinerante cooperativa

**Títulos mais representativos:**

- Justiça Itinerante: equipe conhece principais demandas de território indígena no Amazonas
- Corregedor nacional encerra Semana Solo Seguro Amazônia em solenidade no Amazonas
- Justiça do Amazonas realiza ação para cadastro de profissionais indígenas
- Serviços ampliados e novos fluxos marcam Justiça Itinerante em Boca do Acre/AM e Xapuri/AC
- Profissionais de 50 instituições levaram serviços à população isolada no AM

**Correspondência com taxonomia antiga (6 meses):** Justiça itinerante / cidadania (âncora 'itinerante')


### Tópico 7 — 159 documentos

**Top-15 termos c-TF-IDF:** socioeducativo, adolescentes, socioeducativas, jovens, socioeducativa, medidas socioeducativas, sistema socioeducativo, audiências concentradas, concentradas, pse, infância, adolescente, infância juventude, juventude, gmf

**Títulos mais representativos:**

- Tribunal pernambucano promove o mês das inspeções em programas socioeducativos
- TJPE realiza inspeções em 100% dos programas de atendimento socioeducativo do estado
- Plataforma Socioeducativa chega a Rondônia, somando cinco estados em operação
- CNJ lança estratégia nacional para fortalecer o sistema socioeducativo
- Justiça do Tocantins realiza agendas para a qualificação do Sistema Socioeducativo

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 8 — 93 documentos

**Top-15 termos c-TF-IDF:** leitura, livros, cultura, livro, literárias, mentes, mentes literárias, culturais, prisional, liberdade, escrita, remição, biblioteca, sistema prisional, arte

**Títulos mais representativos:**

- CNJ e tribunal alagoano lançam Projeto Mentes Literárias em presídio de Maceió
- Ação inédita na Bahia inclui adolescentes no projeto Mentes Literárias
- Leitura transforma vidas e reduz conflitos no Centro de Detenção de Cáceres
- Reeducandas do Maranhão participam do projeto Mentes Literárias
- Mentes Literárias: juízes e juízas debatem acesso à cultura no sistema prisional

**Correspondência com taxonomia antiga (6 meses):** Sistema prisional / Pena Justa (âncora 'prisional')


### Tópico 9 — 76 documentos

**Top-15 termos c-TF-IDF:** feminina, gênero, mulheres, participação feminina, perspectiva gênero, incentivo participação, paridade, liderança, paridade gênero, igualdade gênero, protocolo, cargos, igualdade, perspectiva, participação

**Títulos mais representativos:**

- Evento no CNJ debate desafios para ampliar presença de mulheres no Judiciário
- Seminário debate presença de mulheres no sistema de justiça nesta quinta (26)
- Participação institucional feminina no Judiciário avança no Brasil
- Evento debate os avanços da participação feminina no Poder Judiciário e os desafios a serem enfrentados
- Justiça Federal da 8ª Região lança cadastro do repositório de mulheres juristas

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 10 — 97 documentos

**Top-15 termos c-TF-IDF:** direitos humanos, humanos, corte idh, corte, idh, interamericana, direitos, interamericano, sistema interamericano, corte interamericana, interamericana direitos, fachin, interamericano direitos, internacionais, decisões

**Títulos mais representativos:**

- CNJ fortalece integração entre Justiça brasileira e sistema interamericano de direitos humanos
- CNJ reúne tribunais para fortalecer proteção de direitos humanos
- Novos protocolos do CNJ ampliam a cultura de direitos humanos no Judiciário
- Corte Interamericana inicia atividades no Brasil com sessão de abertura no STF
- Em primeira reunião à frente do ODH, ministro Fachin reforça compromisso do Observatório com a democracia

**Correspondência com taxonomia antiga (6 meses):** Direitos humanos / Corte IDH (âncora 'humanos')


### Tópico 11 — 123 documentos

**Top-15 termos c-TF-IDF:** encontro, evento, programação, juizados, youtube, memória, juizados especiais, boas práticas, inscrições, patrimônio cultural, boas, canal, especiais, contará, patrimônio

**Títulos mais representativos:**

- Estão abertas as inscrições para a II Jornada de Boas Práticas em Tutelas Coletivas
- Seminário do CNJ destaca boas práticas na gestão processual do Judiciário
- 31ª edição do Disseminando Boas Práticas do Poder Judiciário acontece na terça (23)
- Último dia para as inscrições do 18.º Encontro Nacional do Poder Judiciário
- Justiça mais próxima, transparente, inclusiva e acessível será debatida por profissionais de comunicação do Judiciário

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 12 — 127 documentos

**Top-15 termos c-TF-IDF:** precatórios, sessão, sessão ordinária, ordinária, plenário, sessões, disciplinares, sustentação, virtuais, ordinária 2025, pauta, controle administrativo, gestão precatórios, 2025, sustentação oral

**Títulos mais representativos:**

- CNJ realizará segunda edição da Semana Nacional dos Juizados Especiais
- CNJ realiza 16ª Sessão Ordinária de 2025 nesta terça (25/11)
- Grupo de trabalho do CNJ avança para definir diretrizes relacionadas à nova norma dos precatórios
- CNJ realiza 17ª Sessão Ordinária de 2025 com despedida de integrantes
- Consulta sobre critérios do Prêmio CNJ de Qualidade 2025 já está à disposição dos tribunais

**Correspondência com taxonomia antiga (6 meses):** Processos disciplinares / sessões (âncora 'disciplinar'); Precatórios / corregedoria (âncora 'precatórios')


### Tópico 13 — 140 documentos

**Top-15 termos c-TF-IDF:** auditoria, auditoria interna, metas, transparência, interna, meta, ranking, gestão, metas nacionais, governança, ranking transparência, nacionais, riscos, jud, pesquisa

**Títulos mais representativos:**

- Pesquisa atualizará dados sobre percepção e avaliação do Judiciário
- Consulta pública envolve a sociedade na elaboração de Metas Nacionais do Judiciário para 2025
- Está no ar o regulamento do Ranking da Transparência do Judiciário 2026
- CNJ reabre edital para realização de pesquisa sobre litigância predatória
- Com nova formação, conselho consultivo sobre pesquisas judiciárias realiza primeira reunião de trabalho

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 14 — 71 documentos

**Top-15 termos c-TF-IDF:** lgbtqia, lgbtqiapn, trans, assédio, pessoas lgbtqia, discriminação, assédio moral, sexual, diversidade, moral, casamento, rogéria, população lgbtqia, gênero, casais

**Títulos mais representativos:**

- Especialistas debatem aspectos jurídicos do registro civil de pessoas LGBTQIA+
- Evento do CNJ pauta desafios e oportunidades para a inclusão efetiva de pessoas LGBTQIA+
- Justiça do Trabalho reforça compromisso com direitos da população LGBTQIA+
- Cartilha aborda direitos da comunidade LGBTQIAPN+
- Promoção e proteção dos direitos LGBTQIA+ são tema de encontro no CNJ nos dias 25 e 26/6

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 15 — 130 documentos

**Top-15 termos c-TF-IDF:** pena, pena justa, penais, justa, prisional, penal, execução, sistema prisional, plano, plano pena, prisões, dmf, fazendo, custódia, alternativas

**Títulos mais representativos:**

- Justiça catarinense se prepara para mutirão processual penal
- Início do Pena Justa para retomada de controle das prisões marcou ações do CNJ em 2025
- CNJ dá início às preparações para o Mutirão Processual Penal de 2024
- Central integrada instalada na Paraíba lança novo olhar sobre penas alternativas à prisão
- Novo Cniep se ajusta a necessidades da magistratura para qualificar inspeções

**Correspondência com taxonomia antiga (6 meses):** Sistema prisional / Pena Justa (âncora 'prisional')


### Tópico 16 — 81 documentos

**Top-15 termos c-TF-IDF:** deficiência, pessoas deficiência, acessibilidade, acessibilidade inclusão, pessoa deficiência, inclusão, libras, pessoa, direitos pessoas, pessoas, deficiência âmbito, barreiras, tea, autista, âmbito judicial

**Títulos mais representativos:**

- Justiça do Piauí lança cartilha de atendimento a PCDs e reforça compromisso com inclusão
- Judiciário busca a eliminação de barreiras para a inclusão de pessoas com deficiência
- Em cinco anos, resolução amplia acessibilidade para pessoas com deficiência na Justiça
- Lei Brasileira de Inclusão completa 10 anos e Justiça capixaba realiza ações de conscientização
- Diagnóstico aponta desafios da acessibilidade no Judiciário, mas destaca avanços na inclusão

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 17 — 92 documentos

**Top-15 termos c-TF-IDF:** inovação, laboratórios, laboratórios inovação, festlabs, inovadoras, prêmio inovação, laboratório, prêmio, soluções, fest labs, fest, labs, conecta, projetos, ideias

**Títulos mais representativos:**

- Caravana Conecta reúne tribunais do Nordeste em São Luís (MA) para compartilhar boas práticas em inovação
- Workshop em Maceió discute tecnologia e inovação com presidentes de TJs
- Caravana Conecta reúne soluções inovadoras do Centro-Oeste em Cuiabá
- Prêmio vai reconhecer soluções inovadoras para desafios da Justiça
- Tribunais do Sudeste apresentam soluções inovadoras para a transformação digital da Justiça

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 18 — 76 documentos

**Top-15 termos c-TF-IDF:** fundiária, regularização fundiária, regularização, solo seguro, solo, títulos, seguro, imóveis, propriedade, fundiária urbana, prêmio solo, urbana, famílias, seguro favela, reurb

**Títulos mais representativos:**

- Mais 60 títulos de imóvel são entregues a famílias de Fortaleza durante a Semana Solo Seguro
- Tribunal de Justiça do Rio já concedeu mais de mil títulos do Programa “Solo Seguro”
- Solo Seguro: inscrições para a 2.ª edição do prêmio seguem abertas até 31 de maio
- Projeto Terra: regularização fundiária avança em municípios gaúchos do Vale do Taquari
- Tribunal do Piauí faz regularização imobiliária da antiga sede da Maternidade D. Evangelina Rosa

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 19 — 100 documentos

**Top-15 termos c-TF-IDF:** conflitos, mediação, conciliação, solução conflitos, conciliar legal, cejusc, solução, conciliar, prêmio conciliar, métodos, minas, mediação conciliação, restaurativa, nupemec, comarca

**Títulos mais representativos:**

- Tribunal e Defensoria de MG promovem Mutirão de Conciliação na Comarca de Taiobeiras
- Conciliação no Amapá: Justiça Itinerante promove 95 audiências e celebra 33 acordos
- Tribunal do Pará instala primeiro Cejusc do 2.º Grau com foco na conciliação
- Tribunais de Minas Gerais se unem para solucionar conflitos fundiários
- Justiça do Mato Grosso do Sul realiza 1º Mutirão da Saúde e registra 60% de acordos

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 20 — 118 documentos

**Top-15 termos c-TF-IDF:** domicílio, domicílio judicial, judicial eletrônico, eletrônico, comunicações, br, jus br, jus, usuários, comunicações processuais, empresas, consulta, portal, judicial, cadastro

**Títulos mais representativos:**

- CNJ alerta para atualização no Domicílio Judicial Eletrônico
- Domicílio Judicial Eletrônico conclui cadastro compulsório de 1,2 milhão de empresas
- Órgãos públicos de todo o país têm até maio para regularizar adesão ao Domicílio Judicial Eletrônico
- Órgãos públicos já podem se cadastrar no Domicílio Judicial Eletrônico
- Ferramenta gratuita para cidadãos facilita consulta de comunicações processuais

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 21 — 68 documentos

**Top-15 termos c-TF-IDF:** curso, cursos, java, ceajud, ciência dados, avançado, superior, autoinstrucional, capacitações, capacitação, ciência, superior trabalho, bnmp, sngb, avançados

**Títulos mais representativos:**

- Webinário apresenta novos cursos de ciência de dados do Justiça 4.0
- CNJ lança capacitação sobre o Domicílio Judicial Eletrônico para pessoa física
- Justiça 4.0 realiza webinário para apresentar novos cursos avançados de ciência de dados
- CNJ lança curso inédito para ferramenta de mineração de processos judiciais
- CNJ lança curso sobre ferramenta de IA generativa para servidores do Judiciário

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 22 — 72 documentos

**Top-15 termos c-TF-IDF:** desembargador, memória, documental, comarca, foro, torcedor, catarina, arenas, sc, paz arenas, santa catarina, gestão documental, arquivo, santa, tjmg

**Títulos mais representativos:**

- Tribunal goiano apresenta balanço do projeto Raízes Kalungas em audiência pública
- Tribunal do Amapá alinha com Ministério Público informações sobre uso do PJe
- Justiça do Pará faz a eliminação sustentável de 7.021 processos físicos
- Tribunal do Piauí instala nova Central de Inquéritos em Floriano
- Programa Novos Caminhos é apresentado para os TJs de SP, PR e RR

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 23 — 69 documentos

**Top-15 termos c-TF-IDF:** eleitoral, eleições, eleitores, votação, tse, eleitorais, tre, eleitoras, eleitor, urnas, eleitoras eleitores, urna, votar, processo eleitoral, deficiência

**Títulos mais representativos:**

- TSE reafirma compromisso com a inclusão eleitoral
- Justiça Eleitoral do Acre intensifica atendimentos a povos indígenas e em áreas de difícil acesso
- Eleições 2024: Justiça Eleitoral fortalece presença de indígenas e quilombolas no Tocantins
- Justiça de Sergipe promove ações educativas do Projeto Eleitora e Eleitor do Futuro
- TSE celebra 30 anos da urna eletrônica com foco na segurança do voto e no combate à desinformação

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 24 — 78 documentos

**Top-15 termos c-TF-IDF:** pena justa, justa, pena, plano, prisional, sistema prisional, penais, plano pena, políticas penais, 347, sistema, penal, inconstitucional, gmf, coisas inconstitucional

**Títulos mais representativos:**

- Justiça pernambucana promove reunião para construir o Plano Pena Justa no estado
- Justiça de PE conclui oficinas do Pena Justa que buscam soluções para o sistema prisional
- Justiça do Ceará tem primeira reunião para dar andamento ao Plano Pena Justa
- Pena Justa: TRT da 7.ª Região e instituições parceiras debatem qualificação para egressos
- Plano Pena Justa apresenta alto índice de cumprimento no primeiro ano

**Correspondência com taxonomia antiga (6 meses):** Sistema prisional / Pena Justa (âncora 'prisional')


### Tópico 25 — 79 documentos

**Top-15 termos c-TF-IDF:** linguagem, linguagem simples, simples, pacto linguagem, selo linguagem, selo, comunicação, ementas, pacto, uso linguagem, compreensível, clara, acessível, trt pr, direta

**Títulos mais representativos:**

- Solenidade marca entrega do Selo Linguagem Simples a 47 órgãos da Justiça
- Linguagem simples: tribunal do Trabalho baiano adota medidas para padronizar ementas
- Turma do Tribunal do Trabalho paranaense implanta projeto-piloto de linguagem simples
- Linguagem simples: Justiça do Trabalho gaúcha lança glossário com expressões jurídicas
- Justiça do Trabalho mineira lança campanha pela linguagem simples “TRT, Explica aí”

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 26 — 92 documentos

**Top-15 termos c-TF-IDF:** saúde, fonajus, fonajus itinerante, judicialização, judicialização saúde, suplementar, medicamentos, direito saúde, natjus, fórum saúde, saúde suplementar, saúde pública, saúde fonajus, daiane, 1234

**Títulos mais representativos:**

- Enfam e CNJ promovem seminário sobre desafios e perspectivas da judicialização da saúde no Brasil
- VII Jornada de Direito da Saúde acontecerá em abril de 2025
- Fonajus Itinerante no Amapá: ações fortalecem diálogo entre Judiciário e Executivo para melhoria da saúde
- Fonajus Itinerante chega a Minas Gerais no dia 4 de junho
- Fonajus Itinerante será realizado em Santa Catarina a partir de 19 de março

**Correspondência com taxonomia antiga (6 meses):** Justiça itinerante / cidadania (âncora 'itinerante'); Saúde / judicialização / SUS (âncora 'saúde')


### Tópico 27 — 41 documentos

**Top-15 termos c-TF-IDF:** enac, exame, exame cartórios, prova, cartórios, cartórios enac, certame, habilitação, fgv, concursos, capitais, serviços notariais, candidatos, notariais, inscritos

**Títulos mais representativos:**

- Corregedoria Nacional acompanhará realização do 2º Enac neste domingo (28/9)
- 2º Enac: FGV divulga gabarito definitivo e resultado preliminar
- Inscrições para o 3º Exame Nacional dos Cartórios começam no dia 19/2
- Nota da Corregedoria Nacional de Justiça
- Resultados preliminares do Exame Nacional dos Cartórios são publicados

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 28 — 127 documentos

**Top-15 termos c-TF-IDF:** sustentabilidade, emissões, carbono, ambientais, sustentável, resíduos, ambiental, energia, climática, gases, estufa, efeito estufa, gases efeito, descarbonização, efeito

**Títulos mais representativos:**

- Sustentabilidade: serviço ambiental prestado por catadores deve ser valorizado por tribunais
- Tribunal do Piauí apresenta versão inicial do Plano de Descarbonização
- Pacto pela Sustentabilidade: tribunais terão 12 meses para desenvolverem práticas
- Judiciário acelera agenda de sustentabilidade e mira à neutralidade de carbono até 2030
- Juízo Verde: CNJ premia ações inovadoras em sustentabilidade

**Correspondência com taxonomia antiga (6 meses):** Sustentabilidade ambiental (âncora 'sustentabilidade')


### Tópico 29 — 71 documentos

**Top-15 termos c-TF-IDF:** execuções, execuções fiscais, fiscais, tributária, execução fiscal, cobrança, extinção, fiscal, dívida, dívida ativa, tributário, litigiosidade, milhões, protesto, pgfn

**Títulos mais representativos:**

- Execução fiscal: acordo entre CNJ e TJRN deve extinguir mais de 35 mil processos
- Presidente do CNJ recebe procuradora-geral da Fazenda Nacional para discutir ações conjuntas
- CNJ firma acordo com tribunal e governo da Bahia para extinguir execuções fiscais no estado
- Com política de eficiência, 12 milhões de execuções fiscais foram extintas
- Política de Eficiência das Execuções Fiscais: 10 milhões de processos extintos em menos de 2 anos

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 30 — 122 documentos

**Top-15 termos c-TF-IDF:** rua, situação rua, popruajud, pessoas situação, situação, população situação, população, atenção pessoas, pop, pop rua, comitê popruajud, mutirão, comitê, pessoas, rua jud

**Títulos mais representativos:**

- Justiça Federal de Mato Grosso participa, em Rondonópolis, de atendimento à população em situação de rua
- Corregedoria Nacional de Justiça marca presença no quarto dia do PopRuaJud Sampa + Registre-se
- Política judiciária para pessoas em situação de rua celebra quatro anos de avanços
- Mutirão atende a pessoas em situação de rua nesta terça (6/5), em Maceió (AL)
- Judiciário de Alagoas se une em prol da população em situação de rua

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 31 — 76 documentos

**Top-15 termos c-TF-IDF:** violência, doméstica, violência doméstica, mulher, medidas protetivas, protetivas, contra, mulheres, violência contra, doméstica familiar, enfrentamento violência, fonar, contra mulher, contra mulheres, risco

**Títulos mais representativos:**

- CNJ amplia proteção a mulheres do Judiciário com protocolo obrigatório contra violência doméstica
- Violência contra mulheres preocupa sociedade, e o Judiciário atua para enfrentar o problema, afirma Fachin
- Webinário do CNJ reforça integração entre Judiciário e Ligue 180 para proteger mulheres
- Observatório de Direitos Humanos do CNJ cria estrutura para integrar dados e ações sobre violência contra mulheres
- Presidente do CNJ acompanha instalação de varas de violência doméstica e familiar contra a mulher em SP

**Correspondência com taxonomia antiga (6 meses):** Violência doméstica / mulheres (âncora 'violência')


### Tópico 32 — 59 documentos

**Top-15 termos c-TF-IDF:** ambiental, verde, pauta verde, semana pauta, ambientais, ambiente, pauta, sustentabilidade, mudas, plantio, processos ambientais, semana, juizados, juizados especiais, fórum ambiental

**Títulos mais representativos:**

- Semana da Pauta Verde: Justiça potiguar realiza mutirão de conciliações em processos ambientais
- Justiça baiana participa da II Semana da Pauta Verde com foco na celeridade dos processos ambientais
- Judiciário Sustentável apresenta novo balanço e marca entrega de Prêmio Juízo Verde
- Conselheira do CNJ conhece iniciativas sustentáveis do Tribunal de Mato Grosso
- Conselheiro do CNJ participa de Encontro de Sustentabilidade em Mato Grosso

**Correspondência com taxonomia antiga (6 meses):** Sustentabilidade ambiental (âncora 'sustentabilidade')


### Tópico 33 — 65 documentos

**Top-15 termos c-TF-IDF:** escravo, trabalho escravo, tráfico pessoas, tráfico, trabalho infantil, infantil, trabalho, combate trabalho, escravidão, escravo tráfico, trabalhadores, trabalho decente, decente, análogas, exploração

**Títulos mais representativos:**

- 2.º Encontro do Fontet define prioridades no combate ao trabalho escravo e ao tráfico de pessoas
- Justiça do Trabalho da 8.ª Região inicia curso de capacitação para refugiados e migrantes
- Trabalhadores, entidades e acadêmicos contribuirão para política judiciária pelo trabalho decente
- Trabalho decente: uma das mais importantes metas buscadas pelo CNJ para a Justiça brasileira
- CNJ disponibiliza dados sobre indígenas, tráfico de pessoas e trabalho escravo

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 34 — 37 documentos

**Top-15 termos c-TF-IDF:** desaparecimento, vítimas, direitos humanos, humanos, sales, pimenta, desaparecimento forçado, óbito, familiares, pessoas desaparecidas, desaparecidas, forçado, ceavs, observatório, direitos

**Títulos mais representativos:**

- CNJ debate no Rio medidas para aprimorar atendimento a vítimas de violência de Estado
- CNJ realiza debate sobre desaparecimento forçado e justiça de transição
- CNJ convida rede de vítimas da violência estatal para atuar em Observatório de Direitos Humanos
- Justiça de Transição e desaparecimento forçado são temas de evento internacional do CNJ
- Observatório inicia 2026 acompanhando casos relacionados a conflitos fundiários, tragédias e crimes dolosos

**Correspondência com taxonomia antiga (6 meses):** Direitos humanos / Corte IDH (âncora 'humanos')


### Tópico 35 — 44 documentos

**Top-15 termos c-TF-IDF:** polícia judicial, segurança institucional, curso, formação, polícia, segurança, inteligência, policiais judiciais, dnpj, policiais, capacitação, socioeducativo, cursos, judicial, enfam

**Títulos mais representativos:**

- CNJ capacita mais de 4,6 mil pessoas no 6.º ciclo de formações sobre o Seeu
- DNPJ conclui 2024 com avanços na formação e na doutrina da polícia judicial
- CNJ apoia formação de juízes em início de carreira sobre tema penal e socioeducativo
- CNJ capacita mais de mil pessoas para aplicarem normas no sistema penal e socioeducativo
- CNJ e Enfam concluem primeira turma de curso sobre sistema socioeducativo

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 36 — 56 documentos

**Top-15 termos c-TF-IDF:** ações coletivas, coletivas, litigância, precedentes, abusiva, meta, processos, litigância abusiva, repetitivos, centros inteligência, júri, fonacor, inteligência, demandas, corregedorias

**Títulos mais representativos:**

- Evento sobre ações coletivas propõe nova lógica da Justiça para reduzir litigância
- CNJ realiza inspeção no TJMT para avaliar eficiência e transparência do Judiciário
- CNJ articula ações com a advocacia para acelerar desjudicialização e simplificar acesso à Justiça
- Corregedorias apontam boas práticas para atuação de correição
- Pesquisa inédita analisa litigância abusiva no Judiciário e propõe medidas de enfrentamento

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 37 — 57 documentos

**Top-15 termos c-TF-IDF:** saúde, prêmio saúde, suplementar, saúde pública, doação, natjus, judicialização, judicialização saúde, notas, fonajus, pública suplementar, aedo, saúde suplementar, doação órgãos, sus

**Títulos mais representativos:**

- CNJ premia melhores práticas judiciárias em saúde
- Ações focadas na melhoria da gestão processual são reconhecidas pelo Prêmio Justiça e Saúde
- Soluções inovadoras em saúde são premiadas durante Congresso do Fonajus
- Palestra sobre importância do NatJus encerra a Semana Nacional de Saúde na Paraíba
- Tribunais participam da 1.ª Semana Nacional da Saúde com ações integradas

**Correspondência com taxonomia antiga (6 meses):** Saúde / judicialização / SUS (âncora 'saúde')


### Tópico 38 — 82 documentos

**Top-15 termos c-TF-IDF:** itinerante, pai, atendimentos, kalungas, paternidade, vara itinerante, comunidades, cavalcante, cidadania, serviços, comunidade, raízes, raízes kalungas, carreta, pai presente

**Títulos mais representativos:**

- Justiça Itinerante realiza mais de 100 atendimentos na zona sul de Porto Alegre
- Justiça Itinerante realiza 51 atendimentos na primeira ação de 2025 em Porto Alegre (RS)
- Tribunal do MT inicia atendimentos em Bom Jesus do Araguaia e leva cidadania a regiões isoladas
- Justiça Itinerante encurta distâncias e garante direitos a comunidades indígenas de Amajari (RR)
- Jornada Terrestre de 2025: comunidade do Ariri (AP) recebe serviços de tribunal e parceiros

**Correspondência com taxonomia antiga (6 meses):** Justiça itinerante / cidadania (âncora 'itinerante')


### Tópico 39 — 100 documentos

**Top-15 termos c-TF-IDF:** itinerante, atendimentos, registro civil, registro, nascimento, registre, civil, serviços, emissão, certidão, carteira, cidadania, semana registro, documentação, casamento

**Títulos mais representativos:**

- Mais de 1,4 mil processos são movimentados em Juizado Itinerante da Justiça Federal do Tocantins
- Campanhas de registro civil de tribunal alagoano realizam mais de 13 mil atendimentos
- Juizado Itinerante em Porto Murtinho (MS) alcança 71% de acordo em audiências realizadas
- Fachin destaca escuta das comunidades no encerramento do Justiça Itinerante no Marajó
- Justiça Itinerante atende a Comunidade Quilombola de Conceição das Crioulas

**Correspondência com taxonomia antiga (6 meses):** Justiça itinerante / cidadania (âncora 'itinerante')


### Tópico 40 — 75 documentos

**Top-15 termos c-TF-IDF:** pje, conecta, soluções, soluções tecnológicas, tecnológicas, pdpj, pdpj br, programa, digital, transformação digital, tecnologia, banco sentenças, superior, tjdft, br

**Títulos mais representativos:**

- Com apoio do CNJ, Tribunal de Justiça do Paraná adere a novo sistema processual eletrônico
- Portal CNJ de Boas Práticas recebe dezesseis novos projetos
- Tecnologia da Informação no Judiciário é tema de série especial no Link CNJ
- CNJ institui diretrizes do Programa Conecta para nacionalização de soluções tecnológicas dos tribunais
- Com 37 projetos de tecnologia, Justiça 4.0 consolida inovação no Judiciário

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 41 — 58 documentos

**Top-15 termos c-TF-IDF:** fundiárias, soluções fundiárias, comissão soluções, comissão, indígenas, fundiários, soluções, conflitos fundiários, terras, povos, comissões, alcântara, conflito, terra, conflitos

**Títulos mais representativos:**

- CNJ recebe povo Pataxó para debater questões sobre o território ancestral
- Comissão de soluções fundiárias fará visita preparatória para mediação de conflitos de terra no sul da Bahia
- Judiciário realiza reuniões e escuta indígenas e proprietários de terra no sul da Bahia
- Comissão Nacional de Soluções Fundiárias acompanha negociações no Norte e Noroeste de MG
- Justiça de Mato Grosso reafirma compromisso com a solução de conflitos agrários

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 42 — 52 documentos

**Top-15 termos c-TF-IDF:** barroso, posse, fachin, conselheiros, conselheiro, presidentes, magistratura, edson fachin, supremo, edson, concurso, homenagem, stf, luís roberto, roberto barroso

**Títulos mais representativos:**

- Presidente do CNJ participa do XIX Consepre em Fortaleza
- Em São Luís, Barroso destaca ações do CNJ para tornar a Justiça acessível e inclusiva
- Conselheiro Pablo Coutinho recebe homenagem em sessão que encerra mandato no CNJ
- Em despedida do CNJ, ministro Salomão destaca ações da Corregedoria Nacional
- Panorama das políticas judiciárias demonstra papel agregador do CNJ para a Justiça

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 43 — 44 documentos

**Top-15 termos c-TF-IDF:** violência, mulheres, mulher, contra, violência contra, violência doméstica, doméstica, enfrentamento violência, violência digital, enfrentamento, contra mulheres, gênero, assédio, assédio sexual, homens

**Títulos mais representativos:**

- CNJ e Vivo voltam a disparar, neste 8/3, alertas sobre a importância do combate à violência contra as mulheres
- Tribunal do Mato Grosso do Sul lança Monitor da Violência contra a Mulher
- Projeto quer fortalecer o acesso à Justiça de vítimas de violência doméstica
- CNJ 20 anos: Justiça garante efetividade ao combate à violência contra mulheres
- CNJ visita projeto de referência na responsabilização de autores de violência contra mulheres em Rondônia

**Correspondência com taxonomia antiga (6 meses):** Violência doméstica / mulheres (âncora 'violência')


### Tópico 44 — 86 documentos

**Top-15 termos c-TF-IDF:** adoção, crianças, crianças adolescentes, sna, pretendentes, adolescentes, busca ativa, infância, criança, acolhimento, família, infância juventude, juventude, adolescente, criança adolescente

**Títulos mais representativos:**

- Coordenadoria da Infância de Alagoas debate estratégias de acolhimento com órgãos do estado
- Encontro discute avanços e desafios do Sistema Nacional de Adoção
- Ação da Justiça baiana promove atualização dos principais alertas do Sistema Nacional de Adoção
- Justiça reforça importância da adoção legal e amplia ações de proteção à infância no Amazonas
- TJRO promove oficina formativa para conselheiros tutelares e unidades de acolhimento

**Correspondência com taxonomia antiga (6 meses):** Infância e juventude (âncora 'crianças')


### Tópico 45 — 58 documentos

**Top-15 termos c-TF-IDF:** depoimento, crianças, crianças adolescentes, depoimento especial, infância, adolescentes, criança, criança adolescente, adolescente, protegida, sexual, proteção, infância juventude, juventude, abuso

**Títulos mais representativos:**

- CNJ inicia mobilização nacional para fortalecer proteção de crianças e adolescentes
- CNJ lança Mês da Infância Protegida com foco no enfrentamento à violência
- Mês da Infância Protegida: Como denunciar violência contra crianças e adolescentes
- Mês da Infância Protegida: políticas judiciárias protegem e asseguram direitos fundamentais
- Mês da Infância Protegida: mutirão antecipa depoimentos especiais de crianças e adolescentes

**Correspondência com taxonomia antiga (6 meses):** Infância e juventude (âncora 'crianças')


---

## min_topic_size = 15

- Tópicos: **66** | coerência c_v: **0.6681** | diversidade: 0.8712 | outliers brutos: 51.59% (2267 docs, reatribuídos por c-TF-IDF para a contagem abaixo)

### Tópico 0 — 164 documentos

**Top-15 termos c-TF-IDF:** racial, racismo, equidade racial, equidade, negras, negra, plural, negros, racismo estrutural, programa plural, pessoas negras, raciais, estrutural, perspectiva racial, discriminação

**Títulos mais representativos:**

- Mutirão Racial 2026 mobiliza tribunais para julgamento de processos em novembro
- Curso aborda aplicação do Protocolo para Julgamento com Perspectiva Racial no Judiciário
- Mutirão Racial e Mês Nacional do Júri são destaques da agenda do CNJ em novembro
- Tribunais concentram esforços para movimentar processos com temática racial no Mês da Consciência Negra
- Fóruns promovem equidade racial e direitos das populações indígenas

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 1 — 144 documentos

**Top-15 termos c-TF-IDF:** conciliação, acordos, semana conciliação, cejusc, milhões, audiências, nupemec, precatórios, semana, conflitos, pagamento, trt, solução, partes, valores

**Títulos mais representativos:**

- 8ª edição do Mutirão de Precatórios de tribunal do Mato Grosso do Sul movimenta R$ 1,1 milhão
- Justiça do Trabalho do Paraná ajusta acordos em R$ 61,4 mi durante a Semana da Conciliação
- Tribunal conquista medalha de prata na 10ª Semana Nacional da Conciliação Trabalhista
- Justiça Federal no Tocantins teve 80% de aproveitamento das audiências de conciliação marcadas em 2025
- Semana Nacional da Conciliação Trabalhista: 8.ª Região garante quase R$ 48 milhões em acordos

**Correspondência com taxonomia antiga (6 meses):** Precatórios / corregedoria (âncora 'precatórios')


### Tópico 2 — 151 documentos

**Top-15 termos c-TF-IDF:** ia, artificial, inteligência artificial, inteligência, uso, uso ia, generativa, ferramentas, tecnologia, ia generativa, ferramenta, proteção dados, uso inteligência, artificial ia, dados

**Títulos mais representativos:**

- CNJ inicia coleta de informações sobre uso de inteligência artificial por tribunais
- Tribunal do Pará apresenta uso da IA na análise de documentos processuais
- Primeiro dia de audiência pública sobre IA na Justiça aborda controle e capacitação
- Webinário apresenta pesquisa sobre o uso de IA no Judiciário
- Corte do DF encerra o 1.º Encontro Nacional dos Tribunais Usuários do PJe sobre IA

**Correspondência com taxonomia antiga (6 meses):** IA / Conecta / Justiça 4.0 (âncora 'inteligência artificial')


### Tópico 3 — 89 documentos

**Top-15 termos c-TF-IDF:** inspeção, corregedoria, setores administrativos, administrativos judiciais, equipe corregedoria, trabalhos, extrajudiciais, prazos processuais, litigância abusiva, abusiva, equipe, litigância, inspeções, arnoldo, serventias extrajudiciais

**Títulos mais representativos:**

- Tribunal receberá comitiva da Corregedoria Nacional de Justiça para inspeção em março
- Corregedoria Nacional inicia inspeção ordinária no Tribunal de Justiça do Espírito Santo
- Inspeção da Corregedoria Nacional no TJRS é encerrada após semana de trabalhos
- Corregedoria Nacional abre trabalhos de inspeção em tribunal alagoano
- TJPI recebe inspeção ordinária da Corregedoria Nacional até quarta-feira (25/9)

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 4 — 88 documentos

**Top-15 termos c-TF-IDF:** amazonas, amazônia, amazônia legal, am, manaus, tjam, legal, xapuri, boca acre, boca, seguro amazônia, itinerante cooperativa, solo, solo seguro, fundiária

**Títulos mais representativos:**

- Justiça Itinerante: equipe conhece principais demandas de território indígena no Amazonas
- Corregedor nacional encerra Semana Solo Seguro Amazônia em solenidade no Amazonas
- Justiça do Amazonas realiza ação para cadastro de profissionais indígenas
- Justiça Itinerante no Amazonas inicia atendimentos do primeiro semestre de 2025
- Serviços ampliados e novos fluxos marcam Justiça Itinerante em Boca do Acre/AM e Xapuri/AC

**Correspondência com taxonomia antiga (6 meses):** Justiça itinerante / cidadania (âncora 'itinerante')


### Tópico 5 — 88 documentos

**Top-15 termos c-TF-IDF:** domicílio, domicílio judicial, judicial eletrônico, eletrônico, comunicações, empresas, comunicações processuais, auditoria, cadastro, usuários, autenticação, judicial, ordens, plataforma, envio

**Títulos mais representativos:**

- CNJ alerta para atualização no Domicílio Judicial Eletrônico
- Órgãos públicos de todo o país têm até maio para regularizar adesão ao Domicílio Judicial Eletrônico
- Órgãos públicos já podem se cadastrar no Domicílio Judicial Eletrônico
- CNJ inicia cadastro compulsório de grandes e médias empresas no Domicílio Judicial Eletrônico
- Domicílio Judicial Eletrônico conclui cadastro compulsório de 1,2 milhão de empresas

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 6 — 115 documentos

**Top-15 termos c-TF-IDF:** conciliação, conflitos, mediação, conciliar, conciliar legal, solução conflitos, cejusc, solução, métodos, prêmio conciliar, consensuais, mediação conciliação, partes, trabalhista, minas

**Títulos mais representativos:**

- Tribunal e Defensoria de MG promovem Mutirão de Conciliação na Comarca de Taiobeiras
- Tribunais de Minas Gerais se unem para solucionar conflitos fundiários
- Tribunal do Pará instala primeiro Cejusc do 2.º Grau com foco na conciliação
- Justiça do Mato Grosso do Sul realiza 1º Mutirão da Saúde e registra 60% de acordos
- Conciliação no Amapá: Justiça Itinerante promove 95 audiências e celebra 33 acordos

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 7 — 78 documentos

**Top-15 termos c-TF-IDF:** feminina, gênero, mulheres, participação feminina, incentivo participação, paridade, liderança, perspectiva gênero, igualdade gênero, paridade gênero, igualdade, cargos, protocolo, perspectiva, participação

**Títulos mais representativos:**

- Evento no CNJ debate desafios para ampliar presença de mulheres no Judiciário
- Seminário debate presença de mulheres no sistema de justiça nesta quinta (26)
- Participação institucional feminina no Judiciário avança no Brasil
- Justiça Federal da 8ª Região lança cadastro do repositório de mulheres juristas
- Evento debate os avanços da participação feminina no Poder Judiciário e os desafios a serem enfrentados

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 8 — 135 documentos

**Top-15 termos c-TF-IDF:** socioeducativo, socioeducativas, socioeducativa, adolescentes, medidas socioeducativas, sistema socioeducativo, audiências concentradas, concentradas, pse, gmf, medida socioeducativa, infância juventude, internação, juventude, adolescente

**Títulos mais representativos:**

- Justiça do Tocantins realiza agendas para a qualificação do Sistema Socioeducativo
- Tribunal pernambucano promove o mês das inspeções em programas socioeducativos
- TJPE realiza inspeções em 100% dos programas de atendimento socioeducativo do estado
- 1.ª Vara Criminal da Infância e Juventude de Maceió promove o 3.º ciclo de audiências concentradas
- Tribunal do Amapá finaliza inspeções no Núcleo de Medida Socioeducativa de Internação Feminina

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 9 — 103 documentos

**Top-15 termos c-TF-IDF:** encontro, evento, programação, cooperação judiciária, cooperação, youtube, programação completa, contará, autoria, pesquisas, reunião preparatória, preparatória, abertura, canal, acesse programação

**Títulos mais representativos:**

- Seminário do CNJ destaca boas práticas na gestão processual do Judiciário
- Estão abertas as inscrições para a II Jornada de Boas Práticas em Tutelas Coletivas
- Último dia para as inscrições do 18.º Encontro Nacional do Poder Judiciário
- 31ª edição do Disseminando Boas Práticas do Poder Judiciário acontece na terça (23)
- Justiça mais próxima, transparente, inclusiva e acessível será debatida por profissionais de comunicação do Judiciário

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 10 — 115 documentos

**Top-15 termos c-TF-IDF:** auditoria, auditoria interna, transparência, interna, ranking, ranking transparência, governança, riscos, gestão, metas, pesquisa, integridade, pontuação, prêmio qualidade, jud

**Títulos mais representativos:**

- Pesquisa atualizará dados sobre percepção e avaliação do Judiciário
- Consulta pública envolve a sociedade na elaboração de Metas Nacionais do Judiciário para 2025
- Está no ar o regulamento do Ranking da Transparência do Judiciário 2026
- CNJ reabre edital para realização de pesquisa sobre litigância predatória
- Pesquisa sobre avaliação do Poder Judiciário pela sociedade será apresentada nesta quinta (18)

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 11 — 96 documentos

**Top-15 termos c-TF-IDF:** precatórios, pagamento, gestão precatórios, sessão, teto, normativo, ato normativo, verbas, sessão ordinária, rabaneda, ato, ordinária, regras, fórum precatórios, indenizatórias

**Títulos mais representativos:**

- Plenário do CNJ analisa na próxima terça (26) resolução que cria contracheque único para magistrados
- CNJ realiza 16ª Sessão Ordinária de 2025 nesta terça (25/11)
- Grupo de trabalho do CNJ avança para definir diretrizes relacionadas à nova norma dos precatórios
- Plenário altera prazo em norma voltada à ocupação de comarcas de difícil provimento
- CNJ e OAB debatem medidas para acelerar e padronizar pagamento de precatórios

**Correspondência com taxonomia antiga (6 meses):** Precatórios / corregedoria (âncora 'precatórios')


### Tópico 12 — 73 documentos

**Top-15 termos c-TF-IDF:** fundiária, regularização fundiária, regularização, solo seguro, solo, títulos, seguro, imóveis, propriedade, fundiária urbana, prêmio solo, urbana, famílias, títulos propriedade, reurb

**Títulos mais representativos:**

- Mais 60 títulos de imóvel são entregues a famílias de Fortaleza durante a Semana Solo Seguro
- Tribunal de Justiça do Rio já concedeu mais de mil títulos do Programa “Solo Seguro”
- Solo Seguro: inscrições para a 2.ª edição do prêmio seguem abertas até 31 de maio
- Projeto Terra: regularização fundiária avança em municípios gaúchos do Vale do Taquari
- Ação de Regularização Fundiária entrega novos títulos à população de baixa renda no ES

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 13 — 62 documentos

**Top-15 termos c-TF-IDF:** deficiência, pessoas deficiência, acessibilidade, acessibilidade inclusão, pessoa deficiência, inclusão, deficiência âmbito, direitos pessoas, barreiras, autista, tea, âmbito judicial, pessoas, pcds, pessoa

**Títulos mais representativos:**

- Justiça do Piauí lança cartilha de atendimento a PCDs e reforça compromisso com inclusão
- Judiciário busca a eliminação de barreiras para a inclusão de pessoas com deficiência
- Em cinco anos, resolução amplia acessibilidade para pessoas com deficiência na Justiça
- Lei Brasileira de Inclusão completa 10 anos e Justiça capixaba realiza ações de conscientização
- Diagnóstico aponta desafios da acessibilidade no Judiciário, mas destaca avanços na inclusão

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 14 — 128 documentos

**Top-15 termos c-TF-IDF:** pena, pena justa, penais, justa, penal, prisional, alternativas, sistema prisional, prisões, execução, drogas, plano pena, seeu, dmf, alternativas penais

**Títulos mais representativos:**

- Justiça catarinense se prepara para mutirão processual penal
- Início do Pena Justa para retomada de controle das prisões marcou ações do CNJ em 2025
- CNJ dá início às preparações para o Mutirão Processual Penal de 2024
- Central integrada instalada na Paraíba lança novo olhar sobre penas alternativas à prisão
- Novo Cniep se ajusta a necessidades da magistratura para qualificar inspeções

**Correspondência com taxonomia antiga (6 meses):** Sistema prisional / Pena Justa (âncora 'prisional')


### Tópico 15 — 105 documentos

**Top-15 termos c-TF-IDF:** adoção, crianças, crianças adolescentes, sna, pai, pretendentes, busca ativa, criança, adolescentes, infância, paternidade, família, acolhimento, infância juventude, juventude

**Títulos mais representativos:**

- Justiça baiana realiza 2.º mutirão de reconhecimento de paternidade
- Encontro discute avanços e desafios do Sistema Nacional de Adoção
- Coordenadoria da Infância de Alagoas debate estratégias de acolhimento com órgãos do estado
- Justiça reforça importância da adoção legal e amplia ações de proteção à infância no Amazonas
- Justiça de Goiás lança Programa Pai Presente Volante na Grande Goiânia

**Correspondência com taxonomia antiga (6 meses):** Infância e juventude (âncora 'crianças')


### Tópico 16 — 84 documentos

**Top-15 termos c-TF-IDF:** inovação, laboratórios, festlabs, laboratórios inovação, inovadoras, prêmio inovação, laboratório, ideias, rede inovação, laboratório inovação, prêmio, soluções, projetos, conecta, inovadora

**Títulos mais representativos:**

- Workshop em Maceió discute tecnologia e inovação com presidentes de TJs
- Caravana Conecta reúne soluções inovadoras do Centro-Oeste em Cuiabá
- Prêmio vai reconhecer soluções inovadoras para desafios da Justiça
- Tribunais do Sudeste apresentam soluções inovadoras para a transformação digital da Justiça
- I Prêmio Inovação do Poder Judiciário recebe 285 inscrições

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 17 — 52 documentos

**Top-15 termos c-TF-IDF:** curso, cursos, java, bnmp, ceajud, ciência dados, avançado, autoinstrucional, capacitações, ciência, capacitação, avançados, python, superior, carga horária

**Títulos mais representativos:**

- Webinário apresenta novos cursos de ciência de dados do Justiça 4.0
- CNJ lança capacitação sobre o Domicílio Judicial Eletrônico para pessoa física
- Justiça 4.0 realiza webinário para apresentar novos cursos avançados de ciência de dados
- CNJ lança curso inédito para ferramenta de mineração de processos judiciais
- CNJ lança curso sobre ferramenta de IA generativa para servidores do Judiciário

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 18 — 85 documentos

**Top-15 termos c-TF-IDF:** meta, distribuídos, metas, metas nacionais, processos, improbidade, julgar, improbidade administrativa, processos distribuídos, julgamento, nacionais, júri, stj, congestionamento, taxa

**Títulos mais representativos:**

- CNJ realiza inspeção no TJMT para avaliar eficiência e transparência do Judiciário
- Meta Nacional da Justiça prioriza em 2024 cerca de 32 milhões de processos mais antigos
- Justiça 4.0: tribunal paulista instala Núcleo para agilizar tramitação de processos no 2º grau
- Evento sobre ações coletivas propõe nova lógica da Justiça para reduzir litigância
- Pesquisa inédita analisa litigância abusiva no Judiciário e propõe medidas de enfrentamento

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 19 — 58 documentos

**Top-15 termos c-TF-IDF:** fonajus, saúde, fonajus itinerante, judicialização, judicialização saúde, suplementar, saúde pública, comitê saúde, assistência saúde, redenção, fórum saúde, natjus, área saúde, itinerante, saúde fonajus

**Títulos mais representativos:**

- Enfam e CNJ promovem seminário sobre desafios e perspectivas da judicialização da saúde no Brasil
- Fonajus Itinerante no RJ discute cooperação para atender demandas de saúde
- Fonajus Itinerante chega a Minas Gerais no dia 4 de junho
- Fonajus Itinerante no Amapá: ações fortalecem diálogo entre Judiciário e Executivo para melhoria da saúde
- Fonajus Itinerante será realizado em Santa Catarina a partir de 19 de março

**Correspondência com taxonomia antiga (6 meses):** Justiça itinerante / cidadania (âncora 'itinerante'); Saúde / judicialização / SUS (âncora 'saúde')


### Tópico 20 — 56 documentos

**Top-15 termos c-TF-IDF:** desembargador, foro, comarca, restaurativa, escolar, sc, 2024 regional, josé campos, raízes kalungas, catarina, 11 2024, floriano, cavalcante, torcedor, inquéritos

**Títulos mais representativos:**

- Tribunal goiano apresenta balanço do projeto Raízes Kalungas em audiência pública
- Tribunal do Amapá alinha com Ministério Público informações sobre uso do PJe
- Tribunal do Piauí instala nova Central de Inquéritos em Floriano
- Justiça do Pará faz a eliminação sustentável de 7.021 processos físicos
- Judiciário do Tocantins avalia audiências concentradas no sistema socioeducativo

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 21 — 76 documentos

**Top-15 termos c-TF-IDF:** pena justa, justa, pena, plano, prisional, sistema prisional, plano pena, penais, políticas penais, 347, inconstitucional, coisas inconstitucional, gmf, penal, coisas

**Títulos mais representativos:**

- Justiça pernambucana promove reunião para construir o Plano Pena Justa no estado
- Justiça de PE conclui oficinas do Pena Justa que buscam soluções para o sistema prisional
- Justiça do Ceará tem primeira reunião para dar andamento ao Plano Pena Justa
- Pena Justa: TRT da 7.ª Região e instituições parceiras debatem qualificação para egressos
- Plano Pena Justa apresenta alto índice de cumprimento no primeiro ano

**Correspondência com taxonomia antiga (6 meses):** Sistema prisional / Pena Justa (âncora 'prisional')


### Tópico 22 — 73 documentos

**Top-15 termos c-TF-IDF:** linguagem, linguagem simples, simples, selo linguagem, pacto linguagem, selo, ementas, pacto, compreensível, uso linguagem, comunicação, clara, ementa, direta, acessível

**Títulos mais representativos:**

- Solenidade marca entrega do Selo Linguagem Simples a 47 órgãos da Justiça
- Linguagem simples: tribunal do Trabalho baiano adota medidas para padronizar ementas
- Turma do Tribunal do Trabalho paranaense implanta projeto-piloto de linguagem simples
- Estão abertas as inscrições para concorrer ao Selo Linguagem Simples
- Linguagem simples: Justiça do Trabalho gaúcha lança glossário com expressões jurídicas

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 23 — 47 documentos

**Top-15 termos c-TF-IDF:** enac, exame, exame cartórios, prova, cartórios, certame, cartórios enac, concursos, fgv, habilitação, capitais, candidatos, serviços notariais, notariais, inscritos

**Títulos mais representativos:**

- Corregedoria Nacional acompanhará realização do 2º Enac neste domingo (28/9)
- 2º Enac: FGV divulga gabarito definitivo e resultado preliminar
- Nota da Corregedoria Nacional de Justiça
- Inscrições para o 3º Exame Nacional dos Cartórios começam no dia 19/2
- CNJ homologa resultado definitivo do 2º Exame Nacional dos Cartórios

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 24 — 73 documentos

**Top-15 termos c-TF-IDF:** sustentabilidade, climática, ambientais, ambiental, cop30, climáticas, clima, mudanças climáticas, conferência, ambiente, feliciano, juízo verde, sustentável, crimes ambientais, responsabilidade social

**Títulos mais representativos:**

- Conferência internacional debate responsabilidade global sobre sustentabilidade
- Pesquisas sobre desafios climáticos e justiça socioambiental são destaque em seminário do CNJ
- Ações para ampliar sustentabilidade no Judiciário contarão com rede de apoio
- Pacto pela Sustentabilidade: tribunais terão 12 meses para desenvolverem práticas
- Pacto envolve tribunais no compromisso do Judiciário com a sustentabilidade

**Correspondência com taxonomia antiga (6 meses):** Sustentabilidade ambiental (âncora 'sustentabilidade')


### Tópico 25 — 62 documentos

**Top-15 termos c-TF-IDF:** execuções fiscais, execuções, fiscais, execução fiscal, tributária, extinção, cobrança, fiscal, dívida, tributário, protesto, litigiosidade, dívida ativa, 547, resolução 547

**Títulos mais representativos:**

- Execução fiscal: acordo entre CNJ e TJRN deve extinguir mais de 35 mil processos
- Presidente do CNJ recebe procuradora-geral da Fazenda Nacional para discutir ações conjuntas
- CNJ firma acordo com tribunal e governo da Bahia para extinguir execuções fiscais no estado
- Com política de eficiência, 12 milhões de execuções fiscais foram extintas
- Extinção de processos de execução fiscal sem andamento é monitorada pelo CNJ

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 26 — 78 documentos

**Top-15 termos c-TF-IDF:** itinerante, atendimentos, inss, itinerância, marajó, benefício, serviços, portel, jef, carteira, breves, população, mil atendimentos, cidadania, casamento

**Títulos mais representativos:**

- Mais de 1,4 mil processos são movimentados em Juizado Itinerante da Justiça Federal do Tocantins
- Juizado Itinerante em Porto Murtinho (MS) alcança 71% de acordo em audiências realizadas
- Juizado itinerante alcança 2,4 mil atendimentos no norte de Minas
- De casamento coletivo à escuta em área quilombola, tem de tudo no Justiça Itinerante
- Política judiciária para pessoas em situação de rua celebra quatro anos de avanços

**Correspondência com taxonomia antiga (6 meses):** Justiça itinerante / cidadania (âncora 'itinerante')


### Tópico 27 — 76 documentos

**Top-15 termos c-TF-IDF:** disciplinar, pad, afastamento, reclamação disciplinar, reclamação, 0000, 00 0000, 00, indícios, cautelar, administrativo disciplinar, corregedor, magistrado, processo administrativo, campbell

**Títulos mais representativos:**

- Juiz do Mato Grosso do Sul responderá a PAD por suspeita de venda de decisões
- Juíza que nomeou peritos sem formação contábil será investigada pelo CNJ
- CNJ abre PAD contra magistrada aposentada da Justiça baiana
- CNJ mantém afastamento e abre PADs contra desembargadores do Mato Grosso do Sul
- PAD investigará supostas vantagens indevidas recebidas por juiz de Mato Grosso

**Correspondência com taxonomia antiga (6 meses):** Processos disciplinares / sessões (âncora 'disciplinar')


### Tópico 28 — 99 documentos

**Top-15 termos c-TF-IDF:** rua, situação rua, popruajud, pessoas situação, situação, população situação, atenção pessoas, população, mutirão, pop, comitê popruajud, pop rua, população rua, comitê, mutirão popruajud

**Títulos mais representativos:**

- Corregedoria Nacional de Justiça marca presença no quarto dia do PopRuaJud Sampa + Registre-se
- Justiça Federal de Mato Grosso participa, em Rondonópolis, de atendimento à população em situação de rua
- Mutirão atende a pessoas em situação de rua nesta terça (6/5), em Maceió (AL)
- Justiça do Trabalho do Ceará faz parcerias e planeja ações em favor da população de rua
- Judiciário de Alagoas se une em prol da população em situação de rua

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 29 — 70 documentos

**Top-15 termos c-TF-IDF:** itinerante, comunidade, kalungas, atendimentos, casamento, cidadania, comunidades, cavalcante, raízes, raízes kalungas, vara itinerante, tjgo, pid, vila, serviços

**Títulos mais representativos:**

- Justiça Itinerante realiza mais de 100 atendimentos na zona sul de Porto Alegre
- Justiça Itinerante realiza 51 atendimentos na primeira ação de 2025 em Porto Alegre (RS)
- Tribunal do MT inicia atendimentos em Bom Jesus do Araguaia e leva cidadania a regiões isoladas
- Justiça na Praça leva ações de cidadania ao município potiguar de Portalegre
- Justiça Itinerante: programa leva serviços e fortalece a cidadania em Niquelândia (GO)

**Correspondência com taxonomia antiga (6 meses):** Justiça itinerante / cidadania (âncora 'itinerante')


### Tópico 30 — 66 documentos

**Top-15 termos c-TF-IDF:** pje, conecta, pdpj, soluções, soluções tecnológicas, pdpj br, tecnológicas, transformação digital, tecnologia, digital, banco sentenças, militares, janus, programa, bastião

**Títulos mais representativos:**

- Com apoio do CNJ, Tribunal de Justiça do Paraná adere a novo sistema processual eletrônico
- Caravana Conecta reúne tribunais do Nordeste em São Luís (MA) para compartilhar boas práticas em inovação
- Portal CNJ de Boas Práticas recebe dezesseis novos projetos
- CNJ institui diretrizes do Programa Conecta para nacionalização de soluções tecnológicas dos tribunais
- Tecnologia da Informação no Judiciário é tema de série especial no Link CNJ

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 31 — 49 documentos

**Top-15 termos c-TF-IDF:** polícia judicial, segurança institucional, curso, formação, polícia, policiais judiciais, capacitação, dnpj, segurança, inteligência, policiais, cniep, inspeções, identificação civil, seeu

**Títulos mais representativos:**

- CNJ capacita mais de 4,6 mil pessoas no 6.º ciclo de formações sobre o Seeu
- DNPJ conclui 2024 com avanços na formação e na doutrina da polícia judicial
- CNJ capacita quase 6 mil pessoas em 5.º Ciclo de formações sobre SEEU
- CNJ capacita mais de mil pessoas para aplicarem normas no sistema penal e socioeducativo
- CNJ apoia formação de juízes em início de carreira sobre tema penal e socioeducativo

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 32 — 52 documentos

**Top-15 termos c-TF-IDF:** leitura, mentes, literárias, mentes literárias, remição, livros, prisional, sistema prisional, livro, escrita, privadas liberdade, liberdade, remição pena, pessoas privadas, prisionais

**Títulos mais representativos:**

- CNJ e tribunal alagoano lançam Projeto Mentes Literárias em presídio de Maceió
- Mentes Literárias: juízes e juízas debatem acesso à cultura no sistema prisional
- Tribunal de Mato Grosso e CNJ lançam projeto de remição pela leitura na Penitenciária Central
- Reeducandas do Maranhão participam do projeto Mentes Literárias
- Ação inédita na Bahia inclui adolescentes no projeto Mentes Literárias

**Correspondência com taxonomia antiga (6 meses):** Sistema prisional / Pena Justa (âncora 'prisional')


### Tópico 33 — 95 documentos

**Top-15 termos c-TF-IDF:** violência, doméstica, violência doméstica, mulher, doméstica familiar, mulheres, enfrentamento violência, contra, fonar, violência contra, contra mulheres, familiar, contra mulher, maria penha, penha

**Títulos mais representativos:**

- CNJ amplia proteção a mulheres do Judiciário com protocolo obrigatório contra violência doméstica
- Violência contra mulheres preocupa sociedade, e o Judiciário atua para enfrentar o problema, afirma Fachin
- Presidente do CNJ acompanha instalação de varas de violência doméstica e familiar contra a mulher em SP
- CNJ visita projeto de referência na responsabilização de autores de violência contra mulheres em Rondônia
- Webinário do CNJ reforça integração entre Judiciário e Ligue 180 para proteger mulheres

**Correspondência com taxonomia antiga (6 meses):** Violência doméstica / mulheres (âncora 'violência')


### Tópico 34 — 38 documentos

**Top-15 termos c-TF-IDF:** desaparecimento, sales pimenta, vítimas, sales, pimenta, desaparecimento forçado, óbito, direitos humanos, humanos, familiares, pessoas desaparecidas, desaparecidas, forçado, ceavs, interamericana

**Títulos mais representativos:**

- CNJ debate no Rio medidas para aprimorar atendimento a vítimas de violência de Estado
- CNJ convida rede de vítimas da violência estatal para atuar em Observatório de Direitos Humanos
- CNJ realiza debate sobre desaparecimento forçado e justiça de transição
- Justiça de Transição e desaparecimento forçado são temas de evento internacional do CNJ
- Observatório inicia 2026 acompanhando casos relacionados a conflitos fundiários, tragédias e crimes dolosos

**Correspondência com taxonomia antiga (6 meses):** Direitos humanos / Corte IDH (âncora 'humanos')


### Tópico 35 — 61 documentos

**Top-15 termos c-TF-IDF:** escravo, trabalho escravo, tráfico pessoas, tráfico, trabalho infantil, infantil, combate trabalho, trabalho, escravo tráfico, trabalhadores, escravidão, fontet, análogas, enfrentamento trabalho, condições análogas

**Títulos mais representativos:**

- 2.º Encontro do Fontet define prioridades no combate ao trabalho escravo e ao tráfico de pessoas
- Justiça do Trabalho da 8.ª Região inicia curso de capacitação para refugiados e migrantes
- Trabalhadores, entidades e acadêmicos contribuirão para política judiciária pelo trabalho decente
- Justiça do Trabalho do Maranhão encerra ação de combate ao tráfico de pessoas e trabalho escravo
- Justiça do Trabalho da 8.ª Região debate o combate ao trabalho escravo contemporâneo

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 36 — 44 documentos

**Top-15 termos c-TF-IDF:** pauta verde, ambiental, semana pauta, ambientais, verde, pauta, processos ambientais, ambiente, fórum ambiental, lixões, semana, 1ª região, questões ambientais, sustentabilidade, ações ambientais

**Títulos mais representativos:**

- Justiça baiana participa da II Semana da Pauta Verde com foco na celeridade dos processos ambientais
- Semana da Pauta Verde: Justiça potiguar realiza mutirão de conciliações em processos ambientais
- Judiciário Sustentável apresenta novo balanço e marca entrega de Prêmio Juízo Verde
- Semana da Pauta Verde: tribunais realizarão ações entre os dias 18 e 22 de agosto
- Poder Judiciário promove o I Encontro Nacional do Fórum Ambiental em São Luís

**Correspondência com taxonomia antiga (6 meses):** Sustentabilidade ambiental (âncora 'sustentabilidade')


### Tópico 37 — 53 documentos

**Top-15 termos c-TF-IDF:** eleitoral, eleições, eleitores, tse, votação, eleitor, eleitorais, eleitoras, eleitoras eleitores, urna, processo eleitoral, eleitorado, voto, votar, urnas

**Títulos mais representativos:**

- TSE reafirma compromisso com a inclusão eleitoral
- Eleições 2024: Justiça Eleitoral fortalece presença de indígenas e quilombolas no Tocantins
- TSE celebra 30 anos da urna eletrônica com foco na segurança do voto e no combate à desinformação
- Justiça Eleitoral do Acre intensifica atendimentos a povos indígenas e em áreas de difícil acesso
- Projetos de TREs fortalecem a democracia e aproximam população da Justiça Eleitoral

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 38 — 46 documentos

**Top-15 termos c-TF-IDF:** direitos humanos, corte idh, idh, humanos, corte, interamericana, interamericano, sistema interamericano, interamericana direitos, corte interamericana, umf, interamericano direitos, direitos, internacionais, humanos corte

**Títulos mais representativos:**

- Novos protocolos do CNJ ampliam a cultura de direitos humanos no Judiciário
- CNJ reúne tribunais para fortalecer proteção de direitos humanos
- CNJ fortalece integração entre Justiça brasileira e sistema interamericano de direitos humanos
- CNJ lança 3ª fase do Pacto Nacional do Judiciário pelos Direitos Humanos
- Magistrados selecionados pelo CNJ chegam à Corte IDH para intercâmbio inédito

**Correspondência com taxonomia antiga (6 meses):** Direitos humanos / Corte IDH (âncora 'humanos')


### Tópico 39 — 56 documentos

**Top-15 termos c-TF-IDF:** fundiárias, soluções fundiárias, comissão soluções, comissão, fundiários, conflitos fundiários, comissões, soluções, alcântara, terras, conflito, conflitos, terra, visitas técnicas, comissões soluções

**Títulos mais representativos:**

- Comissão de soluções fundiárias fará visita preparatória para mediação de conflitos de terra no sul da Bahia
- CNJ recebe povo Pataxó para debater questões sobre o território ancestral
- Judiciário realiza reuniões e escuta indígenas e proprietários de terra no sul da Bahia
- Comissão Nacional de Soluções Fundiárias acompanha negociações no Norte e Noroeste de MG
- Justiça de Mato Grosso reafirma compromisso com a solução de conflitos agrários

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 40 — 98 documentos

**Top-15 termos c-TF-IDF:** paz casa, mulher, violência, violência doméstica, semana paz, doméstica, paz, contra mulher, casa, doméstica familiar, maria penha, penha, contra, mulheres, maria

**Títulos mais representativos:**

- Celeridade processual e mobilização da sociedade marcam a 32ª Semana Justiça pela Paz em Casa
- Justiça pela Paz em Casa: 27.ª edição da ação começa nesta segunda (19/8)
- Justiça do Ceará agenda 353 audiências em ação voltada ao combate da violência contra a mulher
- Início do mutirão de audiências marca a abertura da 28ª Semana Justiça pela Paz em Casa no Acre
- 31ª Semana Justiça pela Paz em Casa acelera julgamentos de casos de violência doméstica

**Correspondência com taxonomia antiga (6 meses):** Violência doméstica / mulheres (âncora 'violência')


### Tópico 41 — 47 documentos

**Top-15 termos c-TF-IDF:** saúde, prêmio saúde, suplementar, saúde pública, judicialização, judicialização saúde, doação, natjus, pública suplementar, fonajus, aedo, notas, doador, demandas saúde, cidadania promoção

**Títulos mais representativos:**

- CNJ premia melhores práticas judiciárias em saúde
- Soluções inovadoras em saúde são premiadas durante Congresso do Fonajus
- Tribunais participam da 1.ª Semana Nacional da Saúde com ações integradas
- Ações focadas na melhoria da gestão processual são reconhecidas pelo Prêmio Justiça e Saúde
- Palestra sobre importância do NatJus encerra a Semana Nacional de Saúde na Paraíba

**Correspondência com taxonomia antiga (6 meses):** Saúde / judicialização / SUS (âncora 'saúde')


### Tópico 42 — 41 documentos

**Top-15 termos c-TF-IDF:** provimento, imóveis, recuperação judicial, recuperação, onr, registro, cartórios, notariais, indisponibilidade, operador, registro imóveis, notarial, registros, atos notariais, registro civil

**Títulos mais representativos:**

- Com novo provimento, cartórios entram em nova fase de modernização tecnológica
- Novo sistema facilita cumprimento de ordens de indisponibilidade de imóveis
- CNJ define diretrizes para modernização e mais segurança jurídica no registro de imóveis
- Tribunal do Rio Grande do Norte desenvolve novo sistema para pagamento de RPV’s
- Tribunal cearense registra emissão de mais de 650 mil certidões judiciais em um ano

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 43 — 61 documentos

**Top-15 termos c-TF-IDF:** depoimento, crianças, crianças adolescentes, depoimento especial, infância, adolescentes, criança, criança adolescente, adolescente, protegida, sexual, abuso, infância juventude, juventude, infância protegida

**Títulos mais representativos:**

- CNJ inicia mobilização nacional para fortalecer proteção de crianças e adolescentes
- CNJ lança Mês da Infância Protegida com foco no enfrentamento à violência
- Mês da Infância Protegida: Como denunciar violência contra crianças e adolescentes
- Mês da Infância Protegida: políticas judiciárias protegem e asseguram direitos fundamentais
- Mês da Infância Protegida: mutirão antecipa depoimentos especiais de crianças e adolescentes

**Correspondência com taxonomia antiga (6 meses):** Infância e juventude (âncora 'crianças')


### Tópico 44 — 37 documentos

**Top-15 termos c-TF-IDF:** programa caminhos, jovens, caminhos, acolhimento, acolhidos, santa catarina, aprendizagem, pnc, catarina, adolescentes, empregabilidade, jovens acolhidos, profissional, santa, correios

**Títulos mais representativos:**

- Justiça fluminense lança programa para capacitar jovens em situação de vulnerabilidade
- Encontro deve fortalecer capacitação profissional e pessoal de jovens acolhidos
- Em Santa Catarina, Novos Caminhos projeta ampliar oportunidades para jovens acolhidos em 2025
- Corregedoria de Justiça capixaba avança nas ações de programa para infância e juventude
- Novos Caminhos completa dois anos com oportunidades para jovens em acolhimento institucional em todo o país

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 45 — 48 documentos

**Top-15 termos c-TF-IDF:** relator, disciplinar, magistrado, 0000, disponibilidade, 00 0000, censura, 00, decisão, revisão disciplinar, sessão, sessão ordinária, voto, administrativo, processo administrativo

**Títulos mais representativos:**

- Desembargador mineiro acusado de conceder vantagem indevida é punido com pena de disponibilidade
- CNJ aplica pena de remoção a juiz que depreciou magistrados e membros do MPF
- CNJ pune com disponibilidade juiz federal que atua no Amapá
- Juiz que negligenciava atuação de assessores recebe pena de disponibilidade por 90 dias
- CNJ impõe pena de disponibilidade a juiz por imprudência em plantão judiciário

**Correspondência com taxonomia antiga (6 meses):** Processos disciplinares / sessões (âncora 'disciplinar')


### Tópico 46 — 26 documentos

**Top-15 termos c-TF-IDF:** lgbtqia, pessoas lgbtqia, rogéria, população lgbtqia, formulário rogéria, lgbtqiapn, trans, transexuais, fórum promoção, promoção direitos, direitos pessoas, travestis, diversidade, formulário, identidade gênero

**Títulos mais representativos:**

- Especialistas debatem aspectos jurídicos do registro civil de pessoas LGBTQIA+
- Evento do CNJ pauta desafios e oportunidades para a inclusão efetiva de pessoas LGBTQIA+
- Cartilha aborda direitos da comunidade LGBTQIAPN+
- Promoção e proteção dos direitos LGBTQIA+ são tema de encontro no CNJ nos dias 25 e 26/6
- Justiça do Trabalho reforça compromisso com direitos da população LGBTQIA+

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 47 — 54 documentos

**Top-15 termos c-TF-IDF:** emissões, energia, carbono, gases, estufa, efeito estufa, gases efeito, efeito, elétrica, energia elétrica, sustentabilidade, descarbonização, consumo, emissões gases, compensação

**Títulos mais representativos:**

- Tribunal do Piauí apresenta versão inicial do Plano de Descarbonização
- Encontro Nacional do Judiciário de 2024 recebe selo por zerar emissão de carbono
- Práticas sustentáveis já utilizadas pelos tribunais serão ampliadas com pacto
- Tribunal gera metade da própria energia a partir de fontes limpas
- Tribunal de Pernambuco reduz energia elétrica e gasto público com mudanças de gestão

**Correspondência com taxonomia antiga (6 meses):** Sustentabilidade ambiental (âncora 'sustentabilidade')


### Tópico 48 — 45 documentos

**Top-15 termos c-TF-IDF:** fachin, democracia, constituição, edson fachin, edson, constitucional, defesa, democrático, direitos humanos, stf, humanos, 1988, constituinte, interamericano, crime organizado

**Títulos mais representativos:**

- Encontro Nacional: Fachin diz que Judiciário deve manter integridade e credibilidade social
- Independência judicial é condição para democracia, afirma Fachin em evento na USP
- Em primeira reunião à frente do ODH, ministro Fachin reforça compromisso do Observatório com a democracia
- Corte Interamericana inicia atividades no Brasil com sessão de abertura no STF
- Na Costa Rica, presidente do CNJ explica experiência brasileira na superação de ataques às instituições

**Correspondência com taxonomia antiga (6 meses):** Direitos humanos / Corte IDH (âncora 'humanos')


### Tópico 49 — 32 documentos

**Top-15 termos c-TF-IDF:** sessão, sessão ordinária, ordinária, sessões, disciplinares, controle administrativo, plenário, processos administrativos, ordinária 2025, secretaria processual, 5180 mail, mail secretaria, 2326 5180, secretaria jus, 5180

**Títulos mais representativos:**

- CNJ realiza 14ª Sessão Ordinária na terça-feira (28/10)
- Nove itens compõem a pauta da 3.ª Sessão Extraordinária de 2025 do CNJ nesta terça-feira (10/6)
- 11.ª Sessão Ordinária de 2025 do CNJ traz pauta com 14 itens
- Plenário do CNJ aprecia 13 itens em sessão extraordinária na terça-feira (27/5)
- CNJ realiza 13ª Sessão Ordinária de 2025 na terça-feira (14/10)

**Correspondência com taxonomia antiga (6 meses):** Processos disciplinares / sessões (âncora 'disciplinar')


### Tópico 50 — 47 documentos

**Top-15 termos c-TF-IDF:** barroso, posse, conselheiros, magistratura, presidentes, conselheiro, luís roberto, roberto barroso, enam, supremo, stf, supremo stf, stf luís, fachin, roberto

**Títulos mais representativos:**

- Presidente do CNJ participa do XIX Consepre em Fortaleza
- Em São Luís, Barroso destaca ações do CNJ para tornar a Justiça acessível e inclusiva
- Panorama das políticas judiciárias demonstra papel agregador do CNJ para a Justiça
- Ministro Barroso destaca realizações no seu primeiro ano de gestão do CNJ
- Presidente do CNJ debate avanços e desafios com a magistratura

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 51 — 54 documentos

**Top-15 termos c-TF-IDF:** memória, patrimônio cultural, patrimônio, preservação, história, gestão documental, documental, cultural, prêmio memória, escravidão, arquivos, documental memória, acervo, valongo, categoria patrimônio

**Títulos mais representativos:**

- Em 2026, Prêmio CNJ Memória do Judiciário terá tema especial sobre escravidão e liberdade
- Congresso debate preservação de arquivos e acesso à informação no Judiciário
- Memória do Poder Judiciário: exposição “150 anos” resgata história de sete tribunais brasileiros
- Memória do Judiciário é tema do programa Link CNJ desta semana
- 5.º Encontro de Memória do Poder Judiciário debate cultura, diversidade e preservação histórica

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 52 — 64 documentos

**Top-15 termos c-TF-IDF:** indígenas, indígena, registro civil, povos, registro, povos indígenas, registre, aldeia, nascimento, civil, sub registro, sub, etnia, documentação, funai

**Títulos mais representativos:**

- Identificação civil: Justiça de Roraima amplia atendimento à comunidade Waimiri Atroari
- Registre-se Brasil Parente leva cidadania à população indígena brasileira
- Tribunal de Roraima lança primeira Ouvidoria Eleitoral dos Povos Indígenas do Brasil
- Inclusão do nome de etnia em registro civil leva cidadania a povos indígenas na Amazônia
- Registre-se: Justiça Federal realizou atendimentos a 222 indígenas em Passo Fundo

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 53 — 30 documentos

**Top-15 termos c-TF-IDF:** libras, intérprete, língua, deficiência auditiva, acessibilidade, auditiva, sinais, balcão, visual, deficiência, surdas, surda, língua sinais, surdos, pessoas surdas

**Títulos mais representativos:**

- Justiça do Trabalho de Campinas amplia serviço remoto de Libras e legendas para audiências
- Atuação de tradutores e intérpretes de Libras aproxima a Justiça cearense da comunidade surda
- Justiça do Trabalho de Sergipe realiza 1ª audiência com intérprete de libras
- Justiça eleitoral do Paraná realiza ações para a inclusão de eleitores com deficiência
- Projeto Manhãs com Libras chega à quarta edição

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 54 — 31 documentos

**Top-15 termos c-TF-IDF:** lgbtqiapn, trans, casais, assédio, casamento, discriminação, assédio moral, homoafetivos, sexual discriminação, sexual, moral, enfrentamento assédio, população lgbtqiapn, diversidade, lgbtqia

**Títulos mais representativos:**

- CNJ marca presença em casamento comunitário LGBTQIAPN+ em Goiás
- Evento da Justiça do Trabalho paulista defende a promoção de direitos das pessoas LGBTQIA+
- Justiça do Amazonas coordena ação para facilitar o reconhecimento de identidade a pessoas trans
- Tribunal de Campinas discute inclusão LGBTQIA+ na Justiça do Trabalho
- Projeto da Justiça potiguar adequa nome e gênero de pessoas trans, travestis e não binárias

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 55 — 25 documentos

**Top-15 termos c-TF-IDF:** idosa, pessoa idosa, idosas, pessoas idosas, idoso, idosos, pessoa, envelhecimento, curatela, selo amigo, população idosa, selo, amigo, resolução 520, 520

**Títulos mais representativos:**

- Tribunal baiano promove semana de mobilização para maior celeridade em processos com idosos
- Conselheiro destaca direitos da pessoa idosa em simpósio no STJ
- Selo Tribunal Amigo da Pessoa Idosa: inscrições se encerram no domingo (31/8)
- Judiciário baiano analisa mais de 169 mil processos envolvendo pessoas idosas
- Corregedoria recomenda esforço concentrado para acelerar processos de idosos no Ceará

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 56 — 61 documentos

**Top-15 termos c-TF-IDF:** jus br, jus, br, sngb, bnp, portal, consulta, superior, saref, consulta processual, unificada, bens, peticionamento, gestão bens, superior trabalho

**Títulos mais representativos:**

- Novo painel monitora a integração de tribunais brasileiros ao Portal Unificado de Serviços
- Mais de 213 mil usuários já acessam serviços do Poder Judiciário via Jus.br
- Jus.br: conheça as funcionalidades do novo portal da Justiça brasileira
- CNJ lança portal que monitora os serviços da Plataforma Digital do Poder Judiciário
- Meio milhão de pessoas já acessa serviços do Judiciário via Jus.br

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 57 — 33 documentos

**Top-15 termos c-TF-IDF:** centros inteligência, centro inteligência, caravana virtual, centros, nota técnica, inteligência, caravana, nota, virtual, caravanas, cipj, virtuais, rede centros, inteligência cipj, centro

**Títulos mais representativos:**

- Centro de Inteligência de tribunal mineiro promove caravana virtual nesta segunda (25/11)
- Tribunal do Paraná recebe Caravana Virtual da Rede de Centros de Inteligência no dia 22/10
- Justiça Federal da 2.ª Região e CNJ discutem as boas práticas dos Centros de Inteligência
- Caravana virtual aborda impactos do uso de assinatura eletrônica em processos judiciais
- Justiça Federal em Sergipe recebe Caravana Virtual dos Centros de Inteligência

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 58 — 27 documentos

**Top-15 termos c-TF-IDF:** caminhos literários, literários, leitura, cultura, letras, socioeducativo, adolescentes, unidades socioeducativas, livros, acesso cultura, literários socioeducativo, caminhos, socioeducativas, sistema socioeducativo, case

**Títulos mais representativos:**

- Adolescentes socioeducandos catarinenses participam do projeto Caminhos Literários
- Projeto do TJES leva cultura para as unidades socioeducativas do Estado
- 3º Caminhos Literários no Socioeducativo celebra o protagonismo juvenil
- CNJ leva clubes de leitura para o sistema socioeducativo
- Caminhos Literários 2025 começa com debates sobre cultura e juventude

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 59 — 43 documentos

**Top-15 termos c-TF-IDF:** resíduos, descarte, reciclagem, recicláveis, catadores, materiais, materiais recicláveis, destinação, toneladas, sustentabilidade, sustentável, documental, logística, coleta, eliminação

**Títulos mais representativos:**

- Encontro da Justiça Federal no Pará reforça compromisso com a gestão de resíduos sólidos
- Justiça Federal no Amapá instala Ecoponto para descarte de vidro
- Corregedoria-Geral da Justiça do Ceará doa quase 100 quilos de materiais recicláveis
- Justiça fluminense amplia projeto sustentável com novo Ecoponto no Fórum Central
- TJRN destina mais de 5,7 toneladas de papel para reciclagem em 2025

**Correspondência com taxonomia antiga (6 meses):** Sustentabilidade ambiental (âncora 'sustentabilidade')


### Tópico 60 — 42 documentos

**Top-15 termos c-TF-IDF:** marajó, meninas mulheres, meninas, ação meninas, mulheres marajó, mulheres, tjpa, melgaço, renata gil, gil, pid, conselheira renata, renata, violência, arquipélago

**Títulos mais representativos:**

- Sertão de Pernambuco recebe “Ação Meninas e Mulheres” do CNJ nos dias 4 e 5 agosto
- Judiciário baiano realiza mobilização em Eunápolis e Porto Seguro contra a violência de gênero
- Menor IDH do Brasil: Melgaço (PA) recebe ação da Justiça no combate à violência contra a mulher
- Justiça voltada ao enfrentamento da violência contra a mulher e à defesa da infância
- Justiça do Pará coordena planejamento da 3.ª Ação de Meninas e Mulheres do Marajó

**Correspondência com taxonomia antiga (6 meses):** Violência doméstica / mulheres (âncora 'violência')


### Tópico 61 — 31 documentos

**Top-15 termos c-TF-IDF:** sexual, assédio, assédio sexual, violência, feminicídio, mulheres, vermelho, mulher, doméstica, violência doméstica, contra, violência contra, contra mulher, sexual trabalho, vítimas

**Títulos mais representativos:**

- CNJ realizará encontros para qualificar responsabilização por violência doméstica em agosto
- Justiça do Maranhão concede mais de 13 mil medidas protetivas no primeiro semestre
- Proteção mais rápida: Justiça concede 225 mil medidas protetivas no primeiro quadrimestre do ano
- Reportagem premiada relata aumento dos casos de violência doméstica em Pernambuco
- Justiça Originária: desafios persistem para levar a Lei Maria da Penha aos territórios indígenas

**Correspondência com taxonomia antiga (6 meses):** Violência doméstica / mulheres (âncora 'violência')


### Tópico 62 — 45 documentos

**Top-15 termos c-TF-IDF:** violência, violência doméstica, doméstica, mulher, violência contra, mulheres, contra, combate violência, contra mulheres, homens, violência digital, violência gênero, contra mulher, prevenção, enfrentamento violência

**Títulos mais representativos:**

- CNJ e Vivo voltam a disparar, neste 8/3, alertas sobre a importância do combate à violência contra as mulheres
- Combate à violência contra a mulher ganha parceria do Ifood e da Faculdade de Direito de Santo André/SP
- Programa Brasil Lilás é lançado para ampliar ações de prevenção à violência de gênero
- CNJ 20 anos: Justiça garante efetividade ao combate à violência contra mulheres
- Projeto quer fortalecer o acesso à Justiça de vítimas de violência doméstica

**Correspondência com taxonomia antiga (6 meses):** Violência doméstica / mulheres (âncora 'violência')


### Tópico 63 — 35 documentos

**Top-15 termos c-TF-IDF:** ouvidoria, encontro popruajud, ouvidorias, rua, popruajud, situação rua, ouvidor, manifestações, terto, população situação, ii encontro, situação, propostas, pessoas situação, rua jud

**Títulos mais representativos:**

- Audiência pública busca ouvir sociedade sobre acesso à Justiça em locais de difícil alcance
- Evento discute práticas para fortalecer direitos das pessoas idosas no sistema de justiça
- Iniciativas do Judiciário para pessoas em situação de rua serão foco em encontro nacional
- Novo Manual Orientativo vai trazer propostas para atendimento à população em situação de rua
- Ouvidoria do Tribunal do Piauí leva serviços à população durante ação da Justiça Itinerante

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 64 — 23 documentos

**Top-15 termos c-TF-IDF:** beneficiários, rpvs, previdenciárias assistenciais, região sede, assistenciais, previdenciárias, trf região, pagamento, jurisdição, saque, valor rpvs, pix, trf, requisições, requisições pequeno

**Títulos mais representativos:**

- Justiça Federal libera pagamento de RPVs a mais de 180 mil beneficiários
- Justiça Federal libera o pagamento de RPVs a mais de 280 mil beneficiários
- Justiça Federal libera o pagamento de RPVs a mais de 199 mil beneficiários
- Justiça Federal libera o pagamento de RPVs a mais de 231 mil beneficiários
- Justiça Federal libera o pagamento de RPVs a mais de 227 mil beneficiários

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 65 — 31 documentos

**Top-15 termos c-TF-IDF:** medicamentos, saúde, fonajus, enunciados, direito saúde, natjus, 1234, sus, suplementar, saúde suplementar, jornada direito, fornecimento, fornecimento medicamentos, judicialização, fórum saúde

**Títulos mais representativos:**

- VII Jornada de Direito da Saúde aprova 30 novos enunciados
- Novos enunciados são aprovados para orientar decisões judiciais sobre saúde
- Participantes da VII Jornada de Direito da Saúde analisarão novos enunciados
- Bases de dados técnicos de saúde devem ser integradas ao e-NatJus 4.0
- Congresso do Fonajus: oficinas vão discutir desafios da judicialização em saúde

**Correspondência com taxonomia antiga (6 meses):** Saúde / judicialização / SUS (âncora 'saúde')


---

## min_topic_size = 10

- Tópicos: **94** | coerência c_v: **0.6289** | diversidade: 0.866 | outliers brutos: 44.11% (1938 docs, reatribuídos por c-TF-IDF para a contagem abaixo)

### Tópico 0 — 146 documentos

**Top-15 termos c-TF-IDF:** ia, artificial, inteligência artificial, inteligência, uso, uso ia, generativa, ferramentas, tecnologia, proteção dados, ia generativa, uso inteligência, artificial ia, ferramenta, privacidade

**Títulos mais representativos:**

- CNJ inicia coleta de informações sobre uso de inteligência artificial por tribunais
- Tribunal do Pará apresenta uso da IA na análise de documentos processuais
- Primeiro dia de audiência pública sobre IA na Justiça aborda controle e capacitação
- Corte do DF encerra o 1.º Encontro Nacional dos Tribunais Usuários do PJe sobre IA
- Lançamento de inovações de inteligência artificial para o Judiciário marcam evento no CNJ

**Correspondência com taxonomia antiga (6 meses):** IA / Conecta / Justiça 4.0 (âncora 'inteligência artificial')


### Tópico 1 — 86 documentos

**Top-15 termos c-TF-IDF:** amazonas, amazônia, am, amazônia legal, manaus, tjam, seguro amazônia, xapuri, legal, itinerante cooperativa, solo seguro, boca acre, solo, boca, fundiária

**Títulos mais representativos:**

- Justiça Itinerante: equipe conhece principais demandas de território indígena no Amazonas
- Corregedor nacional encerra Semana Solo Seguro Amazônia em solenidade no Amazonas
- Justiça do Amazonas realiza ação para cadastro de profissionais indígenas
- Justiça Itinerante no Amazonas inicia atendimentos do primeiro semestre de 2025
- Serviços ampliados e novos fluxos marcam Justiça Itinerante em Boca do Acre/AM e Xapuri/AC

**Correspondência com taxonomia antiga (6 meses):** Justiça itinerante / cidadania (âncora 'itinerante')


### Tópico 2 — 81 documentos

**Top-15 termos c-TF-IDF:** racial, racismo, equidade racial, equidade, negra, negros, raciais, negras, racismo estrutural, perspectiva racial, pessoas negras, julgamento perspectiva, prêmio equidade, estrutural, letramento racial

**Títulos mais representativos:**

- Mutirão Racial 2026 mobiliza tribunais para julgamento de processos em novembro
- Mutirão Racial e Mês Nacional do Júri são destaques da agenda do CNJ em novembro
- Julgamento de processos com temática racial é destaque no Mês da Consciência Negra
- Curso aborda aplicação do Protocolo para Julgamento com Perspectiva Racial no Judiciário
- Indicador de desempenho racial e Prêmio Equidade Racial 2026 incentivam enfrentamento ao racismo

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 3 — 99 documentos

**Top-15 termos c-TF-IDF:** precatórios, pagamento, teto, gestão precatórios, ato normativo, normativo, verbas, sessão, fonaref, indenizatórias, regras, ato, fórum precatórios, rabaneda, prazo

**Títulos mais representativos:**

- Plenário do CNJ analisa na próxima terça (26) resolução que cria contracheque único para magistrados
- Grupo de trabalho do CNJ avança para definir diretrizes relacionadas à nova norma dos precatórios
- CNJ realiza 16ª Sessão Ordinária de 2025 nesta terça (25/11)
- CNJ e OAB debatem medidas para acelerar e padronizar pagamento de precatórios
- Plenário altera prazo em norma voltada à ocupação de comarcas de difícil provimento

**Correspondência com taxonomia antiga (6 meses):** Precatórios / corregedoria (âncora 'precatórios')


### Tópico 4 — 71 documentos

**Top-15 termos c-TF-IDF:** tjgo, desembargador, kalungas, restaurativa, raízes kalungas, cavalcante, foro, regional, goiás, reinaldo, 2024 regional, frança, raízes, jornada, josé campos

**Títulos mais representativos:**

- Tribunal goiano apresenta balanço do projeto Raízes Kalungas em audiência pública
- Tribunal do Amapá alinha com Ministério Público informações sobre uso do PJe
- Tribunal do Piauí instala nova Central de Inquéritos em Floriano
- Estão abertas as inscrições para a II Jornada de Boas Práticas em Tutelas Coletivas
- Judiciário goiano realiza audiência pública sobre metas nacionais do CNJ

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 5 — 70 documentos

**Top-15 termos c-TF-IDF:** feminina, gênero, participação feminina, mulheres, incentivo participação, paridade, perspectiva gênero, paridade gênero, liderança, igualdade gênero, igualdade, cargos, protocolo, institucional feminina, participação institucional

**Títulos mais representativos:**

- Evento no CNJ debate desafios para ampliar presença de mulheres no Judiciário
- Participação institucional feminina no Judiciário avança no Brasil
- Seminário debate presença de mulheres no sistema de justiça nesta quinta (26)
- Violência contra a mulher: articulação oferece respostas mais efetivas do Judiciário, diz Fachin
- Evento debate os avanços da participação feminina no Poder Judiciário e os desafios a serem enfrentados

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 6 — 133 documentos

**Top-15 termos c-TF-IDF:** pena, penais, pena justa, penal, prisional, justa, alternativas, seeu, sistema prisional, prisões, alternativas penais, execução, custódia, dmf, prisão

**Títulos mais representativos:**

- Justiça catarinense se prepara para mutirão processual penal
- Início do Pena Justa para retomada de controle das prisões marcou ações do CNJ em 2025
- Central integrada instalada na Paraíba lança novo olhar sobre penas alternativas à prisão
- CNJ dá início às preparações para o Mutirão Processual Penal de 2024
- Novo Cniep se ajusta a necessidades da magistratura para qualificar inspeções

**Correspondência com taxonomia antiga (6 meses):** Sistema prisional / Pena Justa (âncora 'prisional')


### Tópico 7 — 65 documentos

**Top-15 termos c-TF-IDF:** itinerante, atendimentos, vara itinerante, comunidade, comunidades, cidadania, cavalcante, aldeia, expedição, mutirão, rg, serviços, popruajud, receita, laranjal

**Títulos mais representativos:**

- Justiça Itinerante leva cidadania e serviços essenciais às comunidades ribeirinhas
- Justiça Itinerante realiza 51 atendimentos na primeira ação de 2025 em Porto Alegre (RS)
- Justiça na Praça leva ações de cidadania ao município potiguar de Portalegre
- Justiça Itinerante realiza mais de 100 atendimentos na zona sul de Porto Alegre
- Jornada Terrestre de 2025: comunidade do Ariri (AP) recebe serviços de tribunal e parceiros

**Correspondência com taxonomia antiga (6 meses):** Justiça itinerante / cidadania (âncora 'itinerante')


### Tópico 8 — 83 documentos

**Top-15 termos c-TF-IDF:** conecta, pje, pdpj, soluções tecnológicas, tecnológicas, pdpj br, soluções, tic, tecnologia, transformação digital, banco sentenças, digital, programa conecta, inovação, bastião

**Títulos mais representativos:**

- Com apoio do CNJ, Tribunal de Justiça do Paraná adere a novo sistema processual eletrônico
- Caravana Conecta reúne tribunais do Nordeste em São Luís (MA) para compartilhar boas práticas em inovação
- Portal CNJ de Boas Práticas recebe dezesseis novos projetos
- Tecnologia da Informação no Judiciário é tema de série especial no Link CNJ
- CNJ institui diretrizes do Programa Conecta para nacionalização de soluções tecnológicas dos tribunais

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 9 — 85 documentos

**Top-15 termos c-TF-IDF:** meta, metas, metas nacionais, litigância, abusiva, litigância abusiva, improbidade, improbidade administrativa, processos, distribuídos, nacionais, julgados, processos distribuídos, ações coletivas, administrativa

**Títulos mais representativos:**

- CNJ realiza inspeção no TJMT para avaliar eficiência e transparência do Judiciário
- Meta Nacional da Justiça prioriza em 2024 cerca de 32 milhões de processos mais antigos
- Justiça 4.0: tribunal paulista instala Núcleo para agilizar tramitação de processos no 2º grau
- Corregedorias apontam boas práticas para atuação de correição
- Evento sobre ações coletivas propõe nova lógica da Justiça para reduzir litigância

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 10 — 72 documentos

**Top-15 termos c-TF-IDF:** encontro, programação completa, cooperação judiciária, programação, cooperação jurídica, cooperação, acesse programação, jurídica internacional, youtube, pesquisas, pesquisas empíricas, empíricas, evento, contará, seminário

**Títulos mais representativos:**

- Seminário do CNJ destaca boas práticas na gestão processual do Judiciário
- 31ª edição do Disseminando Boas Práticas do Poder Judiciário acontece na terça (23)
- Justiça mais próxima, transparente, inclusiva e acessível será debatida por profissionais de comunicação do Judiciário
- Gestão de pessoas no Judiciário: inscrições abertas para o 3º encontro nacional
- Encontro nacional no CNJ difunde a cultura de cooperação judiciária

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 11 — 57 documentos

**Top-15 termos c-TF-IDF:** regularização fundiária, fundiária, regularização, títulos, solo seguro, propriedade, solo, imóveis, seguro favela, famílias, favela, títulos propriedade, seguro, moradia, programa regularizar

**Títulos mais representativos:**

- Mais 60 títulos de imóvel são entregues a famílias de Fortaleza durante a Semana Solo Seguro
- Tribunal de Justiça do Rio já concedeu mais de mil títulos do Programa “Solo Seguro”
- Projeto Terra: regularização fundiária avança em municípios gaúchos do Vale do Taquari
- Tribunal piauiense entrega registros de imóveis durante a Semana Solo Seguro — Favela e Comunidades
- Ação de Regularização Fundiária entrega novos títulos à população de baixa renda no ES

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 12 — 108 documentos

**Top-15 termos c-TF-IDF:** rua, situação rua, popruajud, pessoas situação, situação, população situação, atenção pessoas, pop rua, pop, população, rua jud, comitê popruajud, mutirão, resolução 425, 425

**Títulos mais representativos:**

- Corregedoria Nacional de Justiça marca presença no quarto dia do PopRuaJud Sampa + Registre-se
- Justiça Federal de Mato Grosso participa, em Rondonópolis, de atendimento à população em situação de rua
- Mutirão atende a pessoas em situação de rua nesta terça (6/5), em Maceió (AL)
- Justiça do Trabalho do Ceará faz parcerias e planeja ações em favor da população de rua
- Tribunais devem impulsionar atendimento à população em situação de rua

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 13 — 58 documentos

**Top-15 termos c-TF-IDF:** deficiência, pessoas deficiência, acessibilidade, pessoa deficiência, acessibilidade inclusão, deficiência âmbito, inclusão, direitos pessoas, âmbito judicial, barreiras, autista, tea, capacitismo, autistas, pcds

**Títulos mais representativos:**

- Justiça do Piauí lança cartilha de atendimento a PCDs e reforça compromisso com inclusão
- Judiciário busca a eliminação de barreiras para a inclusão de pessoas com deficiência
- Em cinco anos, resolução amplia acessibilidade para pessoas com deficiência na Justiça
- Lei Brasileira de Inclusão completa 10 anos e Justiça capixaba realiza ações de conscientização
- Avaliação biopsicossocial é passo importante para a implementação da Lei de Inclusão

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 14 — 75 documentos

**Top-15 termos c-TF-IDF:** sustentabilidade, climática, ambientais, ambiental, cop30, climáticas, clima, mudanças climáticas, crimes ambientais, conferência, sustentável, ambiente, crise climática, juízo verde, resíduos

**Títulos mais representativos:**

- Conferência internacional debate responsabilidade global sobre sustentabilidade
- Ações para ampliar sustentabilidade no Judiciário contarão com rede de apoio
- Sustentabilidade: serviço ambiental prestado por catadores deve ser valorizado por tribunais
- Pacto envolve tribunais no compromisso do Judiciário com a sustentabilidade
- Judiciário acelera agenda de sustentabilidade e mira à neutralidade de carbono até 2030

**Correspondência com taxonomia antiga (6 meses):** Sustentabilidade ambiental (âncora 'sustentabilidade')


### Tópico 15 — 55 documentos

**Top-15 termos c-TF-IDF:** domicílio, domicílio judicial, judicial eletrônico, comunicações, eletrônico, empresas, comunicações processuais, cadastro, autenticação, usuários, ordens, bloqueio, citações, envio, judicial

**Títulos mais representativos:**

- CNJ alerta para atualização no Domicílio Judicial Eletrônico
- Órgãos públicos de todo o país têm até maio para regularizar adesão ao Domicílio Judicial Eletrônico
- Órgãos públicos já podem se cadastrar no Domicílio Judicial Eletrônico
- Domicílio Judicial Eletrônico conclui cadastro compulsório de 1,2 milhão de empresas
- Ferramenta gratuita para cidadãos facilita consulta de comunicações processuais

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 16 — 80 documentos

**Top-15 termos c-TF-IDF:** pad, disciplinar, afastamento, 0000, reclamação disciplinar, 00 0000, 00, indícios, reclamação, relator, administrativo disciplinar, cautelar, processo administrativo, magistrado, disciplinar pad

**Títulos mais representativos:**

- Juiz do Mato Grosso do Sul responderá a PAD por suspeita de venda de decisões
- Juíza que nomeou peritos sem formação contábil será investigada pelo CNJ
- CNJ abre PAD contra magistrada aposentada da Justiça baiana
- Desembargador aposentado do Tribunal de Justiça do Mato Grosso do Sul responderá a PAD
- CNJ mantém afastamento e abre PADs contra desembargadores do Mato Grosso do Sul

**Correspondência com taxonomia antiga (6 meses):** Processos disciplinares / sessões (âncora 'disciplinar')


### Tópico 17 — 53 documentos

**Top-15 termos c-TF-IDF:** curso, cursos, java, ceajud, ciência dados, avançado, autoinstrucional, capacitações, ciência, bnmp, avançados, python, capacitação, carga horária, horária

**Títulos mais representativos:**

- Webinário apresenta novos cursos de ciência de dados do Justiça 4.0
- CNJ lança capacitação sobre o Domicílio Judicial Eletrônico para pessoa física
- Justiça 4.0 realiza webinário para apresentar novos cursos avançados de ciência de dados
- CNJ lança curso inédito para ferramenta de mineração de processos judiciais
- CNJ lança curso sobre ferramenta de IA generativa para servidores do Judiciário

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 18 — 71 documentos

**Top-15 termos c-TF-IDF:** inovação, laboratórios, festlabs, laboratórios inovação, prêmio inovação, inovadoras, laboratório, ideias, rede inovação, laboratório inovação, soluções inovadoras, prêmio, inovadora, projetos, fest labs

**Títulos mais representativos:**

- Workshop em Maceió discute tecnologia e inovação com presidentes de TJs
- Caravana Conecta reúne soluções inovadoras do Centro-Oeste em Cuiabá
- Prêmio vai reconhecer soluções inovadoras para desafios da Justiça
- 4.º FestLabs: práticas sustentáveis, inovadoras e de impacto social aprimoram a Justiça
- I Prêmio Inovação do Poder Judiciário recebe 285 inscrições

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 19 — 57 documentos

**Top-15 termos c-TF-IDF:** eleitoral, eleições, eleitores, votação, eleitorais, tse, eleitor, eleitoras, eleitoras eleitores, processo eleitoral, urna, eleitorado, votar, assédio eleitoral, voto

**Títulos mais representativos:**

- TSE reafirma compromisso com a inclusão eleitoral
- Eleições 2024: Justiça Eleitoral fortalece presença de indígenas e quilombolas no Tocantins
- TSE celebra 30 anos da urna eletrônica com foco na segurança do voto e no combate à desinformação
- Atualização do cadastro eleitoral garante acessibilidade nas eleições brasileiras
- Justiça Eleitoral do Acre intensifica atendimentos a povos indígenas e em áreas de difícil acesso

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 20 — 108 documentos

**Top-15 termos c-TF-IDF:** violência, doméstica, violência doméstica, mulher, enfrentamento violência, mulheres, violência contra, doméstica familiar, contra, contra mulheres, fonar, contra mulher, maria penha, penha, familiar

**Títulos mais representativos:**

- CNJ amplia proteção a mulheres do Judiciário com protocolo obrigatório contra violência doméstica
- Violência contra mulheres preocupa sociedade, e o Judiciário atua para enfrentar o problema, afirma Fachin
- Presidente do CNJ acompanha instalação de varas de violência doméstica e familiar contra a mulher em SP
- CNJ visita projeto de referência na responsabilização de autores de violência contra mulheres em Rondônia
- Webinário do CNJ reforça integração entre Judiciário e Ligue 180 para proteger mulheres

**Correspondência com taxonomia antiga (6 meses):** Violência doméstica / mulheres (âncora 'violência')


### Tópico 21 — 67 documentos

**Top-15 termos c-TF-IDF:** pena justa, justa, pena, plano, prisional, políticas penais, sistema prisional, plano pena, penais, 347, inconstitucional, coisas inconstitucional, gmf, coisas, comitê políticas

**Títulos mais representativos:**

- Justiça pernambucana promove reunião para construir o Plano Pena Justa no estado
- Justiça de PE conclui oficinas do Pena Justa que buscam soluções para o sistema prisional
- Justiça do Ceará tem primeira reunião para dar andamento ao Plano Pena Justa
- Pena Justa: TRT da 7.ª Região e instituições parceiras debatem qualificação para egressos
- Plano Pena Justa apresenta alto índice de cumprimento no primeiro ano

**Correspondência com taxonomia antiga (6 meses):** Sistema prisional / Pena Justa (âncora 'prisional')


### Tópico 22 — 66 documentos

**Top-15 termos c-TF-IDF:** itinerante, atendimentos, benefício, jef, itinerância, inss, mil atendimentos, marajó, carteira, emissão, portel, serviços, registre, nascimento, registro civil

**Títulos mais representativos:**

- Juizado Itinerante em Porto Murtinho (MS) alcança 71% de acordo em audiências realizadas
- Mais de 1,4 mil processos são movimentados em Juizado Itinerante da Justiça Federal do Tocantins
- De casamento coletivo à escuta em área quilombola, tem de tudo no Justiça Itinerante
- Juizado itinerante alcança 2,4 mil atendimentos no norte de Minas
- Política judiciária para pessoas em situação de rua celebra quatro anos de avanços

**Correspondência com taxonomia antiga (6 meses):** Justiça itinerante / cidadania (âncora 'itinerante')


### Tópico 23 — 69 documentos

**Top-15 termos c-TF-IDF:** linguagem, linguagem simples, simples, selo linguagem, pacto linguagem, ementas, selo, compreensível, uso linguagem, pacto, comunicação, clara, ementa, simplificação, direta compreensível

**Títulos mais representativos:**

- Solenidade marca entrega do Selo Linguagem Simples a 47 órgãos da Justiça
- Linguagem simples: tribunal do Trabalho baiano adota medidas para padronizar ementas
- Estão abertas as inscrições para concorrer ao Selo Linguagem Simples
- Turma do Tribunal do Trabalho paranaense implanta projeto-piloto de linguagem simples
- Tribunal do Tocantins publica decisões com escrita simplificada para facilitar entendimento

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 24 — 47 documentos

**Top-15 termos c-TF-IDF:** enac, exame, exame cartórios, prova, cartórios, certame, cartórios enac, habilitação, concursos, capitais, fgv, serviços notariais, notariais, candidatos, notariais registro

**Títulos mais representativos:**

- Corregedoria Nacional acompanhará realização do 2º Enac neste domingo (28/9)
- 2º Enac: FGV divulga gabarito definitivo e resultado preliminar
- Nota da Corregedoria Nacional de Justiça
- Inscrições para o 3º Exame Nacional dos Cartórios começam no dia 19/2
- Corregedor nacional visita local de provas do Enac neste domingo (27/4)

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 25 — 51 documentos

**Top-15 termos c-TF-IDF:** auditoria, transparência, auditoria interna, ranking transparência, interna, ranking, integridade, riscos, contratações, onit, gestão riscos, governança, controles, compliance, itens

**Títulos mais representativos:**

- Está no ar o regulamento do Ranking da Transparência do Judiciário 2026
- CNJ estabelece novas regras para a edição de 2025 do Ranking da Transparência
- Disseminando Boas Práticas: Gestão Estratégica e Transparência serão tema da 29ª edição
- Transparência e integridade do Judiciário serão acompanhadas por novo colegiado do CNJ
- CNJ convida sociedade a opinar sobre prioridades da Justiça no ciclo 2027–2032

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 26 — 78 documentos

**Top-15 termos c-TF-IDF:** mediação, conflitos, conciliação, solução conflitos, mediação conciliação, conciliar legal, conciliar, solução, cejusc, prêmio conciliar, nupemec, pacificação, métodos, consensuais, métodos consensuais

**Títulos mais representativos:**

- Tribunal e Defensoria de MG promovem Mutirão de Conciliação na Comarca de Taiobeiras
- Tribunais de Minas Gerais se unem para solucionar conflitos fundiários
- Conciliação: Tribunal do Mato Grosso do Sul economiza R$ 8 mi com atuação dos Cejuscs
- Conciliação no Amapá: Justiça Itinerante promove 95 audiências e celebra 33 acordos
- Tribunal do Pará instala primeiro Cejusc do 2.º Grau com foco na conciliação

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 27 — 46 documentos

**Top-15 termos c-TF-IDF:** polícia judicial, segurança institucional, identificação civil, curso, polícia, formação, seeu, policiais judiciais, dnpj, inteligência segurança, policiais, capacitação, socioeducativo, emissão, dmf

**Títulos mais representativos:**

- CNJ capacita mais de 4,6 mil pessoas no 6.º ciclo de formações sobre o Seeu
- DNPJ conclui 2024 com avanços na formação e na doutrina da polícia judicial
- CNJ capacita quase 6 mil pessoas em 5.º Ciclo de formações sobre SEEU
- CNJ capacita mais de mil pessoas para aplicarem normas no sistema penal e socioeducativo
- CNJ apoia formação de juízes em início de carreira sobre tema penal e socioeducativo

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 28 — 65 documentos

**Top-15 termos c-TF-IDF:** execuções fiscais, execuções, fiscais, tributária, execução fiscal, extinção, cobrança, dívida, fiscal, dívida ativa, tributário, litigiosidade, protesto, pgfn, 547

**Títulos mais representativos:**

- Execução fiscal: acordo entre CNJ e TJRN deve extinguir mais de 35 mil processos
- Presidente do CNJ recebe procuradora-geral da Fazenda Nacional para discutir ações conjuntas
- CNJ firma acordo com tribunal e governo da Bahia para extinguir execuções fiscais no estado
- Com política de eficiência, 12 milhões de execuções fiscais foram extintas
- Extinção de processos de execução fiscal sem andamento é monitorada pelo CNJ

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 29 — 53 documentos

**Top-15 termos c-TF-IDF:** escravo, trabalho escravo, tráfico pessoas, tráfico, escravo tráfico, trabalhadores, combate trabalho, escravidão, trabalho decente, decente, enfrentamento trabalho, fontet, análogas, trabalho, condições análogas

**Títulos mais representativos:**

- 2.º Encontro do Fontet define prioridades no combate ao trabalho escravo e ao tráfico de pessoas
- Trabalhadores, entidades e acadêmicos contribuirão para política judiciária pelo trabalho decente
- Justiça do Trabalho da 8.ª Região inicia curso de capacitação para refugiados e migrantes
- Trabalho decente: uma das mais importantes metas buscadas pelo CNJ para a Justiça brasileira
- CNJ disponibiliza dados sobre indígenas, tráfico de pessoas e trabalho escravo

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 30 — 54 documentos

**Top-15 termos c-TF-IDF:** emissões, energia, carbono, gases, estufa, efeito estufa, gases efeito, efeito, elétrica, energia elétrica, descarbonização, emissões gases, consumo, compensação, sustentabilidade

**Títulos mais representativos:**

- Tribunal do Piauí apresenta versão inicial do Plano de Descarbonização
- Encontro Nacional do Judiciário de 2024 recebe selo por zerar emissão de carbono
- Práticas sustentáveis já utilizadas pelos tribunais serão ampliadas com pacto
- Tribunal gera metade da própria energia a partir de fontes limpas
- Tribunal de Pernambuco reduz energia elétrica e gasto público com mudanças de gestão

**Correspondência com taxonomia antiga (6 meses):** Sustentabilidade ambiental (âncora 'sustentabilidade')


### Tópico 31 — 56 documentos

**Top-15 termos c-TF-IDF:** fundiárias, soluções fundiárias, comissão soluções, fundiários, conflitos fundiários, comissão, comissões, terras, alcântara, soluções, conflito, comissões soluções, terra, visitas técnicas, conflitos

**Títulos mais representativos:**

- Comissão de soluções fundiárias fará visita preparatória para mediação de conflitos de terra no sul da Bahia
- Judiciário realiza reuniões e escuta indígenas e proprietários de terra no sul da Bahia
- CNJ recebe povo Pataxó para debater questões sobre o território ancestral
- Comissão Nacional de Soluções Fundiárias acompanha negociações no Norte e Noroeste de MG
- Justiça de Mato Grosso reafirma compromisso com a solução de conflitos agrários

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 32 — 51 documentos

**Top-15 termos c-TF-IDF:** pesquisa, equipes, multidisciplinares, equipes multidisciplinares, gestão pessoas, percepção, atuação equipes, equipes técnicas, metas, dpj, técnicas multiprofissionais, judiciárias, consultivo, cuidados, pesquisa percepção

**Títulos mais representativos:**

- CNJ reabre edital para realização de pesquisa sobre litigância predatória
- Pesquisa atualizará dados sobre percepção e avaliação do Judiciário
- Consulta pública envolve a sociedade na elaboração de Metas Nacionais do Judiciário para 2025
- Pesquisa sobre avaliação do Poder Judiciário pela sociedade será apresentada nesta quinta (18)
- Edital para a realização de pesquisa sobre audiências na Justiça tem prazo prorrogado

**Correspondência com taxonomia antiga (6 meses):** Processos disciplinares / sessões (âncora 'disciplinar')


### Tópico 33 — 55 documentos

**Top-15 termos c-TF-IDF:** infância, crianças, adoção, acolhimento, pacto infância, infância juventude, crianças adolescentes, juventude, pacto, acolhimento familiar, criança, família acolhedora, adoção internacional, adolescentes, legal infância

**Títulos mais representativos:**

- Link CNJ discute avanços e desafios do Pacto pela Primeira Infância
- Coordenadoria da Infância de Alagoas debate estratégias de acolhimento com órgãos do estado
- Ação da Justiça baiana promove atualização dos principais alertas do Sistema Nacional de Adoção
- Encontro discute avanços e desafios do Sistema Nacional de Adoção
- Tribunal do Ceará avança em pautas prioritárias no cuidado à Primeira Infância

**Correspondência com taxonomia antiga (6 meses):** Infância e juventude (âncora 'crianças')


### Tópico 34 — 44 documentos

**Top-15 termos c-TF-IDF:** inspeção, inspeção ordinária, administrativos judiciais, setores administrativos, equipe corregedoria, corregedoria, inspeções, prazos processuais, trabalhos, serventias extrajudiciais, extrajudiciais, setores, serventias, administrativos, corregedoria realiza

**Títulos mais representativos:**

- Tribunal receberá comitiva da Corregedoria Nacional de Justiça para inspeção em março
- Corregedoria Nacional inicia inspeção no TJPE nesta segunda-feira (7/4)
- Corregedoria Nacional de Justiça faz primeira inspeção de 2026 no TJRO
- Corregedoria Nacional de Justiça realiza inspeção no TJRJ a partir de segunda (25/5)
- TJPI recebe inspeção ordinária da Corregedoria Nacional até quarta-feira (25/9)

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 35 — 42 documentos

**Top-15 termos c-TF-IDF:** leitura, mentes, literárias, mentes literárias, remição, livros, projeto mentes, livro, escrita, remição pena, prisional, sistema prisional, biblioteca, privadas liberdade, pessoas privadas

**Títulos mais representativos:**

- Mentes Literárias: juízes e juízas debatem acesso à cultura no sistema prisional
- CNJ e tribunal alagoano lançam Projeto Mentes Literárias em presídio de Maceió
- Tribunal de Mato Grosso e CNJ lançam projeto de remição pela leitura na Penitenciária Central
- 6ª Jornada de Leitura no Cárcere começa segunda-feira (17/11) com transmissão ao vivo
- Mais de 10 mil pessoas privadas de liberdade acompanharam 5.ª Jornada de Leitura no Cárcere

**Correspondência com taxonomia antiga (6 meses):** Sistema prisional / Pena Justa (âncora 'prisional')


### Tópico 36 — 81 documentos

**Top-15 termos c-TF-IDF:** paz casa, mulher, violência doméstica, doméstica, semana paz, violência, contra mulher, maria penha, penha, doméstica familiar, paz, casa, maria, familiar, coordenadoria mulher

**Títulos mais representativos:**

- Justiça pela Paz em Casa: 27.ª edição da ação começa nesta segunda (19/8)
- Justiça do Ceará agenda 353 audiências em ação voltada ao combate da violência contra a mulher
- Início do mutirão de audiências marca a abertura da 28ª Semana Justiça pela Paz em Casa no Acre
- 31ª Semana Justiça pela Paz em Casa acelera julgamentos de casos de violência doméstica
- Justiça pela Paz em Casa: mais de 1,3 mil processos serão levados a julgamento em Goiás

**Correspondência com taxonomia antiga (6 meses):** Violência doméstica / mulheres (âncora 'violência')


### Tópico 37 — 40 documentos

**Top-15 termos c-TF-IDF:** desaparecimento, sales pimenta, sales, desaparecimento forçado, pimenta, vítimas, óbito, pessoas desaparecidas, desaparecidas, direitos humanos, humanos, familiares, forçado, ceavs, observatório

**Títulos mais representativos:**

- CNJ debate no Rio medidas para aprimorar atendimento a vítimas de violência de Estado
- CNJ realiza debate sobre desaparecimento forçado e justiça de transição
- CNJ convida rede de vítimas da violência estatal para atuar em Observatório de Direitos Humanos
- Justiça de Transição e desaparecimento forçado são temas de evento internacional do CNJ
- Observatório inicia 2026 acompanhando casos relacionados a conflitos fundiários, tragédias e crimes dolosos

**Correspondência com taxonomia antiga (6 meses):** Direitos humanos / Corte IDH (âncora 'humanos')


### Tópico 38 — 42 documentos

**Top-15 termos c-TF-IDF:** imóveis, onr, provimento, cartórios, indisponibilidade, pje, notarial, registro, operador, registro imóveis, digitalização, recuperação judicial, serp, recuperação, migração

**Títulos mais representativos:**

- Com novo provimento, cartórios entram em nova fase de modernização tecnológica
- Tribunal do Rio Grande do Norte desenvolve novo sistema para pagamento de RPV’s
- Novo sistema facilita cumprimento de ordens de indisponibilidade de imóveis
- Ferramenta digital do CNJ faz um ano e transforma a rotina dos gabinetes
- Tribunal cearense registra emissão de mais de 650 mil certidões judiciais em um ano

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 39 — 53 documentos

**Top-15 termos c-TF-IDF:** meninas mulheres, marajó, meninas, ação meninas, mulheres marajó, mulheres, violência, mulher, doméstica, violência doméstica, tjpa, violência contra, renata gil, contra, gil

**Títulos mais representativos:**

- Sertão de Pernambuco recebe “Ação Meninas e Mulheres” do CNJ nos dias 4 e 5 agosto
- Celeridade processual e mobilização da sociedade marcam a 32ª Semana Justiça pela Paz em Casa
- CNJ intensifica ações de proteção às mulheres durante Justiça Itinerante no Marajó
- Justiça do Pará coordena planejamento da 3.ª Ação de Meninas e Mulheres do Marajó
- Programa Brasil Lilás é lançado para ampliar ações de prevenção à violência de gênero

**Correspondência com taxonomia antiga (6 meses):** Violência doméstica / mulheres (âncora 'violência')


### Tópico 40 — 45 documentos

**Top-15 termos c-TF-IDF:** memória, patrimônio cultural, patrimônio, história, gestão documental, documental, prêmio memória, preservação, cultural, escravidão, documental memória, arquivos, categoria patrimônio, escravidão liberdade, históricos

**Títulos mais representativos:**

- Memória do Judiciário é tema do programa Link CNJ desta semana
- Congresso debate preservação de arquivos e acesso à informação no Judiciário
- Em 2026, Prêmio CNJ Memória do Judiciário terá tema especial sobre escravidão e liberdade
- Memória do Poder Judiciário: exposição “150 anos” resgata história de sete tribunais brasileiros
- 5.º Encontro de Memória do Poder Judiciário debate cultura, diversidade e preservação histórica

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 41 — 41 documentos

**Top-15 termos c-TF-IDF:** programa caminhos, jovens, caminhos, adolescentes, acolhidos, acolhimento, aprendizagem, pnc, santa catarina, empregabilidade, profissional, catarina, jovens acolhidos, socioeducativo, santa

**Títulos mais representativos:**

- Justiça fluminense lança programa para capacitar jovens em situação de vulnerabilidade
- Justiça do Ceará debate oportunidades de profissionalização para socioeducandos
- Encontro deve fortalecer capacitação profissional e pessoal de jovens acolhidos
- Corregedoria de Justiça capixaba avança nas ações de programa para infância e juventude
- CNJ lança estratégia nacional para fortalecer o sistema socioeducativo

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 42 — 43 documentos

**Top-15 termos c-TF-IDF:** corte idh, idh, direitos humanos, humanos, interamericana, corte, interamericano, sistema interamericano, interamericano direitos, interamericana direitos, umf, corte interamericana, decisões sistema, internacionais, direitos

**Títulos mais representativos:**

- Novos protocolos do CNJ ampliam a cultura de direitos humanos no Judiciário
- CNJ fortalece integração entre Justiça brasileira e sistema interamericano de direitos humanos
- CNJ reúne tribunais para fortalecer proteção de direitos humanos
- CNJ lança 3ª fase do Pacto Nacional do Judiciário pelos Direitos Humanos
- Magistrados selecionados pelo CNJ chegam à Corte IDH para intercâmbio inédito

**Correspondência com taxonomia antiga (6 meses):** Direitos humanos / Corte IDH (âncora 'humanos')


### Tópico 43 — 36 documentos

**Top-15 termos c-TF-IDF:** barroso, enam, magistratura, candidatos, concurso, luís roberto, exame magistratura, roberto barroso, milhões processos, stf luís, fachin, conselheiro, exame, mandato, stf

**Títulos mais representativos:**

- Ministro Barroso destaca realizações no seu primeiro ano de gestão do CNJ
- Em São Luís, Barroso destaca ações do CNJ para tornar a Justiça acessível e inclusiva
- Fachin destaca produtividade do Judiciário ao abrir reunião preparatória do Encontro Nacional
- CNJ avança nos preparativos para o 19.º Encontro Nacional do Poder Judiciário
- Barroso abre reunião preparatória com balanço de metas e desafios do Judiciário

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 44 — 50 documentos

**Top-15 termos c-TF-IDF:** depoimento, depoimento especial, crianças adolescentes, crianças, criança adolescente, adolescentes, criança, protegida, infância, adolescente, vítimas testemunhas, abuso, especial, adolescentes vítimas, proteção crianças

**Títulos mais representativos:**

- CNJ inicia mobilização nacional para fortalecer proteção de crianças e adolescentes
- CNJ lança Mês da Infância Protegida com foco no enfrentamento à violência
- Mês da Infância Protegida: Como denunciar violência contra crianças e adolescentes
- Mês da Infância Protegida: mutirão antecipa depoimentos especiais de crianças e adolescentes
- Mês da Infância Protegida: políticas judiciárias protegem e asseguram direitos fundamentais

**Correspondência com taxonomia antiga (6 meses):** Infância e juventude (âncora 'crianças')


### Tópico 45 — 36 documentos

**Top-15 termos c-TF-IDF:** fundiária, solo seguro, solo, regularização fundiária, fundiária urbana, regularização, prêmio, urbana, seguro, governança fundiária, obras, fundiária rural, rural, premiação, prêmio prioridade

**Títulos mais representativos:**

- Inscrições para o Prêmio Solo Seguro 2025 seguem abertas até 31 de março
- Corregedoria celebra boas práticas com entrega do Prêmio Solo Seguro edição 2024/2025
- Inscrições para o Prêmio Solo Seguro 2025/2026 seguem abertas até 31 de março
- Regularização fundiária e justiça social marcam entrega do Prêmio Solo Seguro 2026
- Tribunal alagoano debate metas da Justiça do Trabalho para 2026 em audiência pública

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 46 — 48 documentos

**Top-15 termos c-TF-IDF:** adoção, pai, sna, pretendentes, busca ativa, paternidade, pai presente, crianças, dot, criança, reconhecimento paternidade, ativa, crianças adolescentes, processo adoção, nome pai

**Títulos mais representativos:**

- Justiça de Goiás lança Programa Pai Presente Volante na Grande Goiânia
- Justiça baiana realiza 2.º mutirão de reconhecimento de paternidade
- Café com adoção: Justiça de Rondônia promove ação de sensibilização com famílias
- Reconhecimento de paternidade: Justiça cearense abre inscrições para mutirão de atendimento
- Justiça mineira realiza 7ª edição do Mutirão de Reconhecimento de Paternidade

**Correspondência com taxonomia antiga (6 meses):** Infância e juventude (âncora 'crianças')


### Tópico 47 — 27 documentos

**Top-15 termos c-TF-IDF:** lgbtqia, pessoas lgbtqia, rogéria, população lgbtqia, formulário rogéria, trans, lgbtqiapn, transexuais, fórum promoção, identidade gênero, orientação sexual, promoção direitos, travestis, direitos pessoas, diversidade

**Títulos mais representativos:**

- Especialistas debatem aspectos jurídicos do registro civil de pessoas LGBTQIA+
- Evento do CNJ pauta desafios e oportunidades para a inclusão efetiva de pessoas LGBTQIA+
- Cartilha aborda direitos da comunidade LGBTQIAPN+
- Promoção e proteção dos direitos LGBTQIA+ são tema de encontro no CNJ nos dias 25 e 26/6
- Compromisso da Justiça com a população LGBTQIAPN+ efetiva direitos fundamentais

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 48 — 47 documentos

**Top-15 termos c-TF-IDF:** saúde, prêmio saúde, suplementar, natjus, judicialização saúde, judicialização, saúde pública, doação, pública suplementar, fonajus, aedo, notas, transplantes, doação órgãos, doador

**Títulos mais representativos:**

- CNJ premia melhores práticas judiciárias em saúde
- Soluções inovadoras em saúde são premiadas durante Congresso do Fonajus
- Palestra sobre importância do NatJus encerra a Semana Nacional de Saúde na Paraíba
- Tribunais participam da 1.ª Semana Nacional da Saúde com ações integradas
- Ações focadas na melhoria da gestão processual são reconhecidas pelo Prêmio Justiça e Saúde

**Correspondência com taxonomia antiga (6 meses):** Saúde / judicialização / SUS (âncora 'saúde')


### Tópico 49 — 50 documentos

**Top-15 termos c-TF-IDF:** indígena, indígenas, registro civil, registro, povos, povos indígenas, aldeia, nascimento, etnia, registre, sub registro, civil, sub, civil nascimento, documentação

**Títulos mais representativos:**

- Identificação civil: Justiça de Roraima amplia atendimento à comunidade Waimiri Atroari
- Registre-se Brasil Parente leva cidadania à população indígena brasileira
- Registre-se: Justiça Federal realizou atendimentos a 222 indígenas em Passo Fundo
- Inclusão do nome de etnia em registro civil leva cidadania a povos indígenas na Amazônia
- Tribunal de Roraima lança primeira Ouvidoria Eleitoral dos Povos Indígenas do Brasil

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 50 — 37 documentos

**Top-15 termos c-TF-IDF:** disponibilidade, disciplinar, relator, revisão disciplinar, censura, 0000, 00 0000, magistrado, 00, sessão ordinária, decisão, voto, pena censura, sessão, ordinária

**Títulos mais representativos:**

- Desembargador mineiro acusado de conceder vantagem indevida é punido com pena de disponibilidade
- CNJ aplica pena de remoção a juiz que depreciou magistrados e membros do MPF
- Juiz que negligenciava atuação de assessores recebe pena de disponibilidade por 90 dias
- CNJ impõe pena de disponibilidade a juiz por imprudência em plantão judiciário
- CNJ pune com disponibilidade juiz federal que atua no Amapá

**Correspondência com taxonomia antiga (6 meses):** Processos disciplinares / sessões (âncora 'disciplinar')


### Tópico 51 — 28 documentos

**Top-15 termos c-TF-IDF:** lgbtqiapn, trans, casais, diversidade, homoafetivos, população lgbtqiapn, lgbtqia, casamentos, casamento, comitê equidade, diversidade gênero, gênero diversidade, pessoas trans, pessoas lgbtqiapn, comunidade lgbtqiapn

**Títulos mais representativos:**

- Evento da Justiça do Trabalho paulista defende a promoção de direitos das pessoas LGBTQIA+
- Justiça do Amazonas coordena ação para facilitar o reconhecimento de identidade a pessoas trans
- Tribunal de Campinas discute inclusão LGBTQIA+ na Justiça do Trabalho
- CNJ marca presença em casamento comunitário LGBTQIAPN+ em Goiás
- Dignidade para a comunidade LGBTQIAPN+ é tema de debate no Tribunal do Trabalho paranaense

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 52 — 43 documentos

**Top-15 termos c-TF-IDF:** descarte, resíduos, recicláveis, reciclagem, materiais, catadores, materiais recicláveis, destinação, toneladas, documental, sustentável, eliminação, coleta seletiva, seletiva, gestão documental

**Títulos mais representativos:**

- Encontro da Justiça Federal no Pará reforça compromisso com a gestão de resíduos sólidos
- Justiça Federal no Amapá instala Ecoponto para descarte de vidro
- Corregedoria-Geral da Justiça do Ceará doa quase 100 quilos de materiais recicláveis
- TJRN destina mais de 5,7 toneladas de papel para reciclagem em 2025
- Justiça fluminense amplia projeto sustentável com novo Ecoponto no Fórum Central

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 53 — 29 documentos

**Top-15 termos c-TF-IDF:** fonajus, fonajus itinerante, saúde, judicialização saúde, judicialização, assistência saúde, suplementar, saúde pública, demandas assistência, estaduais saúde, adequada demandas, fórum saúde, judiciária resolução, pública suplementar, comitês estaduais

**Títulos mais representativos:**

- Fonajus Itinerante chega a Minas Gerais no dia 4 de junho
- São Paulo será primeiro estado a receber Fonajus Itinerante
- Justiça da Paraíba recebe o Fonajus Itinerante nos dias 18 e 19 de junho
- Fórum Nacional de Saúde do Judiciário realiza seu IV Congresso no Ceará
- Fonajus participa de congresso no Rio de Janeiro que discutiu caminhos para a judicialização da saúde

**Correspondência com taxonomia antiga (6 meses):** Justiça itinerante / cidadania (âncora 'itinerante'); Saúde / judicialização / SUS (âncora 'saúde')


### Tópico 54 — 27 documentos

**Top-15 termos c-TF-IDF:** libras, intérprete, auditiva, deficiência auditiva, intérprete libras, surda, surdas, acessibilidade, balcão, sinais, pessoas surdas, deficiência, surdos, visual, língua sinais

**Títulos mais representativos:**

- Justiça do Trabalho de Campinas amplia serviço remoto de Libras e legendas para audiências
- Atuação de tradutores e intérpretes de Libras aproxima a Justiça cearense da comunidade surda
- Justiça do Trabalho de Sergipe realiza 1ª audiência com intérprete de libras
- Seção Judiciária de Mato Grosso contará com serviços de intérprete de Libras
- Projeto Manhãs com Libras chega à quarta edição

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 55 — 39 documentos

**Top-15 termos c-TF-IDF:** pauta verde, semana pauta, verde, ambiental, ambientais, pauta, processos ambientais, fórum ambiental, lixões, ambiente, semana, ii semana, resolução 433, 433 2021, 433

**Títulos mais representativos:**

- Semana da Pauta Verde: Justiça potiguar realiza mutirão de conciliações em processos ambientais
- Justiça baiana participa da II Semana da Pauta Verde com foco na celeridade dos processos ambientais
- Semana da Pauta Verde: tribunais realizarão ações entre os dias 18 e 22 de agosto
- Judiciário Sustentável apresenta novo balanço e marca entrega de Prêmio Juízo Verde
- Semana da Pauta Verde institucionaliza atenção permanente da Justiça com questão ambiental

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 56 — 35 documentos

**Top-15 termos c-TF-IDF:** democracia, fachin, constituição, democrático, constitucional, edson fachin, constituinte, defesa, edson, 1988, criminosas, organizações criminosas, direitos humanos, interamericano, crime organizado

**Títulos mais representativos:**

- Encontro Nacional: Fachin diz que Judiciário deve manter integridade e credibilidade social
- Independência judicial é condição para democracia, afirma Fachin em evento na USP
- Corte Interamericana inicia atividades no Brasil com sessão de abertura no STF
- Em primeira reunião à frente do ODH, ministro Fachin reforça compromisso do Observatório com a democracia
- Fachin defende comunicação do Judiciário como instrumento de confiança e democracia

**Correspondência com taxonomia antiga (6 meses):** Direitos humanos / Corte IDH (âncora 'humanos')


### Tópico 57 — 61 documentos

**Top-15 termos c-TF-IDF:** semana conciliação, conciliação, acordos, milhões, cejusc, trt, trabalhista, audiências, semana, homologados, trabalhistas, cejuscs, conciliação trabalhista, conciliados, solução disputas

**Títulos mais representativos:**

- Justiça do Trabalho do Paraná ajusta acordos em R$ 61,4 mi durante a Semana da Conciliação
- Tribunal conquista medalha de prata na 10ª Semana Nacional da Conciliação Trabalhista
- Semana Nacional da Conciliação Trabalhista: 8.ª Região garante quase R$ 48 milhões em acordos
- Justiça Federal no Tocantins teve 80% de aproveitamento das audiências de conciliação marcadas em 2025
- Semana da Conciliação Trabalhista: Tribunal da 11.ª Região movimenta mais de R$ 20 milhões

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 58 — 30 documentos

**Top-15 termos c-TF-IDF:** medicamentos, saúde, fonajus, direito saúde, natjus, 1234, enunciados, sus, suplementar, saúde suplementar, fornecimento, fornecimento medicamentos, jornada direito, medicamento, vii jornada

**Títulos mais representativos:**

- VII Jornada de Direito da Saúde aprova 30 novos enunciados
- Novos enunciados são aprovados para orientar decisões judiciais sobre saúde
- Participantes da VII Jornada de Direito da Saúde analisarão novos enunciados
- Bases de dados técnicos de saúde devem ser integradas ao e-NatJus 4.0
- Congresso do Fonajus: oficinas vão discutir desafios da judicialização em saúde

**Correspondência com taxonomia antiga (6 meses):** Saúde / judicialização / SUS (âncora 'saúde')


### Tópico 59 — 27 documentos

**Top-15 termos c-TF-IDF:** idosa, pessoa idosa, idosas, pessoas idosas, idoso, idosos, pessoa, envelhecimento, curatela, população idosa, selo amigo, 520, selo, amigo, juizados

**Títulos mais representativos:**

- Tribunal baiano promove semana de mobilização para maior celeridade em processos com idosos
- Conselheiro destaca direitos da pessoa idosa em simpósio no STJ
- Selo Tribunal Amigo da Pessoa Idosa: inscrições se encerram no domingo (31/8)
- Judiciário baiano analisa mais de 169 mil processos envolvendo pessoas idosas
- Evento discute práticas para fortalecer direitos das pessoas idosas no sistema de justiça

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 60 — 26 documentos

**Top-15 termos c-TF-IDF:** caminhos literários, literários, leitura, cultura, letras, socioeducativo, unidades socioeducativas, livros, adolescentes, cria letras, acesso cultura, literários socioeducativo, case, companhia letras, caminhos

**Títulos mais representativos:**

- Adolescentes socioeducandos catarinenses participam do projeto Caminhos Literários
- Projeto do TJES leva cultura para as unidades socioeducativas do Estado
- 3º Caminhos Literários no Socioeducativo celebra o protagonismo juvenil
- Caminhos Literários 2025 começa com debates sobre cultura e juventude
- CNJ leva clubes de leitura para o sistema socioeducativo

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 61 — 31 documentos

**Top-15 termos c-TF-IDF:** centros inteligência, caravana virtual, centro inteligência, caravana, nota técnica, nota, centros, inteligência, virtual, caravanas, cipj, virtuais, inteligência cipj, rede centros, gestão precedentes

**Títulos mais representativos:**

- Centro de Inteligência de tribunal mineiro promove caravana virtual nesta segunda (25/11)
- Tribunal do Paraná recebe Caravana Virtual da Rede de Centros de Inteligência no dia 22/10
- Caravana virtual aborda impactos do uso de assinatura eletrônica em processos judiciais
- Justiça Federal em Sergipe recebe Caravana Virtual dos Centros de Inteligência
- Justiça Federal da 2.ª Região e CNJ discutem as boas práticas dos Centros de Inteligência

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 62 — 56 documentos

**Top-15 termos c-TF-IDF:** jus br, jus, br, sngb, saref, portal, consulta, consulta processual, unificada, peticionamento, bens, gestão bens, bnp, sisperjud, djen

**Títulos mais representativos:**

- Novo painel monitora a integração de tribunais brasileiros ao Portal Unificado de Serviços
- Mais de 213 mil usuários já acessam serviços do Poder Judiciário via Jus.br
- Jus.br: conheça as funcionalidades do novo portal da Justiça brasileira
- CNJ lança portal que monitora os serviços da Plataforma Digital do Poder Judiciário
- Meio milhão de pessoas já acessa serviços do Judiciário via Jus.br

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 63 — 28 documentos

**Top-15 termos c-TF-IDF:** assédio, assédio moral, enfrentamento assédio, assédio discriminação, discriminação, moral, assédio sexual, prevenção enfrentamento, sexual discriminação, moral assédio, combate assédio, sexual, prevenção, prevenção assédio, semana combate

**Títulos mais representativos:**

- Prevenção ao assédio em ambiente institucional ganha reforço com rodada de reuniões feitas pelo CNJ
- Tribunal do Piauí realiza campanha e pesquisa interna para combater o assédio no trabalho
- Balanço da Semana de Combate ao Assédio no TJSC evidencia alcance das ações no Estado
- Judiciário reforça compromisso no combate ao assédio e à discriminação
- Tribunal baiano institui política interna de prevenção ao assédio e à discriminação

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 64 — 22 documentos

**Top-15 termos c-TF-IDF:** sexual, feminicídio, assédio sexual, sexual trabalho, sinal vermelho, violência, sinal, mulheres, vermelho, vítima, contra, campanha sinal, doméstica, violência doméstica, violência contra

**Títulos mais representativos:**

- CNJ realizará encontros para qualificar responsabilização por violência doméstica em agosto
- Proteção mais rápida: Justiça concede 225 mil medidas protetivas no primeiro quadrimestre do ano
- Justiça Originária: desafios persistem para levar a Lei Maria da Penha aos territórios indígenas
- Julgamentos de feminicídio aumentam em 17%, aponta CNJ
- Reportagem premiada relata aumento dos casos de violência doméstica em Pernambuco

**Correspondência com taxonomia antiga (6 meses):** Violência doméstica / mulheres (âncora 'violência')


### Tópico 65 — 26 documentos

**Top-15 termos c-TF-IDF:** beneficiários, rpvs, previdenciárias assistenciais, região sede, assistenciais, previdenciárias, trf região, pagamento, valor rpvs, saque, pix, jurisdição, requisições, requisições pequeno, trf

**Títulos mais representativos:**

- Justiça Federal libera pagamento de RPVs a mais de 180 mil beneficiários
- Justiça Federal libera o pagamento de RPVs a mais de 280 mil beneficiários
- Justiça Federal libera o pagamento de RPVs a mais de 199 mil beneficiários
- Justiça Federal libera o pagamento de RPVs a mais de 231 mil beneficiários
- Justiça Federal libera o pagamento de RPVs a mais de 227 mil beneficiários

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 66 — 40 documentos

**Top-15 termos c-TF-IDF:** pse, socioeducativo, plataforma socioeducativa, socioeducativa, sistema socioeducativo, central vagas, socioeducativas, medidas socioeducativas, vagas, gmf, adolescentes, adolescentes conflito, plataforma, socioeducativa pse, atendimento socioeducativo

**Títulos mais representativos:**

- Plataforma Socioeducativa é implantada no Maranhão seguindo plano de nacionalização
- TJPE realiza inspeções em 100% dos programas de atendimento socioeducativo do estado
- Plataforma Socioeducativa chega ao TJPE e avança para novos estados
- Plataforma Socioeducativa chega a Rondônia, somando cinco estados em operação
- Judiciário paraibano será o terceiro do país a implantar Plataforma Socioeducativa (PSE)

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 67 — 29 documentos

**Top-15 termos c-TF-IDF:** conciliação itinerante, nupemec, conciliação, cejusc, nupemec tjma, união estável, pensão alimentícia, dívidas, alimentícia, estável, tjma, divórcio, paternidade, pensão, débitos

**Títulos mais representativos:**

- Conciliação Itinerante registra quase R$ 1 milhão em acordos no Oeste maranhense
- Projeto Conciliação Itinerante aproxima Justiça das comunidades maranhenses
- Conciliação Itinerante vai atender a população de quatro municípios maranhenses
- Conciliação itinerante: projeto de tribunal maranhense realiza mais de 400 audiências
- Justiça Itinerante atende a Comunidade Quilombola de Conceição das Crioulas

**Correspondência com taxonomia antiga (6 meses):** Justiça itinerante / cidadania (âncora 'itinerante')


### Tópico 68 — 16 documentos

**Top-15 termos c-TF-IDF:** programada, manutenção, atendimento usuário, comunicação dti, dti, departamento tecnologia, necessidade suporte, ti, caso dúvidas, contínua serviços, indisponibilidade, central atendimento, informa, informação comunicação, 20h

**Títulos mais representativos:**

- Infraestrutura de TI do CNJ passa por manutenção entre sexta (20/2) e domingo (22/2)
- CNJ faz manutenção programada no sistema e-Carta
- CNJ informa sobre manutenção em infraestrutura de TI nesta quinta-feira (16/4)
- CNJ informa sobre manutenção programada na infraestrutura de TI
- PJe do CNJ passa por manutenção programada no sábado (11/10)

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 69 — 28 documentos

**Top-15 termos c-TF-IDF:** saúde, redenção, fonajus, semana saúde, fonajus itinerante, judicialização, judicialização saúde, comitê saúde, saúde pública, cejusc saúde, 2ª semana, fórum saúde, demandas saúde, suplementar, 14h

**Títulos mais representativos:**

- Fonajus Itinerante no Amapá: ações fortalecem diálogo entre Judiciário e Executivo para melhoria da saúde
- Enfam e CNJ promovem seminário sobre desafios e perspectivas da judicialização da saúde no Brasil
- Fonajus Itinerante conhece ações da Justiça de Pernambuco sobre litigância em saúde
- TJPB e CNJ realizam Fonajus Itinerante com o tema ‘A Saúde Onde Você Está’
- Fonajus Itinerante no RJ discute cooperação para atender demandas de saúde

**Correspondência com taxonomia antiga (6 meses):** Justiça itinerante / cidadania (âncora 'itinerante'); Saúde / judicialização / SUS (âncora 'saúde')


### Tópico 70 — 24 documentos

**Top-15 termos c-TF-IDF:** inspeção, inspeção corregedoria, arnoldo, corregedoria, desembargador arnoldo, camanho, arnoldo camanho, inspeção ordinária, juiz garantias, central garantias, garantias, nac, tjes, organizações criminosas, criminosas

**Títulos mais representativos:**

- Corregedoria Nacional abre trabalhos de inspeção em tribunal alagoano
- Corregedoria Nacional encerra agenda de inspeções com verificação no TJCE
- Corregedoria Nacional inicia inspeção ordinária no Tribunal de Justiça do Espírito Santo
- Inspeção da Corregedoria Nacional no TJRS é encerrada após semana de trabalhos
- Corregedoria Nacional de Justiça determina correição extraordinária no TJBA

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 71 — 20 documentos

**Top-15 termos c-TF-IDF:** violência, ativismo, combate violência, violência digital, 21 ativismo, doméstica, violência doméstica, mulheres, eca digital, gênero, fim violência, violência gênero, homens, mulher, meninas

**Títulos mais representativos:**

- CNJ promove encontros para fortalecer proteção às mulheres e equidade de gênero
- Projeto quer fortalecer o acesso à Justiça de vítimas de violência doméstica
- CNJ 20 anos: Justiça garante efetividade ao combate à violência contra mulheres
- CNJ aprova novas boas práticas nos eixos de combate à violência e infância e juventude
- Justiça no DF reforça combate à violência de gênero

**Correspondência com taxonomia antiga (6 meses):** Violência doméstica / mulheres (âncora 'violência')


### Tópico 72 — 23 documentos

**Top-15 termos c-TF-IDF:** exposição, arte, mostra, memória, museu, negra, escravização, obras, rua dom, dom manuel, artistas, constituinte, moisés, programa plural, manuel

**Títulos mais representativos:**

- Escola de educação social visita mostra sobre participação negra na Constituinte
- CNJ recebe, no Mês da Consciência Negra, exposição “A Terra que Insiste”
- Diálogos com as Juventudes promove conversa sobre equidade e cidadania digital em escolas do RS
- Exposição “Valongo: Justiça pela Memória do Cais” é prorrogada até março
- TRE-BA lança cartilha educativa sobre cidadania e vivências da Comunidade Quilombola Quingoma

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 73 — 59 documentos

**Top-15 termos c-TF-IDF:** audiências concentradas, concentradas, socioeducativo, socioeducativas, semiliberdade, socioeducativa, adolescentes, medida socioeducativa, internação, medidas socioeducativas, adolescente, infância juventude, audiências, juventude, gmf

**Títulos mais representativos:**

- 1.ª Vara Criminal da Infância e Juventude de Maceió promove o 3.º ciclo de audiências concentradas
- Justiça do Tocantins realiza agendas para a qualificação do Sistema Socioeducativo
- Realizado 1.º ciclo de audiências concentradas de 2025 no socioeducativo de Parnamirim
- Grupo de trabalho inicia ações para a implementação do NAI na Paraíba
- Justiça alagoana promove 1.º ciclo de audiências concentradas no sistema socioeducativo

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 74 — 22 documentos

**Top-15 termos c-TF-IDF:** casamento, casar, casais, casamento coletivo, amor, presídio, sonho, projeto itinerante, noivos, itinerante, matrimônio, filhos, casamento comunitário, união, juntos

**Títulos mais representativos:**

- Tribunal de Goiás celebra primeiro casamento comunitário do Raízes Kalungas
- Em Caxias (RJ), moradores recebem o programa Justiça Itinerante Levando Cidadania
- No Rio de Janeiro, Justiça Itinerante atende 151 internas do Instituto Penal Talavera Bruce
- Justiça Itinerante realiza, em Quatis (RJ), casamento de idosos após 35 anos de união
- Justiça Itinerante fluminense realiza casamentos e atendimentos em penitenciária de Gericinó

**Correspondência com taxonomia antiga (6 meses):** Justiça itinerante / cidadania (âncora 'itinerante')


### Tópico 75 — 19 documentos

**Top-15 termos c-TF-IDF:** trabalhista, execução trabalhista, conciliação trabalhista, semana execução, semana conciliação, conciliação, cneet, trt ba, inclusão processo, semana, processo pauta, efetividade execução, pauta semana, tempo recursos, execução

**Títulos mais representativos:**

- Semana Nacional da Conciliação Trabalhista 2025 será de 26 a 30 de maio
- Semana Nacional da Conciliação Trabalhista será realizada em maio
- Tribunal mineiro faz ajustes finais para a 15.ª Semana Nacional de Execução Trabalhista
- Justiça do Trabalho mineira inicia Semana da Conciliação com 600 processos em pauta
- Semana Nacional da Execução Trabalhista 2025 será realizada de 15 a 19 de setembro

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 76 — 22 documentos

**Top-15 termos c-TF-IDF:** trabalho infantil, infantil, combate trabalho, imposto, aprendizagem, estímulo aprendizagem, infantil estímulo, marajó, erradicação trabalho, crianças, renda, erradicação, imposto renda, crianças adolescentes, renda infância

**Títulos mais representativos:**

- Trabalho infantil: público recebe orientações sobre as formas de combate
- Crianças do Marajó recebem atendimento especializado e garantia de direitos no Justiça Itinerante
- Imposto de Renda 2025: recursos podem beneficiar crianças da Ilha do Marajó
- Comissão de Combate ao Trabalho Infantil participa de ação em feira dos municípios alagoanos
- Justiça do Trabalho da 11.ª Região promove ações no Mês de Combate ao Trabalho Infantil

**Correspondência com taxonomia antiga (6 meses):** Infância e juventude (âncora 'crianças')


### Tópico 77 — 21 documentos

**Top-15 termos c-TF-IDF:** indígenas, povos, povos indígenas, línguas, fonepi, língua, terena, línguas indígenas, direitos povos, adolescentes indígenas, acesso povos, indígena, tradicionais, eloy, manual

**Títulos mais representativos:**

- Fórum do Judiciário amplia debate sobre acesso à Justiça para povos indígenas
- Fórum do Judiciário discutirá acesso à Justiça e causas indígenas
- Congresso discute desafios da Justiça em territórios indígenas e reforça diálogo intercultural
- CNJ lança manual para fortalecer acesso de povos indígenas à Justiça
- Justiça de Rondônia reafirma compromisso com garantia de direitos da comunidade indígena

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 78 — 22 documentos

**Top-15 termos c-TF-IDF:** sessão, sessão ordinária, ordinária, secretaria processual, secretaria jus, mail secretaria, 5180, 5180 mail, 2326 5180, contato secretaria, telefone 61, pauta completa, 61 2326, 2326, controle administrativo

**Títulos mais representativos:**

- CNJ realiza 14ª Sessão Ordinária na terça-feira (28/10)
- 11.ª Sessão Ordinária de 2025 do CNJ traz pauta com 14 itens
- Nove itens compõem a pauta da 3.ª Sessão Extraordinária de 2025 do CNJ nesta terça-feira (10/6)
- Plenário do CNJ aprecia 13 itens em sessão extraordinária na terça-feira (27/5)
- CNJ realiza 7.ª Sessão Ordinária de 2025 na terça-feira (20/5)

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 79 — 16 documentos

**Top-15 termos c-TF-IDF:** assédio, disciplinar, fatos, sexual, acusado, assédio sexual, vítima, estupro, vida privada, contra dignidade, afastamento, pad, dignidade sexual, administrativo disciplinar, espíndola

**Títulos mais representativos:**

- Desembargadores do TJGO responderão por supostamente menosprezarem vítima de assédio
- Plenário do CNJ aprova revisão disciplinar e afastamento de juiz acusado de assédio sexual
- Desembargador será julgado por assédios morais e sexuais cometidos contra servidoras
- Juíza de Santa Catarina recebe pena de censura por violar interesse de criança
- Nota à imprensa: afastamento do desembargador Magid Láuar

**Correspondência com taxonomia antiga (6 meses):** Processos disciplinares / sessões (âncora 'disciplinar')


### Tópico 80 — 21 documentos

**Top-15 termos c-TF-IDF:** torcedor, arenas, estádios, juizado, grandes eventos, juizado torcedor, paz arenas, esportivas, esportivos, eventos, futebol, torcidas, esporte, juizados, torcedor grandes

**Títulos mais representativos:**

- CNJ acompanha ações do Judiciário para reforçar segurança nos estádios
- Encontro Nacional dos Juizados do Torcedor debate desafios e soluções para violência e discriminação nos esportes
- Conselheiros do CNJ conhecem estruturas do Juizado do Torcedor
- GT Paz nas Arenas visita o TJBA e debate propostas para aprimorar a segurança em eventos esportivos
- Encontro Nacional dos Juizados do Torcedor debaterá violência e discriminação nas arenas

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 81 — 26 documentos

**Top-15 termos c-TF-IDF:** precatórios, credores, pagamento, pagamento precatórios, pagamentos, tributária, bilhões, tjse, semana regularização, pagos, alvarás, precatório, trânsito, sergipe, liberação

**Títulos mais representativos:**

- Justiça pernambucana agiliza pagamento de precatórios, só neste ano já foram R$ 186 milhões
- 8ª edição do Mutirão de Precatórios de tribunal do Mato Grosso do Sul movimenta R$ 1,1 milhão
- Tribunal sergipano já pagou mais de R$ 320,6 milhões em precatórios em 2025
- Justiça sergipana pagou mais de R$ 1 bi em precatórios em menos de 2 anos
- TJPR reduz em quatro vezes o tempo para o pagamento de precatórios

**Correspondência com taxonomia antiga (6 meses):** Precatórios / corregedoria (âncora 'precatórios')


### Tópico 82 — 21 documentos

**Top-15 termos c-TF-IDF:** juventudes, diálogos juventudes, estudantes, alunos, diálogos, ensino médio, escolas, escola, projeto diálogos, ensino, barroso, educação cidadania, escolas públicas, democracia, estudantes ensino

**Títulos mais representativos:**

- Oficinas do projeto Diálogos com as Juventudes chegam ao Espírito Santo
- Fortalecimento da educação básica é a ponte para o futuro do Brasil, diz Barroso
- Presidente do STF e do CNJ fala sobre ética e democracia a alunos de escola pública em BH
- Programa do Tribunal de Justiça do Paraná atende mais de 28 mil alunos em 2025
- CNJ, CNMP e MEC fecham acordo para levar conhecimento sobre cidadania e sustentabilidade a escolas públicas

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 83 — 46 documentos

**Top-15 termos c-TF-IDF:** restaurativa, restaurativas, círculos, facilitadores, práticas restaurativas, escolar, construção paz, escolas, paz, ambiente escolar, cultura paz, restaurativos, círculos construção, nejur, conflitos

**Títulos mais representativos:**

- Justiça mineira participa de reunião com CNJ sobre Justiça Restaurativa nas Escolas
- Tribunal maranhense promove fortalecimento da Justiça Restaurativa em escolas
- Tribunal do MS promove formação de facilitadores de Justiça Restaurativa para atuação em escolas
- Justiça Restaurativa: Tribunal do Amapá promove capacitação para docentes da rede pública
- Judiciário lança informativo para fortalecer práticas restaurativas no Maranhão

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 84 — 18 documentos

**Top-15 termos c-TF-IDF:** maternidade, entrega voluntária, gravidez, voluntária, licença maternidade, gestante, gestantes, licença, criança, gravidez adolescência, mães, prevenção gravidez, entrega, médica, candidata

**Títulos mais representativos:**

- Entrega voluntária: CNJ lança cartilha para orientar gestantes e profissionais
- Entrega protegida: Rede de proteção é capacitada sobre o projeto nas comarcas do interior de RO
- Protocolo traz orientações para proteção da maternidade em situação de rua
- Judiciário integra ações intersetoriais na prevenção da gravidez na adolescência
- Protocolo de atendimento a mães que vivem em situação de rua é destaque do Link CNJ

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 85 — 24 documentos

**Top-15 termos c-TF-IDF:** inclusão digital, pid, pids, pontos inclusão, ponto inclusão, comarca, digital, fóruns, fórum digital, fóruns digitais, inclusão, fórum comarca, sede comarca, ponto, digitais

**Títulos mais representativos:**

- Justiça do Pará instala Ponto de Inclusão Digital em Viseu
- Justiça goiana inaugura Ponto de Inclusão Digital na comunidade Vão de Almas
- Tribunal catarinense assina convênio para implantar mais 91 PIDs em cartórios
- Porto Acre recebe a oitava instalação do Ponto de Inclusão Digital no estado
- Santa Rita do Pardo (MS) ganha Ponto de Inclusão Digital para ampliar acesso à Justiça

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 86 — 14 documentos

**Top-15 termos c-TF-IDF:** trabalho decente, decente, trabalho forçado, ouvidoria, precedentes, manifestações, forçado, oit, ouvidoria trt, pedidos informação, pesquisa judiciária, observatório trabalho, pangea, ações coletivas, precedentes qualificados

**Títulos mais representativos:**

- CNJ institui observatório e firma acordo para a construção de política judiciária do trabalho decente
- Tribunal capixaba lança chamada pública para pesquisas empíricas na Justiça do Trabalho
- Conheça o Falcão, o repositório oficial de jurisprudência da Justiça do Trabalho
- Justiça do Trabalho do Piauí inicia pesquisa sobre Metas Nacionais para 2026
- Justiça do Trabalho lança edital de convocação para série “Pesquisa Judiciária Trabalhista”

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 87 — 11 documentos

**Top-15 termos c-TF-IDF:** sessões, sessões virtuais, virtuais, sessão virtual, calendário sessões, calendário, sessões ordinárias, 13h 18h, sessão, haverá sessão, ordinárias, conselheiros conselheiras, semestre, prazos processuais, 13h

**Títulos mais representativos:**

- Confira como o CNJ vai funcionar durante o recesso judiciário e o mês de janeiro
- Calendário das sessões do CNJ no primeiro semestre de 2025 é publicado
- Publicado calendário de sessões do CNJ para o primeiro semestre de 2026
- Plenário do CNJ tem 18 sessões previstas para o 2.º semestre de 2025
- Calendário de sessões do CNJ em 2025 começa no dia 11 de fevereiro

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 88 — 13 documentos

**Top-15 termos c-TF-IDF:** bolsas, ingresso magistratura, fgv, candidatos, programa ações, bolsa, magistratura, indígenas deficiência, negras indígenas, ingresso, afirmativas, ações afirmativas, ação afirmativa, afirmativa, concursos

**Títulos mais representativos:**

- CNJ concederá selo a entidades que contribuem para a diversidade e a inclusão no Judiciário
- CNJ publica novo edital do programa de incentivo à participação de negros e indígenas na magistratura
- Programa de ações afirmativas do CNJ aprova três candidatos à magistratura
- Abertas as inscrições para bolsistas do programa Ações Afirmativas para Ingresso na Magistratura
- Instituições recebem reconhecimento por promover diversidade e inclusão no Judiciário

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 89 — 16 documentos

**Top-15 termos c-TF-IDF:** jornalismo, prêmio qualidade, diamante, autoria, pontuação, prêmio, prata, coautoria, qualidade, premiação, dados tecnologia, categoria, produtividade transparência, corregedoria ética, prêmio corregedoria

**Títulos mais representativos:**

- Tribunal de Roraima conquista o mais alto reconhecimento no Prêmio CNJ de Qualidade
- Prêmio CNJ de Qualidade impulsiona inovação e transparência nos tribunais brasileiros
- Tribunais brasileiros recebem o Prêmio CNJ de Qualidade 2024
- Prêmio CNJ de Qualidade: Justiça do DF conquista Diamante pelo sexto ano consecutivo
- Tribunais recebem Prêmio Corregedoria Ética durante 18.º Encontro Nacional

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 90 — 21 documentos

**Top-15 termos c-TF-IDF:** júri, contra vida, dolosos contra, dolosos, crimes dolosos, homicídio, crimes, julgamento crimes, sessões, julgamento júri, maconha, julgamentos, mapa júri, sessões júri, homicídios

**Títulos mais representativos:**

- Justiça intensifica julgamentos de crimes contra a vida e mira casos antigos e de vulneráveis
- Na Bahia, presidente do CNJ diz que Mapa do Júri é esforço para construir Justiça mais eficiente
- CNJ divulga resultados do Mutirão Processual Penal 2025
- Judiciário se prepara para o Mês Nacional do Júri 2025
- Tribunal do Júri: TJBA dobra meta de audiências em 2025

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 91 — 18 documentos

**Top-15 termos c-TF-IDF:** auditoria, auditoria interna, interna, geração valor, auditorias, prêmio auditoria, auditoria geração, conexão, geração, gestão riscos, fiscalização atos, unidades auditoria, permanente auditoria, tic, experiências disseminação

**Títulos mais representativos:**

- Nova edição do Conexão Auditoria debate fundamentos da Inteligência Artificial
- Conexão Auditoria debate gestão das atividades de auditoria em encontro virtual
- Domicílio Judicial Eletrônico será destaque na 25.ª Reunião de Projetos de TIC
- Encontro promove integração e troca de experiências entre unidades de auditoria do Judiciário
- CNJ promove 4.ª edição do Conexão Auditoria com foco em gestão de competências

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 92 — 20 documentos

**Top-15 termos c-TF-IDF:** distribuídos, plural, 31 12, julgar, meta, distribuídos 31, programa plural, processos distribuídos, trf trf, quilombolas, processos relacionados, distribuídos dezembro, deve julgar, 31, 35 processos

**Títulos mais representativos:**

- Justiça Plural fortalece capacidades do Judiciário em prol de diretos de populações vulneráveis
- CNJ apresenta Programa Justiça Plural ao TJMA
- Protocolo do CNJ orienta atuação do Judiciário em crises socioambientais
- Novo manual reúne diretrizes para garantir direitos da população em situação de rua
- Direitos de indígenas e quilombolas são prioridade nas Metas do Judiciário para 2025

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


### Tópico 93 — 23 documentos

**Top-15 termos c-TF-IDF:** posse, senado, conselheiros, procurador, cerimônia posse, cargo, campbell, desembargadora jaceguara, badaró, botelho, indicados, 7ª região, edson fachin, amorim junior, edson

**Títulos mais representativos:**

- Publicada nomeação de novos conselheiros do CNJ
- CNJ empossa novos representantes da OAB no Conselho
- CNJ realiza solenidade de posse de conselheiras e de conselheiro nesta terça-feira (3/2)
- Presidente do CNJ comemora aprovação de novos integrantes do conselho pelo Senado Federal
- Ministro Mauro Campbell é nomeado novo corregedor nacional da Justiça

**Correspondência com taxonomia antiga (6 meses):** _nenhuma óbvia — decidir do zero._


---
