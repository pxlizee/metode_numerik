panjang_cm = 12.345 #5 angka penting
lebar_m = 0.034 #3 angka penting

lebar_cm = lebar_m * 100 #konversi meter ke cm

luas_sebenarnya = panjang_cm * lebar_cm

luas_akhir = round(luas_sebenarnya, 0) # pembulatan ke 1 angka penting

print(f"Panjang: {panjang_cm} cm")
print(f"Lebar: {lebar_m} m = {lebar_cm} cm")
print("-" * 30)
print(f"Hasil perhitungan Luas (sebelum pembulatan): {luas_sebenarnya:.3f} cm²")
print(f"Hasil akhir sesuai aturan angka penting (2 angka penting): {luas_akhir:.0f} cm²")