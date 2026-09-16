# 📌 MVP - SafeFlow

## 🎯 Objetivo do MVP

- **Qual problema resolve?**
  * Transformar os dados históricos de fiscalização em informações geográficas e operacionais que permitam construir um modelo matemático para apoiar o planejamento das equipes do IPEM-SP.

- **Qual hipótese será validada?**
  * Os endereços disponíveis podem ser geocodificados com qualidade suficiente para representar os pontos de fiscalização;
  * É possível construir uma matriz de distâncias e tempos entre os pontos considerados;
  * As capacidades e restrições operacionais podem ser representadas matematicamente;
  * Um modelo implementado em Python pode gerar soluções viáveis para uma instância de teste do problema.

- **Qual valor será entregue ao usuário final?**
  * Uma primeira solução computacional de Pesquisa Operacional, capaz de processar os dados preparados, considerar restrições definidas e gerar resultados que possam ser analisados e aperfeiçoados nas próximas etapas.

---

## 📝 Descrição da Solução

- **Funcionalidades principais incluídas**
  * Geocodificação dos endereços de fiscalização;
  * Representação geográfica dos pontos em um mapa;
  * Construção da matriz de distâncias e tempos;
  * Identificação e documentação das capacidades e restrições operacionais;
  * Definição da função objetivo, variáveis e restrições matemáticas;
  * Implementação do modelo de otimização em Python;
  * Execução de testes com instâncias controladas;
  * Validação da consistência e viabilidade dos resultados.

- **Limitações conhecidas**
  * A qualidade da geocodificação dependerá dos endereços disponíveis;
  * Endereços incompletos ou ambíguos poderão exigir tratamento adicional;
  * As distâncias e os tempos dependerão da metodologia e das fontes utilizadas;
  * Restrições operacionais ainda não confirmadas pelo IPEM-SP deverão ser identificadas como hipóteses;
  * O modelo inicial poderá utilizar uma instância reduzida para permitir testes e validação;
  * A implementação inicial não garante a obtenção de uma solução ótima global em todas as instâncias.

- **Escopo reduzido**
  * A Sprint 02 será dedicada à construção da estrutura geográfica e matemática e à implementação do primeiro modelo funcional. O aperfeiçoamento da distribuição das equipes, a geração dos roteiros finais, o balanceamento da carga, a simulação ampliada de cenários e a comparação completa com o histórico serão tratados na Sprint 03.

---

## 👥 Personas / Usuários-Alvo

**Gestores do IPEM-SP:** responsáveis pelo planejamento e acompanhamento das operações. Necessitam compreender as capacidades e limitações operacionais consideradas pelo modelo para avaliar a viabilidade das soluções propostas.

**Planejadores operacionais:** responsáveis pela organização das fiscalizações. Necessitam de informações geográficas, distâncias, tempos e restrições para apoiar a distribuição das atividades.

**Analistas e desenvolvedores:** responsáveis pela preparação dos dados e implementação do modelo. Necessitam de parâmetros, variáveis, restrições e resultados verificáveis para desenvolver e validar a solução.

> Os perfis representam usuários-alvo previstos e poderão ser refinados conforme a validação com o IPEM-SP.

---

## 🔑 User Stories (Backlog do MVP)

| Rank | Prioridade | Pergunta | User Story | Estimativa |
|------|------------|----------|------------|------------|
| 11 | Alta | Como representar geograficamente os pontos de fiscalização? | Como analista, quero geocodificar os endereços e visualizá-los em um mapa para compreender sua distribuição territorial. | 16h |
| 12 | Alta | Como calcular as distâncias e os tempos entre os pontos? | Como planejador, quero construir uma matriz considerando fiscalizações e bases operacionais para calcular os deslocamentos. | 16h |
| 13 | Alta | Quais capacidades e restrições operacionais devem ser consideradas? | Como gestor, quero definir jornadas, bases, disponibilidade, especializações e limites das equipes para garantir soluções viáveis. | 10h |
| 14 | Alta | Como representar matematicamente o problema de otimização? | Como planejador, quero definir objetivos, variáveis e restrições para formular o problema em Pesquisa Operacional. | 16h |
| 15 | Alta | Como implementar e validar o modelo de otimização? | Como desenvolvedor, quero implementar o modelo em Python e testar seus resultados para gerar soluções consistentes. | 20h |

### 📌 Resumo da Sprint 02

| Indicador | Planejamento |
|-----------|--------------|
| Entrega prevista | 30/10/2026 |
| User Stories planejadas | 5 |
| Prioridade alta | 5 |
| Esforço total estimado | 78 horas |
| Objetivo da entrega | Primeiro modelo matemático funcional |

> As estimativas representam o esforço total previsto da equipe e poderão ser revisadas durante a execução.

---

## 📅 Sprint(s) Relacionadas

| Sprint | Entregas Principais | Status |
|--------|--------------------|--------|
| 02 | Geocodificação e representação dos pontos de fiscalização | Não iniciada |
| 02 | Construção da matriz de distâncias e tempos | Não iniciada |
| 02 | Definição das capacidades e restrições operacionais | Não iniciada |
| 02 | Formulação do modelo matemático | Não iniciada |
| 02 | Implementação e validação inicial em Python | Não iniciada |

---

## 📊 Critérios de Aceitação

- [ ] Os endereços foram submetidos a um processo documentado de geocodificação;
- [ ] Os pontos geocodificados podem ser visualizados em um mapa;
- [ ] Endereços não localizados ou ambíguos foram identificados;
- [ ] A matriz de distâncias e tempos foi construída e possui metodologia documentada;
- [ ] Os pontos e as bases operacionais considerados na matriz estão identificados;
- [ ] As capacidades e restrições operacionais foram documentadas, distinguindo informações confirmadas de hipóteses;
- [ ] A função objetivo, as variáveis, os parâmetros e as restrições do modelo foram definidos;
- [ ] O modelo matemático foi implementado em Python;
- [ ] O modelo pode ser executado com uma instância de teste documentada;
- [ ] Os resultados foram verificados quanto ao atendimento das restrições implementadas;
- [ ] As limitações e eventuais problemas encontrados durante os testes foram registrados;
- [ ] O código e as decisões técnicas foram documentados no repositório.

> A Sprint 02 será considerada concluída após a execução dos testes, o atendimento dos critérios aplicáveis e a validação dos resultados pela equipe.

---

## 📈 Métricas de Validação

**Qualidade da geocodificação**
  * Quantidade de endereços processados;
  * Quantidade e percentual de endereços geocodificados;
  * Quantidade de endereços não localizados ou ambíguos;
  * Quantidade de pontos utilizados na matriz de deslocamentos.

**Validação do modelo**
  * Quantidade de pontos e equipes considerados na instância de teste;
  * Quantidade de restrições implementadas;
  * Quantidade de testes executados;
  * Quantidade de soluções viáveis encontradas;
  * Tempo de execução do modelo;
  * Valor da função objetivo obtido, com unidade e significado documentados.

**Validação do MVP**
  * Verificação do atendimento às restrições implementadas;
  * Validação dos resultados pela equipe;
  * Feedback do professor e/ou cliente após a apresentação;
  * Problemas e ajustes identificados durante os testes.

---

## 🚀 Próximos Passos

  * Aperfeiçoar a distribuição das fiscalizações entre as equipes;
  * Gerar e analisar as sequências de visitas;
  * Incorporar o balanceamento da carga de trabalho;
  * Simular diferentes cenários operacionais;
  * Comparar os resultados otimizados com o cenário histórico;
  * Consolidar os indicadores, o dashboard comparativo e a documentação final.

---

## 📂 Anexos / Evidências

- 🔗 **Vídeo:**  
  [ADICIONAR LINK, SE APLICÁVEL]

- 📄 **Documentação do modelo matemático:**  
  [ADICIONAR LINK]

- 🗺️ **Mapa / Geocodificação:**  
  [ADICIONAR LINK]

- 📊 **Matriz de distâncias e tempos:**  
  [ADICIONAR LINK]

- 💻 **Código / Scripts:**  
  [ADICIONAR LINK]

- 🧪 **Testes e resultados do modelo:**  
  [ADICIONAR LINK]

---
