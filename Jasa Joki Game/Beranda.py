# ================================================================
# File: Beranda.py (main_app.py)
# Deskripsi:
# Modul antarmuka pengguna utama (landing page) untuk aplikasi
# pemesanan jasa joki game. Dibuat menggunakan framework Streamlit.
# Halaman ini berfungsi sebagai panduan awal dan informasi umum.
# ================================================================

import streamlit as st
from datetime import datetime


def main():
    # ------------------------------------------------------------
    # Konfigurasi awal halaman Streamlit
    # - Judul halaman, ikon, dan tata letak lebar penuh
    # ------------------------------------------------------------
    st.set_page_config(page_title="Beranda", page_icon="🏠", layout="wide")

    # Header utama
    st.title("👋 Selamat Datang di Aplikasi Joki Game")

    # ------------------------------------------------------------
    # Banner pengenalan aplikasi
    # - Menggunakan HTML untuk gaya tampilan yang lebih menarik
    # ------------------------------------------------------------
    st.markdown(
        """
    <div style='
        text-align: center;
        font-size: 18px;
        padding: 15px;
        background-color: #2c2f33;
        color: #ffffff;
        border-radius: 10px;
        border: 1px solid #23272a;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        margin-bottom: 20px;
    '>
        💡 <b>Tempat mudah dan cepat untuk memesan jasa joki berbagai game!</b><br>
        📲 Saat ini tersedia untuk <b>Mobile Legends, PUBG Mobile, dan Free Fire</b>.
    </div>
    """,
        unsafe_allow_html=True
    )

    # ------------------------------------------------------------
    # Penjelasan fitur-fitur utama aplikasi
    # - Ditampilkan secara informatif kepada pengguna
    # ------------------------------------------------------------
    st.markdown("## 🎮 Fitur Aplikasi")
    st.markdown("""
    - 📝 **Pemesanan**: Isi formulir untuk memesan joki dengan sistem rank otomatis.
    - 🛒 **Riwayat Order (Admin)**: Lihat Riwayat Order.
    - 📊 **Statistik Pendapatan (Admin)**: Lihat performa joki dan data transaksi.
    """)

    # ------------------------------------------------------------
    # Petunjuk penggunaan aplikasi (user guidance)
    # ------------------------------------------------------------
    st.markdown("## 📋 Cara Menggunakan")
    st.markdown("""
    1. Klik menu **Pemesanan** di sidebar.
    2. Isi detail akun dan target rank.
    3. Lakukan pembayaran sesuai instruksi.
    4. Pantau status pesanan via kontak admin.

    > **Catatan:** Admin bisa login untuk melihat statistik pemesanan di halaman khusus.
    """)

    # ------------------------------------------------------------
    # Waktu akses terakhir sebagai informasi tambahan
    # ------------------------------------------------------------
    st.markdown("---")
    st.markdown(
        f"🕒 Akses terakhir: `{datetime.now().strftime('%d %B %Y %H:%M:%S')}`")

    # ------------------------------------------------------------
    # Informasi kontak tambahan (opsional)
    # ------------------------------------------------------------
    st.markdown("### 📞 Kontak")
    st.markdown("📱 WhatsApp: [Chat Admin](https://wa.link/c27nhu)")
    st.markdown("📧 Email: admin@jokigame.com")


# Menjalankan fungsi utama jika file ini diakses langsung
if __name__ == "__main__":
    main()
