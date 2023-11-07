import cv2
cap=cv2.VideoCapture("WhatsApp Video 2023-10-24 at 02.28.17_e8fb1cf5.mp4")
#tracker=cv2.legacy.TrackerMOSSE_create()
tracker=cv2.TrackerCSRT_create()
success,frame=cap.read()
bbox=cv2.selectROI("Tracking",frame,False)
tracker.init(frame,bbox)

def drawBox(img,bbox):
    x,y,w,h=[int(x) for x in bbox]
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,255),3,1)
    cv2.putText(img,"Tracking",(75,75),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,255),2)


while True:
    timer=cv2.getTickCount()
    ret,frame=cap.read()
    if not ret or frame is None:
        break
    success,bbox=tracker.update(frame)
    print(type(bbox),bbox)
    if success:
        drawBox(frame,bbox)
    else:
        cv2.putText(frame,"Lost",(75,75),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,255),2)
    fps=cv2.getTickFrequency()/(cv2.getTickCount()-timer)
    cv2.putText(frame,str(int(fps)),(75,50),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,255),2)
    cv2.imshow("track",frame)
    if cv2.waitKey(1) & 0XFF==ord('x'):
        break
cap.release()
cv2.destroyAllWindows()
