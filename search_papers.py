import pandas as pd
import os
import sys

SHEET_URL = "https://docs.google.com/spreadsheets/d/17ru4XAU2NloE9Dfxr2PC1BVcsYkLLT5r7nPSsiOFlvQ/export?format=csv&gid=743838712"

COL_NO = "No"
COL_NIM = "NIM"
COL_NAMA_MHS = "Nama Mahasiswa"
COL_SUMBER = "Sumber Database"
COL_FOKUS = "Fokus Kata Kunci (Pilih No.1 atau 2 atau 3) sesuai yg ada di soal"
COL_JUDUL = "Judul Paper"
COL_TAHUN = "Tahun Terbit"
COL_PENULIS = "Nama Penulis"
COL_ABSTRAK = "Abstrak (langusung copas dari paper)"
COL_KESIMPULAN = "Kesimpulan (Langusung copas dari paper)"
COL_LINK = "Link Paper"

ALL_COLS = [
    COL_NO, COL_NIM, COL_NAMA_MHS, COL_SUMBER, COL_FOKUS,
    COL_JUDUL, COL_TAHUN, COL_PENULIS, COL_ABSTRAK, COL_KESIMPULAN, COL_LINK
]

SEARCH_COLS = {'1': COL_JUDUL, '2': COL_TAHUN, '3': COL_PENULIS}
LABELS = {
    COL_NO: "No",
    COL_NIM: "NIM",
    COL_NAMA_MHS: "Nama Mahasiswa",
    COL_SUMBER: "Sumber Database",
    COL_FOKUS: "Fokus Kata Kunci",
    COL_JUDUL: "Judul Paper",
    COL_TAHUN: "Tahun Terbit",
    COL_PENULIS: "Nama Penulis",
    COL_ABSTRAK: "Abstrak",
    COL_KESIMPULAN: "Kesimpulan",
    COL_LINK: "Link Paper",
}

MULTILINE = {COL_ABSTRAK, COL_KESIMPULAN}

def clear():
    os.system('cls')

def load_data(url):
    print("Mengambil data...")
    df = pd.read_csv(url)
    for col in ALL_COLS:
        if col not in df.columns:
            df[col] = None
    df = df[ALL_COLS]
    return df

def linear_search(df, kata, col):
    kata = str(kata).strip().lower()
    if not kata:
        return pd.DataFrame()
    hasil = df[df[col].astype(str).str.contains(kata, case=False, na=False)]
    return hasil.copy()

def binary_search(df_sorted, kata, col):
    n = len(df_sorted)
    low, high, found_idx = 0, n - 1, -1
    is_tahun = (col == COL_TAHUN)
    val = float(kata) if is_tahun else str(kata).strip().lower()
    if is_tahun and pd.isna(val):
        print(f"Input '{kata}' tidak valid untuk kolom {LABELS.get(col, col)}.")
        return pd.DataFrame()
    if not is_tahun and not val:
        return pd.DataFrame()
    while low <= high:
        mid = (low + high) // 2
        mid_v = df_sorted.iloc[mid][col]
        mid_c = float(mid_v) if is_tahun and pd.notna(mid_v) else (
            float('-inf') if is_tahun else (str(mid_v).strip().lower() if pd.notna(mid_v) else "")
        )
        if mid_c == val:
            found_idx = mid
            break
        elif mid_c < val:
            low = mid + 1
        else:
            high = mid - 1
    indices = []
    if found_idx != -1:
        indices.append(found_idx)
        def check_adjacent(idx):
            if not (0 <= idx < n):
                return False
            v = df_sorted.iloc[idx][col]
            if is_tahun:
                cmp_val = float(v) if pd.notna(v) else float('-inf')
            else:
                cmp_val = str(v).strip().lower() if pd.notna(v) else ""
            return cmp_val == val
        i = found_idx - 1
        while check_adjacent(i):
            indices.append(i)
            i -= 1
        i = found_idx + 1
        while check_adjacent(i):
            indices.append(i)
            i += 1
    return df_sorted.iloc[sorted(indices)].copy() if indices else pd.DataFrame()

def display(results, term, key_disp, method):
    clear()
    print(f"Hasil: '{term}' di '{key_disp}' ({method})")
    if results.empty:
        print("\nData tidak ditemukan.")
        return
    print(f"Ditemukan {len(results)} hasil:")
    disp_df = results.sort_values(by=COL_NO) if COL_NO in results.columns else results
    for i, (_, row) in enumerate(disp_df.iterrows()):
        print(f"\n===== #{i + 1} =====")
        for col in ALL_COLS:
            label = LABELS.get(col, col)
            if col in row:
                v = row[col]
                v_disp = 'N/A' if pd.isna(v) else (
                    int(v) if isinstance(v, float) and col == COL_TAHUN and v == int(v)
                    else (round(v, 2) if isinstance(v, float) else str(v).strip())
                )
                if col in MULTILINE:
                    print(f"\n{label}:")
                    lines = str(v_disp).splitlines()
                    print("\n".join([f"  {line.strip()}" for line in lines if line.strip()]) or "  N/A")
                else:
                    print(f"{label}: {v_disp}")
            else:
                print(f"{label}: ---")
        print("=" * 15)

if __name__ == "__main__":
    df = load_data(SHEET_URL)
    while True:
        clear()
        print("Menu")
        print("Cari berdasarkan:")
        for k, c in SEARCH_COLS.items():
            print(f"{k}. {LABELS.get(c, c)}")
        col_choice = input("Masukkan nomor kolom (atau 'q' untuk keluar): ").strip()
        if col_choice.lower() == 'q':
            break
        s_key = SEARCH_COLS.get(col_choice)
        if not s_key or s_key not in df.columns:
            print("Invalid.")
            input()
            continue
        s_key_disp = LABELS.get(s_key, s_key)
        s_val = input(f"Cari '{s_key_disp}': ").strip()
        m_choice = input("\n[1] Linear\n[2] Binary\nPilih Metode: ").strip()
        res, method = pd.DataFrame(), ""
        if m_choice == '1':
            method = "Linear"
            res = linear_search(df, s_val, s_key)
        elif m_choice == '2':
            method = "Binary"
            print(f"Sorting by '{s_key_disp}'...")
            key_func = (lambda c: c.astype(str).str.lower()) if s_key != COL_TAHUN else None
            sorted_df = df.sort_values(by=s_key, na_position='last', key=key_func).reset_index(drop=True)
            res = binary_search(sorted_df, s_val, s_key)
        else:
            input()
            continue
        display(res, s_val, s_key_disp, method)
        input("\nEnter lanjut...")
    print("\nSelesai.")
    input()