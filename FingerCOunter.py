import cv2
import os
import time
import HandTrackingModule as htm

wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

folderPath = "image"
myList = os.listdir(folderPath)
# print(myList)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    img_1 = cv2.resize(image, (200, 200))
    overlayList.append(img_1)

detector = htm.handDetector(detectionCon=0.75)

tipIds = [4, 8, 12, 16, 20]

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img, draw=False)
    if len(lmList) > 0:
        fingers = []
        if lmList[4][1] > lmList[17][1]:
            # print("Left Hand")
            if lmList[4][1] < lmList[3][1]:
                fingers.append(1)
            else: fingers.append(0)
        else:
            # print("Right Hand")
            if lmList[4][1] > lmList[3][1]:
                fingers.append(1)
            else: fingers.append(0)

        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else: fingers.append(0)
        # print(fingers)
        total_Finger = fingers.count(1)
        print(total_Finger)

        h, w, c = overlayList[total_Finger - 1].shape
        img[0:200, 0:200] = overlayList[total_Finger - 1]
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
    cv2.waitKey(1)
