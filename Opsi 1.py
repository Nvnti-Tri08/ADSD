"""
TUGAS KULIAH - ALGORITMA PENCARIAN DAN PENGURUTAN DATA
Nama  : [Nama Mahasiswa]
NIM   : [NIM Mahasiswa]
Kelas : [Kelas]

DESKRIPSI ALGORITMA:
1. Pencarian  : Sequential Search (Linear Search)
2. Pengurutan : Bubble Sort
"""

import streamlit as st
import random

# ============================================================
# BAGIAN 1: GENERATE DATA (1000 data karyawan)
# ============================================================

def generate_data(jumlah: int) -> list[dict]:
    """
    Fungsi untuk membuat data dummy karyawan sebanyak `jumlah` record.

    Algoritma (Python):
        data = []
        untuk i dari 1 sampai jumlah:
            buat dict karyawan dengan field acak
            tambahkan ke data
        kembalikan data
    """
    random.seed(42)  # seed agar data konsisten setiap run

    nama_depan = [
        "Andi", "Budi", "Citra", "Dewi", "Eka", "Fajar", "Gita", "Hadi",
        "Indah", "Joko", "Kartika", "Lestari", "Maulana", "Nisa", "Oki",
        "Putri", "Reza", "Sari", "Tono", "Umar", "Vera", "Wati", "Yoga",
        "Zahra", "Ahmad", "Bambang", "Cahya", "Dika", "Erni", "Fauzi",
        "Galih", "Hendra", "Irma", "Jaya", "Krisna", "Laila", "Mirna",
        "Nurul", "Oscar", "Pandu", "Rahma", "Sigit", "Tari", "Wahyu",
    ]
    nama_belakang = [
        "Santoso", "Wijaya", "Kurniawan", "Pratama", "Hidayat", "Setiawan",
        "Nugroho", "Susanto", "Rahayu", "Hartono", "Purnomo", "Utama",
        "Saputra", "Wahyudi", "Laksono", "Kusuma", "Surya", "Budiman",
        "Firmansyah", "Gunawan", "Handoko", "Irawan", "Jatmiko",
    ]
    divisi_list   = ["Teknologi", "HR", "Keuangan", "Operasional", "Marketing"]
    jabatan_map   = {
        "Teknologi"  : ["Software Engineer", "Backend Developer", "DevOps", "Data Analyst", "QA Engineer"],
        "HR"         : ["Rekruter", "HR Manager", "Payroll Staff", "Training Officer", "People Ops"],
        "Keuangan"   : ["Akuntan", "Financial Analyst", "Auditor", "Tax Specialist", "CFO Staff"],
        "Operasional": ["Supervisor", "Koordinator", "Logistik", "Admin", "Project Manager"],
        "Marketing"  : ["Content Creator", "Digital Marketer", "Brand Manager", "SEO Specialist", "Copywriter"],
    }
    kota_list   = ["Jakarta", "Surabaya", "Bandung", "Medan", "Semarang",
                   "Makassar", "Yogyakarta", "Palembang", "Depok", "Tangerang"]
    status_list = ["Aktif", "Aktif", "Aktif", "Aktif", "Tidak Aktif", "Pending"]

    data = []
    for i in range(1, jumlah + 1):
        divisi  = random.choice(divisi_list)
        jabatan = random.choice(jabatan_map[divisi])
        record  = {
            "ID"     : i,
            "Nama"   : random.choice(nama_depan) + " " + random.choice(nama_belakang),
            "Divisi" : divisi,
            "Jabatan": jabatan,
            "Kota"   : random.choice(kota_list),
            "Gaji"   : random.randint(4, 35) * 1_000_000,
            "Status" : random.choice(status_list),
            "Tahun"  : random.randint(2015, 2024),
        }
        data.append(record)
    return data


# ============================================================
# BAGIAN 2: ALGORITMA PENCARIAN — Sequential Search
# ============================================================

def sequential_search(data: list[dict], keyword: str, kolom: list[str]) -> list[dict]:
    """
    Algoritma Sequential Search (Linear Search):

        FUNCTION sequential_search(data, keyword, kolom):
            hasil = []
            keyword = ubah_ke_huruf_kecil(keyword)

            UNTUK SETIAP record DALAM data:
                UNTUK SETIAP k DALAM kolom:
                    nilai = ubah_ke_huruf_kecil(str(record[k]))
                    JIKA keyword ADA DI nilai:
                        tambahkan record ke hasil
                        BREAK  # hindari duplikat
            RETURN hasil

    Kompleksitas Waktu : O(n * m) — n=jumlah data, m=jumlah kolom
    Kompleksitas Ruang : O(k) — k=jumlah hasil yang cocok
    """
    hasil   = []
    keyword = keyword.lower().strip()

    if keyword == "":
        return data  # jika kosong, kembalikan semua data

    for record in data:
        ditemukan = False
        for k in kolom:
            nilai = str(record[k]).lower()
            if keyword in nilai:
                ditemukan = True
                break
        if ditemukan:
            hasil.append(record)

    return hasil


# ============================================================
# BAGIAN 3: ALGORITMA PENGURUTAN — Bubble Sort
# ============================================================

def bubble_sort(data: list[dict], kolom: str, ascending: bool = True) -> list[dict]:
    """
    Algoritma Bubble Sort:

        FUNCTION bubble_sort(data, kolom, ascending):
            n    = panjang(data)
            arr  = salin(data)

            UNTUK i DARI 0 SAMPAI n-1:
                UNTUK j DARI 0 SAMPAI n-i-2:
                    a = arr[j][kolom]
                    b = arr[j+1][kolom]

                    JIKA ascending:
                        kondisi = a > b
                    SELAIN ITU:
                        kondisi = a < b

                    JIKA kondisi BENAR:
                        tukar(arr[j], arr[j+1])

            RETURN arr

    Kompleksitas Waktu  : O(n²) worst-case
    Kompleksitas Ruang  : O(1) — in-place (tidak butuh memori tambahan)
    """
    arr = data[:]      # salin agar data asli tidak berubah
    n   = len(arr)

    for i in range(n):
        for j in range(0, n - i - 1):
            a = arr[j][kolom]
            b = arr[j + 1][kolom]

            # bandingkan: string pakai lower() agar case-insensitive
            if isinstance(a, str):
                a = a.lower()
                b = b.lower()

            if ascending:
                perlu_tukar = a > b
            else:
                perlu_tukar = a < b

            if perlu_tukar:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

    return arr


# ============================================================
# BAGIAN 4: ANTARMUKA STREAMLIT
# ============================================================

# --- Konfigurasi halaman ---
st.set_page_config(
    page_title="Pencarian & Pengurutan Data",
    page_icon="🔍",
    layout="wide",
)

st.title("🔍 Aplikasi Pencarian & Pengurutan Data Karyawan")
st.caption("Algoritma: Sequential Search + Bubble Sort | Data: 1.000 record")

# --- Generate data (cache agar tidak digenerate ulang) ---
@st.cache_data
def load_data():
    return generate_data(1000)

data_asli = load_data()

# --- Sidebar: kontrol pencarian & sorting ---
with st.sidebar:
    st.header("⚙️ Pengaturan")

    st.subheader("🔎 Pencarian")
    keyword = st.text_input("Kata kunci", placeholder="Cari nama, kota, divisi...")
    kolom_cari = st.multiselect(
        "Cari di kolom",
        options=["Nama", "Divisi", "Jabatan", "Kota", "Status"],
        default=["Nama", "Divisi", "Kota"],
    )

    st.divider()

    st.subheader("🔃 Pengurutan (Bubble Sort)")
    kolom_sort = st.selectbox(
        "Urutkan berdasarkan",
        options=["ID", "Nama", "Divisi", "Jabatan", "Kota", "Gaji", "Status", "Tahun"],
    )
    arah_sort = st.radio("Arah urutan", ["Ascending ↑", "Descending ↓"])
    ascending  = arah_sort == "Ascending ↑"

    st.divider()

    st.subheader("🏢 Filter Divisi")
    semua_divisi = ["Semua"] + sorted(set(r["Divisi"] for r in data_asli))
    filter_divisi = st.selectbox("Pilih divisi", semua_divisi)

    st.subheader("📋 Filter Status")
    semua_status = ["Semua"] + sorted(set(r["Status"] for r in data_asli))
    filter_status = st.selectbox("Pilih status", semua_status)

    st.divider()
    baris_per_halaman = st.select_slider(
        "Baris per halaman", options=[10, 20, 50, 100], value=20
    )

# --- Proses: filter divisi & status dulu ---
data_filtered = data_asli[:]
if filter_divisi != "Semua":
    data_filtered = [r for r in data_filtered if r["Divisi"] == filter_divisi]
if filter_status != "Semua":
    data_filtered = [r for r in data_filtered if r["Status"] == filter_status]

# --- Proses: Sequential Search ---
if kolom_cari:
    hasil_cari = sequential_search(data_filtered, keyword, kolom_cari)
else:
    hasil_cari = data_filtered

# --- Proses: Bubble Sort ---
# Catatan: bubble sort O(n²) lambat untuk 1000 data di Python murni,
# sehingga kita batasi ke hasil pencarian saja agar tetap responsif.
with st.spinner("Menjalankan Bubble Sort..."):
    hasil_sort = bubble_sort(hasil_cari, kolom_sort, ascending)

# --- Statistik ringkas ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Data Asli",   f"{len(data_asli):,}")
col2.metric("Hasil Pencarian",   f"{len(hasil_sort):,}")
col3.metric("Karyawan Aktif",    f"{sum(1 for r in data_asli if r['Status'] == 'Aktif'):,}")
avg_gaji = sum(r['Gaji'] for r in data_asli) // len(data_asli)
col4.metric("Rata-rata Gaji",    f"Rp {avg_gaji:,}")

st.divider()

# --- Tampilkan tabel dengan paginasi ---
total_hasil  = len(hasil_sort)
total_halaman = max(1, -(-total_hasil // baris_per_halaman))  # ceiling division

if total_hasil == 0:
    st.warning("⚠️ Tidak ada data yang ditemukan. Coba ubah kata kunci atau filter.")
else:
    # Paginasi
    if total_halaman > 1:
        halaman = st.number_input(
            f"Halaman (1 – {total_halaman})",
            min_value=1, max_value=total_halaman, value=1, step=1
        )
    else:
        halaman = 1

    start = (halaman - 1) * baris_per_halaman
    end   = start + baris_per_halaman
    slice_data = hasil_sort[start:end]

    st.caption(
        f"Menampilkan {start + 1}–{min(end, total_hasil)} dari {total_hasil:,} data "
        f"| Diurutkan: **{kolom_sort}** ({arah_sort})"
    )

    # Format gaji sebelum tampil
    tampil = []
    for r in slice_data:
        row = r.copy()
        row["Gaji"] = f"Rp {r['Gaji']:,}"
        tampil.append(row)

    st.dataframe(tampil, width="stretch", hide_index=True)

# --- Penjelasan algoritma (ekspander) ---
with st.expander("📖 Penjelasan Algoritma"):
    st.markdown("""
### Sequential Search (Pencarian Berurutan)

```python
def sequential_search(data, keyword, kolom):
    hasil = []
    keyword = keyword.lower()

    for record in data:
        for k in kolom:
            nilai = str(record[k]).lower()
            if keyword in nilai:
                hasil.append(record)
                break   # hindari duplikat

    return hasil
```
- **Cara kerja**: Periksa setiap elemen satu per satu dari awal hingga akhir.
- **Kompleksitas waktu**: O(n) — berbanding lurus dengan jumlah data.
- **Kelebihan**: Sederhana, tidak butuh data terurut.

---

### Bubble Sort (Pengurutan Gelembung)

```python
def bubble_sort(data, kolom, ascending=True):
    arr = data[:]
    n   = len(arr)

    for i in range(n):
        for j in range(0, n - i - 1):
            a = arr[j][kolom]
            b = arr[j + 1][kolom]
            if ascending:
                perlu_tukar = a > b
            else:
                perlu_tukar = a < b
            if perlu_tukar:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

    return arr
```
- **Cara kerja**: Bandingkan dua elemen berdampingan, tukar jika salah urutan. Ulangi hingga semua terurut.
- **Kompleksitas waktu**: O(n²) — kuadratik terhadap jumlah data.
- **Kelebihan**: Mudah dipahami dan diimplementasikan.
""")