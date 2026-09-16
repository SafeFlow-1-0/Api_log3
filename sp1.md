# 📌 MVP - SafeFlow

## 🎯 Objetivo do MVP
 
- **Qual problema resolve?**  
  * Organizar, tratar e analisar os dados históricos de fiscalização do IPEM-SP, permitindo compreender como a operação foi realizada e estabelecer uma base confiável para as próximas etapas de otimização.

- **Qual hipótese será validada?**
  * A base histórica pode ser tratada e estruturada para representar adequadamente a operação de fiscalização;
  * É possível identificar a distribuição das fiscalizações entre equipes e municípios;
  * Os dados permitem analisar a carga de trabalho, a demanda e os resultados das fiscalizações;
  * É possível construir indicadores que representem o cenário histórico e sirvam posteriormente como referência para comparação com o cenário otimizado.

- **Qual valor será entregue ao usuário final?**  
  * Uma visão estruturada da operação histórica da regional de São José dos Campos, com dados tratados e indicadores que permitam compreender a distribuição das fiscalizações, a demanda e a carga de trabalho das equipes.

---

## 📝 Descrição da Solução
  
- **Funcionalidades principais incluídas**  
  * Tratamento e padronização da base histórica;
  * Identificação de dados ausentes, duplicados e inconsistentes;
  * Diferenciação entre instrumentos, visitas e roteiros;
  * Análise da distribuição de fiscais e motoristas;
  * Análise da carga de trabalho;
  * Análise das fiscalizações por município;
  * Análise dos serviços e instrumentos fiscalizados;
  * Análise dos resultados das fiscalizações;
  * Construção dos principais indicadores históricos;
  * Desenvolvimento de uma visualização inicial dos resultados.

- **Limitações conhecidas**  
  * A Sprint 01 será baseada nos dados históricos disponibilizados pelo IPEM-SP;
  * A qualidade das análises dependerá da qualidade e do preenchimento da base original;
  * Informações não presentes na base não poderão ser determinadas diretamente;
  * Distâncias e tempos de deslocamento ainda não serão considerados;
  * Os roteiros históricos não representam necessariamente o trajeto real percorrido pelas equipes.
  
- **Escopo reduzido**  
  * Nesta Sprint, o foco será exclusivamente o tratamento dos dados e a compreensão da operação histórica. A geocodificação, matriz de distâncias e tempos, modelagem matemática e otimização das rotas serão desenvolvidas nas etapas posteriores.

---

## 👥 Personas / Usuários-Alvo

<p align="justify">
<strong>Gestores do IPEM-SP:</strong> responsáveis pelo planejamento, acompanhamento e tomada de decisões relacionadas às operações de fiscalização. Utilizam os dados e indicadores para identificar a distribuição da demanda, avaliar a carga de trabalho das equipes e apoiar o planejamento das fiscalizações.
</p>

<p align="justify">
<strong>Carlos Bastos:</strong> Cliente e avaliadores do projeto, acompanhando o desenvolvimento da plataforma de BI para o comércio exterior paulista. Necessidades e tarefas atendidas: É necessário que os alunos entreguem uma solução bem documentada, funcional e aderente aos requisitos ágeis, garantindo que o aprendizado e a aplicação prática de competências logísticas e de análise de dados sejam oferecidos.
</p>

<p align="justify">
<strong>Marcus Nascimento:</strong> Cliente, interessado no desempenho do comércio exterior. Necessidades e tarefas atendidas: Precisa de acesso a dados organizados, consolidados e visualmente compreensíveis para apoiar decisões estratégicas e logísticas, atualmente os dados estão dispersos e desativados manual de esforço para análise.
</p>

---
## 🔑 User Stories (Backlog do MVP)

| Rank | Prioridade | Pergunta | User Story | Estimativa |
|------|------------|----------|------------|------------|
| 1 | Alta | Como preparar e validar a base histórica para análise? | Como analista, quero tratar, padronizar e validar os dados, diferenciando instrumentos, visitas e roteiros, para garantir resultados confiáveis. | 16h |
| 2 | Alta | Como fiscais e motoristas foram distribuídos historicamente? | Como gestor, quero visualizar a formação das equipes e os roteiros realizados para compreender como os profissionais foram distribuídos. | 6h |
| 3 | Alta | Como a carga de trabalho foi distribuída entre as equipes? | Como gestor, quero comparar roteiros, visitas e instrumentos por equipe para identificar sobrecarga ou subutilização. | 8h |
| 4 | Alta | Quais municípios concentraram a maior demanda? | Como planejador, quero analisar visitas e instrumentos por município para identificar a concentração territorial das fiscalizações. | 5h |
| 5 | Alta | Quais serviços e tipos de instrumento foram mais frequentes? | Como analista, quero classificar os registros por serviço, espécie e item para compreender o perfil técnico da demanda. | 6h |
| 6 | Alta | Quais resultados e irregularidades foram encontrados nas fiscalizações? | Como gestor, quero analisar aprovações, reprovações, interdições e verificações não realizadas por município e tipo de instrumento. | 6h |
| 7 | Alta | Como a demanda variou ao longo do período analisado? | Como analista, quero comparar meses, dias da semana e estabelecimentos revisitados para identificar padrões temporais e recorrências. | 8h |
| 8 | Alta | Qual foi o perfil dos roteiros históricos? | Como planejador, quero analisar a quantidade de endereços, instrumentos e o intervalo operacional de cada roteiro para compreender sua configuração. | 8h |
| 9 | Alta | Quais indicadores representam o desempenho da operação histórica? | Como gestor, quero acompanhar indicadores de equipes, demanda, carga e resultados para avaliar o cenário histórico. | 8h |
| 10 | Média | Como visualizar e disponibilizar os resultados da análise histórica? | Como usuário, quero consultar um dashboard com filtros e exportar os resultados para apoiar análises, apresentações e decisões. | 12h |

**Estimativa total da Sprint 01: 83 horas.**

---

## 📅 Sprint(s) Relacionadas

| Sprint | Entregas Principais | Status |
|--------|--------------------|--------|
| 01 | Tratamento e validação da base histórica | Em desenvolvimento |
| 01 | Estruturação dos dados de instrumentos, visitas e roteiros | Não iniciada |
| 01 | Análise da distribuição das equipes e da demanda | Não iniciada |
| 01 | Construção dos indicadores históricos | Não iniciada |
| 01 | Visualização inicial dos resultados | Em desenvolvimento |

---

## 📊 Critérios de Aceitação

  * A base histórica deve possuir processo de tratamento documentado e reproduzível;
  * Dados ausentes, duplicados e inconsistentes devem ser identificados e tratados de acordo com regras documentadas;
  * Instrumentos, visitas e roteiros devem possuir critérios claros de identificação;
  * Os principais indicadores da operação histórica devem ser calculados a partir da base tratada;
  * As análises devem permitir compreender a distribuição das equipes, da demanda e da carga de trabalho;
  * Os resultados apresentados devem ser rastreáveis até os dados utilizados no processamento.

---

## 📈 Métricas de Validação

**Qualidade dos dados**
  * Quantidade de registros analisados;
  * Quantidade de dados ausentes identificados;
  * Quantidade de duplicidades identificadas;
  * Quantidade de inconsistências encontradas e tratadas.
    
**Cobertura das análises**
  * Quantidade de roteiros identificados;
  * Quantidade de visitas identificadas;
  * Quantidade de instrumentos analisados;
  * Distribuição das fiscalizações por equipe e município;
  * Indicadores históricos calculados.
    
**Validação do MVP**
  * Validação dos resultados pela equipe;
  * Feedback do professor e/ou cliente após apresentação da entrega;
  * Ajustes identificados durante a homologação.

---

## 🚀 Próximos Passos

  * Geocodificar os pontos de fiscalização;
  * Construir a matriz de distâncias e tempos;
  * Definir as capacidades e restrições operacionais;
  * Iniciar a formulação do modelo matemático de otimização;
  * Utilizar os indicadores históricos como referência para comparação com os futuros cenários otimizados.

---

## 📂 Anexos / Evidências

- 🔗 **Vídeo:**  
  [ADICIONAR LINK]

- 📄 **Documentos:**  
  [ADICIONAR]

- 📊 **Dashboard / Protótipo:**  
  [ADICIONAR]

- 💻 **Código / Scripts:**  
  [ADICIONAR]

