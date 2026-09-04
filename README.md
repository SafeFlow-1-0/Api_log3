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

# ❓ Questões para Análise

Durante o desenvolvimento do projeto, a equipe deverá buscar responder às seguintes questões:

1. Como as equipes foram distribuídas historicamente?
2. Qual seria a melhor distribuição das fiscalizações entre as equipes?
3. Qual a redução potencial de quilômetros e tempo de deslocamento?
4. Como balancear a carga de trabalho?
5. Quais municípios e tipos de fiscalização concentram maior demanda?
6. Como comparar a operação real com a otimizada?

---

<a name="funcionalidades"></a>

# ⚙️ Funcionalidades da Plataforma

A solução deverá contemplar os seguintes módulos:

- 🗺️ Mapa das fiscalizações;
- 🚗 Rotas históricas e rotas otimizadas;
- 📊 Dashboard de indicadores;
- 🔄 Simulação de cenários;
- 📄 Exportação de relatórios.

---

<a name="requisitos"></a>

# 📋 Requisitos do Projeto

| Código | Requisito |
|--------|-----------|
| RN.P.1 | Tratar os dados históricos |
| RN.P.2 | Construir matriz de distâncias e tempos |
| RN.P.3 | Modelar o problema em Programação Inteira Mista |
| RN.P.4 | Implementar em Python (OR-Tools/Pyomo) |
| RN.P.5 | Desenvolver dashboard |
| RN.P.6 | Comparar cenário real e otimizado |
| RN.P.7 | Calcular indicadores de desempenho |
| RN.P.8 | Elaborar relatório técnico |

---

<a name="tecnologias"></a>

# 🛠 Tecnologias Utilizadas

### Tecnologias previstas

- 🐍 **Python** — execução dos modelos de Pesquisa Operacional;
- 🧮 **OR-Tools / Pyomo** — alternativas previstas para implementação do modelo de otimização;
- 📊 **BI** — visualização dos cenários histórico e otimizado;
- 💻 **GitHub** — versionamento, documentação e organização técnica do projeto;
- 📄 **Office** — apresentações, relatório e documentação.

> Outras tecnologias poderão ser adicionadas conforme a evolução e as necessidades do projeto.

---

<a name="backlog"></a>

# 🗂 Backlog do Produto

O backlog será detalhado pela equipe durante o planejamento das Sprints.

| Rank | Prioridade | Requisito / User Story | Estimativa | Sprint |
|------|------------|------------------------|------------|--------|
| 1 | [DEFINIR] | Tratamento dos dados históricos | [DEFINIR] | [DEFINIR] |
| 2 | [DEFINIR] | Construção da matriz de distâncias e tempos | [DEFINIR] | [DEFINIR] |
| 3 | [DEFINIR] | Modelagem do problema em Programação Inteira Mista | [DEFINIR] | [DEFINIR] |
| 4 | [DEFINIR] | Implementação do modelo em Python | [DEFINIR] | [DEFINIR] |
| 5 | [DEFINIR] | Desenvolvimento do dashboard | [DEFINIR] | [DEFINIR] |
| 6 | [DEFINIR] | Comparação entre cenário histórico e otimizado | [DEFINIR] | [DEFINIR] |
| 7 | [DEFINIR] | Cálculo dos indicadores de desempenho | [DEFINIR] | [DEFINIR] |
| 8 | [DEFINIR] | Elaboração do relatório técnico | [DEFINIR] | [DEFINIR] |

---

# 📈 Indicadores Iniciais

Entre os indicadores previstos para análise estão:

- Quantidade de visitas realizadas;
- Tempo médio das fiscalizações;
- Quilômetros percorridos;
- Tempo de deslocamento;
- Distribuição da carga de trabalho;
- Fiscalizações por município;
- Fiscalizações por tipo;
- Comparação entre cenário histórico e cenário otimizado.

---

# 🔄 Fluxo Geral do Projeto

**Dados históricos do IPEM**

⬇️

**Limpeza e tratamento dos dados**

⬇️

**Análise do cenário histórico**

⬇️

**Construção da matriz de distâncias e tempos**

⬇️

**Modelagem em Pesquisa Operacional**

⬇️

**Otimização em Python**

⬇️

**Construção do cenário otimizado**

⬇️

**Comparação Histórico × Otimizado**

⬇️

**Indicadores + Dashboard + Relatório Técnico**

---

<a name="sprints"></a>

# 📅 Registro das Sprints

| Entrega | Previsão | Status | Histórico |
|---------|----------|--------|----------|
| Vídeo de entendimento do problema | 04/09/2026 | ENTREGUE | | [Video](https://www.youtube.com/watch?v=mzAqFt83a5Y) /|
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
