import dht11
import time
import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM)
GPIO.setup(20 ,GPIO.OUT) #kipas
GPIO.setup(9 ,GPIO.OUT) #lampu

# if __name__ == '__main__':
#     x = []
#     for i in range(5):
#         x.append(dht11.ambil())
#         time.sleep(0.2)

def panasDingin(suhu):
        if suhu <= 29:
            GPIO.output(9, GPIO.HIGH) #lampu
            GPIO.output(20, GPIO.LOW) #kipas
            return "masih Dingin"
        elif suhu >= 31:
            GPIO.output(9, GPIO.LOW)
            GPIO.output(20, GPIO.HIGH)
            return "sudah Panas"
        else:
            GPIO.output(9, GPIO.HIGH)
            GPIO.output(20, GPIO.HIGH)
            return "stabil"
# try:
#       while True:
#         lembab,suhu = dht11.ambil()
#         print("%0.1f*C, kondisi "%(suhu) + panasDingin(suhu))
# except KeyboardInterrupt:
#         print("Measurement stopped by User")
#         GPIO.output(9, GPIO.LOW)
#         GPIO.output(20, GPIO.LOW)
#         GPIO.cleanup()
