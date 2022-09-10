#!/usr/bin/env python
import time
import requests
import math
import random
import os
import glob
import RPi.GPIO as GPIO
# import telepot
# from telepot.loop import MessageLoop


from kipaslampu import panasDingin
from ultrasound import distance
from dht11 import ambil

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(9 ,GPIO.OUT) #lampu
GPIO.setup(20 ,GPIO.OUT) #kipas
GPIO.setup(21,GPIO.IN) #TELUR
telur = 0
total = 0
telurlewat = False

#set GPIO servo
servoPIN = 12
GPIO.setup(servoPIN, GPIO.OUT)
servo1 = GPIO.PWM(12,50)  #50Hz
servo1.start(0)
time.sleep(2)
duty = 2

#set GPIO Pins untuk ketinggian air
GPIO_TRIGGER = 23
GPIO_ECHO = 24

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(25, GPIO.OUT)

TOKEN = "BBFF-es28iG81T1Vs7Z6JGtil3jeB2yt2zb"  # Put your TOKEN here
DEVICE_LABEL = "smaciho"  # Put your device label here 
VARIABLE_LABEL_1 = "suhuudara"  # Put your first variable label here
VARIABLE_LABEL_2 = "telur"  # Put your second variable label here
VARIABLE_LABEL_3 = "ketinggianair"  # Put your second variable label here
VARIABLE_LABEL_4 = "makan"  # Put your second variable label here


def build_payload(variable_1, variable_2,variable_3): # jumlah parameter sesual dengan jumlah data yg akan dikirim
    global telur 
    # Baca jarak dari sensor ultrasonik
    print("payload")
    dist = distance()
    print(dist)
    
    # Baca suhu dan kelembaban dari DHT11
    kelembaban_udara,suhu_udara = ambil()
    #----------------------------------------------------
    
    print ("Measured Distance = %.1f cm" % dist)
    payload = {}
    if suhu_udara != None:
        if suhu_udara != 0:
            panasDingin(suhu_udara)
            payload =   {variable_1: suhu_udara,
                         variable_2: telur,
                         variable_3: dist,
                        #  variable_4: 0               
                        }
        else:
            payload = {variable_1: 0,
                       variable_2: 0,
                       variable_3: 0,
                    #    variable_4: 0
                       }
    
    #------------------------------------------------------
    return payload
def get_request(nama_variabel_ubidots):
    # Creates the headers for the HTTP requests
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}/{}/lv".format(url, DEVICE_LABEL,nama_variabel_ubidots)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}
    # https://industrial.api.ubidots.com/api/v1.6/devices/<device_label>/<variable_label>/lv
    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.get(url=url, headers=headers)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    # Processes results
    print(req.status_code, req.text)
    nilai_variabel_ubidots = req.text 
    print("Nilai variable di ubidots {} = {} type : {}".format(nama_variabel_ubidots,nilai_variabel_ubidots,type(nilai_variabel_ubidots)))

    if status >= 400:
        print("[ERROR] Could not get data after 5 attempts, please check \
            your token credentials and internet connection")
        return None

    return nilai_variabel_ubidots

def get_request(nama_variabel_ubidots):
    # Creates the headers for the HTTP requests
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}/{}/lv".format(url, DEVICE_LABEL,nama_variabel_ubidots)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}
    # https://industrial.api.ubidots.com/api/v1.6/devices/<device_label>/<variable_label>/lv
    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.get(url=url, headers=headers)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    # Processes results
    print(req.status_code, req.text)
    nilai_variabel_ubidots = int(float(req.text)) 
    print("Nilai variable di ubidots {} = {} ".format(nama_variabel_ubidots,nilai_variabel_ubidots))

    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return None

    return nilai_variabel_ubidots


def post_request(payload):
    # Creates the headers for the HTTP requests
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    # Processes results
    print(req.status_code, req.json())
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    print("[INFO] request made properly, your device is updated")
    return True

def main():
    global telurlewat
    global telur
    global total
    print("main")
        # Menghitung telur
    sensor=GPIO.input(21)
    print(sensor)
    print("global telurlewat : "+str(telurlewat))
    print("global telur : "+str(telur))
    print("global total : "+str(total))
    if (sensor==1) and ( telurlewat==False):
        telur = telur + 1
        total = total + 1
        print("telur : "+str(telur))
        print("total : "+str(total))
        telurlewat = True
    elif(sensor==0 and telurlewat==True):
        telurlewat = False
        
    payload = build_payload(
                                                VARIABLE_LABEL_1, 
                                                VARIABLE_LABEL_2,
                                                VARIABLE_LABEL_3,
                                                )
    print(payload)

    print("[INFO] Attemping to send data")

    # Mengukur suhu udara
    if payload['suhuudara'] != 0:
        payload = {}
        post_request(payload)
        print("[INFO] finished")
    else:
        print("[INFO] sensor suhu tidak terbaca")

    # Mengukur ketinggian air minum
    dist = distance()
    print(dist)
    if dist < 100:
       print("Air akan penuh")
       GPIO.output(25, True);
       time.sleep(60)
    else:
       GPIO.output(25, False);
        # Reset by pressing CTRL + C
    
    # Menyalakan servo untuk makanan
    servo = get_request(VARIABLE_LABEL_4)
    print ("SERVO BUKA ")
    servo1.ChangeDutyCycle(7)
    time.sleep(10)
    print("TUTUP")
    servo1.ChangeDutyCycle(2)
    time.sleep(2)
    servo1.ChangeDutyCycle(0)
    servo1.stop()
    
# Ini adalah bagian utama program
if __name__ == '__main__':
    try:
        print("mulai")
        while (True):
            main()

    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.output(20, GPIO.HIGH)
        GPIO.output(9, GPIO.HIGH)
        GPIO.cleanup()