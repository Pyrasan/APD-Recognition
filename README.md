# Package Requirement

Package Requirement | local
1. OpenCV Python `pip install opencv-python`
2. CVZone `pip install cvzone`
3. ultralytics `pip install ultralytics`
4. tkinter `pip install tk`
5. PyExcel `pip install opnepyxl`
6. Face Recognition `pip install face_recognition`

All at once `pip install -r local_requirements.txt`

Package Requirement | web
1. Flask `pip install Flask`
2. OpenCV Python `pip install opencv-python`
3. Face Recognition `pip install face_recognition`
4. ultralytics `pip install ultralytics`
5. CVZone `pip install cvzone`
6. PyExcel `pip install openpyxl`

All at once `pip install -r web_requirements.txt`

PyInstaller `pip install pyinstaller` -> Creating .exe

Note: Recommended to use Virtual Environment to avoid issues with another Python version

---------------------------------------------------------------------------------

# Dataset Sample

All in Roboflow `https://universe.roboflow.com/search?q=ppe`

---------------------------------------------------------------------------------

# Dataset Training

Custom Dataset Training using Google Collab:
1. Download Image Labelling from github repository `https://github.com/HumanSignal/labelImg/releases/tag/v1.8.1` choose `windows_v1.8.1.zip`
2. Make 3 folders
   
   a. train
   
   b. valid
   
   c. test
   
   With each of folders contains `images` and `labels` folders
4. Place images that want to be labelled to all 3 folders in `images` folder
5. Open Image Labelling program
6. Open directory to the images
7. Create label from the images
8. Save labels to `labels` folder
9. Create `data.yaml`
10. Write
    
    path: ../drive/MyDrive/(your drive folder path)
    
    train: ../train/images
    
    val: ../valid/images
    
    test: ../test/images

    nc: n `(n=number of classes)`
    
    names: ['(label1)', 'label2', 'etc.']
13. Upload the 3 folders with `data.yaml` to GDrive
14. Open Google Collab
15. Mount GDrive to Google Collab

    or run this code

    `from google.colab import drive`
    
    `drive.mount('/content/drive')`
17. Write 5 lines of program and run one by one
    
    a. `!nvidia-smi` | to check we use graphics card or not
    
    b. `!pip install ultralytics` | install ultraltics library
    
    c. `from ultralytics import YOLO` | import the library
    
    d. `!yolo task=detect mode=predict model=yolov8l.pt conf=0.25 source='online images url'` | for testing
    
    e. `!yolo task=detect mode=train model=yolov8l.pt data=../content/drive/MyDrive/(path to data.yaml) epochs=50 imgsz=640` | Training dataset and creating weights for YOLOv8
18. Write the code and put the weights `best.apt` to the folder

*Note: If download Dataset from outside, skip to step 9

Ready to use `https://colab.research.google.com/drive/1ZeY2375iUu71WsEt9b4CZc5W0yHH6qcQ?usp=sharing#scrollTo=uAHhv_8ph4Er`

-------------------------------------------------------------

# YOLOv8 Weights Download

Ready to use `https://drive.google.com/drive/folders/1hr0uoZPzmqk5PSoxRONG0HotxXcK3Nus?usp=sharing` 

-------------------------------------------------------------

# APD Web

Directory
```
project-folder/
│
├── app.py
├── EncodeFile.p
├── helm.pt
├── rompi.pt
├── sepatu.pt
├── sarungtangan.pt
├── models/
│   └── shape_predictor_68_face_landmarks.dat
├── static/
│   └── detected_images/       <- Hasil deteksi disimpan di sini
├── laporan/                   <- File Excel akan disimpan/diupdate di sini
└── templates/
    └── index.html
```

---------------------------------------------------------------

# Building app.exe

shape_predictor model `http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2` to folder `models` under main folder

Create app.exe Command `pyinstaller --onefile --add-data "templates;templates" --add-data "static;static" --add-data "models;models" --add-data "EncodeFile.p;." --add-data "helm.pt;." --add-data "rompi.pt;." --add-data "sepatu.pt;." --add-data "sarungtangan.pt;." app.py
`
