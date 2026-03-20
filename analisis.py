import pandas as pd
import matplotlib.pyplot as plt

# cargar dataset
df = pd.read_csv("amazon.csv")

# =====================
# LIMPIEZA DE DATOS
# =====================

# limpiar precios
df["discounted_price"] = df["discounted_price"].str.replace("₹", "").str.replace(",", "").astype(float)
df["actual_price"] = df["actual_price"].str.replace("₹", "").str.replace(",", "").astype(float)

# limpiar porcentaje
df["discount_percentage"] = df["discount_percentage"].str.replace("%", "").astype(float)

# convertir rating y cantidad de reviews
df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
df["rating_count"] = pd.to_numeric(df["rating_count"], errors="coerce")

# simplificar categoría (MUY IMPORTANTE)
df["main_category"] = df["category"].str.split("|").str[0]

# =====================
# ANÁLISIS
# =====================

print("\n--- TOP PRODUCTOS POR RATING ---")
top_rating = df.sort_values("rating", ascending=False)[["product_name", "rating"]].head(10)
print(top_rating)

print("\n--- PRODUCTOS MÁS CAROS ---")
top_price = df.sort_values("discounted_price", ascending=False)[["product_name", "discounted_price"]].head(10)
print(top_price)

print("\n--- RATING PROMEDIO POR CATEGORÍA ---")
rating_cat = df.groupby("main_category")["rating"].mean().sort_values()
print(rating_cat)

print("\n--- DESCUENTO PROMEDIO ---")
print(df["discount_percentage"].mean())

# =====================
# GRÁFICO
# =====================

rating_cat.plot(kind="barh")
plt.title("Rating promedio por categoría")
plt.xlabel("Rating")
plt.ylabel("Categoría")
plt.show()

top_confiables = df[df["rating_count"] > 100].sort_values("rating", ascending=False)[["product_name", "rating", "rating_count"]].head(10)

print("\n--- PRODUCTOS CONFIABLES (MUCHAS REVIEWS) ---")
print(top_confiables)