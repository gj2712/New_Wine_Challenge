import cv2
import numpy as np
import glob
import random
import os

# Load Yolo
net = cv2.dnn.readNet("yolov3_custom_last.weights", "yolov3_custom.cfg")
classes = ['Grapes']

images_path=glob.glob(r"C:\Users\garvi_jain\Documents\PycharmProjects\New_Wine\test_data\*.jpg")


layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

random.shuffle(images_path)

# Defining the path where output images will be saved

path_out=r"C:\Users\garvi_jain\Documents\PycharmProjects\New_Wine\Predictions"

# Loading image

c=1

for img_path in images_path:

    img = cv2.imread(img_path)

    img = cv2.resize(img, None, fx=0.4, fy=0.4)

    height, width, channels = img.shape

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
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                # Rectangle coordinates
                x = int(center_x - w / 2)
                
                y = int(center_y - h / 2)

                cv2.rectangle(img, (x, y), (x + w, y + h),(0,255,0), 2)
                boxes.append([x, y, w, h])
                # confidences.append(float(confidence))
                # class_ids.append(class_id)

    print("No. of Grapes detected in this figure is : ",len(boxes))

    ims = cv2.resize(img, (960, 540))
    cv2.imshow("Image", ims)
    cv2.waitKey(0)

    path_new = os.path.join(path_out,str(c)+'.jpg')
    cv2.imwrite(path_new, img)  # save the image
    c=c+1

cv2.destroyAllWindows()