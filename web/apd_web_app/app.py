import os
import cv2
import numpy as np
import re
import pickle
from flask import Flask, render_template, request, url_for
from datetime import datetime
from ultralytics import YOLO
import cvzone
import face_recognition
import openpyxl

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join('static', 'detected_images')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load face encoding
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENCODE_FILE = os.path.join(BASE_DIR, 'EncodeFile.p')

with open(ENCODE_FILE, 'rb') as f:
    encodeListKnown, knownNames = pickle.load(f)

# Load YOLO models untuk masing-masing APD
model_helm = YOLO(os.path.join(BASE_DIR, 'helm.pt'))
model_rompi = YOLO(os.path.join(BASE_DIR, 'rompi.pt'))
model_sepatu = YOLO(os.path.join(BASE_DIR, 'sepatu.pt'))
model_sarungtangan = YOLO(os.path.join(BASE_DIR, 'sarungtangan.pt'))

model_info = [
    (model_helm, "Helm"),
    (model_rompi, "Rompi"),
    (model_sepatu, "Safety Boots"),
    (model_sarungtangan, "Sarung Tangan")
]

# --- Helper Functions ---
def clean_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

def generate_image_filename(name, ext='.jpg'):
    safe_name = clean_filename(name)
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    return f"{safe_name}_{timestamp}{ext}"

def detect_face_from_image(img):
    if img is None:
        print("Gambar tidak valid.")
        return None

    if img.shape[-1] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    imgS = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faces = face_recognition.face_locations(imgS)
    encodings = face_recognition.face_encodings(imgS, faces)

    if encodings:
        encodeFace = encodings[0]
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            return knownNames[matchIndex]
    return None

def detect_apd_from_image(img):
    detected_items = set()
    for model, label in model_info:
        results = model(img, stream=True)
        for r in results:
            for box in r.boxes:
                conf = box.conf[0]
                if conf > 0.65:
                    detected_items.add(label)
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    w, h = x2 - x1, y2 - y1
                    cvzone.cornerRect(img, (x1, y1, w, h))
                    label_text = f'{label} {conf:.2f}'
                    cvzone.putTextRect(img, label_text, (x1, max(35, y1)), scale=2, thickness=2)
    return detected_items

def setup_excel():
    folder = 'laporan'
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, 'DataPekerja.xlsx')
    if not os.path.exists(filepath):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = 'Log Deteksi'
        ws.append(['Nama', 'Status Kerja', 'Waktu Deteksi', 'APD Terdeteksi', 'Nama File Gambar'])
        wb.save(filepath)
    return filepath

def log_to_excel(name, status, apd_list, filename):
    filepath = setup_excel()
    wb = openpyxl.load_workbook(filepath)
    ws = wb.active
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    apd_str = ', '.join(apd_list)
    ws.append([name, status, now, apd_str, filename])
    wb.save(filepath)
    wb.close()

# --- Routes ---
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'confirm' in request.form:
            name = request.form['name']
            status = request.form['status']
            apd = request.form.get('apd', '')
            filename = request.form.get('filename', '')
            apd_list = apd.split(', ') if apd else []
            log_to_excel(name, status, apd_list, filename)
            return render_template('index.html', success="Data berhasil disimpan ke Excel!")

        file = request.files['image']
        if file:
            npimg = np.frombuffer(file.read(), np.uint8)
            img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

            name = detect_face_from_image(img)
            if not name:
                return render_template('index.html', error='Wajah tidak dikenali.')

            detected_apd = detect_apd_from_image(img)
            filename = generate_image_filename(name)
            save_path = os.path.join(UPLOAD_FOLDER, filename)
            print("Menyimpan gambar ke:", save_path.replace("\\", "/"))
            success = cv2.imwrite(save_path, img)
            print("Berhasil simpan?", success)
            print("File ada setelah simpan?", os.path.exists(save_path))

            image_url = url_for('static', filename=f'detected_images/{filename}')
            status = 'Diizinkan' if len(detected_apd) == 4 else 'Tidak Diizinkan'

            return render_template('index.html', result={
                'name': name,
                'status': status,
                'apd': list(detected_apd),
                'filename': filename,
                'image_url': image_url
            })

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
