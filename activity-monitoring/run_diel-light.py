# runs the motion.conf file present in the folder with the settings in the motion.conf file
import csv
import time
import os
import argparse
import yaml
import socket
import sys
import re
import shutil
import subprocess
from datetime import datetime as dt

# ── Resolve the directory this script lives in ──────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# ────────────────────────────────────────────────────────────────────────────

def get_os_version():
    """Return the major OS version, or None when os-release is unavailable."""
    try:
        with open('/etc/os-release', 'r') as file:
            os_release = file.read()
    except OSError:
        return None

    match = re.search(r'^VERSION_ID="?([0-9]+)', os_release, re.MULTILINE)
    return int(match.group(1)) if match else None


def resolve_path(path):
    """Resolve a config or output path consistently from the project directory."""
    expanded_path = os.path.expanduser(str(path))
    if os.path.isabs(expanded_path):
        return expanded_path

    project_path = os.path.join(SCRIPT_DIR, expanded_path)
    if os.path.exists(project_path) or not os.path.exists(expanded_path):
        return project_path
    return os.path.abspath(expanded_path)


version = get_os_version()


def get_args():
    """Parse command-line arguments for setup, execution, and path options."""
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
    parser.add_argument('--autorun',     default=False, action="store_true", help="Allow unattended run and automatic trial numbering")
    parser.add_argument('--silent',      default=False, action="store_true", help="Starts in non-interactive mode")
    args = parser.parse_args()
    return args


def get_time():
    """Print the system date and time used for the experiment."""
    today       = dt.now()
    date_string = dt.strftime(today, '%d %B %Y')
    time_string = dt.strftime(today, '%H:%M:%S')
    print("date is %s" % date_string)
    print("time is %s" % time_string)


def update_time():
    """Prompt for a new system time and apply it with the system date command."""
    string_date  = input("Input current date in YYYY-MM-DD HH:MM, for example 2020-04-28 13:35 ")
    command_time = "sudo date -s \"" + string_date + "\""
    os.system(command_time)
    print("time updated")


def get_last_trial(path):
    """Count direct trial directories to determine the next trial number."""
    trial_pattern = re.compile(r"_trial\d+$")
    return sum(
        os.path.isdir(os.path.join(path, name)) and trial_pattern.search(name)
        for name in os.listdir(path)
    )


def filesystem_name(value):
    """Replace whitespace in a generated file or directory name."""
    # Convert whitespace to underscores and remove unsupported characters.
    value = re.sub(r"\s+", "_", str(value).strip())
    return re.sub(r"[^A-Za-z0-9_-]", "", value)


def main():
    """Load configuration, prepare output, and run the motion experiment."""
    args = get_args()

    # -- Load project config --------------------------------------------------
    project_config_path = resolve_path(args.projectconf)
    with open(project_config_path) as yamlfile:
        config = yaml.load(yamlfile, Loader=yaml.FullLoader) or {}

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
    else:
        silent_mode = not config.get("INTERACTIVE", True)
        print("silent mode: ", silent_mode)

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
        motionconf = config.get("MOTIONPATH", "")
        print("CURRENT PROJECT PARAMETERS \n", ("-" * 20))
        print(" Name: {0} \n Initials: {1} \n Project: {2} \n Location: {3} \n Organism: {4} \n Motion configuration file: {5} "
              .format(name, ins, project, loc, org, motionconf))
        print("Project configuration file at: %s" % project_config_path)
        get_time()
        if exit_flag:
            sys.exit("Please modify project.conf file and restart workflow with --run flag")
        else:
            flag = input("Are details correct, press y to continue and n to exit: ")
            if flag == "n":
                sys.exit("Modify config file in project-configs/project.conf and restart")

    # -- Output directory -----------------------------------------------------
    # Output folder names are filesystem names, so whitespace is normalized.
    out_path = args.out if args.out else filesystem_name(config["OUTPATH"])

    # -- Autostart settings ---------------------------------------------------
    auto_start = args.autorun or config.get("AUTOSTART", False)
    if auto_start:
        start_on_boot    = True
        new_config_path  = os.path.join(resolve_path(out_path), "project_conf_log.txt")
        if os.path.exists(new_config_path):
            # TODO: Add commands to resume from log file
            pass
    else:
        start_on_boot = False

    # -- Run ------------------------------------------------------------------
    if args.run:
        if start_on_boot is False:
            sys.exit("Run with the --autorun flag or set AUTOSTART to True in the config file")

        scripts_path = os.path.join(SCRIPT_DIR, "scripts")
        subprocess.Popen([sys.executable, os.path.join(scripts_path, "save_run_time.py")])

        out_path = resolve_path(out_path)
        print("Output will be written to: ", out_path)

        if not os.path.isdir(out_path):
            print("Creating output directory")
            os.makedirs(out_path, exist_ok=True)

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
            trial_number = str(get_last_trial(out_path) + 1)
        else:
            trial_number = str(config.get("TRIALNUM", 0))

        # -- Trial naming -----------------------------------------------------
        # Trial names become folders, so whitespace is converted to underscores.
        trial_name = config["TRIALNAME"]
        if trial_name is None:
            pi_name        = socket.gethostname()
            today          = dt.now()
            date           = dt.strftime(today, '%Y_%m_%d')
            org            = filesystem_name(config["ORGANISM"])
            info_to_return = date + "_" + org + "_" + filesystem_name(pi_name)
        else:
            info_to_return = filesystem_name(trial_name)

        trial_name = info_to_return + "_trial" + trial_number.zfill(2)
        trial_dir  = os.path.join(out_path, trial_name)

        while os.path.isdir(trial_dir):
            if auto_start:
                trial_number = str(int(trial_number) + 1)
                trial_name = info_to_return + "_trial" + trial_number.zfill(2)
                trial_dir = os.path.join(out_path, trial_name)
                continue
            print("Directory exists, input a new trial number")
            trial_number = filesystem_name(input("Enter another trial number: "))
            trial_name   = info_to_return + "_trial" + trial_number.zfill(2)
            trial_dir    = os.path.join(out_path, trial_name)
        
        os.makedirs(trial_dir)
        os.chdir(trial_dir)

        # -- Motion config path -----------------------------------------------
        # Resolve relative config paths and quote them for shell commands.
        if args.motionconf:
            motion_path_abs = resolve_path(args.motionconf)
        else:
            motion_path_abs = resolve_path(config["MOTIONPATH"])

        # -- Run motion -------------------------------------------------------
        if version and version >= 11:
            print("Running commands for Bullseye and above...")
            if os.path.exists(motion_path_abs):
                libcamerify = shutil.which("libcamerify")
                if libcamerify is None:
                    sys.exit("libcamerify was not found. Install the Raspberry Pi camera compatibility package before running Motion.")
                command = [libcamerify, "motion", "-c", motion_path_abs, "-l", trial_name + "_log.txt"]
            else:
                sys.exit("Cannot find the Motion configuration file: " + motion_path_abs)
        else:
            print("Running commands for versions below Bullseye...")
            if os.path.exists(motion_path_abs):
                motion = shutil.which("motion")
                if motion is None:
                    sys.exit("motion was not found. Install Motion before running the experiment.")
                command = [motion, "-c", motion_path_abs, "-l", trial_name + "_log.txt"]
            else:
                sys.exit("Cannot find the Motion configuration file: " + motion_path_abs)

        print("Location at", os.getcwd())
        subprocess.run(command, check=True)
        os.chdir(SCRIPT_DIR)


if __name__ == '__main__':
    main()