# Import needed libraries(packages)
import cv2 , time
import mediapipe as mp

# Create tools

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

# Reading from webcam >> but you can use other sources line as below :
# img = cv2.imread("Your image/video path") >> define this one in the loop to prevent over-detection points
cap = cv2.VideoCapture(0)
# Define the size of window
cap.set(3,1280)
cap.set(4,720)

# Previous time
pTime = 0

# Do the detection
while True :
    success , img = cap.read()
    # Convert BGR image to RGB image
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    # print(results.pose_landmarks)
    if results.pose_landmarks :
        mpDraw.draw_landmarks(img,results.pose_landmarks,mpPose.POSE_CONNECTIONS)
        for id , lm in enumerate(results.pose_landmarks.landmark) :
            # lm > landmarks
            # h > height , w > width , c > color channels
            h , w , c = img.shape
            # print(id,lm)
            cx , cy = int(lm.x*w) , int(lm.y*h)
            # Draw landmarks
            cv2.circle(img,(cx,cy),5,(0,0,255),cv2.FILLED)
        # cTime > current time
        cTime = time.time()
        # Calculate the fps(frame per second)
        fps = 1/(cTime-pTime)
        pTime = cTime
        # Show the fps
        cv2.putText(img,'FPS : '+str(int(fps)),(70,50),cv2.FONT_HERSHEY_PLAIN,3,(0,0,0),3)
        # Create a window to see the result
        cv2.imshow('Estimation',img)
        # For closing the window
        # 0xFF is escape button
        k = cv2.waitKey(5) & 0xFF
        if k == 27 :
            break