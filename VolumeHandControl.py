import cv2
import mediapipe as mp
import time
import numpy as np
import HandTrackingModule as htm
import math

##############################
# Pycaw

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()

minVol = volRange[0]
maxVol = volRange[1]

#########################################


wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
cTime = 0
volBar = 350
volPer = 0

detector = htm.handDetector()

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img, draw = False)
    if len(lmList) != 0:
        # print(lmList[4], lmList[8])

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(img, (x1, y1), 10, (255, 255, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 255, 0), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 10, (255, 255, 0), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)
        # print(length)

        if length < 30:
            cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

        # Hand range 30 - 300
        # Volume range -65 - 0

        vol = np.interp(length, [30, 300], [minVol, maxVol])
        volPer = np.interp(length, [30, 300], [0, 100])
        volBar = np.interp(length, [30, 300], [350, 150])
        print(vol)
        volume.SetMasterVolumeLevel(vol, None)

    cv2.rectangle(img, (50, 150), (80, 350), (255, 0, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (80, 350), (255, 0, 0), cv2.FILLED)
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    # cv2.putText(img, "fps:" + str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
    cv2.putText(img, str(int(volPer)) + "%", (50, 400), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cv2.waitKey(1)