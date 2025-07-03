# ================================================================
# File: pages/2_Riwayat_Order.py
# Deskripsi:
# Menyediakan fitur manajemen dan visualisasi riwayat order jasa joki.
# Hanya dapat diakses oleh admin melalui sistem autentikasi.
# ================================================================

import pandas as pd
import streamlit as st
from manajer_order import ManajerOrderJoki  # Manajemen data order
from admin_auth import AdminAuthenticator   # Sistem autentikasi berbasis OOP


def main():
    # ------------------------------------------------------------
    # Konfigurasi dasar halaman
    # ------------------------------------------------------------
    st.set_page_config(page_title="Riwayat Order",
                       page_icon="🛒", layout="wide")

    # ------------------------------------------------------------
    # Autentikasi Admin: Gunakan autentikator khusus untuk admin
    # ------------------------------------------------------------
    auth = AdminAuthenticator()
    auth.login_sidebar(key_prefix="riwayat")

    # ------------------------------------------------------------
    # Pembatasan Akses: Halaman hanya bisa diakses oleh admin
    # ------------------------------------------------------------
    if not auth.is_logged_in():
        st.error("❌ Halaman ini hanya untuk admin.")
        st.stop()

    # ------------------------------------------------------------
    # Judul halaman dan sapaan personal
    # ------------------------------------------------------------
    st.title("📜 Riwayat Order Pelanggan")
    st.caption(f"Selamat datang, admin **{auth.get_username()}**!")

    # ------------------------------------------------------------
    # Inisialisasi manajer order untuk mengambil data order
    # ------------------------------------------------------------
    manajer = ManajerOrderJoki()
    df = manajer.get_dataframe_order()

    # ============================================================
    # SECTION: Tampilkan Data Order
    # ============================================================
    if df.empty:
        st.warning("Belum ada data order.")
    else:
        # Format harga menjadi Rupiah (pemformatan numerik)
        df["harga_total"] = df["harga_total"].apply(
            lambda x: f"Rp {int(x):,}".replace(",", ".")
        )

        # Format tanggal menjadi DD-MM-YYYY HH:MM
        df["tanggal_order"] = pd.to_datetime(
            df["tanggal_order"]
        ).dt.strftime("%d-%m-%Y %H:%M")

        # Ganti nama kolom untuk ditampilkan kepada pengguna
        df = df.rename(columns={
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
        })

        # Jadikan kolom "ID" sebagai indeks tabel
        df = df.set_index("ID")

        # Tampilkan tabel data menggunakan komponen Streamlit
        st.dataframe(df, use_container_width=True)

        # ========================================================
        # SECTION OPSIONAL: Hapus Order (CRUD Delete)
        # ========================================================
        with st.expander("🗑️ Hapus Order (Opsional)", expanded=False):
            id_hapus = st.number_input(
                "Masukkan ID Order yang ingin dihapus", min_value=1, step=1
            )
            if st.button("Hapus Order", key="hapus_riwayat_btn"):
                if manajer.hapus_order(id_hapus):
                    st.success(
                        f"✅ Order dengan ID {id_hapus} berhasil dihapus.")
                    st.rerun()  # Refresh halaman setelah penghapusan
                else:
                    st.error("❌ Gagal menghapus. ID tidak ditemukan.")


# Menjalankan fungsi utama jika file ini dipanggil
main()
