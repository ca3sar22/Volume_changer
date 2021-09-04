import cv2
import mediapipe as mp
import time
cap=cv2.VideoCapture(0)

mphand = mp.solutions.hands
hands=mphand.Hands()

mpdraw = mp.solutions.drawing_utils
pretime=0
while True:
    suc,img=cap.read()
    imgRGB=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    res=hands.process(imgRGB)
    #print(res.multi_hand_landmarks)
    if res.multi_hand_landmarks:
         for handmark in res.multi_hand_landmarks:
             for id,lm in enumerate(handmark.landmark):
                 h,w,c=img.shape
                 cx,cy=int(lm.x*w),int(lm.y*h)



             mpdraw.draw_landmarks(img,handmark,mphand.HAND_CONNECTIONS)
        
    currtime=time.time()
    fps=1/(currtime-pretime)
    pretime=currtime
    cv2.putText(img,f'FPS: {int(fps)}',(40,70),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,0,0),1)



    cv2.imshow('Img',img)
    cv2.waitKey(1)
