import cv2
import os
from cvzone.HandTrackingModule import HandDetector

#variables
width, height = 1920, 1080
folderPath =  ("Presentation")

#camera setup
cap = cv2.VideoCapture(0)
cap.set(3,width)
cap.set(4,height)

#Getting Images of Presentation
pathImages = sorted(os.listdir(folderPath), key= len)
# print(pathImages)

#variables
imgNumber = 0
hs, ws = int(120*2), int(213*2)
gestureThreshold = 300
buttonPressed = False
buttonCounter = 0
buttonDelay = 10

#hand Detector
detector = HandDetector(detectionCon=0.8, maxHands= 1)




while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    pathFullImage = os.path.join(folderPath, pathImages[0])
    imgCurrent = cv2.imread(pathFullImage)

    hands, img = detector.findHands(img)
    cv2.line(img, (0, gestureThreshold),(width , gestureThreshold),(0,25,0),10)

    if hands and buttonPressed is False:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        cx, cy = hand['center']
        lmList = hand['lmList']
        indexFinger = lmList[8][0], lmList[8][1]

        if cy <= gestureThreshold :         #if the hand is above the line(threshold)

            #Gesture NO1
            if fingers == [1,0,0,0,0]:
                print('Left')
                
                if imgNumber > 0:   
                    buttonPressed = True 
                    imgNumber -=1

            #Gesture NO2
            if fingers == [0,0,0,0,1]:
                print('Right')
                
                if imgNumber < len(pathImages)-1:
                    buttonPressed = True
                    imgNumber += 1

        #Gesture 3 - show pointer
        if fingers == [0,1,1,0,0]:
            cv2.circle(imgCurrent, indexFinger , 12 ,(0,0,255), cv2.FILLED )

    #button pressed iteration
    if buttonPressed:
        buttonCounter += 1
        if buttonCounter > buttonDelay:
            buttonCounter = 0
            buttonPressed = False


    #Adding Webcam img on Slide
    imgSmall = cv2.resize(img, (ws,hs))
    h, w, _ = imgCurrent.shape
    imgCurrent[0:hs,w-ws:w] = imgSmall


    cv2.imshow("Image", img)
    cv2.imshow("Slide", imgCurrent)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
