-- ============================================================================
-- Script: quality_gold_checks.sql
-- Descrição:
--   Este script executa verificações de qualidade nos dados da camada Gold do Data Warehouse.
--   O objetivo é identificar registros de vendas (fact_sales) que não possuem correspondência
--   nas dimensões de clientes (dim_customers) ou produtos (dim_products), sinalizando possíveis
--   problemas de integridade referencial.
--
-- Objetivo:
--   Garantir a consistência e integridade dos dados analíticos, facilitando a identificação
--   de falhas de integração ou carregamento nas tabelas da camada Gold.
--
-- ============================================================================


SELECT *
FROM gold.fact_sales f
LEFT JOIN gold.dim_customers c
ON c.customer_key = f.customer_key
LEFT JOIN gold.dim_products p
ON p.product_key = f.product_key
WHERE c.customer_key IS NULL
