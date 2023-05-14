#runs the motion.conf file present in the  folder with the settings  in the motion.conf file
import csv
import time
import os
import argparse
import yaml
import socket
import sys
from datetime import datetime as dt
import pdb
#trial number = Trial_number a string value for the trial number this currently is 

# Read the contents of the /etc/os-release file
with open('/etc/os-release', 'r') as file:
    os_release = file.read()

# Extract the version information from the file
version = None
for line in os_release.splitlines():
    if line.startswith('VERSION_ID='):
        version = line.split('=')[1].strip('"\'')

# Check if the version is Bullseye or above (assuming version numbers like "11", "12", etc.)



def get_args():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(usage='%(prog)s [options]', description="Run an diel activity monitoring experiment")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--time', default=False, action="store_true", help='Force system time update')
    mode.add_argument('--setup', default=False, action="store_true",help='Update project update')
    mode.add_argument('--run',default=False,action="store_true", help='Runs the activity detector')
    parser.add_argument('--out',default=False, help='Specify output directory')
    parser.add_argument('--logfile', default='logs/log_running_time.txt', help='Write experiment start times to Log')
    parser.add_argument('--motionconf',nargs='?',default=False,const="configs/motion.conf",help='Config file to open')
    parser.add_argument('--projectconf',default='configs/project.conf', help='Input project config parameters')
    parser.add_argument('--project',help="Input name of project")
    parser.add_argument('--autorun',default=False, action="store_true",help ="starts automatically on reboot")
    parser.add_argument('--silent',default=False, action="store_true",help ="starts in non interactive mode")
    args = parser.parse_args()
    return (args)

#To be implenent check if directory exists, if it does throw and error

#Create a directory with file name trial 
def get_time():
    today= dt.now()
    date_string =dt.strftime(today, '%d %B %Y')
    time_string= dt.strftime(today, '%H:%M:%S')
    print("date is %s"% date_string)
    print("time is %s"% time_string)
    
def update_time():
    string_date=input("Input current date in YYYY-MM-DD HH:MM, for example 2020-04-28 13:35 ")
    #sets time
    command_time="sudo date -s \""+string_date+"\""
    #command_time = "sudo date -s \"2020-04-28 13:35\""
    os.system(command_time)
    print("time updated")
def get_last_trial(path):
    #counts total number
    totalDir=0
    for base, dirs, files in os.walk(path):
        for directories in dirs:
            totalDir += 1
    return totalDir
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
    file_log_time.close()
    
    #Check and update time
    if args.time:
        get_time()
        update_time()
        flag=input("Is time and date correct")
        if flag=="n":
            update_time()
        sys.exit("Time updated restart workflow")
   
    #turns on silent mode
    if args.silent:
        silent_mode = True
        print("silent mode: ",silent_mode)
    elif "INTERACTIVE" in config:
        silent_mode = not config["INTERACTIVE"]
        print("silent mode: ",silent_mode)
    else:
        silent_mode = False
        
    run_setup=args.setup

    exit_flag=True
    if not silent_mode:
    	run_setup=True
    	exit_flag=False

        #forces setup ,but skips exit setup

    if run_setup:
        # modify using https://myopswork.com/parsing-yaml-files-with-python-5aa0d4e2613f
        #Store config variable
        name=config["USER"]
        ins=config["INITIALS"]
        project=config["PROJECT"]
        loc=config["LOCATION"]
        org=config["ORGANISM"]
        motionconf=config["MOTIONPATH"]
        print("CURRENT PROJECT PARAMETERS \n",("-"*20))
        #outputs current setup parameters
        print(" Name: {0} \n Initials: {1} \n Project: {2} \n Location: {3} \n Organism: {4} \n Motion configuration file: {5} ".format(name,ins,project,loc,org,motionconf))
        print("Project configuration file at :%s"%args.projectconf)
        get_time()
        if exit_flag: # interactive mode on by default
            sys.exit("Please modify project.conf file and restart workflow with --run flag")
        else:
            flag=input("Are details correct, press y to continue and n to exit : ")
            if(flag=="n"):
                sys.exit("Modify config file configs/project.conf and restart")

    #Set the output directory
    if args.out:
        out_path=args.out
    else:
        out_path=config["OUTPATH"]
    
    #Settings to ensure autoboot
    
    if args.autorun or config["AUTOSTART"]:
        start_on_boot=True
        #TODO: Adds text to load new yaml file
        new_config_path=out_path+"project_conf_log.txt"
        if os.path.exists(new_config_path):
            #TODO: Add commands to resume from log file
            #with open(new_confif_path) as yamlfile:
        		#config = yaml.load(yamlfile, Loader=yaml.FullLoader)
            pass
    else:
        start_on_boot=False
    if args.run:
        if start_on_boot is False:
            sys.exit("Run with the --autorun tab or change --autorun to True in the config file")
        # call scripts that saves pi running time save_pi_time file
        #Gets base path
        base_path=os.getcwd()
        #tells pi where save_run time script is to save pi data every minute
        home_path=base_path+"/scripts/"
        call_pi="python3 "+home_path+"save_run_time.py"+ "&"
        os.system(call_pi) # tells pi to save data
        log=args.logfile
        #gets current date and time NEED TO ADD TO FILE
        today = dt.today()
        
        
        print("Output will be written to: ",out_path)
        if os.path.isdir(out_path):
            os.chdir(out_path)
            out_path=os.getcwd()
        else:
            print("Creating output directory")
            os.mkdir(out_path)
            os.chdir(out_path)
            out_path=os.getcwd()
        auto_start=args.autorun or config["AUTOSTART"]
        out_config = open("project_conf_log.txt","w+") #re-writes old output but saves a config file     
        for item, doc in config.items():  # get items from config file
            if(item == "TRIALNUM"):
                line="TRIALNUM: "+str(get_last_trial(out_path)+1)+"\n"
                out_config.writelines(line)
            elif(item == "AUTOSTART"):
                line="AUTOSTART:" +str(auto_start)+"\n"
                out_config.writelines(line)    
            else:
                line=item, ":", str(doc)+"\n"
                out_config.writelines(line)
            #yaml.dump(config,out_config) ##Write to file with new parameter
        out_config.close() ## close the file
        
        #NEED TO UNCOMMENT ON PI
        #run motion commands script uncomment out if not running on pi
        #os.chdir(base_path)
        ####Create trial directory
        
        if auto_start:
            trial_number = "0"+str(get_last_trial(out_path)+1)
        else:
            trial_number= "0"+str(config["TRIALNUM"])
        # create directory, before checking if it already exists
        
        #gets info for trial name
        trial_name=config["TRIALNAME"]
        if trial_name == None :
            pi_name=socket.gethostname()
            today= dt.now()
            date =dt.strftime(today,'%Y_%m_%d')
            org=config["ORGANISM"]
            info_to_return=date+"_"+org+"_"+pi_name
        else:
            info_to_return=trial_name
        
        info = info_to_return #autfill text
        trial_name=info+"_trial"+trial_number
        trial_dir=out_path+"/"+trial_name
        
        if os.path.isdir(trial_dir):
            print("Directory exists, input a new trial number")
            trial_number= input("Enter another Trial number ")
        else:
            os.mkdir(trial_dir)
        os.chdir(trial_dir)
        
        #Absoloute motion conf path
        if args.motionconf:
            motion_path_rel=args.motionconf
        else:
            motion_path_rel=config["MOTIONPATH"]
            
        motion_path_abs=base_path+"/"+motion_path_rel
        
        if version and int(version) >= 11:
        # Commands for Bullseye and above
        print("Running commands for Bullseye and above...")
        # Add your commands here for Bullseye and above

        else:
            # Commands for versions below Bullseye
            print("Running commands for versions below Bullseye...")
            # Add your commands here for versions below Bullseye

        
        
        if os.path.exists(motion_path_rel):
            command="libcamerify motion -c "+motion_path_rel+" -l "+trial_name+"_log.txt"
        elif os.path.exists(motion_path_abs):
            command="libcamerify motion -c "+motion_path_abs+" -l "+trial_name+"_log.txt"
        else :
            print("Cannot find motion.conf file running from motion.conf installed in bash")
            command="libcamerify motion "+" -l trial"+trial_number 
        print("Following command will be executed",command)
        
        print("Location at",os.getcwd())
        os.system(command)
        ##Create folder for directory and run the config file or 
        #command="python3 "+current_path+"/scripts/motion_commands.py --motionconf "+motion_path_rel
        os.chdir(base_path)
        #os.system(command)

    


if __name__ == '__main__':
    main()
