"""
TUGAS AKHIR - ALGORITMA PENCARIAN DAN PENGURUTAN DATA
Studi Kasus : Sistem Inventaris Toko Kelontong "Toko Berkah"
Nama        : [Nama Mahasiswa]
NIM         : [NIM Mahasiswa]
Kelas       : [Kelas]

Algoritma Pencarian : Linear Search, Binary Search, Interpolation Search
Algoritma Sorting   : Bubble Sort, Selection Sort, Insertion Sort, Merge Sort
"""

import streamlit as st
import random
import time

# ============================================================
# BAGIAN 1 — GENERATE DATA (1.000 produk toko kelontong)
# ============================================================

def generate_data(jumlah: int = 1000) -> list[dict]:
    """
    Membuat data dummy produk toko kelontong.

    Algoritma:
        data = []
        UNTUK i DARI 1 SAMPAI jumlah:
            pilih kategori dan produk secara acak
            buat record produk
            tambahkan ke data
        RETURN data
    """
    random.seed(99)

    kategori_produk = {
        "Sembako": [
            ("Beras Premium 5kg", "kg"), ("Beras Medium 5kg", "kg"),
            ("Minyak Goreng 1L", "botol"), ("Minyak Goreng 2L", "botol"),
            ("Gula Pasir 1kg", "kg"), ("Tepung Terigu 1kg", "kg"),
            ("Telur Ayam 1kg", "kg"), ("Garam Halus 250g", "bungkus"),
            ("Kecap Manis 135ml", "botol"), ("Saos Sambal 135ml", "botol"),
            ("Kopi Sachet", "sachet"), ("Teh Celup isi 25", "kotak"),
            ("Mie Instan Goreng", "bungkus"), ("Mie Instan Kuah", "bungkus"),
            ("Susu Kental Manis", "kaleng"),
        ],
        "Jajan Ringan": [
            ("Chiki Balls", "bungkus"), ("Qtela Singkong", "bungkus"),
            ("Taro Snack", "bungkus"), ("Richeese Nabati", "bungkus"),
            ("Oreo Original", "bungkus"), ("Roma Kelapa", "bungkus"),
            ("Wafer Tango", "bungkus"), ("Permen Kopiko", "bungkus"),
            ("Coklat Silver Queen", "batang"), ("Beng Beng", "batang"),
            ("Chitato", "bungkus"), ("Cheetos", "bungkus"),
            ("Lays Original", "bungkus"), ("Kacang Garuda", "bungkus"),
            ("Popcorn Caramel", "bungkus"),
        ],
        "Sabun & Mandi": [
            ("Sabun Lifebuoy Batang", "batang"), ("Sabun Dettol Batang", "batang"),
            ("Sabun Giv Batang", "batang"), ("Sabun Lux Batang", "batang"),
            ("Sabun Dove Batang", "batang"), ("Sabun Nuvo Batang", "batang"),
        ],
        "Shampo Sachet": [
            ("Shampo Pantene Sachet", "sachet"), ("Shampo Sunsilk Sachet", "sachet"),
            ("Shampo Clear Sachet", "sachet"), ("Shampo Dove Sachet", "sachet"),
            ("Shampo Head & Shoulders Sachet", "sachet"), ("Shampo Rejoice Sachet", "sachet"),
            ("Shampo Lifebuoy Sachet", "sachet"), ("Shampo Zinc Sachet", "sachet"),
        ],
        "Minuman": [
            ("Aqua 600ml", "botol"), ("Aqua 1500ml", "botol"),
            ("Teh Botol Sosro", "botol"), ("Fanta Merah", "kaleng"),
            ("Sprite", "kaleng"), ("Coca Cola", "kaleng"),
            ("Pocari Sweat", "botol"), ("Mizone", "botol"),
            ("You C 1000", "botol"), ("Indomilk UHT", "kotak"),
        ],
        "Kebutuhan Dapur": [
            ("Royco Ayam Sachet", "sachet"), ("Royco Sapi Sachet", "sachet"),
            ("Masako Sachet", "sachet"), ("Knorr Sachet", "sachet"),
            ("Saori Kecap Asin", "botol"), ("Cuka Makan", "botol"),
            ("Merica Bubuk", "sachet"), ("Ketumbar Bubuk", "sachet"),
        ],
    }

    harga_range = {
        "Sembako"         : (3_000,  85_000),
        "Jajan Ringan"    : (500,    15_000),
        "Sabun & Mandi"   : (2_000,  12_000),
        "Shampo Sachet"   : (500,    3_000),
        "Minuman"         : (1_500,  18_000),
        "Kebutuhan Dapur" : (500,    12_000),
    }

    supplier_list = [
        "UD Makmur", "CV Berkah Jaya", "Toko Grosir Sentosa",
        "PT Sumber Rezeki", "UD Lancar Abadi",
    ]

    data, id_counter = [], 1
    semua = [(kat, nama, sat)
             for kat, prods in kategori_produk.items()
             for nama, sat in prods]

    while len(data) < jumlah:
        for kat, nama, sat in semua:
            if len(data) >= jumlah:
                break
            lo, hi = harga_range[kat]
            harga  = round(random.randint(lo // 500, hi // 500) * 500)
            stok   = random.randint(0, 200)
            data.append({
                "ID"      : id_counter,
                "Nama"    : nama,
                "Kategori": kat,
                "Satuan"  : sat,
                "Harga"   : harga,
                "Stok"    : stok,
                "Supplier": random.choice(supplier_list),
                "Terjual" : random.randint(0, 500),
            })
            id_counter += 1

    return data[:jumlah]


# ============================================================
# BAGIAN 2 — ALGORITMA PENCARIAN
# ============================================================

def linear_search(data: list[dict], keyword: str, kolom: list[str]):
    """
    LINEAR SEARCH (Sequential Search)
    ─────────────────────────────────
    Periksa setiap elemen dari awal hingga akhir.

    Algoritma (Python):
        hasil = []
        UNTUK SETIAP record DALAM data:
            langkah += 1
            UNTUK SETIAP k DALAM kolom:
                JIKA keyword ADA DI str(record[k]):
                    tambah record ke hasil
                    BREAK
        RETURN hasil, langkah

    Kompleksitas Waktu : O(n)
    Kelebihan          : Sederhana, tidak perlu data terurut
    Kekurangan         : Lambat untuk data besar
    """
    kw = keyword.lower().strip()
    if not kw:
        return data, 0

    hasil, langkah = [], 0
    for rec in data:
        langkah += 1
        for k in kolom:
            if kw in str(rec[k]).lower():
                hasil.append(rec)
                break
    return hasil, langkah


def binary_search(data: list[dict], keyword: str, kolom_sort: str = "Nama"):
    """
    BINARY SEARCH
    ─────────────
    Data diurutkan dulu, lalu cari dengan membagi dua rentang pencarian.

    Algoritma (Python):
        arr = sort(data, kolom_sort)
        lo, hi = 0, len(arr)-1
        SELAMA lo <= hi:
            langkah += 1
            mid = (lo + hi) // 2
            val = arr[mid][kolom_sort]
            JIKA val cocok keyword:
                kumpulkan semua yang cocok di sekitar mid
                BREAK
            JIKA val < keyword: lo = mid + 1
            SELAIN ITU       : hi = mid - 1
        RETURN hasil, langkah

    Kompleksitas Waktu : O(log n)
    Kelebihan          : Jauh lebih cepat dari linear untuk data terurut
    Kekurangan         : Data harus diurutkan dulu; hanya cocok pencarian nama/teks awalan
    """
    kw = keyword.lower().strip()
    if not kw:
        return data, 0

    arr = sorted(data, key=lambda r: str(r[kolom_sort]).lower())
    hasil, langkah = [], 0
    lo, hi = 0, len(arr) - 1

    while lo <= hi:
        langkah += 1
        mid = (lo + hi) // 2
        val = str(arr[mid][kolom_sort]).lower()

        if val.startswith(kw):
            hasil.append(arr[mid])
            l = mid - 1
            while l >= 0 and str(arr[l][kolom_sort]).lower().startswith(kw):
                hasil.append(arr[l])
                l -= 1
                langkah += 1
            r = mid + 1
            while r < len(arr) and str(arr[r][kolom_sort]).lower().startswith(kw):
                hasil.append(arr[r])
                r += 1
                langkah += 1
            break
        elif val < kw:
            lo = mid + 1
        else:
            hi = mid - 1

    return hasil, langkah


def interpolation_search(data: list[dict], keyword: str, kolom_sort: str = "Harga"):
    """
    INTERPOLATION SEARCH
    ────────────────────
    Seperti Binary Search, tapi posisi probe dihitung proporsional
    berdasarkan nilai target — cocok untuk data NUMERIK tersebar merata.

    Algoritma (Python):
        arr    = sort(data, kolom_sort)   # harus terurut
        lo, hi = 0, len(arr)-1
        target = int(keyword)

        SELAMA lo <= hi DAN target DALAM rentang [arr[lo], arr[hi]]:
            langkah += 1
            pos = lo + (target - arr[lo]) * (hi - lo) / (arr[hi] - arr[lo])
            JIKA arr[pos] == target: kumpulkan semua yang cocok; BREAK
            JIKA arr[pos] <  target: lo = pos + 1
            SELAIN ITU             : hi = pos - 1
        RETURN hasil, langkah

    Kompleksitas Waktu : O(log log n) rata-rata, O(n) worst-case
    Kelebihan          : Sangat cepat untuk data numerik tersebar merata
    Kekurangan         : Hanya untuk data numerik; perlu data terurut
    """
    kw = keyword.strip()
    if not kw:
        return data, 0
    try:
        target = int(kw)
    except ValueError:
        return [], 0

    arr = sorted(data, key=lambda r: r[kolom_sort])
    hasil, langkah = [], 0
    lo, hi = 0, len(arr) - 1

    while lo <= hi and target >= arr[lo][kolom_sort] and target <= arr[hi][kolom_sort]:
        langkah += 1
        lo_val, hi_val = arr[lo][kolom_sort], arr[hi][kolom_sort]

        if lo_val == hi_val:
            if arr[lo][kolom_sort] == target:
                hasil.append(arr[lo])
            break

        pos = lo + int((target - lo_val) * (hi - lo) / (hi_val - lo_val))
        pos = max(lo, min(pos, hi))
        val = arr[pos][kolom_sort]

        if val == target:
            hasil.append(arr[pos])
            l = pos - 1
            while l >= 0 and arr[l][kolom_sort] == target:
                hasil.append(arr[l])
                l -= 1
                langkah += 1
            r = pos + 1
            while r < len(arr) and arr[r][kolom_sort] == target:
                hasil.append(arr[r])
                r += 1
                langkah += 1
            break
        elif val < target:
            lo = pos + 1
        else:
            hi = pos - 1

    return hasil, langkah


# ============================================================
# BAGIAN 3 — ALGORITMA SORTING
# ============================================================

def _key(rec, kolom):
    v = rec[kolom]
    return v.lower() if isinstance(v, str) else v

def bubble_sort(data: list[dict], kolom: str, asc: bool = True) -> list[dict]:
    """
    BUBBLE SORT — bandingkan elemen berdampingan, tukar jika perlu.
    Kompleksitas: O(n²)
    """
    arr = data[:]
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            cond = _key(arr[j], kolom) > _key(arr[j+1], kolom)
            if cond if asc else not cond:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def selection_sort(data: list[dict], kolom: str, asc: bool = True) -> list[dict]:
    """
    SELECTION SORT — cari min (atau max), taruh di posisi yang benar.
    Kompleksitas: O(n²)
    """
    arr = data[:]
    n = len(arr)
    for i in range(n):
        idx = i
        for j in range(i + 1, n):
            cond = _key(arr[j], kolom) < _key(arr[idx], kolom)
            if cond if asc else not cond:
                idx = j
        arr[i], arr[idx] = arr[idx], arr[i]
    return arr

def insertion_sort(data: list[dict], kolom: str, asc: bool = True) -> list[dict]:
    """
    INSERTION SORT — sisipkan tiap elemen ke posisi yang tepat.
    Kompleksitas: O(n²)
    """
    arr = data[:]
    for i in range(1, len(arr)):
        key_rec = arr[i]
        kv = _key(key_rec, kolom)
        j = i - 1
        while j >= 0 and ((_key(arr[j], kolom) > kv) if asc else (_key(arr[j], kolom) < kv)):
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key_rec
    return arr

def merge_sort(data: list[dict], kolom: str, asc: bool = True) -> list[dict]:
    """
    MERGE SORT — bagi dua, sort masing-masing, lalu gabung.
    Kompleksitas: O(n log n)
    """
    if len(data) <= 1:
        return data
    mid = len(data) // 2
    L = merge_sort(data[:mid], kolom, asc)
    R = merge_sort(data[mid:], kolom, asc)
    result, i, j = [], 0, 0
    while i < len(L) and j < len(R):
        cond = _key(L[i], kolom) <= _key(R[j], kolom)
        if cond if asc else not cond:
            result.append(L[i]); i += 1
        else:
            result.append(R[j]); j += 1
    return result + L[i:] + R[j:]


SORTING_FN = {
    "Bubble Sort"    : bubble_sort,
    "Selection Sort" : selection_sort,
    "Insertion Sort" : insertion_sort,
    "Merge Sort"     : merge_sort,
}

SORT_INFO = {
    "Bubble Sort"    : "O(n²) — bandingkan elemen berdampingan, tukar jika salah urutan.",
    "Selection Sort" : "O(n²) — cari elemen terkecil/terbesar, taruh di posisi yang benar.",
    "Insertion Sort" : "O(n²) — sisipkan tiap elemen ke posisi yang tepat seperti menyusun kartu.",
    "Merge Sort"     : "O(n log n) — bagi dua, sort masing-masing, gabung. Paling efisien.",
}

SEARCH_INFO = {
    "Linear Search"        : ("O(n)", "Cocok untuk semua jenis data. Tidak perlu terurut."),
    "Binary Search"        : ("O(log n)", "Harus terurut. Cari berdasarkan awalan nama produk."),
    "Interpolation Search" : ("O(log log n)", "Untuk data numerik (Harga/Stok). Ketik angka tepat."),
}


# ============================================================
# BAGIAN 4 — ANTARMUKA STREAMLIT
# ============================================================

st.set_page_config(
    page_title="Toko Berkah — Inventaris",
    page_icon="🏪",
    layout="wide",
)

st.title("🏪 Sistem Inventaris Toko Kelontong \"Toko Berkah\"")
st.caption("Studi Kasus Algoritma Pencarian & Pengurutan | 1.000 data produk")

# ── Load data ──────────────────────────────────────────────
@st.cache_data
def load_data():
    return generate_data(1000)

data_asli = load_data()

# ── Sidebar ─────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Pengaturan")

    # ── Filter kategori & supplier ──
    st.subheader("🗂️ Filter Data")
    semua_kat = ["Semua"] + sorted(set(r["Kategori"] for r in data_asli))
    filter_kat = st.selectbox("Kategori", semua_kat)

    semua_sup = ["Semua"] + sorted(set(r["Supplier"] for r in data_asli))
    filter_sup = st.selectbox("Supplier", semua_sup)

    st.divider()

    # ── Pencarian ──
    st.subheader("🔎 Pencarian")
    metode_cari = st.radio(
        "Algoritma pencarian",
        ["Linear Search", "Binary Search", "Interpolation Search"],
    )

    if metode_cari == "Linear Search":
        kolom_cari = st.multiselect(
            "Cari di kolom",
            ["Nama", "Kategori", "Satuan", "Supplier"],
            default=["Nama", "Kategori"],
        )
        keyword = st.text_input("Kata kunci", placeholder="contoh: sabun, mie, aqua...")

    elif metode_cari == "Binary Search":
        kolom_bin = st.selectbox("Kolom (prefix nama)", ["Nama", "Kategori", "Supplier"])
        keyword   = st.text_input("Kata kunci (awalan nama)", placeholder="contoh: sab → Sabun...")
        kolom_cari = [kolom_bin]

    else:  # Interpolation
        kolom_interp = st.selectbox("Kolom numerik", ["Harga", "Stok", "Terjual"])
        keyword = st.text_input(
            f"Cari nilai {kolom_interp} (angka tepat)",
            placeholder=f"contoh: 1500" if kolom_interp == "Harga" else "contoh: 50",
        )
        kolom_cari = [kolom_interp]

    st.divider()

    # ── Sorting ──
    st.subheader("🔃 Pengurutan")
    metode_sort = st.selectbox("Algoritma sorting", list(SORTING_FN.keys()))
    kolom_sort  = st.selectbox(
        "Urutkan berdasarkan",
        ["ID", "Nama", "Kategori", "Harga", "Stok", "Terjual"],
    )
    arah_sort = st.radio("Arah", ["Ascending ↑", "Descending ↓"])
    asc = arah_sort == "Ascending ↑"

    st.divider()
    baris = st.select_slider("Baris per halaman", [10, 20, 50, 100], value=20)

# ── Proses filter kategori & supplier ──────────────────────
data_filtered = data_asli[:]
if filter_kat != "Semua":
    data_filtered = [r for r in data_filtered if r["Kategori"] == filter_kat]
if filter_sup != "Semua":
    data_filtered = [r for r in data_filtered if r["Supplier"] == filter_sup]

# ── Proses pencarian ──────────────────────────────────────
t0 = time.perf_counter()

if metode_cari == "Linear Search":
    hasil_cari, langkah = linear_search(data_filtered, keyword, kolom_cari)
elif metode_cari == "Binary Search":
    hasil_cari, langkah = binary_search(data_filtered, keyword, kolom_cari[0])
else:
    hasil_cari, langkah = interpolation_search(data_filtered, keyword, kolom_cari[0])

waktu_cari = (time.perf_counter() - t0) * 1000  # ms

# ── Proses sorting ────────────────────────────────────────
t1 = time.perf_counter()
sort_fn     = SORTING_FN[metode_sort]
hasil_sort  = sort_fn(hasil_cari, kolom_sort, asc)
waktu_sort  = (time.perf_counter() - t1) * 1000  # ms

# ── Statistik ringkas ─────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Produk",    f"{len(data_asli):,}")
c2.metric("Hasil Filter",    f"{len(hasil_sort):,}")
c3.metric("Langkah Cari",   f"{langkah:,}")
c4.metric("Waktu Cari",     f"{waktu_cari:.2f} ms")
c5.metric("Waktu Sort",     f"{waktu_sort:.2f} ms")

# ── Info algoritma yang dipakai ────────────────────────────
komp, ket = SEARCH_INFO[metode_cari]
st.info(
    f"**{metode_cari}** — Kompleksitas: `{komp}` | {ket}\n\n"
    f"**{metode_sort}** — {SORT_INFO[metode_sort]}"
)

st.divider()

# ── Tabel hasil ───────────────────────────────────────────
total        = len(hasil_sort)
total_hal    = max(1, -(-total // baris))

if total == 0:
    st.warning("⚠️ Data tidak ditemukan. Coba ubah kata kunci atau filter.")
else:
    if total_hal > 1:
        halaman = st.number_input(f"Halaman (1–{total_hal})", 1, total_hal, 1)
    else:
        halaman = 1

    start      = (halaman - 1) * baris
    end        = start + baris
    slice_data = hasil_sort[start:end]

    st.caption(
        f"Menampilkan {start+1}–{min(end, total)} dari **{total:,}** data | "
        f"Diurutkan: **{kolom_sort}** ({arah_sort}) menggunakan **{metode_sort}**"
    )

    tampil = []
    for r in slice_data:
        row          = r.copy()
        row["Harga"] = f"Rp {r['Harga']:,}"
        row["Stok"]  = f"{r['Stok']} {r['Satuan']}"
        tampil.append(row)

    st.dataframe(tampil, width="stretch", hide_index=True)

# ── Penjelasan algoritma ───────────────────────────────────
with st.expander("📖 Penjelasan Lengkap Algoritma"):
    st.markdown("""
## Algoritma Pencarian

### 1. Linear Search
```python
def linear_search(data, keyword, kolom):
    hasil = []
    untuk setiap record dalam data:      # O(n)
        untuk setiap k dalam kolom:
            jika keyword ada di record[k]:
                tambah record ke hasil
                break
    return hasil
```
- Periksa satu per satu dari awal sampai akhir
- **Kompleksitas**: O(n)
- **Cocok untuk**: semua tipe data, tidak perlu diurutkan

---

### 2. Binary Search
```python
def binary_search(data, keyword, kolom):
    arr = sort(data, kolom)              # urutkan dulu
    lo, hi = 0, len(arr)-1
    while lo <= hi:                      # O(log n)
        mid = (lo + hi) // 2
        val = arr[mid][kolom]
        if val cocok keyword:
            kumpulkan semua sekitar mid
            break
        elif val < keyword: lo = mid + 1
        else              : hi = mid - 1
    return hasil
```
- Data diurutkan dulu, lalu pencarian dengan membagi dua rentang
- **Kompleksitas**: O(log n)
- **Cocok untuk**: pencarian teks/nama yang sudah terurut

---

### 3. Interpolation Search
```python
def interpolation_search(data, keyword, kolom):
    arr    = sort(data, kolom)           # urutkan dulu
    lo, hi = 0, len(arr)-1
    target = int(keyword)
    while lo <= hi and target dalam rentang:    # O(log log n)
        # probe dihitung proporsional
        pos = lo + (target - arr[lo]) * (hi - lo) / (arr[hi] - arr[lo])
        if arr[pos] == target: kumpulkan; break
        elif arr[pos] < target: lo = pos + 1
        else                  : hi = pos - 1
    return hasil
```
- Posisi probe dihitung proporsional, tidak selalu di tengah
- **Kompleksitas**: O(log log n) rata-rata
- **Cocok untuk**: data numerik (Harga, Stok) yang tersebar merata

---

## Algoritma Pengurutan

### Bubble Sort — O(n²)
```python
for i in range(n):
    for j in range(n - i - 1):
        if arr[j] > arr[j+1]:
            arr[j], arr[j+1] = arr[j+1], arr[j]
```

### Selection Sort — O(n²)
```python
for i in range(n):
    idx = i
    for j in range(i+1, n):
        if arr[j] < arr[idx]: idx = j
    arr[i], arr[idx] = arr[idx], arr[i]
```

### Insertion Sort — O(n²)
```python
for i in range(1, n):
    key = arr[i]
    j = i - 1
    while j >= 0 and arr[j] > key:
        arr[j+1] = arr[j]; j -= 1
    arr[j+1] = key
```

### Merge Sort — O(n log n)
```python
def merge_sort(arr):
    if len(arr) <= 1: return arr
    mid = len(arr) // 2
    L = merge_sort(arr[:mid])
    R = merge_sort(arr[mid:])
    return merge(L, R)   # gabungkan dua list terurut
```
""")

# ── Visualisasi distribusi harga ───────────────────────────
with st.expander("📊 Visualisasi Distribusi Data"):
    import collections

    st.markdown("#### Jumlah Produk per Kategori")
    kat_count = collections.Counter(r["Kategori"] for r in data_asli)
    st.bar_chart(dict(sorted(kat_count.items())))

    st.markdown("#### Distribusi Rentang Harga")
    rentang = {"< 1.000": 0, "1.000–5.000": 0, "5.001–20.000": 0, "> 20.000": 0}
    for r in data_asli:
        h = r["Harga"]
        if h < 1000:
            rentang["< 1.000"] += 1
        elif h <= 5000:
            rentang["1.000–5.000"] += 1
        elif h <= 20000:
            rentang["5.001–20.000"] += 1
        else:
            rentang["> 20.000"] += 1
    st.bar_chart(rentang)