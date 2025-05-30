Claro! Aqui está a tradução completa para o português:

---

# **Convenções de Nomenclatura**

Este documento descreve as convenções de nomenclatura utilizadas para esquemas, tabelas, views, colunas e outros objetos no data warehouse.

---

## **Princípios Gerais**

* **Padrão de Nomenclatura**: Usar *snake\_case*, com letras minúsculas e sublinhado (`_`) para separar as palavras.
* **Idioma**: Utilizar o inglês para todos os nomes.
* **Evitar Palavras Reservadas**: Não utilizar palavras reservadas da linguagem SQL como nomes de objetos.

---

## **Convenções de Nomes para Tabelas**

### **Regras da Camada Bronze**

* Todos os nomes devem começar com o nome do sistema de origem, e os nomes das tabelas devem corresponder exatamente aos nomes originais (sem renomear).
* **`<sistema_origem>_<entidade>`**

  * `<sistema_origem>`: Nome do sistema de origem (ex: `crm`, `erp`).
  * `<entidade>`: Nome exato da tabela no sistema de origem.
  * Exemplo: `crm_customer_info` → Informações de clientes do sistema CRM.

### **Regras da Camada Silver**

* Mesmas regras da camada Bronze: o nome deve refletir o sistema de origem e manter o nome original da tabela.
* **`<sistema_origem>_<entidade>`**

  * Exemplo: `erp_sales_data` → Dados de vendas do sistema ERP.

### **Regras da Camada Gold**

* Todos os nomes devem ser significativos e alinhados com o negócio, iniciando com um prefixo de categoria.
* **`<categoria>_<entidade>`**

  * `<categoria>`: Define o papel da tabela, como `dim` (dimensão) ou `fact` (fato).
  * `<entidade>`: Nome descritivo da tabela, alinhado ao domínio de negócio (ex: `customers`, `products`, `sales`).
  * Exemplos:

    * `dim_customers` → Tabela de dimensão com dados de clientes.
    * `fact_sales` → Tabela fato contendo transações de vendas.

#### **Glossário de Padrões de Categoria**

| Padrão    | Significado         | Exemplo(s)                                 |
| --------- | ------------------- | ------------------------------------------ |
| `dim_`    | Tabela de dimensão  | `dim_customer`, `dim_product`              |
| `fact_`   | Tabela de fato      | `fact_sales`                               |

---

## **Convenções de Nomes para Colunas**

### **Chaves Substitutas (Surrogate Keys)**

* Toda chave primária em tabelas de dimensão deve usar o sufixo `_key`.
* **`<nome_tabela>_key`**

  * `<nome_tabela>`: Refere-se ao nome da tabela ou entidade à qual a chave pertence.
  * `_key`: Sufixo indicando que a coluna é uma chave substituta.
  * Exemplo: `customer_key` → Chave substituta na tabela `dim_customers`.

### **Colunas Técnicas**

* Toda coluna técnica deve começar com o prefixo `dwh_`, seguido de um nome descritivo indicando a função da coluna.
* **`dwh_<nome_coluna>`**

  * `dwh`: Prefixo exclusivo para metadados gerados pelo sistema.
  * `<nome_coluna>`: Nome descritivo da função da coluna.
  * Exemplo: `dwh_load_date` → Coluna técnica que armazena a data de carregamento do registro.

---

## **Procedures Armazenadas**

* Todas as procedures utilizadas para carregamento de dados devem seguir o padrão:
* **`load_<camada>`**

  * `<camada>`: Representa a camada que está sendo carregada, como `bronze`, `silver` ou `gold`.
  * Exemplo:

    * `load_bronze` → Procedure para carregamento da camada Bronze.
    * `load_silver` → Procedure para carregamento da camada Silver.
