# 📊 Mini-Projeto: Análise Exploratória de Dados (AED) — Varejo

**Aluna:** Jackeline Melo
**Turma:** T6
**Arquivo principal:** `Miniprojeto_JackelineMelo_Analise_de_Dados_T6.py`
**Base de dados:** `Base_Varejo.csv`

---

## 📌 Sobre o projeto

Este mini-projeto aplica uma **Análise Exploratória de Dados (AED)** sobre uma base de dados de varejo, com o objetivo de transformar dados brutos em informações úteis para a tomada de decisão.

A base **"Varejo"** reúne registros reais de compras — datas, compras, clientes e produtos — permitindo praticar diagnóstico de qualidade dos dados, limpeza e geração de estatísticas descritivas, habilidades essenciais para quem trabalha com **BI (Business Intelligence)** e **Visualização de Dados**.

---

## 🗂️ Sobre a base de dados

A base contém **830.000 registros** (cada linha representa um item comprado) e **10 colunas** de informação, além de 4 colunas extras totalmente vazias geradas na exportação do arquivo.

| Coluna | Descrição | Observações |
|---|---|---|
| `DATA` | Data da compra | Formato `dd/mm/aaaa`; período de **04/01/2019 a 08/12/2022** |
| `CO_ID` | Identificador da compra (pedido) | 18.471 compras distintas |
| `CL_ID` | Identificador do cliente | 1.000 clientes distintos |
| `CL_GENERO` | Gênero do cliente | `M` ou `F` |
| `CL_EC` | Estado civil do cliente (código) | Valores de 1 a 5 |
| `CL_FHL` | Quantidade de filhos do cliente | Valores de 0 a 4 |
| `CL_SEG` | Segmento do cliente | `A`, `B` ou `C` |
| `PR_ID` | Identificador do produto | 229 produtos distintos |
| `PR_CAT` | Categoria do produto | Ver distribuição abaixo |
| `PR_NOME` | Nome do produto | 118 nomes distintos |

**Distribuição por categoria de produto (`PR_CAT`):**

| Categoria | Itens vendidos |
|---|---|
| ALIMENTOS | 434.767 |
| HIGIENE | 155.574 |
| LIMPEZA | 145.754 |
| BEBIDAS | 43.299 |
| PET | 32.399 |
| ACESSORIOS | 14.557 |
| `#N/D` (não identificado) | 3.650 |

Em média, cada compra reúne cerca de **45 itens** (variando de 1 a 89 itens por compra).

### ⚠️ Problemas de qualidade identificados

- **96.553 linhas duplicadas** na base;
- **3.650 registros** com categoria de produto marcada como `#N/D` (não disponível/identificada);
- **4 colunas totalmente vazias** (`Unnamed: 10` a `Unnamed: 13`), resultado de formatação do arquivo original em Excel/CSV;
- Colunas categóricas codificadas numericamente (`CL_EC`, `CL_FHL`) que exigem um dicionário de dados para correta interpretação de negócio.

Esses pontos são justamente o alvo do tratamento e limpeza realizados no script principal.

---

## 🎯 Objetivo educacional

Ao final do projeto, a expectativa é saber preparar uma base de dados para análises mais avançadas ou para alimentar um dashboard — ou seja, entender os dados, limpá-los, extrair estatísticas descritivas e comunicar os principais insights de forma objetiva.

---

## 🧭 O que é praticado

Ao longo do projeto, são exercitadas tarefas comuns do dia a dia de um(a) analista de dados:

- **Diagnóstico de qualidade dos dados**: identificação de valores nulos/inválidos (`#N/D`), colunas vazias e registros duplicados;
- **Tratamento e limpeza** desses problemas com a biblioteca `pandas`;
- **Estatísticas descritivas** e funções de agrupamento (`groupby`, `describe`, `value_counts`, etc.);
- **Respostas a perguntas de negócio**, como:
  - Quem compra mais (quais clientes têm maior volume de compras)?
  - Quais categorias de produto vendem mais?
  - Como as compras se comportam entre os diferentes segmentos de clientes (`CL_SEG`)?
  - Como as vendas variam ao longo do tempo (2019–2022)?

---

## 🛠️ Tecnologias utilizadas

- **Python 3**
- **pandas** — leitura, limpeza e manipulação dos dados (arquivo CSV separado por `;`)
- *(inclua aqui outras bibliotecas usadas, como `numpy`, `matplotlib` ou `seaborn`, se aplicável)*

---

## 📁 Estrutura do projeto

```
├── Miniprojeto_JackelineMelo_Analise_de_Dados_T6.py   # Script principal com a análise
├── Base_Varejo.csv                                    # Base de dados utilizada
└── README.md                                          # Este arquivo
```

---

## ▶️ Como executar

1. Clone este repositório ou baixe os arquivos, mantendo `Base_Varejo.csv` na mesma pasta do script.
2. Instale as dependências necessárias:
   ```bash
   pip install pandas
   ```
3. Execute o script principal:
   ```bash
   python Miniprojeto_JackelineMelo_Analise_de_Dados_T6.py
   ```

> 💡 Ao ler o arquivo, lembre-se de indicar o separador correto: `pd.read_csv('Base_Varejo.csv', sep=';')`.

---

## 📈 Principais resultados / insights

### 🚀 Etapas realizadas (Sprints)

O desenvolvimento do projeto foi organizado em 6 sprints, cobrindo desde a importação dos dados até o versionamento final:

| Sprint | Etapa | O que foi realizado |
|---|---|---|
| **1** | Importação dos dados | Importação da base a partir da plataforma Kaggle para a IDE (VS Code ou Google Colab), ambiente onde o script foi executado. |
| **2** | Transformação de Strings, Integer, Float e Datetime | Desenvolvimento de funções de limpeza de texto, números inteiros e decimais, utilizando métodos de string e expressões regulares (regex). |
| **3** | Limpeza de Nulos e Duplicatas | Aplicação de condicionais e funções para identificação e substituição de valores vazios, remoção de duplicatas e conversão da coluna de data (`str` → `datetime`) na tabela de varejo. |
| **4** | Estatística Descritiva | Aplicação de funções estatísticas para extrair parâmetros (média, mediana, desvio-padrão, etc.) da coluna de número de filhos do cliente (`CL_FHL`). |
| **5** | Relatório e Documentação | Construção dos contadores exibidos no relatório final via terminal e finalização deste `README.md`, incluindo a reflexão teórica sobre o processo, com posterior submissão do link no AVA. |
| **6** | Versionamento | Envio dos arquivos do projeto (script, `README.md` e `df_limpo`) via Git para o repositório no GitHub. |

### 🔎 Achados da análise

*(preencha esta seção com os achados específicos da sua análise; alguns pontos de partida a partir do diagnóstico inicial da base:)*

- A categoria **ALIMENTOS** concentra a maior parte dos itens vendidos (mais de 50% do total);
- A base cobre quase **4 anos** de histórico de compras (2019–2022), permitindo análises de sazonalidade;
- Existem **1.000 clientes** distintos e **18.471 compras**, o que permite calcular ticket médio e frequência de compra por cliente;
- *(adicione aqui: cliente(s) que mais compram, comparação entre segmentos A/B/C, variação de vendas por mês/ano, estatísticas da coluna `CL_FHL`, etc.)*

---

## 📄 Licença

Projeto acadêmico, desenvolvido para fins educacionais na Turma T6.

