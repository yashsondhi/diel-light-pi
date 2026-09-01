import tkinter as tk
from tkinter import filedialog
import yaml
import subprocess
import sys
import os

# ── Resolve the directory this script lives in ──────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# ────────────────────────────────────────────────────────────────────────────

config = {}  # Global dictionary to store the configuration options

# ✅ Fixed: paths now relative to SCRIPT_DIR and new folder structure
DEFAULT_MOTION_PATH  = os.path.join(SCRIPT_DIR, 'motion-configs', 'motion_best.conf')
DEFAULT_PROJECT_CONF = os.path.join(SCRIPT_DIR, 'project-configs', 'project.conf')
MAIN_SCRIPT          = os.path.join(SCRIPT_DIR, 'run_diel-light.py')

project_conf_path = DEFAULT_PROJECT_CONF  # updated when user opens/saves a config


def open_config_file():
    file_path = filedialog.askopenfilename(filetypes=[("Conf Files", "*.conf")])
    if file_path:
        with open(file_path, "r") as file:
            config.update(yaml.safe_load(file))
            update_gui_elements()

def open_motion_file():
    file_path = filedialog.askopenfilename(filetypes=[("Conf Files", "*.conf")])
    if file_path:
        config["MOTIONPATH"] = file_path
        motion_file_label.config(text=file_path)
        global project_conf_path
        project_conf_path = file_path  # ✅ Fixed: moved inside if block

def save_config_file():
    file_path = filedialog.asksaveasfilename(filetypes=[("Conf Files", "*.conf")])
    if file_path:
        config.update({
            "USER":        experimenter_entry.get(),
            "INITIALS":    initials_entry.get(),
            "PROJECT":     project_entry.get(),
            "LOCATION":    location_entry.get(),
            "ORGANISM":    organism_entry.get(),
            "OUTPATH":     output_entry.get(),
            "TRIALNAME":   trial_name_entry.get(),
            "TRIALNUM":    trial_num_entry.get(),
            "INTERACTIVE": interactive_var.get(),
            "AUTOSTART":   auto_start_var.get(),
            "MOTIONPATH":  config.get("MOTIONPATH", DEFAULT_MOTION_PATH),  # ✅ Fixed
        })
        with open(file_path, "w") as file:
            yaml.dump(config, file)
        global project_conf_path
        project_conf_path = file_path

def run_experiment():
    motion_path = config.get("MOTIONPATH", DEFAULT_MOTION_PATH)  # ✅ Fixed

    # ✅ Fixed: MAIN_SCRIPT points to run_diel-light.py via SCRIPT_DIR
    command = f"python3 {MAIN_SCRIPT} --run --projectconf {project_conf_path} --motionconf {motion_path}"

    # Open a terminal window and execute the command
    if sys.platform.startswith("win"):      # For Windows
        subprocess.Popen(["cmd.exe", "/c", "start", "cmd.exe", "/k", command])
    elif sys.platform.startswith("darwin"): # For macOS
        subprocess.Popen(["/usr/bin/open", "-n", "-F", "-a", "/Applications/Utilities/Terminal.app", command])
    elif sys.platform.startswith("linux"):  # For Linux
        subprocess.Popen(["x-terminal-emulator", "-e", command])

def update_gui_elements():
    experimenter_entry.delete(0, tk.END)
    experimenter_entry.insert(tk.END, config.get("USER", ""))

    initials_entry.delete(0, tk.END)
    initials_entry.insert(tk.END, config.get("INITIALS", ""))

    project_entry.delete(0, tk.END)
    project_entry.insert(tk.END, config.get("PROJECT", ""))

    location_entry.delete(0, tk.END)
    location_entry.insert(tk.END, config.get("LOCATION", ""))

    organism_entry.delete(0, tk.END)
    organism_entry.insert(tk.END, config.get("ORGANISM", ""))

    trial_name_entry.delete(0, tk.END)
    trial_name_entry.insert(tk.END, config.get("TRIALNAME", ""))

    trial_num_entry.delete(0, tk.END)
    trial_num_entry.insert(tk.END, config.get("TRIALNUM", ""))

    output_entry.delete(0, tk.END)
    output_entry.insert(tk.END, config.get("OUTPATH", ""))

    interactive_var.set(config.get("INTERACTIVE", True))
    auto_start_var.set(config.get("AUTOSTART", True))

    motion_file_label.config(text=config.get("MOTIONPATH", DEFAULT_MOTION_PATH))  # ✅ Fixed


# ── Build the GUI ────────────────────────────────────────────────────────────

window = tk.Tk()
window.title("Activity Monitoring Experiment")

# Open Config File
open_button = tk.Button(window, text="Open Config File", command=open_config_file)
open_button.pack()

# ✅ Fixed: label now shows the correct absolute default path
project_file_label = tk.Label(window, text="Default config: " + DEFAULT_PROJECT_CONF)
project_file_label.pack()

# Open Motion File
motion_button = tk.Button(window, text="Open Motion File", command=open_motion_file)
motion_button.pack()

# ✅ Fixed: label uses DEFAULT_MOTION_PATH
motion_file_label = tk.Label(window, text=DEFAULT_MOTION_PATH)
motion_file_label.pack()

# Experimenter Name
experimenter_label = tk.Label(window, text="Experimenter Name:")
experimenter_label.pack()
experimenter_entry = tk.Entry(window)
experimenter_entry.pack()

# Experimenter Initials
initials_label = tk.Label(window, text="Experimenter Initials:")
initials_label.pack()
initials_entry = tk.Entry(window)
initials_entry.pack()

# Project Name
project_label = tk.Label(window, text="Project Name:")
project_label.pack()
project_entry = tk.Entry(window)
project_entry.pack()

# Location
location_label = tk.Label(window, text="Location:")
location_label.pack()
location_entry = tk.Entry(window)
location_entry.pack()

# Organism
organism_label = tk.Label(window, text="Organism:")
organism_label.pack()
organism_entry = tk.Entry(window)
organism_entry.pack()

# Output Path
output_label = tk.Label(window, text="Output Folder Name:")
output_label.pack()
output_entry = tk.Entry(window)
output_entry.pack()

# Trial Name
trial_name_label = tk.Label(window, text="Trial Name:")
trial_name_label.pack()
trial_name_entry = tk.Entry(window)
trial_name_entry.pack()

# Trial Number
trial_num_label = tk.Label(window, text="Trial Num:")
trial_num_label.pack()
trial_num_entry = tk.Entry(window)
trial_num_entry.pack()

# Interactive Mode
interactive_var = tk.BooleanVar()
interactive_checkbox = tk.Checkbutton(window, text="Interactive Mode", variable=interactive_var)
interactive_checkbox.pack()

# Auto Start
auto_start_var = tk.BooleanVar()
auto_start_checkbox = tk.Checkbutton(window, text="Auto Start", variable=auto_start_var)
auto_start_checkbox.pack()

# Save Config File
save_button = tk.Button(window, text="Save Config File", command=save_config_file)
save_button.pack()

# Run Experiment
run_button = tk.Button(window, text="Run Experiment", command=run_experiment)
run_button.pack()

# Populate GUI with defaults
update_gui_elements()

# Start event loop
window.mainloop()