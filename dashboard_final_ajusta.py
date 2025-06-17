
import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
import base64

st.set_page_config(page_title="Dashboard Pedidos Atacado", layout="wide")

# === Carregar dados ===
df = pd.read_excel("AT - Teste.xlsx")
df.columns = [
    "Pedido", "Data", "Pais", "Mes", "Cliente", "Moeda", "Cambio",
    "Subtotal_USD", "Frete_USD", "Desconto_USD", "Total_USD",
    "Subtotal_BRL", "Frete_BRL", "Desconto_BRL", "Total_BRL"
]
df["Cliente"] = df["Cliente"].str.replace("_", " ")
df["Quantidade de Pedidos"] = 1  # nome limpo

# === Sidebar: Filtro de Cliente ===
st.sidebar.header("🔍 Filtros")
clientes = df["Cliente"].unique()
cliente_sel = st.sidebar.multiselect("Selecione Cliente(s):", sorted(clientes), default=clientes)
df = df[df["Cliente"].isin(cliente_sel)]

# === Logo ===
logo_path = "logo_transstore.png"
with open(logo_path, "rb") as f:
    logo_bytes = f.read()
logo_b64 = base64.b64encode(logo_bytes).decode()
st.markdown(f"<div style='text-align:center;'><img src='data:image/png;base64,{logo_b64}' width='300'></div>", unsafe_allow_html=True)

# === Título e Visão Geral ===
st.markdown("<h1 style='font-size:30px;'>📦 Pedidos Atacado</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='font-size:22px;'>📊 Visão Geral</h2>", unsafe_allow_html=True)

# === Métricas ===
total_pedidos = len(df)
total_pedidos_brl = len(df[df["Moeda"] == "R$"])
total_pedidos_usd = len(df[df["Moeda"] == "U$"])

col1, col2, col3 = st.columns(3)
col1.markdown(f"📦 <span style='font-size:16px;'>Total de Pedidos</span><br><span style='font-size:20px; font-weight:bold; color:#222;'>{total_pedidos}</span>", unsafe_allow_html=True)
col2.markdown(f"💰 <span style='font-size:16px;'>Pedidos em R$</span><br><span style='font-size:20px; font-weight:bold; color:#222;'>{total_pedidos_brl}</span>", unsafe_allow_html=True)
col3.markdown(f"💵 <span style='font-size:16px;'>Pedidos em U$</span><br><span style='font-size:20px; font-weight:bold; color:#222;'>{total_pedidos_usd}</span>", unsafe_allow_html=True)

# === Gráfico: Pedidos por Cliente ===
st.markdown("<h3 style='font-size:22px;'>📈 Pedidos por Cliente</h3>", unsafe_allow_html=True)
pedidos_por_cliente = df.groupby("Cliente")["Quantidade de Pedidos"].sum().reset_index()
fig1 = px.bar(pedidos_por_cliente, x="Cliente", y="Quantidade de Pedidos", color="Cliente",
              color_discrete_sequence=px.colors.qualitative.Bold, height=600)
st.plotly_chart(fig1, use_container_width=True)

# === Gráfico: Evolução de Pedidos por Mês ===
st.markdown("<h3 style='font-size:22px;'>📊 Evolução de Pedidos por Mês</h3>", unsafe_allow_html=True)
ordem_meses = ["março", "abril", "maio"]
evolucao = df.groupby("Mes")["Quantidade de Pedidos"].sum().reindex(ordem_meses).reset_index()
fig2 = px.line(evolucao, x="Mes", y="Quantidade de Pedidos", markers=True,
               line_shape="spline", height=500)
fig2.update_yaxes(autorange=True)
st.plotly_chart(fig2, use_container_width=True)

# === Gráfico: Distribuição de Moeda ===
st.markdown("<h3 style='font-size:22px;'>🪙 Distribuição de Pedidos por Moeda</h3>", unsafe_allow_html=True)
moeda_agg = df.groupby("Moeda")["Quantidade de Pedidos"].sum().reset_index()
fig3 = px.pie(moeda_agg, names="Moeda", values="Quantidade de Pedidos",
              color_discrete_sequence=["#1f77b4", "#0b5fa5"], height=500)
st.plotly_chart(fig3, use_container_width=True)

# === Gráfico: Países com Mais Pedidos ===
st.markdown("<h3 style='font-size:22px;'>🌍 Países com Mais Pedidos</h3>", unsafe_allow_html=True)
ranking_paises = df.groupby("Pais")["Quantidade de Pedidos"].sum().reset_index().sort_values(by="Quantidade de Pedidos", ascending=False)
fig4 = px.bar(ranking_paises, x="Pais", y="Quantidade de Pedidos", color="Pais",
              color_discrete_sequence=px.colors.qualitative.Set3, height=600)
st.plotly_chart(fig4, use_container_width=True)

# === Receita por Moeda ===
st.markdown("<h3 style='font-size:22px;'>💰 Receita por Moeda</h3>", unsafe_allow_html=True)
receita_tipo = st.selectbox("Selecione Receita:", ["Nada", "R$", "U$"])
if receita_tipo == "R$":
    total_valor = df["Total_BRL"].sum()
    st.metric(label="Receita Total em R$", value="R$ {:,.2f}".format(total_valor))
elif receita_tipo == "U$":
    total_valor = df["Total_USD"].sum()
    st.metric(label="Receita Total em U$", value="U$ {:,.2f}".format(total_valor))
