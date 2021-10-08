import cv2
import os

import numpy as np

import HandTrackingModule as htm
import time

brushThickness = 15
eraseThickness = 50

folderPath = "Header"
myList = os.listdir(folderPath)
overlayList = []

for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)

header = overlayList[0]

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = htm.handDetector(detectionCon=0.85)
drawColor = (255, 0, 0)

imgCavas = np.zeros((720, 1280, 3), np.uint8)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1) # flip 1 that follow x-axis, 0 that y-axis

    img = detector.findHands(img)

    lmList, bbox = detector.findPosition(img, draw=False)

    if len(lmList) != 0:

        # tip of index and middle finger
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        fingers = detector.fingersUp()
        print(fingers)

        if fingers[1] and fingers[2]:

            xp, yp = 0, 0

            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)
            print("Selection Mode")

            if y1 < 153:
                if x1 <= 320:
                    header = overlayList[0]
                    drawColor = (0, 0, 0)
                elif x1 <= 640:
                    header = overlayList[1]
                    drawColor = (255, 0, 0)
                elif x1 <= 960:
                    header = overlayList[2]
                    drawColor = (0, 0, 255)
                else:
                    header = overlayList[3]
                    drawColor = (0, 255, 0)

        if fingers[1] and fingers[2] == 0:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            print("Drawing Mode")
            if xp == 0 and yp == 0:
                xp, yp = x1, y2
            if drawColor == (0, 0, 0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraseThickness)
                cv2.line(imgCavas, (xp, yp), (x1, y1), drawColor, eraseThickness)
            else:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCavas, (xp, yp), (x1, y1), drawColor, brushThickness)
            xp, yp = x1, y1

    imgGray = cv2.cvtColor(imgCavas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCavas)



    img[0:152, 0:1280] = header

    img = cv2.addWeighted(img, 0.5, imgCavas, 0.5, 0)
    cv2.imshow("Image", img)
    # cv2.imshow("Canvas", imgCavas)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
    cv2.waitKey(1)
