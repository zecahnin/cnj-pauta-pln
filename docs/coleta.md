# Documentação da Coleta — Fase 1

## Fonte

- **Portal:** Agência CNJ de Notícias — <https://www.cnj.jus.br>
- **API:** WordPress REST API v2 — `https://www.cnj.jus.br/wp-json/wp/v2/posts`
- **Endpoint de categorias:** `https://www.cnj.jus.br/wp-json/wp/v2/categories`

## Conformidade ética e legal

- **robots.txt** (verificado em 2026-06-21): o bloco `User-agent: *` contém
  `Allow: /`. As regras `Disallow` restritivas aplicam-se ao `Googlebot` e a
  caminhos administrativos/sistêmicos (`/wp-admin/`, `*/page/`, `/?page_id=*`).
  O caminho `/wp-json/` **não** é bloqueado. O script valida programaticamente
  `can_fetch` para o nosso *User-agent* e para `*` antes de qualquer coleta
  (`src/collect.py::check_robots`).
- **Rate limit:** ≥ 1,2 s entre requisições (`RATE_LIMIT_SECONDS = 1.2`).
- **Backoff exponencial:** em respostas `429` e `5xx`, com respeito ao header
  `Retry-After` quando presente (2, 4, 8, 16, 32 s; até 5 tentativas).
- **User-agent identificável:** `cnj-pauta-pln/1.0 (pesquisa academica de PLN; ...)`.
- **LGPD:** o conteúdo é jornalístico institucional, de divulgação pública. Não
  se coletam dados pessoais sensíveis; o campo de autoria expõe, na prática,
  apenas o *id* interno do autor da WordPress (conteúdo é institucional, não
  assinado individualmente — ver "Limitações").

## Parâmetros da coleta executada

| Parâmetro | Valor |
|---|---|
| Data de execução | 2026-06-21 |
| Janela temporal | `after=2024-06-21` → `before=2026-06-21` (**~24 meses**) |
| `per_page` | 100 (máximo da API) |
| Paginação | 45 páginas |
| Ordenação | `date desc` |

## Resultado **real** (executado)

- **4.410 notícias** coletadas na janela de 24 meses (`X-WP-Total` da janela =
  baixadas).
- **4.410 ids únicos**, **4.410 urls únicas** → sem duplicatas na coleta.
- **1 registro com `corpo_texto` vazio** (removido na Fase 2).
- Tamanho do corpo bruto (caracteres): mín. 0 (o registro vazio) | mediana 3.129
  | máx. 14.964.
- Intervalo real de publicação: `2024-06-21T08:00:36` → `2026-06-19T12:12:21`.
- Arquivo: `data/raw/noticias.jsonl` (~44 MB).
- Categorias-fonte mapeadas (id → nome) a partir do endpoint de categorias.

> Após a limpeza da Fase 2 (idioma, corpos curtos, dedup MinHash), o corpus cai
> de **4.410 → 4.394 notícias** (16 removidas). Os números das fases seguintes
> usam as **4.394**.

### Distribuição por mês (coleta bruta, 4.410)

| Mês | N | | Mês | N |
|---|---|---|---|---|
| 2024-06 | 46 (janela começa em 21/06) | | 2025-07 | 151 |
| 2024-07 | 175 | | 2025-08 | 221 |
| 2024-08 | 207 | | 2025-09 | 199 |
| 2024-09 | 210 | | 2025-10 | 212 |
| 2024-10 | 213 | | 2025-11 | 209 |
| 2024-11 | 198 | | 2025-12 | 136 |
| 2024-12 | 178 | | 2026-01 | 151 |
| 2025-01 | 110 | | 2026-02 | 136 |
| 2025-02 | 193 | | 2026-03 | 198 |
| 2025-03 | 178 | | 2026-04 | 183 |
| 2025-04 | 180 | | 2026-05 | 176 |
| 2025-05 | 221 | | 2026-06 | 124 (até 19/06) |
| 2025-06 | 205 | | **Total** | **4.410** |

> Os meses extremos (junho/2024 e junho/2026) estão **parciais** — a janela
> começa em 21/06/2024 e termina em 19/06/2026.

### Distribuição por categoria-fonte (corpus bruto)

| Categoria | Notícias |
|---|---|
| Agência CNJ de Notícias | 4.377 |
| Notícias CNJ | 2.413 |
| Notícias do Judiciário | 1.950 |
| Sem categoria | 60 |
| Corte Interamericana de Direitos Humanos (CIDH) | 1 |

> **Observação metodológica:** as categorias-fonte são *grossas* — quase todo o
> acervo cai em 2–3 rótulos genéricos ("Agência CNJ de Notícias", "Notícias CNJ",
> "Notícias do Judiciário"). Isso **justifica a modelagem de tópicos não
> supervisionada**: a taxonomia editorial existente não revela a pauta fina nem
> sua deriva temporal. (Uma notícia pode ter mais de uma categoria, por isso a
> soma excede 4.410.)

## Schema do registro (`data/raw/noticias.jsonl`)

Uma linha JSON por notícia, com os campos:

| Campo | Descrição |
|---|---|
| `id` | id interno da WordPress (chave de dedup) |
| `data_publicacao` | data/hora local de publicação (`date`) |
| `data_publicacao_gmt` | data/hora em GMT (`date_gmt`) |
| `url` | link público (`link`) — segunda chave de dedup |
| `titulo` | título (HTML removido) |
| `categoria_fonte_ids` | ids das categorias |
| `categoria_fonte` | nomes das categorias |
| `corpo_html` | HTML bruto do conteúdo (`content.rendered`) |
| `corpo_texto` | texto extraído (limpeza leve; limpeza pesada na Fase 2) |
| `autoria` | nome do autor se disponível, senão `author_id:<n>` |
| `slug` | slug da URL |
| `modified` | data da última modificação |
| `_coletado_em` | timestamp UTC da coleta (rastreabilidade) |

## Reprodutibilidade

```bash
python src/collect.py --after 2024-06-21 --before 2026-06-21
# ou janela relativa:
python src/collect.py --months 24
# sondagem sem download:
python src/collect.py --dry-run --after 2024-06-21 --before 2026-06-21
```

A coleta é **idempotente**: reexecuções carregam os ids/urls já presentes em
`noticias.jsonl` e só acrescentam registros novos. Como a WP REST API é um alvo
móvel (o acervo cresce e conteúdos podem ser editados), o snapshot coletado é
versionado no git para garantir reprodutibilidade das fases seguintes.

## Limitações conhecidas (resumo; detalhes em `docs/limitacoes.md`)

- A WP REST API retorna apenas o `id` do autor por padrão; a autoria individual
  não é recuperável sem `_embed` por post (não institucionalmente relevante).
- A janela de 24 meses começa em 21/06/2024 e termina em 19/06/2026, então os
  meses extremos estão parciais.
- Conteúdos podem ter sido editados após a publicação (`modified` registrado).
