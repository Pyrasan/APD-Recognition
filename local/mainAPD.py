import cv2
import cvzone
import math
import numpy as np
from ultralytics import YOLO

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

model = YOLO("tes2.pt")

classNames = ["Helm", "Safety Boots", "Rompi", "Sarung Tangan"]

while True:
    success, img = cap.read()
    results = model(img, stream=True)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            conf = box.conf[0]
            if conf > 0.78:  # Hanya proses kalau confidence di atas nilai tersebut
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                w, h = x2 - x1, y2 - y1
                cvzone.cornerRect(img, (x1, y1, w, h))
                conf = math.ceil((conf * 100)) / 100
                cls = int(box.cls[0])

                # Tampilkan di terminal juga hanya kalau conf di atas nilai yang ditentukan
                print(f'Detected {classNames[cls]} with confidence {conf}')

                cvzone.putTextRect(img, f'{classNames[cls]} {conf}', (max(0, x1), max(35, y1)), scale=1, thickness=1)
    
    cv2.imshow("image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
