# ================================================================
# File: setup_db_joki.py
# Deskripsi: Skrip inisialisasi awal untuk membuat folder dan
# database SQLite yang akan digunakan oleh aplikasi layanan joki game.
# Berfungsi sebagai setup mandiri sebelum aplikasi dijalankan.
# ================================================================

import sqlite3
import os
from konfigurasi import DB_PATH  # Mengimpor path database dari file konfigurasi

# Fungsi untuk membuat folder penyimpanan database jika belum ada


def buat_folder_data():
    folder_data = os.path.dirname(DB_PATH)
    try:
        if not os.path.exists(folder_data):
            os.makedirs(folder_data)
            print(f"📁 Folder data dibuat: {folder_data}")
        else:
            print(f"📁 Folder data sudah ada: {folder_data}")
    except Exception as e:
        print(f"Error saat membuat folder data: {e}")

# Fungsi utama untuk membuat database dan tabel orders_joki


def setup_database():
    print(f"\n📦 Memeriksa/membuat database di: {DB_PATH}")
    conn = None
    try:
        # Membuka koneksi ke database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Membuat tabel utama jika belum ada
        print("📑 Membuat tabel 'orders_joki' jika belum ada...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders_joki (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama_pelanggan TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL,
                no_hp TEXT NOT NULL,
                game TEXT NOT NULL,
                rank_awal TEXT NOT NULL,
                rank_tujuan TEXT NOT NULL,
                harga_total INTEGER NOT NULL,
                metode_pembayaran TEXT NOT NULL,
                tanggal_order TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        print("Tabel 'orders_joki' siap digunakan.")
        return True
    except sqlite3.Error as e:
        print(f"❌ ERROR SQLite saat setup: {e}")
        return False
    except Exception as e:
        print(f"❌ ERROR tak terduga saat setup: {e}")
        return False
    finally:
        if conn:
            conn.close()
            print("Koneksi database ditutup.")


# Menjalankan setup jika file ini dijalankan secara langsung
if __name__ == "__main__":
    print("=== Memulai Setup Database Order Joki Game ===")
    buat_folder_data()
    if setup_database():
        print(f"\n Setup database '{os.path.basename(DB_PATH)}'...")
        print("=== Setup Selesai ===")
    else:
        print("Setup Database GAGAL.")
