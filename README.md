PROGRAM PERENCANAAN ITINERARI WISATA HARIAN DI DAERAH ISTIMEWA YOGYAKARTA

Program berbasis terminal (CLI) yang dibuat dengan Python untuk menyusun itinerari wisata harian di Daerah Istimewa Yogyakarta
berdasarkan anggaran, waktu, rating, dan rute terdekat. Data tempat wisata dibaca dari file CSV dan dapat ditambah atau diubah langsung dari dalam program.


## Daftar isi
- Fitur
- Persyaratan
- Struktur folder
- Format dataset
- Cara menjalankan
- Panduan penggunaan
- Cara kerja algoritma itinerari
- Daftar fungsi
- Keterbatasan
- Tim pengembang
  

## Fitur
==============================================================================================================================
|        Fitur           |                                   Keterangan                                                       |
===============================================================================================================================
| Login                  | Autentikasi dengan nama anggota dan NIM sebagai password                                           |
| Pembersihan data       | Baris tidak valid atau duplikat dibuang otomatis, durasi kosong diisi dengan median                |
| Lihat dataset          | Tabel dua kolom, 40 data per halaman, dengan navigasi halaman                                      |
| Tambah / ubah data     | Input per kolom dengan validasi, cek nama duplikat, konfirmasi, lalu langsung tersimpan ke CSV     |
| Itinerari warga lokal  | Berfokus pada rating tertinggi, tanpa batas anggaran                                               |
| Itinerari wisatawan    | Memakai titik awal pilihan, batas anggaran tiket, dan rating minimum                               |
| Rute terdekat          | Urutan kunjungan disusun dengan metode *nearest neighbor* dan jarak Haversine                      | 
| Ringkasan              | Ringkasan total tiket, durasi, dan jarak per itinerari, serta ringkasan aktivitas sesi saat keluar |
===============================================================================================================================


## Persyaratan

- Python 3.13 atau lebih baru
- Tidak perlu instalasi library tambahan (hanya memakai csv, math, os, sys, time, dan statistics dari standard library)


## Struktur folder

- coding_4c.py    # program utama
- tour.csv        # dataset tempat wisata 
- README.md


> File dataset bernama "tour.csv" dan harus berada di folder yang sama dengan "coding_4c.py", kecuali Anda memberikan path lain saat menjalankan program.


## Format dataset

File CSV wajib memiliki tujuh kolom berikut :
====================================================================
|    Kolom     | Tipe  |               Aturan nilai                |
====================================================================
| Place_Name   | Teks  | Tidak boleh kosong dan harus unik         |
| Category     | Teks  | Tidak boleh kosong                        |
| Price        | Angka | Harga tiket dalam Rupiah, minimal 0       |
| Rating       | Angka | 0 sampai 5                                |
| Time_Minutes | Angka | Lama kunjungan dalam menit, 1 sampai 1440 |
| Latitude     | Angka | -90 sampai 90                             |
| Longitude    | Angka | -180 sampai 180                           |
====================================================================

Ketentuan saat data dibaca:
- Baris dengan nama/kategori kosong, nilai angka tidak valid, nilai di luar rentang, atau nama yang sudah muncul sebelumnya akan dilewati.
- Jika "Time_Minutes" kosong, durasi diisi dengan median durasi pada kategori yang sama. Jika kategori tidak punya data durasi, dipakai median seluruh data, dan jika masih tidak ada, dipakai 60 menit.
- Jika ada kolom wajib yang hilang, program berhenti dan menampilkan pesan [ERROR].


## Cara menjalankan

Gunakan dataset ("tour.csv" di folder program):
python coding_4c.py

Gunakan file dataset lain:
python coding_4c.py path/ke/dataset.csv

Tekan "Ctrl+C" kapan saja untuk menghentikan program.


## Panduan penggunaan

1. Login
   Masukkan nama (tidak sensitif huruf besar/kecil) dan NIM sebagai password. Hanya anggota kelompok yang terdaftar di program yang dapat masuk. Jika salah, input akan diminta ulang.

2. Menu utama
   MENU UTAMA - PERENCANA WISATA YOGYAKARTA
   1. Tampilkan dataset
   2. Tambah / ubah data
   3. Itinerari warga lokal Jogja (fokus rating)
   4. Itinerari wisatawan (titik awal, anggaran, rating)
   5. Keluar

3. Tampilkan dataset
   Menampilkan seluruh nama tempat dalam tabel dua kolom.
   | Input |       Fungsi       |
   ==============================
   | n     | Halaman berikutnya |
   | p     | Halaman sebelumnya |
   | Enter | Kembali ke menu    |
   ==============================

4. Tambah / ubah data
==================================================
| Input |                  Fungsi                 |
===================================================
| 1     | Tambah data baru                        |
| 2     | Ubah data (pilih nomor data dari tabel) |
| Enter | Kembali ke menu                         |
===================================================
Saat mengisi kolom: tekan Enter untuk mempertahankan nilai lama dan ketik batal untuk membatalkan seluruh proses. Input yang tidak valid akan diminta ulang. Sebelum disimpan, program memeriksa nama tempat duplikat dan meminta konfirmasi (y/n). Perubahan langsung ditulis ke file CSV, dan data valid diperbarui otomatis.

5. Itinerari
Kedua mode meminta parameter berikut (nilai dalam kurung siku adalah default, cukup tekan Enter):
==============================================================================================================
|      Parameter       |            Default            |                  Keterangan                         |
==============================================================================================================
| Jumlah hari          | 2                             | Jumlah hari perjalanan                              |
| Jam wisata per hari  | 8                             | Batas total waktu (perjalanan + kunjungan) per hari |
| Jam mulai            | 8                             | Contoh: `8` atau `8.5` untuk 08:30                  |
| Rating minimum       | 4.0 (lokal) / 4.3 (wisatawan) | Rentang 0 sampai 5                                  |
| Batas jarak per hari | 60 km                         | Total jarak tempuh per hari                         |
| Kecepatan kendaraan  | 30 km/jam                     | Dipakai untuk menghitung waktu perjalanan           |
| Kategori             | Semua                         | Pilih nomor kategori, pisahkan dengan koma          |
==============================================================================================================
Khusus mode wisatawan (menu 4), ditambah:
================================================================================================================
|     Parameter  |           Default          |                         Keterangan                             |
================================================================================================================
| Titik awal     | Nol Kilometer Jl.Malioboro | Ketik sebagian nama tempat di dataset atau koordinat lat,lon   |
| Anggaran tiket | Rp200.000                  | Total biaya tiket seluruh perjalanan                           |
================================================================================================================
Pada mode warga lokal (menu 3), tidak ada batas anggaran dan titik awal otomatis diambil dari tempat dengan rating tertinggi.
Hasilnya berupa tabel per hari (destinasi, kategori, rating, tiket, durasi, jarak perjalanan, dan perkiraan jam datang sampai selesai) disertai ringkasan total destinasi, tiket, sisa anggaran, durasi, dan jarak.

6. Keluar
Menu 5 menampilkan ringkasan sesi: nama pengguna, lama sesi, jumlah itinerari dibuat, serta jumlah data yang ditambahkan dan diubah.


## Cara kerja algoritma itinerari

1. Seleksi kandidat. Tempat difilter berdasarkan kategori terpilih dan rating minimum, lalu diurutkan dari rating tertinggi (jika sama, dari harga termurah).
2. Penempatan ke hari. Setiap kandidat dicoba pada setiap hari. Kandidat hanya diterima jika total waktu hari tersebut tidak melebihi jam wisata dan total jarak tidak melebihi batas jarak. Dari hari-hari yang memenuhi syarat, dipilih hari dengan tambahan jarak paling kecil.
3. Kontrol anggaran. Pada mode wisatawan, tempat dengan harga di atas sisa anggaran dilewati.
4. Pengurutan rute. Setiap hari diurutkan dengan *nearest neighbor*, yaitu selalu memilih tempat terdekat berikutnya dari posisi saat ini.
5. Perhitungan jarak. Memakai rumus **Haversine** (jari-jari bumi 6371,0088 km), sehingga jarak yang ditampilkan adalah jarak garis lurus.
6. Perhitungan waktu. waktu = jarak / kecepatan × 60 + durasi kunjungan.


## Daftar fungsi
==========================================================================================================================
|                  Fungsi                 |                                    Peran                                     |
=========================================================================================================================
| main()                                  | Alur utama: cover, login, baca dataset, menu utama, ringkasan sesi           |
| buat_cover()                            | Membuat halaman sampul teks                                                  |
| login()                                 | Autentikasi pengguna                                                         |
| bersihkan(baris)                        | Validasi, deduplikasi, dan pengisian durasi kosong                           |
| tampilkan_dataset(baris, pilih_data)    | Menampilkan dataset berhalaman, juga dipakai untuk memilih data yang diubah  |
| kelola_data(path, kolom, baris, sesi)   | Tambah dan ubah data dengan validasi                                         |
| simpan_csv(path, kolom, baris)          | Menulis data ke file CSV                                                     |
| buat_itinerari(tempat, lokal)           | Proses lengkap pembuatan itinerari                                           |
| pilih_titik_awal(tempat)                | Menentukan titik awal (nama tempat atau koordinat)                           |
| urut(awal, tempat)                      | Mengurutkan rute dengan nearest neighbor                                     |
| ukur(awal, rute, kecepatan)             | Menghitung total jarak dan total waktu rute                                  |
| haversine(lat1, lon1, lat2, lon2)       | Jarak antar dua koordinat (km)                                               |
| tanya, angka, rupiah, jam, tabel, judul | Fungsi bantu input, konversi, dan tampilan                                   |
==========================================================================================================================

## Keterbatasan

- Jarak dihitung garis lurus, bukan jarak jalan sebenarnya.
- Nearest neighbor dan penempatan **greedy** menghasilkan rute yang baik, tetapi tidak dijamin optimal.
- Daftar pengguna login ditulis langsung di dalam kode (*hard-coded*).
- Titik awal default (Nol Kilometer Jl.Malioboro) hanya dikenali jika namanya ada di dataset. Jika tidak ada, masukkan titik awal secara manual.


## Tim pengembang
**Kelompok 4C**
=========================================
|            Nama          |    NIM     |
=========================================
| Dela Firnia              | 2610932026 |
| Haikal Yandri            | 2610932022 |
| Khairina Ardelia Tarigan | 2610933004 |
| Zahwa Aqila Ramadhani    | 2610933024 |
=========================================
**Dosen pengampu:** Dr. Asmuliardi Muluk, S.T., M.T.
**Asisten pembimbing:** Kurnia Rahmat Illahi

---

Dibuat untuk keperluan akademik, mata kuliah Pemrograman Komputer, Universitas Andalas, 2026.
