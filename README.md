# 📌 SafeFlow – Otimização das Rotas das Equipes de Fiscalização do IPEM-SP

Projeto desenvolvido no 3º semestre do curso de Logística da Fatec São José dos Campos, no contexto da Aprendizagem por Projetos Integradores (API).

O projeto tem como objetivo desenvolver uma solução baseada em Pesquisa Operacional para otimizar o planejamento das equipes de fiscalização do IPEM-SP, utilizando dados históricos de inspeções para reduzir deslocamentos e tempos de viagem, balancear a carga de trabalho e apoiar o planejamento das operações.

---

# 📑 Índice

| Seção | Link |
|------|------|
| 📊 Projeto | [Clique aqui](#projeto) |
| 👥 Equipe | [Clique aqui](#equipe) |
| 🎯 Objetivo do Projeto | [Clique aqui](#objetivo) |
| ❓ Questões para Análise | [Clique aqui](#questoes) |
| ⚙️ Funcionalidades | [Clique aqui](#funcionalidades) |
| 📋 Requisitos do Projeto | [Clique aqui](#requisitos) |
| 🛠 Tecnologias Utilizadas | [Clique aqui](#tecnologias) |
| 🗂 Backlog do Produto | [Clique aqui](#backlog) |
| 📅 Registro das Sprints | [Clique aqui](#sprints) |

---

<a name="projeto"></a>

# 📊 Projeto

## Otimização das Rotas das Equipes de Fiscalização do IPEM-SP

O IPEM-SP — Instituto de Pesos e Medidas do Estado de São Paulo — realiza fiscalizações de instrumentos e equipamentos, como balanças e bombas de combustível.

O desafio deste projeto consiste em analisar os dados históricos das fiscalizações e desenvolver uma solução capaz de propor uma distribuição otimizada das atividades entre as equipes.

A solução deverá utilizar conceitos de Pesquisa Operacional e modelos matemáticos de roteirização para comparar a operação historicamente realizada com um cenário otimizado.

### Principais pontos

- Analisar o histórico de fiscalizações;
- Tratar e organizar a base de dados;
- Analisar a distribuição histórica das equipes;
- Construir uma matriz de distâncias e tempos;
- Desenvolver um modelo matemático de otimização;
- Implementar o modelo em Python;
- Comparar rotas históricas e otimizadas;
- Balancear a carga de trabalho entre as equipes;
- Calcular indicadores de desempenho;
- Demonstrar os possíveis ganhos de eficiência.

---

<a name="equipe"></a>

# 👥 Equipe

| Função | Nome | LinkedIn & GitHub |
|--------|------|------------------|
| Product Owner | Ana Clara Dias | [LinkedIn](http://linkedin.com/in/ana-clara-dias-de-souza-927431179) \| [GitHub](https://github.com/AninhaDias) |
| Team Member | Kauan Souza | [LinkedIn](https://linkedin.com/in/kauan-souza-9247aa377) \| [GitHub](https://github.com/kauanzcsouza10-art) |
| Team Member | Davi Pais | [LinkedIn](https://linkedin.com/in/davi-pais-340989359) \| [GitHub](https://github.com/DaviPaisKitada) |
| Team Member | Mariana Leal | [LinkedIn](https://linkedin.com/in/mariana-leal-a708b8335) \| [GitHub](https://github.com/marileal071415-create) |

> As funções da equipe poderão ser atualizadas conforme a organização definida durante o desenvolvimento do projeto.

---

<a name="objetivo"></a>

# 🎯 Objetivo do Projeto

Desenvolver uma proposta de otimização e escalonamento das equipes de fiscalização do IPEM-SP, aplicando modelos de Pesquisa Operacional aos dados históricos da regional de São José dos Campos.

A solução deverá apoiar o planejamento das operações buscando:

- Minimizar os deslocamentos das equipes;
- Reduzir o tempo de viagem;
- Balancear a carga de trabalho;
- Melhorar a distribuição das fiscalizações;
- Apoiar o planejamento das equipes;
- Comparar o cenário histórico com um cenário otimizado;
- Demonstrar os ganhos de eficiência obtidos.

### Resultado esperado

Ao final do projeto, espera-se obter um modelo matemático de roteirização baseado em **VRP / Workforce Routing**, capaz de apoiar o planejamento das equipes de fiscalização.

O resultado deverá permitir comparar os cenários histórico e otimizado por meio de indicadores e visualizações.

---

<a name="questoes"></a>

<a name="questoes"></a>

# ❓ Questões para Análise

As questões do projeto foram organizadas em duas etapas. A primeira utiliza diretamente os dados históricos fornecidos pelo IPEM-SP. A segunda dependerá do enriquecimento geográfico da base, da definição das restrições operacionais e da construção do modelo de otimização.

## 📊 Etapa 1 — Diagnóstico da operação histórica

Com os dados atualmente disponíveis, a equipe buscará responder:

1. Como os fiscais e motoristas foram distribuídos historicamente?
2. Quantos roteiros foram realizados por fiscal?
3. Quantas visitas foram realizadas por equipe?
4. Quantos instrumentos foram verificados por equipe?
5. Quais municípios concentraram a maior quantidade de visitas?
6. Quais municípios concentraram o maior volume de instrumentos verificados?
7. Quais serviços, espécies e tipos de instrumento foram mais frequentes?
8. Quais resultados foram encontrados nas verificações?
9. Quais municípios concentraram mais reprovações e interdições?
10. Quais estabelecimentos foram visitados mais de uma vez?
11. Quantos endereços e instrumentos foram atendidos em cada roteiro?
12. Como a demanda por fiscalizações variou ao longo de 2018?
13. Quais combinações de fiscal e motorista foram mais utilizadas?
14. Como a carga histórica de trabalho foi distribuída entre os fiscais?
15. Quais dados estão ausentes, duplicados ou inconsistentes?

## 🧮 Etapa 2 — Otimização da operação

Após o tratamento e o enriquecimento geográfico da base, a equipe buscará responder:

1. Qual seria a melhor distribuição das fiscalizações entre as equipes?
2. Como agrupar fiscalizações geograficamente próximas?
3. Como reduzir deslocamentos desnecessários?
4. Qual seria a melhor sequência de visitas em cada roteiro?
5. Como equilibrar a carga de trabalho entre as equipes?
6. Qual é a redução potencial de quilômetros percorridos?
7. Qual é a redução potencial do tempo de deslocamento?
8. A operação otimizada mantém a mesma quantidade de atendimentos?
9. A operação otimizada mantém ou amplia a cobertura dos municípios?
10. Como comparar a operação histórica com a operação otimizada?
11. Como diferentes quantidades de equipes afetam o planejamento?
12. Quantas fiscalizações adicionais poderiam ser realizadas com os recursos economizados?

> As respostas relacionadas a distâncias, tempos e rotas dependerão da geocodificação dos endereços, da construção de uma matriz de distâncias e tempos e da definição das restrições reais da operação.

---

<a name="funcionalidades"></a>

# ⚙️ Funcionalidades da Plataforma

A plataforma será desenvolvida de forma progressiva, acompanhando as etapas de análise e otimização do projeto.

## 📊 Módulos do diagnóstico histórico

- 🧹 Tratamento e padronização dos dados;
- 👥 Análise da distribuição de fiscais e motoristas;
- 📍 Análise das visitas por município;
- ⚖️ Análise da carga histórica de trabalho;
- 🧰 Análise dos serviços e instrumentos verificados;
- ✅ Análise dos resultados das verificações;
- 📈 Dashboard de indicadores históricos;
- 🔎 Filtros por período, município, fiscal, motorista, serviço e resultado;
- 📄 Exportação dos resultados.

## 🗺️ Módulos da otimização

- 🗺️ Mapa geográfico das fiscalizações;
- 📏 Matriz de distâncias e tempos;
- 🚗 Representação aproximada dos roteiros históricos;
- 🧮 Modelo matemático de otimização;
- ⚙️ Distribuição otimizada das fiscalizações;
- 🔄 Simulação de diferentes cenários;
- 🔍 Comparação entre os cenários histórico e otimizado;
- 📊 Dashboard comparativo;
- 📄 Exportação de relatórios técnicos.

> A representação dos roteiros históricos será tratada como uma aproximação, pois a base registra os horários das verificações, mas não contém explicitamente a sequência real dos deslocamentos realizados.

---

<a name="requisitos"></a>

# 📋 Requisitos do Projeto

Os requisitos foram organizados conforme a ordem lógica de desenvolvimento da solução.

| Código | Requisito |
|--------|-----------|
| RN.P.1 | Importar e preservar a base histórica original |
| RN.P.2 | Identificar a estrutura e o nível de granularidade dos registros |
| RN.P.3 | Tratar dados ausentes, inconsistentes e duplicados |
| RN.P.4 | Padronizar datas, horários, nomes, endereços e categorias |
| RN.P.5 | Diferenciar instrumentos, visitas e roteiros |
| RN.P.6 | Identificar fiscais, motoristas e combinações históricas de equipe |
| RN.P.7 | Extrair e padronizar os municípios a partir dos endereços |
| RN.P.8 | Analisar a distribuição histórica dos roteiros |
| RN.P.9 | Analisar visitas e instrumentos por município |
| RN.P.10 | Analisar serviços, espécies e tipos de instrumento |
| RN.P.11 | Analisar os resultados das verificações |
| RN.P.12 | Calcular indicadores históricos de desempenho |
| RN.P.13 | Desenvolver o dashboard do cenário histórico |
| RN.P.14 | Geocodificar os endereços válidos |
| RN.P.15 | Construir a matriz de distâncias e tempos |
| RN.P.16 | Definir objetivos, parâmetros e restrições operacionais |
| RN.P.17 | Modelar o problema em Programação Inteira Mista |
| RN.P.18 | Implementar o modelo de otimização em Python |
| RN.P.19 | Construir o cenário otimizado |
| RN.P.20 | Comparar os cenários histórico e otimizado |
| RN.P.21 | Permitir a simulação de diferentes cenários |
| RN.P.22 | Exportar indicadores e resultados |
| RN.P.23 | Elaborar o relatório técnico do projeto |
| RN.P.24 | Documentar limitações, premissas e critérios utilizados |

---

<a name="tecnologias"></a>

# 🛠 Tecnologias Utilizadas

### Tecnologias previstas

- 🐍 **Python** — tratamento dos dados, análises e execução dos modelos de Pesquisa Operacional;
- 🧹 **Pandas** — limpeza, transformação e análise da base histórica;
- 🧮 **OR-Tools / Pyomo** — alternativas previstas para implementação do modelo de otimização;
- 🗺️ **Geocodificação e matriz de distâncias** — transformação dos endereços em coordenadas e cálculo dos deslocamentos;
- 📊 **BI** — construção dos dashboards histórico, otimizado e comparativo;
- 💻 **GitHub** — versionamento, documentação e organização técnica do projeto;
- 📄 **Office** — apresentações, relatório técnico e documentação acadêmica.

> A escolha definitiva das ferramentas de geocodificação, visualização e otimização será realizada após a validação técnica da base e das necessidades do projeto.

---

<a name="backlog"></a>

# 🗂 Backlog do Produto

O backlog foi organizado priorizando as questões que podem ser respondidas com a base histórica atualmente disponível. As questões relacionadas às rotas, distâncias e otimização serão desenvolvidas após a preparação dos dados geográficos e das restrições operacionais.

## 📊 Diagnóstico histórico

| Rank | Prioridade | Pergunta | User Story | Estimativa | Sprint |
|-----:|------------|----------|------------|------------|--------|
| 1 | Alta | Como preservar a integridade da base histórica original? | Como analista, quero importar e preservar a base original para garantir a rastreabilidade dos dados utilizados no projeto. | [DEFINIR] | [DEFINIR] |
| 2 | Alta | Qual é a granularidade dos registros da base? | Como analista, quero diferenciar instrumentos, visitas e roteiros para utilizar a unidade correta em cada análise. | [DEFINIR] | [DEFINIR] |
| 3 | Alta | Quais dados estão ausentes, duplicados ou inconsistentes? | Como analista, quero identificar problemas de qualidade para evitar que registros inadequados prejudiquem os resultados. | [DEFINIR] | [DEFINIR] |
| 4 | Alta | Como padronizar datas, horários, nomes e categorias? | Como analista, quero padronizar os campos da base para preparar os registros para análise. | [DEFINIR] | [DEFINIR] |
| 5 | Alta | Como identificar e padronizar os municípios das fiscalizações? | Como analista, quero extrair os municípios dos endereços para analisar corretamente a distribuição territorial. | [DEFINIR] | [DEFINIR] |
| 6 | Alta | Como fiscais e motoristas foram distribuídos historicamente? | Como gestor, quero visualizar a distribuição histórica dos fiscais e motoristas para compreender como as equipes foram organizadas. | [DEFINIR] | [DEFINIR] |
| 7 | Alta | Quantos roteiros foram realizados por fiscal? | Como gestor, quero visualizar a quantidade de roteiros realizados por fiscal para comparar a atuação dos profissionais. | [DEFINIR] | [DEFINIR] |
| 8 | Alta | Quantas visitas foram realizadas por equipe? | Como gestor, quero consultar a quantidade de endereços atendidos por equipe para analisar a distribuição da carga operacional. | [DEFINIR] | [DEFINIR] |
| 9 | Alta | Quantos instrumentos foram verificados por equipe? | Como analista, quero calcular a quantidade de instrumentos verificados por equipe para medir o volume de trabalho executado. | [DEFINIR] | [DEFINIR] |
| 10 | Alta | Quais municípios concentraram a maior quantidade de visitas? | Como planejador, quero identificar os municípios com maior quantidade de visitas para compreender a concentração territorial da demanda. | [DEFINIR] | [DEFINIR] |
| 11 | Alta | Quais municípios concentraram o maior volume de instrumentos verificados? | Como analista, quero identificar os municípios com maior volume de instrumentos para compreender a demanda técnica regional. | [DEFINIR] | [DEFINIR] |
| 12 | Alta | Quais serviços foram realizados com maior frequência? | Como analista, quero classificar os registros por serviço para compreender quais atividades foram mais executadas. | [DEFINIR] | [DEFINIR] |
| 13 | Alta | Quais espécies e tipos de instrumento foram mais verificados? | Como analista, quero classificar os instrumentos por espécie e item para compreender o perfil técnico das verificações. | [DEFINIR] | [DEFINIR] |
| 14 | Alta | Quais resultados foram encontrados nas verificações? | Como gestor, quero acompanhar aprovações, reprovações, interdições e verificações não realizadas para avaliar os resultados da operação. | [DEFINIR] | [DEFINIR] |
| 15 | Alta | Quais municípios concentraram mais reprovações e interdições? | Como gestor, quero identificar a concentração territorial de irregularidades para apoiar o planejamento das fiscalizações. | [DEFINIR] | [DEFINIR] |
| 16 | Média | Quais estabelecimentos foram visitados mais de uma vez? | Como analista, quero identificar estabelecimentos revisitados para analisar a recorrência dos atendimentos. | [DEFINIR] | [DEFINIR] |
| 17 | Média | Quantos endereços foram atendidos em cada roteiro? | Como planejador, quero conhecer a quantidade de endereços atendidos por roteiro para comparar as configurações históricas da operação. | [DEFINIR] | [DEFINIR] |
| 18 | Média | Quantos instrumentos foram verificados em cada roteiro? | Como planejador, quero conhecer a quantidade de instrumentos por roteiro para comparar o volume de trabalho executado. | [DEFINIR] | [DEFINIR] |
| 19 | Média | Como a demanda variou ao longo de 2018? | Como analista, quero visualizar a demanda por mês e dia da semana para identificar variações temporais. | [DEFINIR] | [DEFINIR] |
| 20 | Média | Quais combinações de fiscal e motorista foram mais utilizadas? | Como gestor, quero conhecer as combinações de fiscal e motorista para compreender a formação histórica das equipes. | [DEFINIR] | [DEFINIR] |
| 21 | Alta | Como a carga histórica foi distribuída entre os fiscais? | Como gestor, quero comparar roteiros, visitas e instrumentos por fiscal para identificar diferenças na carga de trabalho. | [DEFINIR] | [DEFINIR] |
| 22 | Média | Qual foi o intervalo entre a primeira e a última verificação de cada roteiro? | Como analista, quero calcular o intervalo operacional aparente de cada roteiro para comparar os períodos registrados de atividade. | [DEFINIR] | [DEFINIR] |
| 23 | Alta | Quais indicadores demonstram o desempenho histórico da operação? | Como gestor, quero acompanhar indicadores históricos para avaliar a distribuição, a demanda e os resultados das fiscalizações. | [DEFINIR] | [DEFINIR] |
| 24 | Alta | Como visualizar os indicadores históricos? | Como gestor, quero consultar um dashboard para interpretar os dados históricos de maneira clara e objetiva. | [DEFINIR] | [DEFINIR] |
| 25 | Média | Como consultar análises específicas da operação? | Como usuário, quero aplicar filtros por período, município, equipe, serviço e resultado para investigar diferentes aspectos da operação. | [DEFINIR] | [DEFINIR] |
| 26 | Média | Como disponibilizar os resultados históricos? | Como usuário, quero exportar os resultados para utilizá-los em apresentações, análises e relatórios. | [DEFINIR] | [DEFINIR] |

## 🧮 Otimização da operação

| Rank | Prioridade | Pergunta | User Story | Estimativa | Sprint |
|-----:|------------|----------|------------|------------|--------|
| 27 | Alta | Como visualizar geograficamente as fiscalizações? | Como analista, quero geocodificar os endereços e visualizar as fiscalizações em um mapa para compreender sua distribuição territorial. | [DEFINIR] | [DEFINIR] |
| 28 | Alta | Quais são as distâncias e os tempos entre os pontos de fiscalização? | Como planejador, quero construir uma matriz de distâncias e tempos para calcular os deslocamentos entre os locais atendidos. | [DEFINIR] | [DEFINIR] |
| 29 | Alta | Quais são os pontos de saída e retorno das equipes? | Como planejador, quero definir as bases operacionais das equipes para calcular roteiros compatíveis com a operação real. | [DEFINIR] | [DEFINIR] |
| 30 | Alta | Quais capacidades, jornadas e restrições devem ser respeitadas? | Como gestor, quero definir as restrições das equipes para garantir que as soluções propostas sejam operacionalmente viáveis. | [DEFINIR] | [DEFINIR] |
| 31 | Alta | Como representar matematicamente o problema de distribuição? | Como planejador, quero formular o problema em Programação Inteira Mista para representar os objetivos e as restrições da operação. | [DEFINIR] | [DEFINIR] |
| 32 | Alta | Como implementar o modelo de otimização? | Como desenvolvedor, quero implementar o modelo em Python para gerar e avaliar cenários otimizados. | [DEFINIR] | [DEFINIR] |
| 33 | Alta | Qual seria a melhor distribuição das fiscalizações entre as equipes? | Como planejador, quero otimizar a distribuição das fiscalizações para melhorar a utilização das equipes disponíveis. | [DEFINIR] | [DEFINIR] |
| 34 | Alta | Como agrupar fiscalizações geograficamente próximas? | Como planejador, quero agrupar pontos próximos para reduzir deslocamentos desnecessários. | [DEFINIR] | [DEFINIR] |
| 35 | Alta | Qual seria a melhor sequência de visitas para cada equipe? | Como planejador, quero gerar uma sequência otimizada de visitas para reduzir as distâncias e os tempos de deslocamento. | [DEFINIR] | [DEFINIR] |
| 36 | Alta | Como equilibrar a carga de trabalho entre as equipes? | Como gestor, quero distribuir as atividades de forma equilibrada para evitar sobrecarga ou subutilização das equipes. | [DEFINIR] | [DEFINIR] |
| 37 | Alta | Qual é a redução potencial de quilômetros percorridos? | Como planejador, quero comparar as distâncias dos cenários histórico e otimizado para medir a redução de quilômetros. | [DEFINIR] | [DEFINIR] |
| 38 | Alta | Qual é a redução potencial do tempo de deslocamento? | Como planejador, quero comparar os tempos dos cenários histórico e otimizado para medir o ganho operacional. | [DEFINIR] | [DEFINIR] |
| 39 | Alta | A otimização mantém a quantidade de atendimentos? | Como gestor, quero confirmar que a redução dos deslocamentos não diminui a quantidade de visitas realizadas. | [DEFINIR] | [DEFINIR] |
| 40 | Alta | A otimização mantém a cobertura territorial? | Como gestor, quero verificar se os municípios atendidos historicamente continuam contemplados no cenário otimizado. | [DEFINIR] | [DEFINIR] |
| 41 | Alta | Como comparar a operação histórica com a otimizada? | Como gestor, quero comparar os dois cenários para avaliar os ganhos e impactos da otimização. | [DEFINIR] | [DEFINIR] |
| 42 | Média | Como diferentes quantidades de equipes afetam a operação? | Como planejador, quero simular diferentes quantidades de equipes para avaliar o impacto da disponibilidade de recursos. | [DEFINIR] | [DEFINIR] |
| 43 | Média | Quantas fiscalizações adicionais poderiam ser realizadas com os recursos economizados? | Como gestor, quero estimar a capacidade adicional gerada pela otimização para avaliar possíveis ganhos de produtividade. | [DEFINIR] | [DEFINIR] |
| 44 | Alta | Como visualizar os resultados dos dois cenários? | Como gestor, quero consultar um dashboard comparativo para avaliar as diferenças entre a operação histórica e a otimizada. | [DEFINIR] | [DEFINIR] |
| 45 | Alta | Quais premissas e limitações influenciam os resultados? | Como usuário, quero consultar as premissas e limitações do modelo para interpretar os resultados de maneira responsável. | [DEFINIR] | [DEFINIR] |
| 46 | Alta | Como apresentar os resultados finais do projeto? | Como usuário, quero exportar um relatório técnico contendo metodologia, indicadores, resultados e limitações. | [DEFINIR] | [DEFINIR] |

<a name="indicadores"></a>

# 📈 Indicadores Iniciais

Os indicadores também foram separados conforme sua disponibilidade.

## 📊 Indicadores disponíveis na base histórica

- Quantidade de roteiros realizados;
- Quantidade de visitas a endereços;
- Quantidade de instrumentos verificados;
- Roteiros por fiscal;
- Visitas por fiscal;
- Instrumentos verificados por fiscal;
- Participação dos motoristas nos roteiros;
- Combinações de fiscal e motorista;
- Visitas por município;
- Instrumentos verificados por município;
- Fiscalizações por serviço;
- Instrumentos por espécie;
- Instrumentos por descrição de item;
- Quantidade e percentual de aprovações;
- Quantidade e percentual de reprovações;
- Quantidade e percentual de interdições;
- Quantidade de verificações não realizadas;
- Estabelecimentos revisitados;
- Demanda por mês;
- Demanda por dia da semana;
- Média de visitas por roteiro;
- Média de instrumentos por roteiro;
- Distribuição histórica da carga de trabalho.

## 🧮 Indicadores dependentes da otimização

- Quilômetros estimados no cenário histórico;
- Quilômetros do cenário otimizado;
- Redução absoluta e percentual de quilômetros;
- Tempo estimado de deslocamento histórico;
- Tempo de deslocamento otimizado;
- Redução absoluta e percentual de tempo;
- Distribuição otimizada da carga de trabalho;
- Diferença entre a maior e a menor carga;
- Cobertura territorial;
- Quantidade de atendimentos mantidos;
- Utilização estimada das equipes;
- Capacidade adicional de fiscalização;
- Economia operacional estimada.

> A diferença entre instrumentos, visitas e roteiros deverá ser mantida em todas as análises para evitar interpretações incorretas dos dados.

---

<a name="fluxo"></a>

# 🔄 Fluxo Geral do Projeto

O projeto começará pela compreensão e pelo diagnóstico da operação histórica. Somente após a validação dos dados serão desenvolvidas a matriz de deslocamentos e a otimização.

```mermaid
flowchart TD
    A["📂 Base histórica do IPEM-SP"] --> B["🔍 Compreensão da granularidade"]
    B --> C["🧹 Limpeza e padronização"]
    C --> D["📊 Diagnóstico histórico"]
    D --> E["📈 Indicadores e dashboard inicial"]
    E --> F["🌐 Geocodificação dos endereços"]
    F --> G["🗺️ Matriz de distâncias e tempos"]
    G --> H["📋 Definição das restrições"]
    H --> I["🧮 Modelagem matemática"]
    I --> J["🐍 Otimização em Python"]
    J --> K["⚙️ Cenário otimizado"]
    K --> L["🔍 Comparação dos cenários"]
    L --> M["📊 Dashboard e relatório técnico"]
---

### 📋 Etapas do Projeto

| Etapa | Desenvolvimento |
|------|-----------------|
| 📂 **1. Dados históricos** | Recebimento e compreensão da base de fiscalizações do IPEM |
| 🧹 **2. Tratamento** | Limpeza, padronização e preparação dos dados |
| 📊 **3. Cenário histórico** | Análise de como as fiscalizações foram realizadas |
| 🗺️ **4. Distâncias e tempos** | Construção da matriz necessária para análise das rotas |
| 🧮 **5. Modelagem** | Formulação do problema de Pesquisa Operacional |
| 🐍 **6. Otimização** | Execução do modelo matemático em Python |
| ⚙️ **7. Cenário otimizado** | Construção da nova proposta de distribuição das equipes |
| 🔍 **8. Comparação** | Comparação entre a operação histórica e a otimizada |
| 📈 **9. Resultados** | Indicadores, dashboard e relatório técnico |

---
<a name="sprints"></a>

# 📅 Registro das Sprints

| Entrega | Previsão | Status | Histórico |
|---------|----------|--------|-----------|
| Vídeo de entendimento do problema | 04/09/2026 | ENTREGUE | [Aqui](https://www.youtube.com/watch?v=mzAqFt83a5Y) |
| Sprint 01 / Entrega 1 | 02/10/2026 | Não iniciada | [MVP](sp1.md) |
| Sprint 02 / Entrega 2 | 30/10/2026 | Não iniciada | [MVP](sp2.md) |
| Sprint 03 / Entrega 3 + Vídeo | 27/11/2026 | Não iniciada | [MVP](sp3.md) |
| Feira de Soluções | 03/12/2026 | Não iniciada | --- |

---
# 📝 Observações

Algumas informações operacionais ainda deverão ser confirmadas com o IPEM durante o desenvolvimento, incluindo:

- Quantidade e composição das equipes;
- Jornada de trabalho;
- Características e duração dos diferentes tipos de fiscalização;
- Área geográfica considerada;
- Restrições operacionais;
- Prioridades e frequências das fiscalizações;
- Tratamento de urgências e estabelecimentos prioritários;
- Critérios definitivos utilizados para avaliar o cenário otimizado.

Essas informações serão incorporadas à documentação conforme forem validadas durante o projeto.
