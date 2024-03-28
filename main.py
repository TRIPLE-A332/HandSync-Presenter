import cv2
import os
from cvzone.HandTrackingModule import HandDetector

#variables
width, height = 1280, 720
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
<<<<<<< HEAD
hs, ws = int(120*2), int(213*2)
gestureThreshold = 300

#hand Detector
detector = HandDetector(detectionCon=0.8, maxHands= 1)




while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    pathFullImage = os.path.join(folderPath, pathImages[0])
    imgCurrent = cv2.imread(pathFullImage)

    hands, img = detector.findHands(img, flipType= False)
    cv2.line(img, (0, gestureThreshold),(width , gestureThreshold),(0,25,0),10)

    if hands:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        print(fingers)


    #Adding Webcam img on Slide
    imgSmall = cv2.resize(img, (ws,hs))
    h, w, _ = imgCurrent.shape
    imgCurrent[0:hs,w-ws:w] = imgSmall


    cv2.imshow("Image", img)
    cv2.imshow("Slide", imgCurrent)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
=======
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

    if hands and buttonPressed is False:  # If hand is detected

        hand = hands[0]
        cx, cy = hand["center"]
        lmList = hand["lmList"]  # List of 21 Landmark points
        fingers = detectorHand.fingersUp(hand)  # List of which fingers are up
>>>>>>> f649448fe3b808a989eb2de99f1a5e0dcf5e81aa
