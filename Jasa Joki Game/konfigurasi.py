# ================================================================
# File: konfigurasi.py
# Deskripsi: Menyediakan konfigurasi global untuk aplikasi layanan
# jasa joki game, termasuk pengaturan database, daftar game, rank,
# harga layanan, dan metode pembayaran.
# ================================================================

import os

# Menentukan path dasar dari file ini (lokasi direktori saat ini)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Nama file database SQLite
NAMA_DB = 'orders_joki.db'

# Path absolut ke file database SQLite
DB_PATH = os.path.join(BASE_DIR, 'data', NAMA_DB)

# Daftar game yang didukung dalam layanan joki
DAFTAR_GAMES = ["Mobile Legends", "PUBG Mobile", "Free Fire"]

# Daftar rank resmi untuk masing-masing game
RANKS_ML = ["Warrior", "Elite", "Master", "Grandmaster",
            "Epic", "Legend", "Mythic", "Mythical Honor", "Mythical Glory", "Mythical Immortal"]
RANKS_PUBG = ["Bronze", "Silver", "Gold", "Platinum",
              "Diamond", "Crown", "Ace", "Ace Mentor", "Ace Dominator", "Conqueror"]
RANKS_FF = ["Bronze", "Silver", "Gold",
            "Platinum", "Diamond", "Heroic", "Grandmaster"]

# Struktur harga untuk setiap peningkatan rank per game
# Format: {Nama Game: {(Rank Awal, Rank Tujuan): Harga}}
HARGA_RANK_DEFAULT = {
    "Mobile Legends": {
        ("Warrior", "Elite"): 27000,
        ("Elite", "Master"): 42000,
        ("Master", "Grandmaster"): 64000,
        ("Grandmaster", "Epic"): 125000,
        ("Epic", "Legend"): 150000,
        ("Legend", "Mythic"): 175000,
        ("Mythic", "Mythical Honor"): 200000,
        ("Mythical Honor", "Mythical Glory"): 225000,
        ("Mythical Glory", "Mythical Immortal"): 600000
    },
    "PUBG Mobile": {
        ("Bronze", "Silver"): 30000,
        ("Silve", "Gold"): 50000,  # Typo: "Silve" seharusnya "Silver"
        ("Gold", "Platinum"): 75000,
        ("Platinum", "Diamond"): 100000,
        ("Diamond", "Crown"): 130000,
        ("Crown", "Ace"): 220000,
        ("Ace", "Ace Mentor"): 250000,
        ("Ace Mentor", "Ace Dominator"): 320000,
        ("Ace Dominator", "Conqueror"): 700000
    },
    "Free Fire": {
        ("Bronze", "Silver"): 18000,
        ("Silver", "Gold"): 36000,
        ("Gold", "Platinum"): 74000,
        ("Platinum", "Diamond"): 80000,
        ("Diamond", "Heroic"): 180000,
        ("Heroic", "Grandmaster"): 450000
    }
}

# Metode pembayaran digital yang diterima
METODE_PEMBAYARAN = [
    "GoPay", "OVO", "DANA", "ShopeePay"
]

# Asosiasi daftar rank per game untuk akses terstruktur
DAFTAR_RANK_PER_GAME = {
    "Mobile Legends": RANKS_ML,
    "PUBG Mobile": RANKS_PUBG,
    "Free Fire": RANKS_FF
}
