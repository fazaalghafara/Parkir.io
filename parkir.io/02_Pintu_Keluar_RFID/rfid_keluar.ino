#include "soc/soc.h"           // Untuk matikan Brownout
#include "soc/rtc_cntl_reg.h"  // Untuk matikan Brownout
#include <WiFi.h>
#include <HTTPClient.h>
#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN    21  // SDA di D21
#define RST_PIN   22  // RST di D22

MFRC522 mfrc522(SS_PIN, RST_PIN);

// Sesuaikan dengan nama baru yang tanpa spasi tadi
const char *ssid = "DESKTOP-E07CSGF 7255";
const char *password = "6#52o2V2";

// Gateway XAMPP Mobile Hotspot Laptop
const char* serverUrl = "http://192.168.1.7/db_parkir_api/keluar.php"; 

void setup() {
  // 1. Matikan detektor brownout di baris paling pertama
  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0); 
  
  Serial.begin(115200);
  delay(1000); 
  
  Serial.println("\n=================================");
  Serial.println("SISTEM PINTU KELUAR RFID START");
  Serial.println("=================================");
  
  // 2. LOGIKA DIURUTKAN: KONEKSI WI-FI DULUAN SEBELUM SENSOR AKTIF
  WiFi.mode(WIFI_STA);
  WiFi.disconnect(); 
  delay(500);
  
  Serial.print("Menghubungkan ke Wi-Fi: ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  
  // Tunggu koneksi Wi-Fi berhasil
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("\n>>> [SUCCESS] ESP32 Terhubung ke Wi-Fi!");
  Serial.print(">>> IP Address: ");
  Serial.println(WiFi.localIP());
  
  // 3. SETELAH WI-FI AMAN, BARU NYALAKAN HARDWARE SPI DAN RFID
  Serial.println(">>> Mengaktifkan Sensor RFID RC522...");
  SPI.begin();
  mfrc522.PCD_Init(); 
  Serial.println(">>> [READY] Sistem Siap Digunakan. Silakan Tempel Kartu.");
}

void loop() {
  // Cek apakah ada kartu RFID baru
  if ( ! mfrc522.PICC_IsNewCardPresent()) return;
  if ( ! mfrc522.PICC_ReadCardSerial()) return;

  // Membaca UID dari kartu RFID
  String uidString = "";
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    uidString += String(mfrc522.uid.uidByte[i] < 0x10 ? "0" : "");
    uidString += String(mfrc522.uid.uidByte[i], HEX);
  }
  uidString.toUpperCase();
  Serial.println("\n>>> Kartu Terdeteksi! UID: " + uidString);

  // Kirim data ke Laptop via HTTP POST
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/x-www-form-urlencoded");
    
    String httpRequestData = "uid=" + uidString + "&lokasi=Parkir A";
    
    Serial.println(">>> Mengirim data keluar ke database...");
    int httpResponseCode = http.POST(httpRequestData);
    
    if (httpResponseCode > 0) {
      Serial.print(">>> [SUCCESS] Respon Server XAMPP: ");
      Serial.println(httpResponseCode);
    } else {
      Serial.print(">>> [ERROR] Gagal kirim ke database. Code: ");
      Serial.println(httpResponseCode);
    }
    http.end();
  } else {
    Serial.println(">>> [WARNING] Wi-Fi Terputus!");
  }
  
  mfrc522.PICC_HaltA();
  delay(2000); 
}