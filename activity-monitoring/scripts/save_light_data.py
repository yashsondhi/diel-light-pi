import board
import busio
import csv
import adafruit_tsl2591
import time



# creates a script to save images and light data in a csv file


# Initialize the I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)
# Initialize the sensor.
sensor = adafruit_tsl2591.TSL2591(i2c)
sensor_gain_input=input("Input gain low, medium, high or max ")
                        
if sensor_gain_input == "low":
                        sensor.gain = adafruit_tsl2591.GAIN_LOW
elif sensor_gain_input == "med":
                        sensor.gain = adafruit_tsl2591.GAIN_MED
elif sensor_gain_input == "high":
                        sensor.gain = adafruit_tsl2591.GAIN_HIGH
elif sensor_gain_input == "max":
                        sensor.gain = adafruit_tsl2591.GAIN_MAX
else:
                        sensor.gain = adafruit_tsl2591.GAIN_MED

sensor_integrationtime_input=int(input("Input sensor intehration time (100,200,300,400,500,600) "))
if sensor_integrationtime_input == 100:
                        sensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_100MS
elif sensor_integrationtime_input == 200:
                        sensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_200MS
elif sensor_integrationtime_input == 300:
                        sensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_300MS
elif sensor_integrationtime_input == 400:
                        sensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_400MS
elif sensor_integrationtime_input == 500:
                        sensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_500MS
elif sensor_integrationtime_input == 600:
                        sensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_600MS
else:
                        sensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_100MS




# You can optionally change the gain and integration time:

# You can optionally change the gain and integration time:
#sensor.gain = adafruit_tsl2591.GAIN_LOW (1x gain)
#sensor.gain = adafruit_tsl2591.GAIN_MED (25x gain, the default)
#sensor.gain = adafruit_tsl2591.GAIN_HIGH (428x gain)
#sensor.gain = adafruit_tsl2591.GAIN_MAX (9876x gain)
#sensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_100MS (100ms, default)
#sensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_200MS (200ms)
#sensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_300MS (300ms)
#sensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_400MS (400ms)
#sensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_500MS (500ms)
#sensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_600MS (600ms)




trial_number= input("Enter a Trial number ")

frequency = float(input("Enter frequency to store light reading "))

if (frequency < 0.0):
    frequency = 1.0

filename= "trial "+trial_number+".csv"

myFile = open(filename, 'w') # create a new file
localtime = time.asctime(time.localtime(time.time())) #Saves local time in a specifivc format
print(sensor_integrationtime_input)
myData=[["##TLight sensor data from TSL2591. Trial number {0}".format(trial_number),"Sensor Gain {0}".format(sensor_gain_input),"Sensor intergration time {0}".format(str(sensor_integrationtime_input))],["lux","infrared","visible","full spectrum","localtime"]]
print(frequency)
#import pdb; pdb.set_trace()

with myFile:
	writer = csv.writer(myFile)
	writer.writerows(myData)
    
# Read the total lux, IR, and visible light levels and print it every second.
while True:
    # Read and calculate the light level in lux.
    lux = sensor.lux
    print('Total light: {0}lux'.format(lux))
    # You can also read the raw infrared and visible light levels.
    # These are unsigned, the higher the number the more light of that type.
    # There are no units like lux.
    # Infrared levels range from 0-65535 (16-bit)
    infrared = sensor.infrared
    print('Infrared light: {0}'.format(infrared))
    # Visible-only levels range from 0-2147483647 (32-bit)
    visible = sensor.visible
    print('Visible light: {0}'.format(visible))
    # Full spectrum (visible + IR) also range from 0-2147483647 (32-bit)
    full_spectrum = sensor.full_spectrum
    print('Full spectrum (IR + visible) light: {0}'.format(full_spectrum))
    data_entry=[lux,infrared,visible,full_spectrum,time.asctime(time.localtime(time.time()))]
    appendFile = open(filename, 'a')
    with appendFile:
        writer =csv.writer(appendFile)
        writer.writerow(data_entry)

    time.sleep(frequency)

