import time
import RPi.GPIO as GPIO
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np
import glob
import random

# initialize the camera
camera = PiCamera()
camera.resolution = (640,480)
camera.framerate = 60
rawCapture = PiRGBArray(camera,size = (640,480))
firstFrame = None
time.sleep(2)

# Load Yolo
net = cv2.dnn.readNet("yolov3_custom_last.weights", "yolov3_custom.cfg")

# Name custom object
classes = ["Pothole"]

# Images path
images_path = glob.glob(r"/home/pi/Desktop/positive/pothole1.jpg")



layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

# loop through all the images
for f in camera.capture_continuous(rawCapture , format= "rgb" ,use_video_port=True):
    # Loading image
    img = f.array
    img = cv2.resize(img, None, fx=0.4, fy=0.4)
    height, width, channels = img.shape
    #cv2.imshow("camera",img)
    # Detecting objects
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

    net.setInput(blob)
    outs = net.forward(output_layers)

    # Showing informations on the screen
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.3:
                # Object detected
                print(class_id)
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    print(indexes)
    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = colors[class_ids[i]]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, label, (x, y + 30), font, 3, color, 2)


    cv2.imshow("Image", img)
    key = cv2.waitKey(0)

cv2.destroyAllWindows()
