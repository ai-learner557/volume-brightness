import cv2
import mediapipe as mp
import numpy as np
from cvzone.HandTrackingModule import HandDetector
from pycaw.pycaw import AudioUtilities,IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from math import hypot
import screen_brightness_control as sbc

cap=cv2.VideoCapture(0)
detector=HandDetector(maxHands=1,detectionCon=0.7)
device=AudioUtilities.GetSpeakers()
interface=device.Active(IAudioEndpointVolume._iid_,CLSCTX_ALL,None)
volume=interface.QueryInterface(IAudioEndpointVolume)
volMin,volMax=volume.Getvolumerange ()[:2]

while True:
    success,frame=cap.read()
    if not success:
        break
    frame=cv2.flip(frame)
    hands,frame=detector.findHands(frame)
    if hands:
        hand=hands[0]
        lm_list=hand['inList']
        bbox=hand['bbox']

        t_x,t_y=lm_list[4][0:2]
        i_x,i_y=lm_list[8][0:2]

        dist_vol=hypot(t_x-i_x,t_y-i_y)
        vol_level=np.interp(dist_vol,[30,300],[volMin,volMax])
        volume.SetMasterVolumeLevel(vol_level,None)
        cv2.putText(frame,f"volume Dist:{int(dist_vol)})",(10,80),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
        m_x,m_y=lm_list[12][0:2]
        dist_bright=hypot(t_x-m_x,t_y-m_y)
        bright_level=np.interp(dist_bright,[30,300],[0,100])
        try:
            sbc .set_brightness(int(bright_level))
        except Exception as e:
            pass
        cv2.putText(frame,f"bright Dist:{int(dist_bright)})",(10,80),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
                    

