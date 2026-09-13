# runs the motion.conf file present in the folder with the settings in the motion.conf file
import argparse
import os
import subprocess
import sys

import yaml

from run_helpers import (
    build_motion_command,
    display_setup,
    filesystem_name,
    get_last_trial,
    get_os_version,
    get_time,
    resolve_path,
    resolve_trial_name,
    update_time,
    write_config_log,
    write_run_log,
)

# ── Resolve the directory this script lives in ───────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# ─────────────────────────────────────────────────────────────────────────────

version = get_os_version()


def get_args():
    """Parse command-line arguments for setup, execution, and path options."""
    parser = argparse.ArgumentParser(
        usage="%(prog)s [options]",
        description="Run a diel activity monitoring experiment",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--time",  default=False, action="store_true", help="Force system time update")
    mode.add_argument("--setup", default=False, action="store_true", help="Update project setup")
    mode.add_argument("--run",   default=False, action="store_true", help="Runs the activity detector")

    parser.add_argument("--out",     default=False, help="Specify output directory")
    parser.add_argument(
        "--logfile",
        default=os.path.join(SCRIPT_DIR, "logs", "log_running_time.txt"),
        help="Write experiment start times to log",
    )
    parser.add_argument(
        "--motionconf",
        nargs="?",
        default=False,
        const=os.path.join(SCRIPT_DIR, "motion-configs", "motion.conf"),
        help="Config file to open",
    )
    parser.add_argument(
        "--projectconf",
        default=os.path.join(SCRIPT_DIR, "project-configs", "project.conf"),
        help="Input project config parameters",
    )
    parser.add_argument("--project", help="Input name of project")
    parser.add_argument("--autorun", default=False, action="store_true",
                        help="Allow unattended run and automatic trial numbering")
    parser.add_argument("--silent",  default=False, action="store_true",
                        help="Starts in non-interactive mode")
    return parser.parse_args()


def main():
    """Load configuration, prepare output, and run the motion experiment."""
    args = get_args()

    # -- Load project config --------------------------------------------------
    project_config_path = resolve_path(args.projectconf, SCRIPT_DIR)
    with open(project_config_path) as yamlfile:
        config = yaml.load(yamlfile, Loader=yaml.FullLoader) or {}

    # -- Project name ---------------------------------------------------------
    project = args.project if args.project else config["PROJECT"]
    print("Start activity detector on project: " + project)

    # -- Write to run log -----------------------------------------------------
    write_run_log(args.logfile, project)

    # -- Time update ----------------------------------------------------------
    if args.time:
        get_time()
        update_time()
        if input("Is time and date correct? ") == "n":
            update_time()
        sys.exit("Time updated -- restart workflow")

    # -- Silent mode ----------------------------------------------------------
    silent_mode = True if args.silent else not config.get("INTERACTIVE", True)
    print("silent mode: ", silent_mode)

    run_setup  = args.setup
    exit_flag  = True

    if not silent_mode:
        run_setup = True
        exit_flag = False

    # -- Setup display --------------------------------------------------------
    if run_setup:
        display_setup(config, project_config_path)
        if exit_flag:
            sys.exit("Please modify project.conf file and restart workflow with --run flag")
        else:
            if input("Are details correct, press y to continue and n to exit: ") == "n":
                sys.exit("Modify config file in project-configs/project.conf and restart")

    # -- Output directory -----------------------------------------------------
    out_path = args.out if args.out else filesystem_name(config["OUTPATH"])

    # -- Autostart settings ---------------------------------------------------
    auto_start = args.autorun or config.get("AUTOSTART", False)
    if auto_start:
        start_on_boot   = True
        new_config_path = os.path.join(resolve_path(out_path, SCRIPT_DIR), "project_conf_log.txt")
        if os.path.exists(new_config_path):
            # TODO: Add commands to resume from log file
            pass
    else:
        start_on_boot = False

    # -- Run ------------------------------------------------------------------
    if args.run:
        if not start_on_boot:
            sys.exit("Run with the --autorun flag or set AUTOSTART to True in the config file")

        scripts_path = os.path.join(SCRIPT_DIR, "scripts")
        subprocess.Popen([sys.executable, os.path.join(scripts_path, "save_run_time.py")])

        out_path = resolve_path(out_path, SCRIPT_DIR)
        print("Output will be written to: ", out_path)

        if not os.path.isdir(out_path):
            print("Creating output directory")
            os.makedirs(out_path, exist_ok=True)

        # -- Write config log -------------------------------------------------
        write_config_log(config, out_path, auto_start)

        # -- Trial naming and numbering ---------------------------------------
        auto_number = config.get("AUTONUMBER", auto_start)
        trial_name, trial_dir = resolve_trial_name(config, out_path, auto_number)

        os.makedirs(trial_dir)
        os.chdir(trial_dir)

        # -- Motion config path -----------------------------------------------
        if args.motionconf:
            motion_path_abs = resolve_path(args.motionconf, SCRIPT_DIR)
        else:
            motion_path_abs = resolve_path(config["MOTIONPATH"], SCRIPT_DIR)

        # -- Run motion -------------------------------------------------------
        command = build_motion_command(motion_path_abs, trial_name, version)
        print("Location at", os.getcwd())
        subprocess.run(command, check=True)
        os.chdir(SCRIPT_DIR)


if __name__ == "__main__":
    main()