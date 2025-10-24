import math

def hampiran_ex_maclaurin_orde3(x):
    """
    Menghitung hampiran niai e^x menggunakan deret Maclaurin hingga orde 3.
    Rumus: 1 + x + (x^2/2) + (x^3/6)
    """

    suku_0 = 1
    suku_1 = x
    suku_2 = (x ** 2) / 2.0
    suku_3 = (x ** 3) / 6.0

    return suku_0 + suku_1 + suku_2 + suku_3

print("=" * 50)
print("Program Hampiran Nilai e^x dengan Deret Maclaurin Orde 3")
print("          f(x) ≈ 1 + x + x²/2 + x³/6")
print("=" * 50)

try:
    nilai_x = float(input("Masukkan nilai x: (contoh: 0.1, 0.5, -0.2) "))
    nilai_hampiran = hampiran_ex_maclaurin_orde3(nilai_x)
    nilai_sebenarnya = math.exp(nilai_x)

    galat_absolut = abs(nilai_sebenarnya - nilai_hampiran)

    print("\n" + "=" * 20 + " Hasil Perhitungan " + "=" * 20)
    print(f"Hampiran e^{nilai_x} dengan deret Maclaurin orde 3: {nilai_hampiran:.6f}")
    print(f"Nilai sebenarnya e^{nilai_x}: {nilai_sebenarnya:.6f}")
    print(f"Galat absolut: {galat_absolut:.6f}")
    print("=" * 50)

except ValueError:
    print("Input tidak valid. Silakan masukkan angka yang benar.")
