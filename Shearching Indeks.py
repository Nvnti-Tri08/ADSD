import random
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

# konstanta
RANDOM_SEED = 42
PRODUCT_COUNT = 500
PRICE_MIN, PRICE_MAX, PRICE_MULTIPLIER = 50, 500, 10000
RATING_MIN, RATING_MAX = 3.0, 5.0
WINDOW_TITLE = "🛒 Pencarian Produk E-Commerce"
WINDOW_SIZE = "1200x800"
WINDOW_MIN_SIZE = (800, 600)
COLOR_BG_DARK, COLOR_BG_HEADER, COLOR_BG_TABLE = "#0f172a", "#16213e", "#252540"
COLOR_ACCENT, COLOR_ACCENT_HOVER = "#00bcd4", "#0097a7"
COLOR_BUTTON_PRIMARY, COLOR_BUTTON_PRIMARY_HOVER = "#22c55e", "#16a34a"
COLOR_BUTTON_SECONDARY, COLOR_BUTTON_SECONDARY_HOVER = "#ef4444", "#dc2626"
COLOR_SUCCESS, COLOR_WARNING, COLOR_ERROR = "lightgreen", "orange", "red"
PRODUCT_NAMES = ["Laptop","Mouse","Keyboard","Monitor","Headset","Webcam","Printer",
    "Scanner","Speaker","Charger","Flashdisk","Hardisk","SSD","RAM","Processor",
    "Motherboard","VGA","PSU","Casing","Cooling Fan"]
ALGORITHM_OPTIONS = ["Linear Search", "Binary Search", "Interpolation Search"]
ALGORITHM_DEFAULT = "Pilih Algoritma"


def generate_products(count):
    random.seed(RANDOM_SEED)
    daftar_produk = []
    for i in range(1, count + 1):
        daftar_produk.append({
            "id": i,
            "nama": random.choice(PRODUCT_NAMES) + " " + str(i),
            "harga": random.randint(PRICE_MIN, PRICE_MAX) * PRICE_MULTIPLIER,
            "rating": round(random.uniform(RATING_MIN, RATING_MAX), 1),
        })
    return daftar_produk


def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target: return i, i + 1
    return -1, len(arr)

def binary_search(arr, target):
    low, high, steps = 0, len(arr) - 1, 0
    while low <= high:
        steps = steps + 1
        mid = (low + high) // 2
        if arr[mid] == target: return mid, steps
        elif arr[mid] < target: low = mid + 1
        else: high = mid - 1
    return -1, steps

def interpolation_search(arr, target):
    low, high, steps = 0, len(arr) - 1, 0
    while low <= high and arr[low] <= target <= arr[high]:
        steps = steps + 1
        if arr[low] == arr[high]: break
        pos = low + (target - arr[low]) * (high - low) // (arr[high] - arr[low])
        if not (0 <= pos <= high): break
        if arr[pos] == target: return pos, steps
        elif arr[pos] < target: low = pos + 1
        else: high = pos - 1
    return -1, steps

def run_all_searches(id_list, target):
    return {
        "Linear Search": linear_search(id_list, target),
        "Binary Search": binary_search(id_list, target),
        "Interpolation Search": interpolation_search(id_list, target),
    }


class BarChart:
    BAR_COLORS = ["#00bcd4", "#4ade80", "#f59e0b"]
    BAR_LABELS = ["Linear", "Binary", "Interpolation"]
    BAR_WIDTH, BAR_GAP = 60, 40
    MT, ML, MB, MR = 40, 60, 60, 20

    def __init__(self, parent):
        self._pending_steps = None
        self.canvas = tk.Canvas(parent, bg=COLOR_BG_TABLE, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        self.canvas.bind("<Configure>", self._on_resize)

    def draw(self, steps):
        self._pending_steps = steps
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        if w > 1 and h > 1: self._render(steps, w, h)

    def clear(self):
        self._pending_steps = None
        self.canvas.delete("all")

    def _on_resize(self, event):
        if self._pending_steps is not None:
            self._render(self._pending_steps, event.width, event.height)

    def _render(self, steps, width, height):
        self.canvas.delete("all")
        self._draw_axes(width, height)
        max_steps = max(steps) if max(steps) > 0 else 1
        inner_h = height - self.MT - self.MB
        total_w = len(steps) * self.BAR_WIDTH + (len(steps) - 1) * self.BAR_GAP
        start_x = self.ML + max(0, width - self.ML - self.MR - total_w) // 2
        y_base = height - self.MB
        for i in range(len(steps)):
            x0 = start_x + i * (self.BAR_WIDTH + self.BAR_GAP)
            x1 = x0 + self.BAR_WIDTH
            y0 = y_base - (steps[i] / max_steps) * inner_h
            xm = (x0 + x1) / 2
            self.canvas.create_rectangle(x0, y0, x1, y_base, fill=self.BAR_COLORS[i], outline="white")
            self.canvas.create_text(xm, y0 - 12, text=str(steps[i]), fill="white", font=("Arial", 10, "bold"))
            self.canvas.create_text(xm, y_base + 20, text=self.BAR_LABELS[i], fill="white", font=("Arial", 10))

    def _draw_axes(self, width, height):
        y = height - self.MB
        self.canvas.create_line(self.ML, self.MT, self.ML, y, fill="#606080", width=2)
        self.canvas.create_line(self.ML, y, width - self.MR, y, fill="#606080", width=2)


class ProductTable:
    COLUMNS = ("ID Produk", "Nama Produk", "Harga", "Rating")

    def __init__(self, parent):
        self._apply_style()
        self.tree = self._build_tree(parent)
        sb = ttk.Scrollbar(parent, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y", pady=10)

    def populate(self, products):
        for p in products:
            self.tree.insert("", "end", values=(
                p["id"], p["nama"], "Rp " + f"{p['harga']:,}", str(p["rating"]) + " ⭐"))

    def highlight_row(self, index):
        for row in self.tree.get_children(): self.tree.item(row, tags=())
        item_id = self.tree.get_children()[index]
        self.tree.item(item_id, tags=("found",))
        self.tree.tag_configure("found", background=COLOR_ACCENT)
        self.tree.see(item_id)

    def _apply_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=COLOR_BG_TABLE, foreground="white",
            rowheight=36, fieldbackground=COLOR_BG_TABLE, borderwidth=0, font=("Arial", 16))
        style.configure("Treeview.Heading", background=COLOR_ACCENT, foreground="white", font=("Arial", 16, "bold"))
        style.map("Treeview", background=[("selected", COLOR_ACCENT)])

    def _build_tree(self, parent):
        tree = ttk.Treeview(parent, columns=self.COLUMNS, show="headings")
        for col in self.COLUMNS: tree.heading(col, text=col)
        tree.column("ID Produk", width=100, anchor="center")
        tree.column("Nama Produk", width=320, anchor="w")
        tree.column("Harga", width=180, anchor="center")
        tree.column("Rating", width=120, anchor="center")
        tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        return tree


class SearchApp:
    def __init__(self):
        self.products = generate_products(PRODUCT_COUNT)
        self.id_list = []
        for p in self.products: self.id_list.append(p["id"])
        self.app = self._setup_window()
        self._build_header()
        self._build_search_bar()
        self._build_main_content()

    def run(self):
        self.app.mainloop()

    def _setup_window(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        app = ctk.CTk()
        app.title(WINDOW_TITLE)
        app.geometry(WINDOW_SIZE)
        app.resizable(True, True)
        app.minsize(WINDOW_MIN_SIZE[0], WINDOW_MIN_SIZE[1])
        return app

    def _build_header(self):
        frame = ctk.CTkFrame(self.app, fg_color=COLOR_BG_HEADER)
        frame.pack(fill="x")
        ctk.CTkLabel(frame, text="🛒 Sistem Pencarian Produk E-Commerce",
            font=ctk.CTkFont(size=22, weight="bold"), text_color="white").pack(pady=15)

    def _build_search_bar(self):
        frame = ctk.CTkFrame(self.app, fg_color=COLOR_BG_DARK, corner_radius=10)
        frame.pack(padx=20, pady=10, fill="x")
        ctk.CTkLabel(frame, text="ID Produk:", font=ctk.CTkFont(size=13)).grid(row=0, column=0, padx=10, pady=10)
        self.entry_id = ctk.CTkEntry(frame, placeholder_text="Contoh: 78", width=150)
        self.entry_id.grid(row=0, column=1, padx=10, pady=10)
        ctk.CTkLabel(frame, text="Algoritma:", font=ctk.CTkFont(size=13)).grid(row=0, column=2, padx=10, pady=10)
        self.combo_algo = ctk.CTkComboBox(frame, values=ALGORITHM_OPTIONS, width=200)
        self.combo_algo.set(ALGORITHM_DEFAULT)
        self.combo_algo.grid(row=0, column=3, padx=10, pady=10)
        ctk.CTkButton(frame, text="🔍 CARI", width=100, fg_color=COLOR_BUTTON_PRIMARY,
            hover_color=COLOR_BUTTON_PRIMARY_HOVER, text_color="white", command=self._on_search).grid(row=0, column=4, padx=10, pady=10)
        ctk.CTkButton(frame, text="🔄 RESET", width=100, fg_color=COLOR_BUTTON_SECONDARY,
            hover_color=COLOR_BUTTON_SECONDARY_HOVER, text_color="white", command=self._on_reset).grid(row=0, column=5, padx=10, pady=10)

    def _build_main_content(self):
        frame = ctk.CTkFrame(self.app)
        frame.pack(padx=20, pady=10, fill="both", expand=True)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        # panel kiri: tabel
        tabel_frame = ctk.CTkFrame(frame, fg_color=COLOR_BG_DARK, corner_radius=10)
        tabel_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        tabel_frame.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(tabel_frame, text="📦 Data Produk Gudang",
            font=ctk.CTkFont(size=16, weight="bold"), text_color="white").pack(pady=8)
        self.label_count = ctk.CTkLabel(tabel_frame, text=f"Jumlah Produk: {len(self.products)}",
            font=ctk.CTkFont(size=14), text_color="white")
        self.label_count.pack(pady=(0, 8))
        self.table = ProductTable(tabel_frame)
        self.table.populate(self.products)
        # panel kanan: hasil + chart
        kanan_frame = ctk.CTkFrame(frame)
        kanan_frame.grid(row=0, column=1, sticky="nsew")
        kanan_frame.grid_rowconfigure(1, weight=1)
        kanan_frame.grid_columnconfigure(0, weight=1)
        result_frame = ctk.CTkFrame(kanan_frame, fg_color=COLOR_BG_DARK, corner_radius=10)
        result_frame.pack(fill="x", pady=(0, 8))
        ctk.CTkLabel(result_frame, text="🔎 Hasil Pencarian",
            font=ctk.CTkFont(size=14, weight="bold"), text_color="white").pack(pady=(8, 4))
        self.label_result = ctk.CTkLabel(result_frame, text="Masukkan ID produk dan pilih algoritma",
            font=ctk.CTkFont(size=15), justify="left", wraplength=300)
        self.label_result.pack(padx=15, pady=10)
        chart_frame = ctk.CTkFrame(kanan_frame, fg_color=COLOR_BG_DARK, corner_radius=10)
        chart_frame.pack(fill="both", expand=True)
        ctk.CTkLabel(chart_frame, text="📊 Perbandingan Algoritma",
            font=ctk.CTkFont(size=14, weight="bold"), text_color="white").pack(pady=(8, 4))
        self.chart = BarChart(chart_frame)

    def _on_search(self):
        algorithm = self.combo_algo.get()
        raw_id = self.entry_id.get().strip()
        if algorithm == ALGORITHM_DEFAULT:
            self._show_result("⚠️ Silakan pilih algoritma terlebih dahulu!", COLOR_WARNING)
            return
        if not raw_id.isdigit():
            self._show_result("⚠️ Masukkan ID berupa angka!", COLOR_WARNING)
            return
        target = int(raw_id)
        results = run_all_searches(self.id_list, target)
        selected_idx, selected_steps = results[algorithm]
        if selected_idx == -1:
            self._show_result("❌ Produk ID " + str(target) + " tidak ditemukan!", COLOR_ERROR)
            self.chart.clear()
            return
        product = self.products[selected_idx]
        self._show_result(self._format_result(product, algorithm, selected_idx, selected_steps), COLOR_SUCCESS)
        self.table.highlight_row(selected_idx)
        semua_steps = []
        for nama_algo in results:
            idx, steps = results[nama_algo]
            semua_steps.append(steps)
        self.chart.draw(semua_steps)

    def _on_reset(self):
        self.entry_id.delete(0, "end")
        self.combo_algo.set(ALGORITHM_DEFAULT)
        self._show_result("Masukkan ID produk dan pilih algoritma", "white")
        self.chart.clear()
        for row in self.table.tree.get_children(): self.table.tree.item(row, tags=())

    def _format_result(self, product, algorithm, index, steps):
        return (
            "✅ Produk Ditemukan!\n\n"
            "ID Produk : " + str(product["id"]) + "\n"
            "Nama      : " + product["nama"] + "\n"
            "Harga     : Rp " + f"{product['harga']:,}" + "\n"
            "Rating    : " + str(product["rating"]) + " ⭐\n"
            "Indeks    : " + str(index) + "\n"
            "Algoritma : " + algorithm + "\n"
            "Steps     : " + str(steps) + " langkah"
        )

    def _show_result(self, message, color):
        self.label_result.configure(text=message, text_color=color)


if __name__ == "__main__":
    app = SearchApp()
    app.run()