import cv2
import mediapipe as mp
import time
import numpy as np
import math
import HandTracking as htm
import autopy

# ----------------------------------------------------------------
wCam, hCam = 1280, 720
# -----------------------------------------------
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector()

while True:
    success, img = cap.read()
    img = detector.findHands(img, draw=False)
    lmlist = detector.findPosition(img, draw=False)
    # 2 get the tip of middle and index
    if len(lmlist) != 0:
        x1, y1 = lmlist[8][1:]
        x2, y2 = lmlist[12][1:]

    # 3 check which fing are up
    fingers = detector.fingersUp()
    # cv2.rectangle(
    #     img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2
    # )

    # 4 only index finger : Move mouse
    if fingers[1] == 1 and fingers[2] == 0:
        # 5 Convert Coordinates
        x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
        y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
        # 6 Smothen values
        clocX = plocX + (x3 - plocX) / smoothening
        clocY = plocY + (y3 - plocY) / smoothening
        # 7 move mouse
        autopy.mouse.move(wScr - clocX, clocY)
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        plocX, plocY = clocX, clocY

    # 8 Both index and middle are up: click
    if fingers[1] == 1 and fingers[2] == 1:
        # 9 Find distance btw fingers
        length, img, lineInfo = detector.findDistance(8, 12, img)
        print(length)
        # 10 Click mouse if Distance is less
        if length < 40:
            cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
            autopy.mouse.click()

    # 11 frame rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(
        img, str(int(fps)), (50, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 25, 50), 3
    )
    # 12 display
    cv2.imshow("Img", img)
    cv2.waitKey(1)
