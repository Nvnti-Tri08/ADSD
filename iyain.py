import streamlit as st
import pandas as pd
import random
import time

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="SIGUDANG - Sistem Informasi Gudang",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    * { font-family: 'Poppins', sans-serif; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .stApp { background: #f0f2f5; }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%) !important;
        border-right: none !important;
    }
    [data-testid="stSidebar"] * { color: #e0e0e0 !important; }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 { color: #ffffff !important; }
    [data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.15) !important; }
    [data-testid="stSidebar"] label {
        color: #b0b8c8 !important;
        font-size: 0.82rem !important;
        font-weight: 500 !important;
    }

    .sister-header {
        background: linear-gradient(135deg, #2d6a4f 0%, #40916c 50%, #52b788 100%);
        padding: 18px 28px;
        border-radius: 12px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 4px 20px rgba(45, 106, 79, 0.35);
    }
    .sister-header-left h1 {
        color: white !important; font-size: 1.5rem !important;
        font-weight: 700 !important; margin: 0 !important; padding: 0 !important;
    }
    .sister-header-left p {
        color: rgba(255,255,255,0.85) !important;
        font-size: 0.82rem !important; margin: 2px 0 0 0 !important;
    }
    .sister-header-badge {
        background: rgba(255,255,255,0.2);
        border: 1px solid rgba(255,255,255,0.35);
        border-radius: 8px; padding: 8px 16px; text-align: center;
    }
    .sister-header-badge .badge-val {
        color: white !important; font-size: 1.4rem !important;
        font-weight: 700 !important; line-height: 1;
    }
    .sister-header-badge .badge-lbl { color: rgba(255,255,255,0.8) !important; font-size: 0.72rem !important; }

    .metric-card {
        background: white; border-radius: 12px; padding: 18px 20px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.07);
        border-left: 4px solid #40916c;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .metric-card:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,0.12); }
    .metric-card.blue  { border-left-color: #2196F3; }
    .metric-card.orange{ border-left-color: #FF9800; }
    .metric-card.purple{ border-left-color: #9C27B0; }
    .metric-card.green { border-left-color: #40916c; }
    .metric-card .mc-label {
        color: #888 !important; font-size: 0.75rem !important;
        font-weight: 600 !important; text-transform: uppercase !important;
        letter-spacing: 0.07em !important; margin-bottom: 6px;
    }
    .metric-card .mc-value { color: #1a1a2e !important; font-size: 1.6rem !important; font-weight: 700 !important; line-height: 1; }
    .metric-card .mc-sub  { color: #aaa !important; font-size: 0.72rem !important; margin-top: 4px; }

    .search-card {
        background: white; border-radius: 12px;
        padding: 20px 24px; box-shadow: 0 2px 12px rgba(0,0,0,0.07); margin-bottom: 16px;
    }
    .table-card {
        background: white; border-radius: 12px;
        padding: 20px; box-shadow: 0 2px 12px rgba(0,0,0,0.07); margin-top: 8px;
    }
    .setting-card {
        background: white; border-radius: 12px;
        padding: 28px 32px; box-shadow: 0 2px 12px rgba(0,0,0,0.07); margin-bottom: 20px;
    }
    .setting-card h3 { color: #1a1a2e !important; font-size: 1rem !important; font-weight: 600 !important; margin-bottom: 4px !important; }
    .setting-card p  { color: #888 !important; font-size: 0.82rem !important; margin-bottom: 16px !important; }

    .highlight-badge {
        background: #fff3cd; color: #856404;
        border: 1px solid #ffc107; border-radius: 20px;
        padding: 4px 12px; font-size: 0.78rem; font-weight: 600;
        display: inline-block; margin-left: 8px;
    }
    .sort-info {
        background: #e8f5e9; border: 1px solid #a5d6a7;
        border-radius: 8px; padding: 6px 14px;
        font-size: 0.78rem; color: #2d6a4f; font-weight: 500;
        display: inline-flex; align-items: center; gap: 6px;
    }
    .time-pill {
        background: linear-gradient(135deg, #e8f5e9, #f1f8e9);
        border: 1px solid #a5d6a7; border-radius: 20px;
        padding: 4px 14px; font-size: 0.76rem; color: #2d6a4f;
        font-weight: 600; display: inline-block;
    }

    /* Nav button style */
    .stButton button {
        background: transparent !important;
        color: #b0b8c8 !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        font-size: 0.88rem !important;
        text-align: left !important;
        padding: 10px 14px !important;
        width: 100% !important;
        transition: all 0.2s !important;
    }
    .stButton button:hover {
        background: rgba(255,255,255,0.08) !important;
        color: white !important;
    }

    /* Active nav */
    .nav-active button {
        background: rgba(64,145,108,0.25) !important;
        color: #52b788 !important;
        font-weight: 600 !important;
        border-left: 3px solid #52b788 !important;
    }

    /* Green action button */
    .btn-green button,
    .search-card .stButton button {
        background: linear-gradient(135deg, #f9c846, #f08f00) !important;
        color: #1a1a2e !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        padding: 14px 22px !important;
        letter-spacing: 0.02em !important;
        min-height: 52px !important;
        box-shadow: 0 6px 18px rgba(240, 143, 0, 0.25) !important;
    }
    .btn-green button:hover,
    .search-card .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(240, 143, 0, 0.35) !important;
    }

    .stDownloadButton button {
        background: white !important; color: #40916c !important;
        border: 1.5px solid #40916c !important; border-radius: 8px !important;
        font-weight: 600 !important;
    }
    .stTextInput input {
        border-radius: 8px !important; border: 1.5px solid #e0e0e0 !important;
        padding: 10px 14px !important; font-size: 0.9rem !important;
    }
    .stTextInput input:focus { border-color: #40916c !important; box-shadow: 0 0 0 3px rgba(64,145,108,0.15) !important; }
    .stAlert { border-radius: 8px !important; }
    .block-container { padding: 1.5rem 2rem !important; max-width: 100% !important; }
</style>
""", unsafe_allow_html=True)


# =========================
# DATA GENERATOR
# =========================
NAMA_BARANG = [
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

@st.cache_data
def generate_data(n=500):
    gudang   = ["A", "B", "C", "D"]
    rak      = ["1", "2", "3", "4", "5", "6"]
    shelf    = ["A1", "A2", "B1", "B2", "C1", "C2", "D1", "D2"]
    kategori = ["Bahan Baku", "Packaging", "Produk Jadi"]
    data = []
    for i in range(n):
        data.append({
            "ID"         : str(i + 1).zfill(4),
            "Nama Barang": random.choice(NAMA_BARANG),
            "Kategori"   : random.choice(kategori),
            "Gudang"     : random.choice(gudang),
            "Rak"        : random.choice(rak),
            "Shelf"      : random.choice(shelf),
            "Stok"       : random.randint(5, 999),
        })
    return pd.DataFrame(data)


def search_dataframe(df, query, columns):
    if not query.strip():
        return df, 0.0
    start  = time.perf_counter()
    mask   = pd.Series(False, index=df.index)
    for col in columns:
        if col in df.columns:
            mask |= df[col].astype(str).str.contains(query.strip(), case=False, na=False)
    elapsed = (time.perf_counter() - start) * 1000
    return df[mask], elapsed


# =========================
# SESSION STATE
# =========================
for key, val in {
    "df": None, "data_source": None,
    "sort_col": "ID", "sort_asc": True,
    "page": "Data Barang",
}.items():
    if key not in st.session_state:
        st.session_state[key] = val


# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown("""
    <div style="padding:10px 0 20px 0; text-align:center;">
        <div style="font-size:2rem;">🏭</div>
        <div style="color:white; font-size:1.1rem; font-weight:700; margin-top:4px;">SIGUDANG</div>
        <div style="color:#8899aa; font-size:0.72rem; margin-top:2px;">Sistem Informasi Gudang</div>
    </div>
    <hr style="margin:0 0 8px 0;">
    """, unsafe_allow_html=True)

    # --- Navigation buttons ---
    pages = [
        ("📦", "Data Barang"),
        ("⚙️", "Pengaturan"),
    ]
    for icon, name in pages:
        is_active = st.session_state.page == name
        container = st.container()
        with container:
            if is_active:
                st.markdown('<div class="nav-active">', unsafe_allow_html=True)
            if st.button(f"{icon}  {name}", key=f"nav_{name}", use_container_width=True):
                st.session_state.page = name
                st.rerun()
            if is_active:
                st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<hr style='margin:12px 0;'>", unsafe_allow_html=True)

    # Info data aktif
    if st.session_state.df is not None:
        n = len(st.session_state.df)
        src = str(st.session_state.data_source)
        label = f"Data Dummy ({n} item)" if src.startswith("dummy") else src
        st.markdown(f"""
        <div style="background:rgba(64,145,108,0.15); border:1px solid rgba(64,145,108,0.3);
             border-radius:8px; padding:10px 14px; margin-top:4px;">
            <div style="color:#52b788; font-size:0.7rem; font-weight:600; text-transform:uppercase; letter-spacing:0.07em;">Data Aktif</div>
            <div style="color:white; font-size:0.82rem; margin-top:4px;">📋 {label}</div>
        </div>
        """, unsafe_allow_html=True)

    # Sorting — hanya tampil di halaman Data Barang
    if st.session_state.page == "Data Barang" and st.session_state.df is not None:
        df_tmp = st.session_state.df
        st.markdown("<hr style='margin:12px 0;'>", unsafe_allow_html=True)
        st.markdown("<div style='color:#8899aa; font-size:0.72rem; font-weight:600; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:10px;'>SORTING</div>", unsafe_allow_html=True)
        col_opts = list(df_tmp.columns)
        sort_col_dd = st.selectbox(
            "Kolom", col_opts,
            index=col_opts.index(st.session_state.sort_col) if st.session_state.sort_col in col_opts else 0,
            label_visibility="visible"
        )
        sort_dir_dd = st.radio(
            "Arah",
            ["⬆️ A → Z / Kecil → Besar", "⬇️ Z → A / Besar → Kecil"],
            label_visibility="visible"
        )
        st.session_state.sort_col = sort_col_dd
        st.session_state.sort_asc = "⬆️" in sort_dir_dd
        st.markdown("<div style='color:#8899aa; font-size:0.72rem; margin-top:4px;'>💡 Atau klik header kolom di tabel</div>", unsafe_allow_html=True)


# =========================
# PAGE: DATA BARANG
# =========================
def page_data_barang():
    df = st.session_state.df

    # Header
    n_gudang  = df["Gudang"].nunique() if df is not None and "Gudang" in df.columns else 0
    n_kat     = df["Kategori"].nunique() if df is not None and "Kategori" in df.columns else 0
    st.markdown(f"""
    <div class="sister-header">
        <div class="sister-header-left">
            <h1>📦 Data Barang</h1>
            <p>SIGUDANG — Sistem Informasi Manajemen Gudang Kosmetik</p>
        </div>
        <div style="display:flex; gap:12px;">
            <div class="sister-header-badge">
                <div class="badge-val">{n_gudang}</div>
                <div class="badge-lbl">Gudang</div>
            </div>
            <div class="sister-header-badge">
                <div class="badge-val">{n_kat}</div>
                <div class="badge-lbl">Kategori</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if df is None:
        st.markdown("""
        <div style="background:white; border-radius:12px; padding:56px; text-align:center; box-shadow:0 2px 12px rgba(0,0,0,0.07);">
            <div style="font-size:3.5rem;">📦</div>
            <h3 style="color:#1a1a2e; margin:14px 0 8px;">Belum ada data</h3>
            <p style="color:#888; font-size:0.88rem;">
                Buka halaman <b>⚙️ Pengaturan</b> di sidebar untuk memuat data dummy<br>
                atau upload file CSV Anda sendiri.
            </p>
        </div>
        """, unsafe_allow_html=True)
        return

    # Search bar
    st.markdown('<div class="search-card">', unsafe_allow_html=True)
    sc1, sc2, sc3 = st.columns([4, 2, 1])
    with sc1:
        search_query = st.text_input(
            "Cari", placeholder="🔍  Ketik nama barang, kategori, gudang, rak, shelf...",
            label_visibility="collapsed"
        )
    with sc2:
        search_cols_map = {
            "🔎 Semua Kolom" : list(df.columns),
            "📦 Nama Barang" : ["Nama Barang"],
            "🏷️ Kategori"    : ["Kategori"],
            "🏭 Gudang"      : ["Gudang"],
            "📚 Rak"         : ["Rak"],
            "📌 Shelf"       : ["Shelf"],
        }
        search_in = st.selectbox("Cari di", list(search_cols_map.keys()), label_visibility="collapsed")
    with sc3:
        st.markdown('<div class="btn-green">', unsafe_allow_html=True)
        st.button("Cari", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Apply search
    search_time = None
    filtered    = df.copy()
    if search_query:
        filtered, search_time = search_dataframe(filtered, search_query, search_cols_map[search_in])

    # Apply sort
    sc = st.session_state.sort_col
    sa = st.session_state.sort_asc
    if sc in filtered.columns:
        filtered = filtered.sort_values(by=sc, ascending=sa, ignore_index=True)

    # Metric cards
    total_items = len(filtered)
    total_all   = len(df)
    total_stok  = int(filtered["Stok"].sum()) if "Stok" in filtered.columns and not filtered.empty else 0
    avg_stok    = round(filtered["Stok"].mean(), 1) if "Stok" in filtered.columns and not filtered.empty else 0
    n_gudang_f  = filtered["Gudang"].nunique() if "Gudang" in filtered.columns else 0

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f'<div class="metric-card green"><div class="mc-label">Total Item</div><div class="mc-value">{total_items:,}</div><div class="mc-sub">dari {total_all:,} item</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric-card blue"><div class="mc-label">Total Stok</div><div class="mc-value">{total_stok:,}</div><div class="mc-sub">unit tersedia</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="metric-card orange"><div class="mc-label">Rata-rata Stok</div><div class="mc-value">{avg_stok:,}</div><div class="mc-sub">per item</div></div>', unsafe_allow_html=True)
    with m4:
        st.markdown(f'<div class="metric-card purple"><div class="mc-label">Gudang Aktif</div><div class="mc-value">{n_gudang_f}</div><div class="mc-sub">lokasi</div></div>', unsafe_allow_html=True)

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

    # Status bar
    c1, c2, c3 = st.columns([5, 2, 1])
    with c1:
        if search_query:
            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:10px; padding:6px 0;">
                <span style="color:#1a1a2e; font-size:0.88rem; font-weight:500;">🔍 Hasil: "<b>{search_query}</b>"</span>
                <span class="highlight-badge">{len(filtered)} item</span>
                {f'<span class="time-pill">⏱ {search_time:.3f} ms</span>' if search_time else ''}
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="color:#555; font-size:0.87rem; padding:6px 0;">📋 Menampilkan <b>{len(filtered)}</b> item {"(semua data)" if len(filtered)==total_all else f"dari {total_all}"}</div>', unsafe_allow_html=True)
    with c2:
        arrow = "⬆️" if sa else "⬇️"
        st.markdown(f'<div class="sort-info">{arrow} <b>{sc}</b></div>', unsafe_allow_html=True)
    with c3:
        csv_bytes = filtered.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ CSV", data=csv_bytes, file_name="data_gudang.csv", mime="text/csv", use_container_width=True)

    # Table
    st.markdown('<div class="table-card">', unsafe_allow_html=True)
    if filtered.empty:
        st.markdown("""
        <div style="text-align:center; padding:40px 20px;">
            <div style="font-size:2.5rem;">🔍</div>
            <h4 style="color:#555; margin:10px 0 6px;">Tidak ada hasil</h4>
            <p style="color:#999; font-size:0.85rem;">Coba ubah kata kunci pencarian.</p>
        </div>""", unsafe_allow_html=True)
    else:
        def highlight_row(row):
            if search_query:
                for col in search_cols_map[search_in]:
                    if col in row.index and search_query.lower() in str(row[col]).lower():
                        return ["background-color: #fffde7;"] * len(row)
            return [""] * len(row)

        styled = (
            filtered.style
            .apply(highlight_row, axis=1)
            .format({"Stok": "{:,}"})
        )
        st.dataframe(
            styled,
            use_container_width=True,
            height=min(600, max(200, len(filtered) * 38 + 60)),
            column_config={
                "ID"         : st.column_config.TextColumn("ID", width=60),
                "Nama Barang": st.column_config.TextColumn("Nama Barang", width=220),
                "Kategori"   : st.column_config.TextColumn("Kategori", width=130),
                "Gudang"     : st.column_config.TextColumn("Gudang", width=80),
                "Rak"        : st.column_config.TextColumn("Rak", width=70),
                "Shelf"      : st.column_config.TextColumn("Shelf", width=80),
                "Stok"       : st.column_config.NumberColumn("Stok", width=90, format="%d pcs"),
            },
            hide_index=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# PAGE: PENGATURAN
# =========================
def page_pengaturan():
    st.markdown("""
    <div class="sister-header">
        <div class="sister-header-left">
            <h1>⚙️ Pengaturan</h1>
            <p>SIGUDANG — Konfigurasi sumber data dan preferensi aplikasi</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- Kartu 1: Data Dummy ---
    st.markdown('<div class="setting-card">', unsafe_allow_html=True)
    st.markdown("""
    <h3>📋 Generate Data Dummy</h3>
    <p>Buat data barang acak untuk keperluan testing atau demo aplikasi.</p>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns([3, 1])
    with col_a:
        jumlah = st.slider("Jumlah data yang di-generate", 100, 1000, 500, step=50)
        st.caption(f"Akan membuat **{jumlah}** baris data dengan kolom: ID, Nama Barang, Kategori, Gudang, Rak, Shelf, Stok")
    with col_b:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        st.markdown('<div class="btn-green">', unsafe_allow_html=True)
        if st.button("🔄 Generate Sekarang", use_container_width=True):
            generate_data.clear()
            st.session_state.df          = generate_data(jumlah)
            st.session_state.data_source = f"dummy_{jumlah}"
            st.session_state.sort_col    = "ID"
            st.session_state.sort_asc    = True
            st.success(f"✅ Berhasil generate **{jumlah}** data dummy!")
            st.toast("Data berhasil dibuat!", icon="✅")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Kartu 2: Upload CSV ---
    st.markdown('<div class="setting-card">', unsafe_allow_html=True)
    st.markdown("""
    <h3>📂 Upload File CSV</h3>
    <p>Muat data dari file CSV milik Anda. Pastikan file memiliki kolom yang sesuai.</p>
    """, unsafe_allow_html=True)

    col_c, col_d = st.columns([2, 1])
    with col_c:
        uploaded = st.file_uploader("Pilih file CSV", type=["csv"], label_visibility="collapsed")
        if uploaded:
            try:
                df_up = pd.read_csv(uploaded)
                st.session_state.df          = df_up
                st.session_state.data_source = uploaded.name
                st.session_state.sort_col    = df_up.columns[0]
                st.session_state.sort_asc    = True
                st.success(f"✅ **{uploaded.name}** berhasil dimuat — {len(df_up):,} baris, {len(df_up.columns)} kolom")
                st.toast("CSV berhasil dimuat!", icon="📂")
            except Exception as e:
                st.error(f"❌ Gagal membaca CSV: {e}")
    with col_d:
        st.markdown("""
        <div style="background:#f8f9fa; border-radius:10px; padding:16px; font-size:0.82rem; color:#555;">
            <b>Format kolom disarankan:</b><br><br>
            <code>ID, Nama Barang, Kategori,<br>Gudang, Rak, Shelf, Stok</code><br><br>
            <span style="color:#888;">Format lain juga bisa dimuat, namun fitur sorting/search menyesuaikan nama kolom CSV Anda.</span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Kartu 3: Status data aktif ---
    st.markdown('<div class="setting-card">', unsafe_allow_html=True)
    st.markdown("<h3>📊 Status Data Aktif</h3>", unsafe_allow_html=True)
    df = st.session_state.df
    if df is not None:
        src = str(st.session_state.data_source)
        tipe = "Data Dummy" if src.startswith("dummy") else f"CSV: {src}"
        s1, s2, s3, s4 = st.columns(4)
        s1.metric("Sumber", tipe if len(tipe) < 18 else tipe[:16]+"…")
        s2.metric("Total Baris", f"{len(df):,}")
        s3.metric("Total Kolom", len(df.columns))
        s4.metric("Total Stok", f'{int(df["Stok"].sum()):,}' if "Stok" in df.columns else "—")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑️ Hapus Data Aktif", type="secondary"):
            st.session_state.df          = None
            st.session_state.data_source = None
            st.rerun()
    else:
        st.info("ℹ️ Belum ada data yang dimuat. Generate data dummy atau upload CSV di atas.")
    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# ROUTER
# =========================
if st.session_state.page == "Data Barang":
    page_data_barang()
elif st.session_state.page == "Pengaturan":
    page_pengaturan()