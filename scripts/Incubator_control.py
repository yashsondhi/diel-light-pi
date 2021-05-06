import sys
import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import datetime
"Script to control incubator temperature"
# temp=25.0
log_fn = "./temp_log.csv"
temp_key = 1 # changes how temperature is checked, 0 takes an input 25, 1 takes reading from sensor
sensor = 22
pin = 4
set_temp = 25.0
temp_error = .2
# set defaults for day:night light cycle
day_start = 6
day_stop = 18
light_pin = 22
GPIO.setmode(GPIO.BOARD)
GPIO.setup(light_pin, GPIO.OUT)
class Light():
    def __init__(self, light_pin=light_pin):
        self.light_pin = light_pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.light_pin, GPIO.OUT)
        self.light_on = True
    def on(self):
        GPIO.output(self.light_pin, False)
        self.light_on = True
    def off(self):
        GPIO.output(self.light_pin, True)
        self.light_on = False
    def toggle(self):
        GPIO.output(self.light_pin, self.light_on)
        self.light_on = not self.light_on
light = Light()
# Creates GPIO for 
in1 = 16
in2 = 18
in3 = 13
in4 = 15
GPIO.setmode(GPIO.BOARD) #GPIO NUmbers instead of board numbers 
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)

def heat():
    time.sleep(2)
    GPIO.output(in1, False)
    GPIO.output(in2, False)
    time.sleep(5)
    GPIO.output(in3, True)
    GPIO.output(in4, True)
def cool():
    time.sleep(2)
    GPIO.output(in3, False)
    GPIO.output(in4, False)
    time.sleep(5)
    GPIO.output(in1, True)
    GPIO.output(in2, True)

def stop():
    GPIO.output(in3, False)
    GPIO.output(in4, False)
    time.sleep(5)
    GPIO.output(in1, False)
    GPIO.output(in2, False)

def find_temp():
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None: 
        print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
        s = "{},{},{}\n".format(str(datetime.datetime.now()),str(temperature),str(humidity))
    else:
        print('Failed to get reading. Try again!')
        s = "{},,\n".format(str(datetime.datetime.now()))
    with open(log_fn, 'a+') as log:
        log.write(s)
    return temperature

heat()
time.sleep(5)
cool()

def check(temp_key=temp_key):
    if(temp_key==0):
        "Returns temperature from sensor"
        temp = float(input("enter a temperature"))
    elif(temp_key==1):
        temp=find_temp()
    return temp

try:
    while True:
        current_temp=check()
        if current_temp is not None:
            if(current_temp > set_temp + temp_error):
                cool()
            elif(current_temp < set_temp - temp_error):
                heat()
            else:
                stop()
            if (datetime.datetime.now().hour >= day_start
                and datetime.datetime.now().hour < day_stop):
                if not light.light_on:
                    light.on()
            else:
                if light.light_on:
                    light.off()
except KeyboardInterrupt:
    GPIO.cleanup()




