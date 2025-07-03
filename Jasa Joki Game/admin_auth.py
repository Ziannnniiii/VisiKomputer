# ================================================================
# File: admin_auth.py
# Deskripsi:
# Modul ini mengatur autentikasi admin berbasis Streamlit sidebar.
# Menerapkan konsep OOP (abstraction & inheritance) melalui kelas
# autentikasi berbasis antarmuka (interface) dan implementasi konkrit.
# ================================================================

import streamlit as st
from abc import ABC, abstractmethod


# ================================================================
# ABSTRACT AUTHENTICATOR
# ---------------------------------------------------------------
# Kelas abstrak yang mendefinisikan kontrak untuk sistem autentikasi.
# Bertujuan agar struktur autentikasi bisa diperluas di masa depan.
# ================================================================

class BaseAuthenticator(ABC):
    @abstractmethod
    def login_sidebar(self, key_prefix: str = "auth"):
        """Menampilkan antarmuka login di sidebar Streamlit."""
        pass

    @abstractmethod
    def is_logged_in(self) -> bool:
        """Mengembalikan status autentikasi."""
        pass

    @abstractmethod
    def get_username(self) -> str | None:
        """Mengambil username yang sedang login."""
        pass

    @abstractmethod
    def logout(self):
        """Menghapus status login dari session."""
        pass


# ================================================================
# IMPLEMENTASI: AdminAuthenticator
# ---------------------------------------------------------------
# Kelas ini menangani proses login/logout admin menggunakan sidebar
# Streamlit. Mengambil data kredensial dari file konfigurasi .secrets.toml
# ================================================================

class AdminAuthenticator(BaseAuthenticator):
    def __init__(self):
        # Mengambil kredensial admin dari file konfigurasi Streamlit
        self._credentials = st.secrets.get("admin_accounts", {})

        # Inisialisasi session state jika belum tersedia
        if "is_admin" not in st.session_state:
            st.session_state["is_admin"] = False
        if "admin_username" not in st.session_state:
            st.session_state["admin_username"] = None

    def login_sidebar(self, key_prefix="auth"):
        """Menampilkan form login dan tombol logout di sidebar Streamlit."""
        with st.sidebar:
            st.markdown("### 🔐 Panel Admin")

            if self.is_logged_in():
                # Jika sudah login, tampilkan status dan tombol logout
                st.success(f"✅ Login sebagai: {self.get_username()}")
                if st.button("Logout", key=f"{key_prefix}_logout_btn"):
                    self.logout()
                    st.rerun()
            else:
                # Form login jika belum login
                username = st.text_input(
                    "Username", key=f"{key_prefix}_username")
                password = st.text_input(
                    "Password", type="password", key=f"{key_prefix}_password")
                if st.button("Login", key=f"{key_prefix}_login_btn"):
                    # Proses autentikasi: cek ke dictionary dari .secrets
                    if username in self._credentials and password == self._credentials[username]:
                        st.session_state["is_admin"] = True
                        st.session_state["admin_username"] = username
                        st.success("✅ Login berhasil!")
                        st.rerun()
                    else:
                        st.error("❌ Username atau password salah.")

    def is_logged_in(self) -> bool:
        """Cek apakah admin sedang login berdasarkan session state."""
        return st.session_state.get("is_admin", False)

    def get_username(self) -> str | None:
        """Ambil nama pengguna admin dari session."""
        return st.session_state.get("admin_username")

    def logout(self):
        """Reset session untuk keluar dari mode admin."""
        st.session_state["is_admin"] = False
        st.session_state["admin_username"] = None
