# import cv2
# import numpy as np
# import Handtracking as htm
# import time
# import autopy
#
# ##########################
# wCam, hCam = 640, 480
# frameR = 100  # Frame Reduction
# smoothening = 8
# #########################
#
# pTime = 0
# plocX, plocY = 0, 0 #prev loc, curr loc
# clocX, clocY = 0, 0
#
# cap = cv2.VideoCapture(0)
# cap.set(3, wCam)
# cap.set(4, hCam)
# detector = htm.handDetector(maxHands=1)
# wScr, hScr = autopy.screen.size()
# # print(wScr, hScr)
#
# while True:
#     # 1. Find hand Landmarks
#     success, img = cap.read()
#     img = detector.findHands(img)
#     lmList, bbox = detector.findPosition(img)
#     # 2. Get the tip of the index and middle fingers
#     if len(lmList) != 0:
#          x1, y1 = lmList[8][1:]
#          x2, y2 = lmList[12][1:]
#          #print(x1, y1, x2, y2)
#
#          # 3. Check which fingers are up
#          fingers = detector.fingersUp()
#          #print(fingers)
#          cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
#                   (255, 0, 255), 2)
#          # 4. Only Index Finger - Moving Mode
#          if fingers[1] == 1 and fingers[2] == 0:
#             # 5. Convert Coordinates(when not using entire camera)
#             x3 = np.interp(x1, (frameR, wCam-frameR ), (0, wScr))
#             y3 = np.interp(y1, (frameR, hCam-frameR ), (0, hScr))
#
#             # 6. Smoothen Values
#             clocX = plocX + (x3 - plocX) / smoothening
#             clocY = plocY + (y3 - plocY) / smoothening
#
#             # 7. Move Mouse
#             autopy.mouse.move(wScr - clocX, clocY)
#             cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
#             plocX, plocY = clocX, clocY
#
#          # 8. Both Index and middle fingers are up : Clicking Mode
#          if fingers[1] == 1 and fingers[2] == 1:
#              length, img, _ = detector.findDistance(8, 12, img)
#              # 9. Find distance between fingers
#              length, img, lineInfo = detector.findDistance(8, 12, img)
#              print(length)
#              # 10. Click mouse if distance short
#              if length < 40:
#               cv2.circle(img, (lineInfo[4], lineInfo[5]),
#                          15, (0, 255, 0), cv2.FILLED)
#               autopy.mouse.click()
#     #
#     # 11. Frame Rate
#     cTime = time.time()
#     fps = 1 / (cTime - pTime) #curr-prev time
#     pTime = cTime
#     cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
#                 (255, 0, 0), 3)
#     #  12. Display
#     cv2.imshow("Image", img)
#     cv2.waitKey(1)

import cv2
import numpy as np
import Handtracking as htm
import time
import pyautogui #autopy not good for scrolling

##########################
wCam, hCam = 640, 480
frameR = 100  # Frame Reduction
smoothening = 8
scrollSpeed = 150  # Increased scroll speed
#########################

pTime = 0
plocX, plocY = 0, 0  # previous location
clocX, clocY = 0, 0  # current location

# Cursor trail variables
trail_points = []
max_trail_points = 20

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1) #initalize handdetector for 1 hand
screenWidth, screenHeight = pyautogui.size()

while True:
    #1. Capture frame from camera and detect hands
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    #2. Check if hand landmarks are detected
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]  # Index finger tip
        x2, y2 = lmList[12][1:]  # Middle finger tip
        #3. check which fingers are up
        fingers = detector.fingersUp()
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)
        #4. Index finger up - moving mouse
        if fingers[1] == 1 and fingers[2] == 0:
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, screenWidth))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, screenHeight))
            # Smooth the movement of the cursor
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            pyautogui.moveTo(screenWidth - clocX, clocY)
            #draw circle at index finger
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY

            trail_points.append((int(x1), int(y1)))
            if len(trail_points) > max_trail_points:
                trail_points.pop(0)
        #5. Index and middle finger up - Click mode
        if fingers[1] == 1 and fingers[2] == 1:
            length, img, lineInfo = detector.findDistance(8, 12, img)
            if length < 40: # if dis less than 40 , click
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                pyautogui.click()
        #6. Index, Middle and Ring finger up - Scroll
        if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1:
            # Scroll up - if index finger higher than middle of screen
            if y1 < hCam // 2:
                pyautogui.scroll(scrollSpeed)
            # Scroll down - if index finger lower than middle of screen
            elif y1 > hCam // 2:
                pyautogui.scroll(-scrollSpeed)
            cv2.putText(img, "Scrolling Mode", (20, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

    for i in range(1, len(trail_points)):
        cv2.line(img, trail_points[i - 1], trail_points[i], (255, 0, 255), 2)
        size = int(15 * (i / len(trail_points)))
        cv2.circle(img, trail_points[i], size, (255, 0, 255), 1)

    #7. Display the frame rate on the image
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f"FPS: {int(fps)}", (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1) #refresh frame after every 1ms

