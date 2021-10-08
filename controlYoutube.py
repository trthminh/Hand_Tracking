import cv2
import HandTrackingModule as htm
import time
import pyautogui

# pyautogui.hotkey('space', 'enter')
# Cuộn xuống để tìm bài mới: (x=1358, y=185)
# bài ở vị trí đầu tiên: (x=918, y=452)

x_pause, y_pause = (127, 570)
x_mute, y_mute = (214, 569)
x_move, y_move = (171, 565)
x_adver, y_adver = (779, 484)

print(pyautogui.position())
cap = cv2.VideoCapture(0)
detector = htm.handDetector()


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)

    cv2.rectangle(img, (0, 0), (200, 480), (255, 0, 0), 3)

    lmList, _ = detector.findPosition(img, draw=False)
    finger_up = detector.fingersUp()
    num_finger_up = finger_up.count(1)
    no_process = 0

    if len(lmList) != 0:
        for id in range(0, 21):
            if lmList[id][1] < 0 or lmList[id][1] > 200 or lmList[id][2] < 0 or lmList[id][2] > 480:
                no_process = 1
                break
    cv2.putText(img, "** This way just True in case small screen", (201, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
    cv2.putText(img, "* 1 fingersUp that Pause/Continue", (201, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
    cv2.putText(img, "* 2 fingersUp that Release", (201, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
    cv2.putText(img, "* 3 fingersUp that Toward", (201, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
    cv2.putText(img, "* 4 fingersUp that Move to other video", (201, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
    cv2.putText(img, "* 5 fingersUp that Mute/UnMute", (201, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
    cv2.putText(img, "* thumb and index fingersUp that skip ad", (201, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)

    if no_process == 0:
        if len(finger_up) != 0:
            # Pause / Continue
            if num_finger_up == 1:
                pyautogui.click(x_pause, y_pause)

            # Mute
            if num_finger_up == 5:
                pyautogui.click(x_mute, y_mute)
            # Toward
            if num_finger_up == 3:
                pyautogui.hotkey('right')

            if num_finger_up == 2:
                # Skip ad
                if finger_up[0] == 1 and finger_up[1] == 1:
                    pyautogui.click(x_adver, y_adver)
                # Release
                else: pyautogui.hotkey('left')

            # Move to other video
            if num_finger_up == 4:
                pyautogui.click(x_move, y_move)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break
    cv2.waitKey(1)
    cv2.imshow("Image", img)
