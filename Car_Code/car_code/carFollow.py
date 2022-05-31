import cv2  # 导入库
import numpy as np
import time
import threading
import RPi.GPIO as GPIO
import pigpio
import os

import z_uart as myUart
import z_beep as myBeep
from math import *

TRIG = 17
ECHO = 18

# 启动脚本杀死影响程序的进程
os.system('./killmain.sh')

text_lower = np.array([13, 96, 119])
text_upper = np.array([23, 255, 255])

color_lower = text_lower  # 选择要识别的颜色
color_upper = text_upper

# 引脚定义
PIN_yuntai = 26
PIN_camera = 12

# 传感器引脚定义
PIN_pengzhuang1 = 23
PIN_pengzhuang2 = 3

# 蜂鸣器引脚定义
BEEP_PIN = 21

# 全局变量定义
c_x = 160
c_y = 120
x_bias = 0
y_bias = 0
area = 0
next_time = 50
pwm_value1 = 1400
pwm_value2 = 1900

systick_ms_bak = 0
# 使用之前,如果连接了摄像头，需要先关闭mjpg进程 ps -elf|grep mjpg  找到进程号，杀死进程  sudo kill -9 xxx   xxx代表进程号

# 类实例化
pi = pigpio.pi()

width = 320
hight = 240

cap = cv2.VideoCapture(0)  # 打开摄像头 最大范围 640×480
cap.set(3, width)  # 设置画面宽度
cap.set(4, hight)  # 设置画面高度

myBeep.setup_beep()
myUart.setup_uart(115200)

# 发出哔哔哔作为开机声音
myBeep.beep(0.1)
myBeep.beep(0.1)
myBeep.beep(0.1)

pi.set_servo_pulsewidth(PIN_yuntai, pwm_value1)
pi.set_servo_pulsewidth(PIN_camera, pwm_value2)

'''
csb
'''


def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def distance():
    err = 0
    GPIO.output(TRIG, 0)
    time.sleep(0.000002)

    GPIO.output(TRIG, 1)
    time.sleep(0.00001)
    GPIO.output(TRIG, 0)

    time0 = time.time()
    while GPIO.input(ECHO) == 0 and time.time() - time0 < 0.1:
        a = 0
    if time.time() - time0 >= 0.1:
        err = 1
        return 0

    time1 = time.time()
    while GPIO.input(ECHO) == 1 and time.time() - time1 < 0.1:
        a = 1

    if time.time() - time1 >= 0.1:
        err = 1
        return 0

    time2 = time.time()

    during = time2 - time1
    return during * 340 / 2 * 100


def destroy():
    GPIO.cleanup()


# csb chushihua
setup()  # csb setup

'''
pengzhuang
'''


# 初始化设备引脚
def setup_dev():
    GPIO.setup(PIN_pengzhuang1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(PIN_pengzhuang2, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# 读取devValue的值,触发为低电平
def devValue_left():
    return GPIO.input(PIN_pengzhuang1)


# 读取devValue的值,触发为低电平
def devValue_right():
    return GPIO.input(PIN_pengzhuang2)


def destory():
    beep_off()
    GPIO.cleanup()


# 蜂鸣器鸣叫
def beep_on():
    GPIO.output(BEEP_PIN, 1)


# 蜂鸣器关闭
def beep_off():
    GPIO.output(BEEP_PIN, 0)


def collision_detection_left():
    if (devValue_left() == 0):
        time.sleep(0.02)  # qu dou dong
        if (devValue_left() == 0):
            print(">Dev get Low")
            beep_on()

            while (devValue_left() == 0):
                car_left_turn()
                dis = distance()
                print('dis:%d cm' % dis)
                time.sleep(0.1)

            beep_off()
            print(">>>Dev get High")


def collision_detection_right():
    if (devValue_right() == 0):
        time.sleep(0.02)  # qu dou dong
        if (devValue_right() == 0):
            print(">Dev get Low")
            beep_on()

            while (devValue_right() == 0):
                car_right_turn()
                dis = distance()
                print('dis:%d cm' % dis)
                time.sleep(0.1)

            beep_off()
            print(">>>Dev get High")


# pengzhuang chushihua
setup_dev()

D = threading.Thread(target=collision_detection_left)
D.setDaemon(False)
D.start()

E = threading.Thread(target=collision_detection_right)
E.setDaemon(False)
E.start()


# 小车跟随
def car_follow():
    global systick_ms_bak, next_time, x_bias, y_bias, area
    while True:
        if int((time.time() * 1000)) - systick_ms_bak >= int(next_time):
            systick_ms_bak = int((time.time() * 1000))

            # print(int(x_bias),int(y_bias),int(area))
            if abs(x_bias) < 10 and area > 400:
                car_go_back(400)
                next_time = 0


            elif int(x_bias) > 10:
                next_time = 0
                interval_time = x_bias / 100
                car_left_turn()


            elif int(x_bias) < -10:
                next_time = 0
                interval_time = -x_bias / 100
                car_right_turn()


            elif area == 0:
                car_left_turn()
                time.sleep(0.5)

                car_stop()
                time.sleep(1)

                car_right_turn()
                time.sleep(0.5)

                car_stop()
                time.sleep(1)


'''
函数功能：串口发送指令控制电机转动
范围：-1000～+1000
'''


def car_run(speed_l1, speed_r1, speed_l2, speed_r2):
    textSrt = '#006P{:0>4d}T0000!#007P{:0>4d}T0000!#008P{:0>4d}T0000!#009P{:0>4d}T0000!'.format(speed_l1, speed_r1,
                                                                                                speed_l2, speed_r2)
    #     print(textSrt)
    myUart.uart_send_str(textSrt)


'''
函数功能：小车前进后退
正值小车前进，负值小车后退
范围：-1000～+1000
'''


def car_go_back(speed):
    car_run(1500 + speed, 1500 - speed, 1500 + speed, 1500 - speed)


'''
函数功能：小车左转
负值小车左转
范围：0～+1000

pwm 1500 == stop
'''


def car_left_turn():
    speed = 800
    speedl = 1500 + speed * 2 // 3
    speedr = 1500
    car_run(speedl, speedr, speedl, speedr)


'''
函数功能：小车右转
正值小车右转
范围：-1000～0
'''


def car_right_turn():
    speed = -800
    speedl = 1500
    speedr = 1500 + speed * 2 // 3
    car_run(speedl, speedr, speedl, speedr)


'''
函数功能：小车停止
'''


def car_stop():
    myUart.uart_send_str('#255P1500T1000!')


C = threading.Thread(target=car_follow)
C.setDaemon(True)
C.start()

# 无限循环
while 1:  # 进入无线循环
    collision_detection_left()
    # 将摄像头拍摄到的画面作为frame的值
    ret, frame = cap.read()
    # 高斯滤波GaussianBlur() 让图片模糊
    frame = cv2.GaussianBlur(frame, (5, 5), 0)
    # 将图片的色域转换为HSV的样式 以便检测
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, color_lower, color_upper)  # 设置阈值，去除背景 保留所设置的颜色
    # 显示腐蚀后的图像
    mask = cv2.erode(mask, None, iterations=2)

    # 高斯模糊
    mask = cv2.GaussianBlur(mask, (3, 3), 0)

    # 图像合并
    res = cv2.bitwise_and(frame, frame, mask=mask)

    # 边缘检测
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

    if len(cnts) > 0:  # 通过边缘检测来确定所识别物体的位置信息得到相对坐标

        cnt = max(cnts, key=cv2.contourArea)
        rect = cv2.minAreaRect(cnt)
        # 获取最小外接矩形的4个顶点
        box = cv2.boxPoints(rect)

        # 获取坐标 长宽 角度
        c_x, c_y = rect[0]
        c_h, c_w = rect[1]
        c_angle = rect[2]
        if c_angle < -45:
            c_angle = -(90 + c_angle)
        # 为了防止背景的干扰，限定识别到木块的像素值范围
        if 3 < c_h < 180 and 3 < c_w < 180:
            # 绘制轮廓
            cv2.drawContours(frame, [np.int0(box)], -1, (0, 255, 255), 2)
            x_bias = c_x - width / 2
            y_bias = c_y - hight / 2
            area = c_h * c_w
            # print(time.time(), 'x=', int(c_x), 'y=', int(c_y), 'c_h=', int(c_h), 'c_w=', int(c_w), 'angle=', int(c_angle))
    else:
        c_h = 0
        c_w = 0
        x_bias = 0
        y_bias = 0
        area = 0
    cv2.imshow('frame', frame)  # 将具体的测试效果显示出来

    # cv2.imshow('mask',mask)
    # cv2.imshow('res',res)
    if cv2.waitKey(5) & 0xFF == 27:  # 如果按了ESC就退出 当然也可以自己设置
        break

cap.release()
cv2.destroyAllWindows()  # 后面两句是常规操作,每次使用摄像头都需要这样设置一波
