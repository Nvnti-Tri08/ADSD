"""SIGUDANG — Sistem Informasi Gudang Skincare berbasis Streamlit."""

import time
import random

import pandas as pd
import streamlit as st

# ── Konfigurasi ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="SIGUDANG - Sistem Informasi Gudang",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Konstanta ─────────────────────────────────────────────────────────────────

DAFTAR_BARANG = [
    "Fragrance Rose 10ml", "Fragrance Vanilla 10ml", "Fragrance Jasmine 5ml",
    "Fragrance Lavender 10ml", "Fragrance Citrus 15ml", "Fragrance Oud 5ml",
    "Bottle 30ml Clear", "Bottle 50ml Clear", "Bottle 100ml Clear",
    "Bottle 50ml Frosted", "Bottle 200ml Pump", "Bottle 500ml HDPE",
    "Tube 50ml", "Tube 100ml", "Tube 200ml Flip Cap",
    "Label Premium Glossy", "Label Matte A4", "Label Waterproof",
    "Box Packaging Small", "Box Packaging Medium", "Box Premium Gift",
    "Serum Vitamin C", "Serum Retinol", "Serum Hyaluronic Acid",
    "Serum Brightening", "Serum Anti-Aging", "Serum Niacinamide",
    "Face Wash Foam", "Face Wash Gel", "Face Wash Cream",
    "Toner Hydrating", "Toner Exfoliating", "Toner Rose Water",
    "Moisturizer Day Cream", "Moisturizer Night Cream", "Moisturizer SPF 30",
    "Sunscreen SPF 50", "BB Cream", "CC Cream",
    "Eye Cream 15ml", "Lip Balm SPF", "Hand Cream 75ml",
    "Body Lotion 250ml", "Body Scrub 200ml", "Bath Salt 300g",
    "Shampoo 250ml", "Conditioner 250ml", "Hair Mask 200ml",
    "Nail Polish Remover", "Micellar Water 200ml", "Cleansing Oil 150ml",
]

FILTER_KOLOM = {
    "🔎 Semua Kolom": None,
    "📦 Nama Barang": ["Nama Barang"],
    "🏷️ Kategori":   ["Kategori"],
    "🏭 Gudang":      ["Gudang"],
    "📚 Rak":         ["Rak"],
    "📌 Shelf":       ["Shelf"],
}

KOLOM_CONFIG = {
    "ID"         : st.column_config.TextColumn("ID", width=80),
    "Nama Barang": st.column_config.TextColumn("Nama Barang", width=250),
    "Kategori"   : st.column_config.TextColumn("Kategori", width=150),
    "Gudang"     : st.column_config.TextColumn("Gudang", width=100),
    "Rak"        : st.column_config.TextColumn("Rak", width=90),
    "Shelf"      : st.column_config.TextColumn("Shelf", width=110),
    "Stok"       : st.column_config.NumberColumn("Stok", width=120, format="%d pcs"),
}

NAV_MENU = [
    ("📦", "Data Barang"),
    ("🛠️", "Kelola Data"),
    ("⚙️", "Pengaturan"),
    ("ℹ️", "Tentang Sistem"),
]

# ── CSS ───────────────────────────────────────────────────────────────────────

def apply_styles():
    st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background-color: #4b1f15;
            color: #f5e8df;
        }
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] p { color: #fde8dd !important; }
        [data-testid="stSidebar"] button {
            background-color: rgba(123,63,30,0.18);
            color: #f3e4dc;
            border: 1px solid rgba(255,255,255,0.14);
            border-radius: 8px;
            padding: 10px 14px;
        }
        [data-testid="stSidebar"] button:hover { background-color: #fff; color: #000; }
        .page-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: linear-gradient(135deg, #4a1f18, #7a3728);
            padding: 20px;
            border-radius: 12px;
            border-left: 6px solid #8b4513;
            margin-bottom: 25px;
        }
        .page-header h1 { margin: 0; color: #f8fafc; font-size: 2rem; }
        .page-header p  { margin: 5px 0 0; color: #d1fae5; }
        .badge-box {
            background: #1f2937;
            padding: 8px 16px;
            border-radius: 8px;
            text-align: center;
            min-width: 90px;
            border: 1px solid #374151;
        }
        .badge-value { font-size: 1.4rem; font-weight: bold; color: #c7d2fe; }
        .badge-label { font-size: 0.75rem; color: #cbd5e1; }
        .metric-card {
            padding: 20px;
            border-radius: 12px;
            color: white;
            margin-bottom: 15px;
            background: linear-gradient(135deg, #6b2d1d, #b76f52);
        }
        .metric-card .label { font-size: 0.85rem; font-weight: 600; opacity: 0.9; }
        .metric-card .value { font-size: 2rem; font-weight: 800; margin: 8px 0; }
        .metric-card .sub   { font-size: 0.8rem; opacity: 0.85; font-style: italic; }
        .search-box {
            background: #111827;
            padding: 18px;
            border-radius: 12px;
            border: 1px solid #1f2937;
            margin-bottom: 20px;
        }
        .setting-card {
            background: #111827;
            padding: 20px;
            border-radius: 12px;
            border-top: 4px solid #8b4513;
            margin-bottom: 15px;
        }
        .setting-card h3 { margin: 0 0 8px; color: #f8fafc; }
        .setting-card p  { margin: 0; color: #cbd5e1; font-size: 0.9rem; }
    </style>
    """, unsafe_allow_html=True)

# ── Helper: Data ──────────────────────────────────────────────────────────────

@st.cache_data
def buat_data_dummy(jumlah: int) -> pd.DataFrame:
    return pd.DataFrame([{
        "ID"         : str(i + 1).zfill(4),
        "Nama Barang": random.choice(DAFTAR_BARANG),
        "Kategori"   : random.choice(["Bahan Baku", "Packaging", "Produk Jadi"]),
        "Gudang"     : random.choice(["A", "B", "C", "D"]),
        "Rak"        : random.choice(["1", "2", "3", "4", "5", "6"]),
        "Shelf"      : random.choice(["A1", "A2", "B1", "B2", "C1", "C2", "D1", "D2"]),
        "Stok"       : random.randint(5, 999),
    } for i in range(jumlah)])


def cari_data(df: pd.DataFrame, kata_kunci: str, kolom: list) -> tuple[pd.DataFrame, float]:
    """Sequential search O(n) — kembalikan (hasil, waktu_ms)."""
    mulai = time.perf_counter()
    mask = pd.Series(False, index=df.index)
    for col in kolom:
        if col in df.columns:
            mask |= df[col].astype(str).str.contains(kata_kunci.strip(), case=False, na=False)
    return df[mask], (time.perf_counter() - mulai) * 1000


def ensure_id(df: pd.DataFrame) -> pd.DataFrame:
    if "ID" not in df.columns:
        df = df.copy()
        df.insert(0, "ID", [str(i + 1).zfill(4) for i in range(len(df))])
    return df


def next_id(df: pd.DataFrame) -> str:
    nums = df["ID"].astype(str).str.extract(r"(\d+)$", expand=False).dropna()
    nums = [int(v) for v in nums if v.isdigit()]
    return str((max(nums) + 1) if nums else len(df) + 1).zfill(4)


def id_list(df: pd.DataFrame) -> list[str]:
    return df["ID"].astype(str).tolist() if "ID" in df.columns else []

# ── Session State ─────────────────────────────────────────────────────────────

def init_session():
    defaults = {
        "df": None, "data_source": None,
        "sort_col": "ID", "sort_asc": True,
        "halaman": "Data Barang",
    }
    for k, v in defaults.items():
        st.session_state.setdefault(k, v)

# ── Sidebar ───────────────────────────────────────────────────────────────────

def tampilkan_sidebar():
    with st.sidebar:
        st.markdown("""
        <h2 style='margin-bottom:0;'>🏭 SIGUDANG</h2>
        <p style='margin-top:0; opacity:0.7; font-size:0.85rem;'>Sistem Informasi Gudang</p>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        for ikon, nama in NAV_MENU:
            if st.button(f"{ikon}  {nama}", key=f"nav_{nama}", width="stretch"):
                st.session_state.halaman = nama
                st.rerun()

        st.markdown("<hr style='opacity:0.3;'>", unsafe_allow_html=True)

        df = st.session_state.df
        if st.session_state.halaman != "Data Barang" or df is None:
            return

        src = str(st.session_state.data_source)
        label = f"Data Dummy ({len(df)} item)" if src.startswith("dummy") else src
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.06); border:1px solid rgba(148,163,184,0.25);
             border-radius:8px; padding:10px 14px;">
            <div style="color:#818cf8; font-size:0.7rem; font-weight:600;">DATA AKTIF</div>
            <div style="color:#f8fafc; font-size:0.85rem; margin-top:4px;">📋 {label}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr style='opacity:0.3;'>", unsafe_allow_html=True)
        st.markdown("<div style='color:#cbd5e1; font-size:0.75rem; font-weight:600;'>OPSI SORTIR</div>", unsafe_allow_html=True)

        cols = list(df.columns)
        idx = cols.index(st.session_state.sort_col) if st.session_state.sort_col in cols else 0
        st.session_state.sort_col = st.selectbox("Kolom", cols, index=idx)
        st.session_state.sort_asc = "⬆️" in st.radio("Arah", ["⬆️ Kecil → Besar", "⬇️ Besar → Kecil"])

# ── Halaman: Data Barang ──────────────────────────────────────────────────────

def halaman_data_barang():
    df = st.session_state.df

    n_gudang   = df["Gudang"].nunique()   if df is not None and "Gudang"   in df.columns else 0
    n_kategori = df["Kategori"].nunique() if df is not None and "Kategori" in df.columns else 0

    st.markdown(f"""
    <div class="page-header">
        <div>
            <h1>📦 Data Barang</h1>
            <p>SIGUDANG — Manajemen Inventaris Gudang Skincare</p>
        </div>
        <div style="display:flex; gap:12px;">
            <div class="badge-box">
                <div class="badge-value">{n_gudang}</div>
                <div class="badge-label">Gudang</div>
            </div>
            <div class="badge-box">
                <div class="badge-value">{n_kategori}</div>
                <div class="badge-label">Kategori</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if df is None:
        st.markdown("""
        <div style="background:#111827; border-radius:12px; padding:50px; text-align:center; border:1px solid #334155;">
            <div style="font-size:4rem;">📦</div>
            <h3 style="color:#f8fafc; margin:10px 0;">Belum Ada Data</h3>
            <p style="color:#cbd5e1;">Buka halaman <b>⚙️ Pengaturan</b> untuk membuat data dummy atau upload file CSV.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    if "ID" not in df.columns:
        st.session_state.df = df = ensure_id(df)

    # Form pencarian
    st.markdown('<div class="search-box">', unsafe_allow_html=True)
    c1, c2 = st.columns([4, 2])
    kata_kunci = c1.text_input("Cari", placeholder="🔍 Ketik nama barang, kategori, lokasi...", label_visibility="collapsed")
    filter_key = c2.selectbox("Filter", list(FILTER_KOLOM.keys()), label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)

    kolom_aktif = FILTER_KOLOM[filter_key] or list(df.columns)

    # Cari + sortir
    if kata_kunci:
        hasil, waktu_ms = cari_data(df, kata_kunci, kolom_aktif)
    else:
        hasil, waktu_ms = df.copy(), 0.0

    sc, sa = st.session_state.sort_col, st.session_state.sort_asc
    if sc in hasil.columns:
        hasil = hasil.sort_values(by=sc, ascending=sa, ignore_index=True)

    # Statistik ringkas
    st.markdown(f"""
    <div class="metric-card">
        <div class="label">TOTAL ITEM DITAMPILKAN</div>
        <div class="value">{len(hasil):,}</div>
        <div class="sub">dari {len(df):,} barang terdaftar</div>
    </div>
    """, unsafe_allow_html=True)

    # Status bar
    c1, c2, c3 = st.columns([5, 2, 1])
    with c1:
        if kata_kunci:
            st.markdown(f'Hasil: **"{kata_kunci}"** — **{len(hasil)}** ditemukan ⏱ {waktu_ms:.2f} ms')
        else:
            st.markdown(f'Menampilkan **{len(hasil)}** item.')
    c2.markdown(f'<div style="text-align:right; color:#cbd5e1;">{"⬆️" if sa else "⬇️"} <b>{sc}</b></div>', unsafe_allow_html=True)
    c3.download_button("⬇️ CSV", data=hasil.to_csv(index=False).encode("utf-8"),
                       file_name="data_gudang.csv", mime="text/csv", width="stretch")

    if hasil.empty:
        st.markdown("""
        <div style="text-align:center; padding:40px; background:#111827; border-radius:12px;">
            <div style="font-size:2.5rem;">🔍</div>
            <h4 style="color:#cbd5e1;">Data Tidak Ditemukan</h4>
            <p style="color:#94a3b8; font-size:0.85rem;">Coba periksa kembali ejaan kata kunci Anda.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    def sorot_baris(row):
        cocok = any(
            kata_kunci.lower() in str(row[c]).lower()
            for c in kolom_aktif if c in row.index
        )
        style = "background-color: #1e293b; color: #c7d2fe;" if (kata_kunci and cocok) else ""
        return [style] * len(row)

    st.dataframe(
        hasil.style.apply(sorot_baris, axis=1).format({"Stok": "{:,}"}),
        width="stretch",
        height=min(550, max(200, len(hasil) * 38 + 60)),
        column_config=KOLOM_CONFIG,
        hide_index=True,
    )

# ── Halaman: Kelola Data ──────────────────────────────────────────────────────

def _opts_dari_df(col: str) -> list[str]:
    """Ambil nilai unik dari kolom df aktif, sudah terurut."""
    df = st.session_state.get("df")
    if df is None or col not in df.columns:
        return []
    return sorted(df[col].dropna().astype(str).unique().tolist())


def _selectbox_dengan_fallback(label, col, default, prefix):
    """Selectbox jika ada opsi, text_input jika tidak."""
    opts = _opts_dari_df(col)
    cur  = str(default)
    key  = f"{prefix}_{col.lower().replace(' ', '_')}"
    if opts:
        if cur not in opts:
            opts = [cur] + opts
        return st.selectbox(label, opts, index=opts.index(cur), key=key)
    return st.text_input(label, value=cur, key=key)


def _form_fields(prefix: str, defaults: dict) -> dict:
    """Render field input barang, kembalikan dict nilai."""
    nama = st.text_input(
        "Nama Barang",
        value="" if prefix == "edit" else defaults.get("Nama Barang", ""),
        key=f"{prefix}_nama",
    )
    kategori = _selectbox_dengan_fallback("Kategori", "Kategori", defaults.get("Kategori", "Produk Jadi"), prefix)
    gudang   = _selectbox_dengan_fallback("Gudang",   "Gudang",   defaults.get("Gudang",   "A"),           prefix)
    rak      = _selectbox_dengan_fallback("Rak",      "Rak",      defaults.get("Rak",      "1"),           prefix)
    shelf    = _selectbox_dengan_fallback("Shelf",    "Shelf",    defaults.get("Shelf",    "A1"),          prefix)
    stok     = st.number_input("Stok", min_value=0, value=int(defaults.get("Stok", 0)), step=1, key=f"{prefix}_stok")
    return {"Nama Barang": nama, "Kategori": kategori, "Gudang": gudang,
            "Rak": rak, "Shelf": shelf, "Stok": stok}


def _bersihkan_vals(vals: dict) -> dict:
    return {k: v.strip() if isinstance(v, str) else int(v) for k, v in vals.items()}


def halaman_kelola_data():
    st.markdown("""
    <div style="background:#111827; padding:15px 20px; border-radius:12px;
         margin-bottom:20px; border-left:6px solid #8b4513;">
        <h2 style="margin:0; color:#f8fafc;">🛠️ Kelola Data</h2>
        <p style="margin:5px 0 0; color:#cbd5e1; font-size:0.9rem;">Tambah, edit, atau hapus item inventaris.</p>
    </div>
    """, unsafe_allow_html=True)

    df = st.session_state.df
    if df is None:
        st.info("Belum ada data aktif. Buka halaman Pengaturan untuk membuat atau upload data.")
        return

    if "ID" not in df.columns:
        st.session_state.df = df = ensure_id(df)

    ids = id_list(df)
    col_tambah, col_edit, col_hapus = st.columns(3)

    # ── Tambah ────────────────────────────────────────────────────────────────
    with col_tambah:
        with st.form("form_tambah"):
            st.subheader("Tambah Data Baru")
            vals = _form_fields("tambah", {})
            submit = st.form_submit_button("Tambah Data")
        if submit:
            if not vals["Nama Barang"].strip():
                st.warning("Nama Barang tidak boleh kosong.")
            else:
                baru = {"ID": next_id(df), **_bersihkan_vals(vals)}
                st.session_state.df = pd.concat([df, pd.DataFrame([baru])], ignore_index=True)
                st.success("Barang baru berhasil ditambahkan.")

    # ── Edit ──────────────────────────────────────────────────────────────────
    with col_edit:
        with st.form("form_edit"):
            st.subheader("Edit Data")
            edit_id = st.selectbox("Pilih ID", ids, key="edit_id_select")
            row  = df[df["ID"] == edit_id].iloc[0].to_dict()
            vals = _form_fields("edit", row)
            submit = st.form_submit_button("Simpan Perubahan")
        if submit:
            if not vals["Nama Barang"].strip():
                st.warning("Nama Barang tidak boleh kosong.")
            else:
                idx = df.index[df["ID"] == edit_id][0]
                for k, v in _bersihkan_vals(vals).items():
                    df.loc[idx, k] = v
                st.session_state.df = df
                st.success(f"Data ID {edit_id} berhasil diperbarui.")

    # ── Hapus ─────────────────────────────────────────────────────────────────
    with col_hapus:
        with st.form("form_hapus"):
            st.subheader("Hapus Data")
            hapus_ids = st.multiselect("Pilih ID", ids, key="hapus_ids_select")
            submit = st.form_submit_button("Hapus Item")
        if submit:
            if not hapus_ids:
                st.warning("Pilih minimal satu ID untuk dihapus.")
            else:
                st.session_state.df = df.drop(df[df["ID"].isin(hapus_ids)].index).reset_index(drop=True)
                st.success(f"{len(hapus_ids)} item berhasil dihapus.")

# ── Halaman: Pengaturan ───────────────────────────────────────────────────────

def halaman_pengaturan():
    st.markdown("""
    <div style="background:#111827; padding:15px 20px; border-radius:12px;
         margin-bottom:20px; border-left:6px solid #8b4513;">
        <h2 style="margin:0; color:#f8fafc;">⚙️ Pengaturan</h2>
        <p style="margin:5px 0 0; color:#cbd5e1; font-size:0.9rem;">Konfigurasi sumber data gudang</p>
    </div>
    """, unsafe_allow_html=True)

    # Generate dummy
    st.markdown('<div class="setting-card"><h3>📋 Buat Data Dummy</h3><p>Generate data inventaris acak untuk simulasi.</p></div>', unsafe_allow_html=True)
    c1, c2 = st.columns([3, 1])
    jumlah = c1.slider("Jumlah baris data", 100, 1000, 500, step=50)
    c1.caption(f"Akan dibuat **{jumlah}** baris data acak.")
    c2.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    if c2.button("🔄 Generate Data", type="primary", width="stretch"):
        st.cache_data.clear()
        st.session_state.update(df=buat_data_dummy(jumlah), data_source=f"dummy_{jumlah}",
                                sort_col="ID", sort_asc=True, halaman="Data Barang")
        st.toast("Data berhasil dibuat!", icon="✅")
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Upload CSV
    st.markdown('<div class="setting-card"><h3>📂 Upload File CSV</h3><p>Gunakan data gudang nyata dari file .CSV milik Anda.</p></div>', unsafe_allow_html=True)
    c1, c2 = st.columns([2, 1])
    with c1:
        file = st.file_uploader("Upload file CSV", type=["csv"], label_visibility="collapsed")
        if file:
            try:
                df_upload = pd.read_csv(file)
                st.session_state.update(df=df_upload, data_source=file.name,
                                        sort_col=df_upload.columns[0], sort_asc=True)
                st.success(f"File '{file.name}' berhasil diunggah!")
                st.rerun()
            except Exception as e:
                st.error(f"Gagal membaca file: {e}")
    c2.markdown("""
    <div style="background:#111827; border-radius:10px; padding:14px;
         font-size:0.8rem; color:#cbd5e1; border:1px dashed #4b5563;">
        <b>Format kolom yang disarankan:</b><br>
        <code>ID, Nama Barang, Kategori, Gudang, Rak, Shelf, Stok</code>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Status data aktif
    st.markdown('<div class="setting-card"><h3>📊 Status Data Saat Ini</h3></div>', unsafe_allow_html=True)
    df = st.session_state.df
    if df is None:
        st.info("Belum ada data aktif. Silakan generate dummy atau upload CSV terlebih dahulu.")
        return

    src  = str(st.session_state.data_source)
    tipe = "Data Dummy" if src.startswith("dummy") else f"File: {src}"
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Sumber Data",  tipe[:20])
    k2.metric("Jumlah Baris", f"{len(df):,}")
    k3.metric("Jumlah Kolom", len(df.columns))
    k4.metric("Total Stok",   f'{int(df["Stok"].sum()):,}' if "Stok" in df.columns else "—")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑️ Hapus Data", type="secondary", width="stretch"):
        st.session_state.update(df=None, data_source=None)
        st.toast("Data dihapus!", icon="🗑️")
        st.rerun()

# ── Halaman: Tentang Sistem ───────────────────────────────────────────────────

def halaman_tentang():
    st.markdown("""
    <div style="background:#111827; border-radius:14px; padding:28px 32px;
         border:1px solid #1f2937; margin-bottom:16px;">
        <h2 style="color:#f8fafc; margin-top:0;">📘 Tentang Sistem</h2>
        <p style="color:#94a3b8; margin:0;">Penjelasan singkat cara kerja SIGUDANG di balik layar.</p>
    </div>
    """, unsafe_allow_html=True)

    sections = [
        ("🔎 Sequential Search", [
            "Pencarian dilakukan dengan mengecek tiap baris data satu per satu dari atas ke bawah.",
            "Kalau kata kunci ketemu di kolom mana pun, baris itu langsung masuk hasil.",
            "Sederhana dan cukup untuk skala data gudang seperti ini, kompleksitas waktu <b>O(n)</b>.",
        ]),
        ("🔄 Timsort", [
            "Semua pengurutan pakai fungsi bawaan Pandas yaitu <code>sort_values()</code>.",
            "Di balik layar, Pandas pakai Timsort — gabungan merge sort dan insertion sort.",
            "Hasilnya cepat dan stabil, kompleksitas waktu <b>O(n log n)</b>.",
        ]),
        ("📦 Manajemen Inventaris", [
            "Data barang disimpan lengkap dengan lokasi: Gudang, Rak, dan Shelf.",
            "Stok bisa dipantau langsung, ditambah, diedit, atau dihapus kapan saja.",
            "Semua perubahan langsung tersimpan di sesi yang sedang aktif.",
        ]),
        ("📂 Sumber Data", [
            "Bisa pakai data dummy yang di-generate otomatis, atau upload CSV sendiri.",
            "Data hanya tersimpan selama sesi berlangsung — refresh halaman = data hilang.",
            "Untuk menyimpan permanen, gunakan tombol unduh CSV yang ada di halaman Data Barang.",
        ]),
        ("⚙️ Teknologi yang Dipakai", [
            "Ditulis pakai <b>Python</b> dengan framework <b>Streamlit</b> untuk antarmukanya.",
            "Pengolahan data pakai <b>Pandas</b>. Tidak ada database eksternal.",
        ]),
    ]

    for judul, poin in sections:
        isi = "".join(f'<li style="color:#cbd5e1; margin-bottom:6px;">{p}</li>' for p in poin)
        st.markdown(f"""
        <div style="background:#1f2937; border-radius:10px; padding:20px 24px;
             margin-bottom:12px; border-left:4px solid #8b4513;">
            <h3 style="color:#f8fafc; margin:0 0 12px;">{judul}</h3>
            <ul style="margin:0; padding-left:20px; line-height:1.8;">{isi}</ul>
        </div>
        """, unsafe_allow_html=True)

# ── Entry Point ───────────────────────────────────────────────────────────────

HALAMAN = {
    "Data Barang"   : halaman_data_barang,
    "Kelola Data"   : halaman_kelola_data,
    "Pengaturan"    : halaman_pengaturan,
    "Tentang Sistem": halaman_tentang,
}

def main():
    apply_styles()
    init_session()
    tampilkan_sidebar()
    HALAMAN[st.session_state.halaman]()

if __name__ == "__main__" or True:
    main()