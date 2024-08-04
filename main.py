# The DragRect class defines a draggable rectangle with a specified position and size that can be
# updated based on cursor movement.
import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.9)
colorR = 255,0,0

cx,cy,w,h =100,100,200,200





class DragRect():
    def __init__(self ,poscenter,size=[200,200]):
        self.poscenter = poscenter
        self.size = size
        
    def update(self,cursor):
        cx,cy=self.poscenter
        w,h=self.size
        
        if cx-w//2<cursor[0]<cx+w//2 and cy-h//2<cursor[1]<cy+h//2:
                self.poscenter = cursor
                
rectList = []
for x in range(6):       
    rectList.append(DragRect([x*250+150,150]))
    
while True:
    success, img = cap.read()
    if not success:
        print("Failed to capture image, reinitializing camera")
        cap.release()
        cap = cv2.VideoCapture(0)
        cap.set(3, 1280)
        cap.set(4, 720)
        continue
    img = cv2.flip(img, 1)
    hands,img =detector.findHands(img,flipType=False)
    lmList=[]
    if hands:
        hand = hands[0]
        lmList = hand["lmList"] # list of 21 hand points 
        bbox = hand["bbox"] # bounding box info x,y,w,h
        centerPoint = hand["center"] # center point cx, cy
        handtype = hand["type"] # hand type left or right 
        
        
        fingers1=detector.fingersUp(hand)
        
        if len(hands)==2:
            hand2 = hands[0]
            lmList2 = hand2["lmList"] # list of 21 hand points 
            bbox2 = hand2["bbox"] # bounding box info x,y,w,h
            centerPoint2 = hand2["center"] # center point cx, cy
            handtype2 = hand2["type"] # hand type left or right 
            
            fingers2=detector.fingersUp(hand2)
    
    if lmList:
        p1 = lmList[8][:2]
        p2 = lmList[12][:2]
        l,info, img=detector.findDistance(p1,p2,img)
        
        # if l<40:
        cursor = lmList[8][:2]
        for rect in rectList:
            rect.update(cursor)


    for rect in rectList:
        cx,cy=rect.poscenter
        w,h=rect.size       
        cv2.rectangle(img,(cx-w//2,cy-h//2),(cx+w//2,cy+h//2),colorR,cv2.FILLED)        
        cvzone.cornerRect(img,(cx-w//2,cy-h//2,w,h),20,rt=0)
    
    cv2.imshow("image", img)
    cv2.waitKey(1)

