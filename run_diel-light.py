#runs the motion.conf file present in the  folder with the settings  in the motion.conf file

import csv
import time
import os
import argparse
import yaml
import sys
from datetime import date
import pdb
#trial number = Trial_number a string value for the trial number this currently is 

def get_args():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(usage='%(prog)s [options]', description="Run an diel activity monitoring experiment")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--time', default=False, action="store_true", help='Force system time update')
    mode.add_argument('--setup', default=False, action="store_true",help='Update project update')
    mode.add_argument('--run',default=False,action="store_true", help='Runs the activity detector')
    parser.add_argument('--out',default=False, help='Specify output directory')
    parser.add_argument('--logfile', default='logs/log_running_time.txt', help='Log file to write logs to')
    parser.add_argument('--motionconf', default='configs/motion.conf', help='Config file to open')
    parser.add_argument('--projectconf',default='configs/project.conf', help='Input project config parameters')
    parser.add_argument('--project',help="Input name of project")
    #parser.add_argument('--size', choices=["t", "genome"], help='Reference to use')
    #parser.add_argument('--dea', default=False, action="store_true", help='Perform dea')
    #parser.add_argument('--visualize', action="store_true", help='Perform visualization')
    args = parser.parse_args()
    return (args)

#To be implenent check if directory exists, if it does throw and error

#Create a directory with filen name trial no


def main():
    """Main function of the script"""
    args=get_args()
    # Input project metadata
    with open(args.projectconf) as yamlfile:
        config = yaml.load(yamlfile, Loader=yaml.FullLoader)
    # Input project name
    if args.project:
        project = args.project
    else:
        project = config["PROJECT"]
    print("Start activity detector on project: " + project)
    #Write data to project run log
    file_log_time = open(args.logfile, "a+")
    file_log_time.write("\nProject name: " + project + "\n")
    file_log_time.write("Start time: " + time.ctime() + "\n")
    #Check and update time
    if args.time:
        get_time()
        update_time()
        flag=input("Is time and date correct")
        if flag=="n":
            update_time()
        sys.exit("Time updated restart workflow")

    if args.setup:
        # NEED TO FIX add parameters
        # modify using https://myopswork.com/parsing-yaml-files-with-python-5aa0d4e2613f
        #Store config variable
        name=config["USER"]
        ins=config["INITIALS"]
        project=config["PROJECT"]
        loc=config["LOCATION"]
        print("CURRENT PROJECT PARAMETERS \n",("-"*20))
        #outputs current setup parameters
        print(" Name: {0} \n Initials: {1} \n Project: {2} \n Location: {3}".format(name,ins,project,loc))
        print("Project configuration file at :%s"%args.projectconf)
        sys.exit("Please modify project.conf file and restart workflow with -r flag")
    
    #Set the output directory
    if args.out:
        out_path=args.out
    else:
        out_path=config["OUTPATH"]
    if args.run:
        log=args.logfile
        #gets current date and time NEED TO ADD TO FILE
        today = date.today()
        base_path=os.getcwd()
        print("Output will be written to: ",out_path)
        if os.path.isdir(out_path):
            os.chdir(out_path)
            out_path=os.getcwd()
        else:
            print("Creating output directory")
            os.mkdir(out_path)
            os.chdir(out_path)
            out_path=os.getcwd()
            
        out_config = open("out.yml","w+") #re-writes old output but saves a config file 
        yaml.dump(config,out_config) ##Write to file with new parameter
        out_config.close() ## close the file
        #NEED TO UNCOMMENT ON PI
        #run motion commands script uncomment out if not running on pi
        #os.chdir(base_path)
        
        ####Create trial direcotry
        trial_number= input("Enter a Trial number ")
        # create directory, before checking if it already exists
        trial_dir=out_path+"/trial"+trial_number
        if os.path.isdir(trial_dir):
            print("Directory exists, input a new trial number")
            trial_number= input("Enter another Trial number ")
        else:
            os.mkdir(trial_dir)
        
        os.chdir(trial_dir)
        #Absoloute motion conf path
        motion_path_abs=base_path+"/"+args.motionconf
        
        if os.path.exists(args.motionconf):
            command="motion -c "+args.motionconf+" -l "+trial_dir+"/"+trial_number+"_log.txt"
        elif os.path.exists(motion_path_abs):
            command="motion -c "+motion_path_abs+" -l "+trial_dir+"/"+trial_number+"log.txt"
        else :
            print("Cannot find motion.conf file running from motion.conf installed in bash")
            command="motion "+" -l trial"+trial_number 
        print("Following command will be executed",command)
        print("Location at",os.getcwd())
        os.system(command)
        ##Create folder for directory and run the config file or 
        #command="python3 "+current_path+"/scripts/motion_commands.py --motionconf "+args.motionconf
        os.chdir(base_path)
        #os.system(command)

    file_log_time.write("Finish time: " + time.ctime() + "\n")
    file_log_time.close()


if __name__ == '__main__':
    main()
