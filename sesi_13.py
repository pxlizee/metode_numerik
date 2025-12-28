def hitung_pendinginan_euler():
    #parameter awal
    T_ruangan = 25.0  # Suhu ruangan (konstan)
    k = 0.1           # Konstanta laju pendinginan
    T = 80.0          # Suhu awal benda T(0)
    h = 1             # Langkah waktu (step size)
    target_waktu = 3  # Waktu akhir yang dicari (t = 3)
    
    t = 0 # Waktu saat ini

    print("--- Hasil Perhitungan Metode Euler ---")
    print(f"Saat t = {t}, Suhu (T) = {T:.4f} °C (Kondisi Awal)")

    # 2. Loop Iterasi
    while t < target_waktu:
        # Menghitung gradien (dT/dt) berdasarkan persamaan diferensial:
        # dT/dt = -k * (T - T_ruangan)
        gradien = -k * (T - T_ruangan)
        
        # Rumus Metode Euler: T_baru = T_lama + (h * gradien)
        T_baru = T + (h * gradien)
        
        # Update nilai T dan t untuk iterasi berikutnya
        T = T_baru
        t += h # Menambah waktu sebesar h (1 detik)
        
        print(f"Saat t = {t}, Suhu (T) = {T:.4f} °C")

if __name__ == "__main__":
    hitung_pendinginan_euler()