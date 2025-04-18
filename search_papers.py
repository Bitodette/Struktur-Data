import sqlite3
import time
import traceback
import os

sqlite_db_path = 'papers_database.db'
table_name = 'papers'

COL_JUDUL = 'judul_paper'
COL_TAHUN = 'tahun_terbit'
COL_PENULIS = 'nama_penulis'
COLUMNS_TO_FETCH = [COL_JUDUL, COL_TAHUN, COL_PENULIS]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def connect_db(db_path):
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        print(f"Berhasil terhubung ke database: {db_path}")
        return conn
    except sqlite3.Error as e:
        print(f"Error koneksi database: {e}")
        return None

def fetch_all_data(conn, table, columns):
    if not conn:
        print("Koneksi database tidak tersedia.")
        return []
    cursor = conn.cursor()
    safe_columns = [f'"{col}"' for col in columns]
    cols_string = ", ".join(safe_columns)
    query = f"SELECT {cols_string} FROM \"{table}\""
    print(f"Mengambil data dari tabel '{table}'...")
    try:
        cursor.execute(query)
        data = [dict(row) for row in cursor.fetchall()]
        print(f"Berhasil mengambil {len(data)} baris data.")
        return data
    except sqlite3.Error as e:
        print(f"Error saat mengambil data: {e}")
        if "no such column" in str(e): print(f"!!! KESALAHAN NAMA KOLOM? Periksa `COLUMNS_TO_FETCH`.")
        elif "no such table" in str(e): print(f"!!! KESALAHAN NAMA TABEL? Periksa `table_name`.")
        return []

def linear_search(data_list, search_term, column_key):
    results = []
    search_term_clean = str(search_term).strip().lower()
    if not search_term_clean:
        print("Kata kunci pencarian kosong.")
        return []
    start_time = time.time()
    for item in data_list:
        if column_key in item and item[column_key] is not None:
            value_str_clean = str(item[column_key]).strip().lower()
            if search_term_clean in value_str_clean:
                results.append(item)
    end_time = time.time()
    print(f"Linear Search selesai dalam {end_time - start_time:.6f} detik.")
    return results

def binary_search(sorted_data_list, search_term, column_key):
    results = []
    low = 0
    if not sorted_data_list: return []
    high = len(sorted_data_list) - 1
    found_index = -1

    try:
        if column_key == COL_TAHUN: search_term_val = float(search_term)
        else: search_term_val = str(search_term).strip().lower()
    except ValueError:
         print(f"Error: Input '{search_term}' tidak valid untuk kolom '{column_key}'.")
         if column_key == COL_TAHUN: print("Kolom tahun memerlukan input angka.")
         return []

    start_time = time.time()
    while low <= high:
        mid = (low + high) // 2
        item = sorted_data_list[mid]

        try:
            original_mid_value = item[column_key]
            if column_key == COL_TAHUN: mid_val = float(original_mid_value)
            else: mid_val = str(original_mid_value).strip().lower()
        except (ValueError, TypeError):
             if low == high : break
             if mid % 2 == 0: high = mid - 1
             else: low = mid + 1
             continue

        if mid_val == search_term_val:
            found_index = mid
            break
        elif mid_val < search_term_val:
            low = mid + 1
        else:
            high = mid - 1

    if found_index != -1:
        results.append(sorted_data_list[found_index])
        i = found_index - 1
        while i >= 0:
            item = sorted_data_list[i]
            try:
                item_val = float(item[column_key]) if column_key == COL_TAHUN else str(item[column_key]).strip().lower()
                if item_val == search_term_val:
                    results.append(item); i -= 1
                else: break
            except (ValueError, TypeError): i -= 1
        i = found_index + 1
        while i < len(sorted_data_list):
            item = sorted_data_list[i]
            try:
                item_val = float(item[column_key]) if column_key == COL_TAHUN else str(item[column_key]).strip().lower()
                if item_val == search_term_val:
                    results.append(item); i += 1
                else: break
            except (ValueError, TypeError): i += 1

    end_time = time.time()
    print(f"Binary Search selesai dalam {end_time - start_time:.6f} detik.")
    return results

if __name__ == "__main__":
    clear_screen()
    print("--- Program Pencarian Data Paper (Linear & Binary Search - Final Clean) ---")

    conn = connect_db(sqlite_db_path)
    all_data = []
    if conn:
        all_data = fetch_all_data(conn, table_name, COLUMNS_TO_FETCH)
        conn.close()
        print("Koneksi database ditutup.")

    if not all_data:
        print("\nTidak ada data yang bisa diproses. Program berhenti.")
        input("Tekan Enter untuk keluar...")
    else:
        while True:
            clear_screen()
            print("\n--- Menu Pencarian ---")
            print("Pilih kolom untuk pencarian:")
            print(f"1. Judul ({COL_JUDUL})")
            print(f"2. Tahun ({COL_TAHUN})")
            print(f"3. Penulis ({COL_PENULIS})")
            choice_col = input("Masukkan nomor kolom (atau ketik 'q' untuk keluar): ")

            if choice_col.lower() == 'q': break

            search_key = ""
            if choice_col == '1': search_key = COL_JUDUL
            elif choice_col == '2': search_key = COL_TAHUN
            elif choice_col == '3': search_key = COL_PENULIS
            else:
                print("Pilihan kolom tidak valid.")
                input("Tekan Enter untuk mencoba lagi...")
                continue

            print(f"\nAnda memilih mencari berdasarkan: {search_key.replace('_',' ').title()}")
            search_value = input(f"Masukkan kata kunci pencarian untuk '{search_key}': ")

            if not search_value.strip():
                 print("Kata kunci tidak boleh kosong.")
                 input("Tekan Enter untuk mencoba lagi...")
                 continue

            print("\nPilih metode pencarian:")
            print("1. Linear Search (Mencari jika kata kunci *ada di dalam* teks)")
            print("2. Binary Search (Mencari kecocokan *persis* setelah teks dibersihkan)")
            choice_method = input("Masukkan pilihan metode (1/2): ")

            results = []
            if choice_method == '1':
                print("\nMelakukan Linear Search...")
                results = linear_search(all_data, search_value, search_key)
            elif choice_method == '2':
                print("\nMelakukan Binary Search...")
                print(f"Memfilter data (kolom '{search_key}')...")
                filtered_data = [item for item in all_data if search_key in item and item[search_key] is not None]
                if not filtered_data:
                     print("Tidak ada data valid di kolom ini setelah filtering.")
                else:
                    print(f"Data valid tersisa: {len(filtered_data)} baris.")
                    print(f"Mengurutkan data berdasarkan '{search_key}'...")
                    start_sort_time = time.time()

                    def sort_key_func(item):
                        value = item.get(search_key)
                        processed_value = value
                        try:
                            if search_key == COL_TAHUN: processed_value = float(value)
                            elif isinstance(value, str): processed_value = value.strip().lower()
                        except (ValueError, TypeError):
                             pass
                        return processed_value

                    try:
                        sorted_data = sorted(filtered_data, key=sort_key_func)
                        end_sort_time = time.time()
                        print(f"Data diurutkan dalam {end_sort_time - start_sort_time:.4f} detik.")

                        results = binary_search(sorted_data, search_value, search_key)
                    except TypeError as te:
                          print(f"\nError Sorting Kritis: {te}")
                          print("Gunakan Linear Search atau periksa data.")
            else:
                print("Pilihan metode tidak valid.")

            print(f"\n--- Hasil Pencarian ('{search_value}' di kolom '{search_key}') ---")
            if results:
                print(f"Ditemukan {len(results)} hasil:")
                try:
                    results.sort(key=sort_key_func)
                except Exception as sort_err:
                    print(f"(Peringatan: Gagal mengurutkan hasil akhir - {sort_err})")

                for i, row in enumerate(results):
                    print(f"\n#{i+1}")
                    for col_name in COLUMNS_TO_FETCH:
                        display_value = row.get(col_name, 'N/A')
                        if isinstance(display_value, str): display_value = display_value.strip()
                        print(f"  {col_name.replace('_',' ').title():<10}: {display_value}")
                    print("-" * 15)
            else:
                print("Tidak ada hasil yang ditemukan.")

            input("\nTekan Enter untuk melanjutkan ke pencarian berikutnya...")

    print("\nProgram pencarian selesai.")
