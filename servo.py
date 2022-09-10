import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode (GPIO.BCM)

GPIO.setup(12,GPIO.OUT)
servo1 = GPIO.PWM(12,50)  #50Hz

#mulai running pwm
servo1.start(0)
time.sleep(2)

duty = 2

print ("90 derajat ")
servo1.ChangeDutyCycle(7)
time.sleep(10)
print("turning kembali 0 derajat")
servo1.ChangeDutyCycle(2)
time.sleep(2)
servo1.ChangeDutyCycle(0)
servo1.stop()
GPIO.cleanup()