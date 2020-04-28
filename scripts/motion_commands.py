#runs the motion.conf file present in the  folder with the settings  in the motion.conf file

import csv
import time
import os

#trial number = Trial_number a string value for the trial number this currently is 
trial_number= input("Enter a Trial number ")

#time_lapse_period =Input time_lapse period in milliseconds

#To be implenent check if directory exists, if it does throw and error

#Create a directory with filen name trialno

if os.path.isdir("trial"+trial_number):
    print("Directory exists, input a new trial number")
    trial_number= input("Enter a Trial number ")
else:
    os.system("mkdir trial"+trial_number)
os.chdir("trial"+trial_number)

command="motion -c ../motion.conf -l trial"+trial_number+"_log.txt"
print(command)
os.system(command)

os.chdir("..")




