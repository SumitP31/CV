import cv2
import mediapipe as mp
import time
import numpy as np
import math


class handDetector:
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            self.mode, self.maxHands, 1, self.detectionCon, self.trackCon
        )
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(
                        img, handLms, self.mpHands.HAND_CONNECTIONS
                    )
        return img

    def findPosition(self, img, handNo=0, draw=True):
        xlist = []
        ylist = []
        bbox = []
        self.lmlist = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print(id,lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id, cx, cy)
                xlist.append(cx)
                ylist.append(cy)
                self.lmlist.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (150, 255, 79), cv2.FILLED)

                xmin, xmax = min(xlist), max(xlist)
                ymin, ymax = min(ylist), max(ylist)
                bbox = xmin, ymin, xmax, ymax

                if draw:
                    cv2.rectangle(
                        img,
                        (xmin - 20, ymin - 20),
                        (xmax + 20, ymax + 20),
                        (0, 255, 0),
                        2,
                    )

        return self.lmlist

    # figers up
    def fingersUp(self):
        fingers = []
        # Thumb
        if self.lmlist[4][1] > self.lmlist[4 - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Fingers
        for id in (8, 12, 16, 20):
            if self.lmlist[id][2] < self.lmlist[id - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        # totalFingers = fingers.count(1)

        return fingers

    # find distance
    def findDistance(self, p1, p2, img, draw=True, r=15, t=3):
        x1, y1 = self.lmlist[p1][1:]
        x2, y2 = self.lmlist[p2][1:]
        x3, y3 = self.lmlist[16][1], self.lmlist[16][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.circle(img, (x1, y1), 15, (255, 38, 173), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 38, 173), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 36), 3)
            cv2.circle(img, (cx, cy), 15, (255, 38, 173), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)
        length2 = math.hypot(x3 - x1, y3 - y1)

        return length, img, [x1, x2, y1, y2], length2


# imgRGB =  cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# results = hands.process(imgRGB)

# if results.multi_hand_landmarks:
#     for handLms in results.multi_hand_landmarks:
#         for id, lm in enumerate(handLms.landmark):
#                 # print(id,lm)
#                 h, w, c = img.shape
#                 cx, cy = int(lm.x*w), int(lm.y*h)
#                 print(id, cx, cy)

#         mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

#     cTime = time.time()
#     fps = 1/(cTime-pTime)
#     pTime = cTime

#     cv2.putText(img, str(int(fps)), (50, 50), cv2.FONT_HERSHEY_PLAIN, 3,
#                 (255,25,50), 3)

#     cv2.imshow("Image", img)
#     cv2.waitKey(1)


def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmlist, bbox = detector.findPosition(img)
        if len(lmlist) != 0:
            print(lmlist[4])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(
            img, str(int(fps)), (50, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 25, 50), 3
        )

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
