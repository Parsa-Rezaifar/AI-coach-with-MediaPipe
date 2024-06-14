# Import needed libraries(packages)
import cv2
import time
import PoseModule as pm

cap = cv2.VideoCapture(0)

pTime = 0

detector = pm.Pose_Detector()

while True:
    success, img = cap.read()
    img = detector.findPose(img)
    lmList = detector.findPosition(img, draw=False)
    # lmList > landmarks list
    if len(lmList) != 0 :
        # print(lmList[14])
        # Draw landmarks
        cv2.circle(img,(lmList[14][1], lmList[14][2]),15,(0,0,255),cv2.FILLED)
    # cTime > current time
    cTime = time.time()
    # Calculate fps(frame per second)
    fps = 1/(cTime -pTime)
    pTime = cTime
    # Show fps
    cv2.putText(img,'FPS : '+str(int(fps)),(70,50),cv2.FONT_HERSHEY_PLAIN,3,
                (255,0,0),3)
    # cv2.imshow("Screen",img) >> Show a small screen
    # Make screen full screen
    cv2.namedWindow('Screen',cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('Screen', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    # Create a window to see the result
    cv2.imshow('Screen',img)
    # For closing the window
    # 0xFF is escape button
    k = cv2.waitKey(5) & 0xFF
    if k == 27 :
        break