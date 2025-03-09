import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set style for better aesthetics
sns.set(style='whitegrid')

# Judul Dashboard
st.title("🌍 Dashboard Analisis Kualitas Udara")

# Load dataset
df = pd.read_csv("/Users/rizqiamaliakartika/PYTHON/DICODING/Submission_mc219d5x1732/dashboard/PRSA_Data_Dingling_20130301-20170228.csv")

# Konversi kolom waktu jika belum bertipe datetime
df['hour'] = pd.to_numeric(df['hour'], errors='coerce')

def format_number(num):
    return f"{num:,.2f}" if not np.isnan(num) else "-"

# Menampilkan ringkasan data
with st.expander("🔍 Lihat Data Mentah"):
    st.dataframe(df.head())

# Menampilkan metrik utama
col1, col2, col3 = st.columns(3)
col1.metric("📊 Jumlah Data", len(df))
col2.metric("💨 Rata-rata PM2.5", format_number(df['PM2.5'].mean()) + " µg/m³")
col3.metric("☔ Rata-rata Curah Hujan", format_number(df['RAIN'].mean()) + " mm")

# Visualisasi Hubungan Hujan dan Polusi
st.subheader("☔ Hubungan Curah Hujan dan Polusi")
pollutant = st.selectbox("Pilih Polutan", ["PM2.5", "PM10", "NO2", "O3", "SO2", "CO"], index=0)
fig, ax = plt.subplots(figsize=(8,5))
sns.scatterplot(x=df["RAIN"], y=df[pollutant], alpha=0.5, color='royalblue', ax=ax)
ax.set_xlabel("Hujan (mm)")
ax.set_ylabel(f"{pollutant} (µg/m³)")
ax.set_title(f'Hubungan Curah Hujan dengan {pollutant}')
st.pyplot(fig)

# Analisis Berdasarkan Curah Hujan
st.subheader("🌧️ Analisis Polusi Berdasarkan Kategori Hujan")
df['Kategori_Hujan'] = pd.cut(df['RAIN'], bins=[0, 5, 20, 50, np.inf], 
                              labels=['Tanpa Hujan', 'Hujan Ringan', 'Hujan Sedang', 'Hujan Lebat'])
pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
fig, axes = plt.subplots(2, 3, figsize=(12,6))
for i, pol in enumerate(pollutants):
    row, col = i // 3, i % 3
    sns.boxplot(x=df['Kategori_Hujan'], y=df[pol], palette='Blues', ax=axes[row, col])
    axes[row, col].set_title(f'Polutan {pol}')
plt.tight_layout()
st.pyplot(fig)

# Polusi Berdasarkan Waktu
st.subheader("🕒 Pola Polusi Udara Berdasarkan Waktu")
if 'hour' in df.columns:
    df_hourly = df.groupby('hour')[['PM2.5', 'NO2', 'O3']].mean()
    fig, ax = plt.subplots(figsize=(8,5))
    sns.lineplot(data=df_hourly, palette='coolwarm', linewidth=2, ax=ax)
    ax.set_title("Pola Polusi Udara Berdasarkan Jam")
    ax.set_xlabel("Jam")
    ax.set_ylabel("Kadar Polusi (µg/m³)")
    st.pyplot(fig)
else:
    st.warning("Data tidak memiliki informasi waktu (hour) untuk analisis ini.")



