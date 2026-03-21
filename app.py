import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Amazon Products Dashboard 💻📊")

# cargar datos
df = pd.read_csv("amazon.csv")

# limpieza de datos
df["discounted_price"] = df["discounted_price"].str.replace("₹", "").str.replace(",", "").astype(float)
df["actual_price"] = df["actual_price"].str.replace("₹", "").str.replace(",", "").astype(float)
df["discount_percentage"] = df["discount_percentage"].str.replace("%", "").astype(float)
df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
df["rating_count"] = pd.to_numeric(df["rating_count"], errors="coerce")
df["main_category"] = df["category"].str.split("|").str[0]

# filtros interactivos
st.sidebar.header("Filtros")
category = st.sidebar.selectbox("Select Category", df["main_category"].unique())
max_price = st.sidebar.slider("Maximum Price", int(df["discounted_price"].min()), int(df["discounted_price"].max()), int(df["discounted_price"].max()))
min_rating = st.sidebar.slider("Minimum Rating", 0.0, 5.0, 3.0, 0.1)

filtered_df = df[
    (df["main_category"] == category) &
    (df["discounted_price"] <= max_price) &
    (df["rating"] >= min_rating)
]

# métricas
st.subheader("Metrics 📌")
st.write("Average rating:", round(filtered_df["rating"].mean(), 2))
st.write("Average price:", round(filtered_df["discounted_price"].mean(), 2))
st.write("Number of products:", filtered_df.shape[0])

# top productos
st.subheader("Top Products ⭐")
top_products = filtered_df.sort_values(["rating", "rating_count"], ascending=[False, False])
st.write(top_products[["product_name", "rating", "rating_count", "discounted_price"]].head(10))

# gráfico 1: rating promedio por categoría
st.subheader("Average Rating by Category 📊")
rating_cat = df.groupby("main_category")["rating"].mean().sort_values()

fig, ax = plt.subplots()
rating_cat.plot(kind="barh", ax=ax, color="skyblue")
ax.set_xlabel("Average Rating")
ax.set_ylabel("Category")
st.pyplot(fig)

# gráfico 2: precio promedio por categoría
st.subheader("Average Discounted Price by Category 💰")
price_cat = df.groupby("main_category")["discounted_price"].mean().sort_values()

fig2, ax2 = plt.subplots()
price_cat.plot(kind="barh", ax=ax2, color="lightgreen")
ax2.set_xlabel("Average Price (₹)")
ax2.set_ylabel("Category")
st.pyplot(fig2)