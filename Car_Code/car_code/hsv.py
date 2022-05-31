import cv2
import numpy as np
import RPi.GPIO as GPIO
from time import sleep
import time
import threading


def empty(a):
    pass

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)  # 0对应笔记本自带摄像头
cap.set(3, frameWidth)  # set中，这里的3，下面的4和10是类似于功能号的东西，数字的值没有实际意义
cap.set(4, frameHeight)
cap.set(10, 50)        # 设置亮度
pulse_ms = 30

# 调试用代码，用来产生控制滑条
cv2.namedWindow("HSV")
cv2.resizeWindow("HSV", 640, 300)
cv2.createTrackbar("HUE Min", "HSV", 13, 179, empty)
cv2.createTrackbar("SAT Min", "HSV", 96, 255, empty)
cv2.createTrackbar("VALUE Min", "HSV", 119, 255, empty)
cv2.createTrackbar("HUE Max", "HSV", 23, 179, empty)
cv2.createTrackbar("SAT Max", "HSV", 255, 255, empty)
cv2.createTrackbar("VALUE Max", "HSV", 255, 255, empty)

lower = np.array([13, 96, 119])     
upper = np.array([23, 255, 255])
erorr=0
targetPos_x = 0
targetPos_y = 0
lastPos_x = 0
lastPos_y = 0


while True:
    _, img = cap.read()
    imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# # 
    h_min = cv2.getTrackbarPos("HUE Min", "HSV")
    h_max = cv2.getTrackbarPos("HUE Max", "HSV")
    s_min = cv2.getTrackbarPos("SAT Min", "HSV")
    s_max = cv2.getTrackbarPos("SAT Max", "HSV")
    v_min = cv2.getTrackbarPos("VALUE Min", "HSV")
    v_max = cv2.getTrackbarPos("VALUE Max", "HSV")
    
# #     #
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    imgMask = cv2.inRange(imgHsv, lower, upper)     # 获取遮罩
    imgOutput = cv2.bitwise_and(img, img, mask=imgMask)
    imgMask = cv2.cvtColor(imgMask, cv2.COLOR_GRAY2BGR)     # 转换后，后期才能够与原画面拼接，否则与原图维数不同

    imgStack = np.hstack([img, imgOutput])
    cv2.namedWindow("imgMask",0)
    cv2.resizeWindow("imgMask",800,400)
    cv2.imshow('imgMask', imgStack)     # 显示
    if cv2.waitKey(pulse_ms) & 0xFF == ord('q'):          # 按下“q”推出（英文输入法）
        print("Quit\n")
        break

cap.release()
cv2.destroyAllWindows()

