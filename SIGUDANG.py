import time
import random

import pandas as pd
import streamlit as st

# KONFIGURASI HALAMAN
st.set_page_config(
    page_title="SIGUDANG - Sistem Informasi Gudang Skincare",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ALGORITMA UTAMA
def linear_search(data: list[dict], kata_kunci: str, kolom: list[str]) -> tuple:
    mulai = time.perf_counter()
    hasil = []
    kw = kata_kunci.strip().lower()
    for i, baris in enumerate(data):
        for col in kolom:
            if kw in str(baris.get(col, "")).lower():
                hasil.append(baris)
                break
    waktu_ms = (time.perf_counter() - mulai) * 1000
    return hasil, len(data), waktu_ms


def _ambil_nilai(baris: dict, kolom: str):
    val = baris.get(kolom, "")
    if isinstance(val, (int, float)):
        return val
    try:
        return float(val)
    except (ValueError, TypeError):
        return str(val).lower()


def insertion_sort(data: list[dict], kolom: str, ascending: bool = True) -> tuple:
    mulai = time.perf_counter()
    arr = [b.copy() for b in data]
    perbandingan = 0
    for i in range(1, len(arr)):
        kunci = arr[i]
        nilai_kunci = _ambil_nilai(kunci, kolom)
        j = i - 1
        while j >= 0:
            perbandingan += 1
            nilai_j = _ambil_nilai(arr[j], kolom)
            harus_geser = nilai_j > nilai_kunci if ascending else nilai_j < nilai_kunci
            if harus_geser:
                arr[j + 1] = arr[j]
                j -= 1
            else:
                break
        arr[j + 1] = kunci
    waktu_ms = (time.perf_counter() - mulai) * 1000
    return arr, perbandingan, waktu_ms

# KONSTANTA
_TIPE   = ["Serum", "Moisturizer", "Toner", "Cleanser", "Sunscreen", "Mask", "Eye Cream", "Ampoule"]
_BAHAN  = ["Vitamin C", "Retinol", "Niacinamide", "Hyaluronic Acid", "Peptide", "AHA BHA", "Bakuchiol", "Centella"]
_UKURAN = {
    "Serum"     : "30ml",
    "Moisturizer": "50ml",
    "Toner"     : "150ml",
    "Cleanser"  : "100ml",
    "Sunscreen" : "50ml",
    "Mask"      : "75ml",
    "Eye Cream" : "15ml",
    "Ampoule"   : "30ml",
}

DAFTAR_BARANG = [
    f"{tipe} {bahan} {_UKURAN[tipe]}"
    for tipe  in _TIPE
    for bahan in _BAHAN
]

FILTER_KOLOM = {
    "🔎 Semua Kolom" : None,
    "🆔 ID"          : ["ID"],
    "📦 Nama Barang" : ["Nama Barang"],
    "🏷️ Kategori"    : ["Kategori"],
    "🏭 Gudang"      : ["Gudang"],
    "📚 Rak"         : ["Rak"],
    "📌 Shelf"       : ["Shelf"],
}

KOLOM_SORTIR = ["ID", "Nama Barang", "Kategori", "Gudang", "Rak", "Shelf", "Stok"]

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

# CSS
def apply_styles():
    st.markdown("""
    <style>
        .main {
            background: linear-gradient(180deg, #faf8f7, #f3efec) !important;
        }

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

        .setting-card {
            background: #111827;
            padding: 20px;
            border-radius: 12px;
            border-top: 4px solid #8b4513;
            margin-bottom: 15px;
        }
        .setting-card h3 { margin: 0 0 8px; color: #f8fafc; }
        .setting-card p  { margin: 0; color: #cbd5e1; font-size: 0.9rem; }

        .sigudang-footer {
            margin-top: 60px;
            padding: 20px 0 8px;
            border-top: 1px solid #d6ccc7;
            text-align: center;
        }
        .sigudang-footer .footer-brand {
            font-size: 0.85rem;
            font-weight: 700;
            color: #7a3728;
            letter-spacing: 0.05em;
        }
        .sigudang-footer .footer-sub {
            font-size: 0.75rem;
            color: #a08070;
            margin-top: 3px;
            letter-spacing: 0.02em;
        }
    </style>
    """, unsafe_allow_html=True)

# HELPER: DATA
@st.cache_data
def buat_data_dummy(jumlah: int) -> list[dict]:
    return [
        {
            "ID"         : str(i + 1).zfill(4),
            "Nama Barang": random.choice(DAFTAR_BARANG),
            "Kategori"   : random.choice(["Bahan Baku", "Packaging", "Produk Jadi"]),
            "Gudang"     : random.choice(["A", "B", "C", "D"]),
            "Rak"        : random.choice(["1", "2", "3", "4", "5", "6"]),
            "Shelf"      : random.choice(["A1", "A2", "B1", "B2", "C1", "C2", "D1", "D2"]),
            "Stok"       : random.randint(5, 999),
        }
        for i in range(jumlah)
    ]


def ensure_id(data: list[dict]) -> list[dict]:
    return [
        {**b, "ID": str(b["ID"]).strip() if str(b.get("ID", "")).strip() else str(i + 1).zfill(4)}
        for i, b in enumerate(data)
    ]


def next_id(data: list[dict]) -> str:
    angka = [int(str(b.get("ID", 0))) for b in data if str(b.get("ID", "")).isdigit()]
    return str((max(angka) + 1) if angka else len(data) + 1).zfill(4)


def list_ke_df(data: list[dict]) -> pd.DataFrame:
    if not data:
        return pd.DataFrame(columns=["ID", "Nama Barang", "Kategori", "Gudang", "Rak", "Shelf", "Stok"])
    df = pd.DataFrame(data)
    if "Stok" in df.columns:
        df["Stok"] = pd.to_numeric(df["Stok"], errors="coerce").fillna(0).astype(int)
    return df


def csv_ke_list(file) -> list[dict]:
    df = pd.read_csv(file)
    if "Stok" in df.columns:
        df["Stok"] = pd.to_numeric(df["Stok"], errors="coerce").fillna(0).astype(int)
    return df.to_dict("records")

# SESSION STATE
def init_session():
    defaults = {
        "data"       : None,
        "data_source": None,
        "sort_col"   : "ID",
        "sort_asc"   : True,
        "halaman"    : "Data Barang",
    }
    for k, v in defaults.items():
        st.session_state.setdefault(k, v)

# SIDEBAR
def tampilkan_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style='font-size:2.8rem; line-height:1;'>🏭</div>
        <h1 style='margin:6px 0 2px; font-size:1.9rem; font-weight:800;'>SIGUDANG</h1>
        <p style='margin-top:0; opacity:0.6; font-size:1rem;'>Sistem Informasi Gudang Skincare</p>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        for ikon, nama in NAV_MENU:
            if st.button(f"{ikon}  {nama}", key=f"nav_{nama}", width="stretch"):
                st.session_state.halaman = nama
                st.rerun()

        st.markdown("<hr style='opacity:0.3;'>", unsafe_allow_html=True)

        data = st.session_state.data
        if st.session_state.halaman != "Data Barang" or data is None:
            return

        src   = str(st.session_state.data_source)
        label = f"Data Dummy ({len(data)} item)" if src.startswith("dummy") else src
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.06); border:1px solid rgba(148,163,184,0.25);
             border-radius:8px; padding:10px 14px;">
            <div style="color:#818cf8; font-size:0.7rem; font-weight:600;">DATA AKTIF</div>
            <div style="color:#f8fafc; font-size:0.85rem; margin-top:4px;">📋 {label}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr style='opacity:0.3;'>", unsafe_allow_html=True)
        st.markdown("<div style='color:#cbd5e1; font-size:0.75rem; font-weight:600;'>OPSI SORTIR</div>",
                    unsafe_allow_html=True)

        cols_tersedia = [c for c in KOLOM_SORTIR if data and c in data[0]]
        idx = cols_tersedia.index(st.session_state.sort_col) \
              if st.session_state.sort_col in cols_tersedia else 0

        st.session_state.sort_col = st.selectbox("Kolom", cols_tersedia, index=idx)
        st.session_state.sort_asc = "⬆️" in st.radio(
            "Arah", ["⬆️ Kecil → Besar", "⬇️ Besar → Kecil"])

# HALAMAN: DATA BARANG
def halaman_data_barang():
    data = st.session_state.data

    n_gudang   = len({b["Gudang"]   for b in data}) if data else 0
    n_kategori = len({b["Kategori"] for b in data}) if data else 0

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

    if data is None:
        st.markdown("""
        <div style="background:#111827; border-radius:12px; padding:50px; text-align:center;
             border:1px solid #334155;">
            <div style="font-size:4rem;">📦</div>
            <h3 style="color:#f8fafc; margin:10px 0;">Belum Ada Data</h3>
            <p style="color:#cbd5e1;">Buka halaman <b>⚙️ Pengaturan</b> untuk membuat data
            dummy atau upload file CSV.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    c1, c2 = st.columns([5, 3])
    kata_kunci  = c1.text_input("Cari", placeholder="🔍 Ketik nama barang, kategori, lokasi...",
                                label_visibility="collapsed")
    filter_key  = c2.selectbox("Filter", list(FILTER_KOLOM.keys()), label_visibility="collapsed")
    kolom_aktif = FILTER_KOLOM[filter_key] or list(data[0].keys())

    if kata_kunci.strip():
        hasil_list, _, _ = linear_search(data, kata_kunci, kolom_aktif)
    else:
        hasil_list = data.copy()

    sc = st.session_state.sort_col
    sa = st.session_state.sort_asc
    if hasil_list and sc in hasil_list[0]:
        hasil_sorted, _, _ = insertion_sort(hasil_list, sc, sa)
    else:
        hasil_sorted = hasil_list

    st.markdown(f"""
    <div class="metric-card">
        <div class="label">TOTAL ITEM DITAMPILKAN</div>
        <div class="value">{len(hasil_sorted):,}</div>
        <div class="sub">dari {len(data):,} barang terdaftar</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([5, 2, 1])
    c1.markdown(
        f'Hasil: **"{kata_kunci}"** — **{len(hasil_sorted)}** ditemukan'
        if kata_kunci.strip()
        else f'Menampilkan **{len(hasil_sorted)}** item.'
    )
    c2.markdown(
        f'<div style="text-align:right; color:#cbd5e1;">{"⬆️" if sa else "⬇️"} <b>{sc}</b></div>',
        unsafe_allow_html=True)

    if hasil_sorted:
        c3.download_button(
            "⬇️ CSV",
            data=list_ke_df(hasil_sorted).to_csv(index=False).encode("utf-8"),
            file_name="data_gudang.csv",
            mime="text/csv",
            width="stretch",
        )

    if not hasil_sorted:
        st.markdown("""
        <div style="text-align:center; padding:40px; background:#111827; border-radius:12px;">
            <div style="font-size:2.5rem;">🔍</div>
            <h4 style="color:#cbd5e1;">Data Tidak Ditemukan</h4>
            <p style="color:#94a3b8; font-size:0.85rem;">Coba periksa kembali ejaan kata kunci.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    df_tampil = list_ke_df(hasil_sorted)

    def sorot_baris(row):
        if not kata_kunci.strip():
            return [""] * len(row)
        kw = kata_kunci.strip().lower()
        cocok = any(kw in str(row[c]).lower() for c in kolom_aktif if c in row.index)
        return ["background-color:#1e293b; color:#c7d2fe;"] * len(row) if cocok else [""] * len(row)

    tabel = (
        df_tampil.style.apply(sorot_baris, axis=1).format({"Stok": "{:,}"})
        if kata_kunci.strip() and len(df_tampil) <= 800
        else df_tampil
    )

    st.dataframe(
        tabel,
        width="stretch",
        height=min(550, max(200, len(df_tampil) * 38 + 60)),
        column_config=KOLOM_CONFIG,
        hide_index=True,
    )

# HALAMAN: KELOLA DATA
def _nilai_unik_terurut(col: str) -> list[str]:
    data = st.session_state.data
    if not data or col not in data[0]:
        return []
    seen, hasil = set(), []
    for b in data:
        v = str(b.get(col, ""))
        if v not in seen:
            seen.add(v)
            hasil.append(v)
    for i in range(1, len(hasil)):
        kunci = hasil[i]
        j = i - 1
        while j >= 0 and hasil[j].lower() > kunci.lower():
            hasil[j + 1] = hasil[j]
            j -= 1
        hasil[j + 1] = kunci
    return hasil


def _selectbox_atau_input(label: str, col: str, default, prefix: str) -> str:
    opts = _nilai_unik_terurut(col)
    cur  = str(default)
    key  = f"{prefix}_{col.lower().replace(' ', '_')}"
    if opts:
        if cur not in opts:
            opts = [cur] + opts
        return st.selectbox(label, opts, index=opts.index(cur), key=key)
    return st.text_input(label, value=cur, key=key)


def _form_fields(prefix: str, defaults: dict) -> dict:
    nama     = st.text_input(
        "Nama Barang",
        value="" if prefix == "tambah" else defaults.get("Nama Barang", ""),
        key=f"{prefix}_nama",
    )
    kategori = _selectbox_atau_input("Kategori", "Kategori", defaults.get("Kategori", "Produk Jadi"), prefix)
    gudang   = _selectbox_atau_input("Gudang",   "Gudang",   defaults.get("Gudang",   "A"),           prefix)
    rak      = _selectbox_atau_input("Rak",       "Rak",      defaults.get("Rak",      "1"),           prefix)
    shelf    = _selectbox_atau_input("Shelf",     "Shelf",    defaults.get("Shelf",    "A1"),          prefix)
    stok     = st.number_input("Stok", min_value=0, value=int(defaults.get("Stok", 0)),
                               step=1, key=f"{prefix}_stok")
    return {"Nama Barang": nama, "Kategori": kategori, "Gudang": gudang,
            "Rak": rak, "Shelf": shelf, "Stok": stok}


def halaman_kelola_data():
    st.markdown("""
    <div style="background:#111827; padding:15px 20px; border-radius:12px;
         margin-bottom:20px; border-left:6px solid #8b4513;">
        <h2 style="margin:0; color:#f8fafc;">🛠️ Kelola Data</h2>
        <p style="margin:5px 0 0; color:#cbd5e1; font-size:0.9rem;">
        Tambah, edit, atau hapus item inventaris.</p>
    </div>
    """, unsafe_allow_html=True)

    data = st.session_state.data
    if data is None:
        st.info("Belum ada data aktif. Buka halaman Pengaturan untuk membuat atau upload data.")
        return

    ids       = [str(b["ID"]) for b in data]
    label_map = {b["ID"]: f"{b['ID']} — {b.get('Nama Barang', '(tanpa nama)')}" for b in data}

    col_tambah, col_edit, col_hapus = st.columns(3)

    with col_tambah:
        with st.form("form_tambah"):
            st.subheader("Tambah Data Baru")
            vals   = _form_fields("tambah", {})
            submit = st.form_submit_button("Tambah Data")

        if submit:
            if not vals["Nama Barang"].strip():
                st.warning("Nama Barang tidak boleh kosong.")
            else:
                baru = {
                    "ID": next_id(data),
                    **{k: (int(v) if k == "Stok" else str(v).strip()) for k, v in vals.items()},
                }
                st.session_state.data = data + [baru]
                st.success(f"✅ Barang **{baru['Nama Barang']}** (ID {baru['ID']}) berhasil ditambahkan.")

    with col_edit:
        if not ids:
            st.info("Tidak ada data untuk diedit.")
        else:
            st.subheader("Edit Data")
            edit_id = st.selectbox("Pilih ID", ids, key="edit_id_select")

            hasil_cari, _, _ = linear_search(data, edit_id, ["ID"])
            baris_list = [b for b in hasil_cari if str(b["ID"]) == str(edit_id)]

            if not baris_list:
                st.warning("ID tidak ditemukan.")
            else:
                old = baris_list[0]
                eid = str(edit_id).replace(" ", "_")

                with st.form(f"form_edit_{eid}"):
                    nama     = st.text_input("Nama Barang", value=str(old.get("Nama Barang", "")),
                                             key=f"edit_nama_{eid}")
                    kategori = _selectbox_atau_input("Kategori", "Kategori", old.get("Kategori", ""), f"edit_{eid}")
                    gudang   = _selectbox_atau_input("Gudang",   "Gudang",   old.get("Gudang",   ""), f"edit_{eid}")
                    rak      = _selectbox_atau_input("Rak",      "Rak",      old.get("Rak",      ""), f"edit_{eid}")
                    shelf    = _selectbox_atau_input("Shelf",    "Shelf",    old.get("Shelf",    ""), f"edit_{eid}")
                    stok     = st.number_input("Stok", min_value=0, value=int(old.get("Stok", 0)),
                                               step=1, key=f"edit_stok_{eid}")
                    simpan   = st.form_submit_button("Simpan Perubahan")

                if simpan:
                    if not nama.strip():
                        st.warning("Nama Barang tidak boleh kosong.")
                    else:
                        new_vals = {
                            "Nama Barang": nama.strip(),
                            "Kategori"   : str(kategori).strip(),
                            "Gudang"     : str(gudang).strip(),
                            "Rak"        : str(rak).strip(),
                            "Shelf"      : str(shelf).strip(),
                            "Stok"       : int(st.session_state[f"edit_stok_{eid}"]),
                        }
                        data_baru, changed = [], []
                        for b in data:
                            if str(b["ID"]) == str(edit_id):
                                changed = [
                                    f"**{k}**: `{b.get(k)}` → `{v}`"
                                    for k, v in new_vals.items()
                                    if str(b.get(k, "")) != str(v)
                                ]
                                data_baru.append({**b, **new_vals})
                            else:
                                data_baru.append(b)
                        st.session_state.data = data_baru
                        if changed:
                            st.success("✅ Data diperbarui:\n" + "\n".join(f"- {c}" for c in changed))
                        else:
                            st.info("ℹ️ Tidak ada perubahan.")

    with col_hapus:
        st.subheader("Hapus Data")
        label_list  = list(label_map.values())
        label_to_id = {v: k for k, v in label_map.items()}

        hapus_labels = st.multiselect(
            "Pilih Barang yang akan Dihapus",
            options=label_list,
            key="hapus_labels_select",
            placeholder="Cari ID atau nama barang...",
        )
        hapus_ids = [label_to_id[lbl] for lbl in hapus_labels if lbl in label_to_id]

        if hapus_ids:
            preview = [b for b in data if b["ID"] in hapus_ids]
            st.markdown(
                f"<div style='background:#2d1a1a; border:1px solid #7f1d1d; border-radius:8px;"
                f"padding:10px 14px; margin:8px 0;'>"
                f"<span style='color:#fca5a5; font-size:0.8rem; font-weight:600;'>"
                f"⚠️ {len(hapus_ids)} item akan dihapus:</span></div>",
                unsafe_allow_html=True,
            )
            st.dataframe(
                list_ke_df(preview),
                hide_index=True,
                width="stretch",
                column_config={
                    "ID"         : st.column_config.TextColumn("ID", width=55),
                    "Nama Barang": st.column_config.TextColumn("Nama Barang", width=150),
                    "Stok"       : st.column_config.NumberColumn("Stok", format="%d pcs"),
                },
            )

        if st.button(
            "🗑️ Hapus Item Terpilih",
            key="btn_hapus",
            type="primary" if hapus_ids else "secondary",
            disabled=not hapus_ids,
        ):
            nama_dihapus = [b["Nama Barang"] for b in data if b["ID"] in hapus_ids]
            st.session_state.data = [b for b in data if b["ID"] not in hapus_ids]
            st.success(
                f"✅ {len(hapus_ids)} item dihapus:\n" +
                "\n".join(f"- {n}" for n in nama_dihapus)
            )

# HALAMAN: PENGATURAN
def halaman_pengaturan():
    st.markdown("""
    <div style="background:#111827; padding:15px 20px; border-radius:12px;
         margin-bottom:20px; border-left:6px solid #8b4513;">
        <h2 style="margin:0; color:#f8fafc;">⚙️ Pengaturan</h2>
        <p style="margin:5px 0 0; color:#cbd5e1; font-size:0.9rem;">
        Konfigurasi sumber data gudang</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="setting-card"><h3>📋 Buat Data Dummy</h3>'
                '<p>Generate data inventaris acak untuk simulasi.</p></div>',
                unsafe_allow_html=True)

    c1, c2 = st.columns([3, 1])
    jumlah = c1.slider("Jumlah baris data", 50, 1000, 200, step=50)
    c1.caption(f"Akan dibuat **{jumlah}** baris data acak.")
    c2.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

    if c2.button("🔄 Generate Data", type="primary", width="stretch"):
        st.cache_data.clear()
        st.session_state.update(
            data=buat_data_dummy(jumlah),
            data_source=f"dummy_{jumlah}",
            sort_col="ID", sort_asc=True,
            halaman="Data Barang",
        )
        st.toast("Data berhasil dibuat!", icon="✅")
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<div class="setting-card"><h3>📂 Upload File CSV</h3>'
                '<p>Gunakan data gudang nyata dari file .CSV milik Anda.</p></div>',
                unsafe_allow_html=True)

    c1, c2 = st.columns([2, 1])
    with c1:
        file = st.file_uploader("Upload file CSV", type=["csv"], label_visibility="collapsed")
        if file:
            try:
                with st.spinner("Memproses CSV..."):
                    raw = ensure_id(csv_ke_list(file))
                    st.session_state.update(
                        data=raw,
                        data_source=file.name,
                        sort_col="ID", sort_asc=True,
                        halaman="Data Barang",
                    )
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

    st.markdown('<div class="setting-card"><h3>📊 Status Data Saat Ini</h3></div>',
                unsafe_allow_html=True)
    data = st.session_state.data
    if data is None:
        st.info("Belum ada data aktif. Silakan generate dummy atau upload CSV terlebih dahulu.")
        return

    src  = str(st.session_state.data_source)
    tipe = "Data Dummy" if src.startswith("dummy") else f"File: {src}"
    total_stok = sum(int(b.get("Stok", 0)) for b in data)

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Sumber Data",  tipe[:20])
    k2.metric("Jumlah Baris", f"{len(data):,}")
    k3.metric("Jumlah Kolom", len(data[0]) if data else 0)
    k4.metric("Total Stok",   f"{total_stok:,}")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑️ Hapus Data", type="secondary", width="stretch"):
        st.session_state.update(data=None, data_source=None)
        st.toast("Data dihapus!", icon="🗑️")
        st.rerun()

# HALAMAN: TENTANG SISTEM
def halaman_tentang():
    st.markdown("""
    <div style="background:#111827; border-radius:14px; padding:28px 32px;
         border:1px solid #1f2937; margin-bottom:16px;">
        <h2 style="color:#f8fafc; margin-top:0;">📘 Tentang Sistem</h2>
        <p style="color:#94a3b8; margin:0;">Penjelasan algoritma yang digunakan di dalam SIGUDANG.</p>
    </div>
    """, unsafe_allow_html=True)

    sections = [
        ("🔍 Linear Search — Algoritma Pencarian", [
            "<b>Sumber materi:</b> Pertemuan 10 — Algoritma Searching Python.",
            "Mengecek setiap elemen data <b>satu per satu</b> dari indeks 0 hingga akhir secara berurutan.",
            "Cocok untuk data gudang karena pencarian dilakukan secara <b>partial match (substring)</b> "
            "pada teks nama barang, kategori, atau lokasi — tidak bisa menggunakan Binary Search.",
            "<b>Kompleksitas waktu:</b> O(n) — best case O(1) jika ditemukan di indeks pertama, "
            "worst case O(n) jika tidak ditemukan.",
            "Tidak memerlukan data dalam kondisi terurut terlebih dahulu.",
        ]),
        ("📊 Insertion Sort — Algoritma Pengurutan", [
            "<b>Sumber materi:</b> Pertemuan 9 — Sorting (Algoritma dan Struktur Data).",
            "Bekerja dengan <b>menyisipkan elemen</b> satu per satu ke posisi yang tepat "
            "pada bagian array yang sudah terurut.",
            "Proses dimulai dari indeks ke-2, dengan asumsi elemen ke-1 sudah 'terurut'. "
            "Setiap elemen baru dibandingkan mundur hingga menemukan posisi sisipnya.",
            "<b>Kompleksitas waktu:</b> O(n²) worst case, O(n) best case (data sudah terurut). "
            "Dipilih karena data gudang berskala kecil-menengah.",
            "Bersifat <b>stabil</b>: item dengan nilai kolom yang sama tetap mempertahankan "
            "urutan relatifnya — penting untuk konsistensi tampilan.",
        ]),
        ("🗂️ Struktur Data yang Digunakan", [
            "Data inventaris disimpan sebagai <b>List of Dictionary</b> Python — "
            "setara dengan array of records.",
            "Setiap elemen list adalah satu baris barang dengan key: "
            "ID, Nama Barang, Kategori, Gudang, Rak, Shelf, Stok.",
            "Akses ke seluruh data untuk searching maupun sorting dilakukan langsung "
            "pada struktur ini tanpa menggunakan database eksternal.",
        ]),
        ("⚙️ Teknologi", [
            "Ditulis menggunakan <b>Python</b> dengan framework <b>Streamlit</b>.",
            "Algoritma Searching dan Sorting ditulis <b>manual dari awal</b> "
            "(tidak menggunakan built-in <code>sort()</code>, <code>sorted()</code>, "
            "atau <code>str.contains()</code>).",
            "Pandas hanya digunakan untuk konversi ke DataFrame saat render tabel dan baca/tulis CSV.",
        ]),
    ]

    for judul, poin in sections:
        isi = "".join(
            f'<li style="color:#cbd5e1; margin-bottom:8px; line-height:1.6;">{p}</li>'
            for p in poin
        )
        st.markdown(f"""
        <div style="background:#1f2937; border-radius:10px; padding:20px 24px;
             margin-bottom:12px; border-left:4px solid #8b4513;">
            <h3 style="color:#f8fafc; margin:0 0 12px;">{judul}</h3>
            <ul style="margin:0; padding-left:20px;">{isi}</ul>
        </div>
        """, unsafe_allow_html=True)

# FOOTER
def tampilkan_footer():
    st.markdown("""
    <div class="sigudang-footer">
        <div class="footer-brand">SIGUDANG v1.0</div>
        <div class="footer-sub">Algoritma dan Struktur Data &nbsp;·&nbsp; Universitas Yudharta Pasuruan</div>
    </div>
    """, unsafe_allow_html=True)

# ENTRY POINT
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
    tampilkan_footer()

if __name__ == "__main__" or True:
    main()