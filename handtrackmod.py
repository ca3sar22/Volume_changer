import cv2
import mediapipe as mp
import time


class dec():
    def __init__(self, mode=False,maxhands=2,detectioncon=0.5,trackcon=0.5):
        self.mode=mode
        self.maxhands=maxhands
        self.detectioncon=detectioncon
        self.trackcon=trackcon

        self.mphand = mp.solutions.hands
        self.hands=self.mphand.Hands(self.mode, self.maxhands, self.detectioncon, self.trackcon)
        self.mpdraw = mp.solutions.drawing_utils
    
    def findhand(self,img,drw=True):
    
        imgRGB=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        self.res=self.hands.process(imgRGB) 
        #print(res.multi_hand_landmarks)
        if self.res.multi_hand_landmarks:
            for handmark in self.res.multi_hand_landmarks:
                if drw:

                    self.mpdraw.draw_landmarks(img,handmark,self.mphand.HAND_CONNECTIONS)
        return img

    def findpos(self,img,handno=0,draw=True):
        lmlist=[]
        if self.res.multi_hand_landmarks:
            thehand=self.res.multi_hand_landmarks[handno]
            for id,lm in enumerate(thehand.landmark):
                h,w,c=img.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                lmlist.append([id,cx,cy])
                if draw:
                    cv2.circle(img,(cx,cy),2,(255,0,255),cv2.FILLED)
                
        return lmlist



def main():
    cap=cv2.VideoCapture(0)

    detector=dec()

    pretime=0
    while True:
        suc,img=cap.read()
        img=detector.findhand(img)
        lmlist=detector.findpos(img)
        if len(lmlist)!=0:
            print(lmlist[4])
        currtime=time.time()
        fps=1/(currtime-pretime)
        pretime=currtime
        cv2.putText(img,f'FPS: {int(fps)}',(40,70),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,0,0),1)
        cv2.imshow('Img',img)
        cv2.waitKey(1)



    cv2.imshow('Img',img)
    cv2.waitKey(1)



if __name__=="__main__":
    main()
