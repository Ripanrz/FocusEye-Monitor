# 👁️ FocusEye-Monitor

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green?style=for-the-badge&logo=opencv&logoColor=white)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Face%20Mesh-orange?style=for-the-badge)

**FocusEye-Monitor** adalah sistem deteksi kelelahan dan kantuk (*drowsiness detection*) berbasis Computer Vision yang berjalan secara *real-time*.

Sistem ini dirancang untuk memantau tingkat kewaspadaan pengemudi atau pekerja dengan menganalisis pola kedipan mata menggunakan algoritma **Eye Aspect Ratio (EAR)**. Dilengkapi dengan fitur *Anti-False-Alarm*, sistem ini dapat membedakan antara kedipan normal dan tanda-tanda microsleep.

## 🚀 Fitur Unggulan

* **Real-Time Monitoring:** Deteksi wajah dan mata tanpa delay menggunakan webcam laptop standar.
* **Smart EAR Calculation:** Menggunakan perhitungan geometri Euclidean untuk akurasi tinggi.
* **Intelligent Blink Filter:** Sistem **tidak reaktif** terhadap kedipan biasa. Alarm hanya akan berbunyi jika mata tertutup melebihi durasi waktu tertentu (microsleep).
* **Visual Alert System:** Memberikan peringatan visual (Bingkai Merah & Status Teks) saat bahaya terdeteksi.
* **Privacy Focused:** Semua pemrosesan data dilakukan secara lokal (On-Device), tidak ada video yang dikirim ke server cloud.

## 🛠️ Teknologi yang Digunakan

* **Python 3.12**: Bahasa pemrograman utama.
* **OpenCV (`cv2`)**: Pustaka pengolahan citra untuk akses kamera dan visualisasi frame.
* **MediaPipe Face Mesh**: Model Deep Learning Google untuk memetakan 468 titik landmark wajah secara presisi.
* **SciPy & NumPy**: Untuk komputasi matematika dan aljabar linear (menghitung jarak titik mata).

## ⚙️ Cara Instalasi & Menjalankan

Pastikan Python sudah terinstal di komputer Anda.

1.  **Clone repository ini:**
    ```bash
    git clone [https://github.com/Ripanrz/FocusEye-Monitor.git](https://github.com/Ripanrz/FocusEye-Monitor.git)
    cd FocusEye-Monitor
    ```

2.  **Install library yang dibutuhkan:**
    Gunakan perintah pip berikut di terminal:
    ```bash
    pip install mediapipe opencv-python scipy numpy
    atau
    pip install mediapipe opencv-python --upgrade --user
    ```

3.  **Jalankan aplikasi:**
    ```bash
    python FocusEye-Monitor.py
    ```

4.  **Cara Keluar:**
    Tekan tombol `Q` atau `Esc` pada keyboard untuk menghentikan program.

## 🧠 Cara Kerja Algoritma (EAR)

Sistem ini bekerja dengan memetakan 6 titik koordinat (landmark) pada setiap mata manusia.



Rumus **Eye Aspect Ratio (EAR)** digunakan untuk menghitung rasio pembukaan mata:
* **EAR Tinggi (> 0.25):** Mata terbuka lebar (Sadar/Fokus).
* **EAR Rendah (< 0.25):** Mata tertutup atau menyipit (Mengantuk).

**Logika Counter (Anti-Baper):**
Sistem menggunakan *frame counter*. Jika EAR terdeteksi rendah, sistem tidak langsung membunyikan alarm, melainkan mulai menghitung. Jika kondisi mata tertutup bertahan selama **15 frame berturut-turut** (setara ±0.5 detik), barulah status berubah menjadi **"BAHAYA: MENGANTUK!"**.

## 🤝 Kontribusi & Pengembangan

Proyek ini dikembangkan sebagai bagian dari eksplorasi Data Science dan Computer Vision.

Ide pengembangan masa depan:
- [ ] Menambahkan alarm suara (Beep sound).
- [ ] Integrasi dengan IoT untuk mematikan mesin jika pengemudi tertidur.
- [ ] Analisis *Yawn Detection* (Deteksi Menguap).

---
