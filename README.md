# UTS Struktur Data - Pencarian Paper

Proyek ini berisi dua skrip Python yang berfungsi untuk mengelola data paper penelitian dari file Excel dan menyediakan fitur pencarian.

## Daftar Skrip

1.  **convert.py**  
    Skrip untuk mengonversi data dari file Excel (.xlsx) ke dalam basis data SQLite (.db).  
    - Membaca file Excel dan sheet tertentu.  
    - Memasukkan data yang telah dibersihkan ke dalam tabel SQLite.  

2.  **search_papers.py**  
    Skrip untuk mencari data paper di dalam basis data SQLite.  
    - Mendukung pencarian berdasarkan kolom tertentu (judul paper, tahun terbit, dan nama penulis).  
    - Mendukung dua metode pencarian:  
      - Linear Search (pencarian baris demi baris)  
      - Binary Search (dengan melakukan sorting terlebih dahulu untuk kolom terkait)  
    - Menampilkan hasil pencarian yang mencakup No, NIM, Nama Mahasiswa, Sumber Database, Fokus Kata Kunci, Judul Paper, Tahun Terbit, Nama Penulis, Abstrak, dan Kesimpulan.  

## Persiapan

1.  Install Python 3.x.  
2.  Install library pandas (digunakan oleh convert.py):
    ```bash
    pip install pandas
    ```
3.  sqlite3 merupakan library bawaan Python, tidak perlu di-install terpisah.

## Cara Menggunakan

1.  **Clone Repositori:**  
    Clone repositori ini dari GitHub:
    ```bash
    git clone https://github.com/Bitodette/Struktur-Data.git
    ```
    Masuk ke direktori proyek:
    ```bash
    cd Struktur-Data
    ```

2.  **Konversi Excel ke Database:**  
    Jalankan skrip convert.py untuk membuat atau meng-update basis data SQLite:
    ```bash
    python convert.py
    ```
    - Secara default, file database yang dihasilkan bernama `papers_database.db`.

3.  **Lakukan Pencarian Data Paper:**  
    Jalankan skrip search_papers.py untuk melakukan pencarian data paper:
    ```bash
    python search_papers.py
    ```
    - Ikuti instruksi yang muncul di layar untuk memilih kolom, metode pencarian, dan memasukkan kata kunci.
