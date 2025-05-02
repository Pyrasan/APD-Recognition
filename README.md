# APD-Recognition

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

Note: Recommended to use Virtual Environment to avoid issues with another Python version

---------------------------------------------------------------------------------

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
    
    path: ../drive/MyDrive/(your drive path)
    
    train: ../train/images
    
    val: ../valid/images
    
    test: ../test/images

    nc: n `(n=number of classes)`
    
    names: ['(your labels seperate with coma)']
13. Upload the 3 folders to GDrive
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
