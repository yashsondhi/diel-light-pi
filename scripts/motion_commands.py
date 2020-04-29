#runs the motion.conf file present in the  folder with the settings  in the motion.conf file

import csv
import time
import os
from datetime import datetime as dt


#convert to argumetns
flag_set_date= True

def get_date():
    today= dt.now()
    date_string =dt.strftime(today, '%d %B %Y')
    time_string= dt.strftime(today, '%H:%M:%S')
    print("date is %s"% date_string)
    print("time is %s"% time_string)
def set_date():
    string_date=input("Input current date in YYYY-MM-DD HH:MM, for example 2020-04-28 13:35 ")
    #sets time
    command_time="sudo date -s \""+string_date+"\""
    #command_time = "sudo date -s \"2020-04-28 13:35\""
    os.system(command_time)
    print("done")

#trial number = Trial_number a string value for the trial number this currently is 
get_date()
print("Please check date and time, if the rasberry pi is not connected to the internet please run with flag -st to ensure date is correct")

if flag_set_date:
    set_date()
    print("updated date is: ")
    get_date()
    check_date=input("Is this date and time correct (y/n)")
    if(check_date is "n"):
        set_date()

             
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

command="motion -c ./configs/motion.conf -l trial"+trial_number+"_log.txt"
print(command)
os.system(command)

os.chdir("..")




