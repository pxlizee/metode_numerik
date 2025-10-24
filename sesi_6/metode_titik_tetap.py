import numpy as np

# 1. Definisikan fungsi sesuai soal
def f(x):
  """Menghitung nilai f(x) = x^3 - 4x + 1"""
  return x**3 - 4*x + 1

# 2. Tentukan parameter untuk tabel
x_start = -2.0
x_end = 2.0
interval = 0.5

# --- Bagian Utama Program ---
print("=" * 45)
print("   PROGRAM METODE TABEL UNTUK MENCARI AKAR")
print("   Fungsi: f(x) = x³ - 4x + 1")
print("=" * 45)

# Cetak header tabel
print(f"{'x':>8} | {'f(x)':>12}")
print("-" * 24)

# Inisialisasi list untuk menyimpan interval akar
interval_akar = []

# Loop untuk menghasilkan nilai dan mengecek perubahan tanda
x_sebelumnya = None
y_sebelumnya = None

for x in np.arange(x_start, x_end + interval, interval):
  y = f(x)
  print(f"{x:>8.1f} | {y:>12.3f}")

  # Cek perubahan tanda (mulai dari iterasi kedua)
  if x_sebelumnya is not None:
    if y_sebelumnya * y < 0: # Jika hasil kali negatif, berarti tanda berbeda
      interval_akar.append(f"[{x_sebelumnya}, {x}]")

  # Simpan nilai saat ini untuk iterasi berikutnya
  x_sebelumnya = x
  y_sebelumnya = y

# --- Cetak Kesimpulan ---
print("=" * 45)
print("KESIMPULAN:")
print("Berdasarkan tabel di atas, akar-akar fungsi")
print("ditemukan pada interval [a, b] berikut:")
for i, interval_str in enumerate(interval_akar):
  print(f"{i+1}. Interval {interval_str}")
print("=" * 45)