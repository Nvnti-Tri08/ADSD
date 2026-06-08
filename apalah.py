import streamlit as st
import pandas as pd
import random
import time

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Gudang Kosmetik Finder", layout="wide")

st.title("🧴 Sistem Pencarian Gudang Kosmetik")
st.caption("Aplikasi sederhana untuk mencari lokasi barang di gudang pabrik kosmetik")

st.markdown("---")
with st.container():
    search_col, info_col = st.columns([3, 1])
    with search_col:
        st.subheader("🔎 Pencarian Cepat")
        st.info("Masukkan kata kunci di bawah untuk mencari nama barang atau lokasi gudang.")
        search = st.text_input(
            "🔍 Kata kunci pencarian",
            placeholder="Contoh: Serum, A, rak 2, C1"
        )
    with info_col:
        st.subheader("📌 Petunjuk")
        st.markdown(
            "- Ketik kata kunci untuk mencari nama barang atau lokasi gudang.\n"
            "- Hasil akan dicari secara otomatis di semua kolom utama.\n"
            "- Klik pilihan item untuk melihat detail lokasi."
        )

# =========================
# DATA GENERATOR
# =========================
def generate_data(n=200):
    nama_barang = [  
        "Fragrance Rose 10ml", "Fragrance Vanilla 10ml", "Bottle 50ml",
        "Bottle 100ml", "Label Premium", "Box Packaging", "Serum A",
        "Serum B", "Face Wash", "Toner", "Moisturizer"
    ]
    gudang = ["A", "B", "C"]
    rak = ["1", "2", "3", "4", "5"]
    shelf = ["A1", "A2", "B1", "B2", "C1"]

    data = []
    for i in range(n):
        item = {
            "id": i + 1,
            "nama": random.choice(nama_barang),
            "kategori": random.choice(["Bahan Baku", "Packaging", "Produk Jadi"]),
            "gudang": random.choice(gudang),
            "rak": random.choice(rak),
            "shelf": random.choice(shelf),
            "stok": random.randint(1, 500)
        }
        data.append(item)

    return pd.DataFrame(data)


def search_dataframe(df, query, columns):
    """Cari query di beberapa kolom. Algoritma sederhana: linear scan / filter DataFrame."""
    if not query:
        return df

    query = str(query).strip()
    mask = pd.Series(False, index=df.index)

    for col in columns:
        if col in df.columns:
            mask = mask | df[col].astype(str).str.contains(query, case=False, na=False)

    return df[mask]


# =========================
# LOAD DATA
# =========================
st.sidebar.header("⚙️ Pengaturan Data")
mode = st.sidebar.radio("Pilih sumber data:", ["Data Dummy", "Upload CSV"])

# FIX: Gunakan session_state agar data tidak di-generate ulang setiap interaksi
if "df" not in st.session_state:
    st.session_state.df = None
if "last_mode" not in st.session_state:
    st.session_state.last_mode = None
if "last_n" not in st.session_state:
    st.session_state.last_n = 200

df = None

if mode == "Data Dummy":
    jumlah = st.sidebar.slider("Jumlah data", 50, 1000, 200)

    # Hanya generate ulang jika jumlah berubah atau mode baru dipilih
    if (st.session_state.last_mode != "Data Dummy" or
            st.session_state.last_n != jumlah or
            st.session_state.df is None):
        st.session_state.df = generate_data(jumlah)
        st.session_state.last_mode = "Data Dummy"
        st.session_state.last_n = jumlah
       

    df = st.session_state.df

elif mode == "Upload CSV":
    file = st.sidebar.file_uploader("Upload file CSV", type=["csv"])
    if file:
        # FIX: Baca ulang hanya jika file baru di-upload
        if st.session_state.last_mode != file.name:
            st.session_state.df = pd.read_csv(file)
            st.session_state.last_mode = file.name
        df = st.session_state.df
    else:
        st.session_state.df = None
        st.warning("Silakan upload file CSV terlebih dahulu")

# =========================
# VALIDASI KOLOM CSV
# =========================
REQUIRED_COLUMNS = {"nama", "kategori", "gudang", "rak", "shelf", "stok"}

if df is not None:
    missing_cols = REQUIRED_COLUMNS - set(df.columns)
    if missing_cols:
        st.error(f"❌ CSV tidak memiliki kolom yang dibutuhkan: {', '.join(missing_cols)}")
        st.info("Kolom yang diperlukan: id, nama, kategori, gudang, rak, shelf, stok")
        st.stop()

    # Tambah kolom id jika tidak ada (untuk CSV custom)
    if "id" not in df.columns:
        df.insert(0, "id", range(1, len(df) + 1))

    # =========================
    # DATA MENTAH
    # =========================
    with st.expander("📊 Lihat Semua Data Mentah", expanded=False):
        st.dataframe(df, width="stretch")

    filtered = df.copy()

    if search:
        start_time = time.perf_counter()
        search_columns = ["nama", "kategori", "gudang", "rak", "shelf"]
        filtered = search_dataframe(filtered, search, search_columns)
        end_time = time.perf_counter()
        search_time = (end_time - start_time) * 1000
    else:
        search_time = None

    # =========================
    # STATISTIK
    # =========================
    st.subheader("📈 Statistik Gudang")
    stat_text = "Algoritma pencarian: filter / linear scan pada data. Cocok untuk inventori kecil sampai menengah."
    if search:
        stat_text += f" | ⏱️ Waktu pencarian: **{search_time:.4f} ms**"
    st.info(stat_text)
    
    if search:
        st.write(
            f"📊 Linear Search memeriksa **{len(df)}** data dan menemukan **{len(filtered)}** hasil."
        )
    else:
        st.write(
            f"📊 Total data tersedia untuk pencarian: **{len(df)}** item"
        )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Item (Filter)", len(filtered))
    col2.metric("Total Stok (Filter)", int(filtered["stok"].sum()) if not filtered.empty else 0)
    col3.metric("Rata-rata Stok", round(filtered["stok"].mean(), 2) if not filtered.empty else 0)
    col4.metric("Total Item (Keseluruhan)", len(df))

    # =========================
    # HASIL PENCARIAN / DAFTAR
    # =========================
    if search:
        st.subheader("📦 Hasil Pencarian")
        st.info(f"Menampilkan hasil pencarian untuk: **'{search}'** — ditemukan **{len(filtered)}** item")

        if not filtered.empty:
            st.dataframe(filtered, width="stretch")
        else:
            st.error("❌ Tidak ada barang yang cocok dengan pencarian.")
            st.info("💡 Coba ubah kata kunci pencarian atau gunakan istilah lain.")
    else:
        st.info(
            "🔍 **Masukkan kata kunci pencarian** di atas untuk menemukan barang berdasarkan nama, kategori, gudang, rak, atau shelf."
        )

else:
    st.info("ℹ️ Data belum tersedia. Pilih 'Data Dummy' atau upload CSV di sidebar.")