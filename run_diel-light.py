#runs the motion.conf file present in the  folder with the settings  in the motion.conf file

import csv
import time
import os
import argparse
breakpoint()
#trial number = Trial_number a string value for the trial number this currently is 
trial_number= input("Enter a Trial number ")

def get_args():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(usage='%(prog)s [options]', description="Run an diel activity monitoring experiment")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--time', default=False, action="store_true", help='Force system time update')
    parser.add_argument('--logfile', default="logs/log_running_time.txt", help='Log file to write logs to')
    parser.add_argument('--motionconf', default='configs/motion.conf', help='Config file to open')
    parser.add_argument('--projectconf',default='configs/project.conf' help='Input project parameters')
    parser.add_argument('--reference', choices=["transcriptome", "genome"], help='Reference to use')
    parser.add_argument('--dea', default=False, action="store_true", help='Perform dea')
    parser.add_argument('--visualize', action="store_true", help='Perform visualization')
    args = parser.parse_args()
    return (args)
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

def main()
    """Main function of the script"""
    args=get_args()
    # Parameters to control the workflow
    with open(args.config) as yamlfile:
        config = yaml.load(yamlfile, Loader=yaml.FullLoader)
    # Project
    if args.project:
        project = args.project
    else:
        project = config["PROJECT"]

    command="motion -c "+args.config+" -l trial"+trial_number+args.logfile"_log.txt"
