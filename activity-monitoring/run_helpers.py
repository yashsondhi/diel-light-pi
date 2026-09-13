# experiment_helpers.py
"""
Pure utility functions for the diel activity monitoring experiment.
No global state — every function receives what it needs as parameters.
"""

import csv
import os
import re
import shutil
import socket
import subprocess
import sys
import time
from datetime import datetime as dt

import yaml


# ── OS / path helpers ────────────────────────────────────────────────────────

def get_os_version():
    """Return the major OS version, or None when os-release is unavailable."""
    try:
        with open("/etc/os-release", "r") as fh:
            os_release = fh.read()
    except OSError:
        return None

    match = re.search(r'^VERSION_ID="?([0-9]+)', os_release, re.MULTILINE)
    return int(match.group(1)) if match else None


def resolve_path(path, script_dir):
    """Resolve a config or output path consistently from the project directory."""
    expanded = os.path.expanduser(str(path))
    if os.path.isabs(expanded):
        return expanded

    project_path = os.path.join(script_dir, expanded)
    if os.path.exists(project_path) or not os.path.exists(expanded):
        return project_path
    return os.path.abspath(expanded)


def filesystem_name(value):
    """Replace whitespace in a generated file or directory name."""
    value = re.sub(r"\s+", "_", str(value).strip())
    return re.sub(r"[^A-Za-z0-9_-]", "", value)


# ── Trial helpers ─────────────────────────────────────────────────────────────

def get_last_trial(path):
    """Count direct trial directories to determine the next trial number."""
    trial_pattern = re.compile(r"_trial\d+$")
    return sum(
        os.path.isdir(os.path.join(path, name)) and trial_pattern.search(name)
        for name in os.listdir(path)
    )


def resolve_trial_name(config, out_path, auto_number):
    """
    Build the full trial directory path, incrementing as needed to avoid
    collisions.

    Returns:
        tuple[str, str]: (trial_name, trial_dir)
    """
    trial_name_raw = config.get("TRIALNAME")

    if trial_name_raw is None:
        pi_name = socket.gethostname()
        today   = dt.now()
        date    = dt.strftime(today, "%Y_%m_%d")
        org     = filesystem_name(config["ORGANISM"])
        base    = date + "_" + org + "_" + filesystem_name(pi_name)
    else:
        base = filesystem_name(trial_name_raw)

    if auto_number:
        trial_number = str(get_last_trial(out_path) + 1)
    else:
        trial_number = str(config.get("TRIALNUM", 0))

    trial_name = base + "_trial" + trial_number.zfill(2)
    trial_dir  = os.path.join(out_path, trial_name)

    while os.path.isdir(trial_dir):
        if auto_number:
            trial_number = str(int(trial_number) + 1)
        else:
            print("Directory exists, input a new trial number")
            trial_number = filesystem_name(input("Enter another trial number: "))
        trial_name = base + "_trial" + trial_number.zfill(2)
        trial_dir  = os.path.join(out_path, trial_name)

    return trial_name, trial_dir


# ── Time helpers ──────────────────────────────────────────────────────────────

def get_time():
    """Print the system date and time used for the experiment."""
    today = dt.now()
    print("date is %s" % dt.strftime(today, "%d %B %Y"))
    print("time is %s" % dt.strftime(today, "%H:%M:%S"))


def update_time():
    """Prompt for a new system time and apply it with the system date command."""
    string_date  = input("Input current date in YYYY-MM-DD HH:MM, for example 2020-04-28 13:35 ")
    command_time = 'sudo date -s "' + string_date + '"'
    os.system(command_time)
    print("time updated")


# ── Logging helpers ───────────────────────────────────────────────────────────

def write_run_log(logfile, project):
    """Append the project name and start time to the run log."""
    log_dir = os.path.dirname(logfile)
    os.makedirs(log_dir, exist_ok=True)
    with open(logfile, "a+") as fh:
        fh.write("\nProject name: " + project + "\n")
        fh.write("Start time: "    + time.ctime() + "\n")


def write_config_log(config, out_path, auto_start):
    """
    Write a snapshot of the active configuration to project_conf_log.txt
    inside the output directory.
    """
    log_path = os.path.join(out_path, "project_conf_log.txt")
    with open(log_path, "w+") as fh:
        for item, doc in config.items():
            if item == "TRIALNUM":
                fh.write("TRIALNUM: " + str(get_last_trial(out_path) + 1) + "\n")
            elif item == "AUTOSTART":
                fh.write("AUTOSTART:" + str(auto_start) + "\n")
            else:
                fh.write(str(item) + ":" + str(doc) + "\n")


# ── Setup display ─────────────────────────────────────────────────────────────

def display_setup(config, project_config_path):
    """Print the current project parameters to the console."""
    print("CURRENT PROJECT PARAMETERS \n", ("-" * 20))
    print(
        " Name: {0} \n Initials: {1} \n Project: {2} \n"
        " Location: {3} \n Organism: {4} \n Motion configuration file: {5} "
        .format(
            config["USER"],
            config["INITIALS"],
            config["PROJECT"],
            config["LOCATION"],
            config["ORGANISM"],
            config.get("MOTIONPATH", ""),
        )
    )
    print("Project configuration file at: %s" % project_config_path)
    get_time()


# ── Motion runner ─────────────────────────────────────────────────────────────

def build_motion_command(motion_path_abs, trial_name, version):
    """
    Return the shell command list for the appropriate Motion invocation.

    Raises:
        SystemExit: when the binary or config file cannot be found.
    """
    if not os.path.exists(motion_path_abs):
        sys.exit("Cannot find the Motion configuration file: " + motion_path_abs)

    log_arg = trial_name + "_log.txt"

    if version and version >= 11:
        print("Running commands for Bullseye and above...")
        binary = shutil.which("libcamerify")
        if binary is None:
            sys.exit(
                "libcamerify was not found. "
                "Install the Raspberry Pi camera compatibility package before running Motion."
            )
        return [binary, "motion", "-c", motion_path_abs, "-l", log_arg]

    print("Running commands for versions below Bullseye...")
    binary = shutil.which("motion")
    if binary is None:
        sys.exit("motion was not found. Install Motion before running the experiment.")
    return [binary, "-c", motion_path_abs, "-l", log_arg]