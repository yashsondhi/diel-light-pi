import csv
import adafruit_tsl2591
import time
import os
# creates a script to save pi running time for each trial
path="/home/pi/Desktop/diel-light-pi/logs/"

frequency = 60
    
filename="log_pi_time.txt"
log_pi_time_file = open(path+filename, 'a+') # create a new file
localtime = time.asctime(time.localtime(time.time())) #Saves local time in a specific format
line_header=["Pi_on_time",localtime]
#import pdb; pdb.set_trace()

# write header file 
with log_pi_time_file:
	writer = csv.writer(log_pi_time_file)
	writer.writerow(line_header)

# Record system time every x second
while True:
    # Saves local time in file
    appendFile = open(path+filename, 'a+')
    with appendFile:
        writer =csv.writer(appendFile)
        line_content=["Pi_run_time",localtime]
        writer.writerow(line_content)

    time.sleep(frequency)

