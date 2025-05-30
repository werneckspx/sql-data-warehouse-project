# Catálogo de Dados da Camada Gold

## Visão Geral

A **Camada Gold** representa os dados em nível de negócio, estruturados para dar suporte a casos de uso analíticos e de relatórios. Ela é composta por **tabelas de dimensão** e **tabelas de fato** voltadas para métricas específicas de negócio.

---

### 1. **gold.dim\_customers**

* **Finalidade:** Armazena os dados dos clientes, enriquecidos com informações demográficas e geográficas.
* **Colunas:**

| Nome da Coluna   | Tipo de Dado | Descrição                                                                                      |
| ---------------- | ------------ | ---------------------------------------------------------------------------------------------- |
| customer\_key    | INT          | Chave substituta que identifica exclusivamente cada registro de cliente na tabela de dimensão. |
| customer\_id     | INT          | Identificador numérico único atribuído a cada cliente.                                         |
| customer\_number | VARCHAR(50)  | Identificador alfanumérico do cliente, usado para rastreamento e referência.                   |
| first\_name      | VARCHAR(50)  | Primeiro nome do cliente, conforme registrado no sistema.                                      |
| last\_name       | VARCHAR(50)  | Sobrenome do cliente.                                                                          |
| country          | VARCHAR(50)  | País de residência do cliente (ex: 'Australia').                                               |
| marital\_status  | VARCHAR(50)  | Estado civil do cliente (ex: 'Married','Single').                                              |
| gender           | VARCHAR(50)  | Gênero do cliente (ex: 'Male', 'Female', 'n/a').                                               |
| birthdate        | DATE         | Data de nascimento do cliente, no formato AAAA-MM-DD (ex: 1971-10-06).                         |
| create\_date     | DATE         | Data e hora em que o registro do cliente foi criado no sistema.                                |

---

### 2. **gold.dim\_products**

* **Finalidade:** Fornece informações sobre os produtos e seus atributos.
* **Colunas:**

| Nome da Coluna        | Tipo de Dado | Descrição                                                                                       |
| --------------------- | ------------ | ----------------------------------------------------------------------------------------------- |
| product\_key          | INT          | Chave substituta que identifica exclusivamente cada produto na tabela de dimensão.              |
| product\_id           | INT          | Identificador único atribuído ao produto para rastreamento interno.                             |
| product\_number       | VARCHAR(50)  | Código alfanumérico estruturado que representa o produto, usado em categorização ou inventário. |
| product\_name         | VARCHAR(50)  | Nome descritivo do produto, incluindo detalhes como tipo, cor e tamanho.                        |
| category\_id          | VARCHAR(50)  | Identificador único da categoria do produto, usado para classificação em alto nível.            |
| category              | VARCHAR(50)  | Classificação geral do produto (ex: Bikes, Components).                                         |
| subcategory           | VARCHAR(50)  | Classificação mais detalhada do produto dentro da categoria, "tipo de produto".                 |
| maintenance\_required | VARCHAR(50)  | Indica se o produto requer manutenção (ex: 'Yes', 'No').                                        |
| product\_cost         | INT          | Custo ou preço base do produto, em unidades monetárias inteiras.                                |
| product\_line         | VARCHAR(50)  | Linha ou série específica à qual o produto pertence (ex: Estrada, Montanha).                    |
| start\_date           | DATE         | Data em que o produto se tornou disponível para venda ou uso.                                   |

---

### 3. **gold.fact\_sales**

* **Finalidade:** Armazena dados transacionais de vendas para fins analíticos.
* **Colunas:**

| Nome da Coluna | Tipo de Dado | Descrição                                                                             |
| -------------- | ------------ | ------------------------------------------------------------------------------------- |
| order\_number  | VARCHAR(50)  | Identificador alfanumérico único para cada pedido de venda (ex: 'SO54496').           |
| product\_key   | INT          | Chave substituta que liga o pedido à tabela de dimensão de produtos.                  |
| customer\_key  | INT          | Chave substituta que liga o pedido à tabela de dimensão de clientes.                  |
| order\_date    | DATE         | Data em que o pedido foi realizado.                                                   |
| shipping\_date | DATE         | Data em que o pedido foi enviado ao cliente.                                          |
| due\_date      | DATE         | Data de vencimento do pagamento do pedido.                                            |
| sales\_amount  | INT          | Valor total da venda para o item da linha, em unidades monetárias inteiras (ex: 25).  |
| quantity       | INT          | Quantidade de unidades do produto vendidas no item da linha (ex: 1).                  |
| price          | INT          | Preço unitário do produto no item da linha, em unidades monetárias inteiras (ex: 25). |