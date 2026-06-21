# Referências

DOIs verificados por resolução em `doi.org` (junho/2026). Divididas em
referências de **domínio** (comunicação institucional, agenda-setting,
modelagem de tópicos aplicada a notícias/cultura) e de **técnica** (métodos de
PLN empregados no pipeline).

## Domínio (5)

1. **McCombs, M. E., & Shaw, D. L. (1972).** The Agenda-Setting Function of Mass
   Media. *Public Opinion Quarterly*, 36(2), 176–187.
   DOI: [10.1086/267990](https://doi.org/10.1086/267990)
   — Fundamento teórico para "deriva de pauta": como a mídia define a saliência
   relativa dos temas. Aqui, aplicado à comunicação institucional do CNJ.

2. **DiMaggio, P., Nag, M., & Blei, D. (2013).** Exploiting affinities between
   topic modeling and the sociological perspective on culture: Application to
   newspaper coverage of U.S. government arts funding. *Poetics*, 41(6), 570–606.
   DOI: [10.1016/j.poetic.2013.08.004](https://doi.org/10.1016/j.poetic.2013.08.004)
   — Referência seminal de uso de modelagem de tópicos (LDA) sobre cobertura
   jornalística para revelar enquadramentos e diferenças entre fontes.

3. **Jacobi, C., van Atteveldt, W., & Welbers, K. (2016).** Quantitative analysis
   of large amounts of journalistic texts using topic modelling.
   *Digital Journalism*, 4(1), 89–106.
   DOI: [10.1080/21670811.2015.1093271](https://doi.org/10.1080/21670811.2015.1093271)
   — Guia metodológico de modelagem de tópicos para grandes acervos de textos
   jornalísticos, incluindo análise temporal — diretamente análogo a este projeto.

4. **Grimmer, J., & Stewart, B. M. (2013).** Text as Data: The Promise and
   Pitfalls of Automatic Content Analysis Methods for Political Texts.
   *Political Analysis*, 21(3), 267–297.
   DOI: [10.1093/pan/mps028](https://doi.org/10.1093/pan/mps028)
   — Boas práticas e armadilhas da análise automática de conteúdo; embasa a
   postura de validação (rótulos fracos + gold set) adotada na Fase 6.

5. **Souza, F., Nogueira, R., & Lotufo, R. (2020).** BERTimbau: Pretrained BERT
   Models for Brazilian Portuguese. In *Intelligent Systems (BRACIS 2020)*,
   LNCS vol. 12319, 403–417. Springer.
   DOI: [10.1007/978-3-030-61377-8_28](https://doi.org/10.1007/978-3-030-61377-8_28)
   — Referência de PLN para português do Brasil; contextualiza as escolhas de
   modelos para pt-BR (alternativa nacional ao embedding multilíngue usado).

## Técnica (5)

6. **Grootendorst, M. (2022).** BERTopic: Neural topic modeling with a
   class-based TF-IDF procedure. *arXiv preprint*.
   DOI: [10.48550/arXiv.2203.05794](https://doi.org/10.48550/arXiv.2203.05794)
   — Método central da Fase 4 (embeddings → UMAP → HDBSCAN → c-TF-IDF).

7. **Reimers, N., & Gurevych, I. (2019).** Sentence-BERT: Sentence Embeddings
   using Siamese BERT-Networks. In *EMNLP-IJCNLP 2019*.
   DOI: [10.18653/v1/D19-1410](https://doi.org/10.18653/v1/D19-1410)
   — Base dos *sentence embeddings* (modelo `paraphrase-multilingual-mpnet`).

8. **McInnes, L., Healy, J., Saul, N., & Großberger, L. (2018).** UMAP: Uniform
   Manifold Approximation and Projection. *Journal of Open Source Software*,
   3(29), 861.
   DOI: [10.21105/joss.00861](https://doi.org/10.21105/joss.00861)
   — Redução de dimensionalidade antes da clusterização.

9. **McInnes, L., Healy, J., & Astels, S. (2017).** hdbscan: Hierarchical density
   based clustering. *Journal of Open Source Software*, 2(11), 205.
   DOI: [10.21105/joss.00205](https://doi.org/10.21105/joss.00205)
   — Clusterização por densidade que define os tópicos e identifica outliers.

10. **Röder, M., Both, A., & Hinneburg, A. (2015).** Exploring the Space of Topic
    Coherence Measures. In *WSDM '15*, 399–408.
    DOI: [10.1145/2684822.2685324](https://doi.org/10.1145/2684822.2685324)
    — Define a coerência **c_v** usada para selecionar `min_topic_size` na Fase 4.

---

### Observação sobre integridade

Todos os 10 DOIs foram verificados resolvendo `https://doi.org/<doi>` e
confirmando o redirecionamento ao registro do editor correto (Springer, JOSS,
Elsevier/Poetics, Taylor & Francis/Digital Journalism, ACM, Oxford/POQ,
ACL Anthology, arXiv). Nenhuma referência foi inventada.
