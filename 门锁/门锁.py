# -*- coding:utf-8 -*-
import time
import RPi.GPIO as GPIO
import urllib.request
from PIL import Image
import os, signal, subprocess
#初始化
GPIO.setmode(GPIO.BCM)
#超声波
GPIO.setup(24, GPIO.OUT)
GPIO.setup(23, GPIO.IN)
#LED
GPIO.setup(25, GPIO.OUT)
#继电器
GPIO.setup(8, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
#超声波读取距离函数
def checkdist():
    GPIO.output(25, True)
    time.sleep(0.03)
    GPIO.output(25, False)
    GPIO.output(24, GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(24,GPIO.LOW)
    while not GPIO.input(23):
        pass
    t1 = time.time()
    while GPIO.input(23):
        pass
    t2 = time.time()
    return (t2-t1)*340/2
#开、关门函数
def downPower():
    GPIO.output(8, False)
    GPIO.output(21, False)
def openDoor():
    GPIO.output(21, True)
    time.sleep(3)
    GPIO.output(21, False)
def closeDoor():
    GPIO.output(8, True)
    time.sleep(3)
    GPIO.output(8, False)
#二维码读取函数
def lesen():
    #拍摄一幅图像
    os.system("raspistill -w 640 -h 480 -o /home/pi/cameraqrc/image.jpg -t 100 ")
    print ("raspistill finished")
    #处理图像以方便读取
    im = Image.open("/home/pi/cameraqrc/image.jpg").rotate(180).convert("L").save("/home/pi/cameraqrc/image-1.jpg")
    GPIO.output(25, True)
    time.sleep(0.1)
    GPIO.output(25, False)
     
    #读取二维码
    zbarcam=subprocess.Popen("zbarimg --raw /home/pi/cameraqrc/image-1.jpg", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
    qrcodetext=zbarcam.stdout.readline()
         
    return qrcodetext
#主函数
def havePhone():
    urlc = "https://xxx.flyhigher.top/checkkey/?lock_id=test001"
    content = urllib.request.urlopen(urlc).read().decode("utf-8")
    print(content)
    if content == "true":
        result=lesen().strip().decode("utf-8")
        print(result)
        if result != '':
            headers = { 'User-Agent' : 'Lock/Beta1'}
            urld="https://xxx.flyhigher.top/ifkey/"
            pdata={'lock_id':'test001','passw':result}
            pdata=urllib.parse.urlencode(pdata)
            binary_data = pdata.encode('ascii')
            print('Checking!')
            req = urllib.request.Request(urld, binary_data, headers)
            fd = urllib.request.urlopen(req).read().decode("utf-8")
            print(fd)
            if fd == "test001":
                print("开门")
                downPower()
                openDoor()
                time.sleep(7)
                print("关门")
                downPower()
                closeDoor()
            else:
                print("Wrong!")
        else:
            print('Continue!')
   #方便调试时关机
    elif content == "die":
        print('Yes!')
        os.system("sudo shutdown")
#主循环
while True:
    dis = checkdist()*100
    print(dis)
    if dis <= 30:
        havePhone()
    time.sleep(0.5)