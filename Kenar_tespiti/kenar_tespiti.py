import cv2
import numpy as np
from random import randint as rnd
#Webcam görüntüsündeki renkli cismin kenarlarını trackbar yardımıyla çizen program

def callback(x):
    pass

camera = cv2.VideoCapture(0)
cv2.namedWindow("image", cv2.WINDOW_NORMAL)


cv2.createTrackbar('LH','image',0,255,callback)
cv2.createTrackbar('HH','image',255,255,callback)

cv2.createTrackbar('LS','image',0,255,callback)
cv2.createTrackbar('HS','image',255,255,callback)

cv2.createTrackbar('LV','image',0,255,callback)
cv2.createTrackbar('HV','image',255,255,callback)

kernel = np.ones((5,5),np.uint8)
while True:
    
    ret, frame = camera.read()
    img = frame.copy()
    
    LH = cv2.getTrackbarPos('LH', 'image')
    HH = cv2.getTrackbarPos('HH', 'image')
    LS = cv2.getTrackbarPos('LS', 'image')
    HS = cv2.getTrackbarPos('HS', 'image')
    LV = cv2.getTrackbarPos('LV', 'image')
    HV = cv2.getTrackbarPos('HV', 'image')

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    lower_hsv = np.array([LH, LS, LV])
    higher_hsv = np.array([HH, HS, HV])
    
    mask = cv2.inRange(hsv, lower_hsv, higher_hsv)
    
    #Anlık görüntünün kasmaması için morfolojik işlem uyguladık.
    mask = cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel)
    mask = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel)
    
    frame = cv2.bitwise_and(frame, frame, mask=mask)
    
    #contours = çevre noktaların koordinatları olan liste , cv2.CHAIN_APPROX_SIMPLE : köşe olması olası değerleri alır.(NONE,tüm değerleri alır.)
    contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    #Contoursları kullanarak görüntünün üzerine şekil çizme
    for i,cnt in enumerate(contours):
        #area :piksel alanı, piksel alanı 200-50000 arası olan nesneleri algıladık.
        area = cv2.contourArea(cnt)
        
        if area > 50000 or area < 200:
            continue 

        x,y,w,h = cv2.boundingRect(cnt)
        #print(x,y,w,h)
        color = (rnd(0,256), rnd(0,256), rnd(0,256))
        
        cv2.drawContours(img,contours,i,color,3, cv2.LINE_8,hierarchy,0)
    
    
    cv2.imshow("image", frame)
    cv2.imshow("contour", img)
    
    if cv2.waitKey(33) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()
camera.release()