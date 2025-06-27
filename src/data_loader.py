import pandas as pd
from sqlalchemy import create_engine
import os 

def get_db_engine():
    """Cria e retorna um engine SQLAlchemy para o banco de dados."""
    db_connection_str = os.getenv("DATABASE_URL", 
                                  "postgresql+psycopg2://postgres:felipe@localhost:5432/datawarehouse")
    engine = create_engine(db_connection_str)
    return engine

def load_gold_data(engine):
    """
    Carrega as views da camada Gold em DataFrames do Pandas.
    Args:
        engine: Um objeto SQLAlchemy Engine conectado ao banco de dados.
    Returns:
        Um dicionário contendo os DataFrames:
        {'customers': df_customers, 'products': df_products, 'sales': df_sales}
    """
    print("Carregando dados da camada Gold...")
    df_customers = pd.read_sql("SELECT * FROM gold.dim_customers", engine)
    df_products = pd.read_sql("SELECT * FROM gold.dim_products", engine)
    df_sales = pd.read_sql("SELECT * FROM gold.fact_sales", engine)

    print("Dados da camada Gold carregados com sucesso!")
    print(f"Shape df_customers: {df_customers.shape}")
    print(f"Shape df_products: {df_products.shape}")
    print(f"Shape df_sales: {df_sales.shape}")

    return {
        'customers': df_customers,
        'products': df_products,
        'sales': df_sales
    }

if __name__ == '__main__':
    engine = get_db_engine()
    try:
        gold_data = load_gold_data(engine)
        print("\nExemplo de head do DataFrame de clientes:")
        print(gold_data['customers'].head())
        print("\nExemplo de head do DataFrame de produtos:")
        print(gold_data['products'].head())
        print("\nExemplo de head do DataFrame de vendas:")
        print(gold_data['sales'].head())
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        engine.dispose()
        print("Conexão com o banco de dados encerrada.")