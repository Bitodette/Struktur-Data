# Struktur Data: Implementasi Pencarian Linear & Binary Search pada Dataset Paper

Repositori ini berisi program Python untuk mencari data paper akademik menggunakan **algoritma Linear Search dan Binary Search**. Data paper diambil otomatis dari Google Spreadsheet (format CSV).

---

## Daftar File

- `search_papers.py`  
  Program utama untuk pencarian data paper menggunakan Linear Search dan Binary Search.

---

## Cara Menjalankan

1. **Pastikan memiliki Python 3.x**  
2. **Jalankan program di terminal:**
   ```sh
   python search_papers.py
   ```
3. **Ikuti menu interaktif** untuk memilih kriteria pencarian (judul, tahun, penulis), masukkan kata kunci, dan pilih metode pencarian (Linear/Binary).

---

## Penjelasan Singkat

- **Struktur Data:**  
  Data paper dibaca dari Google Sheets CSV dan disimpan sebagai list of dict (dictionary per paper).

- **Fitur Pencarian:**
  - *Linear Search:*  
    Mencari satu per satu, cocok untuk pencarian substring (judul/penulis/tahun).
  - *Binary Search:*  
    Data diurutkan dulu, pencarian exact match (judul/penulis/tahun), efisien untuk data besar.

- **Hasil Pencarian:**  
  Ditampilkan lengkap di terminal, termasuk semua kolom penting (judul, tahun, penulis, abstrak, dsb).

---

## Sumber Data

- Data diambil otomatis dari Google Spreadsheet:  
  [Sheet CSV Link](https://docs.google.com/spreadsheets/d/17ru4XAU2NloE9Dfxr2PC1BVcsYkLLT5r7nPSsiOFlvQ/export?format=csv&gid=743838712)

---

## Tentang

Tugas UTS Struktur Data  
Universitas Sultan Ageng Tirtayasa  
Oleh: Muhammad Faried Risky Feriawan (3337240084)  
Dosen: Cakra Adipura Wicaksana, S.T., M.T
