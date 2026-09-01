# runs the motion.conf file present in the folder with the settings in the motion.conf file
import csv
import time
import os
import argparse
import yaml
import socket
import sys
from datetime import datetime as dt
import pdb

# ── Resolve the directory this script lives in ──────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# ────────────────────────────────────────────────────────────────────────────

# Read the contents of the /etc/os-release file
with open('/etc/os-release', 'r') as file:
    os_release = file.read()

# Extract the version information from the file
version = None
for line in os_release.splitlines():
    if line.startswith('VERSION_ID='):
        version = line.split('=')[1].strip('"\'')


def get_args():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(usage='%(prog)s [options]', description="Run a diel activity monitoring experiment")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--time',    default=False, action="store_true", help='Force system time update')
    mode.add_argument('--setup',   default=False, action="store_true", help='Update project setup')
    mode.add_argument('--run',     default=False, action="store_true", help='Runs the activity detector')
    parser.add_argument('--out',         default=False, help='Specify output directory')
    parser.add_argument('--logfile',     default=os.path.join(SCRIPT_DIR, 'logs', 'log_running_time.txt'),
                                         help='Write experiment start times to log')
    parser.add_argument('--motionconf',  nargs='?', default=False,
                                         const=os.path.join(SCRIPT_DIR, 'motion-configs', 'motion.conf'),
                                         help='Config file to open')
    parser.add_argument('--projectconf', default=os.path.join(SCRIPT_DIR, 'project-configs', 'project.conf'),
                                         help='Input project config parameters')
    parser.add_argument('--project',     help="Input name of project")
    parser.add_argument('--autorun',     default=False, action="store_true", help="Starts automatically on reboot")
    parser.add_argument('--silent',      default=False, action="store_true", help="Starts in non-interactive mode")
    args = parser.parse_args()
    return args


def get_time():
    today       = dt.now()
    date_string = dt.strftime(today, '%d %B %Y')
    time_string = dt.strftime(today, '%H:%M:%S')
    print("date is %s" % date_string)
    print("time is %s" % time_string)


def update_time():
    string_date  = input("Input current date in YYYY-MM-DD HH:MM, for example 2020-04-28 13:35 ")
    command_time = "sudo date -s \"" + string_date + "\""
    os.system(command_time)
    print("time updated")


def get_last_trial(path):
    totalDir = 0
    for base, dirs, files in os.walk(path):
        for directories in dirs:
            totalDir += 1
    return totalDir


def main():
    """Main function of the script"""
    args = get_args()

    # -- Load project config --------------------------------------------------
    with open(args.projectconf) as yamlfile:
        config = yaml.load(yamlfile, Loader=yaml.FullLoader)

    # -- Project name ---------------------------------------------------------
    project = args.project if args.project else config["PROJECT"]
    print("Start activity detector on project: " + project)

    # -- Write to run log -----------------------------------------------------
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(args.logfile)
    os.makedirs(log_dir, exist_ok=True)

    file_log_time = open(args.logfile, "a+")
    file_log_time.write("\nProject name: " + project + "\n")
    file_log_time.write("Start time: "    + time.ctime() + "\n")
    file_log_time.close()

    # -- Time update ----------------------------------------------------------
    if args.time:
        get_time()
        update_time()
        flag = input("Is time and date correct? ")
        if flag == "n":
            update_time()
        sys.exit("Time updated -- restart workflow")

    # -- Silent mode ----------------------------------------------------------
    if args.silent:
        silent_mode = True
        print("silent mode: ", silent_mode)
    elif "INTERACTIVE" in config:
        silent_mode = not config["INTERACTIVE"]
        print("silent mode: ", silent_mode)
    else:
        silent_mode = False

    run_setup  = args.setup
    exit_flag  = True

    if not silent_mode:
        run_setup = True
        exit_flag = False

    # -- Setup display --------------------------------------------------------
    if run_setup:
        name       = config["USER"]
        ins        = config["INITIALS"]
        project    = config["PROJECT"]
        loc        = config["LOCATION"]
        org        = config["ORGANISM"]
        motionconf = config["MOTIONPATH"]
        print("CURRENT PROJECT PARAMETERS \n", ("-" * 20))
        print(" Name: {0} \n Initials: {1} \n Project: {2} \n Location: {3} \n Organism: {4} \n Motion configuration file: {5} "
              .format(name, ins, project, loc, org, motionconf))
        print("Project configuration file at: %s" % args.projectconf)
        get_time()
        if exit_flag:
            sys.exit("Please modify project.conf file and restart workflow with --run flag")
        else:
            flag = input("Are details correct, press y to continue and n to exit: ")
            if flag == "n":
                sys.exit("Modify config file in project-configs/project.conf and restart")

    # -- Output directory -----------------------------------------------------
    out_path = args.out if args.out else config["OUTPATH"]

    # -- Autostart settings ---------------------------------------------------
    if args.autorun or config["AUTOSTART"]:
        start_on_boot    = True
        new_config_path  = os.path.join(out_path, "project_conf_log.txt")
        if os.path.exists(new_config_path):
            # TODO: Add commands to resume from log file
            pass
    else:
        start_on_boot = False

    # -- Run ------------------------------------------------------------------
    if args.run:
        if start_on_boot is False:
            sys.exit("Run with the --autorun flag or set AUTOSTART to True in the config file")

        # ✅ Fixed: use SCRIPT_DIR to find save_run_time.py in scripts/
        scripts_path = os.path.join(SCRIPT_DIR, "scripts")
        call_pi      = "python3 " + os.path.join(scripts_path, "save_run_time.py") + " &"
        os.system(call_pi)

        print("Output will be written to: ", out_path)

        if os.path.isdir(out_path):
            os.chdir(out_path)
            out_path = os.getcwd()
        else:
            print("Creating output directory")
            os.mkdir(out_path)
            os.chdir(out_path)
            out_path = os.getcwd()

        auto_start = args.autorun or config["AUTOSTART"]

        # -- Write config log -------------------------------------------------
        out_config = open("project_conf_log.txt", "w+")
        for item, doc in config.items():
            if item == "TRIALNUM":
                line = "TRIALNUM: " + str(get_last_trial(out_path) + 1) + "\n"
                out_config.writelines(line)
            elif item == "AUTOSTART":
                line = "AUTOSTART:" + str(auto_start) + "\n"
                out_config.writelines(line)
            else:
                line = item, ":", str(doc) + "\n"
                out_config.writelines(line)
        out_config.close()

        # -- Trial numbering --------------------------------------------------
        if auto_start:
            trial_number = "0" + str(get_last_trial(out_path) + 1)
        else:
            trial_number = "0" + str(config["TRIALNUM"])

        # -- Trial naming -----------------------------------------------------
        trial_name = config["TRIALNAME"]
        if trial_name is None:
            pi_name        = socket.gethostname()
            today          = dt.now()
            date           = dt.strftime(today, '%Y_%m_%d')
            org            = config["ORGANISM"]
            info_to_return = date + "_" + org + "_" + pi_name
        else:
            info_to_return = trial_name

        trial_name = info_to_return + "_trial" + trial_number
        trial_dir  = os.path.join(out_path, trial_name)

        if os.path.isdir(trial_dir):
            print("Directory exists, input a new trial number")
            trial_number = input("Enter another trial number: ")
            trial_name   = info_to_return + "_trial" + trial_number
            trial_dir    = os.path.join(out_path, trial_name)
        
        os.mkdir(trial_dir)
        os.chdir(trial_dir)

        # -- Motion config path -----------------------------------------------
        # ✅ Fixed: resolve motion config relative to SCRIPT_DIR
        if args.motionconf:
            motion_path_abs = args.motionconf if os.path.isabs(args.motionconf) \
                              else os.path.join(SCRIPT_DIR, args.motionconf)
        else:
            motion_path_abs = os.path.join(SCRIPT_DIR, config["MOTIONPATH"])

        # -- Run motion -------------------------------------------------------
        if version and int(version) >= 11:
            print("Running commands for Bullseye and above...")
            if os.path.exists(motion_path_abs):
                command = "libcamerify motion -c " + motion_path_abs + " -l " + trial_name + "_log.txt"
            else:
                print("Cannot find motion.conf file -- running from motion.conf installed in bash")
                command = "libcamerify motion -l trial" + trial_number
        else:
            print("Running commands for versions below Bullseye...")
            if os.path.exists(motion_path_abs):
                command = "motion -c " + motion_path_abs + " -l " + trial_name + "_log.txt"
            else:
                print("Cannot find motion.conf file -- running from motion.conf installed in bash")
                command = "motion -l trial" + trial_number

        print("Location at", os.getcwd())
        os.system(command)
        os.chdir(SCRIPT_DIR)  # ✅ Fixed: return to SCRIPT_DIR instead of os.getcwd()


if __name__ == '__main__':
    main()