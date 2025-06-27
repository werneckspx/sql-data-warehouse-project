"""
Módulo: dashboard_vendas.py

Este módulo implementa um dashboard interativo de vendas utilizando a biblioteca Streamlit,
permitindo a visualização e análise de dados de vendas, clientes e produtos.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

# --- Configuração do Ambiente ---

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))

# Importa as funções específicas para carregar o engine do banco de dados e os dados gold.
from data_loader import get_db_engine, load_gold_data

# --- Configurações da Página do Streamlit ---
st.set_page_config(page_title="Dashboard de Vendas Avançado", layout="wide", initial_sidebar_state="expanded")

st.title("Dashboard ")

st.markdown(
    """
    <style>
    /* Fonte moderna e clean */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #f0f2f6;
        background-color: #111827;
    }

    /* Barra lateral escura e sem borda */
    .css-1d391kg {
        background-color: ##0d1f3d;
        border-right: 1px solid #1e293b;
    }

    /* Títulos elegantes */
    h1, h2, h3 {
        font-weight: 700;
        color: #f9fafb;
    }

    /* Cards de KPI com efeito glassmorphism */
    .stMetric {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        padding: 20px;
        border-radius: 16px;
        transition: all 0.3s ease-in-out;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }

    .stMetric:hover {
        transform: scale(1.02);
        border-color: #38bdf8;
    }

    /* Containers dos gráficos com padding e sombra */
    .element-container {
        padding: 3px;
        border-radius: 3px;
        background-color: #00000;
        box-shadow: 0 4px 8px rgba(0,0,0,0);
        margin-bottom: 3px;
    }

    /* Rodapé e header */
    footer, header, .css-18ni7ap {
        background-color: transparent !important;
    }

    /* Botões e inputs mais arredondados */
    button, .stButton>button, input, .stDateInput input {
        border-radius: 2px !important;
    }

    /* Destaque para seleção de filtro */
    .stSelectbox, .stDateInput {
        background-color: #000000 !important;
    }

    /* Animação de entrada suave */
    .element-container, .stMetric {
        animation: fadeIn 0.5s ease-in-out;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Borda lateral de destaque */
    .block-container::before {
        content: "";
        position: fixed;
        left: 0;
        top: 0;
        height: 100vh;
        width: 4px;
        background: linear-gradient(180deg, #0ea5e9, #6366f1);
        z-index: 999;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# --- Função de Carregamento e Pré-processamento de Dados ---
@st.cache_data # Cache para evitar recarregar dados a cada interação do usuário
def load_data():
    """
    Carrega, processa e consolida os dados de vendas, produtos e clientes.

    Esta função realiza as seguintes etapas:
    1. Conecta-se ao banco de dados e carrega os DataFrames de clientes, produtos e vendas.
    2. Trata possíveis erros durante o carregamento dos dados e garante o fechamento da conexão.
    3. Converte colunas de data para o tipo datetime.
    4. Realiza junções (merge) entre os DataFrames para criar um DataFrame consolidado.
    5. Garante que colunas numéricas essenciais estejam no formato correto e trata valores.
    6. Calcula o lucro por unidade e o lucro total.
    7. Cria uma coluna 'order_month' para análise temporal.
    8. Calcula a idade dos clientes e os agrupa em faixas etárias.

    Returns:
        pd.DataFrame: O DataFrame consolidado e pré-processado pronto para análise.
    """
    # Crie o engine do DB para conexão.
    engine = get_db_engine()

    # Carregue os dados de cada tabela.
    try:
        gold_data = load_gold_data(engine)
        df_customers = gold_data['customers']
        df_products = gold_data['products']
        df_sales = gold_data['sales']

    except Exception as e:
        # Captura e imprime qualquer erro que ocorra durante o carregamento dos dados.
        print(f"Não foi possível carregar os dados: {e}")
        st.error(f"Erro ao carregar os dados: {e}. Por favor, verifique a conexão com o banco de dados.")
        st.stop() 
    finally:
        # Garante que a conexão com o banco de dados seja sempre fechada.
        engine.dispose()
        print("Conexão com o banco de dados encerrada no notebook.")

    # Converter colunas de data para o formato datetime para permitir operações de data.
    for df_temp in [df_customers, df_products, df_sales]:
        for col in df_temp.columns:
            if 'date' in col or 'dt' in col:
                df_temp[col] = pd.to_datetime(df_temp[col], errors='coerce')

    # Primeiro, junta vendas com produtos.
    sales_with_products = pd.merge(
        df_sales,
        df_products[['product_key', 'product_number', 'product_name', 'product_cost', 'category', 'subcategory', 'product_line']],
        on='product_key',
        how='left'
    )
    # Depois, junta o resultado com os dados dos clientes.
    full_df = pd.merge(sales_with_products, df_customers, on='customer_key', how='left')

    # Garantir tipos numéricos e preencher NaNs para cálculos financeiros e de quantidade.
    full_df['product_cost'] = pd.to_numeric(full_df['product_cost'], errors='coerce').fillna(0)
    full_df['sls_price'] = pd.to_numeric(full_df['sls_price'], errors='coerce').fillna(0)
    full_df['quantity'] = pd.to_numeric(full_df['quantity'], errors='coerce').fillna(0)
    full_df['sales_amount'] = pd.to_numeric(full_df['sales_amount'], errors='coerce').fillna(0)

    # Calcular o Lucro para cada transação.
    full_df['unit_profit'] = full_df['sls_price'] - full_df['product_cost']
    full_df['total_profit'] = full_df['unit_profit'] * full_df['quantity']

    # Criar 'order_month' para gráficos de tempo, convertendo para o primeiro dia do mês.
    full_df['order_month'] = full_df['order_date'].dt.to_period('M').dt.to_timestamp()
    
    # Calcular idade do cliente e agrupá-los em faixas etárias.
    current_year = pd.Timestamp.now().year
    full_df['age'] = (pd.to_datetime(f'{current_year}-01-01') - full_df['birthdate']).dt.days / 365.25
    full_df['age_group'] = pd.cut(full_df['age'], bins=[0, 18, 25, 35, 50, 65, 100],
                                     labels=['0-18', '19-25', '26-35', '36-50', '51-65', '65+'], right=False)

    return full_df

df = load_data()

# Remover registros com NaN ou com a string 'n/a' em colunas críticas para garantir a integridade dos gráficos.
colunas_criticas = ['gender', 'country', 'category', 'product_line', 'product_name', 'age_group']

df = df[~df[colunas_criticas].isin(['n/a']).any(axis=1)]
df = df.dropna(subset=colunas_criticas)

# --- Sidebar para Filtros de Análise ---
st.sidebar.header("Filtros de Análise")

# Filtro de Gênero do Cliente.
gender_options = ['Todos'] + sorted(df['gender'].unique().tolist())
selected_gender = st.sidebar.selectbox("Gênero do Cliente", gender_options)

# Filtro de País do Cliente.
country_options = ['Todos'] + sorted(df['country'].unique().tolist())
selected_country = st.sidebar.selectbox("País do Cliente", country_options)

# Filtro de Categoria de Produto.
category_options = ['Todas'] + sorted(df['category'].unique().tolist())
selected_category = st.sidebar.selectbox("Categoria de Produto", category_options)

# Filtro de Linha de Produto.
product_line_options = ['Todas'] + sorted(df['product_line'].unique().tolist())
selected_product_line = st.sidebar.selectbox("Linha de Produto", product_line_options)

# Filtro de Período das Vendas - Entrada manual de datas.
st.sidebar.markdown("### Período das Vendas")

min_date = df['order_date'].min().date()
max_date = df['order_date'].max().date()

start_date = st.sidebar.date_input("Data Inicial", min_value=min_date, max_value=max_date, value=min_date)
end_date = st.sidebar.date_input("Data Final", min_value=min_date, max_value=max_date, value=max_date)

# Validação do período de datas selecionado.
if start_date > end_date:
    st.sidebar.error("❌ A data inicial deve ser anterior à data final.")
    st.stop() # Interrompe a execução para evitar erros nos gráficos.

# --- Aplicação dos Filtros ---
filtered_df = df.copy()

# Agrupa os dados por mês e linha de produto para análise temporal.
sales_time_series = filtered_df.groupby(['order_month', 'product_line'])['sales_amount'].sum().reset_index()

# Aplica os filtros selecionados pelo usuário.
if selected_gender != 'Todos':
    filtered_df = filtered_df[filtered_df['gender'] == selected_gender]
if selected_country != 'Todos':
    filtered_df = filtered_df[filtered_df['country'] == selected_country]
if selected_category != 'Todas':
    filtered_df = filtered_df[filtered_df['category'] == selected_category]
if selected_product_line != 'Todas':
    filtered_df = filtered_df[filtered_df['product_line'] == selected_product_line]
    
# Aplica o filtro de data.
filtered_df = filtered_df[
    (filtered_df['order_date'].dt.date >= start_date) &
    (filtered_df['order_date'].dt.date <= end_date)
]

# --- Verificação de Dados Após Filtros ---
if filtered_df.empty:
    st.warning("Nenhum dado encontrado com os filtros selecionados. Tente ajustar os filtros.")
    st.stop() 

# --- 1. KPIs (Key Performance Indicators) no Topo ---

col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)

# Calcula os valores dos KPIs.
total_sales = filtered_df['sales_amount'].sum()
total_profit = filtered_df['total_profit'].sum()
num_customers = filtered_df['customer_key'].nunique()
num_orders = filtered_df['order_number'].nunique()

# Exibe os KPIs com formatação monetária e de números.
col_kpi1.metric("💰 Total de Vendas", f"R$ {total_sales:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
col_kpi2.metric("💸 Lucro Total", f"R$ {total_profit:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
col_kpi3.metric("👥 Clientes Únicos", f"{num_customers:,}".replace(",", "."))
col_kpi4.metric("📦 Pedidos Únicos", f"{num_orders:,}".replace(",", "."))


# --- 2. Visualizações (Layout em Colunas) ---

col1, col2, col3 = st.columns(3)

with col1:
    #st.subheader("Evolução do Lucro ao Longo do Tempo")
    # Agrupa os dados por mês para o gráfico de linha de lucro.
    time_series_data = filtered_df.groupby('order_month').agg(
        total_sales=('sales_amount', 'sum'),
        total_profit=('total_profit', 'sum')
    ).reset_index()

    fig_time_series = px.line(
        time_series_data,
        x='order_month',
        y=['total_profit'], 
        title='Lucro por Mês',
        labels={'value': 'Total de Lucro (R$)', 'order_month': 'Mês', 'variable': 'Métrica'},
        markers=True,
        color_discrete_sequence=["#1c7022"]  # Cor azul para o lucro
    )
    fig_time_series.update_layout(hovermode="x unified") 
    st.plotly_chart(fig_time_series, use_container_width=True)

with col2:
    #st.subheader("Top 10 Produtos por Lucro")
    profit_by_product = filtered_df.groupby(['product_number', 'product_name'])['total_profit'].sum().reset_index()
    profit_by_product = profit_by_product.sort_values(by='total_profit', ascending=False).head(10)

    fig_top_products_profit = px.bar(
        profit_by_product,
        x='total_profit',
        y='product_name',
        orientation='h', 
        title='Produtos Mais Lucrativos',
        labels={'total_profit': 'Lucro Total (R$)', 'product_name': 'Produto'},
        color='total_profit', 
        color_continuous_scale=px.colors.sequential.Greens
    )
    fig_top_products_profit.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_top_products_profit, use_container_width=True)
    
with col3:
    #st.subheader("Lucro por País do Cliente")
    sales_by_country = filtered_df.groupby('country')['total_profit'].sum().reset_index()

    fig_country_bar = px.bar(
        sales_by_country.sort_values('total_profit', ascending=False),
        x='country',
        y='total_profit',
        title='Total de Lucro por País',
        labels={'total_profit': 'Total de Lucro (R$)', 'country': 'País'},
        color='total_profit',
        color_continuous_scale=px.colors.sequential.Greens
    )
    st.plotly_chart(fig_country_bar, use_container_width=True)

col4 = st.columns(1)[0]

with col4:
    #st.subheader("Distribuição de Vendas por Categoria e Subcategoria")
    
    sales_by_cat_subcat = filtered_df.groupby(['category', 'subcategory'])['sales_amount'].sum().reset_index()

    fig_treemap = px.treemap(
        sales_by_cat_subcat,
        path=[px.Constant("Todas as Categorias"), 'category', 'subcategory'], 
        values='sales_amount',
        title='Vendas por Categoria e Subcategoria',
        color='sales_amount',
        color_continuous_scale='Blues'
    )
    fig_treemap.update_layout(margin = dict(t=50, l=25, r=25, b=25)) 
    st.plotly_chart(fig_treemap, use_container_width=True)

col5, col6 = st.columns(2)

with col5:
    #st.subheader("Distribuição de Clientes por Faixa Etária")
    
    age_group_data = filtered_df['age_group'].value_counts().reset_index()
    age_group_data.columns = ['age_group', 'count'] 

    ordered_age_groups = ['0-18', '19-25', '26-35', '36-50', '51-65', '65+']
    age_group_data['age_group'] = pd.Categorical(age_group_data['age_group'], categories=ordered_age_groups, ordered=True)
    age_group_data = age_group_data.sort_values('age_group')

    fig_age_distribution = px.bar(
        age_group_data,
        x='age_group',
        y='count',
        title='Clientes por Faixa Etária',
        labels={'age_group': 'Faixa Etária', 'count': 'Número de Clientes'}
    )
    st.plotly_chart(fig_age_distribution, use_container_width=True)

with col6:
    #st.subheader("Itens Mais Vendidos (Quantidade)")
    top_sold_items = filtered_df.groupby(['product_name', 'category'])['quantity'].sum().reset_index()
    top_sold_items = top_sold_items.sort_values(by='quantity', ascending=False).head(10)

    fig_top_items_qty = px.bar(
        top_sold_items,
        x='quantity',
        y='product_name',
        orientation='h',
        title='Produtos Mais Vendidos por Quantidade',
        labels={'quantity': 'Quantidade Total Vendida', 'product_name': 'Produto'},
        color='quantity',
        color_continuous_scale=px.colors.sequential.Plasma
    )
    fig_top_items_qty.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_top_items_qty, use_container_width=True)
    
col7 = st.columns(1)[0]

with col7:
    
    #st.subheader("Evolução de Vendas por Linha de Produto")
    fig_line_time_series = px.line(
        sales_time_series,
        x='order_month',
        y='sales_amount',
        color='product_line',
        title='Vendas Mensais por Linha de Produto',
        labels={
            'order_month': 'Mês do Pedido',
            'sales_amount': 'Total de Vendas (R$)',
            'product_line': 'Linha de Produto'
        },
        markers=True
    )

    fig_line_time_series.update_layout(
        xaxis_title='Mês',
        yaxis_title='Vendas (R$)',
        hovermode='x unified',
        legend_title_text='Linha de Produto'
    )

    st.plotly_chart(fig_line_time_series, use_container_width=True)

# --- Seção para Dados Brutos ---

st.subheader("Dados Brutos Filtrados (Primeiras 100 linhas)")
st.dataframe(filtered_df.head(100))

