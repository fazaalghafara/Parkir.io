import serial
import mysql.connector
from datetime import datetime

# 1. KONEKSI DATABASE
db = mysql.connector.connect(
    host="localhost", user="root", password="", database="db_parkir"
)
cursor = db.cursor()

# 2. SETTING PORT USB ESP32 KAMU (Cek di Arduino IDE kamu COM berapa, misal COM4)
# sesuaikan 'COM4' dengan port yang terbaca di laptopmu
ser = serial.Serial('COM4', 115200, timeout=1)

print(">>> Python Bridge Ready, Menunggu Tap Kartu RFID dari Pintu Keluar...")

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        
        # Cek apakah data yang masuk mengandung kode RFID KELUAR
        if line.startswith("RFID_KELUAR:"):
            uid = line.split(":")[1]
            waktu_sekarang = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            lokasi = "Parkir A"
            
            print(f"\n>>> [TAP KARTU] Terdeteksi UID: {uid} pada {waktu_sekarang}")
            
            try:
                # A. Input Log Keluar
                query_log = "INSERT INTO log_parkir (waktu, tipe_kendaraan, track_id, lokasi, status) VALUES (%s, 'RFID_Card', %s, %s, 'KELUAR')"
                cursor.execute(query_log, (waktu_sekarang, uid, lokasi))
                
                # B. Kurangi Slot Terisi (-1)
                query_update = "UPDATE status_parkir SET slot_terisi = slot_terisi - 1 WHERE lokasi = %s AND slot_terisi > 0"
                cursor.execute(query_update, (lokasi,))
                
                db.commit()
                print(">>> [SUCCESS] Database berhasil diperbarui (-1 Slot)!")
            except Exception as e:
                print(f">>> [ERROR] Gagal update database: {e}")