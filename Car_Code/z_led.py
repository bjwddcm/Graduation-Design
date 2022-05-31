#导包
import RPi.GPIO as GPIO
import time

#端口模式设置
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#引脚定义
LED1_PIN = 5
LED2_PIN = 26

#全局变量
systick_ms_bak = 0

#点亮LED 参数led_pin 为引脚编号
def on(led_pin):
    if led_pin == 1:
        GPIO.output(LED1_PIN, 0)
    elif led_pin == 2:
        GPIO.output(LED2_PIN, 0)

#熄灭LED 参数led_pin 为引脚编号
def off(led_pin):
    if led_pin == 1:
        GPIO.output(LED1_PIN, 1)
    elif led_pin == 2:
        GPIO.output(LED2_PIN, 1)

#反转LED 参数led_pin 为引脚编号
def flip(led_pin):
    if led_pin == 1:
        GPIO.output(LED1_PIN, not GPIO.input(LED1_PIN))
    elif led_pin == 2:
        GPIO.output(LED2_PIN, not GPIO.input(LED2_PIN))

#初始化LED灯
def setup_led():
    GPIO.setup(LED1_PIN, GPIO.OUT, initial = 0)
    GPIO.setup(LED2_PIN, GPIO.OUT, initial = 1)


#大循环LED灯
def loop_led():
    global systick_ms_bak
    if(int((time.time() * 1000))- systick_ms_bak > 500):
        systick_ms_bak = int((time.time() * 1000))
        flip(2)

#程序反复执行处
if __name__ == "__main__":
    setup_led()
    try:
        while True:
            loop_led()
    except KeyboardInterrupt:
        off(1)
        off(2)
