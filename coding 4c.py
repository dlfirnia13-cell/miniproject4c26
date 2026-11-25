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

def login():
    judul("LOGIN - PERENCANA WISATA YOGYAKARTA")
    users = {}
    if os.path.exists(FILE_USER):
        with open(FILE_USER, encoding="utf-8") as f:
            for baris in f:
                bagian = baris.rstrip("\n").split("\t")
                if len(bagian) == 2:
                    users[bagian[0]] = bagian[1]

    nama = ""
    while not nama:
        nama = input("Nama: ").strip().replace("\t", " ")

    if nama not in users:                                 
        if input(f"'{nama}' belum terdaftar. Daftar? (y/n) [y]: ").strip().lower() == "n":
            return None
        while True:
            sandi = input("Buat password (min 4 karakter): ")
            if len(sandi) >= 4:
                break
        with open(FILE_USER, "a", encoding="utf-8") as f:
            f.write(f"{nama}\t{sandi}\n")
        print(f"Akun dibuat. Selamat datang, {nama}!")
        return nama

    for _ in range(3):                                      
        if input("Password: ") == users[nama]:
            print(f"Login berhasil. Selamat datang kembali, {nama}!")
            return nama
        print("  Password salah.")
    return None

def bersihkan(baris):
    tempat, nama_ada, durasi_kat = [], set(), {}
    for r in baris:
        nama = (r["Place_Name"] or "").strip()
        kat = (r["Category"] or "").strip()
        harga, rating, lat, lon = (angka(r[k]) for k in ("Price", "Rating", "Latitude", "Longitude"))
        if not nama or not kat or None in (harga, rating, lat, lon) or nama in nama_ada:
            continue
        if harga < 0 or not 0 <= rating <= 5 or not -90 <= lat <= 90 or not -180 <= lon <= 180:
            continue
        durasi = angka(r["Time_Minutes"])
        tempat.append({"nama": nama, "kategori": kat, "harga": harga, "rating": rating,
                       "lat": lat, "lon": lon, "durasi": durasi})
        nama_ada.add(nama)
        if durasi is not None:
            durasi_kat.setdefault(kat, []).append(durasi)

    semua = [d for daftar in durasi_kat.values() for d in daftar]
    median_umum = median(semua) if semua else 60
    for t in tempat:
        if t["durasi"] is None:
            t["durasi"] = median(durasi_kat[t["kategori"]]) if t["kategori"] in durasi_kat else median_umum
    return tempat


def tampilkan_dataset(baris, per_halaman=15):
    if not baris:
        input("Dataset kosong. Tekan ENTER...")
        return
    kop = ["No"] + KOLOM
    isi = [[i] + [(r[k] or "-")[:30] for k in KOLOM] for i, r in enumerate(baris, 1)]
    total_hal = math.ceil(len(isi) / per_halaman)
    hal = 0
    while True:
        mulai = hal * per_halaman
        tabel(kop, isi[mulai:mulai + per_halaman])
        print(f"Halaman {hal + 1}/{total_hal} | total {len(isi)} data")
        p = input("[n] berikut  [p] sebelumnya  [Enter] kembali: ").strip().lower()
        if p == "":
            return
        if p == "n" and hal < total_hal - 1:
            hal += 1
        elif p == "p" and hal > 0:
            hal -= 1


def kelola_data(path, kolom, baris, sesi):
    batas = {"Price": (0, 1e12), "Rating": (0, 5), "Time_Minutes": (1, 1440),
             "Latitude": (-90, 90), "Longitude": (-180, 180)}
    judul("KELOLA DATA")
    pilih = input("1. Tambah data  2. Ubah data  (Enter = batal): ").strip()
    if pilih == "1":
        asli, data = None, dict.fromkeys(kolom, "")
    elif pilih == "2":
        tampilkan_dataset(baris)
        no = input("Nomor data yang diubah: ").strip()
        if not (no.isdigit() and 1 <= int(no) <= len(baris)):
            return
        asli = baris[int(no) - 1]
        data = dict(asli)
    else:
        return

    for k in KOLOM:                                       
        lama = data[k] or ""
        while True:
            isi = input(f"{k}" + (f" [{lama}]" if lama else "") + ": ").strip() or lama
            if k in ("Place_Name", "Category"):
                ok = isi != ""
            else:
                x = angka(isi)
                ok = x is not None and batas[k][0] <= x <= batas[k][1]
            if ok:
                break
            print("  Input tidak valid.")
        data[k] = isi

    for r in baris:                                     
        if r is not asli and r["Place_Name"].strip().lower() == data["Place_Name"].lower():
            print("[!] Nama sudah dipakai. Dibatalkan.")
            return

    if asli is None:
        baris.append(data)
        sesi["tambah"] += 1
    else:
        asli.update(data)
        sesi["ubah"] += 1
    simpan_csv(path, kolom, baris)
    print("Perubahan disimpan ke CSV.")

def urut(awal, tempat):
    sisa, rute, pos = list(tempat), [], awal
    while sisa:
        t = min(sisa, key=lambda x: haversine(pos[0], pos[1], x["lat"], x["lon"]))
        rute.append(t)
        sisa.remove(t)
        pos = (t["lat"], t["lon"])
    return rute

def ukur(awal, rute, kecepatan):
    pos, jarak = awal, 0.0
    for t in rute:
        jarak += haversine(pos[0], pos[1], t["lat"], t["lon"])
        pos = (t["lat"], t["lon"])
    return jarak, jarak / kecepatan * 60 + sum(t["durasi"] for t in rute)

def pilih_titik_awal(tempat):
    print(f"\nTitik awal: Enter = {TITIK_DEFAULT}, atau ketik sebagian nama / 'lat,lon'")
    while True:
        isi = input("Titik awal: ").strip() or TITIK_DEFAULT
        if "," in isi and angka(isi.split(",")[0]) is not None:
            try:
                lat, lon = [float(x) for x in isi.split(",")]
                return (lat, lon), f"Koordinat ({lat}, {lon})"
            except ValueError:
                print("  Format koordinat salah.")
                continue
        cocok = [t for t in tempat if isi.lower() in t["nama"].lower()]
        if len(cocok) == 1:
            return (cocok[0]["lat"], cocok[0]["lon"]), cocok[0]["nama"]
        print("  Tidak ditemukan." if not cocok else
              "  Ada beberapa: " + "; ".join(t["nama"] for t in cocok[:8]))


def buat_itinerari(tempat, lokal):
    judul("ITINERARI WARGA LOKAL (FOKUS RATING)" if lokal else "ITINERARI WISATAWAN")

    n_hari = tanya("Jumlah hari", 2, int)
    if lokal:
        anggaran, rating_def = None, 4.0
    else:
        titik, nama_awal = pilih_titik_awal(tempat)
        anggaran, rating_def = tanya("Anggaran tiket Rp", 200000, int), 4.3
    jam_hari = tanya("Jam wisata per hari", 8)
    mulai = tanya("Jam mulai (contoh 8 atau 8.5)", 8) * 60
    rating_min = tanya("Rating minimum (0-5)", rating_def)
    maks_km = tanya("Batas jarak per hari (km)", 60)
    kecepatan = max(tanya("Kecepatan kendaraan (km/jam)", 30), 1)

    daftar_kat = sorted({t["kategori"] for t in tempat})
    for no, k in enumerate(daftar_kat, 1):
        print(f"  {no}. {k}")
    isi = input("Pilih nomor kategori (pisah koma, Enter = semua): ").strip()
    try:
        pilihan = [daftar_kat[int(x) - 1] for x in isi.split(",")] if isi else daftar_kat
    except (ValueError, IndexError):
        print("Input tidak valid, memakai semua kategori.")
        pilihan = daftar_kat

    kandidat = [t for t in tempat if t["kategori"] in pilihan and t["rating"] >= rating_min]
    kandidat.sort(key=lambda t: (-t["rating"], t["harga"]))
    if not kandidat:
        input("\n[!] Tidak ada destinasi yang sesuai. Tekan ENTER...")
        return False

    if lokal:                                  
        titik, nama_awal = (kandidat[0]["lat"], kandidat[0]["lon"]), kandidat[0]["nama"]

    hari = [[] for _ in range(n_hari)]
    sisa = anggaran
    for t in kandidat:
        if anggaran is not None and t["harga"] > sisa:
            continue
        terbaik = None                   
        for h in range(n_hari):
            rute = urut(titik, hari[h] + [t])
            jarak, menit = ukur(titik, rute, kecepatan)
            if menit > jam_hari * 60 or jarak > maks_km:
                continue
            tambahan = jarak - ukur(titik, hari[h], kecepatan)[0]
            if terbaik is None or tambahan < terbaik[0]:
                terbaik = (tambahan, h, rute)
        if terbaik:
            hari[terbaik[1]] = terbaik[2]
            if anggaran is not None:
                sisa -= t["harga"]

    if not any(hari):
        input("\n[!] Tidak ada destinasi yang muat. Longgarkan parameter. Tekan ENTER...")
        return False

    judul("ITINERARI WISATA YOGYAKARTA")
    print(f"Titik awal: {nama_awal} | {n_hari} hari | mulai {jam(mulai)} | {jam_hari} jam/hari")
    kop = ["No", "Destinasi", "Kategori", "Rating", "Tiket", "Durasi", "Perjalanan", "Perkiraan"]
    total_biaya, total_menit, total_jarak = 0, 0, 0

    for no_hari, rute in enumerate(hari, 1):
        if not rute:
            print(f"\nHARI {no_hari}: (tidak ada destinasi)")
            continue
        pos, waktu, isi = titik, mulai, []
        for urutan, t in enumerate(rute, 1):
            jarak = haversine(pos[0], pos[1], t["lat"], t["lon"])
            tempuh = jarak / kecepatan * 60
            datang = waktu + tempuh
            waktu = datang + t["durasi"]
            isi.append([urutan, t["nama"], t["kategori"], t["rating"],
                        "Gratis" if t["harga"] == 0 else rupiah(t["harga"]),
                        f"{int(t['durasi'])} mnt", f"+{jarak:.1f} km ({int(round(tempuh))} mnt)",
                        f"{jam(datang)} - {jam(waktu)}"])
            pos = (t["lat"], t["lon"])

        jarak_hari, menit_hari = ukur(titik, rute, kecepatan)
        biaya = sum(t["harga"] for t in rute)
        print(f"\nHARI {no_hari}")
        tabel(kop, isi)
        print(f"  {len(rute)} destinasi | tiket {rupiah(biaya)} | "
              f"{menit_hari / 60:.1f} jam | {jarak_hari:.1f} km")
        total_biaya += biaya
        total_menit += menit_hari
        total_jarak += jarak_hari

    judul("RINGKASAN TOTAL")
    print(f"Total destinasi : {sum(len(h) for h in hari)}")
    print(f"Total tiket     : {rupiah(total_biaya)}")
    if anggaran is not None:
        print(f"Sisa anggaran   : {rupiah(sisa)}")
    print(f"Total durasi    : {total_menit / 60:.1f} jam")
    print(f"Total jarak     : {total_jarak:.1f} km (garis lurus)")

    input("\nTekan ENTER untuk kembali ke menu...")
    return True

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(FOLDER, "tour.csv")

    print("=" * 70)
    print("MINI PROJECT PEMROGRAMAN KOMPUTER".center(70))
    print("Program Perencanaan Itinerari Wisata Harian di Yogyakarta".center(70))
    print("Kelompok 4C - Universitas Andalas".center(70))
    print("=" * 70)

    nama = login()
    if not nama:
        print("Login gagal. Program ditutup.")
        return

    if not os.path.exists(path):
        print(f"[ERROR] File dataset tidak ditemukan: {path}")
        return
    with open(path, newline="", encoding="utf-8-sig") as f:
        pembaca = csv.DictReader(f)
        kolom, baris = list(pembaca.fieldnames or []), list(pembaca)
    hilang = [k for k in KOLOM if k not in kolom]
    if hilang:
        print(f"[ERROR] Kolom wajib tidak ada: {hilang}")
        return

    tempat = bersihkan(baris)
    print(f"\nDataset: {len(baris)} baris -> {len(tempat)} data valid dipakai")
    time.sleep(1.5)

    sesi = {"itinerari": 0, "tambah": 0, "ubah": 0}
    mulai = time.time()
    while True:
        judul("MENU UTAMA - PERENCANA WISATA YOGYAKARTA")
        print("  1. Tampilkan dataset")
        print("  2. Tambah / ubah data")
        print("  3. Itinerari warga lokal Jogja (fokus rating)")
        print("  4. Itinerari wisatawan (titik awal, anggaran, rating)")
        print("  5. Keluar")
        pilih = input("Pilih menu (1-5): ").strip()

        if pilih == "1":
            tampilkan_dataset(baris)
        elif pilih == "2":
            kelola_data(path, kolom, baris, sesi)
            tempat = bersihkan(baris)
        elif pilih in ("3", "4"):
            if not tempat:
                print("Tidak ada data valid.")
            elif buat_itinerari(tempat, lokal=(pilih == "3")):
                sesi["itinerari"] += 1
        elif pilih == "5":
            judul("RINGKASAN SESI")
            print(f"Pengguna         : {nama}")
            print(f"Lama sesi        : {(time.time() - mulai) / 60:.1f} menit")
            print(f"Itinerari dibuat : {sesi['itinerari']}")
            print(f"Data ditambahkan : {sesi['tambah']}")
            print(f"Data diubah      : {sesi['ubah']}")
            print("\nTerima kasih. Sampai jumpa!")
            return
        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\nProgram dihentikan pengguna.")