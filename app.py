import streamlit as st
import pandas as pd
import plotly.express as px

# Настройки страницы
st.set_page_config(
    page_title="JUNION Fashion Dashboard",
    page_icon="👗",
    layout="wide"
)

# Загрузка данных
@st.cache_data(ttl=300)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTdbFQUQMBj8Zvxx3ig-7uAaVO3NGQ54A4ux4Nv1dWWQB4x4Y0_IYkmIWB5_DyimA39fK3MNp8nftJb/pub?gid=28005582&single=true&output=csv"
    df = pd.read_csv(url)
    return df

df = load_data()

# Заголовок
st.title("👗 JUNION Fashion — Ассортиментная матрица")
st.markdown("---")

# Фильтры
col1, col2, col3, col4 = st.columns(4)

with col1:
    seasons = ["Все"] + sorted(df["Season"].dropna().unique().tolist())
    selected_season = st.selectbox("🗓 Сезон", seasons)

with col2:
    pattern_statuses = ["Все"] + sorted(df["Pattern status"].dropna().unique().tolist())
    selected_pattern = st.selectbox("🏭 Статус производства", pattern_statuses)

with col3:
    delivery_statuses = ["Все"] + sorted(df["Delivery status"].dropna().unique().tolist())
    selected_delivery = st.selectbox("🚚 Статус отгрузки", delivery_statuses)

with col4:
    categories = ["Все"] + sorted(df["Category Level 1"].dropna().unique().tolist())
    selected_category = st.selectbox("👔 Категория", categories)

# Применяем фильтры
filtered_df = df.copy()

if selected_season != "Все":
    filtered_df = filtered_df[filtered_df["Season"] == selected_season]
if selected_pattern != "Все":
    filtered_df = filtered_df[filtered_df["Pattern status"] == selected_pattern]
if selected_delivery != "Все":
    filtered_df = filtered_df[filtered_df["Delivery status"] == selected_delivery]
if selected_category != "Все":
    filtered_df = filtered_df[filtered_df["Category Level 1"] == selected_category]

# KPI карточки
st.markdown("### 📊 Общая статистика")
k1, k2, k3, k4 = st.columns(4)

k1.metric("📦 Всего артикулов", len(filtered_df))
k2.metric("👔 Категорий", filtered_df["Category Level 1"].nunique())
k3.metric("🏭 Статусов производства", filtered_df["Pattern status"].nunique())
k4.metric("🚚 Статусов отгрузки", filtered_df["Delivery status"].nunique())

st.markdown("---")

# Графики
col_g1, col_g2 = st.columns(2)

with col_g1:
    st.markdown("#### 🏭 По статусу производства")
    pattern_counts = filtered_df["Pattern status"].value_counts().reset_index()
    pattern_counts.columns = ["Статус", "Количество"]
    fig1 = px.bar(
        pattern_counts,
        x="Количество",
        y="Статус",
        orientation="h",
        color="Статус",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig1.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig1, use_container_width=True)

with col_g2:
    st.markdown("#### 👔 По категориям")
    cat_counts = filtered_df["Category Level 1"].value_counts().reset_index()
    cat_counts.columns = ["Категория", "Количество"]
    fig2 = px.pie(
        cat_counts,
        values="Количество",
        names="Категория",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig2.update_layout(height=400)
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# Таблица
st.markdown("### 📋 Таблица артикулов")

cols_to_show = [
    "Season", "Category Level 1", "Article",
    "Pattern status", "Delivery status",
    "1st sample status", "PPS status", "Moscow"
]

existing_cols = [c for c in cols_to_show if c in filtered_df.columns]
st.dataframe(filtered_df[existing_cols], use_container_width=True, height=500)

# Обновление данных
st.markdown("---")
if st.button("🔄 Обновить данные"):
    st.cache_data.clear()
    st.rerun()
