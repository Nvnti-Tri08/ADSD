import json
import random

def data_barang(num=200):
    dataset = []
    for i in range(num):
        dataset.append({
            "product_id": f"PRD-{i:04d}-{'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[i % 26]}",
            "nama_produk": f"Produk-{i:04d}-{'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[i % 26]}",
            "harga": random.randint(5, 500) * 1000,
            "rating": round(random.uniform(1.0, 5.0), 1)
        })
    return dataset

# Membuat file JSON
data_awal = data_barang(200)
with open("data_produk.json", "w") as f:
    json.dump(data_awal, f, indent=4)

# Selection Sort Harga ASCENDING
def selection_sort_by_price(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j]['harga'] < arr[min_idx]['harga']:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

# Insertion Sort Rating DESCENDING
def insertion_sort_by_rating(arr):
    n = len(arr)
    for i in range(1, n):
        key_item = arr[i]
        j = i - 1
        while j >= 0 and key_item['rating'] > arr[j]['rating']:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key_item
    return arr

# Membaca JSON
with open("data_produk.json", "r") as f:
    data_produk = json.load(f)

# Urut harga termurah
hasil_harga = selection_sort_by_price(data_produk.copy())

# Dari hasil itu urut lagi rating tertinggi
hasil_final = insertion_sort_by_rating(hasil_harga)

# OUTPUT AKHIR
print("=" * 60)
print(f"{'No':<4} {'Nama Produk':<22} {'Harga':>10} {'Rating':>10}")
print("=" * 60)
print("--- TOP 10 PRODUK (Harga terendah + Rating tertinggi) ---")

for i, product in enumerate(hasil_final[:10], start=1):
    print(f"{i:<4} {product['nama_produk']:<22} Rp{product['harga']:>9,} {product['rating']:>7}")
print("=" * 60)
    