# APD-Recognition

Steps
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
11. Upload the 3 folders to GDrive
12. Open Google Collab
13. Mount GDrive to Google Collab
14. Write 5 lines of program and run one by one
    
    a. `!nvidia-smi` | to check we use graphics card or not
    
    b. `!pip install ultralytics` | install ultraltics library
    
    c. `from ultralytics import YOLO` | import the library
    
    d. `!yolo task=detect mode=predict model=yolov8l.pt conf=0.25 source='online images url'` | for testing
    
    e. `!yolo task=detect mode=train model=yolov8l.pt data=../content/drive/MyDrive/(path to data.yaml) epochs=50 imgsz=640` | Training dataset and creating weights for YOLOv8
15. Write the code and put the weights `best.apt` to the folder
