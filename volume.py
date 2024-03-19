import cv2
import time
import numpy as np
import HandTracking as htm
from HandTracking import main
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# ----------------------------------------------------------------
wCam, hCam = 1280, 720
# -----------------------------------------------
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.5)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()

minVol = volRange[0]
maxVol = volRange[1]
# print(minVol)
# print(maxVol)
# Main loop for display
while True:
    success, img = cap.read()
    img = detector.findHands(img, draw=False)
    lmlist = detector.findPosition(img, draw=False)

    if len(lmlist) != 0:
        # x1, y1 = lmlist[4][1], lmlist[4][2]
        # x2, y2 = lmlist[8][1], lmlist[8][2]
        # x3, y3 = lmlist[16][1], lmlist[16][2]

        # cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        # cv2.circle(img, (x1, y1), 15, (255, 38, 173), cv2.FILLED)
        # cv2.circle(img, (x2, y2), 15, (255, 38, 173), cv2.FILLED)
        # cv2.circle(img, (x3, y3), 15, (255, 38, 173), cv2.FILLED)
        # cv2.line(img, (x1, y1), (x2, y2), (255, 255, 36), 3)
        # cv2.circle(img, (cx, cy), 15, (255, 38, 173), cv2.FILLED)

        # length = math.hypot(x2 - x1, y2 - y1)
        # length2 = math.hypot(x3 - x1, y3 - y1)
        coordinates = []
        length, img, coordinates, length2 = detector.findDistance(4, 8, img)
        # print(length)
        # if length <= 50:
        #     cv2.circle(img, (cx, cy), 15, (0, 2, 0), cv2.FILLED)

        # hand range = 50 -300
        # volume range = -65 - 0
        vol = np.interp(length, [100, 300], [minVol, maxVol])
        # per = maxVol - minVol / 100
        volu = round(vol / 4.8) * 4.8
        # print(vol)
        print(volu)
        volume.SetMasterVolumeLevel(volu, None)

        # if length2 <= 20:
        #     break

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(
        img, str(int(fps)), (50, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 25, 50), 3
    )

    # cv2.imshow("Img", img)
    cv2.waitKey(1)
