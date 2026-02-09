# Install dulu library yang dibutuhkan:
# pip install mediapipe opencv-python --upgrade --user

import cv2
import mediapipe as mp
import numpy as np
from scipy.spatial import distance as dist
import time

# --- 1. SETUP MEDIAPIPE ---
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Indeks Mata (MediaPipe)
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

# --- 2. FUNGSI HITUNG EAR ---
def calculate_ear(eye_landmarks, w, h):
    coords = []
    for landmark in eye_landmarks:
        coords.append((int(landmark.x * w), int(landmark.y * h)))

    # Jarak Vertikal
    A = dist.euclidean(coords[1], coords[5])
    B = dist.euclidean(coords[2], coords[4])
    # Jarak Horizontal
    C = dist.euclidean(coords[0], coords[3])

    # Rumus EAR
    ear = (A + B) / (2.0 * C)
    return ear

# --- 3. KONFIGURASI PENTING ---
# Batas mata dianggap tertutup (semakin kecil, semakin harus merem rapat)
EAR_THRESHOLD = 0.25 

# BERAPA LAMA HARUS MEREM? (Sensitivitas Waktu)
# Asumsi kamera berjalan 30 FPS. 
# Jika 15 Frame = berarti harus merem 0.5 detik baru alarm bunyi.
# Kalau masih sering salah deteksi kedip, NAIKKAN angka ini jadi 20 atau 30.
CLOSED_FRAMES_THRESHOLD = 15 

# Variabel penghitung (Counter)
blink_counter = 0
alarm_on = False

# --- 4. BUKA KAMERA ---
cap = cv2.VideoCapture(0)

print("Sistem Berjalan... Tekan 'Q' untuk keluar.")

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Kamera tidak ditemukan!")
        break

    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    h, w, _ = image.shape
    
    # Default status
    status = "Aman (Melek)"
    color = (0, 255, 0) # Hijau

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            left_lm = [face_landmarks.landmark[i] for i in LEFT_EYE]
            right_lm = [face_landmarks.landmark[i] for i in RIGHT_EYE]

            leftEAR = calculate_ear(left_lm, w, h)
            rightEAR = calculate_ear(right_lm, w, h)
            avgEAR = (leftEAR + rightEAR) / 2.0

            # --- LOGIKA COUNTER ---
            if avgEAR < EAR_THRESHOLD:
                # Jika mata tertutup, tambah counter
                blink_counter += 1
                
                # Jika counter melebihi batas, baru nyalakan ALARM
                if blink_counter >= CLOSED_FRAMES_THRESHOLD:
                    alarm_on = True
                    status = "BAHAYA: MENGANTUK!"
                    color = (0, 0, 255) # Merah
                    cv2.rectangle(image, (0,0), (w, h), (0, 0, 255), 10)
            
            else:
                # Jika mata terbuka, RESET counter ke 0
                blink_counter = 0
                alarm_on = False

            # Tampilkan data debug di layar
            cv2.putText(image, f"EAR: {avgEAR:.2f}", (30, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(image, f"Frames Merem: {blink_counter}", (30, 60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    # Tampilkan Status
    cv2.putText(image, status, (50, 400), cv2.FONT_HERSHEY_SIMPLEX, 
                1.2, color, 3)

    cv2.imshow('Smart Fatigue Detector (Tekan Q Keluar)', image)

    key = cv2.waitKey(5) & 0xFF
    if key == ord('q') or key == 27:
        break

cap.release()
cv2.destroyAllWindows()