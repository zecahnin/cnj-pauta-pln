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
| Janela temporal | `after=2025-12-21` → `before=2026-06-21` (6 meses) |
| `per_page` | 100 (máximo da API) |
| Paginação | 10 páginas |
| Ordenação | `date desc` |

## Resultado **real** (executado)

- **983 notícias** coletadas (`X-WP-Total` da janela = 983; baixadas = 983).
- **983 ids únicos**, **983 urls únicas** → sem duplicatas.
- **0 registros com `corpo_texto` vazio.**
- Tamanho do corpo (caracteres): mín. 224 | mediana 3.116 | máx. 10.619.
- Intervalo real de publicação: `2025-12-22T08:00:13` → `2026-06-19T13:02:35`.
- Arquivo: `data/raw/noticias.jsonl` (~8,9 MB).
- **288 categorias** mapeadas (id → nome) a partir do endpoint de categorias.

### Distribuição por mês

| Mês | Notícias |
|---|---|
| 2025-12 | 15 (janela começa em 21/12) |
| 2026-01 | 151 |
| 2026-02 | 136 |
| 2026-03 | 198 |
| 2026-04 | 183 |
| 2026-05 | 176 |
| 2026-06 | 124 (até 19/06) |

### Distribuição por categoria-fonte (top)

| Categoria | Notícias |
|---|---|
| Agência CNJ de Notícias | 977 |
| Notícias CNJ | 615 |
| Notícias do Judiciário | 344 |
| Sem categoria (rótulo "Sem categoria") | 17 |
| Corte Interamericana de Direitos Humanos (CIDH) | 1 |

> **Observação metodológica:** as categorias-fonte são *grossas* — quase todo o
> acervo cai em 2–3 rótulos genéricos ("Agência CNJ de Notícias", "Notícias CNJ",
> "Notícias do Judiciário"). Isso **justifica a modelagem de tópicos não
> supervisionada**: a taxonomia editorial existente não revela a pauta fina nem
> sua deriva temporal. (Uma notícia pode ter mais de uma categoria, por isso a
> soma excede 983.)

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
python src/collect.py --after 2025-12-21 --before 2026-06-21
# ou janela relativa:
python src/collect.py --months 6
# sondagem sem download:
python src/collect.py --dry-run --after 2025-12-21 --before 2026-06-21
```

A coleta é **idempotente**: reexecuções carregam os ids/urls já presentes em
`noticias.jsonl` e só acrescentam registros novos. Como a WP REST API é um alvo
móvel (o acervo cresce e conteúdos podem ser editados), o snapshot coletado é
versionado no git para garantir reprodutibilidade das fases seguintes.

## Limitações conhecidas (resumo; detalhes em `docs/limitacoes.md`)

- A WP REST API retorna apenas o `id` do autor por padrão; a autoria individual
  não é recuperável sem `_embed` por post (não institucionalmente relevante).
- A janela de 6 meses começa em 21/12, então dezembro/2025 está parcial.
- Conteúdos podem ter sido editados após a publicação (`modified` registrado).
