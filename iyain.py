import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

DB_PATH = "gudang_kosmetik.db"

# ── Database setup ──────────────────────────────────────────────────────────

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS produk (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            kode        TEXT UNIQUE NOT NULL,
            nama        TEXT NOT NULL,
            merek       TEXT NOT NULL,
            kategori    TEXT NOT NULL,
            satuan      TEXT NOT NULL,
            stok        INTEGER DEFAULT 0,
            min_stok    INTEGER DEFAULT 10,
            harga_beli  REAL DEFAULT 0,
            lokasi_rak  TEXT,
            kadaluarsa  TEXT,
            keterangan  TEXT
        )
    """)

    c.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS produk_fts
        USING fts5(kode, nama, merek, kategori, keterangan, content='produk', content_rowid='id')
    """)

    # Trigger sinkronisasi FTS
    c.execute("""
        CREATE TRIGGER IF NOT EXISTS produk_ai AFTER INSERT ON produk BEGIN
            INSERT INTO produk_fts(rowid, kode, nama, merek, kategori, keterangan)
            VALUES (new.id, new.kode, new.nama, new.merek, new.kategori, new.keterangan);
        END
    """)
    c.execute("""
        CREATE TRIGGER IF NOT EXISTS produk_ad AFTER DELETE ON produk BEGIN
            INSERT INTO produk_fts(produk_fts, rowid, kode, nama, merek, kategori, keterangan)
            VALUES ('delete', old.id, old.kode, old.nama, old.merek, old.kategori, old.keterangan);
        END
    """)
    c.execute("""
        CREATE TRIGGER IF NOT EXISTS produk_au AFTER UPDATE ON produk BEGIN
            INSERT INTO produk_fts(produk_fts, rowid, kode, nama, merek, kategori, keterangan)
            VALUES ('delete', old.id, old.kode, old.nama, old.merek, old.kategori, old.keterangan);
            INSERT INTO produk_fts(rowid, kode, nama, merek, kategori, keterangan)
            VALUES (new.id, new.kode, new.nama, new.merek, new.kategori, new.keterangan);
        END
    """)

    # Cek apakah data sudah ada
    if c.execute("SELECT COUNT(*) FROM produk").fetchone()[0] == 0:
        seed_data(c)

    conn.commit()
    conn.close()


def seed_data(c):
    data = [
        ("KOS-001", "Lipstik Matte Ultra Stay", "Wardah", "Lipstik", "pcs", 150, 20, 35000, "A1-01", "2026-08-01", "Warna tahan lama, tidak luntur"),
        ("KOS-002", "Foundation Liquid Coverage", "Maybelline", "Foundation", "pcs", 80, 15, 95000, "A1-02", "2026-06-15", "SPF 18, cocok kulit berminyak"),
        ("KOS-003", "Bedak Tabur Luminous", "Wardah", "Bedak", "pcs", 200, 30, 42000, "A1-03", "2026-10-20", "Memberikan efek glowing"),
        ("KOS-004", "Mascara Volume Extreme", "L'Oreal", "Mascara", "pcs", 60, 10, 120000, "A2-01", "2025-12-01", "Bulu mata tebal dan panjang"),
        ("KOS-005", "Eyeliner Pencil Black", "Wardah", "Eyeliner", "pcs", 300, 50, 18000, "A2-02", "2027-01-10", "Mudah diaplikasikan, waterproof"),
        ("KOS-006", "Blush On Peach Glow", "Emina", "Blush On", "pcs", 90, 15, 38000, "A2-03", "2026-09-30", "Warna natural untuk sehari-hari"),
        ("KOS-007", "Serum Vitamin C Brightening", "Somethinc", "Skincare", "pcs", 45, 10, 185000, "B1-01", "2025-11-15", "Mencerahkan dan anti-oksidan"),
        ("KOS-008", "Moisturizer Gel Hydrating", "Cetaphil", "Skincare", "pcs", 70, 12, 210000, "B1-02", "2026-07-20", "Cocok untuk kulit sensitif"),
        ("KOS-009", "Sunscreen SPF 50 PA+++", "Biore", "Skincare", "pcs", 120, 20, 95000, "B1-03", "2026-04-30", "Perlindungan UV maksimal"),
        ("KOS-010", "Toner Rose Water", "The Body Shop", "Skincare", "pcs", 55, 10, 220000, "B2-01", "2026-03-15", "Menyegarkan dan melembapkan"),
        ("KOS-011", "Sabun Muka Foam Cleanser", "Garnier", "Pembersih", "pcs", 180, 25, 48000, "B2-02", "2026-08-10", "Formula lembut tanpa paraben"),
        ("KOS-012", "Micellar Water 400ml", "Bioderma", "Pembersih", "botol", 40, 8, 165000, "B2-03", "2027-02-28", "Membersihkan makeup tanpa bilas"),
        ("KOS-013", "Shampoo Anti-Dandruff 340ml", "Head & Shoulders", "Rambut", "botol", 95, 15, 58000, "C1-01", "2026-11-05", "Mengatasi ketombe membandel"),
        ("KOS-014", "Kondisioner Smooth & Shiny", "Pantene", "Rambut", "botol", 85, 15, 55000, "C1-02", "2026-10-15", "Rambut lembut dan berkilau"),
        ("KOS-015", "Hair Mask Keratin 200ml", "TRESemmé", "Rambut", "tube", 50, 8, 88000, "C1-03", "2026-05-20", "Memperbaiki rambut rusak"),
        ("KOS-016", "Parfum Floral Women 50ml", "Oriflame", "Parfum", "botol", 35, 5, 145000, "D1-01", "2028-01-01", "Aroma bunga segar tahan lama"),
        ("KOS-017", "Body Lotion Whitening 400ml", "Vaseline", "Body Care", "botol", 140, 20, 65000, "D1-02", "2026-12-31", "Mencerahkan kulit tubuh"),
        ("KOS-018", "Deodorant Roll-On 50ml", "Dove", "Body Care", "pcs", 160, 30, 32000, "D1-03", "2026-09-15", "Perlindungan 48 jam"),
        ("KOS-019", "Lip Balm SPF 15", "Blistex", "Lip Care", "pcs", 220, 40, 28000, "A3-01", "2026-06-30", "Melembapkan dan melindungi bibir"),
        ("KOS-020", "Cushion Foundation Medium", "BBIA", "Foundation", "pcs", 30, 8, 195000, "A1-04", "2026-02-28", "Coverage tinggi, finish dewy"),
    ]
    c.executemany("""
        INSERT INTO produk (kode, nama, merek, kategori, satuan, stok, min_stok, harga_beli, lokasi_rak, kadaluarsa, keterangan)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)
    """, data)


def get_conn():
    return sqlite3.connect(DB_PATH)


def cari_produk(keyword: str, kategori: str, filter_stok: bool):
    conn = get_conn()
    params = []

    if keyword.strip():
        # Bersihkan karakter khusus FTS
        kw = keyword.replace('"', '').replace("'", "").strip()
        query = """
            SELECT p.id, p.kode, p.nama, p.merek, p.kategori,
                   p.stok, p.min_stok, p.satuan, p.harga_beli,
                   p.lokasi_rak, p.kadaluarsa
            FROM produk p
            JOIN produk_fts f ON f.rowid = p.id
            WHERE produk_fts MATCH ?
        """
        params.append(f'"{kw}"*')
    else:
        query = """
            SELECT id, kode, nama, merek, kategori,
                   stok, min_stok, satuan, harga_beli,
                   lokasi_rak, kadaluarsa
            FROM produk WHERE 1=1
        """

    if kategori != "Semua":
        query += " AND p.kategori = ?" if keyword.strip() else " AND kategori = ?"
        params.append(kategori)

    if filter_stok:
        query += " AND p.stok <= p.min_stok" if keyword.strip() else " AND stok <= min_stok"

    query += " ORDER BY p.nama" if keyword.strip() else " ORDER BY nama"

    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df


def get_semua_kategori():
    conn = get_conn()
    rows = conn.execute("SELECT DISTINCT kategori FROM produk ORDER BY kategori").fetchall()
    conn.close()
    return ["Semua"] + [r[0] for r in rows]


def get_statistik():
    conn = get_conn()
    total = conn.execute("SELECT COUNT(*) FROM produk").fetchone()[0]
    stok_rendah = conn.execute("SELECT COUNT(*) FROM produk WHERE stok <= min_stok").fetchone()[0]
    total_nilai = conn.execute("SELECT SUM(stok * harga_beli) FROM produk").fetchone()[0] or 0
    kategori_count = conn.execute("SELECT COUNT(DISTINCT kategori) FROM produk").fetchone()[0]
    conn.close()
    return total, stok_rendah, total_nilai, kategori_count


def tambah_produk(kode, nama, merek, kategori, satuan, stok, min_stok, harga_beli, lokasi_rak, kadaluarsa, keterangan):
    conn = get_conn()
    try:
        conn.execute("""
            INSERT INTO produk (kode, nama, merek, kategori, satuan, stok, min_stok, harga_beli, lokasi_rak, kadaluarsa, keterangan)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)
        """, (kode, nama, merek, kategori, satuan, stok, min_stok, harga_beli, lokasi_rak, kadaluarsa, keterangan))
        conn.commit()
        return True, "Produk berhasil ditambahkan!"
    except sqlite3.IntegrityError:
        return False, f"Kode produk '{kode}' sudah ada."
    finally:
        conn.close()


def update_stok(kode, stok_baru):
    conn = get_conn()
    conn.execute("UPDATE produk SET stok=? WHERE kode=?", (stok_baru, kode))
    conn.commit()
    conn.close()


# ── Streamlit UI ────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Gudang Kosmetik",
    page_icon="💄",
    layout="wide",
)

st.markdown("""
<style>
    .stApp { background-color: #fdf6f9; }
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 16px 20px;
        border-left: 4px solid;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }
    .stok-rendah { color: #e74c3c; font-weight: 600; }
    .stok-ok { color: #27ae60; font-weight: 600; }
    div[data-testid="stDataFrame"] { border-radius: 8px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

init_db()

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 💄 Gudang Kosmetik")
    st.markdown("Sistem pencarian & manajemen stok produk")
    st.divider()

    menu = st.radio("Menu", ["🔍 Cari Produk", "➕ Tambah Produk", "📊 Laporan Stok"])

# ── Statistik header ─────────────────────────────────────────────────────────
total, stok_rendah, total_nilai, kat_count = get_statistik()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Produk", f"{total} item")
col2.metric("Stok Menipis", f"{stok_rendah} item", delta=f"-{stok_rendah}" if stok_rendah else None, delta_color="inverse")
col3.metric("Nilai Stok", f"Rp {total_nilai:,.0f}")
col4.metric("Kategori", f"{kat_count} jenis")

st.divider()

# ── Halaman: Cari Produk ─────────────────────────────────────────────────────
if menu == "🔍 Cari Produk":
    st.subheader("🔍 Pencarian Produk")

    col_search, col_kat, col_filter = st.columns([3, 2, 1.5])
    with col_search:
        keyword = st.text_input("Cari nama, merek, kode, atau keterangan...", placeholder="contoh: lipstik, wardah, vitamin c")
    with col_kat:
        kategori = st.selectbox("Kategori", get_semua_kategori())
    with col_filter:
        st.markdown("<br>", unsafe_allow_html=True)
        filter_stok = st.checkbox("Stok menipis saja")

    hasil = cari_produk(keyword, kategori, filter_stok)

    st.markdown(f"**{len(hasil)} produk ditemukan**")

    if hasil.empty:
        st.info("Tidak ada produk yang cocok dengan pencarian.")
    else:
        # Tandai stok menipis
        def warna_stok(row):
            if row["stok"] <= row["min_stok"]:
                return ["background-color: #fff0f0"] * len(row)
            return [""] * len(row)

        tampilan = hasil.rename(columns={
            "kode": "Kode", "nama": "Nama Produk", "merek": "Merek",
            "kategori": "Kategori", "stok": "Stok", "min_stok": "Min. Stok",
            "satuan": "Satuan", "harga_beli": "Harga Beli",
            "lokasi_rak": "Lokasi Rak", "kadaluarsa": "Kadaluarsa"
        }).drop(columns=["id"])

        tampilan["Harga Beli"] = tampilan["Harga Beli"].apply(lambda x: f"Rp {x:,.0f}")

        st.dataframe(
            tampilan.style.apply(warna_stok, axis=1),
            use_container_width=True,
            hide_index=True,
        )

        # Update stok inline
        with st.expander("✏️ Update stok produk"):
            kode_list = hasil["kode"].tolist()
            kode_pilih = st.selectbox("Pilih kode produk", kode_list)
            stok_skrg = hasil[hasil["kode"] == kode_pilih]["stok"].values[0]
            stok_baru = st.number_input("Stok baru", min_value=0, value=int(stok_skrg))
            if st.button("Simpan perubahan"):
                update_stok(kode_pilih, stok_baru)
                st.success(f"Stok {kode_pilih} diperbarui menjadi {stok_baru}.")
                st.rerun()

# ── Halaman: Tambah Produk ───────────────────────────────────────────────────
elif menu == "➕ Tambah Produk":
    st.subheader("➕ Tambah Produk Baru")

    with st.form("form_tambah"):
        c1, c2 = st.columns(2)
        kode    = c1.text_input("Kode Produk*", placeholder="KOS-021")
        nama    = c2.text_input("Nama Produk*", placeholder="Lipstik Matte Red")
        merek   = c1.text_input("Merek*", placeholder="Wardah")
        kategori_input = c2.selectbox("Kategori*", [k for k in get_semua_kategori() if k != "Semua"] + ["Lainnya"])
        satuan  = c1.selectbox("Satuan", ["pcs", "botol", "tube", "sachet", "box", "lusin"])
        stok    = c2.number_input("Stok Awal", min_value=0, value=0)
        min_stok = c1.number_input("Minimum Stok (alert)", min_value=0, value=10)
        harga   = c2.number_input("Harga Beli (Rp)", min_value=0, value=0)
        lokasi  = c1.text_input("Lokasi Rak", placeholder="A1-01")
        exp     = c2.date_input("Tanggal Kadaluarsa", value=date(2026, 12, 31))
        ket     = st.text_area("Keterangan tambahan", placeholder="Deskripsi singkat produk...")

        submitted = st.form_submit_button("💾 Simpan Produk", use_container_width=True)

    if submitted:
        if not kode or not nama or not merek:
            st.error("Kode, nama, dan merek wajib diisi.")
        else:
            ok, msg = tambah_produk(kode, nama, merek, kategori_input, satuan,
                                     stok, min_stok, harga, lokasi, str(exp), ket)
            if ok:
                st.success(msg)
            else:
                st.error(msg)

# ── Halaman: Laporan Stok ────────────────────────────────────────────────────
elif menu == "📊 Laporan Stok":
    st.subheader("📊 Laporan Stok per Kategori")

    conn = get_conn()
    df_lap = pd.read_sql_query("""
        SELECT kategori,
               COUNT(*) as jumlah_item,
               SUM(stok) as total_stok,
               SUM(stok * harga_beli) as nilai_stok,
               SUM(CASE WHEN stok <= min_stok THEN 1 ELSE 0 END) as stok_menipis
        FROM produk
        GROUP BY kategori
        ORDER BY nilai_stok DESC
    """, conn)
    conn.close()

    df_lap["nilai_stok"] = df_lap["nilai_stok"].apply(lambda x: f"Rp {x:,.0f}")
    df_lap = df_lap.rename(columns={
        "kategori": "Kategori", "jumlah_item": "Jml Item",
        "total_stok": "Total Stok", "nilai_stok": "Nilai Stok",
        "stok_menipis": "Stok Menipis"
    })

    st.dataframe(df_lap, use_container_width=True, hide_index=True)

    st.subheader("⚠️ Produk dengan Stok Menipis")
    conn = get_conn()
    df_menipis = pd.read_sql_query("""
        SELECT kode, nama, merek, kategori, stok, min_stok, lokasi_rak
        FROM produk WHERE stok <= min_stok ORDER BY stok ASC
    """, conn)
    conn.close()

    if df_menipis.empty:
        st.success("Semua stok dalam kondisi aman.")
    else:
        st.warning(f"{len(df_menipis)} produk perlu segera direstok!")
        st.dataframe(df_menipis.rename(columns={
            "kode": "Kode", "nama": "Nama", "merek": "Merek",
            "kategori": "Kategori", "stok": "Stok Saat Ini",
            "min_stok": "Min. Stok", "lokasi_rak": "Lokasi Rak"
        }), use_container_width=True, hide_index=True)