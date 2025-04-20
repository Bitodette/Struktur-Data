import csv
import os
import urllib.request

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
    os.system('cls' if os.name == 'nt' else 'clear')

def load_data(url):
    print("Mengambil data dari URL...")
    response = urllib.request.urlopen(url)
    lines = (l.decode('utf-8-sig') for l in response)
    reader = csv.DictReader(lines)
    data = []
    for row in reader:
        paper = {}
        for col in ALL_COLS:
            if row.get(col):
                paper[col] = row.get(col, "").strip()
            else:
                paper[col] = ""
        data.append(paper)
    return data

def linear_search(data, KataKunci, mode):
    KataKunci = KataKunci.strip().lower()
    results = []
    if mode == COL_TAHUN:
        for row in data:
            if row[mode].strip() == KataKunci:
                results.append(row)
    else:
        for row in data:
            if KataKunci in row[mode].lower():
                results.append(row)
    return results

def binary_search(data, KataKunci, mode):
    results = []
    KataKunci_clean = KataKunci.strip()
    if mode == COL_TAHUN:
        filtered_data = []
        for row in data:
            tahun = row[mode].strip()
            if tahun.isdigit():
                filtered_data.append(row)
        sorted_data = sorted(filtered_data, key=lambda x: int(x[mode].strip()))
        left, right = 0, len(sorted_data) - 1
        try:
            KataKunci_num = int(KataKunci_clean)
        except:
            print("Tahun harus berupa angka.")
            return []
        while left <= right:
            mid = (left + right) // 2
            mid_val = int(sorted_data[mid][mode].strip())
            if mid_val == KataKunci_num:
                l, r = mid, mid
                while l >= 0 and int(sorted_data[l][mode].strip()) == KataKunci_num:
                    results.append(sorted_data[l])
                    l -= 1
                while r+1 < len(sorted_data) and int(sorted_data[r+1][mode].strip()) == KataKunci_num:
                    r += 1
                    results.append(sorted_data[r])
                break
            elif mid_val < KataKunci_num:
                left = mid + 1
            else:
                right = mid - 1
    else:
        sorted_data = sorted(data, key=lambda x: x[mode].strip().lower())
        KataKunci_clean_lower = KataKunci_clean.lower()
        left, right = 0, len(sorted_data) - 1
        while left <= right:
            mid = (left + right) // 2
            mid_val = sorted_data[mid][mode].strip().lower()
            if mid_val == KataKunci_clean_lower:
                l, r = mid, mid
                while l >= 0 and sorted_data[l][mode].strip().lower() == KataKunci_clean_lower:
                    results.append(sorted_data[l])
                    l -= 1
                while r+1 < len(sorted_data) and sorted_data[r+1][mode].strip().lower() == KataKunci_clean_lower:
                    r += 1
                    results.append(sorted_data[r])
                break
            elif mid_val < KataKunci_clean_lower:
                left = mid + 1
            else:
                right = mid - 1
    return results

def display_results(hasil, KataKunci, keyDis, method):
    clear()
    print(f"Hasil: '{KataKunci}' di '{keyDis}' ({method})")
    if not hasil:
        print("\nData tidak ditemukan.")
        return
    print(f"Ditemukan {len(hasil)} hasil:")
    for i, row in enumerate(hasil):
        print(f"\n===== #{i + 1} =====")
        for col in ALL_COLS:
            label = LABELS[col]
            val = row[col] if row[col] else '---'
            if col in MULTILINE:
                print(f"\n{label}:")
                lines = val.splitlines()
                ada = False
                for line in lines:
                    if line.strip():
                        print(line.strip())
                        ada = True
                if not ada:
                    print("  N/A")
            else:
                print(f"{label}: {val}")
        print("=" * 15)

def main():
    data = load_data(SHEET_URL)
    while True:
        clear()
        print("Menu")
        print("Cari berdasarkan:")
        for nomor, kolom in SEARCH_COLS.items():
            print(f"{nomor}. {LABELS.get(kolom, kolom)}")
        col_choice = input("Masukkan nomor kolom (atau 'q' untuk keluar): ").strip()
        if col_choice.lower() == 'q':
            break
        col = SEARCH_COLS.get(col_choice)
        if not col:
            print("Pilihan kolom tidak valid.")
            input("Enter untuk lanjut...")
            continue
        key_disp = LABELS.get(col, col)
        KataKunci = input(f"Cari '{key_disp}': ").strip()
        m_choice = input("\n[1] Linear\n[2] Binary\nPilih Metode: ").strip()
        if m_choice == '2':
            method = "Binary"
            results = binary_search(data, KataKunci, col)
        else:
            method = "Linear"
            results = linear_search(data, KataKunci, col)
        display_results(results, KataKunci, key_disp, method)
        input("\nEnter lanjut...")
    print("\nSelesai.")
    input()

if __name__ == "__main__":
    main()