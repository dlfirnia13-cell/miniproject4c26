import csv
import math
import os
import sys
import time
from statistics import median

KOLOM = ["Place_Name", "Category", "Price", "Rating", "Time_Minutes", "Latitude", "Longitude"]
FOLDER = os.path.dirname(os.path.abspath(__file__))
FILE_USER = os.path.join(FOLDER, "users.txt")
TITIK_DEFAULT = "Nol Kilometer Jl.Malioboro"

def angka(teks):
    try:
        x = float(str(teks).strip())
        return None if math.isnan(x) else x
    except ValueError:
        return None

def rupiah(n):
    return "Rp" + f"{n:,.0f}".replace(",", ".")

def jam(menit):
    menit = int(round(menit))
    return f"{(menit // 60) % 24:02d}:{menit % 60:02d}"

def tanya(pesan, default, tipe=float):
    while True:
        isi = input(f"{pesan} [{default}]: ").strip()
        if isi == "":
            return default
        try:
            return tipe(isi.replace(".", "") if tipe is int else isi)
        except ValueError:
            print("  Masukkan angka yang valid.")

def tabel(kop, isi):
    semua = [kop] + isi
    lebar = [max(len(str(b[i])) for b in semua) + 2 for i in range(len(kop))]
    garis = "+" + "+".join("-" * w for w in lebar) + "+"
    print(garis)
    for n, b in enumerate(semua):
        print("|" + "|".join(str(s).center(w) for s, w in zip(b, lebar)) + "|")
        if n == 0:
            print(garis)
    print(garis)


def judul(teks):
    print("\n" + "=" * 70 + "\n" + teks.center(70) + "\n" + "=" * 70)


def haversine(lat1, lon1, lat2, lon2):
    p1, p2 = math.radians(lat1), math.radians(lat2)
    a = (math.sin((p2 - p1) / 2) ** 2
         + math.cos(p1) * math.cos(p2) * math.sin(math.radians(lon2 - lon1) / 2) ** 2)
    return 2 * 6371.0088 * math.asin(math.sqrt(a))


def simpan_csv(path, kolom, baris):
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=kolom, extrasaction="ignore", restval="")
        w.writeheader()
        w.writerows(baris)
