#导包
import RPi.GPIO as GPIO
import time

#端口模式设置
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
  
#引脚定义  
BEEP_PIN = 21

#蜂鸣器鸣叫
def on():
    GPIO.output(BEEP_PIN, 1)
    
#蜂鸣器关闭
def off():
    GPIO.output(BEEP_PIN, 0)
    

#蜂鸣器端口反转
def flip():
    GPIO.output(BEEP_PIN, not GPIO.input(BEEP_PIN))

#间接发出响声，x代表间接的时间，单位为秒
def beep(x):
    on()
    time.sleep(x)
    off()
    time.sleep(x)

#初始化蜂鸣器
def setup_beep():
    GPIO.setup(BEEP_PIN, GPIO.OUT, initial = 0)

#循环蜂鸣器，间隔1秒响一次
def loop_beep():
    beep(0.1)

#程序反复执行处
if __name__ == "__main__":
    setup_beep()
    #发出哔哔哔作为开机声音
    beep(0.1)
    beep(0.1)
    beep(0.1)
    try:
        while True:
            loop_beep()
    except KeyboardInterrupt:
        off()
