import streamlit as st
import pandas as pd
import plotly.express as px
from awDb import get_data_from_db

# Mendapatkan data dari tabel baru
sales_fact_df = get_data_from_db("""
    SELECT 
        fis.OrderDateKey AS time_key, 
        fis.ProductKey AS product_key, 
        fis.SalesAmount AS LineTotal, 
        fis.OrderQuantity AS OrderQty,
        fis.UnitPrice, 
        dt.FullDateAlternateKey AS fulldates,
        dt.CalendarYear AS years
    FROM 
        factinternetsales fis
    JOIN 
        dimtime dt ON fis.OrderDateKey = dt.TimeKey
""")
product_fact_df = get_data_from_db("""
    SELECT 
        dp.ProductKey AS id, 
        dp.EnglishProductName AS name, 
        dpc.EnglishProductCategoryName AS category 
    FROM 
        dimproduct dp
    JOIN 
        dimproductsubcategory dps ON dp.ProductSubcategoryKey = dps.ProductSubcategoryKey
    JOIN 
        dimproductcategory dpc ON dps.ProductCategoryKey = dpc.ProductCategoryKey
""")

# Konversi kolom tanggal
sales_fact_df['fulldates'] = pd.to_datetime(sales_fact_df['fulldates'])

# Sidebar options
st.sidebar.header('Options')

# Memilih tahun
selected_year = st.sidebar.selectbox('Select Year', sales_fact_df['years'].unique())

# Filter data berdasarkan tahun yang dipilih
filtered_sales_fact_df = sales_fact_df[sales_fact_df['years'] == selected_year]

# Data untuk plot tren penjualan harian
sales_time_df = filtered_sales_fact_df.copy()

# Gabungkan data penjualan dengan data produk
sales_product_df = pd.merge(filtered_sales_fact_df, product_fact_df, left_on='product_key', right_on='id')

# Data untuk plot pie kontribusi kategori
category_sales_df = sales_product_df.groupby('category').agg({'LineTotal': 'sum'}).reset_index()

# Data untuk histogram distribusi penjualan
sales_time_hist_df = sales_time_df['LineTotal']

# Judul utama dashboard
st.title('Sales Dashboard')

# Layout dengan kolom
col1, col2 = st.columns([2, 3])  # Mengatur lebar kolom

# Kolom pertama (sisi kiri)
with col1:
    # Plot Tren Penjualan Harian menjadi Scatter Plot dengan warna kategori
    st.header('Tren Penjualan Harian (Scatter Plot)')
    daily_sales = sales_time_df.groupby('fulldates').agg({'LineTotal': 'sum'}).reset_index()
    scatter_fig = px.scatter(daily_sales, x='fulldates', y='LineTotal', color=daily_sales['fulldates'].dt.month_name(), title='Tren Penjualan Harian')
    st.plotly_chart(scatter_fig)
    st.write("Scatter plot ini menunjukkan bagaimana penjualan berubah setiap harinya sepanjang tahun yang dipilih. Pola ini dapat membantu mengidentifikasi tren musiman atau hari-hari dengan penjualan tertinggi.")
    st.write("Kesimpulan: Dari tahun ke tahun, penjualan mengalami naik turun, di awal tahun trend penjualan nya adalah naik, namun cenderung tidak signifikan. namun di tahun 2002 mengalami penjualan menurun, namun setelah itu malah terjadi lonjakan penjualan di tahun 2003 dan tahun selanjutnya memberikan gambaran tren penjualan yang naik")

# Kolom kedua (sisi kanan)
with col2:
    # Top 10 Produk Terlaris
    st.header('Top 10 Produk Terlaris')
    top_products = sales_product_df.groupby('name').agg({'LineTotal': 'sum'}).nlargest(10, 'LineTotal').reset_index()
    for index, row in top_products.iterrows():
        progress_percent = row['LineTotal'] / top_products['LineTotal'].max()
        st.write(f"{row['name']} - Total Penjualan: {row['LineTotal']}")
        st.progress(progress_percent)
    st.write("Bagian ini menampilkan produk-produk dengan total penjualan tertinggi sepanjang tahun yang dipilih. Ini membantu mengidentifikasi produk-produk yang paling populer di kalangan pelanggan.")
