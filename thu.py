import cv2
import HandTrackingModule as htm

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
detector = htm.handDetector()

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    detector.findHands(img)
    lmList, _ = detector.findPosition(img, draw=False)
    cv2.rectangle(img, (0, 0), (300, 480), (255, 0, 0), 2)
    cv2.rectangle(img, (0, 0), (150, 240), (255, 0, 0), 2)
    cv2.rectangle(img, (0, 240), (150, 240), (255, 0, 0), 2)
    cv2.rectangle(img, (150, 0), (300, 240), (255, 0, 0), 2)
    cv2.rectangle(img, (150, 240), (300, 480), (255, 0, 0), 2)
    # cx, cy = 150, 240
    if len(lmList) != 0:
        xmid, ymid = (lmList[0][1] + lmList[9][1])//2, (lmList[0][2] + lmList[9][2])//2
        # cv2.circle(img, (xmid, ymid), 5, (0, 0, 255), cv2.FILLED)


    if cv2.waitKey(1) & 0xff == ord('q'):
        break
    cv2.waitKey(1)
    cv2.imshow("Image", img)