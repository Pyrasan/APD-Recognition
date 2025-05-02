import cv2
import face_recognition
import pickle
import os

# Path folder untuk menyimpan data wajah dan file encoding
FOLDER_PATH = 'Wajah'
ENCODE_FILE = 'EncodeFile.p'

# Pastikan folder ada
if not os.path.exists(FOLDER_PATH):
    os.makedirs(FOLDER_PATH)

# Load daftar gambar dari folder
pathList = os.listdir(FOLDER_PATH)
imgList = []
knownIds = []

for path in pathList:
    imgList.append(cv2.imread(os.path.join(FOLDER_PATH, path)))

    # Menggunakan nama file sebagai ID - Nama
    id_name = os.path.splitext(path)[0]  # Menghapus ekstensi file
    knownIds.append(id_name)  # Simpan dalam format "01 - Bob"

# Fungsi untuk melakukan encoding wajah
def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)
        if encode:
            encodeList.append(encode[0])
    return encodeList

print('Encoding Start...')
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, knownIds]
print('Encoding Complete')

# Simpan hasil encoding ke file pickle
with open(ENCODE_FILE, 'wb') as file:
    pickle.dump(encodeListKnownWithIds, file)

print(f'File Saved: {ENCODE_FILE}')
