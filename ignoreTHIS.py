import cv2
import os
from cvzone.HandTrackingModule import HandDetector
import matplotlib.pyplot as plt
import numpy as np
import time
import pyautogui

#variables
width, height = 1280, 720
folderPath =  ("Presentation")

#camera setup
cap = cv2.VideoCapture(0)
cap.set(3,width)
cap.set(4,height)
pTime = 0

#Getting Images of Presentation
pathImages = sorted(os.listdir(folderPath), key= len)
# print(pathImages)

#variables
imgNumber = 0
hs, ws = int(120*1.5), int(213*1.5)
gestureThreshold = 300
buttonPressed = False
buttonCounter = 0
buttonDelay = 15
annotations = [[]]
annotationNumber = -1
annotationStart = False
screen_width, screen_height = pyautogui.size()

#hand Detector
detector = HandDetector(detectionCon=0.8, maxHands= 1)




while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    pathFullImage = os.path.join(folderPath, pathImages[0])
    imgCurrent = cv2.imread(pathFullImage)

    hands, img = detector.findHands(img)
    cv2.line(img, (0, gestureThreshold),(width , gestureThreshold),(0,25,0),10)

    #FPS
    cTime = time.time()
    fps = 1/ (cTime - pTime)
    pTime = cTime
    cv2.putText(img , str(int(fps)), (20,50), cv2.FONT_HERSHEY_PLAIN, 3 , (255,0,0) , 3 )     

    if hands and buttonPressed is False:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        cx, cy = hand['center']
        lmList = hand['lmList']

        #contraint values for easy drawing 
        xVal = int(np.interp(lmList[8][0],[width//2, width], [0,width]))
        yVal = int(np.interp(lmList[8][1],[150, height-150], [0,height]))
        indexFinger = xVal, yVal


        if cy <= gestureThreshold :         #if the hand is above the line(threshold)

            #Gesture NO1
            if fingers == [1,0,0,0,0]:
                print('Left')
                
                if imgNumber > 0:   
                    buttonPressed = True 
                    annotations = [[]]
                    annotationNumber = -1
                    annotationStart = False
                    imgNumber -=1

            #Gesture NO2
            if fingers == [0,0,0,0,1]:
                print('Right')
                
                if imgNumber < len(pathImages)-1:
                    buttonPressed = True
                    annotations = [[]]
                    annotationNumber = -1
                    annotationStart = False
                    imgNumber += 1

        #Gesture 3 - show pointer
        if fingers == [0,1,1,0,0]:
            cv2.circle(imgCurrent, indexFinger , 12 ,(0,0,255), cv2.FILLED )
        
        #Gesture 4 - drawing pointer
        if fingers == [0,1,0,0,0]:
            if annotationStart is False:
                annotationStart = True
                annotationNumber += 1
                annotations.append([])
            cv2.circle(imgCurrent, indexFinger , 12 ,(0,0,200), cv2.FILLED )
            annotations[annotationNumber].append(indexFinger)
        else:
            annotationStart = False

        #Gesture 5 - Erase
        if fingers == [0,1,1,1,0]:
            if annotations:
                annotations.pop(-1)
                annotationNumber = -1
                buttonPressed = True

        #Additional Gesture
                # Gesture 6 - Cursor
        if fingers == [1,1,0,0,0]:
            
            index_cx = screen_width/w*cx
            index_cy = screen_height/h*cy
            pyautogui.moveTo(index_cx,index_cy)
            thumb_tip = lmList[4]
            index_tip = lmList[8]
            thumb_to_index_distance = np.linalg.norm(np.array(thumb_tip) - np.array(index_tip))
            # if thumb_to_index_distance < 30:  
            #     print('click')
            #     pyautogui.click()
        
            #Gesture 6' - Zoom In/Out
        

            if thumb_to_index_distance < 50:  # Zoom In Gesture
                print("Zoom In")
                # buttonPressed = True
                # Adjust zoom level accordingly
                imgCurrent = cv2.resize(imgCurrent, None, fx=1.5, fy=1.5)

            elif thumb_to_index_distance > 200:  # Zoom Out Gesture
                print("Zoom Out")
                # buttonPressed = True
                # Adjust zoom level accordingly
                imgCurrent = cv2.resize(imgCurrent, None, fx=0.7, fy=0.7)
    else :
        annotationStart = False

    #button pressed iteration
    if buttonPressed:
        buttonCounter += 1
        if buttonCounter > buttonDelay:
            buttonCounter = 0
            buttonPressed = False


    for i in range(len(annotations)):
        for j in range(len(annotations[i])):
            if j != 0:
                cv2.line(imgCurrent,annotations[i][j - 1], annotations[i][j], (0,0,200), 12)

    #Adding Webcam img on Slide
    imgSmall = cv2.resize(img, (ws,hs))
    h, w, _ = imgCurrent.shape
    imgCurrent[0:hs,w-ws:w] = imgSmall


    cv2.imshow("Image", img)
    cv2.imshow("Slide", imgCurrent)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
