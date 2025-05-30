# Data Warehouse e Analytics Project

Este projeto utiliza uma arquitetura de Data Warehouse moderna baseada na Arquitetura Medallion, que organiza os dados em camadas (Bronze, Silver e Gold), com o objetivo de garantir a ingestão eficiente de dados, padronização, escabilidade e disponibilização para consumo analítico e preditivo.

### 🔧 Componentes Principais

* **📐 Arquitetura de Dados:** Estruturada com base na abordagem Medallion, permitindo um fluxo limpo e controlado de dados desde o estágio bruto até a camada pronta para consumo.
* **⚙️ Pipelines de ETL:** Automatização do processo de extração, transformação e carga dos dados provenientes de sistemas-fonte (como CRM e ERP) para o Data Warehouse.
* **🧩 Modelagem de Dados:** Criação de **tabelas fato e dimensão**, otimizadas para consultas analíticas de alta performance.
* **📊 Análises e Relatórios:** Geração de insights por meio de consultas SQL, apoiando decisões orientadas a dados.

> ✅ Desenvolvido com foco em qualidade de dados, arquitetura modular e prontidão para uso em BI e Machine Learning.

---

### 📁 1. Data Sources

Os dados são provenientes de sistemas transacionais como CRM e ERP, exportados no formato **CSV** e armazenados em **pastas locais**.

* **Formato:** Arquivos CSV
* **Interface de ingestão:** Leitura de arquivos em diretórios/folders

---

### 🟫 2. Bronze Layer – Raw Data

Nesta camada, os dados são ingeridos em seu formato original, sem qualquer tipo de transformação. Ela serve como repositório histórico bruto para rastreabilidade.

* **Tipo de Objeto:** Tabelas
* **Carga:** Batch Processing, Full Load, Truncate & Insert
* **Transformações:** Nenhuma (dados "as-is")
* **Modelo de Dados:** Não estruturado
* **Execução:** Procedures SQL automatizadas

---

### ⬜ 3. Silver Layer – Cleaned & Standardized Data

Aqui os dados passam por processos de limpeza, padronização e enriquecimento, tornando-se consistentes e prontos para análises intermediárias.

* **Tipo de Objeto:** Tabelas
* **Carga:** Batch Processing, Full Load, Truncate & Insert
* **Transformações Aplicadas:**

  * Data Cleansing (remoção de duplicatas, nulos, erros)
  * Data Standardization (formatação de datas, números, etc.)
  * Data Normalization (ajuste de escalas ou padrões)
  * Derived Columns (criação de colunas)
  * Data Enrichment (inclusão de informações complementares)
* **Modelo de Dados:** Ainda não modelado (intermediário)
* **Execução:** Procedures SQL

---

### 🟨 4. Gold Layer – Business-Ready Data

Camada otimizada para o consumo. Os dados são integrados e modelados segundo lógicas de negócio, prontos para análises em ferramentas de BI e modelos de machine learning.

* **Tipo de Objeto:** Views (consultas SQL pré-definidas)
* **Carga:** Nenhuma (execução sob demanda via views)
* **Transformações Aplicadas:**

  * Data Integration (junções)
  * Aggregations 
  * Business Logic 
* **Modelo de Dados:**

  * Star Schema
  * Flat Tables
  * Aggregated Tables

---

### 📊 5. Consumption Layer – Data Consumers

Os dados da Gold Layer podem ser consumidos por diferentes aplicações e usuários finais:

* **BI & Dashboards:** Power BI, Tableau, etc.
* **Consultas Ad-Hoc:** SQL queries diretas em views
* **Machine Learning:** Dados prontos para pipelines preditivos

---

### 🎯 Benefícios da Arquitetura

* Separação clara de responsabilidades por camada
* Rastreabilidade e versionamento de dados
* Flexibilidade para diferentes tipos de consumo (BI, ML, SQL)
* Aderência a boas práticas de governança e qualidade de dados

---

## 🚀 Project Requirements

Para executar e testar este projeto de Data Warehouse, são necessários os seguintes requisitos:

### Banco de Dados

- **PostgreSQL** (utilizado 17)
  - Extensões padrão habilitadas (ex: `plpgsql`)

### Ferramentas

- **psql** (cliente de linha de comando do PostgreSQL)  
  Ou qualquer ferramenta de administração SQL compatível (utilizado pgAdmin).

### Estrutura de Diretórios

```
sql-data-warehouse-project/
│
├── datasets/
│   ├── source_crm/
│   │   ├── cust_info.csv
│   │   ├── prd_info.csv
│   │   └── sales_details.csv
│   └── source_erp/
│       ├── cust_az12.csv
│       ├── loc_a101.csv
│       └── px_cat_g1v2.csv
│
├── scripts/
│   ├── init_database_sql
│   ├── bronze/
│   │   ├── ddl_bronze.sql
│   │   └── proc_load_bronze.sql
│   ├── silver/
│   │   ├── ddl_silver.sql
│   │   └── proc_load_silver.sql
│   └── gold/
│       └── ddl_gold.sql
│
├── test/
│   ├── quality_silver_checks.sql
│   └── quality_gold_checks.sql
│
├── README.md
└── .gitignore
```

- **datasets/**: Contém os arquivos CSV de entrada, separados por origem (CRM e ERP).
- **scripts/**: Scripts SQL para criação de banco, schemas, tabelas e procedures de carga e transformação.
  - **bronze/**: Scripts para camada Bronze (dados brutos).
  - **silver/**: Scripts para camada Silver (dados tratados).
  - **gold/**: Scripts para camada Gold (views analíticas).
- **test/**: Scripts de checagem e validação da qualidade dos dados.
- **README.md**: Documentação do projeto.
- **.gitignore**: Arquivos e pastas ignorados pelo controle de versão.

---

## 👤 Sobre Mim

Olá! Meu nome é Felipe Werneck e sou um estudante de **engenharia da computação** e tenho interesse na área de engenharia e análise de dados;

Desenvolvi este projeto como parte do meu portfólio com o objetivo de:

* Aprimorar habilidades práticas em **modelagem de dados**, **SQL** e **data warehouse**;
* Demonstrar o uso da **Arquitetura Medallion** em um contexto realista;
* Praticar boas práticas de versionamento, organização e documentação de projetos de dados.

📫 **Contato**

* [LinkedIn](www.linkedin.com/in/felipe-werneck-93520a209)
* [E-mail](mailto:felipwerneck@gmail.com)

Agradeço pela visita ao projeto! 😊

> 🔍 Este projeto foi desenvolvido com base em um estudo guiado pelo tutorial de [Data with Baraa](https://www.youtube.com/@DataWithBaraa).
