# ================================================================
# File: model.py
# Deskripsi: Modul ini menerapkan pemrograman berorientasi objek (OOP)
# untuk mendefinisikan struktur data dan perilaku entitas order joki game.
# ================================================================

import datetime
from abc import ABC, abstractmethod

# ============================
# ABSTRACTION & INHERITANCE
# ============================


class BaseOrder(ABC):
    """Abstract base class untuk semua jenis order.
    Menggunakan modul 'abc' untuk menetapkan kontrak perilaku
    yang wajib diimplementasikan oleh subclass.
    """

    @abstractmethod
    def to_dict(self) -> dict:
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass

# ============================
# CLASS UTAMA: OrderJoki
# ============================


class OrderJoki(BaseOrder):
    """Merepresentasikan satu entitas order jasa joki game.
    Menerapkan prinsip OOP: encapsulation, abstraction, polymorphism.
    """

    def __init__(
        self,
        nama_pelanggan: str,
        email: str,
        password: str,
        no_hp: str,
        game: str,
        rank_awal: str,
        rank_tujuan: str,
        harga_total: int,
        metode_pembayaran: str,
        tanggal_order: datetime.datetime | str | None = None,
        id_order: int | None = None
    ):
        self.id = id_order
        self.nama_pelanggan = nama_pelanggan.strip() or "Tanpa Nama"
        self._email = email.strip()                 # Encapsulation
        self._password = password.strip()           # Encapsulation
        self._no_hp = no_hp.strip()                 # Encapsulation
        self.game = game.strip()
        self.rank_awal = rank_awal.strip()
        self.rank_tujuan = rank_tujuan.strip()
        self.metode_pembayaran = metode_pembayaran.strip()
        self._harga_total = self._validate_harga(harga_total)
        self.tanggal_order = self._parse_tanggal(tanggal_order)

    # ============================
    # ENCAPSULATION: Property Getter/Setter
    # ============================

    @property
    def email(self):
        return self._email

    @property
    def no_hp(self):
        return self._no_hp

    @property
    def harga_total(self):
        return self._harga_total

    @harga_total.setter
    def harga_total(self, value):
        self._harga_total = self._validate_harga(value)

    # Validasi harga agar selalu integer positif
    def _validate_harga(self, harga_total):
        try:
            harga_int = int(harga_total)
            if harga_int < 0:
                print("⚠️  Peringatan: Harga tidak boleh negatif.")
                return 0
            return harga_int
        except (ValueError, TypeError):
            print("⚠️  Peringatan: Nilai harga_total tidak valid.")
            return 0

    # ============================
    # ABSTRACTION: Parsing input tanggal
    # ============================

    def _parse_tanggal(self, tanggal_input):
        if isinstance(tanggal_input, datetime.datetime):
            return tanggal_input
        elif isinstance(tanggal_input, str):
            for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
                try:
                    dt = datetime.datetime.strptime(tanggal_input, fmt)
                    # Jika hanya tanggal tanpa jam, tambahkan waktu sekarang
                    if fmt == "%Y-%m-%d":
                        now = datetime.datetime.now()
                        dt = dt.replace(
                            hour=now.hour, minute=now.minute, second=now.second)
                    return dt
                except ValueError:
                    continue
            print("⚠️  Format tanggal salah. Gunakan 'YYYY-MM-DD [HH:MM:SS]'.")
        return datetime.datetime.now()

    # ============================
    # POLYMORPHISM: Override __repr__
    # ============================

    def __repr__(self) -> str:
        try:
            import locale
            locale.setlocale(locale.LC_ALL, 'id_ID.UTF-8')
            harga_str = locale.format_string(
                "%d", self._harga_total, grouping=True)
        except:
            harga_str = f"{self._harga_total:,}"

        return (
            f"OrderJoki(ID: {self.id}, Nama: '{self.nama_pelanggan}', Email: '{self._email}', "
            f"Game: '{self.game}', Rank: {self.rank_awal} → {self.rank_tujuan}, "
            f"Harga: Rp{harga_str}, Metode: {self.metode_pembayaran}, "
            f"Tanggal: {self.tanggal_order.strftime('%Y-%m-%d %H:%M:%S')})"
        )

    # ============================
    # POLYMORPHISM: to_dict()
    # ============================

    def to_dict(self) -> dict:
        return {
            "id_order": self.id,
            "nama_pelanggan": self.nama_pelanggan,
            "email": self._email,
            "password": self._password,  # Disimpan dalam plaintext karena prototipe
            "no_hp": self._no_hp,
            "game": self.game,
            "rank_awal": self.rank_awal,
            "rank_tujuan": self.rank_tujuan,
            "harga_total": self._harga_total,
            "metode_pembayaran": self.metode_pembayaran,
            "tanggal_order": self.tanggal_order.strftime("%Y-%m-%d %H:%M:%S")
        }
