# ================================================================
# File: manajer_order.py
# Deskripsi: Modul ini bertanggung jawab sebagai pengelola (manager)
# dari data pesanan jasa joki. Mengimplementasikan prinsip OOP
# melalui inheritance dan abstraction.
# ================================================================

from abc import ABC, abstractmethod
from typing import List
import pandas as pd

import database
from model import OrderJoki
from konfigurasi import HARGA_RANK_DEFAULT, DAFTAR_RANK_PER_GAME


# ================================================================
# ABSTRACT BASE MANAGER
# ---------------------------------------------------------------
# Kelas dasar abstrak untuk manajer data order.
# Menjamin adanya kontrak metode yang wajib diimplementasikan oleh subclass.
# ================================================================

class BaseOrderManager(ABC):
    @abstractmethod
    def refresh_data(self):
        """Memperbarui data dari sumber (misal: database)."""
        pass

    @abstractmethod
    def tambah_order(self, order: OrderJoki) -> bool:
        pass

    @abstractmethod
    def hapus_order(self, id_order: int) -> bool:
        pass

    @abstractmethod
    def get_all_orders(self) -> List[OrderJoki]:
        pass

    @abstractmethod
    def get_dataframe_order(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def total_pendapatan(self) -> int:
        pass


# ================================================================
# IMPLEMENTASI KHUSUS UNTUK ORDER JOKI
# ---------------------------------------------------------------
# Kelas ini merepresentasikan concrete implementation dari BaseOrderManager
# dan mengatur seluruh alur CRUD serta perhitungan harga pada aplikasi.
# ================================================================

class ManajerOrderJoki(BaseOrderManager):
    def __init__(self):
        # Cache lokal agar tidak perlu akses DB terus-menerus
        self._semua_order: List[OrderJoki] = []
        self.refresh_data()

    def refresh_data(self):
        """Muat ulang data order dari database ke cache lokal."""
        self._semua_order = database.get_all_orders_as_objects()

    def tambah_order(self, order: OrderJoki) -> bool:
        """Menambahkan order ke database dan memperbarui cache."""
        if not isinstance(order, OrderJoki):
            return False

        inserted_id = database.insert_order(order.to_dict())
        if inserted_id:
            self.refresh_data()
            return True
        return False

    def hapus_order(self, id_order: int) -> bool:
        """Menghapus order berdasarkan ID dan memperbarui cache."""
        if database.delete_order_by_id(id_order):
            self.refresh_data()
            return True
        return False

    def update_order(self, id_order: int, data: dict) -> bool:
        """Melakukan pembaruan data order tertentu berdasarkan ID."""
        success = database.update_order(id_order, data)
        if success:
            self.refresh_data()
        return success

    def get_all_orders(self) -> List[OrderJoki]:
        """Mengembalikan semua order dalam bentuk list objek."""
        return self._semua_order

    def get_dataframe_order(self) -> pd.DataFrame:
        """Mengembalikan semua data order dalam bentuk DataFrame (untuk analisis/tabular)."""
        if not self._semua_order:
            return pd.DataFrame()
        return pd.DataFrame([o.to_dict() for o in self._semua_order])

    def hitung_harga_otomatis(self, game: str, rank_awal: str, rank_tujuan: str) -> int:
        """
        Menghitung total harga berdasarkan rank awal dan tujuan, 
        menggunakan peta harga di konfigurasi.
        """
        harga_total = 0
        try:
            rank_list = DAFTAR_RANK_PER_GAME.get(game)
            if not rank_list:
                return 0

            idx_awal = rank_list.index(rank_awal)
            idx_tujuan = rank_list.index(rank_tujuan)

            if idx_awal >= idx_tujuan:
                return 0

            harga_map = HARGA_RANK_DEFAULT.get(game, {})
            for i in range(idx_awal, idx_tujuan):
                dari = rank_list[i]
                ke = rank_list[i + 1]
                harga_total += harga_map.get((dari, ke), 0)

        except Exception as e:
            print(f"[ERROR] Gagal menghitung harga: {e}")
        return harga_total

    def total_pendapatan(self) -> int:
        """Menghitung total pendapatan dari seluruh order yang ada."""
        return sum(order.harga_total for order in self._semua_order)
