import RPi.GPIO as GPIO
import BlynkLib
import requests
from time import sleep
import time
trig=5
echo=6
ir=25
buzzer=26
m1 = (17,18,27,22)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(trig,GPIO.OUT)
GPIO.setup(echo,GPIO.IN)
GPIO.setup(m1,GPIO.OUT)
GPIO.setup(ir,GPIO.IN)
GPIO.setup(buzzer,GPIO.OUT)

#Blynk details
blynk_auth= "UgLbiwEl86tnMjHUZpVwNZXUA56ccyxr"
blynk=BlynkLib.Blynk(blynk_auth)

@blynk.on("connected")
def connected():
    print(connected)
@blynk.on("disconnected")
def disconnected():
    blynk.connect()

def ultra():
    GPIO.output(trig,GPIO.LOW)
    sleep(2)
    GPIO.output(trig,GPIO.HIGH)
    sleep(0.00001)
    GPIO.output(trig,GPIO.LOW)
    while GPIO.input(echo)==0:
        e_start=time.time()
    while GPIO.input(echo)==1:
        e_stop=time.time()

    duration=e_stop - e_start
    global distance
    distance=round(duration*17150,2)
    thingspeak()
    blynk.virtual_write(6,distance)
    if distance<=20:
        blynk.virtual_write(5,1)
    else:
        blynk.virtual_write(5,0)
    print(distance)
    return distance

def detect():
    distance=ultra()
    GPIO.output(buzzer,GPIO.LOW)
    if (GPIO.input(ir)==0 and distance>20):
        print("hoo",GPIO.input(ir))
        forward()
        sleep(5)
        backward()
    elif (GPIO.input(ir)==0 and distance<=20):
        print("he;;",GPIO.input(ir))
        GPIO.output(buzzer,GPIO.HIGH)
      
def forward():
    b=0
    while b<950:
        GPIO.output(m1, (GPIO.LOW,GPIO.LOW,GPIO.LOW,GPIO.HIGH))  			
        sleep(0.002)
        GPIO.output(m1, (GPIO.LOW,GPIO.LOW,GPIO.HIGH,GPIO.LOW))
        sleep(0.002)
        GPIO.output(m1, (GPIO.LOW,GPIO.HIGH,GPIO.LOW,GPIO.LOW))
        sleep(0.002)
        GPIO.output(m1, (GPIO.HIGH,GPIO.LOW,GPIO.LOW,GPIO.LOW))
        sleep(0.002)
       
        b+=1
   
def backward():
    d=0
    while d<950:

        GPIO.output(m1, (GPIO.HIGH,GPIO.LOW,GPIO.LOW,GPIO.LOW))
        sleep(0.002)
        GPIO.output(m1, (GPIO.LOW,GPIO.HIGH,GPIO.LOW,GPIO.LOW))
        sleep(0.002)
        GPIO.output(m1, (GPIO.LOW,GPIO.LOW,GPIO.HIGH,GPIO.LOW))
        sleep(0.002)
        GPIO.output(m1, (GPIO.LOW,GPIO.LOW,GPIO.LOW,GPIO.HIGH))
        sleep(0.002)
        
        d+=1
def thingspeak():
    data={"api_key":"OPNVLQYQLK5KDB7V",
            "field3":distance}
    r=requests.get('https://api.thingspeak.com/update',params=data)
    if r.status_code == requests.codes.ok:
        print("data recived")
    else:
        print("error code"+str(r.status_code))
   
while True:
    ultra()
    blynk.run()
    

