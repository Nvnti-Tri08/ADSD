import time
import random
import pandas as pd
import streamlit as st

st.set_page_config(page_title="SIGUDANG", layout="wide", initial_sidebar_state="expanded")

# KONSTANTA
TIPE   = ["Serum", "Moisturizer", "Toner", "Cleanser", "Sunscreen", "Mask", "Eye Cream", "Ampoule"]
BAHAN  = ["Vitamin C", "Retinol", "Niacinamide", "Hyaluronic Acid", "Peptide", "AHA BHA", "Bakuchiol", "Centella"]
UKURAN = {
    "Serum": "30ml", "Moisturizer": "50ml", "Toner": "150ml", "Cleanser": "100ml",
    "Sunscreen": "50ml", "Mask": "75ml", "Eye Cream": "15ml", "Ampoule": "30ml",
}

DAFTAR_PRODUK = [f"{t} {b} {UKURAN[t]}" for t in TIPE for b in BAHAN]

KOLOM_WAJIB = ["ID", "Nama Barang", "Kategori", "Gudang", "Rak", "Shelf", "Stok"]

# Daftar nama alternatif untuk setiap kolom standar (untuk auto-detect CSV)
SINONIM_KOLOM = {
    "ID"         : ["id", "kode", "no", "nomor", "code", "item_id"],
    "Nama Barang": ["nama barang", "nama_barang", "produk", "product", "item", "barang", "name"],
    "Kategori"   : ["kategori", "category", "jenis", "tipe", "type"],
    "Gudang"     : ["gudang", "warehouse", "gedung", "wh", "depo"],
    "Rak"        : ["rak", "rack", "baris", "row", "aisle"],
    "Shelf"      : ["shelf", "posisi", "slot", "bin", "level", "laci"],
    "Stok"       : ["stok", "stock", "qty", "quantity", "jumlah", "sisa"],
}

# Pilihan filter kolom pencarian
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

MENU = [("📦", "Data Barang"), ("🛠️", "Kelola Data"), ("⚙️", "Pengaturan"), ("ℹ️", "Tentang Sistem")]


def linear_search(data, kata_kunci, kolom_cari):
    mulai    = time.perf_counter()
    kw       = kata_kunci.strip().lower()
    hasil    = []

    for barang in data:
        for kolom in kolom_cari:
            if kw in str(barang.get(kolom, "")).lower():
                hasil.append(barang)
                break  # hindari duplikat jika cocok di lebih dari satu kolom

    waktu_ms = (time.perf_counter() - mulai) * 1000
    return hasil, len(data), waktu_ms


def ambil_nilai(barang, kolom):
    """Kembalikan nilai kolom sebagai angka (jika bisa) atau string huruf kecil."""
    nilai = barang.get(kolom, "")
    if isinstance(nilai, (int, float)):
        return nilai
    try:
        return float(nilai)
    except ValueError:
        return str(nilai).lower()


def insertion_sort(data, kolom, urutan_naik=True):
    mulai        = time.perf_counter()
    arr          = [b.copy() for b in data]
    perbandingan = 0

    for i in range(1, len(arr)):
        elemen = arr[i]
        nilai  = ambil_nilai(elemen, kolom)
        j      = i - 1

        while j >= 0:
            perbandingan += 1
            nilai_j       = ambil_nilai(arr[j], kolom)
            harus_geser   = (nilai_j > nilai) if urutan_naik else (nilai_j < nilai)

            if harus_geser:
                arr[j + 1] = arr[j]
                j -= 1
            else:
                break

        arr[j + 1] = elemen

    waktu_ms = (time.perf_counter() - mulai) * 1000
    return arr, perbandingan, waktu_ms

# FUNGSI BANTU DATA
@st.cache_data
def buat_data_dummy(jumlah):
    """Generate data inventaris acak sejumlah `jumlah` baris."""
    return [
        {
            "ID"         : str(i + 1).zfill(4),
            "Nama Barang": random.choice(DAFTAR_PRODUK),
            "Kategori"   : random.choice(["Bahan Baku", "Packaging", "Produk Jadi"]),
            "Gudang"     : random.choice(["A", "B", "C", "D"]),
            "Rak"        : random.choice(["1", "2", "3", "4", "5", "6"]),
            "Shelf"      : random.choice(["A1", "A2", "B1", "B2", "C1", "C2", "D1", "D2"]),
            "Stok"       : random.randint(5, 999),
        }
        for i in range(jumlah)
    ]


def buat_id_baru(data):
    """Buat ID baru berdasarkan ID terbesar yang sudah ada."""
    angka = [int(str(b.get("ID", 0))) for b in data if str(b.get("ID", "")).isdigit()]
    return str((max(angka) + 1) if angka else len(data) + 1).zfill(4)


def pastikan_id_ada(data):
    """Pastikan setiap baris punya ID; isi otomatis jika kosong."""
    return [
        {**b, "ID": str(b.get("ID", "")).strip() or str(i + 1).zfill(4)}
        for i, b in enumerate(data)
    ]


def list_ke_df(data):
    """Ubah list of dict menjadi DataFrame dengan kolom Stok bertipe int."""
    if not data:
        return pd.DataFrame(columns=KOLOM_WAJIB)
    df = pd.DataFrame(data)
    if "Stok" in df.columns:
        df["Stok"] = pd.to_numeric(df["Stok"], errors="coerce").fillna(0).astype(int)
    return df


def csv_ke_list(file):
    """Baca file CSV dan kembalikan sebagai list of dict."""
    df = pd.read_csv(file)
    if "Stok" in df.columns:
        df["Stok"] = pd.to_numeric(df["Stok"], errors="coerce").fillna(0).astype(int)
    return df.to_dict("records")

# FUNGSI BANTU MAPPING KOLOM CSV
def deteksi_kolom(kolom_csv):
    """
    Cocokkan nama kolom dari CSV dengan kolom standar SIGUDANG
    menggunakan daftar sinonim.
    """
    index = {k.lower().strip(): k for k in kolom_csv}
    return {
        std: next((index[s] for s in syns if s in index), None)
        for std, syns in SINONIM_KOLOM.items()
    }


def terapkan_mapping(data, mapping):
    """Ubah nama kolom CSV menjadi nama kolom standar SIGUDANG."""
    kolom_dimapping = set(mapping.values())
    return [
        {
            **{std: b.get(asal, "") for std, asal in mapping.items()},
            **{k: v for k, v in b.items() if k not in kolom_dimapping},
        }
        for b in data
    ]


def nilai_unik_terurut(kolom):
    """
    Ambil nilai unik dari sebuah kolom, lalu urutkan A-Z secara manual
    menggunakan insertion sort (tanpa sorted()).
    """
    data = st.session_state.data
    if not data or kolom not in data[0]:
        return []

    seen, hasil = set(), []
    for b in data:
        v = str(b.get(kolom, ""))
        if v not in seen:
            seen.add(v)
            hasil.append(v)

    # Insertion sort A-Z
    for i in range(1, len(hasil)):
        k = hasil[i]
        j = i - 1
        while j >= 0 and hasil[j].lower() > k.lower():
            hasil[j + 1] = hasil[j]
            j -= 1
        hasil[j + 1] = k

    return hasil

# CSS
def terapkan_css():
    st.markdown("""
    <style>
    .main { background: linear-gradient(180deg, #faf8f7, #f3efec) !important; }

    [data-testid="stSidebar"] { background-color: #4b1f15; color: #f5e8df; }
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] p  { color: #fde8dd !important; }
    [data-testid="stSidebar"] button {
        background-color: rgba(123, 63, 30, .18);
        color: #f3e4dc;
        border: 1px solid rgba(255, 255, 255, .14);
        border-radius: 8px;
        padding: 10px 14px;
    }
    [data-testid="stSidebar"] button:hover { background-color: #fff; color: #000; }

    .page-header {
        display: flex; justify-content: space-between; align-items: center;
        background: linear-gradient(135deg, #4a1f18, #7a3728);
        padding: 20px; border-radius: 12px;
        border-left: 6px solid #8b4513; margin-bottom: 25px;
    }
    .page-header h1 { margin: 0; color: #f8fafc; font-size: 2rem; }
    .page-header p  { margin: 5px 0 0; color: #d1fae5; }

    .badge-box {
        background: #1f2937; padding: 8px 16px; border-radius: 8px;
        text-align: center; min-width: 90px; border: 1px solid #374151;
    }
    .badge-angka { font-size: 1.4rem; font-weight: bold; color: #c7d2fe; }
    .badge-label { font-size: .75rem; color: #cbd5e1; }

    .metric-card {
        padding: 20px; border-radius: 12px; color: white; margin-bottom: 15px;
        background: linear-gradient(135deg, #6b2d1d, #b76f52);
    }
    .metric-card .label { font-size: .85rem; font-weight: 600; opacity: .9; }
    .metric-card .value { font-size: 2rem; font-weight: 800; margin: 8px 0; }
    .metric-card .sub   { font-size: .8rem; opacity: .85; font-style: italic; }

    .setting-card {
        background: #111827; padding: 20px; border-radius: 12px;
        border-top: 4px solid #8b4513; margin-bottom: 15px;
    }
    .setting-card h3 { margin: 0 0 8px; color: #f8fafc; }
    .setting-card p  { margin: 0; color: #cbd5e1; font-size: .9rem; }

    .sigudang-footer {
        margin-top: 60px; padding: 20px 0 8px;
        border-top: 1px solid #d6ccc7; text-align: center;
    }
    .footer-brand { font-size: .85rem; font-weight: 700; color: #7a3728; letter-spacing: .05em; }
    .footer-sub   { font-size: .75rem; color: #a08070; margin-top: 3px; letter-spacing: .02em; }
    </style>
    """, unsafe_allow_html=True)

# SESSION STATE
def init_session():
    """Siapkan nilai default session_state agar tidak hilang saat rerun."""
    defaults = {
        "data"       : None,
        "data_source": None,
        "sort_col"   : "ID",
        "sort_asc"   : True,
        "halaman"    : "Data Barang",
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)

# SIDEBAR
def tampilkan_sidebar():
    with st.sidebar:
        st.markdown("""
            <div style='font-size:2.8rem'>🏭</div>
            <h1 style='margin:6px 0 2px; font-size:1.9rem; font-weight:800'>SIGUDANG</h1>
            <p style='margin-top:0; opacity:.6'>Sistem Informasi Gudang Skincare</p>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        for ikon, nama in MENU:
            if st.button(f"{ikon}  {nama}", key=f"nav_{nama}", width="stretch"):
                st.session_state.halaman = nama
                st.rerun()

        st.markdown("<hr style='opacity:.3'>", unsafe_allow_html=True)

        data = st.session_state.data
        if st.session_state.halaman != "Data Barang" or data is None:
            return

        # Tampilkan info data aktif
        sumber = str(st.session_state.data_source)
        label  = f"Data Dummy ({len(data)} item)" if sumber.startswith("dummy") else sumber
        st.markdown(f"""
            <div style="background:rgba(255,255,255,.06); border:1px solid rgba(148,163,184,.25);
                border-radius:8px; padding:10px 14px">
                <div style="color:#818cf8; font-size:.7rem; font-weight:600">DATA AKTIF</div>
                <div style="color:#f8fafc; font-size:.85rem; margin-top:4px">📋 {label}</div>
            </div>
        """, unsafe_allow_html=True)

        # Opsi sortir
        st.markdown("<hr style='opacity:.3'>", unsafe_allow_html=True)
        st.markdown("<div style='color:#cbd5e1; font-size:.75rem; font-weight:600'>OPSI SORTIR</div>", unsafe_allow_html=True)

        kolom_ada = [k for k in KOLOM_SORTIR if data and k in data[0]]
        idx = kolom_ada.index(st.session_state.sort_col) if st.session_state.sort_col in kolom_ada else 0
        st.session_state.sort_col = st.selectbox("Kolom", kolom_ada, index=idx)
        st.session_state.sort_asc = "⬆️" in st.radio("Arah", ["⬆️ Kecil → Besar", "⬇️ Besar → Kecil"])

# HALAMAN: DATA BARANG
def halaman_data_barang():
    data = st.session_state.data

    n_gudang   = len({b.get("Gudang", "")   for b in data} - {""}) if data else 0
    n_kategori = len({b.get("Kategori", "") for b in data} - {""}) if data else 0

    st.markdown(f"""
        <div class="page-header">
            <div>
                <h1>📦 Data Barang</h1>
                <p>SIGUDANG — Manajemen Inventaris Gudang Skincare</p>
            </div>
            <div style="display:flex; gap:12px">
                <div class="badge-box">
                    <div class="badge-angka">{n_gudang}</div>
                    <div class="badge-label">Gudang</div>
                </div>
                <div class="badge-box">
                    <div class="badge-angka">{n_kategori}</div>
                    <div class="badge-label">Kategori</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if data is None:
        st.markdown("""
            <div style="background:#111827; border-radius:12px; padding:50px;
                text-align:center; border:1px solid #334155">
                <div style="font-size:4rem">📦</div>
                <h3 style="color:#f8fafc; margin:10px 0">Belum Ada Data</h3>
                <p style="color:#cbd5e1">Buka halaman <b>⚙️ Pengaturan</b> untuk membuat data dummy atau upload file CSV.</p>
            </div>
        """, unsafe_allow_html=True)
        return

    # --- Pencarian & filter ---
    c1, c2     = st.columns([5, 3])
    kata_kunci = c1.text_input("Cari", placeholder="🔍 Ketik nama barang, kategori, lokasi...", label_visibility="collapsed")
    filter_dipilih = c2.selectbox("Filter", list(FILTER_KOLOM.keys()), label_visibility="collapsed")
    kolom_cari = FILTER_KOLOM[filter_dipilih] or list(data[0].keys())

    # Jalankan Linear Search
    if kata_kunci.strip():
        hasil = linear_search(data, kata_kunci, kolom_cari)[0]
    else:
        hasil = data.copy()

    # Jalankan Insertion Sort
    sc, sa = st.session_state.sort_col, st.session_state.sort_asc
    if hasil and sc in hasil[0]:
        hasil = insertion_sort(hasil, sc, sa)[0]

    # --- Ringkasan hasil ---
    st.markdown(f"""
        <div class="metric-card">
            <div class="label">TOTAL ITEM DITAMPILKAN</div>
            <div class="value">{len(hasil):,}</div>
            <div class="sub">dari {len(data):,} barang terdaftar</div>
        </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([5, 2, 1])
    if kata_kunci.strip():
        c1.markdown(f'Hasil: **"{kata_kunci}"** — **{len(hasil)}** ditemukan')
    else:
        c1.markdown(f'Menampilkan **{len(hasil)}** item.')
    c2.markdown(f'<div style="text-align:right; color:#cbd5e1">{"⬆️" if sa else "⬇️"} <b>{sc}</b></div>', unsafe_allow_html=True)

    if hasil:
        c3.download_button(
            "⬇️ CSV",
            data=list_ke_df(hasil).to_csv(index=False).encode("utf-8"),
            file_name="data_gudang.csv",
            mime="text/csv",
            width="stretch",
        )

    if not hasil:
        st.markdown("""
            <div style="text-align:center; padding:40px; background:#111827; border-radius:12px">
                <div style="font-size:2.5rem">🔍</div>
                <h4 style="color:#cbd5e1">Data Tidak Ditemukan</h4>
                <p style="color:#94a3b8; font-size:.85rem">Coba periksa kembali ejaan kata kunci.</p>
            </div>
        """, unsafe_allow_html=True)
        return

    # --- Render tabel ---
    df = list_ke_df(hasil)

    def sorot(baris):
        if not kata_kunci.strip():
            return [""] * len(baris)
        ada = any(
            kata_kunci.strip().lower() in str(baris[k]).lower()
            for k in kolom_cari if k in baris.index
        )
        if ada:
            return ["background-color:#1e293b; color:#c7d2fe;"] * len(baris)
        return [""] * len(baris)

    tabel = df.style.apply(sorot, axis=1).format({"Stok": "{:,}"}) if kata_kunci.strip() and len(df) <= 800 else df

    st.dataframe(
        tabel,
        width="stretch",
        height=min(550, max(200, len(df) * 38 + 60)),
        column_config=KOLOM_CONFIG,
        hide_index=True,
    )

# HALAMAN: KELOLA DATA
def selectbox_atau_input(label, kolom, default, prefix):
    """
    Tampilkan selectbox jika sudah ada nilai unik di kolom tersebut,
    atau text_input jika datanya masih kosong.
    """
    opsi = nilai_unik_terurut(kolom)
    cur  = str(default)
    key  = f"{prefix}_{kolom.lower().replace(' ', '_')}"

    if opsi:
        if cur not in opsi:
            opsi = [cur] + opsi
        return st.selectbox(label, opsi, index=opsi.index(cur), key=key)
    return st.text_input(label, value=cur, key=key)


def form_barang(prefix, nilai_awal):
    """Form isian data barang — digunakan untuk tambah maupun edit."""
    nama = st.text_input(
        "Nama Barang",
        value="" if prefix == "tambah" else nilai_awal.get("Nama Barang", ""),
        key=f"{prefix}_nama",
    )
    return {
        "Nama Barang": nama,
        "Kategori"   : selectbox_atau_input("Kategori", "Kategori", nilai_awal.get("Kategori", "Produk Jadi"), prefix),
        "Gudang"     : selectbox_atau_input("Gudang",   "Gudang",   nilai_awal.get("Gudang", "A"),             prefix),
        "Rak"        : selectbox_atau_input("Rak",      "Rak",      nilai_awal.get("Rak", "1"),                prefix),
        "Shelf"      : selectbox_atau_input("Shelf",    "Shelf",    nilai_awal.get("Shelf", "A1"),             prefix),
        "Stok"       : st.number_input("Stok", min_value=0, value=int(nilai_awal.get("Stok", 0)), step=1, key=f"{prefix}_stok"),
    }


def halaman_kelola_data():
    st.markdown("""
        <div style="background:#111827; padding:15px 20px; border-radius:12px;
            margin-bottom:20px; border-left:6px solid #8b4513">
            <h2 style="margin:0; color:#f8fafc">🛠️ Kelola Data</h2>
            <p style="margin:5px 0 0; color:#cbd5e1; font-size:.9rem">Tambah, edit, atau hapus item inventaris.</p>
        </div>
    """, unsafe_allow_html=True)

    data = st.session_state.data
    if data is None:
        st.info("Belum ada data aktif. Buka halaman Pengaturan untuk membuat atau upload data.")
        return

    daftar_id = [str(b["ID"]) for b in data]
    label_map = {b["ID"]: f"{b['ID']} — {b.get('Nama Barang', '(tanpa nama)')}" for b in data}
    c_tambah, c_edit, c_hapus = st.columns(3)

    # ── TAMBAH ─────────────────────────────────────────────────────────────
    with c_tambah:
        with st.form("form_tambah"):
            st.subheader("Tambah Data Baru")
            isian  = form_barang("tambah", {})
            simpan = st.form_submit_button("Tambah Data")

        if simpan:
            if not isian["Nama Barang"].strip():
                st.warning("Nama Barang tidak boleh kosong.")
            else:
                baru = {
                    "ID": buat_id_baru(data),
                    **{k: (int(v) if k == "Stok" else str(v).strip()) for k, v in isian.items()},
                }
                st.session_state.data = data + [baru]
                st.success(f"✅ **{baru['Nama Barang']}** (ID {baru['ID']}) berhasil ditambahkan.")

    # ── EDIT ───────────────────────────────────────────────────────────────
    with c_edit:
        if not daftar_id:
            st.info("Tidak ada data untuk diedit.")
        else:
            st.subheader("Edit Data")
            id_dipilih = st.selectbox("Pilih ID", daftar_id, key="edit_id_select")

            cari, _, _ = linear_search(data, id_dipilih, ["ID"])
            baris_list = [b for b in cari if str(b["ID"]) == str(id_dipilih)]

            if not baris_list:
                st.warning("ID tidak ditemukan.")
            else:
                lama = baris_list[0]
                fk   = str(id_dipilih).replace(" ", "_")

                with st.form(f"form_edit_{fk}"):
                    nama     = st.text_input("Nama Barang", value=str(lama.get("Nama Barang", "")), key=f"edit_nama_{fk}")
                    kategori = selectbox_atau_input("Kategori", "Kategori", lama.get("Kategori", ""), f"edit_{fk}")
                    gudang   = selectbox_atau_input("Gudang",   "Gudang",   lama.get("Gudang", ""),   f"edit_{fk}")
                    rak      = selectbox_atau_input("Rak",      "Rak",      lama.get("Rak", ""),      f"edit_{fk}")
                    shelf    = selectbox_atau_input("Shelf",    "Shelf",    lama.get("Shelf", ""),    f"edit_{fk}")
                    stok     = st.number_input("Stok", min_value=0, value=int(lama.get("Stok", 0)), step=1, key=f"edit_stok_{fk}")
                    simpan   = st.form_submit_button("Simpan Perubahan")

                if simpan:
                    if not nama.strip():
                        st.warning("Nama Barang tidak boleh kosong.")
                    else:
                        nilai_baru = {
                            "Nama Barang": nama.strip(),
                            "Kategori"   : str(kategori).strip(),
                            "Gudang"     : str(gudang).strip(),
                            "Rak"        : str(rak).strip(),
                            "Shelf"      : str(shelf).strip(),
                            "Stok"       : int(st.session_state[f"edit_stok_{fk}"]),
                        }
                        data_baru  = []
                        perubahan  = []

                        for b in data:
                            if str(b["ID"]) == str(id_dipilih):
                                perubahan = [
                                    f"**{k}**: `{b.get(k)}` → `{v}`"
                                    for k, v in nilai_baru.items()
                                    if str(b.get(k, "")) != str(v)
                                ]
                                data_baru.append({**b, **nilai_baru})
                            else:
                                data_baru.append(b)

                        st.session_state.data = data_baru

                        if perubahan:
                            st.success("✅ Diperbarui:\n" + "\n".join(f"- {p}" for p in perubahan))
                        else:
                            st.info("ℹ️ Tidak ada perubahan.")

    # ── HAPUS ──────────────────────────────────────────────────────────────
    with c_hapus:
        st.subheader("Hapus Data")

        id_per_label  = {v: k for k, v in label_map.items()}
        label_dipilih = st.multiselect(
            "Pilih Barang yang akan Dihapus",
            list(label_map.values()),
            key="hapus_select",
            placeholder="Cari ID atau nama barang...",
        )
        id_hapus = [id_per_label[l] for l in label_dipilih if l in id_per_label]

        if id_hapus:
            st.markdown(f"""
                <div style='background:#2d1a1a; border:1px solid #7f1d1d; border-radius:8px; padding:10px 14px; margin:8px 0'>
                    <span style='color:#fca5a5; font-size:.8rem; font-weight:600'>⚠️ {len(id_hapus)} item akan dihapus:</span>
                </div>
            """, unsafe_allow_html=True)
            st.dataframe(
                list_ke_df([b for b in data if b["ID"] in id_hapus]),
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
            type="primary" if id_hapus else "secondary",
            disabled=not id_hapus,
        ):
            nama_hapus            = [b["Nama Barang"] for b in data if b["ID"] in id_hapus]
            st.session_state.data = [b for b in data if b["ID"] not in id_hapus]
            st.success(f"✅ {len(id_hapus)} item dihapus:\n" + "\n".join(f"- {n}" for n in nama_hapus))

# HALAMAN: PENGATURAN
def halaman_pengaturan():
    st.markdown("""
        <div style="background:#111827; padding:15px 20px; border-radius:12px;
            margin-bottom:20px; border-left:6px solid #8b4513">
            <h2 style="margin:0; color:#f8fafc">⚙️ Pengaturan</h2>
            <p style="margin:5px 0 0; color:#cbd5e1; font-size:.9rem">Konfigurasi sumber data gudang</p>
        </div>
    """, unsafe_allow_html=True)

    # --- Generate data dummy ---
    st.markdown('<div class="setting-card"><h3>📋 Buat Data Dummy</h3><p>Generate data inventaris acak untuk simulasi.</p></div>', unsafe_allow_html=True)

    c1, c2 = st.columns([3, 1])
    jumlah = c1.slider("Jumlah baris data", 50, 1000, 200, step=50)
    c1.caption(f"Akan dibuat **{jumlah}** baris data acak.")
    c2.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

    if c2.button("🔄 Generate Data", type="primary", width="stretch"):
        st.cache_data.clear()
        st.session_state.update(
            data=buat_data_dummy(jumlah),
            data_source=f"dummy_{jumlah}",
            sort_col="ID",
            sort_asc=True,
            halaman="Data Barang",
        )
        st.toast("Data berhasil dibuat!", icon="✅")
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Upload CSV ---
    st.markdown('<div class="setting-card"><h3>📂 Upload File CSV</h3><p>Gunakan data gudang nyata dari file .CSV milik Anda.</p></div>', unsafe_allow_html=True)

    c1, c2 = st.columns([2, 1])
    with c1:
        file = st.file_uploader("Upload file CSV", type=["csv"], label_visibility="collapsed")
        if file:
            try:
                data_mentah = csv_ke_list(file)

                if not data_mentah:
                    st.error("❌ File CSV kosong!")
                else:
                    kolom_csv   = list(data_mentah[0].keys())
                    mapping     = deteksi_kolom(kolom_csv)
                    kolom_gagal = [k for k, v in mapping.items() if v is None]

                    if not kolom_gagal:
                        # Semua kolom terdeteksi otomatis
                        hasil = pastikan_id_ada(terapkan_mapping(data_mentah, mapping))
                        st.session_state.update(
                            data=hasil, data_source=file.name,
                            sort_col="ID", sort_asc=True, halaman="Data Barang",
                        )
                        st.success(f"✅ **'{file.name}'** berhasil diunggah ({len(hasil):,} baris) — kolom terdeteksi otomatis!")
                        with st.expander("🔍 Lihat hasil mapping kolom"):
                            for std, asal in mapping.items():
                                st.markdown(f"- `{asal}` → **{std}**")
                        st.rerun()
                    else:
                        # Ada kolom yang tidak terdeteksi → minta mapping manual
                        st.warning(
                            f"⚠️ **{len(kolom_gagal)} kolom tidak terdeteksi:** "
                            f"`{'`, `'.join(kolom_gagal)}`\n\nSilakan pilih secara manual."
                        )

                        # Simpan state mapping sementara
                        if "tmp_raw" not in st.session_state or st.session_state.get("tmp_file") != file.name:
                            st.session_state.tmp_raw     = data_mentah
                            st.session_state.tmp_file    = file.name
                            st.session_state.tmp_mapping = mapping.copy()

                        opsi           = ["— Pilih —"] + kolom_csv
                        mapping_manual = st.session_state.tmp_mapping.copy()

                        ck, cn = st.columns(2)
                        for i, std in enumerate(KOLOM_WAJIB):
                            with (ck if i % 2 == 0 else cn):
                                det = mapping.get(std)
                                idx = opsi.index(det) if det and det in opsi else 0
                                p   = st.selectbox(
                                    f"**{std}**" + (" ✅" if det else " ❓"),
                                    opsi, index=idx, key=f"map_{std}",
                                )
                                mapping_manual[std] = p if p != "— Pilih —" else None

                        kosong = [k for k, v in mapping_manual.items() if v is None]
                        if kosong:
                            st.info(f"Belum dipilih: `{'`, `'.join(kosong)}`")

                        if st.button("✅ Terapkan & Simpan", type="primary", disabled=bool(kosong)):
                            hasil = pastikan_id_ada(terapkan_mapping(st.session_state.tmp_raw, mapping_manual))
                            st.session_state.update(
                                data=hasil, data_source=file.name,
                                sort_col="ID", sort_asc=True, halaman="Data Barang",
                            )
                            for k in ["tmp_raw", "tmp_file", "tmp_mapping"]:
                                st.session_state.pop(k, None)
                            st.success(f"✅ Data berhasil disimpan ({len(hasil):,} baris)!")
                            st.rerun()

            except Exception as e:
                st.error(f"❌ Gagal membaca file: {e}")

    with c2:
        kolom_list = "".join(f"<code>{k}</code><br>" for k in KOLOM_WAJIB)
        st.markdown(f"""
            <div style="background:#111827; border-radius:10px; padding:14px;
                font-size:.8rem; color:#cbd5e1; border:1px dashed #4b5563">
                <b>Kolom standar SIGUDANG:</b><br><br>
                {kolom_list}<br>
                <span style="color:#6b7280">Nama kolom berbeda akan dideteksi otomatis atau bisa dipetakan manual.</span>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Status data saat ini ---
    st.markdown('<div class="setting-card"><h3>📊 Status Data Saat Ini</h3></div>', unsafe_allow_html=True)

    data = st.session_state.data
    if data is None:
        st.info("Belum ada data aktif.")
        return

    sumber = str(st.session_state.data_source)
    tipe   = "Data Dummy" if sumber.startswith("dummy") else f"File: {sumber}"

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Sumber Data",   tipe[:20])
    k2.metric("Jumlah Baris",  f"{len(data):,}")
    k3.metric("Jumlah Kolom",  len(data[0]) if data else 0)
    k4.metric("Total Stok",    f"{sum(int(b.get('Stok', 0)) for b in data):,}")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑️ Hapus Data", type="secondary", width="stretch"):
        st.session_state.update({"data": None, "data_source": None})
        st.toast("Data dihapus!", icon="🗑️")
        st.rerun()

# HALAMAN: TENTANG SISTEM
def halaman_tentang():
    st.markdown("""
        <div style="background:#111827; border-radius:14px; padding:28px 32px;
            border:1px solid #1f2937; margin-bottom:16px">
            <h2 style="color:#f8fafc; margin-top:0">📘 Tentang Sistem</h2>
            <p style="color:#94a3b8; margin:0">Penjelasan algoritma yang digunakan di dalam SIGUDANG.</p>
        </div>
    """, unsafe_allow_html=True)

    konten = [
        ("🔍 Linear Search — Algoritma Pencarian", [
            "<b>Sumber materi:</b> Pertemuan 10 — Algoritma Searching Python.",
            "Mengecek setiap elemen data <b>satu per satu</b> dari indeks 0 hingga akhir secara berurutan.",
            "Cocok untuk data gudang karena pencarian dilakukan secara <b>partial match (substring)</b> — tidak bisa menggunakan Binary Search.",
            "<b>Kompleksitas waktu:</b> O(n) — best case O(1), worst case O(n).",
            "Tidak memerlukan data dalam kondisi terurut terlebih dahulu.",
        ]),
        ("📊 Insertion Sort — Algoritma Pengurutan", [
            "<b>Sumber materi:</b> Pertemuan 9 — Sorting (Algoritma dan Struktur Data).",
            "Bekerja dengan <b>menyisipkan elemen</b> satu per satu ke posisi yang tepat.",
            "Dimulai dari indeks ke-2; setiap elemen dibandingkan mundur hingga menemukan posisi sisipnya.",
            "<b>Kompleksitas waktu:</b> O(n²) worst case, O(n) best case.",
            "Bersifat <b>stabil</b>: urutan relatif elemen bernilai sama tidak berubah.",
        ]),
        ("🗂️ Struktur Data yang Digunakan", [
            "Data inventaris disimpan sebagai <b>List of Dictionary</b> Python — setara dengan array of records.",
            "Setiap elemen list adalah satu baris barang: ID, Nama Barang, Kategori, Gudang, Rak, Shelf, Stok.",
            "Akses data untuk searching dan sorting dilakukan langsung tanpa database eksternal.",
        ]),
        ("⚙️ Teknologi", [
            "Ditulis menggunakan <b>Python</b> dengan framework <b>Streamlit</b>.",
            "Algoritma ditulis <b>manual dari awal</b> — tidak menggunakan <code>sort()</code>, <code>sorted()</code>, atau <code>str.contains()</code>.",
            "Pandas hanya untuk konversi ke DataFrame saat render tabel dan baca/tulis CSV.",
        ]),
    ]

    for judul, poin_list in konten:
        isi = "".join(
            f'<li style="color:#cbd5e1; margin-bottom:8px; line-height:1.6">{p}</li>'
            for p in poin_list
        )
        st.markdown(f"""
            <div style="background:#1f2937; border-radius:10px; padding:20px 24px;
                margin-bottom:12px; border-left:4px solid #8b4513">
                <h3 style="color:#f8fafc; margin:0 0 12px">{judul}</h3>
                <ul style="margin:0; padding-left:20px">{isi}</ul>
            </div>
        """, unsafe_allow_html=True)

# FOOTER
def tampilkan_footer():
    st.markdown("""
        <div class="sigudang-footer">
            <div class="footer-brand">SIGUDANG ~ 4 $ 4</div>
            <div class="footer-sub">Algoritma dan Struktur Data &nbsp;·&nbsp; Universitas Yudharta Pasuruan</div>
        </div>
    """, unsafe_allow_html=True)

# ROUTING + ENTRY POINT
HALAMAN = {
    "Data Barang"   : halaman_data_barang,
    "Kelola Data"   : halaman_kelola_data,
    "Pengaturan"    : halaman_pengaturan,
    "Tentang Sistem": halaman_tentang,
}


def main():
    terapkan_css()                               # 1. Terapkan CSS
    init_session()                               # 2. Siapkan session_state
    tampilkan_sidebar()                          # 3. Render sidebar
    HALAMAN[st.session_state.halaman]()          # 4. Tampilkan halaman aktif
    tampilkan_footer()                           # 5. Render footer


main()