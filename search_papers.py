import sqlite3
# import time # Dihapus
import traceback
import os
import sys

# --- Konfigurasi (Sama seperti sebelumnya) ---
SQLITE_DB_PATH = 'papers_database.db'
TABLE_NAME = 'papers'
ALL_DATABASE_COLUMNS = [
    "no", "nim", "nama_mahasiswa", "sumber_database",
    "fokus_kata_kunci_pilih_no1_atau_2_atau_3_sesuai_yg_ada_di_soal",
    "judul_paper", "tahun_terbit", "nama_penulis",
    "abstrak_langusung_copas_dari_paper",
    "kesimpulan_langusung_copas_dari_paper", "link_paper"
]
SEARCHABLE_COLUMNS = {
    '1': 'judul_paper',
    '2': 'tahun_terbit',
    '3': 'nama_penulis'
}
COLUMN_DISPLAY_LABELS = {
    "fokus_kata_kunci_pilih_no1_atau_2_atau_3_sesuai_yg_ada_di_soal": "Fokus Kata Kunci",
    "abstrak_langusung_copas_dari_paper": "Abstrak",
    "kesimpulan_langusung_copas_dari_paper": "Kesimpulan"
}
MULTILINE_COLUMNS = {
    "abstrak_langusung_copas_dari_paper",
    "kesimpulan_langusung_copas_dari_paper"
}
COL_TAHUN = 'tahun_terbit'

def clear_screen():
    os.system('cls')

def connect_db(db_path):
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        print(f"Berhasil terhubung ke db: {db_path}")
        return conn
    except sqlite3.Error as e:
        print(f"\nError koneksi db: {e}\nPastikan file '{db_path}' ada.")
        return None

def fetch_all_data(conn, table, columns_to_fetch):
    if not conn: return []
    cursor = conn.cursor()
    cols_string = ", ".join([f'"{col}"' for col in columns_to_fetch])
    query = f'SELECT {cols_string} FROM "{table}"'
    print(f"Mengambil data dari tabel '{table}'...")
    try:
        cursor.execute(query)
        data = [dict(row) for row in cursor.fetchall()]
        return data
    except sqlite3.Error as e:
        print(f"\nError mengambil data: {e}")
        if "no such column" in str(e).lower(): print("Periksa nama kolom")
        elif "no such table" in str(e).lower(): print(f"Periksa nama tabel '{table}")
        return []

#linear
def linear_search(data_list, search_term, column_key):
    results = []
    search_term_clean = str(search_term).strip().lower()
    if not search_term_clean: return []
    for item in data_list:
        value = item.get(column_key)
        if value is not None and search_term_clean in str(value).strip().lower():
            results.append(item)
    print(f"Linear Search done.")
    return results

def binary_search(sorted_data_list, search_term, column_key):
    results = []
    if not sorted_data_list: return []
    low, high = 0, len(sorted_data_list) - 1
    found_index = -1

    try:
        search_term_val = float(search_term) if column_key == COL_TAHUN else str(search_term).strip().lower()
    except ValueError:
        print(f"\nError: Input '{search_term}' tidak valid untuk kolom '{column_key}'.")
        if column_key == COL_TAHUN: print("Kolom tahun memerlukan angka.")
        return []

    while low <= high:
        mid = (low + high) // 2
        item = sorted_data_list[mid]
        try:
            mid_value = item.get(column_key)
            if mid_value is None:
                 if mid > low: high = mid - 1
                 elif mid < high: low = mid + 1
                 else: break
                 continue
            mid_val_cmp = float(mid_value) if column_key == COL_TAHUN else str(mid_value).strip().lower()
        except (ValueError, TypeError):
             if mid > low: high = mid - 1
             elif mid < high: low = mid + 1
             else: break
             continue

        if mid_val_cmp == search_term_val:
            found_index = mid
            break
        elif mid_val_cmp < search_term_val:
            low = mid + 1
        else:
            high = mid - 1

    if found_index != -1:
        def check_match(index):
            if 0 <= index < len(sorted_data_list):
                item = sorted_data_list[index]
                try:
                    val = item.get(column_key)
                    if val is None: return False
                    item_val_cmp = float(val) if column_key == COL_TAHUN else str(val).strip().lower()
                    return item_val_cmp == search_term_val
                except (ValueError, TypeError):
                    return False
            return False

        results.append(sorted_data_list[found_index])
        i = found_index - 1
        while check_match(i):
            results.append(sorted_data_list[i])
            i -= 1
        i = found_index + 1
        while check_match(i):
            results.append(sorted_data_list[i])
            i += 1

    print(f"Binary Search done.")
    return results

def sort_key_func(item, sort_column_key):
    value = item.get(sort_column_key)
    if value is None:
        return float('inf') if sort_column_key == COL_TAHUN else ""
    try:
        if sort_column_key == COL_TAHUN:
            return float(value)
        elif isinstance(value, str):
            return value.strip().lower()
        return value
    except (ValueError, TypeError):
        return float('inf') if sort_column_key == COL_TAHUN else ""

def main():
    clear_screen()
    print("--- Program Pencarian Data Paper ---")

    conn = connect_db(SQLITE_DB_PATH)
    if not conn:
        input("Tekan Enter untuk keluar...")
        sys.exit()

    all_data = fetch_all_data(conn, TABLE_NAME, ALL_DATABASE_COLUMNS)
    conn.close()
    print("Koneksi database ditutup.")

    if not all_data:
        print("\nTidak ada data. Program berhenti.")
        input("Tekan Enter untuk keluar...")
        sys.exit()

    sorted_data_cache = {}

    while True:
        clear_screen()
        print("Menu")
        print("Pilih kolom dasar untuk pencarian:")
        for key, col_name in SEARCHABLE_COLUMNS.items():
            print(f"{key}. {col_name.replace('_',' ').title()}")
        choice_col = input("Masukkan nomor kolom (atau 'q' untuk keluar): ").strip()

        if choice_col.lower() == 'q':
            break

        search_key = SEARCHABLE_COLUMNS.get(choice_col)
        if not search_key:
            print("Pilihan kolom tidak valid.")
            input("Tekan Enter...")
            continue

        print(f"\nMencari berdasaran: {search_key.replace('_',' ').title()}")
        search_value = input(f"Masukkan kata kunci pencarian: ").strip()
        if not search_value:
            print("Kata kunci tidak boleh kosong.")
            input("Tekan Enter...")
            continue

        print("\nPilih metode pencarian:")
        print("1. Linear Search")
        print("2. Binary Search")
        choice_method = input("Masukkan pilihan metode (1/2): ").strip()

        results = []

        if choice_method == '1':
            print("\nMelakukan Linear Search...")
            results = linear_search(all_data, search_value, search_key)
        elif choice_method == '2':
            print("\nMelakukan Binary Search...")
            if search_key not in sorted_data_cache:
                print(f"Mengurutkan data berdasarkan '{search_key}'...")
                try:
                    def sort_func(item):
                        return sort_key_func(item, search_key)
                    sorted_data_cache[search_key] = sorted(all_data, key=sort_func)
                    print(f"Data diurutkan.")
                except Exception as e:
                    print(f"\nError saat sorting: {e}")
                    traceback.print_exc()
                    input("Tekan Enter...")
                    continue
            else:
                print(f"Menggunakan data terurut dari cache untuk '{search_key}'.")

            results = binary_search(sorted_data_cache[search_key], search_value, search_key)
        else:
            print("Pilihan metode tidak valid.")
            input("Tekan Enter...")
            continue

        clear_screen()
        print(f"Hasil Pencarian ('{search_value}' di '{search_key}')")
        if choice_method == '1':
            print("(Metode: Linear Search)")
        else:
            print("(Metode: Binary Search)")

        if results:
            print(f"Ditemukan {len(results)} hasil:")
            try:
                def sort_by_no(item):
                    return item.get('no', 0)
                results.sort(key=sort_by_no)
            except Exception:
                pass

            for i, row in enumerate(results):
                print(f"\n===== #{i + 1} =====")
                for col_name in ALL_DATABASE_COLUMNS:
                    value = row.get(col_name)
                    value_display = 'N/A'

                    if value is not None:
                        if col_name == 'tahun_terbit':
                            try:
                                value_display = int(float(value))
                            except (ValueError, TypeError):
                                value_display = value
                        else:
                            value_display = value

                    default_label = col_name.replace('_', ' ').title()
                    label = COLUMN_DISPLAY_LABELS.get(col_name, default_label)

                    if col_name in MULTILINE_COLUMNS:
                        print(f"\n{label}:")
                        indented_value = "\n".join(["  " + line.strip() for line in str(value_display).splitlines()])
                        print(indented_value if indented_value.strip() else "  N/A")
                    else:
                        print(f"{label}: {value_display}")
                print("=" * 25)
        else:
            print("\nTidak ada hasil yang cocok ditemukan.")

        input("\nTekan Enter untuk pencarian berikutnya...")

    print("\nProgram pencarian selesai.")
    input("Tekan Enter untuk keluar...")

if __name__ == "__main__":
    main()