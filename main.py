from cvzone.HandTrackingModule import HandDetector
import cv2
import os
import numpy as np
import time
import pyautogui    

# Parameters
width, height = 1280, 720
gestureThreshold = 300
folderPath = "Presentation"
screen_width, screen_height = pyautogui.size()

# Camera Setup
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)
pTime = 0

# Hand Detector
detectorHand = HandDetector(detectionCon=0.8, maxHands=1)

# Variables
imgList = []
delay = 30
buttonPressed = False
counter = 0
drawMode = False
imgNumber = 0
delayCounter = 0
annotations = [[]]
annotationNumber = -1
annotationStart = False
hs, ws = int(120 * 1), int(213 * 1)  # width and height of small image

# Get list of presentation images
pathImages = sorted(os.listdir(folderPath), key=len)
print(pathImages)

while True:
    # Get image frame
    success, img = cap.read()
    img = cv2.flip(img, 1)
    pathFullImage = os.path.join(folderPath, pathImages[imgNumber])
    imgCurrent = cv2.imread(pathFullImage)

    # Find the hand and its landmarks
    hands, img = detectorHand.findHands(img)  # with draw
    # Draw Gesture Threshold line
    cv2.line(img, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 10)

    #FPS
    cTime = time.time()
    fps = 1/ (cTime - pTime)
    pTime = cTime
    cv2.putText(img , str(int(fps)), (20,50), cv2.FONT_HERSHEY_PLAIN, 3 , (255,0,0) , 3 )

    if hands and buttonPressed is False:  # If hand is detected

        hand = hands[0]
        cx, cy = hand["center"]
        lmList = hand["lmList"]  # List of 21 Landmark points
        fingers = detectorHand.fingersUp(hand)  # List of which fingers are up

        # Constrain values for easier drawing
        xVal = int(np.interp(lmList[8][0], [width // 2, width], [0, width]))
        yVal = int(np.interp(lmList[8][1], [150, height-150], [0, height]))
        indexFinger = xVal, yVal

        if cy <= gestureThreshold:  # If hand is at the height of the face
            if fingers == [1, 0, 0, 0, 0]: #Gesture1
                print("Left")
                buttonPressed = True
                if imgNumber > 0:
                    imgNumber -= 1
                    annotations = [[]]
                    annotationNumber = -1
                    annotationStart = False
            if fingers == [0, 0, 0, 0, 1]:    #Gesture2
                print("Right")
                buttonPressed = True
                if imgNumber < len(pathImages) - 1:
                    imgNumber += 1
                    annotations = [[]]
                    annotationNumber = -1
                    annotationStart = False

        if fingers == [0, 1, 1, 0, 0]:   #Gesture 3 - show pointer
            cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)

        if fingers == [0, 1, 0, 0, 0]:        #Gesture 4 - drawing pointer
            if annotationStart is False:
                annotationStart = True
                annotationNumber += 1
                annotations.append([])
            print(annotationNumber)
            annotations[annotationNumber].append(indexFinger)
            cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)

        else:
            annotationStart = False

        if fingers == [0, 1, 1, 1, 0]:          #Gesture 5 - Erase
            if annotations:
                annotations.pop(-1)
                annotationNumber -= 1
                buttonPressed = True
        
                # Gesture 6 - Cursor
        if fingers == [1,1,0,0,0]:
            
            index_cx = screen_width/w*cx
            index_cy = screen_height/h*cy
            pyautogui.moveTo(index_cx,index_cy)
            thumb_tip = lmList[4]
            index_tip = lmList[8]
            thumb_to_index_distance = np.linalg.norm(np.array(thumb_tip) - np.array(index_tip))
            if thumb_to_index_distance < 30:  
                print('click')
                pyautogui.click()
        
            #Gesture 6' - Zoom In/Out
        

            # if thumb_to_index_distance < 50:  # Zoom In Gesture
            #     print("Zoom In")
            #     # buttonPressed = True
            #     # Adjust zoom level accordingly
            #     imgCurrent = cv2.resize(imgCurrent, None, fx=1.5, fy=1.5)

            # elif thumb_to_index_distance > 200:  # Zoom Out Gesture
            #     print("Zoom Out")
            #     # buttonPressed = True
            #     # Adjust zoom level accordingly
            #     imgCurrent = cv2.resize(imgCurrent, None, fx=0.7, fy=0.7)


    else:
        annotationStart = False

    #button pressed iteration
    if buttonPressed:
        counter += 1
        if counter > delay:
            counter = 0
            buttonPressed = False

    for i, annotation in enumerate(annotations):
        for j in range(len(annotation)):
            if j != 0:
                cv2.line(imgCurrent, annotation[j - 1], annotation[j], (0, 0, 200), 12)

    #Adding Webcam img on Slide
    imgSmall = cv2.resize(img, (ws, hs))
    h, w, _ = imgCurrent.shape
    imgCurrent[0:hs, w - ws: w] = imgSmall

    cv2.imshow("Slides", imgCurrent)
    cv2.imshow("Image", img)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break