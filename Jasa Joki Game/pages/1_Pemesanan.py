# ================================================================
# File: pages/1_Pemesanan.py
# Deskripsi:
# Modul antarmuka pengguna untuk proses pemesanan jasa joki game.
# Menerapkan prinsip form handling dan integrasi dengan objek OOP.
# ================================================================

import streamlit as st
from datetime import datetime
# Manajer order sebagai logika bisnis
from manajer_order import ManajerOrderJoki
from model import OrderJoki  # Representasi data pesanan berbasis OOP
from konfigurasi import DAFTAR_RANK_PER_GAME, METODE_PEMBAYARAN


def main():
    # ------------------------------------------------------------
    # Konfigurasi awal halaman Streamlit
    # ------------------------------------------------------------
    st.set_page_config(page_title="Pemesanan Joki",
                       page_icon="🕹️", layout="wide")

    # ------------------------------------------------------------
    # Inisialisasi objek manajer sebagai jembatan ke database
    # ------------------------------------------------------------
    manajer = ManajerOrderJoki()

    st.title("📝 Pemesanan dan Pembayaran Joki")

    # ============================================================
    # SECTION: PILIHAN GAME & RANK
    # Menyesuaikan rank berdasarkan game yang dipilih
    # ============================================================
    st.subheader("🎮 Pilih Game dan Rank")

    game = st.selectbox(
        "Pilih Game", ["-- Pilih Game --"] + list(DAFTAR_RANK_PER_GAME.keys()))
    rank_list = DAFTAR_RANK_PER_GAME.get(game, [])

    # Validasi awal untuk mencegah pengisian rank tanpa memilih game
    if game == "-- Pilih Game --":
        st.warning("🔔 Pilih game terlebih dahulu untuk menampilkan daftar rank.")
        rank_awal = rank_tujuan = "--"
    else:
        rank_awal = st.selectbox("Rank Awal", ["-- Rank Awal --"] + rank_list)
        rank_tujuan = st.selectbox(
            "Rank Tujuan", ["-- Rank Tujuan --"] + rank_list[::-1])

    # ============================================================
    # SECTION: FORMULIR PEMESANAN
    # Mengumpulkan informasi pelanggan dan memproses input
    # ============================================================
    with st.form("form_order", clear_on_submit=True):
        st.subheader("📋 Formulir Pemesanan")

        nama = st.text_input("Nama Pelanggan")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        no_hp = st.text_input("Nomor HP / WA")
        metode = st.selectbox("Metode Pembayaran", [
                              "-- Pilih --"] + METODE_PEMBAYARAN)
        tanggal = st.date_input("Tanggal Order", datetime.today())

        # ------------------------------------------------------------
        # Otomatisasi: Hitung harga jika pilihan lengkap
        # ------------------------------------------------------------
        if (
            game != "-- Pilih Game --"
            and rank_awal not in ["", "-- Rank Awal --"]
            and rank_tujuan not in ["", "-- Rank Tujuan --"]
        ):
            harga = manajer.hitung_harga_otomatis(game, rank_awal, rank_tujuan)
            st.info(f"💰 Total Harga : Rp {harga:,}")
        else:
            harga = 0

        # ------------------------------------------------------------
        # Tombol simpan order: Validasi dan pemrosesan
        # ------------------------------------------------------------
        submit = st.form_submit_button("Simpan Order")

        if submit:
            # Validasi input
            if (
                not nama or not email or not password or not no_hp
                or game == "-- Pilih Game --"
                or rank_awal.startswith("--") or rank_tujuan.startswith("--")
                or metode == "-- Pilih --"
            ):
                st.error("❌ Harap lengkapi semua kolom sebelum menyimpan.")
            else:
                # Inisialisasi objek OOP untuk data order
                order = OrderJoki(
                    nama_pelanggan=nama,
                    email=email,
                    password=password,
                    no_hp=no_hp,
                    game=game,
                    rank_awal=rank_awal,
                    rank_tujuan=rank_tujuan,
                    harga_total=harga,
                    metode_pembayaran=metode,
                    tanggal_order=tanggal.strftime("%Y-%m-%d")
                )

                # Simpan ke database melalui manajer
                if manajer.tambah_order(order):
                    st.success("✅ Order berhasil disimpan!")
                else:
                    st.error("❌ Gagal menyimpan order.")


# Menjalankan fungsi utama
main()
