import random

# --- TAHAP 1: Generate Data Produk ---
random.seed(42)

nama_produk = [
    "Laptop", "Mouse", "Keyboard", "Monitor", "Headset",
    "Webcam", "Printer", "Scanner", "Speaker", "Charger",
    "Flashdisk", "Hardisk", "SSD", "RAM", "Processor",
    "Motherboard", "VGA", "PSU", "Casing", "Cooling Fan"
]

produk_list = []
for i in range(1, 501):
    produk = {
        "id": i * 1,
        "nama": f"{random.choice(nama_produk)} {i}",
        "harga": random.randint(50, 500) * 10000,
        "rating": round(random.uniform(3.0, 5.0), 1),
    }
    produk_list.append(produk)

# Data ID untuk algoritma (sudah terurut)
id_list = [p["id"] for p in produk_list]


def generate_numeric_data(n=100, start=10, step=10, shuffle=True):
    """Generate numeric-only ID list (no product names).

    Returns a list of integers. If `shuffle` is True, the list is shuffled
    to simulate unsorted warehouse data.
    """
    data = [start + i * step for i in range(n)]
    if shuffle:
        random.shuffle(data)
    return data


def run_single_algorithm(algo, arr=None, target=None):
    """Run a single specified algorithm on given array.

    `algo` can be: 'linear', 'binary', 'interpolation', or 'hash'.
    If `arr` is None, generate numeric data without product names.
    If `target` is None, pick a random element from `arr`.
    Returns: (index, steps, algo_used)
    """
    if arr is None:
        arr = generate_numeric_data()

    if target is None:
        import random as _r
        target = _r.choice(arr)

    if algo == 'linear':
        idx, steps = linear_search(arr, target)
    elif algo == 'binary':
        # ensure sorted for binary
        sorted_arr = sorted(arr)
        pos, steps = binary_search(sorted_arr, target)
        if pos == -1:
            idx = -1
        else:
            # map back to original array index (first occurrence)
            try:
                idx = arr.index(sorted_arr[pos])
            except ValueError:
                idx = -1
    elif algo == 'interpolation':
        # interpolation expects numeric array; sort to improve chance
        sorted_arr = sorted(arr)
        pos, steps = interpolation_search(sorted_arr, target)
        if pos == -1:
            idx = -1
        else:
            try:
                idx = arr.index(sorted_arr[pos])
            except ValueError:
                idx = -1
    elif algo == 'hash':
        idx_map = build_index(arr)
        idx, steps = hash_search(idx_map, target)
    else:
        raise ValueError('Unknown algorithm: ' + str(algo))

    return idx, steps, algo


# --- TAHAP 2: Algoritma Pencarian ---

def linear_search(arr, target):
    steps = 0
    for i in range(len(arr)):
        steps += 1
        if arr[i] == target:
            return i, steps
    return -1, steps


def binary_search(arr, target):
    low, high, steps = 0, len(arr) - 1, 0
    while low <= high:
        steps += 1
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid, steps
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1, steps


def interpolation_search(arr, target):
    low, high, steps = 0, len(arr) - 1, 0
    while low <= high and target >= arr[low] and target <= arr[high]:
        steps += 1
        # Hindari pembagian nol
        if arr[high] == arr[low]:
            break
        pos = low + ((target - arr[low]) * (high - low) // (arr[high] - arr[low]))
        if pos < 0 or pos > high:
            break
        if arr[pos] == target:
            return pos, steps
        elif arr[pos] < target:
            low = pos + 1
        else:
            high = pos - 1
    return -1, steps


def build_index(arr):
    """Bangun indeks hash sederhana: nilai -> indeks pertama."""
    return {val: idx for idx, val in enumerate(arr)}


def hash_search(index_map, target):
    """Cari menggunakan indeks hash (dictionary)."""
    steps = 1
    if isinstance(index_map, dict):
        return index_map.get(target, -1), steps
    return -1, steps


def is_sorted(arr):
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1)) if len(arr) > 1 else True


def search(arr, target, mode='auto'):
    """Wrapper pencarian yang memilih algoritma sesuai skenario.

    mode: 'linear' | 'binary' | 'interpolation' | 'hash' | 'auto'
    Returns: (index, steps)
    """
    # Jika pengguna memberikan dictionary sebagai index map atau meminta hash
    if isinstance(arr, dict) or mode == 'hash':
        index_map = arr if isinstance(arr, dict) else build_index(arr)
        return hash_search(index_map, target)

    if not isinstance(arr, list):
        return -1, 0

    if mode == 'linear':
        return linear_search(arr, target)

    if mode == 'binary':
        if not is_sorted(arr):
            sorted_arr = sorted(arr)
            pos, steps = binary_search(sorted_arr, target)
            if pos == -1:
                return -1, steps
            try:
                orig_idx = arr.index(sorted_arr[pos])
                return orig_idx, steps
            except ValueError:
                return -1, steps
        return binary_search(arr, target)

    if mode == 'interpolation':
        return interpolation_search(arr, target)

    # auto
    if is_sorted(arr):
        return binary_search(arr, target)

    if all(isinstance(x, (int, float)) for x in arr) and len(arr) >= 20:
        rng = max(arr) - min(arr) if arr else 0
        if rng > 0 and (rng / len(arr)) >= 1:
            return interpolation_search(arr, target)

    return linear_search(arr, target)


# --- TAHAP 3: GUI CustomTkinter ---

if __name__ == '__main__':
    import sys
    try:
        import customtkinter as ctk
    except ImportError:
        print("Error: Modul 'customtkinter' tidak ditemukan.")
        print("Silakan install dengan: python -m pip install customtkinter")
        sys.exit(1)
    from tkinter import ttk
    import tkinter as tk
    import time

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("🛒 Pencarian Produk E-Commerce")
    app.geometry("1200x800")
    app.state('zoomed')
    app.resizable(True, True)

    # Header and control layout
    frame_top = ctk.CTkFrame(app, fg_color="#1f2833")
    frame_top.pack(fill="x", padx=12, pady=(10, 4))
    frame_top.grid_columnconfigure(0, weight=1)
    frame_top.grid_columnconfigure(1, weight=0)

    header = ctk.CTkLabel(
        frame_top,
        text="🛒 Sistem Pencarian Produk E-Commerce",
        font=ctk.CTkFont(size=24, weight="bold"),
        text_color="white"
    )
    header.grid(row=0, column=0, sticky="w", padx=15, pady=(10, 4))

    subtitle = ctk.CTkLabel(
        frame_top,
        text="Dashboard modern untuk pencarian produk dan perbandingan algoritma",
        font=ctk.CTkFont(size=13),
        text_color="#b0bec5"
    )
    subtitle.grid(row=1, column=0, sticky="w", padx=15, pady=(0, 10))

    frame_top_right = ctk.CTkFrame(frame_top, fg_color="#1f2833", corner_radius=15)
    frame_top_right.grid(row=0, column=1, rowspan=2, sticky="ne", padx=15, pady=12)

    label_online = ctk.CTkLabel(frame_top_right, text="🟢 Online", font=ctk.CTkFont(size=12, weight="bold"), text_color="#2ecc71")
    label_online.pack(anchor="e", pady=(12, 2), padx=(0, 8))
    label_clock = ctk.CTkLabel(frame_top_right, text="00:00:00", font=ctk.CTkFont(size=18, weight="bold"), text_color="white")
    label_clock.pack(anchor="e", pady=(0, 4), padx=(0, 8))
    label_header_algo = ctk.CTkLabel(frame_top_right, text="Algoritma: -", font=ctk.CTkFont(size=11), text_color="#b0bec5")
    label_header_algo.pack(anchor="e", pady=(0, 10), padx=(0, 8))

    # Search and algorithm controls
    frame_controls = ctk.CTkFrame(app, fg_color="#16222a")
    frame_controls.pack(fill="x", padx=12, pady=4)

    ctk.CTkLabel(frame_controls, text="ID Produk:", font=ctk.CTkFont(size=14)).grid(row=0, column=0, padx=(12, 8), pady=10)
    entry_id = ctk.CTkEntry(frame_controls, placeholder_text=f"Contoh: 1-{len(produk_list)}", width=160)
    entry_id.grid(row=0, column=1, padx=(0, 8), pady=10)

    ctk.CTkLabel(frame_controls, text="Algoritma:", font=ctk.CTkFont(size=14)).grid(row=0, column=2, padx=(8, 8), pady=10)
    combo_algo = ctk.CTkComboBox(
        frame_controls,
        values=["Linear Search", "Binary Search", "Interpolation Search"],
        width=200,
    )
    combo_algo.set("Pilih Algoritma")
    combo_algo.grid(row=0, column=3, padx=12, pady=12)

    # Main content area with sidebar
    frame_body = ctk.CTkFrame(app, fg_color="#0f1419")
    frame_body.pack(fill="both", expand=True, padx=12, pady=(0, 12))

    # Sidebar removed. Search status now shows in the result panel.

    # Table and result section
    frame_main = ctk.CTkFrame(frame_body, fg_color="#0f1419")
    frame_main.pack(fill="both", expand=True, pady=0)

    def clear_result():
        entry_id.delete(0, "end")
        combo_algo.set("Pilih Algoritma")
        label_hasil.configure(
            text="Masukkan ID produk dan pilih algoritma, lalu klik CARI.",
            text_color="white"
        )
        label_search_status.configure(text="Belum ada pencarian")
        label_header_algo.configure(text="Algoritma: -")
        chart_canvas.delete("all")
        for row in tree.get_children():
            tree.item(row, tags=())

    def update_algorithm_chart(target):
        values = {
            "Linear": linear_search(id_list, target)[1],
            "Binary": binary_search(id_list, target)[1],
            "Interpolation": interpolation_search(id_list, target)[1],
        }
        chart_canvas.delete("all")
        chart_canvas.configure(bg="#0f1419")
        chart_canvas.update_idletasks()
        
        # Get actual canvas dimensions or use defaults
        chart_width = chart_canvas.winfo_width()
        chart_height = chart_canvas.winfo_height()
        if chart_width <= 1:
            chart_width = 480
        if chart_height <= 1:
            chart_height = 380
            
        max_steps = max(values.values()) if values else 1
        # Add buffer to max_steps for better visualization
        max_steps_display = int(max_steps * 1.2) + 1

        margin_left = 60
        margin_right = 30
        margin_top = 50
        margin_bottom = 110
        inner_width = chart_width - margin_left - margin_right
        inner_height = chart_height - margin_top - margin_bottom
        
        num_bars = len(values)
        bar_width = max(40, min(80, int(inner_width / (num_bars * 2.5))))
        gap = max(20, int(bar_width * 0.6))
        total_width = num_bars * bar_width + (num_bars - 1) * gap
        start_x = margin_left + max(10, (inner_width - total_width) / 2)
        
        colors = {"Linear": "#e74c3c", "Binary": "#2ecc71", "Interpolation": "#3498db"}

        # Draw title
        chart_canvas.create_text(chart_width / 2, 18, text="Step Count Comparison", fill="#e0e0e0", font=("Arial", 12, "bold"))
        
        # Draw axes
        axis_color = "#2d3748"
        chart_canvas.create_line(margin_left, margin_top, margin_left, chart_height - margin_bottom, fill=axis_color, width=2)
        chart_canvas.create_line(margin_left, chart_height - margin_bottom, chart_width - margin_right, chart_height - margin_bottom, fill=axis_color, width=2)
        
        # Draw grid lines and Y-axis labels
        num_grid_lines = 5
        for i in range(num_grid_lines):
            y = margin_top + i * (inner_height / (num_grid_lines - 1))
            value = int(max_steps_display * (1 - i / (num_grid_lines - 1)))
            
            # Grid line
            chart_canvas.create_line(margin_left, y, chart_width - margin_right, y, fill="#1a202c", dash=(2, 4))
            
            # Y-axis label
            chart_canvas.create_text(margin_left - 12, y, text=str(value), fill="#a0aec0", font=("Arial", 9), anchor="e")

        # Draw bars
        available_height = inner_height - 20
        for idx, (label, step) in enumerate(values.items()):
            x0 = start_x + idx * (bar_width + gap)
            x1 = x0 + bar_width
            bar_height = max(15, int((step / max_steps_display) * available_height))
            y0 = (chart_height - margin_bottom) - bar_height
            y1 = chart_height - margin_bottom
            
            # Draw bar with shadow effect
            chart_canvas.create_rectangle(x0, y0, x1, y1, fill=colors[label], outline="#ffffff", width=1)
            
            # Draw step count on top of bar
            chart_canvas.create_text((x0 + x1) / 2, y0 - 15, text=str(step), fill="white", font=("Arial", 11, "bold"))
            
            # Draw algorithm label below X-axis
            chart_canvas.create_text((x0 + x1) / 2, chart_height - margin_bottom + 40, text=label, fill="#cbd5e0", font=("Arial", 10, "bold"))

    def cari_produk():
        input_id = entry_id.get().strip()
        algoritma = combo_algo.get()

        if algoritma not in ("Linear Search", "Binary Search", "Interpolation Search"):
            label_hasil.configure(text="⚠️ Pilih algoritma terlebih dahulu!", text_color="#f1c40f")
            return

        if not input_id.isdigit():
            label_hasil.configure(text="⚠️ Masukkan ID berupa angka!", text_color="#f1c40f")
            return

        target = int(input_id)
        if target < min(id_list) or target > max(id_list):
            label_hasil.configure(
                text=f"⚠️ ID yang dimasukkan tidak tersedia. Gunakan ID antara {min(id_list)} dan {max(id_list)}.",
                text_color="#f1c40f"
            )
            label_search_status.configure(text="ID di luar range data")
            label_search_steps.configure(text="Steps: -")
            label_search_index.configure(text="Indeks: -")
            chart_canvas.delete("all")
            return

        if algoritma == "Linear Search":
            start_time = time.perf_counter()
            indeks, steps = linear_search(id_list, target)
            exec_time = time.perf_counter() - start_time
            complexity = "O(n)"
            status_text = "Standard"
        elif algoritma == "Binary Search":
            start_time = time.perf_counter()
            indeks, steps = binary_search(id_list, target)
            exec_time = time.perf_counter() - start_time
            complexity = "O(log n)"
            status_text = "Optimal"
        else:
            start_time = time.perf_counter()
            indeks, steps = interpolation_search(id_list, target)
            exec_time = time.perf_counter() - start_time
            complexity = "O(log n)"
            status_text = "Optimal"

        label_header_algo.configure(text=f"Algoritma: {algoritma}")

        if indeks != -1:
            p = produk_list[indeks]
            hasil = (
                f"✅ Produk Ditemukan!\n\n"
                f"ID Produk : {p['id']}\n"
                f"Nama      : {p['nama']}\n"
                f"Harga     : Rp {p['harga']:,}\n"
                f"Rating    : {p['rating']} ⭐\n"
                f"Indeks    : {indeks}\n"
                f"Algoritma : {algoritma}\n"
                f"Steps     : {steps}\n"
                f"Complexity: {complexity}\n"
                f"Execution : {exec_time:.6f}s\n"
                f"Status    : {status_text}"
            )
            label_hasil.configure(text=hasil, text_color="#2ecc71")
            label_search_status.configure(text="Produk ditemukan dengan sukses")
            label_search_steps.configure(text=f"Steps: {steps}")
            label_search_index.configure(text=f"Indeks: {indeks}")
            for row in tree.get_children():
                tree.item(row, tags=())
            item_id = tree.get_children()[indeks]
            tree.item(item_id, tags=("found",))
            tree.tag_configure("found", background="#ffeaa7")
            tree.see(item_id)
            update_algorithm_chart(target)
        else:
            hasil = (
                f"❌ Produk ID {target} tidak ditemukan!\n"
                f"Algoritma  : {algoritma}\n"
                f"Steps      : {steps}\n"
                f"Complexity : {complexity}\n"
                f"Execution  : {exec_time:.6f}s\n"
                f"Status     : {status_text}"
            )
            label_hasil.configure(text=hasil, text_color="#e74c3c")
            label_search_status.configure(text="Produk tidak ditemukan")
            label_search_steps.configure(text=f"Steps: {steps}")
            label_search_index.configure(text="Indeks: -")
            chart_canvas.delete("all")

    btn_cari = ctk.CTkButton(
        frame_controls,
        text="🔍 CARI PRODUK",
        width=150,
        fg_color="#f39c12",
        hover_color="#fbbf24",
        text_color="white",
        command=cari_produk,
    )
    btn_cari.grid(row=0, column=4, padx=(10, 6), pady=10)

    btn_reset = ctk.CTkButton(
        frame_controls,
        text="⟳ RESET",
        width=120,
        fg_color="#7f8c8d",
        hover_color="#8B5CF6",
        text_color="white",
        command=clear_result,
    )
    btn_reset.grid(row=0, column=5, padx=(6, 12), pady=12)

    # Table area
    frame_tabel = ctk.CTkFrame(frame_main, fg_color="#16222a")
    frame_tabel.pack(side="left", fill="both", expand=True, padx=(12, 6), pady=8)

    frame_cards = ctk.CTkFrame(frame_tabel, fg_color="#16222a")
    frame_cards.pack(fill="x", padx=12, pady=(10, 4))
    card = ctk.CTkFrame(frame_cards, fg_color="#1f2833", corner_radius=18, border_width=1, border_color="#2D3748")
    card.pack(fill="x", padx=6, pady=1)
    ctk.CTkLabel(card, text="📦 Total Produk", font=ctk.CTkFont(size=14, weight="bold"), text_color="#b0bec5").pack(anchor="w", padx=16, pady=(10, 2))
    ctk.CTkLabel(card, text=str(len(produk_list)), font=ctk.CTkFont(size=24, weight="bold"), text_color="#F59E0B").pack(anchor="w", padx=16, pady=(0, 10))

    ctk.CTkLabel(frame_tabel, text="📦 Data Produk Gudang", font=ctk.CTkFont(size=16, weight="bold"), text_color="#f5f7fa").pack(pady=(0, 10))

    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Treeview",
        background="#1f2833",
        foreground="white",
        rowheight=40,
        fieldbackground="#1f2833",
        bordercolor="#1f2833",
        borderwidth=0,
        font=("Arial", 11),
    )
    style.configure("Treeview.Heading", background="#EAB308", foreground="white", font=("Arial", 12, "bold"))
    style.map("Treeview", background=[("selected", "#ff6f61")])

    columns = ("ID Produk", "Nama Produk", "Harga", "Rating")
    tree = ttk.Treeview(frame_tabel, columns=columns, show="headings", height=15)
    for col in columns:
        tree.heading(col, text=col)
    tree.column("ID Produk", width=120, anchor="center")
    tree.column("Nama Produk", width=320, anchor="w")
    tree.column("Harga", width=180, anchor="e")
    tree.column("Rating", width=120, anchor="center")

    scrollbar = ttk.Scrollbar(frame_tabel, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(side="left", fill="both", expand=True, padx=(12, 0), pady=12)
    scrollbar.pack(side="right", fill="y", pady=12, padx=(0, 12))

    for p in produk_list:
        tree.insert("", "end", values=(p["id"], p["nama"], f"Rp {p['harga']:,}", f"{p['rating']} ⭐"))

    # Result panel
    frame_hasil = ctk.CTkFrame(frame_main, fg_color="#1f2833", width=520)
    frame_hasil.pack(side="right", fill="y", padx=(6, 12), pady=12)
    frame_hasil.pack_propagate(False)

    ctk.CTkLabel(frame_hasil, text="🔎 Hasil Pencarian", font=ctk.CTkFont(size=16, weight="bold"), text_color="white").pack(pady=(20, 10))

    result_top = ctk.CTkFrame(frame_hasil, fg_color="transparent")
    result_top.pack(fill="x", padx=20, pady=(0, 10), anchor="n")

    label_hasil = ctk.CTkLabel(
        result_top,
        text="Masukkan ID produk dan pilih algoritma, lalu klik CARI.",
        font=ctk.CTkFont(family="Consolas", size=13),
        wraplength=440,
        justify="left"
    )
    label_hasil.pack(in_=result_top, anchor="nw")

    label_search_status = ctk.CTkLabel(
        result_top,
        text="Belum ada pencarian",
        font=ctk.CTkFont(size=12),
        text_color="#b0bec5",
        wraplength=400,
        justify="left"
    )
    label_search_status.pack(anchor="nw", pady=(8, 0))

    label_search_steps = ctk.CTkLabel(result_top, text="Steps: -", font=ctk.CTkFont(size=12), text_color="#ffffff")
    label_search_steps.pack(anchor="nw", pady=(8, 0))
    label_search_index = ctk.CTkLabel(result_top, text="Indeks: -", font=ctk.CTkFont(size=12), text_color="#ffffff")
    label_search_index.pack(anchor="nw", pady=(4, 2))

    chart_frame = ctk.CTkFrame(frame_hasil, fg_color="#16222a", height=5000)
    chart_frame.pack(fill="both", expand=True, padx=20, pady=(10, 12))
    chart_frame.pack_propagate(False)
    ctk.CTkLabel(chart_frame, text="📊 Grafik Perbandingan Algoritma", font=ctk.CTkFont(size=13, weight="bold"), text_color="#e0e0e0").pack(pady=(8, 8))
    chart_canvas = tk.Canvas(chart_frame, width=5200, height=430, bg="#0f1419", highlightthickness=0, relief="flat")
    chart_canvas.pack(fill="both", expand=True, padx=12, pady=(0, 12))

    def refresh_time():
        now = time.strftime("%H:%M:%S")
        label_clock.configure(text=now)
        app.after(1000, refresh_time)

    refresh_time()
    app.mainloop()
