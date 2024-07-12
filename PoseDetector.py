# Import needed libraries(packages)
import time , cv2
import numpy as np
import PoseModule as pm

# Reading from webcam >> but you can use other sources like as below :
# img = cv2.imread("Your image path") >> define this one in the loop to prevent over-detection points
cap = cv2.VideoCapture(0)
# Define the size of window
cap.set(3,1280)
cap.set(4,720)
# For video
# cap = cv2.VideoCapture("Your video path with it's format")
# For image
# cap = cv2.imread("Your image path with it's format")
'''
If you want to user image you must change the code and note using while loop
But for webcam and video inout this code will work fine

Pay attention to your video dimension(height frame and width frame) to see a nice window al last

'''

# User the class as the detector(create an instance of class)
detector = pm.Pose_Detector()

# For calculating count
count = 0
# There is two directions >> 0(up) and 1(down)
direction = 0

# Previous time
pTime = 0

# Define the main function to run the code
while True :
    success , img = cap.read()
    # For resizing the image our video or webcam >> img = cv2.resize(img,(1280,720)) >> You can also do this outside the loop
    # Resizing have effects on pfs
    # img = cv2.imread("Your image/video path")

    # If draw = True it also shows other connections
    img = detector.findPose(img,draw=False)
    # If draw=True it just shows points
    lmList = detector.findPosition(img,draw=False)
    # lmList > landmark List
    # print(lmList)
    if len(lmList) != 0 :
        # Find angle for left arm
        angle = detector.findAngle(img,p1=11,p2=13,p3=15,draw=True)
        percentage = np.interp(angle,xp=(210,310),fp=(0,100))
        # For creating the bar
        bar = np.interp(angle,xp=(220,310),fp=(650,100))
        # print(angle,percentage)
        # Check for curls
        # Default color
        color = (0,255,0)
        # If the bar is completed
        # When the bar reaches to 100 %((100)and remain in this position) gets green
        if percentage == 100 :
            # If up
            if direction == 0 :
                count += 0.5
                # Change the direction to down(1)
                direction = 1
        # If the bar is not completed
        # When the bar is 0 % it's color is black
        if percentage == 0 :
            # The color of bar is black
            color = (0,0,0)
            # If down
            if direction == 1 :
                count += 0.5
                # Change the direction to up
                direction = 0
        # This if statement works like : the bar when is completing fills(1-100) with white and when it starts evacuating fills with red
        if 0 < percentage < 100 :
            color = (0,0,255)
            if direction == 0 :
                color = (255,255,255)
        # print(count)
        # Draw Bar
        cv2.rectangle(img,(1100,100),(1175,650),color,3)
        cv2.rectangle(img,(1100,int(bar)),(1175,650),color,cv2.FILLED)
        cv2.putText(img,f'{int(percentage)} %',(1100,75),cv2.FONT_HERSHEY_PLAIN,4,color,4)
        # Draw curl count
        # Create a background(optional / to put count and fps in it)
        # cv2.rectangle()
        # Or str(count)
        cv2.putText(img,'Count : '+str(int(count)),(50,100),cv2.FONT_HERSHEY_PLAIN,5,(0,0,0),5)
        # Current time
        cTime = time.time()
        # Calculate the fps(frame per second)# Calculate the fps(frame per second)
        fps = 1 / (cTime-pTime)
        pTime = cTime
        # Show the fps
        cv2.putText(img,'FPS : '+str(int(fps)),(50,250),cv2.FONT_HERSHEY_PLAIN,5,(0,0,0),5)
    # Create a window to see the result
    cv2.imshow("AI coach",img)
    # For closing the window
    # 0xFF is escape button
    k = cv2.waitKey(5) & 0xFF
    if k == 27 :
        break
