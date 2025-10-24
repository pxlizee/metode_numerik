import numpy as np

def cek_konvergensi(matriks):
    """Cek apakah sebuah matriks dominan secara diagonal.(diagonally dominant).
    Ini adalah syarat cukup untuk konvergensi metode iteratif seperti Jacobi dan Gauss-Seidel."""

    is_diagonally_dominant = True

    print("Syarat konvergensi:  | A[i,i] > Σ |A[i,j]| untuk j ≠ i\n")
    for i in range(len(matriks)):
        diagonal_element = abs(matriks[i][i])

        off_diagonal_sum = np.sum(np.abs(matriks[i, :])) - diagonal_element

        print(f"Mengecek baris {i + 1}:")
        print(f"  Apakah |{matriks[i, i]}| > {off_diagonal_sum} ?")
        
        if diagonal_element > off_diagonal_sum:
            print(f"  -> {diagonal_element} > {off_diagonal_sum} (✔️ Benar)")
        else:
            print(f"  -> {diagonal_element} <= {off_diagonal_sum} (❌ Salah)")
            is_diagonally_dominant = False # Jika satu baris gagal, seluruh sistem gagal
            
    return is_diagonally_dominant

# --- Program Utama ---

# Definisikan matriks koefisien A dari sistem persamaan:
# 4x - y + z = 7
#  x + 3y - z = 4
#  x - y + 5z = 6
A = np.array([
    [4, -1, 1],
    [1, 3, -1],
    [1, -1, 5]
])

print("="*55)
print("  PROGRAM PENGECEKAN KONVERGENSI SISTEM PERSAMAAN LINEAR")
print("="*55)
print("Matriks Koefisien (A):\n", A, "\n")

# Panggil fungsi untuk mengecek dan simpan hasilnya
hasil_konvergensi = cek_konvergensi(A)

# Cetak kesimpulan akhir
print("\n" + "-"*20 + " KESIMPULAN " + "-"*20)
if hasil_konvergensi:
    print("✔️ Ya, sistem ini DIJAMIN KONVERGEN.")
    print("   Karena matriksnya 'Strictly Diagonally Dominant'.")
else:
    print("❌ Tidak, konvergensi sistem ini TIDAK DIJAMIN oleh syarat ini.")
print("="*55)