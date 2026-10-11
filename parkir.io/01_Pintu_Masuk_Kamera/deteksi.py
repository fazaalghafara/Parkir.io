import cv2
from ultralytics import YOLO
from datetime import datetime
import mysql.connector
import requests
import numpy as np
import time

# =====================================================================
# 1. KONEKSI KE DATABASE MYSQL LOCAL (XAMPP)
# =====================================================================
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",          # Default XAMPP
        password="",          # Default XAMPP kosong
        database="db_parkir"
    )
    cursor = db.cursor()
    print(">>> [SUCCESS] Berhasil terhubung ke Database MySQL!")
except mysql.connector.Error as err:
    print(f">>> [ERROR] Gagal konek DB: {err}")
    print("Pastikan XAMPP (Apache & MySQL) sudah di-Start!")
    exit()

# =====================================================================
# 2. INITIALIZE YOLO & ESP32-CAM (HIGH-FPS SESSION MODE)
# =====================================================================
model = YOLO("yolov8n.pt")

# Jalur resmi snapshot untuk firmware OV3660 kamu
url_esp32 = "http://192.168.137.17/capture"  

# Penanda lokasi kamera aktif (Sesuai Arsitektur IA)
lokasi_kamera = "Parkir A" 

line_y = 120 # Posisi garis horizontal tepat di tengah layar QVGA (320x240)
track_history = {}
counted_ids = set()
counter_mobil = 0
counter_motor = 0

# Membuat session HTTP agar koneksi tetap terbuka terus (Mendongkrak FPS)
session = requests.Session()

print(f">>> Menghubungkan ke ESP32-CAM OV3660 [{lokasi_kamera}] via Mode Stream Cepat...")
print(">>> AI Siap. Tekan 'q' pada jendela video untuk keluar.")

while True:
    try:
        # Mengambil gambar snapshot dengan koneksi yang tetap terbuka (Persistent)
        response = session.get(url_esp32, timeout=5)
        
        if response.status_code == 200:
            arr = np.frombuffer(response.content, dtype=np.uint8)
            frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        else:
            continue
            
        if frame is None:
            continue
            
        # Kasih rem tipis banget (10ms) supaya laptop stabil tapi FPS tetap dapet kencang
        time.sleep(0.01)
        
    except Exception as e:
        print(f">>> [WARNING] Gagal mengambil frame dari ESP32-CAM: {e}")
        time.sleep(1) # Tunggu 1 detik sebelum mencoba menghubungkan ulang
        continue

    # =====================================================================
    # 3. PROSES DETEKSI YOLOv8 & PENGHITUNGAN GARIS
    # =====================================================================
    
    # classes=[2, 3, 5, 7] agar HANYA mendeteksi Mobil, Motor, Bus, dan Truk
    results = model.track(frame, persist=True, conf=0.3, classes=[2, 3, 5, 7])

    # Gambar Garis Batas Hitung (Warna Merah)
    cv2.line(frame, (0, line_y), (frame.shape[1], line_y), (0, 0, 255), 3)

    # Cek apakah ada kendaraan yang terdeteksi
    if results[0].boxes.id is not None:
        boxes = results[0].boxes.xyxy.int().cpu().tolist()
        track_ids = results[0].boxes.id.int().cpu().tolist()
        cls_ids = results[0].boxes.cls.int().cpu().tolist()
        
        for box, track_id, cls_id in zip(boxes, track_ids, cls_ids):
            x1, y1, x2, y2 = box
            
            # Hitung titik tengah kendaraan
            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)

            # Gambar titik hijau di tengah kendaraan
            cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

            # Mapping ID Kelas YOLO ke teks Bahasa Indonesia
            if cls_id == 2:
                tipe = "mobil"
            elif cls_id == 3:
                tipe = "motor"
            elif cls_id == 5:
                tipe = "bus"
            elif cls_id == 7:
                tipe = "truk"
            else:
                tipe = "kendaraan"

            # LOGIKA MELEWATI GARIS (Dari Atas ke Bawah)
            if track_id in track_history:
                prev_y = track_history[track_id]
                
                if prev_y < line_y <= cy and track_id not in counted_ids:
                    counted_ids.add(track_id)
                    
                    # Tambah counter lokal sesuai kategori
                    if tipe == "mobil":
                        counter_mobil += 1
                    elif tipe == "motor":
                        counter_motor += 1
                    
                    waktu_sekarang = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(f">>> BARU MASUK: {tipe} (ID: {track_id}) di {lokasi_kamera} pada {waktu_sekarang}")
                    
                    try:
                        # A. INPUT DATA KE LOG PARKIR (Status MASUK)
                        query_log = "INSERT INTO log_parkir (waktu, tipe_kendaraan, track_id, lokasi, status) VALUES (%s, %s, %s, %s, 'MASUK')"
                        cursor.execute(query_log, (waktu_sekarang, tipe, track_id, lokasi_kamera))
                        
                        # B. UPDATE SLOT TERISI DI DATABASE (+1)
                        query_update = "UPDATE status_parkir SET slot_terisi = slot_terisi + 1 WHERE lokasi = %s"
                        cursor.execute(query_update, (lokasi_kamera,))
                        
                        db.commit() 
                        print(">>> [DB UPDATE] Berhasil menambah slot kendaraan di database.")
                    except mysql.connector.Error as db_err:
                        print(f">>> [DB ERROR] Gagal update data: {db_err}")

            track_history[track_id] = cy

            # Gambar kotak bounding box dan teks label di layar
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{tipe} ID:{track_id}", (x1, y1 - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Tampilkan live counter di layar monitor
    cv2.putText(frame, f"LOKASI: {lokasi_kamera}", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    cv2.putText(frame, f"KENDARAAN MASUK (LIVE): {counter_mobil + counter_motor}", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Tampilkan live window
    cv2.imshow("Sistem Deteksi Parkir AI Real-Time (ESP32-CAM)", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

db.close()
cv2.destroyAllWindows()