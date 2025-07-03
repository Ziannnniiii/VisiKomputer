@echo off
:: ================================
:: Pindah ke direktori tempat script ini berada
:: ================================
cd /d "%~dp0"

:: ================================
:: CEK VIRTUAL ENVIRONMENT
:: ================================
if not exist ".venv\" (
    echo Membuat virtual environment .venv ...
    python -m venv .venv
)

:: Aktifkan virtual environment
call .venv\Scripts\activate

:: ================================
:: CEK APAKAH SUDAH INSTALL LIBRARY
:: (gunakan file penanda agar install hanya sekali)
:: ================================
if not exist ".venv\.installed" (
    echo Menginstall pustaka eksternal...
    pip install streamlit pandas

    :: Buat file penanda bahwa sudah install
    echo installed > .venv\.installed
) else (
    echo Semua pustaka sudah terinstall.
)

:: ================================
:: JALANKAN APLIKASI DI TERMINAL BARU
:: ================================
echo Menjalankan aplikasi Streamlit ...
start cmd /k ".venv\Scripts\activate && streamlit run Beranda.py --server.fileWatcherType none"
