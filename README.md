Parkir.io

Repositori ini berisi dokumentasi dan kode sumber lengkap untuk proyek tugas akhir **Sistem Monitoring Slot Parkir Pintar**. Sistem ini menggunakan pendekatan hibrida untuk mengelola alur masuk dan keluar kendaraan secara *real-time*, mengintegrasikan teknologi *Computer Vision* dan *RFID*.

---

## 🛠️ Arsitektur Sistem

Sistem ini terdiri dari dua sub-sistem utama yang berjalan secara independen namun terhubung ke basis data MySQL pusat:

### 1. Sub-Sistem Pintu Masuk (Computer Vision)
- **Perangkat:** ESP32-CAM.
- **Teknologi:** Streaming IP Kamera & Python (OpenCV).
- **Alur:** ESP32-CAM melakukan streaming video ke server (laptop) via Wi-Fi. Skrip `deteksi.py` di server memproses video tersebut untuk mendeteksi kendaraan menggunakan model YOLOv8. Saat kendaraan terdeteksi masuk, skrip akan meng-update database MySQL untuk **menambah jumlah slot terisi (+1)** dan mencatat log masuk.

### 2. Sub-Sistem Pintu Keluar (RFID)
- **Perangkat:** ESP32 DevKit V1 + Modul RFID MFRC522.
- **Teknologi:** Komunikasi Serial (USB) & Python (PySerial).
- **Alur:** Karena kendala stabilitas Wi-Fi pada unit ESP32 pintu keluar, sistem menggunakan komunikasi serial USB. ESP32 membaca UID kartu RFID dan mengirimkannya lewat kabel USB. Skrip `baca_rfid.py` di server membaca data serial tersebut, memvalidasi kartu, mencatat log keluar, dan meng-update database untuk **mengurangi jumlah slot terisi (-1)**.

---

## 📂 Struktur Repositori & Penjelasan File

### Folder: `01_Pintu_Masuk_Kamera`
- **`deteksi.py`**: Skrip utama Python yang melakukan *capture* stream dari ESP32-CAM, menjalankan logika deteksi objek (kendaraan), dan melakukan query `INSERT`/`UPDATE` ke MySQL saat kendaraan masuk.
- *(Opsional)* `haarcascade_car.xml`: File model yang digunakan oleh OpenCV di dalam `deteksi.py`.

### Folder: `02_Pintu_Keluar_RFID`
- **`rfid_keluar.ino`**: Kode *firmware* (Arduino C++) untuk ESP32 pintu keluar. Fungsinya murni untuk inisialisasi modul RFID dan melakukan `Serial.println()` berisi UID kartu saat terdeteksi.
- **`baca_rfid.py`**: Skrip Python "bridge" yang mendengarkan (*listen*) port serial USB, menangkap UID yang dikirim ESP32, dan menjalankan query MySQL untuk proses keluar.

### File: `db_parkir.sql`
- File SQL untuk mempermudah replikasi struktur tabel database (`log_parkir` dan `status_parkir`) yang dibutuhkan sistem.

---

## 🔧 Panduan Instalasi & Cara Menjalankan

### Persyaratan Awal (Prerequisites)
1.  **Hardware:** ESP32-CAM, ESP32 DevKit V1, Modul RFID RC522.
2.  **Software:** XAMPP (Apache & MySQL), Python (v3.9 ke atas), Arduino IDE.
3.  **Library Python:**
    ```bash
    pip install opencv-python mysql-connector-python pyserial numpy
    ```

### Langkah-langkah:

1.  **Setup Database:** Impor file `db_parkir.sql` ke phpMyAdmin. Pastikan tabel `status_parkir` sudah berisi nilai kapasitas maksimum.
2.  **Konfigurasi Pintu Keluar (RFID):**
    - Upload `rfid_keluar.ino` ke ESP32.
    - Rakit RFID RC522 ke ESP32 sesuai pinout di kode `.ino`.
    - Colok ESP32 ke USB laptop. Pastikan port COM sesuai di `baca_rfid.py`.
3.  **Konfigurasi Pintu Masuk (Kamera):**
    - Upload firmware kamera ke ESP32-CAM (konfigurasi SSID & Password Wi-Fi).
    - Ambil IP Address kamera dan paste ke variabel di `deteksi.py`.

### Cara Menjalankan Saat Demo:

1.  Jalankan XAMPP.
2.  Buka terminal/command prompt pertama, jalankan script kamera masuk:
    ```bash
    cd 01_Pintu_Masuk_Kamera
    python deteksi.py
    ```
3.  Buka terminal/command prompt kedua, jalankan script RFID keluar:
    ```bash
    cd 02_Pintu_Keluar_RFID
    python baca_rfid.py
    ```

Sistem sekarang siap memantau slot parkir secara *real-time* dari kedua sisi.

---

## 📌 Catatan Akhir & Analisis Integrasi (PENTING)

Arsip ini mendokumentasikan bagaimana integrasi sistem parkir *real-time* dapat dicapai bahkan dengan kendala hardware. Penggunaan Python sebagai "jembatan" pusat (menerima input dari kamera dan serial USB) memungkinkan sistem yang berbeda teknologi dapat berkomunikasi dan memperbarui satu *database* MySQL yang sama secara sinkron. Ini adalah contoh Information Architecture (IA) yang fleksibel untuk proyek IoT.
