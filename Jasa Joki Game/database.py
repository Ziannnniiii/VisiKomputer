# ================================================================
# File: database.py
# Deskripsi: Modul ini mengatur koneksi ke database SQLite dan
# menyediakan fungsi-fungsi untuk operasi CRUD terhadap tabel
# 'orders_joki'. Modul ini mendukung alur kerja aplikasi berbasis OOP.
# ================================================================

import sqlite3
import pandas as pd
from konfigurasi import DB_PATH
from model import OrderJoki
from typing import Optional
import datetime

# Fungsi pembantu untuk membuat koneksi ke database SQLite


def get_db_connection() -> sqlite3.Connection | None:
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10,
                               detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row  # Agar hasil query bisa diakses seperti dictionary
        return conn
    except sqlite3.Error as e:
        print(f"ERROR [database.py] Koneksi DB gagal: {e}")
        return None

# Menjalankan query umum (insert, update, delete)


def execute_query(query: str, params: Optional[tuple] = None, return_type="rowcount"):
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        conn.commit()

        if return_type == "lastrowid":
            return cursor.lastrowid
        elif return_type == "rowcount":
            return cursor.rowcount
        else:
            return True
    except sqlite3.Error as e:
        print(f"ERROR [database.py] Query gagal: {e} | Query: {query[:60]}")
        conn.rollback()
        return None
    finally:
        conn.close()

# Menjalankan query SELECT dan mengembalikan hasil


def fetch_query(query: str, params: Optional[tuple] = None, fetch_all: bool = True):
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        return cursor.fetchall() if fetch_all else cursor.fetchone()
    except sqlite3.Error as e:
        print(f"ERROR [database.py] Fetch gagal: {e}")
        return None
    finally:
        conn.close()

# Mengambil hasil SELECT dalam bentuk DataFrame (untuk statistik/tabel)


def get_dataframe(query: str, params: Optional[tuple] = None) -> pd.DataFrame:
    conn = get_db_connection()
    if not conn:
        return pd.DataFrame()
    try:
        return pd.read_sql_query(query, conn, params=params)
    except Exception as e:
        print(f"ERROR [database.py] Gagal baca ke DataFrame: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

# Inisialisasi database (pembuatan tabel jika belum ada)


def setup_database_initial() -> bool:
    print(f"📦 Setup database: {DB_PATH}")
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        query = """
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
        """
        cursor.execute(query)
        conn.commit()
        print("✅ Tabel 'orders_joki' siap digunakan.")
        return True
    except sqlite3.Error as e:
        print(f"ERROR [database.py] Setup gagal: {e}")
        return False
    finally:
        conn.close()

# Menambahkan data pesanan baru ke database


def insert_order(order_data: dict) -> int | None:
    query = """
        INSERT INTO orders_joki 
        (nama_pelanggan, email, password, no_hp, game, rank_awal, rank_tujuan, harga_total, metode_pembayaran, tanggal_order)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    params = (
        order_data["nama_pelanggan"],
        order_data["email"],
        order_data["password"],
        order_data["no_hp"],
        order_data["game"],
        order_data["rank_awal"],
        order_data["rank_tujuan"],
        order_data["harga_total"],
        order_data["metode_pembayaran"],
        order_data["tanggal_order"]
    )
    return execute_query(query, params, return_type="lastrowid")

# Mengambil semua data pesanan (berurutan dari yang terbaru)


def get_all_orders() -> list[sqlite3.Row] | None:
    query = "SELECT * FROM orders_joki ORDER BY tanggal_order DESC;"
    return fetch_query(query)

# Mengubah baris data menjadi objek OrderJoki (berbasis class OOP)


def order_row_to_obj(row: sqlite3.Row) -> OrderJoki:
    return OrderJoki(
        nama_pelanggan=row["nama_pelanggan"],
        email=row["email"],
        password=row["password"],
        no_hp=row["no_hp"],
        game=row["game"],
        rank_awal=row["rank_awal"],
        rank_tujuan=row["rank_tujuan"],
        harga_total=row["harga_total"],
        metode_pembayaran=row["metode_pembayaran"],
        tanggal_order=row["tanggal_order"],
        id_order=row["id"]
    )

# Mengubah seluruh data ke dalam bentuk list of objects


def get_all_orders_as_objects() -> list[OrderJoki]:
    rows = get_all_orders()
    return [order_row_to_obj(row) for row in rows] if rows else []

# Menghapus data pesanan berdasarkan ID


def delete_order_by_id(order_id: int) -> bool:
    query = "DELETE FROM orders_joki WHERE id = ?"
    affected = execute_query(query, (order_id,), return_type="rowcount")
    return affected is not None and affected > 0

# Melakukan update terhadap data pesanan tertentu


def update_order(order_id: int, data: dict) -> bool:
    allowed_keys = {
        "nama_pelanggan", "email", "password", "no_hp", "game",
        "rank_awal", "rank_tujuan", "harga_total", "metode_pembayaran"
    }
    update_fields = []
    params = []

    for key in data:
        if key in allowed_keys:
            update_fields.append(f"{key} = ?")
            params.append(data[key])

    if not update_fields:
        print("Tidak ada field yang valid untuk diupdate.")
        return False

    query = f"""
        UPDATE orders_joki
        SET {', '.join(update_fields)}
        WHERE id = ?;
    """
    params.append(order_id)

    result = execute_query(query, tuple(params))
    return result is not None and result > 0
