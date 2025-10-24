import math

galat_relatif_persen = 3.0
nilai_pendekatan = 97.0

galat_relatif_desimal = galat_relatif_persen / 100

# compute safely to avoid division by zero
nilai_aktual_1 = None
nilai_aktual_2 = None
if 1 - galat_relatif_desimal != 0:
	nilai_aktual_1 = nilai_pendekatan / (1 - galat_relatif_desimal)
if 1 + galat_relatif_desimal != 0:
	nilai_aktual_2 = nilai_pendekatan / (1 + galat_relatif_desimal)

print("-" * 40)
print("Program Menghitung Nilai Aktual")
print("-" * 40)
print(f"Nilai Pendekatan       : {nilai_pendekatan:.2f}")
print(f"Galat Relatif (%)      : {galat_relatif_persen:.2f} %")
print("-" * 40)
print("Ada dua kemungkinan nilai aktual:")

print("1. Jika nilai pendekatan lebih kecil dari nilai aktual:")
print(f"   Nilai Aktual = {nilai_pendekatan} / (1 - {galat_relatif_desimal:.4f})")
if nilai_aktual_1 is not None and not math.isinf(nilai_aktual_1):
	print(f"   Nilai Aktual = {nilai_aktual_1:.2f}")
else:
	print("   Nilai Aktual = Tidak terdefinisi (pembagi nol)")

print()

print("2. Jika nilai pendekekatan lebih besar dari nilai aktual:")
print(f"   Nilai Aktual = {nilai_pendekatan} / (1 + {galat_relatif_desimal:.4f})")
if nilai_aktual_2 is not None and not math.isinf(nilai_aktual_2):
	print(f"   Nilai Aktual = {nilai_aktual_2:.2f}")
else:
	print("   Nilai Aktual = Tidak terdefinisi (pembagi nol)")
print("-" * 40)
