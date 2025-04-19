import sqlite3
import time
import traceback
import os
import sys

sqlite_db_path = 'papers_database.db'
table_name = 'papers'

ALL_DATABASE_COLUMNS = [
    "no",
    "nim",
    "nama_mahasiswa",
    "sumber_database",
    "fokus_kata_kunci_pilih_no1_atau_2_atau_3_sesuai_yg_ada_di_soal",
    "judul_paper",
    "tahun_terbit",
    "nama_penulis",
    "abstrak_langusung_copas_dari_paper",
    "kesimpulan_langusung_copas_dari_paper",
    "link_paper"
]

COL_JUDUL = 'judul_paper'
COL_TAHUN = 'tahun_terbit'
COL_PENULIS = 'nama_penulis'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def connect_db(db_path):
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        print(f"Berhasil terhubung ke database: {db_path}")
        return conn
    except sqlite3.Error as e:
        print(f"\nError koneksi database: {e}")
        print(f"Pastikan file '{db_path}' ada dan bisa diakses.")
        return None

def fetch_all_data(conn, table, columns_to_fetch):
    if not conn:
        print("Koneksi database tidak tersedia.")
        return []
    cursor = conn.cursor()
    safe_columns = [f'"{col}"' for col in columns_to_fetch]
    cols_string = ", ".join(safe_columns)
    query = f'SELECT {cols_string} FROM "{table}"'
    print(f"Mengambil data dari tabel '{table}' (Kolom: {len(columns_to_fetch)})...")
    try:
        cursor.execute(query)
        data = [dict(row) for row in cursor.fetchall()]
        print(f"Berhasil mengambil {len(data)} baris data.")
        return data
    except sqlite3.Error as e:
        print(f"\nError saat mengambil data: {e}")
        error_msg = str(e).lower()
        if "no such column" in error_msg:
             print(f"!!! KESALAHAN NAMA KOLOM? Periksa list `ALL_DATABASE_COLUMNS`.")
        elif "no such table" in error_msg:
             print(f"!!! KESALAHAN NAMA TABEL? Periksa `table_name` ('{table}').")
        return []

def linear_search(data_list, search_term, column_key):
    results = []
    search_term_clean = str(search_term).strip().lower()
    if not search_term_clean:
        print("Kata kunci pencarian kosong.")
        return []

    start_time = time.time()
    count = 0
    for item in data_list:
        if column_key in item and item[column_key] is not None:
            value_str_clean = str(item[column_key]).strip().lower()
            if search_term_clean in value_str_clean:
                results.append(item)
        count += 1

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
        if column_key == COL_TAHUN:
            try:
                search_term_val = int(search_term)
            except ValueError:
                search_term_val = float(search_term)
        else:
            search_term_val = str(search_term).strip().lower()
    except ValueError:
         print(f"\nError: Input '{search_term}' tidak valid untuk kolom '{column_key}'.")
         if column_key == COL_TAHUN: print("Kolom tahun memerlukan input angka (integer atau desimal).")
         return []

    start_time = time.time()
    while low <= high:
        mid = (low + high) // 2
        item = sorted_data_list[mid]

        try:
            original_mid_value = item.get(column_key)
            if original_mid_value is None:
                 if mid > low: high = mid - 1
                 elif mid < high: low = mid + 1
                 else: break
                 continue

            if column_key == COL_TAHUN:
                try: mid_val = int(original_mid_value)
                except ValueError: mid_val = float(original_mid_value)
            else:
                mid_val = str(original_mid_value).strip().lower()

        except (ValueError, TypeError):
             if mid > low: high = mid - 1
             elif mid < high: low = mid + 1
             else: break
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
                item_val_orig = item.get(column_key)
                if item_val_orig is None: i -= 1; continue
                if column_key == COL_TAHUN:
                    try: item_val = int(item_val_orig)
                    except ValueError: item_val = float(item_val_orig)
                else: item_val = str(item_val_orig).strip().lower()

                if item_val == search_term_val:
                    results.append(item)
                    i -= 1
                else:
                    break
            except (ValueError, TypeError):
                i -= 1
        i = found_index + 1
        while i < len(sorted_data_list):
            item = sorted_data_list[i]
            try:
                item_val_orig = item.get(column_key)
                if item_val_orig is None: i += 1; continue
                if column_key == COL_TAHUN:
                    try: item_val = int(item_val_orig)
                    except ValueError: item_val = float(item_val_orig)
                else: item_val = str(item_val_orig).strip().lower()

                if item_val == search_term_val:
                    results.append(item)
                    i += 1
                else:
                    break
            except (ValueError, TypeError):
                 i += 1

    end_time = time.time()
    print(f"Binary Search selesai dalam {end_time - start_time:.6f} detik.")
    return results

def sort_key_func(item, sort_column_key):
    value = item.get(sort_column_key)
    processed_value = value

    if value is not None:
        try:
            if sort_column_key == COL_TAHUN:
                try: processed_value = int(value)
                except ValueError: processed_value = float(value)
            elif isinstance(value, str):
                processed_value = value.strip().lower()
        except (ValueError, TypeError):
             if sort_column_key == COL_TAHUN: return float('inf')
             else: return ""
    else:
        if sort_column_key == COL_TAHUN: return float('inf')
        else: return ""

    return processed_value

if __name__ == "__main__":
    clear_screen()
    print("--- Program Pencarian Data Paper (Menampilkan Semua Kolom) ---")

    conn = connect_db(sqlite_db_path)
    all_data = []
    if conn:
        all_data = fetch_all_data(conn, table_name, ALL_DATABASE_COLUMNS)
        conn.close()
        print("Koneksi database ditutup.")

    if not all_data:
        print("\nTidak ada data yang bisa diproses. Program berhenti.")
        input("Tekan Enter untuk keluar...")
        sys.exit()
    else:
        while True:
            clear_screen()
            print("\n--- Menu Pencarian ---")
            print("Pilih kolom dasar untuk pencarian:")
            print(f"1. Judul ({COL_JUDUL})")
            print(f"2. Tahun ({COL_TAHUN})")
            print(f"3. Penulis ({COL_PENULIS})")
            choice_col = input("Masukkan nomor kolom (atau ketik 'q' untuk keluar): ").strip()

            if choice_col.lower() == 'q':
                break

            search_key = ""
            if choice_col == '1': search_key = COL_JUDUL
            elif choice_col == '2': search_key = COL_TAHUN
            elif choice_col == '3': search_key = COL_PENULIS
            else:
                print("Pilihan kolom tidak valid.")
                input("Tekan Enter untuk mencoba lagi...")
                continue

            print(f"\nAnda memilih mencari berdasarkan: {search_key.replace('_',' ').title()}")
            search_value = input(f"Masukkan kata kunci pencarian untuk '{search_key}': ").strip()

            if not search_value:
                 print("Kata kunci tidak boleh kosong.")
                 input("Tekan Enter untuk mencoba lagi...")
                 continue

            print("\nPilih metode pencarian:")
            print("1. Linear Search (Mencari 'mengandung' kata kunci)")
            print("2. Binary Search (Mencari 'sama persis' setelah diurutkan, case-insensitive)")
            choice_method = input("Masukkan pilihan metode (1/2): ").strip()

            results = []
            search_start_time = time.time()

            if choice_method == '1':
                print("\nMelakukan Linear Search...")
                results = linear_search(all_data, search_value, search_key)
            elif choice_method == '2':
                print("\nMelakukan Binary Search...")
                print(f"Mengurutkan data berdasarkan '{search_key}'...")
                start_sort_time = time.time()
                try:
                    sorted_data = sorted(all_data, key=lambda item: sort_key_func(item, search_key))
                    end_sort_time = time.time()
                    print(f"Data diurutkan dalam {end_sort_time - start_sort_time:.4f} detik.")

                    results = binary_search(sorted_data, search_value, search_key)
                except Exception as e:
                      print(f"\nError saat sorting atau persiapan binary search: {e}")
                      print("Traceback:")
                      traceback.print_exc()
                      print("\nBinary search tidak dapat dilanjutkan.")
                      input("Tekan Enter untuk kembali ke menu...")
                      continue
            else:
                print("Pilihan metode tidak valid.")
                input("Tekan Enter untuk mencoba lagi...")
                continue

            search_end_time = time.time()

            clear_screen()
            print(f"\n--- Hasil Pencarian untuk '{search_value}' di kolom '{search_key}' ---")
            print(f"(Metode: {'Linear' if choice_method == '1' else 'Binary'} Search, Waktu: {search_end_time - search_start_time:.4f} detik)")

            if results:
                print(f"Ditemukan {len(results)} hasil:")

                try:
                    results.sort(key=lambda item: item.get('no', 0))
                except Exception as sort_err:
                    print(f"(Peringatan: Gagal mengurutkan hasil akhir - {sort_err})")

                for i, row in enumerate(results):
                    print(f"\n===== Hasil #{i + 1} =====")
                    for col_name in ALL_DATABASE_COLUMNS:
                        value = row.get(col_name, '[Kolom Tidak Ditemukan]')
                        value_display = value if value is not None else 'N/A'

                        label = col_name.replace('_', ' ').title()

                        if col_name in ["abstrak_langusung_copas_dari_paper", "kesimpulan_langusung_copas_dari_paper"]:
                            print(f"\n{label}:")
                            print(f"  {value_display}")
                        else:
                            print(f"{label}: {value_display}")

                    print("=" * 25)
            else:
                print("\nTidak ada hasil yang cocok ditemukan.")

            input("\nTekan Enter untuk melanjutkan ke pencarian berikutnya...")

    print("\nProgram pencarian selesai.")
    input("Tekan Enter untuk keluar...")