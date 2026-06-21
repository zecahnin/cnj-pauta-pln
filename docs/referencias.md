# Referências

DOIs verificados por resolução em `doi.org` (junho/2026), confirmando o
redirecionamento ao registro do editor correto. Divididas em **domínio**
(agenda-setting, comunicação institucional, modelagem de tópicos sobre notícias,
PLN jurídico em português) e **técnica** (métodos de PLN/ML empregados no
pipeline). As poucas obras sem DOI (livro/JMLR) são citadas com a URL canônica e
sinalizadas explicitamente.

## Domínio (6)

1. **McCombs, M. E., & Shaw, D. L. (1972).** The Agenda-Setting Function of Mass
   Media. *Public Opinion Quarterly*, 36(2), 176–187.
   DOI: [10.1086/267990](https://doi.org/10.1086/267990)
   — Fundamento teórico para "deriva de pauta": como a mídia define a saliência
   relativa dos temas. Aqui, aplicado à comunicação institucional do CNJ.

2. **DiMaggio, P., Nag, M., & Blei, D. (2013).** Exploiting affinities between
   topic modeling and the sociological perspective on culture: Application to
   newspaper coverage of U.S. government arts funding. *Poetics*, 41(6), 570–606.
   DOI: [10.1016/j.poetic.2013.08.004](https://doi.org/10.1016/j.poetic.2013.08.004)
   — Referência seminal de uso de modelagem de tópicos sobre cobertura
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
   postura de validação (rótulos fracos + gold set humano) adotada na Fase 6.

5. **Luz de Araujo, P. H., de Campos, T. E., de Oliveira, R. R. R., Stauffer, M.,
   Couto, S., & Bermejo, P. (2018).** LeNER-Br: A Dataset for Named Entity
   Recognition in Brazilian Legal Text. In *Computational Processing of the
   Portuguese Language (PROPOR 2018)*, LNCS vol. 11122, 313–323. Springer.
   DOI: [10.1007/978-3-319-99722-3_32](https://doi.org/10.1007/978-3-319-99722-3_32)
   — NER em texto jurídico brasileiro; ancora a Fase 6b (extração de entidades em
   pt-BR no domínio da Justiça).

6. **Lage-Freitas, A., Allende-Cid, H., Santana, O., & Oliveira-Lage, L. (2022).**
   Predicting Brazilian Court Decisions. *PeerJ Computer Science*, 8, e904.
   DOI: [10.7717/peerj-cs.904](https://doi.org/10.7717/peerj-cs.904)
   — PLN jurídico em português com classificadores e Deep Learning; precedente de
   domínio para a classificação supervisionada da Fase 6.

## Técnica (11 + 2 sem DOI)

7. **Salton, G., & Buckley, C. (1988).** Term-weighting approaches in automatic
   text retrieval. *Information Processing & Management*, 24(5), 513–523.
   DOI: [10.1016/0306-4573(88)90021-0](https://doi.org/10.1016/0306-4573(88)90021-0)
   — Fundamento do **TF-IDF**, base das features de Bag-of-Words dos
   classificadores (Modelos A e B da Fase 6).

8. **Manning, C. D., Raghavan, P., & Schütze, H. (2008).** *Introduction to
   Information Retrieval.* Cambridge University Press.
   DOI: [10.1017/CBO9780511809071](https://doi.org/10.1017/CBO9780511809071)
   — Texto-base de **Bag-of-Words, TF-IDF e Naive Bayes** para classificação de
   texto (Modelo A, baseline).

9. **Grootendorst, M. (2022).** BERTopic: Neural topic modeling with a class-based
   TF-IDF procedure. *arXiv preprint*.
   DOI: [10.48550/arXiv.2203.05794](https://doi.org/10.48550/arXiv.2203.05794)
   — Método central da Fase 4 (embeddings → UMAP → HDBSCAN → c-TF-IDF).

10. **Reimers, N., & Gurevych, I. (2019).** Sentence-BERT: Sentence Embeddings
    using Siamese BERT-Networks. In *EMNLP-IJCNLP 2019*.
    DOI: [10.18653/v1/D19-1410](https://doi.org/10.18653/v1/D19-1410)
    — Base dos *sentence embeddings* (modelo `paraphrase-multilingual-mpnet`) da
    descoberta exploratória.

11. **McInnes, L., Healy, J., Saul, N., & Großberger, L. (2018).** UMAP: Uniform
    Manifold Approximation and Projection. *Journal of Open Source Software*,
    3(29), 861.
    DOI: [10.21105/joss.00861](https://doi.org/10.21105/joss.00861)
    — Redução de dimensionalidade antes da clusterização (Fase 4).

12. **McInnes, L., Healy, J., & Astels, S. (2017).** hdbscan: Hierarchical density
    based clustering. *Journal of Open Source Software*, 2(11), 205.
    DOI: [10.21105/joss.00205](https://doi.org/10.21105/joss.00205)
    — Clusterização por densidade que define os tópicos e identifica outliers.

13. **Röder, M., Both, A., & Hinneburg, A. (2015).** Exploring the Space of Topic
    Coherence Measures. In *WSDM '15*, 399–408.
    DOI: [10.1145/2684822.2685324](https://doi.org/10.1145/2684822.2685324)
    — Define a coerência **c_v** usada para selecionar `min_topic_size` na Fase 4.

14. **Vaswani, A., et al. (2017).** Attention Is All You Need. *arXiv preprint*
    (NeurIPS 2017).
    DOI: [10.48550/arXiv.1706.03762](https://doi.org/10.48550/arXiv.1706.03762)
    — Arquitetura **Transformer**, base do BERT/BERTimbau (Modelo C e NER).

15. **Devlin, J., Chang, M.-W., Lee, K., & Toutanova, K. (2019).** BERT:
    Pre-training of Deep Bidirectional Transformers for Language Understanding.
    In *NAACL-HLT 2019*, 4171–4186.
    DOI: [10.18653/v1/N19-1423](https://doi.org/10.18653/v1/N19-1423)
    — **BERT**, fundamento dos embeddings contextuais usados na Fase 6/6b.

16. **Souza, F., Nogueira, R., & Lotufo, R. (2020).** BERTimbau: Pretrained BERT
    Models for Brazilian Portuguese. In *Intelligent Systems (BRACIS 2020)*,
    LNCS vol. 12319, 403–417. Springer.
    DOI: [10.1007/978-3-030-61377-8_28](https://doi.org/10.1007/978-3-030-61377-8_28)
    — **BERTimbau**, o transformer de pt-BR usado como Modelo C da classificação.

17. **Kingma, D. P., & Ba, J. (2015).** Adam: A Method for Stochastic
    Optimization. In *ICLR 2015* (*arXiv:1412.6980*).
    DOI: [10.48550/arXiv.1412.6980](https://doi.org/10.48550/arXiv.1412.6980)
    — Otimizador **Adam** usado no treino da MLP (Modelo B).

**Sem DOI (citadas pela URL canônica — honestidade de fonte):**

18. **Srivastava, N., Hinton, G., Krizhevsky, A., Sutskever, I., &
    Salakhutdinov, R. (2014).** Dropout: A Simple Way to Prevent Neural Networks
    from Overfitting. *Journal of Machine Learning Research*, 15, 1929–1958.
    URL: <https://jmlr.org/papers/v15/srivastava14a.html> *(JMLR não emite DOI.)*
    — Fundamento do **Dropout** estudado na análise de overfit/regularização da
    Fase 6.

19. **Goodfellow, I., Bengio, Y., & Courville, A. (2016).** *Deep Learning.*
    MIT Press. URL: <https://www.deeplearningbook.org> *(livro; sem DOI.)*
    — Texto-base de redes neurais profundas, overfit/underfit, regularização e
    otimização (Módulo 2 do curso).

---

### Observação sobre integridade

Todos os DOIs acima foram **verificados** resolvendo `https://doi.org/<doi>` e
confirmando o redirecionamento ao editor correto (Cambridge, Springer, Elsevier,
PeerJ, JOSS, ACM, Oxford/POQ, Taylor & Francis, ACL Anthology, arXiv). As duas
obras sem DOI (Dropout/JMLR e *Deep Learning*/MIT Press) não possuem DOI emitido
e são citadas pela URL canônica. **Nenhuma referência foi inventada.**
