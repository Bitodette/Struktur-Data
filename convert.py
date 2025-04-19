import pandas as pd
import sqlite3
import os

# --- Variabel Konfigurasi ---
excel_file_path = r"C:\Users\Literataa\Downloads\Struktur_Data_Dataset_Kelas_A_B_C (51).xlsx"
excel_sheet_name = 'Sheet1'
sqlite_db_path = 'papers_database.db'
table_name = 'papers'
if_exists_option = 'replace' # Untuk replace tabel jika sudah ada
excel_header_row = 0 # baris pertama (index 0) = header

def convert_xlsx_to_sqlite(excel_path, sheet_name, header_row, db_path, table_name, if_exists='fail'):
    """Membaca data dari file Excel dan menyimpannya ke tabel SQLite."""
    print(f"Membaca file Excel: {excel_path}")
    print(f"Menggunakan Sheet: '{sheet_name or 'Default'}'")
    print(f"Mencari Header di baris Excel ke-{header_row + 1} (indeks {header_row})")

    try:
        # Membaca file
        df = pd.read_excel(excel_path, sheet_name=sheet_name, header=header_row)
        print(f"Berhasil membaca {len(df)} baris data dari Excel.")

        # Membersihkan nama kolom
        original_columns = df.columns.tolist()
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace(r'[^a-z0-9_]', '', regex=True)
        cleaned_columns = df.columns.tolist()

        # Menghapus kolom 'unnamed' jika ada
        columns_to_drop = ['unnamed_11', 'unnamed_12']
        existing_columns_to_drop = [col for col in columns_to_drop if col in df.columns]

        if existing_columns_to_drop:
            df = df.drop(columns=existing_columns_to_drop)
        else:
            print(f"Kolom {columns_to_drop} tidak ditemukan, tidak ada yang dihapus.")
            print("-" * 30)

        # Peringatan jika ada nama kolom kosong setelah pembersihan
        if '' in df.columns:
             print("PERINGATAN: Ada nama kolom yang kosong setelah dibersihkan. Periksa header Excel.")

    except FileNotFoundError:
        print(f"Error: File Excel tidak ditemukan di '{excel_path}'")
        return
    except ValueError as ve: # Menampilkan error jika sheet tidak ada
         if 'Worksheet' in str(ve) and 'not found' in str(ve):
             print(f"Error: Sheet '{sheet_name}' tidak ditemukan di '{excel_path}'.")
         else:
             print(f"Error saat membaca file Excel: {ve}")
         return
    except Exception as e:
        print(f"Error saat membaca file Excel: {e}")
        return

    conn = None 
    print(f"\nMenyambungkan ke database SQLite: {db_path}")
    try:
        # Membuat koneksi ke database SQLite
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor() 

        print(f"Menulis data ke tabel {table_name}")
        # Menulis DataFrame ke tabel SQLite
        df.to_sql(table_name, conn, if_exists=if_exists, index=False)

        print(f"Berhasil")
        conn.commit() # Commit perubahan

    except sqlite3.Error as e:
        print(f"Error SQLite: {e}")
        if conn:
            conn.rollback() # Rollback jika error
    except Exception as e:
        print(f"Error saat menulis ke database: {e}")
        if conn:
            conn.rollback()
    finally:
        # Menutup koneksi database
        if conn:
            conn.close()
            print("Tutup koneksi db.")

# --- Eksekusi Konversi ---
if __name__ == "__main__":
    # Cek apakah file Excel ada
    if not os.path.exists(excel_file_path):
         print(f"KESALAHAN FATAL: File Excel tidak ditemukan di '{excel_file_path}'. Skrip dihentikan.")
    else:
        convert_xlsx_to_sqlite(
            excel_path=excel_file_path,
            sheet_name=excel_sheet_name,
            header_row=excel_header_row,
            db_path=sqlite_db_path,
            table_name=table_name,
            if_exists=if_exists_option
        )
        print("\nkonversi selesai.")
