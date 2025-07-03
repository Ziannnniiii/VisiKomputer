# ===============================================================
# File: pages/3_Statistik_Pendapatan.py
# Deskripsi:
# Halaman Streamlit ini dikhususkan untuk admin guna menampilkan
# statistik pendapatan dari jasa joki game. Fitur mencakup:
# - Filter rentang tanggal dinamis
# - Visualisasi pendapatan per game
# - Total pendapatan terhitung otomatis
# - Riwayat transaksi dalam bentuk tabel
# - Ekspor data ke format CSV
# ===============================================================

import streamlit as st
import pandas as pd
from datetime import datetime
from manajer_order import ManajerOrderJoki
from admin_auth import AdminAuthenticator


def main():
    # -----------------------------------------------------------
    # Konfigurasi dasar halaman Streamlit
    # -----------------------------------------------------------
    st.set_page_config(
        page_title="Statistik Pendapatan",
        page_icon="📊",
        layout="wide"
    )

    # -----------------------------------------------------------
    # Autentikasi Admin: Validasi identitas pengguna
    # -----------------------------------------------------------
    auth = AdminAuthenticator()
    auth.login_sidebar(key_prefix="statistik")
    if not auth.is_logged_in():
        st.error("❌ Halaman ini hanya untuk admin.")
        st.stop()

    # -----------------------------------------------------------
    # Judul dan Sapaan Dinamis
    # -----------------------------------------------------------
    st.title("📊 Statistik Pendapatan")
    st.caption(f"Hai, admin **{auth.get_username()}**!")

    # -----------------------------------------------------------
    # Ambil Data Order dari Manajer (OOP + Caching)
    # -----------------------------------------------------------
    manajer = ManajerOrderJoki()
    df = manajer.get_dataframe_order()

    if df.empty:
        st.warning("Belum ada data.")
        return

    # -----------------------------------------------------------
    # Persiapan Data: Parsing waktu dan konversi harga
    # -----------------------------------------------------------
    df["harga_total"] = df["harga_total"].astype(float)
    df["tanggal_order"] = pd.to_datetime(df["tanggal_order"])

    # ===========================================================
    # SECTION: Filter Rentang Tanggal Dinamis
    # Tujuan: Memungkinkan analisis per periode waktu tertentu
    # ===========================================================
    st.subheader("📅 Filter Tanggal")

    min_date = df["tanggal_order"].min().date()
    max_date = df["tanggal_order"].max().date()

    # Hindari error jika hanya ada 1 tanggal
    default_start = min_date
    default_end = max_date if min_date != max_date else min_date

    date_range = st.date_input(
        "Pilih rentang tanggal:",
        value=(default_start, default_end),
        min_value=min_date,
        max_value=max_date
    )

    # Validasi input pengguna
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        st.warning("Silakan pilih *dua tanggal* sebagai rentang.")
        return

    # Filter data sesuai rentang tanggal
    df_filtered = df[
        (df["tanggal_order"].dt.date >= start_date) &
        (df["tanggal_order"].dt.date <= end_date)
    ]

    if df_filtered.empty:
        st.warning("Tidak ada data pada rentang tanggal ini.")
        return

    # ===========================================================
    # SECTION: Total Pendapatan
    # Tujuan: Menyajikan total akumulasi harga dari data terfilter
    # ===========================================================
    total = df_filtered["harga_total"].sum()
    st.metric(label="💰 Total Pendapatan",
              value=f"Rp {total:,.0f}".replace(",", "."))

    # ===========================================================
    # SECTION: Grafik Pendapatan per Game
    # Tujuan: Visualisasi untuk membantu analisis performa game
    # ===========================================================
    st.subheader("🎮 Grafik Pendapatan per Game")
    pendapatan_per_game = df_filtered.groupby(
        "game")["harga_total"].sum().sort_values(ascending=False)
    st.bar_chart(pendapatan_per_game)

    # ===========================================================
    # SECTION: Tabel Riwayat Order
    # Tujuan: Memberikan tampilan rinci data transaksi
    # ===========================================================
    st.subheader("📋 Riwayat Order")

    df_display = df_filtered.copy()
    df_display["harga_total"] = df_display["harga_total"].apply(
        lambda x: f"Rp {int(x):,}".replace(",", "."))
    df_display["tanggal_order"] = df_display["tanggal_order"].dt.strftime(
        "%d-%m-%Y %H:%M")

    df_display = df_display.rename(columns={
        "id_order": "ID",
        "nama_pelanggan": "Nama",
        "email": "Email",
        "no_hp": "No. HP",
        "game": "Game",
        "rank_awal": "Rank Awal",
        "rank_tujuan": "Rank Tujuan",
        "harga_total": "Harga",
        "metode_pembayaran": "Pembayaran",
        "tanggal_order": "Tanggal"
    }).set_index("ID")

    # Sembunyikan index default dari Streamlit agar tampilan bersih
    st.markdown("""
        <style>
        .row-heading.level0, .blank {display: none;}
        </style>
    """, unsafe_allow_html=True)

    st.dataframe(df_display, use_container_width=True)

    # ===========================================================
    # SECTION: Ekspor Data ke CSV
    # Tujuan: Memberikan opsi backup atau analisis lebih lanjut
    # ===========================================================
    with st.expander("📥 Download Data"):
        st.download_button(
            label="Download sebagai CSV",
            data=df_display.reset_index().to_csv(index=False),
            file_name="riwayat_joki.csv",
            mime="text/csv"
        )


# Jalankan fungsi utama saat file ini dipanggil langsung
main()
