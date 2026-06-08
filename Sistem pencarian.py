import json
import os
import random

DATA_FILE = "data_produk.json"


def generate_sample_data(num=100):
    dataset = []
    for i in range(num):
        dataset.append({
            "product_id": f"PRD-{i:04d}-{'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[i % 26]}",
            "nama_produk": f"Produk-{i:04d}-{'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[i % 26]}",
            "harga": random.randint(5, 500) * 1000,
            "rating": round(random.uniform(1.0, 5.0), 1),
        })
    return dataset


def save_data(products, filename=DATA_FILE):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=4)


def load_data(filename=DATA_FILE):
    if not os.path.exists(filename):
        products = generate_sample_data(100)
        save_data(products, filename)
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def linear_search(products, target_id):
    for index, item in enumerate(products):
        if item["product_id"] == target_id:
            return index, item
    return -1, None


def binary_search(products, target_id):
    low = 0
    high = len(products) - 1
    while low <= high:
        mid = (low + high) // 2
        mid_id = products[mid]["product_id"]
        if mid_id == target_id:
            return mid, products[mid]
        if mid_id < target_id:
            low = mid + 1
        else:
            high = mid - 1
    return -1, None


def build_index(products):
    return {item["product_id"]: index for index, item in enumerate(products)}


def hash_search(products, products_index, target_id):
    index = products_index.get(target_id, -1)
    return (index, products[index]) if index != -1 else (-1, None)


def print_search_result(method_name, result):
    index, item = result
    if index == -1:
        print(f"[{method_name}] Produk tidak ditemukan.")
        return
    print(f"[{method_name}] Ditemukan di indeks: {index}")
    print(f"  ID   : {item['product_id']}")
    print(f"  Nama : {item['nama_produk']}")
    print(f"  Harga: Rp{item['harga']:,}")
    print(f"  Rating: {item['rating']}")


def main():
    products = load_data()

    print("=== Tugas Pencarian Produk berdasarkan ID ===")
    print("1. Linear Search (data tidak terurut)")
    print("2. Binary Search (data terurut menurut product_id)")
    print("3. Hash Search (index cepat dari dictionary)")
    print("---")

    target_id = input("Masukkan Product ID yang dicari (misal PRD-0005-F): ").strip()
    print()

    print_search_result("Linear Search", linear_search(products, target_id))

    sorted_products = sorted(products, key=lambda item: item["product_id"])
    print_search_result("Binary Search", binary_search(sorted_products, target_id))

    products_index = build_index(products)
    print_search_result("Hash Search", hash_search(products, products_index, target_id))

    print("\n--- Contoh 10 produk pertama ---")
    for idx, item in enumerate(products[:10]):
        print(f"{idx:02d}. {item['product_id']} | {item['nama_produk']} | Rp{item['harga']:,} | {item['rating']}")


if __name__ == "__main__":
    main()
