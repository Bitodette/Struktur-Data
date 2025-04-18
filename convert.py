import pandas as pd
import sqlite3
import os

excel_file_path = r"C:/Users/Literataa/Downloads/Struktur_Data_Dataset_Kelas_A_B_C (40).xlsx"
excel_sheet_name = 'Sheet1'

sqlite_db_path = 'papers_database.db'
table_name = 'papers'

if_exists_option = 'replace'

excel_header_row = 1

def convert_xlsx_to_sqlite(excel_path, sheet_name, header_row, db_path, table_name, if_exists='fail'):
    print(f"Membaca file Excel: {excel_path}")
    print(f"Menggunakan Sheet: '{sheet_name or 'Default'}'")
    print(f"Mencari Header di baris Excel ke-{header_row + 1} (indeks {header_row})")

    try:
        df = pd.read_excel(excel_path, sheet_name=sheet_name, header=header_row)
        print(f"Berhasil membaca {len(df)} baris data dari Excel.")

        original_columns = df.columns.tolist()
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace(r'[^a-z0-9_]', '', regex=True)
        cleaned_columns = df.columns.tolist()

        print("\nNama Kolom Asli dari Excel:")
        print(original_columns)
        print("\nNama Kolom Setelah Dibersihkan:")
        print(cleaned_columns)
        print("-" * 30)

        columns_to_drop = ['unnamed_11', 'unnamed_12']
        existing_columns_to_drop = [col for col in columns_to_drop if col in df.columns]

        if existing_columns_to_drop:
            print(f"Menghapus kolom: {existing_columns_to_drop}")
            df = df.drop(columns=existing_columns_to_drop)
            print("Kolom berhasil dihapus.")
            print("\nNama Kolom Setelah Penghapusan:")
            print(df.columns.tolist())
            print("-" * 30)
        else:
            print(f"Kolom {columns_to_drop} tidak ditemukan dalam data setelah pembersihan, tidak ada yang dihapus.")
            print("-" * 30)

        if '' in df.columns:
             print("PERINGATAN: Beberapa nama kolom menjadi kosong setelah dibersihkan/dihapus. Periksa header Excel Anda.")

    except FileNotFoundError:
        print(f"Error: File Excel tidak ditemukan di '{excel_path}'")
        return
    except IndexError:
        print(f"Error: Tidak dapat menemukan header di baris ke-{header_row + 1}. Periksa 'excel_header_row'.")
        return
    except Exception as e:
        print(f"Error saat membaca file Excel: {e}")
        return

    print(f"\nMenyambungkan ke database SQLite: {db_path}")
    try:
        conn = sqlite3.connect(db_path)

        print(f"Menulis data ke tabel '{table_name}' (Mode: {if_exists})...")
        df.to_sql(table_name, conn, if_exists=if_exists, index=False)

        print(f"Berhasil mengonversi data ke tabel '{table_name}' di '{db_path}'.")

    except sqlite3.Error as e:
        print(f"Error SQLite: {e}")
    except Exception as e:
        print(f"Error saat menulis ke database: {e}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()
            print("Koneksi database ditutup.")

if __name__ == "__main__":
    if not os.path.exists(excel_file_path):
         print(f"PERINGATAN: File Excel tidak ditemukan di '{excel_file_path}'. Pastikan path sudah benar!")
    else:
        convert_xlsx_to_sqlite(
            excel_path=excel_file_path,
            sheet_name=excel_sheet_name,
            header_row=excel_header_row,
            db_path=sqlite_db_path,
            table_name=table_name,
            if_exists=if_exists_option
        )