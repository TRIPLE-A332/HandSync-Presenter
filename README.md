# HandSync Presenter 

A **hand gesture-controlled presentation system** built using **OpenCV** and **CVZone** to enable **touch-free slide control**. This project aims to create an intuitive and hardware-free interface for presenters by leveraging real-time computer vision and gesture recognition.

> **B.Tech Final Year Major Project** — Department of Computer Engineering

## Motivation

Traditional clicker-based slide navigation tools restrict mobility and often require hardware. **HandSync Presenter** addresses this by using **hand gestures** to control slides, offering a **contactless**, **portable**, and **cost-effective** solution that works with just a webcam.

##  Features

-  Hand gestures to **control slides**, **draw**, and **emulate cursor clicks**
-  Automatically loads all slides from a specified folder
-  Draw directly on slides using index finger
-  Use hand gestures as a virtual mouse
-  Undo the last drawn annotation

##  Gesture Controls

| Gesture                                  | Action                                  |
|------------------------------------------|------------------------------------------|
| **Show Small Finger**                    |  Next Slide                            |
| **Show Thumb**                          |  Previous Slide                         |
| **Index Finger**                         |  Start Drawing                          |
| **Index + Middle Fingers**              |  Cursor Mode (move pointer)           |
| **Index + Middle + Ring Fingers**       |  Undo Last Drawing                      |
| **Index + Thumb (pinch/tap)**           |  Cursor Click (mouse click action)     |

## Tech Stack

| Tool/Library  | Purpose                         |
|---------------|----------------------------------|
| Python        | Core programming language        |
| OpenCV        | Image capture and processing     |
| CVZone        | Hand tracking and gesture support|
| MediaPipe     | Underlying hand landmark model   |


## Acknowledgements
CVZone Library by Murtaza Hassan
MediaPipe by Google Research
