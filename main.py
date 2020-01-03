import cv2
import numpy as np
import time
import os
import datetime
import array
import random



countoursPoints = [[[211, 111]],

       [[212, 110]],

       [[218, 110]],

       [[219, 111]],

       [[222, 111]],

       [[223, 112]],

       [[228, 112]],

       [[229, 113]],

       [[232, 113]],

       [[233, 114]],

       [[238, 114]],

       [[239, 115]],

       [[243, 115]],

       [[244, 116]],

       [[249, 116]],

       [[250, 117]],

       [[251, 117]],

       [[252, 116]],

       [[253, 116]],

       [[255, 118]],

       [[259, 118]],

       [[256, 118]],

       [[255, 117]],

       [[255, 116]],

       [[256, 115]],

       [[257, 116]],

       [[263, 116]],

       [[264, 117]],

       [[273, 117]],

       [[274, 118]],

       [[276, 118]],

       [[277, 119]],

       [[279, 119]],

       [[280, 120]],

       [[281, 120]],

       [[282, 121]],

       [[283, 121]],

       [[284, 122]],

       [[283, 123]],

       [[281, 123]],

       [[284, 123]],

       [[285, 124]],

       [[288, 124]],

       [[289, 125]],

       [[293, 125]],

       [[294, 126]],

       [[298, 126]],

       [[299, 127]],

       [[301, 127]],

       [[302, 128]],

       [[307, 128]],

       [[308, 129]],

       [[310, 129]],

       [[311, 130]],

       [[315, 130]],

       [[316, 131]],

       [[319, 131]],

       [[320, 132]],

       [[324, 132]],

       [[325, 133]],

       [[329, 133]],

       [[330, 134]],

       [[334, 134]],

       [[335, 135]],

       [[338, 135]],

       [[339, 136]],

       [[342, 136]],

       [[343, 137]],

       [[347, 137]],

       [[348, 138]],

       [[352, 138]],

       [[353, 139]],

       [[355, 139]],

       [[356, 140]],

       [[359, 140]],

       [[361, 142]],

       [[361, 146]],

       [[362, 147]],

       [[362, 159]],

       [[363, 160]],

       [[362, 161]],

       [[362, 163]],

       [[363, 164]],

       [[363, 174]],

       [[364, 175]],

       [[364, 189]],

       [[365, 190]],

       [[364, 191]],

       [[364, 192]],

       [[365, 193]],

       [[364, 194]],

       [[364, 195]],

       [[365, 196]],

       [[365, 207]],

       [[366, 208]],

       [[366, 226]],

       [[367, 227]],

       [[367, 234]],

       [[366, 235]],

       [[356, 235]],

       [[355, 234]],

       [[347, 234]],

       [[346, 233]],

       [[339, 233]],

       [[338, 232]],

       [[337, 233]],

       [[336, 233]],

       [[335, 232]],

       [[327, 232]],

       [[326, 231]],

       [[318, 231]],

       [[317, 230]],

       [[307, 230]],

       [[306, 229]],

       [[305, 230]],

       [[304, 229]],

       [[297, 229]],

       [[296, 228]],

       [[287, 228]],

       [[286, 227]],

       [[284, 227]],

       [[283, 228]],

       [[282, 228]],

       [[281, 227]],

       [[277, 227]],

       [[276, 226]],

       [[266, 226]],

       [[265, 225]],

       [[259, 225]],

       [[258, 224]],

       [[247, 224]],

       [[246, 223]],

       [[241, 223]],

       [[240, 222]],

       [[230, 222]],

       [[229, 221]],

       [[221, 221]],

       [[220, 220]],

       [[211, 220]],

       [[210, 219]],

       [[210, 212]],

       [[209, 211]],

       [[210, 210]],

       [[210, 205]],

       [[209, 204]],

       [[210, 203]],

       [[210, 132]],

       [[211, 131]]]



screenContour = np.array(countoursPoints).reshape((-1,1,2)).astype(np.int32)


def sizeFiltering(contours):

    y = 0
    x = 0
    w = 0
    h = 0

    filtredContours = []

    heightmax = 500
    widthmax  = 500

    widthMin  = 100
    heightMin = 100
    
    for cnt in contours:
        rect = cv2.minAreaRect(cnt)       #I have used min Area rect for better result
        width = rect[1][0]
        height = rect[1][1]

        if (width < widthmax) and (height < heightmax) and (width > widthMin) and (height > heightMin):
            filtredContours.append(cnt)

    return filtredContours, [y,x,h,w]

currentframe = 0

screenOn = True

total = 0
success = 0


while 1:  
     # reading from frame 


    if screenOn:
        os.system('ssh -i /home/selman/.ssh/comelit-device -p8222  root@172.22.0.70 "echo 1 > /sys/class/backlight/rk28_bl/bl_power"')

        os.system('ssh -i /home/selman/.ssh/comelit-device -p8222  root@172.22.0.70 "echo 1 > /sys/class/graphics/fb0/blank"')
      
        screenOn = False

        
    else:
        os.system('ssh -i /home/selman/.ssh/comelit-device -p8222  root@172.22.0.70 "echo 0 > /sys/class/backlight/rk28_bl/bl_power"')
        os.system('ssh -i /home/selman/.ssh/comelit-device -p8222  root@172.22.0.70 "echo 0 > /sys/class/graphics/fb0/blank"')
      
        screenOn = True

        
    time.sleep(3)
    

    if screenOn:

        vidcap = cv2.VideoCapture(0) 

        ret,frame = vidcap.read() 

        if ret:

            timestamp = str(datetime.datetime.now().timestamp())

            name = './image/' + timestamp + '.jpg'
         
            imgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(imgray, 110, 255, 0)
            # contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            # contours, rectCountour = sizeFiltering(contours)

            cv2.drawContours(frame, screenContour, -1, (0,255,0), 3)

            cv2.imwrite(name, frame)  

            if (len(screenContour) > 0):
                x, y, w, h = cv2.boundingRect(screenContour)
                roi = thresh[y:y + h, x:x + w]
                count = cv2.countNonZero(roi)

                if count > 10000:
                    print("SCREEN IS ON: ", count )
                    success +=1
                else:
                    print("SCREEN IS OFF: ", count)
                    exit()

            total += 1

            print("total/success: ", total,"/",success, "image: ", timestamp)
        
        vidcap.release()

        currentframe += 1

    time.sleep(1)


