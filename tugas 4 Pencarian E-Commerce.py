import json
import random

# MEMBUAT DATA RANDOM
def get_sample_data(num=100):
    dataset = []
    for i in range(num):
        dataset.append({
            "product_id": f"PRD-{i:03d}-{'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[i % 26]}",
            "nama_produk": f"Produk-{i:03d}-{'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[i % 26]}",
            "harga": random.randint(5, 500) * 1000,
            "rating": round(random.uniform(1.0, 5.0), 1),
        })
    return dataset

# GENERATE & SIMPAN DATA
data_awal = get_sample_data(100)
with open("data_produk.json", "w") as f:
    json.dump(data_awal, f, indent=4)

# SELECTION SORT (Berdasarkan HARGA - Ascending)
def selection_sort_by_price(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j]['harga'] < arr[min_idx]['harga']:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

# INSERTION SORT (Berdasarkan RATING - Descending)
def insertion_sort_by_rating(arr):
    for i in range(1, len(arr)):
        key_item = arr[i]
        j = i - 1
        while j >= 0 and key_item['rating'] > arr[j]['rating']:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key_item
    return arr


# MEMBACA DATA JSON
with open("data_produk.json", 'r') as f:
    products = json.load(f)

# SORTING DATA
sorted_by_price  = selection_sort_by_price(products.copy())
sorted_by_rating = insertion_sort_by_rating(products.copy())

# OUTPUT 
pemisah = "-" * 55

print("\n[SELECTION SORT] Top 10 Harga secara Ascending:")
print(pemisah)
print(f"{'No':>5} {'Nama Produk':<20} {'Harga':>12} {'Rating':>10}")
print(pemisah)
for i, p in enumerate(sorted_by_price[:10], 1):
    print(f"  {i:>2}. {p['nama_produk']:<20} | Rp{p['harga']:>10,.0f} | ⭐ {p['rating']:<3}")

print("\n[INSERTION SORT] Top 10 Rating secara Descending:")
print(pemisah)
print(f"{'No':>5} {'Nama Produk':<20} {'Harga':>12} {'Rating':>10}")
print(pemisah)
for i, p in enumerate(sorted_by_rating[:10], 1):
    print(f"  {i:>2}. {p['nama_produk']:<20} | ⭐ {p['rating']:<3}  | Rp{p['harga']:>10,.0f}")

print("\n" + pemisah)