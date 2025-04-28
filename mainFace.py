import cv2
import pickle
import face_recognition
import numpy as np
import time

# Path file encoding wajah
ENCODE_FILE = 'EncodeFile.p'

# Load encode file
print('Loading Encode File...')
with open(ENCODE_FILE, 'rb') as file:
    encodeListKnownWithIds = pickle.load(file)

encodeListKnown, knownNames = encodeListKnownWithIds
print('Encode File Loaded')

# Inisialisasi kamera
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Variabel kontrol deteksi
detection_paused = False
resume_time = 0
pause_duration = 5  # dalam detik

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    # Cek apakah deteksi sedang dijeda
    if not detection_paused:
        faceCurFrame = face_recognition.face_locations(imgS)
        encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

        if encodeCurFrame:  # Jika ada wajah terdeteksi
            # Ambil hanya wajah pertama
            encodeFace = encodeCurFrame[0]
            faceLoc = faceCurFrame[0]

            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis) if faceDis.size > 0 else -1

            if matchIndex != -1 and matches[matchIndex]:
                name_with_id = knownNames[matchIndex]

                # Kalau wajah dikenali, baru gambar kotak dan tampilkan nama
                y1, x2, y2, x1 = [v * 4 for v in faceLoc]
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img, name_with_id, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

                print("Detected:", name_with_id)

                # Aktifkan jeda deteksi
                detection_paused = True
                resume_time = time.time() + pause_duration
            else:
                # Kalau tidak dikenali, tidak lakukan apa-apa
                pass
    else:
        # Tampilkan waktu jeda
        remaining = int(resume_time - time.time())
        if remaining > 0:
            cv2.putText(img, f"Tunggu {remaining}s...", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        # Cek apakah sudah waktunya mendeteksi lagi
        if time.time() >= resume_time:
            detection_paused = False

    cv2.imshow("Face Recognition", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
