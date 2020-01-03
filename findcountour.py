import cv2
import numpy as np
import time
import os
import datetime
import array


def sizeFiltering(contours):

    y = 0
    x = 0
    w = 0
    h = 0

    filtredContours = []

    heightmax = 200
    widthmax  = 200

    widthMin  = 100
    heightMin = 100
    
    for cnt in contours:
        rect = cv2.minAreaRect(cnt)       #I have used min Area rect for better result
        width = rect[1][0]
        height = rect[1][1]

        if (width < widthmax) and (height < heightmax) and (width > widthMin) and (height > heightMin):
            filtredContours.append(cnt)

    return filtredContours, [y,x,h,w]



vidcap = cv2.VideoCapture(0) 

ret,frame = vidcap.read() 

if ret:


    imgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 110, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours, rectCountour = sizeFiltering(contours)

    cv2.drawContours(frame, contours, -1, (0,255,0), 3)

    print(contours)


    cv2.imshow('image',frame)
    cv2.waitKey(0)

vidcap.release()
