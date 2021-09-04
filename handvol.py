import cv2
import numpy as np
import time
import handtrackmod as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wcam,hcam=640,480 
cap = cv2.VideoCapture(1)
cap.set(3,wcam)
cap.set(4,hcam)
pretime=0
detector = htm.dec(detectioncon=0.7)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volrange=volume.GetVolumeRange()

minvol=volrange[0]
maxvol=volrange[1]

volb=400
volper=0
while True:
    suc,img=cap.read()

    img=detector.findhand(img)
    lmlist = detector.findpos(img,draw=False)
    if len(lmlist)!=0:

        x1,y1=lmlist[4][1],lmlist[4][2]
        x2,y2=lmlist[8][1], lmlist[8][2]
        cx,cy=(x1+x2)//2,(y1+y2)//2

        cv2.circle(img,(x1,y1),12,(255,0,0),cv2.FILLED)
        cv2.circle(img,(x2,y2),12,(255,0,0),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,0),3)
        cv2.circle(img,(cx,cy),12,(255,0,0),cv2.FILLED)

        length = math.hypot(x2-x1,y2-y1)

        #vol=np.interp(length,[55,260],[minvol,maxvol])
        volb=np.interp(length,[55,240],[400,150])
        volper=np.interp(length,[55,240],[0,100])

        chick=10
        volper=chick*round(volper/chick)

        volume.SetMasterVolumeLevelScalar(volper/100, None)

        #print(vol)
        if length<55:
            cv2.circle(img,(cx,cy),12,(0,0,255),cv2.FILLED)
    
    cv2.rectangle(img,(50,150),(85,400),(0,255,0), 2)
    cv2.rectangle(img,(50,int(volb)),(85,400),(0,255,0), cv2.FILLED)
    cv2.putText(img,f'VOL: {int(volper)} %',(45,460),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)


    currtime=time.time()
    fps=1/(currtime-pretime)
    pretime=currtime
    cv2.putText(img,f'FPS: {int(fps)}',(40,70),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),1)
    cv2.imshow('Img',img)

    


    cv2.waitKey(1)

