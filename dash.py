import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np

# Config
st.set_page_config(
    page_title="Dashboard Avançado de Vendas",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard Avançado de Vendas")
st.markdown("Simulação de análise de dados em ambiente real")

# Gerando dados automáticos 
np.random.seed(42)

datas = pd.date_range(start="2026-04-25", periods=120)
produtos = ["Notbook", "Mouse", "Teclado", "Monitor", "Cama", "Armário"]
categorias = ["Eletronicos", "Móveis"]

dados = []

for data in datas:
    produto = np.random.choice(produtos)
    categoria = "Eletronicos" if produto in ["Notbook", "Mouse", "Teclado", "Monitor"] else "Móveis"
    valor = np.random.randint(50, 4000)
    quantidade = np.random.randint(1, 5)

    dados.append([data, produto, categoria, valor, quantidade])

df = pd.DataFrame(dados, columns=["data", "produto", "categoria", "valor", "quantidade"])

df['faturamento'] = df['valor'] * df['quantidade']
df['mes'] = df['data'].dt.to_period('M').astype(str)

# Sidebar
st.sidebar.header("🔎 Filtros")

categoria = st.sidebar.multiselect(
    "Categoria",
    df['categoria'].unique(),
    default=df['categoria'].unique()
)

periodo = st.sidebar.date_input(
    "Periodo",
    [df['data'].min(), df['data'].max()]
)

df_filtrado = df[
    (df['categoria'].isin(categoria)) &
    (df['data'] >= pd.to_datetime(periodo[0])) &
    (df['data'] <= pd.to_datetime(periodo[1]))
]

# KPIS com variação

faturamento_total = df_filtrado['faturamento'].sum()

faturamento_mes = df_filtrado.groupby('mes')['faturamento'].sum()

if len(faturamento_mes) > 1:
        variacao = ((faturamento_mes.iloc[-1] - faturamento_mes.iloc[-2]) / faturamento_mes.iloc[-2]) * 100
else:
      variacao = 0

ticket_medio = df_filtrado['faturamento'].mean()
qtd_total = df_filtrado['quantidade'].sum()

col1, col2, col3 = st.columns(3)

col1.metric("💰 Faturamento", f"R$ {faturamento_total:,.2f}", f"{variacao:.2f}%")
col2.metric("📈 Ticket Médio", f"R$ {ticket_medio:,.2f}")
col3.metric("📦 Quantidade", qtd_total)

st.divider()

# Gráficos
col4, col5 = st.columns(2)

fig1 = px.bar(
     df_filtrado.groupby('produto')['faturamento'].sum().reset_index(),
     x= 'produto',
     y='faturamento',
     title="Faturamento por produto", 
     text_auto=True
)

col4.plotly_chart(fig1, use_container_width=True)

fig2 = px.pie(
      df_filtrado,
      names='categoria',
      values='faturamento',
      title="Distribuição por Categoria",
      hole=0.5
)

col5.plotly_chart(fig2, use_container_width=True)

# Evolução
st.subheader("📈 Evolução Mensal")

fig3 = px.line(
      df_filtrado.groupby('mes')['faturamento'].sum().reset_index(),
      x='mes',
      y='faturamento',
      markers=True
)

st.plotly_chart(fig3, use_container_width=True)

# Comparação mes a mes
st.subheader("📊 Comparação Mês a Mês")

comparacao = df_filtrado.groupby('mes')['faturamento'].sum().pct_change() * 100

st.bar_chart(comparacao)

#Download
st.subheader("📥 Exportar Dados")

csv = df_filtrado.to_csv(index=False).encode('utf-8')

st.download_button(
      label="Baixar CSV",
      data=csv,
      file_name="dados_filtrados.csv",
      mime="text/csv"
)

# Tabela

st.subheader("📋 Dados")
st.dataframe(df_filtrado, use_container_width=True)






