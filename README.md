# 📌 SafeFlowFlowSafeGeometry

Projeto desenvolvido no 3º semestre do curso de Logística da Fatec São José dos Campos, no contexto da Aprendizagem por Projetos Integradores (API).

O SafeFlow tem como objetivo analisar os dados históricos da regional do IPEM-SP de São José dos Campos e aplicar conceitos de Pesquisa Operacional para melhorar a distribuição das fiscalizações, reduzir deslocamentos e equilibrar a carga de trabalho entre as equipes.

---

# 📑 Índice

- [Projeto](#projeto)
- [Equipe](#equipe)
- [Objetivo](#objetivo)
- [Questões para análise](#questoes)
- [Funcionalidades](#funcionalidades)
- [Requisitos](#requisitos)
- [Tecnologias](#tecnologias)
- [Backlog do produto](#backlog)
- [Indicadores](#indicadores)
- [Fluxo do projeto](#fluxo)
- [Registro das Sprints](#sprints)

---

<a name="projeto"></a>

# 📊 Projeto

O IPEM-SP realiza a verificação e a fiscalização de instrumentos de medição, incluindo balanças comerciais, bombas de combustível e outros equipamentos regulamentados.

O projeto será desenvolvido em duas etapas:

1. **Análise histórica:** tratamento dos dados e estudo da distribuição das equipes, dos municípios atendidos, dos tipos de fiscalização, da carga de trabalho e dos resultados obtidos;
2. **Otimização:** construção de um modelo matemático para propor uma distribuição mais eficiente das fiscalizações e comparar o novo cenário com a operação histórica.

A proposta busca utilizar dados, indicadores e Pesquisa Operacional para apoiar o planejamento das equipes da regional de São José dos Campos.

---

<a name="equipe"></a>

# 👥 Equipe

| Função | Nome | LinkedIn e GitHub |
|--------|------|-------------------|
| Product Owner | Ana Clara Dias | [LinkedIn](http://linkedin.com/in/ana-clara-dias-de-souza-927431179) \| [GitHub](https://github.com/AninhaDias) |
| Team Member | Kauan Souza | [LinkedIn](https://linkedin.com/in/kauan-souza-9247aa377) \| [GitHub](https://github.com/kauanzcsouza10-art) |
| Team Member | Davi Pais | [LinkedIn](https://linkedin.com/in/davi-pais-340989359) \| [GitHub](https://github.com/DaviPaisKitada) |
| Team Member | Mariana Leal | [LinkedIn](https://linkedin.com/in/mariana-leal-a708b8335) \| [GitHub](https://github.com/marileal071415-create) |

---

<a name="objetivo"></a>

# 🎯 Objetivo

Desenvolver uma solução baseada em Pesquisa Operacional para:

- Analisar a operação histórica;
- Melhorar a distribuição das fiscalizações;
- Reduzir deslocamentos e tempo de viagem;
- Balancear a carga de trabalho;
- Comparar os cenários histórico e otimizado.

---

<a name="questoes"></a>

# ❓ Questões para Análise

As questões foram divididas entre a compreensão da operação histórica e a construção do cenário otimizado.

## 📊 Análise do histórico

1. Como preparar e validar a base histórica?
2. Como fiscais e motoristas foram distribuídos?
3. Como a carga de trabalho foi distribuída entre as equipes?
4. Quais municípios concentraram a maior demanda?
5. Quais serviços e instrumentos foram mais frequentes?
6. Quais resultados e irregularidades foram encontrados?
7. Como a demanda variou ao longo do período?
8. Qual foi o perfil dos roteiros históricos?
9. Quais indicadores representam o desempenho histórico?
10. Como visualizar e disponibilizar os resultados?

## 🧮 Otimização da operação

11. Como representar geograficamente as fiscalizações?
12. Como calcular as distâncias e os tempos entre os pontos?
13. Quais capacidades e restrições devem ser consideradas?
14. Como formular matematicamente o problema?
15. Como implementar e validar o modelo de otimização?
16. Qual é a melhor distribuição das fiscalizações?
17. Qual é a melhor sequência de visitas para cada equipe?
18. Como equilibrar a carga de trabalho?
19. Como diferentes cenários afetam o planejamento?
20. Quais ganhos são obtidos em relação ao cenário histórico?

---

<a name="funcionalidades"></a>

# ⚙️ Funcionalidades

A solução deverá contemplar:

- 🧹 Tratamento e validação dos dados;
- 📊 Análise da operação histórica;
- 🗺️ Mapa das fiscalizações;
- 🚗 Rotas históricas e otimizadas;
- ⚖️ Análise da carga de trabalho;
- 🧮 Otimização da distribuição das equipes;
- 🔄 Simulação de cenários;
- 📈 Dashboard histórico e comparativo;
- 📄 Exportação de relatórios.

> As funcionalidades serão desenvolvidas progressivamente durante as Sprints.

---

<a name="requisitos"></a>

# 📋 Requisitos

| Código | Requisito |
|--------|-----------|
| RN.P.1 | Tratar, padronizar e validar os dados históricos |
| RN.P.2 | Diferenciar instrumentos, visitas e roteiros |
| RN.P.3 | Analisar equipes, demanda, carga e resultados |
| RN.P.4 | Geocodificar os pontos de fiscalização |
| RN.P.5 | Construir a matriz de distâncias e tempos |
| RN.P.6 | Definir as capacidades e restrições operacionais |
| RN.P.7 | Formular o modelo matemático de otimização |
| RN.P.8 | Implementar e validar o modelo em Python |
| RN.P.9 | Construir e simular cenários otimizados |
| RN.P.10 | Comparar os cenários por meio de indicadores |
| RN.P.11 | Desenvolver o dashboard |
| RN.P.12 | Exportar os resultados e elaborar o relatório técnico |

---

<a name="tecnologias"></a>

# 🛠 Tecnologias Previstas

- **Python e Pandas** — tratamento e análise dos dados;
- **OR-Tools ou Pyomo** — modelagem e otimização;
- **Serviço de geocodificação** — conversão dos endereços em coordenadas;
- **Matriz de distâncias e tempos** — cálculo dos deslocamentos;
- **BI** — dashboards histórico e comparativo;
- **GitHub** — versionamento e documentação;
- **Office** — apresentações e relatório técnico.

> As ferramentas definitivas de geocodificação, otimização e visualização serão escolhidas durante o desenvolvimento.

---

<a name="backlog"></a>

# 🗂 Backlog do Produto

O backlog foi estruturado em 20 questões centrais, divididas igualmente entre a análise histórica e a otimização da operação.

A primeira etapa busca compreender como as fiscalizações foram realizadas. A segunda utiliza os resultados históricos para propor, simular e avaliar uma distribuição otimizada das atividades.

## 📊 Análise do histórico

| Rank | Prioridade | Pergunta | User Story | Estimativa | Sprint |
|-----:|------------|----------|------------|------------|--------|
| 1 | Alta | Como preparar e validar a base histórica para análise? | Como analista, quero tratar, padronizar e validar os dados, diferenciando instrumentos, visitas e roteiros, para garantir resultados confiáveis. | [DEFINIR] | [DEFINIR] |
| 2 | Alta | Como fiscais e motoristas foram distribuídos historicamente? | Como gestor, quero visualizar a formação das equipes e os roteiros realizados para compreender como os profissionais foram distribuídos. | [DEFINIR] | [DEFINIR] |
| 3 | Alta | Como a carga de trabalho foi distribuída entre as equipes? | Como gestor, quero comparar roteiros, visitas e instrumentos por equipe para identificar sobrecarga ou subutilização. | [DEFINIR] | [DEFINIR] |
| 4 | Alta | Quais municípios concentraram a maior demanda? | Como planejador, quero analisar visitas e instrumentos por município para identificar a concentração territorial das fiscalizações. | [DEFINIR] | [DEFINIR] |
| 5 | Alta | Quais serviços e tipos de instrumento foram mais frequentes? | Como analista, quero classificar os registros por serviço, espécie e item para compreender o perfil técnico da demanda. | [DEFINIR] | [DEFINIR] |
| 6 | Alta | Quais resultados e irregularidades foram encontrados nas fiscalizações? | Como gestor, quero analisar aprovações, reprovações, interdições e verificações não realizadas por município e tipo de instrumento. | [DEFINIR] | [DEFINIR] |
| 7 | Alta | Como a demanda variou ao longo do período analisado? | Como analista, quero comparar meses, dias da semana e estabelecimentos revisitados para identificar padrões temporais e recorrências. | [DEFINIR] | [DEFINIR] |
| 8 | Alta | Qual foi o perfil dos roteiros históricos? | Como planejador, quero analisar a quantidade de endereços, instrumentos e o intervalo operacional de cada roteiro para compreender sua configuração. | [DEFINIR] | [DEFINIR] |
| 9 | Alta | Quais indicadores representam o desempenho da operação histórica? | Como gestor, quero acompanhar indicadores de equipes, demanda, carga e resultados para avaliar o cenário histórico. | [DEFINIR] | [DEFINIR] |
| 10 | Média | Como visualizar e disponibilizar os resultados da análise histórica? | Como usuário, quero consultar um dashboard com filtros e exportar os resultados para apoiar análises, apresentações e decisões. | [DEFINIR] | [DEFINIR] |

## 🧮 Otimização da operação

| Rank | Prioridade | Pergunta | User Story | Estimativa | Sprint |
|-----:|------------|----------|------------|------------|--------|
| 11 | Alta | Como representar geograficamente os pontos de fiscalização? | Como analista, quero geocodificar os endereços e visualizá-los em um mapa para compreender sua distribuição territorial. | [DEFINIR] | [DEFINIR] |
| 12 | Alta | Como calcular as distâncias e os tempos entre os pontos? | Como planejador, quero construir uma matriz considerando fiscalizações e bases operacionais para calcular os deslocamentos. | [DEFINIR] | [DEFINIR] |
| 13 | Alta | Quais capacidades e restrições operacionais devem ser consideradas? | Como gestor, quero definir jornadas, bases, disponibilidade, especializações e limites das equipes para garantir soluções viáveis. | [DEFINIR] | [DEFINIR] |
| 14 | Alta | Como representar matematicamente o problema de otimização? | Como planejador, quero definir objetivos, variáveis e restrições para formular o problema em Pesquisa Operacional. | [DEFINIR] | [DEFINIR] |
| 15 | Alta | Como implementar e validar o modelo de otimização? | Como desenvolvedor, quero implementar o modelo em Python e testar seus resultados para gerar soluções consistentes. | [DEFINIR] | [DEFINIR] |
| 16 | Alta | Qual é a melhor distribuição das fiscalizações entre as equipes? | Como planejador, quero agrupar e distribuir as fiscalizações para reduzir deslocamentos e melhorar a utilização das equipes. | [DEFINIR] | [DEFINIR] |
| 17 | Alta | Qual é a melhor sequência de visitas para cada equipe? | Como planejador, quero gerar roteiros otimizados para reduzir quilômetros e tempo de deslocamento. | [DEFINIR] | [DEFINIR] |
| 18 | Alta | Como equilibrar a carga de trabalho no cenário otimizado? | Como gestor, quero distribuir as atividades considerando visitas, instrumentos, tempo e deslocamento para evitar desequilíbrios. | [DEFINIR] | [DEFINIR] |
| 19 | Média | Como diferentes cenários afetam o planejamento das equipes? | Como planejador, quero simular mudanças na quantidade de equipes, capacidade e restrições para avaliar alternativas operacionais. | [DEFINIR] | [DEFINIR] |
| 20 | Alta | Quais ganhos são obtidos ao comparar os cenários histórico e otimizado? | Como gestor, quero comparar distância, tempo, carga, cobertura e atendimentos para avaliar os benefícios e as limitações da otimização. | [DEFINIR] | [DEFINIR] |

---

> As perguntas relacionadas às rotas, distâncias e tempos dependerão da geocodificação dos endereços, da construção da matriz de deslocamentos e da validação das restrições operacionais com o cliente.

<a name="indicadores"></a>

# 📈 Indicadores

## 📊 Cenário histórico

- Quantidade de roteiros, visitas e instrumentos;
- Distribuição de fiscais e motoristas;
- Carga de trabalho por equipe;
- Visitas e instrumentos por município;
- Fiscalizações por serviço e tipo de instrumento;
- Aprovações, reprovações e interdições;
- Variação da demanda ao longo do período.

## 🧮 Cenário otimizado

- Quilômetros e tempo de deslocamento;
- Carga de trabalho por equipe;
- Quantidade de atendimentos;
- Cobertura dos municípios;
- Redução percentual de distância e tempo;
- Comparação entre os cenários histórico e otimizado.

> Os indicadores de distância e tempo dependerão da geocodificação dos endereços e da construção da matriz de deslocamentos.

---

<a name="fluxo"></a>

# 🔄 Fluxo Geral do Projeto

O projeto será desenvolvido em duas etapas: análise da operação histórica e construção do cenário otimizado.

```mermaid
flowchart TD
    A["Dados históricos"] --> B["Tratamento e validação"]
    B --> C["Análise do histórico"]
    C --> D["Indicadores iniciais"]
    D --> E["Geocodificação e matriz"]
    E --> F["Modelagem matemática"]
    F --> G["Otimização em Python"]
    G --> H["Simulação de cenários"]
    H --> I["Comparação e resultados"]
```

---
<a name="sprints"></a>

# 📅 Registro das Sprints

| Entrega | Previsão | Status | Histórico |
|---------|----------|--------|-----------|
| Vídeo de entendimento do problema | 04/09/2026 | Entregue | [Vídeo](https://www.youtube.com/watch?v=mzAqFt83a5Y) |
| Sprint 01 / Entrega 1 | 02/10/2026 | Não iniciada | [MVP](sp1.md) |
| Sprint 02 / Entrega 2 | 30/10/2026 | Não iniciada | [MVP](sp2.md) |
| Sprint 03 / Entrega 3 + vídeo | 27/11/2026 | Não iniciada | [MVP](sp3.md) |
| Feira de Soluções | 03/12/2026 | Não iniciada | — |

---

# 📝 Observação

As restrições operacionais, a composição das equipes e os critérios do modelo serão detalhados durante as próximas etapas, conforme a validação com o IPEM-SP.
