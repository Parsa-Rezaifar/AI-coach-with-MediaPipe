# Import needed libraries(packages)
import time , math , cv2
import mediapipe as mp

# Create Pose detector class to do the detention
class Pose_Detector :
    # Initiate the Pose_Detector class
    def __init__(self,mode=False,upBody=False,smooth=True,detectionCon=True,trackCon=True) :
        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.results = None
        self.lmList = None
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode,self.upBody,self.smooth,self.detectionCon,self.trackCon)
    # Find the pose of body
    def findPose(self,img,draw=True) :
        # Convert BGR image to RGB
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks :
            if draw :
                self.mpDraw.draw_landmarks(img,self.results.pose_landmarks,self.mpPose.POSE_CONNECTIONS)
        return img
    # Find the position
    def findPosition(self,img,draw=True) :
        # If you write >> lmList = [] >> This would be a local variable
        # If you write >> self.lmList = [] >> This would be a global variable
        self.lmList = []
        # lmList > landmark List
        if self.results.pose_landmarks :
            for id , lm in enumerate(self.results.pose_landmarks.landmark) :
                # lm > landmarks
                # h > height , w > width , c > color channels
                h , w , c = img.shape
                # print(id,lm)
                cx , cy = int(lm.x*w) , int(lm.y*h)
                self.lmList.append([id,cx,cy])
                if draw :
                    cv2.circle(img,(cx,cy),4,(0,0,255),cv2.FILLED)
        return self.lmList
    # Find the angle between three given points
    def findAngle(self,img,p1,p2,p3,draw=True) :
        # Get the landmarks
        # You can either write >> _ , x1 , y1 = self.lmList[p1] or x1 , y1 = self.lmList[p1][1:]
        x1 , y1 = self.lmList[p1][1:]
        x2 , y2 = self.lmList[p2][1:]
        x3 , y3 = self.lmList[p3][1:]
        # Calculate the angle using p1(point one) , p2(point two) , p3(point three)
        angle = math.degrees(math.atan2(y3-y2,x3-x2) - math.atan2(y1-y2,x1-x2))
        # print(angle)
        # If angle was negative :
        if angle < 0 :
            angle += 360
        # Draw those three points and show the angle
        if draw :
            # Draw two line to show the angle between them
            cv2.line(img,(x1,y1),(x2,y2),(0,0,0),3)
            cv2.line(img,(x3,y3),(x2,y2),(0,0,0),3)
            # Draw two circle for each point
            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
            # Draw two circle for each point
            cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
            # Draw two circle for each point
            cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
            # Draw angle
            cv2.putText(img,str(int(angle)),(x2-30,y2+80),cv2.FONT_HERSHEY_PLAIN,2,(0,255,0),2)
        return angle
# Define the main function to run the code
def main() :
    # Reading from webcam >> but you can use other sources
    cap = cv2.VideoCapture(0)
    # Define the size of window
    cap.set(3, 1280)
    cap.set(4, 720)
    # previous Time
    pTime = 0
    # User the class as the detector(create an instance of class)
    detector = Pose_Detector()
    # Do the detection
    while True :
        success , img = cap.read()
        img = detector.findPose(img)
        lmList = detector.findPosition(img,draw=False)
        if len(lmList) != 0 :
            # print(lmList[14])
            # Draw circles for each landmark
            cv2.circle(img,(lmList[14][1],lmList[14][2]),15,(0,0,255),cv2.FILLED)
        # Current time
        cTime = time.time()
        # Calculate the fps(frame per second)
        fps = 1/(cTime-pTime)
        pTime = cTime
        # Show the fps
        cv2.putText(img,'FPS : '+str(int(fps)),(70,50),cv2.FONT_HERSHEY_PLAIN,3,(0,0,255),3)
        # Create a window to see the result
        cv2.imshow("Screen is on now",img)
        # For closing the window
        # 0xFF is escape button
        k = cv2.waitKey(5) & 0xFF
        if k == 27 :
            break
if __name__=="__main__" :
    main()