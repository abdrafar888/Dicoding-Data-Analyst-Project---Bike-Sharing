import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style='darkgrid')


def load_data_day():
    return pd.read_csv("data/day.csv")

def load_data_hour():
    return pd.read_csv("data/hour.csv")

day_df = load_data_day()
hour_df = load_data_hour()

if "dteday" in day_df.columns:
    day_df["dteday"] = pd.to_datetime(day_df["dteday"])

min_date_days = day_df["dteday"].min()
max_date_days = day_df["dteday"].max()

st.sidebar.title("Navigasi Halaman")
page = st.sidebar.radio("Pilih Halaman:", ["Rata-rata Penyewaan Berdasarkan Jam", "Total Penyewaan Harian", "Analisis Penyewaan per Tahun"])

if page == "Rata-rata Penyewaan Berdasarkan Jam":
    st.title("Rata-rata Penyewaan Sepeda Berdasarkan Jam 🕒")
    
    hour_filter = st.sidebar.slider(
        "Pilih Rentang Jam:",
        min_value=int(hour_df["hr"].min()),
        max_value=int(hour_df["hr"].max()),
        value=(int(hour_df["hr"].min()), int(hour_df["hr"].max()))
    )

    filtered_data_hour = hour_df[
        hour_df["hr"].between(hour_filter[0], hour_filter[1])
    ]

    if "hr" in filtered_data_hour.columns and "cnt" in filtered_data_hour.columns:
        avg_rentals_by_hour = filtered_data_hour.groupby("hr")["cnt"].mean()
        fig, ax = plt.subplots(figsize=(10, 6))
        avg_rentals_by_hour.plot(kind="bar", color="skyblue", ax=ax)
        ax.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Jam (Dengan Filter)", fontsize=16)
        ax.set_xlabel("Jam dalam Sehari", fontsize=14)
        ax.set_ylabel("Rata-rata Jumlah Penyewaan", fontsize=14)
        ax.tick_params(axis="x", labelsize=12)
        ax.tick_params(axis="y", labelsize=12)
        ax.grid(axis="y", linestyle="--", alpha=0.7)
        st.pyplot(fig)
    else:
        st.error("Kolom 'hr' atau 'cnt' tidak ditemukan dalam dataset.")

elif page == "Total Penyewaan Harian":
    st.title("Total Penyewaan Sepeda Harian 🚴‍♀️")
    
    st.sidebar.image("https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/image1_hH9B4gs.jpg", width=200)
    st.sidebar.header("Filter Rentang Waktu")
    start_date, end_date = st.sidebar.date_input(
        label="Pilih Rentang Waktu:",
        min_value=min_date_days,
        max_value=max_date_days,
        value=[min_date_days, max_date_days]
    )
    
    filtered_day_df = day_df[(day_df["dteday"] >= pd.Timestamp(start_date)) & (day_df["dteday"] <= pd.Timestamp(end_date))]
    
    if not filtered_day_df.empty:
        daily_rentals = filtered_day_df.groupby("dteday")["cnt"].sum().reset_index()
        fig, ax = plt.subplots(figsize=(14, 6))
        sns.lineplot(x="dteday", y="cnt", data=daily_rentals, ax=ax)
        ax.set_title("Tren Penyewaan Sepeda Harian (Difilter Rentang Waktu)", fontsize=18)
        ax.set_xlabel("Tanggal", fontsize=14)
        ax.set_ylabel("Total Penyewaan", fontsize=14)
        plt.xticks(rotation=45, fontsize=12)
        plt.yticks(fontsize=12)
        ax.grid(axis="y", linestyle="--", alpha=0.7)
        st.pyplot(fig)
    else:
        st.warning("Tidak ada data untuk rentang waktu yang dipilih.")

elif page == "Analisis Penyewaan per Tahun":
    st.title("Analisis Penyewaan per Tahun 📊")
    
    if "dteday" in day_df.columns and "cnt" in day_df.columns:
        day_df["year"] = day_df["dteday"].dt.year
        yearly_rentals = day_df.groupby("year")["cnt"].sum()

        fig, ax = plt.subplots(figsize=(10, 6))
        yearly_rentals.plot(kind="bar", color="orange", ax=ax)
        ax.set_title("Total Penyewaan Sepeda per Tahun", fontsize=16)
        ax.set_xlabel("Tahun", fontsize=14)
        ax.set_ylabel("Total Penyewaan", fontsize=14)
        ax.grid(axis="y", linestyle="--", alpha=0.7)
        st.pyplot(fig)
    else:
        st.error("Kolom 'dteday' atau 'cnt' tidak ditemukan dalam dataset.")

st.markdown("---")
st.caption("Dashboard Penyewaan Sepeda © 2025 | Dibangun oleh Abdul Rafar")
