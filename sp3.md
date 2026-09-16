# 📌 MVP - SafeFlow

## 🎯 Objetivo do MVP

- **Qual problema resolve?**
  * Aperfeiçoar o planejamento das fiscalizações do IPEM-SP por meio da otimização da distribuição das equipes e da sequência de visitas, permitindo comparar os resultados gerados com a operação histórica.

- **Qual hipótese será validada?**
  * O modelo matemático desenvolvido pode gerar uma distribuição viável das fiscalizações entre as equipes;
  * A otimização pode reduzir a distância geográfica aproximada total em relação a um cenário histórico reconstruído sob a mesma metodologia;
  * É possível melhorar o balanceamento da carga de trabalho respeitando as restrições operacionais consideradas;
  * Diferentes configurações de equipes e capacidades podem produzir resultados distintos;
  * Os indicadores permitem identificar os benefícios e as limitações da solução proposta.

- **Qual valor será entregue ao usuário final?**
  * Uma solução de apoio ao planejamento das fiscalizações, capaz de gerar cenários otimizados, apresentar indicadores comparativos e disponibilizar informações para avaliar alternativas de distribuição das equipes e organização dos roteiros.

---

## 📝 Descrição da Solução

- **Funcionalidades principais incluídas**
  * Otimização da distribuição das fiscalizações entre as equipes;
  * Geração de sequências de visitas para cada equipe;
  * Análise e balanceamento da carga de trabalho;
  * Simulação de diferentes cenários operacionais;
  * Comparação entre os cenários histórico e otimizado;
  * Cálculo de indicadores de distância geográfica aproximada, carga de trabalho, cobertura e atendimentos;
  * Desenvolvimento do dashboard comparativo;
  * Consolidação da documentação técnica e dos resultados;
  * Preparação das evidências e da apresentação final.

- **Limitações conhecidas**
  * As distâncias geográficas aproximadas não representam necessariamente os trajetos rodoviários reais;
  * Não será possível afirmar reduções reais de tempo de viagem sem dados ou metodologia adicional para estimá-lo;
  * A comparação dependerá da possibilidade de reconstruir os roteiros históricos com os dados disponíveis;
  * Restrições operacionais não confirmadas deverão permanecer identificadas como hipóteses;
  * Os resultados dependerão da qualidade dos dados, da formulação matemática e das configurações do solucionador;
  * Uma solução viável não representa necessariamente uma solução ótima global;
  * A utilização operacional da solução dependerá de validação pelo IPEM-SP.

- **Escopo reduzido**
  * A Sprint 03 será dedicada à conclusão e validação da solução desenvolvida nas etapas anteriores. O foco será gerar cenários otimizados, comparar indicadores e consolidar os resultados. Não estão previstos implantação em produção, integração com sistemas internos do IPEM-SP ou acompanhamento de equipes em tempo real.

---

## 👥 Personas / Usuários-Alvo

**Gestores do IPEM-SP:** responsáveis pelo planejamento e acompanhamento das operações de fiscalização. Necessitam comparar cenários, avaliar a distribuição da carga de trabalho e compreender os resultados e as limitações da otimização.

**Planejadores operacionais:** responsáveis pela organização das fiscalizações. Necessitam consultar a distribuição das atividades, as sequências de visitas e os cenários gerados para apoiar o planejamento das equipes.

**Analistas e desenvolvedores:** responsáveis pela implementação, validação e manutenção da solução. Necessitam consultar os parâmetros, indicadores, testes e resultados para verificar o funcionamento do modelo.

> Os perfis representam usuários-alvo previstos e poderão ser refinados conforme a validação com o IPEM-SP.

---

## 🔑 User Stories (Backlog do MVP)

| Rank | Prioridade | Pergunta | User Story | Estimativa |
|------|------------|----------|------------|------------|
| 16 | Alta | Qual é a melhor distribuição das fiscalizações entre as equipes? | Como planejador, quero agrupar e distribuir as fiscalizações para reduzir deslocamentos e melhorar a utilização das equipes. | 16h |
| 17 | Alta | Qual é a melhor sequência de visitas para cada equipe? | Como planejador, quero gerar roteiros otimizados para reduzir quilômetros e tempo de deslocamento. | 20h |
| 18 | Alta | Como equilibrar a carga de trabalho no cenário otimizado? | Como gestor, quero distribuir as atividades considerando visitas, instrumentos, tempo e deslocamento para evitar desequilíbrios. | 10h |
| 19 | Média | Como diferentes cenários afetam o planejamento das equipes? | Como planejador, quero simular mudanças na quantidade de equipes, capacidade e restrições para avaliar alternativas operacionais. | 12h |
| 20 | Alta | Quais ganhos são obtidos ao comparar os cenários histórico e otimizado? | Como gestor, quero comparar distância, tempo, carga, cobertura e atendimentos para avaliar os benefícios e as limitações da otimização. | 16h |

### 📌 Resumo da Sprint 03

| Indicador | Planejamento |
|-----------|--------------|
| Entrega prevista | 27/11/2026 |
| User Stories planejadas | 5 |
| Prioridade alta | 4 |
| Prioridade média | 1 |
| Esforço total estimado | 74 horas |
| Objetivo da entrega | Otimização, comparação e validação final |

> As estimativas representam o esforço total previsto da equipe e poderão ser revisadas durante a execução.

---

## 📅 Sprint(s) Relacionadas

| Sprint | Entregas Principais | Status |
|--------|--------------------|--------|
| 03 | Otimização da distribuição das fiscalizações | Não iniciada |
| 03 | Geração das sequências de visitas | Não iniciada |
| 03 | Balanceamento da carga de trabalho | Não iniciada |
| 03 | Simulação de cenários operacionais | Não iniciada |
| 03 | Comparação dos resultados e consolidação da entrega final | Não iniciada |

---

## 📊 Critérios de Aceitação

- [ ] O modelo gera uma distribuição das fiscalizações entre as equipes;
- [ ] As soluções geradas são verificadas quanto ao atendimento das restrições implementadas;
- [ ] As sequências de visitas são geradas e podem ser consultadas;
- [ ] A distância geográfica aproximada total é calculada com metodologia documentada;
- [ ] A carga de trabalho pode ser comparada entre as equipes;
- [ ] O balanceamento considera os parâmetros operacionais definidos;
- [ ] O sistema permite executar e comparar diferentes cenários;
- [ ] Os cenários histórico e otimizado são comparados utilizando critérios e unidades compatíveis;
- [ ] As diferenças entre os cenários são apresentadas por meio de indicadores;
- [ ] O dashboard comparativo permite visualizar os principais resultados;
- [ ] As limitações da comparação são documentadas;
- [ ] O código, os testes e as decisões técnicas estão documentados;
- [ ] O relatório técnico e as evidências da entrega foram consolidados.

> A Sprint 03 será considerada concluída após o atendimento dos critérios aplicáveis, a execução dos testes e a validação dos resultados pela equipe.

---

## 📈 Métricas de Validação

**Desempenho da otimização**
  * Distância geográfica aproximada total por cenário;
  * Diferença absoluta e percentual de distância entre os cenários;
  * Quantidade de fiscalizações distribuídas;
  * Quantidade de atendimentos por equipe;
  * Quantidade de equipes utilizadas;
  * Tempo de execução do modelo;
  * Situação da solução encontrada: viável, ótima comprovada ou sem solução viável, conforme o retorno do solucionador.

**Balanceamento e cobertura**
  * Quantidade de visitas e instrumentos por equipe;
  * Distribuição da carga de trabalho;
  * Diferença de carga entre as equipes;
  * Quantidade de municípios atendidos;
  * Quantidade de fiscalizações não atribuídas, quando aplicável.

**Comparação dos cenários**
  * Indicadores históricos e otimizados calculados com metodologia compatível;
  * Diferenças absolutas e percentuais dos indicadores comparáveis;
  * Restrições atendidas em cada cenário;
  * Limitações e hipóteses consideradas na comparação.

**Validação do MVP**
  * Quantidade de testes executados;
  * Verificação das restrições implementadas;
  * Validação dos resultados pela equipe;
  * Feedback do professor e/ou cliente;
  * Ajustes identificados durante a homologação.

> Os indicadores de tempo de deslocamento somente serão apresentados se houver dados ou metodologia adicional que permita estimá-los de forma documentada.

---

## 🚀 Próximos Passos

  * Apresentar os resultados finais ao professor e ao IPEM-SP;
  * Registrar o feedback e as limitações identificadas;
  * Consolidar o relatório técnico e a documentação do projeto;
  * Preparar o vídeo da terceira entrega;
  * Preparar a apresentação para a Feira de Soluções de 03/12/2026.

---

## 📂 Anexos / Evidências

- 🔗 **Vídeo da entrega final:**  
  [ADICIONAR LINK]

- 📄 **Relatório técnico:**  
  [ADICIONAR LINK]

- 🗺️ **Rotas e cenários otimizados:**  
  [ADICIONAR LINK]

- 📊 **Dashboard comparativo:**  
  [ADICIONAR LINK]

- 💻 **Código / Scripts:**  
  [ADICIONAR LINK]

- 🧪 **Testes e resultados:**  
  [ADICIONAR LINK]

- 🎓 **Apresentação final:**  
  [ADICIONAR LINK]

---
