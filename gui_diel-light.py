import tkinter as tk
from tkinter import filedialog
import yaml
import subprocess
import sys

config = {}  # Global dictionary to store the configuration options
project_conf_path = "configs/project.conf"  # Default project configuration file path

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
    project_conf_path=file_path

def save_config_file():
    file_path = filedialog.asksaveasfilename(filetypes=[("Conf Files", "*.conf")])
    if file_path:
        # Retrieve the values from the GUI elements and update the config dictionary accordingly
        config.update({
            "USER": experimenter_entry.get(),
            "INITIALS": initials_entry.get(),
            "PROJECT": project_entry.get(),
            "LOCATION": location_entry.get(),
            "ORGANISM": organism_entry.get(),
            "OUTPATH": output_entry.get(),
            "INTERACTIVE": interactive_var.get(),
            "AUTOSTART": auto_start_var.get(),
            "MOTIONPATH": config.get("MOTIONPATH", "configs/motion_best.conf"),  # Save the motion path to the config file
            # Add other configuration options and their values here
        })

        with open(file_path, "w") as file:
            yaml.dump(config, file)
    global project_conf_path
    project_conf_path=file_path
def run_experiment():
    # Retrieve the values from the GUI elements and run the experiment
    experimenter_name = experimenter_entry.get()
    experimenter_initials = initials_entry.get()
    project_name = project_entry.get()
    location = location_entry.get()
    organism = organism_entry.get()
    output_path = output_entry.get()
    interactive_mode = interactive_var.get()
    auto_start = auto_start_var.get()
    
    # Generate the Python command
    command = f"python3 run_diel-light.py --run --projectconf {project_conf_path} --motionconf {config.get('MOTIONPATH', 'configs/motion_best.conf')}"

    # Open a terminal window and execute the command
    if sys.platform.startswith("win"):  # For Windows
        subprocess.Popen(["cmd.exe", "/c", "start", "cmd.exe", "/k", command])
    elif sys.platform.startswith("darwin"):  # For macOS
        subprocess.Popen(["/usr/bin/open", "-n", "-F", "-a", "/Applications/Utilities/Terminal.app", command])
    elif sys.platform.startswith("linux"):  # For Linux
        subprocess.Popen(["x-terminal-emulator", "-e", command])

def update_gui_elements():
    # Update the GUI elements with the values from the config dictionary
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

    output_entry.delete(0, tk.END)
    output_entry.insert(tk.END, config.get("OUTPATH", ""))

    interactive_var.set(config.get("INTERACTIVE", True)) # by defult is set to True, turn off to enable auto start
    auto_start_var.set(config.get("AUTOSTART", False))

    motion_file_label.config(text=config.get("MOTIONPATH", "configs/motion_best.conf"))

# Create the main window
window = tk.Tk()
window.title("Activity Monitoring Experiment")

# Create Open Config File button
open_button = tk.Button(window, text="Open Config File", command=open_config_file)
open_button.pack()

# Create Config File Label
project_file_label = tk.Label(window, text="Open example file at diel-light-pi/"+project_conf_path)
project_file_label.pack()


# Create Open Motion File button
motion_button = tk.Button(window, text="Open Motion File", command=open_motion_file)
motion_button.pack()

# Create Motion File Label
motion_file_label = tk.Label(window, text=config.get("MOTIONPATH", "configs/motion_best.conf"))
motion_file_label.pack()


# Create Experimenter Name label and entry
experimenter_label = tk.Label(window, text="Experimenter Name:")
experimenter_label.pack()

experimenter_entry = tk.Entry(window)
experimenter_entry.pack()

# Create Experimenter Initials label and entry
initials_label = tk.Label(window, text="Experimenter Initials:")
initials_label.pack()

initials_entry = tk.Entry(window)
initials_entry.pack()

# Create Project Name label and entry
project_label = tk.Label(window, text="Project Name:")
project_label.pack()

project_entry = tk.Entry(window)
project_entry.pack()

# Create Location label and entry
location_label = tk.Label(window, text="Location:")
location_label.pack()

location_entry = tk.Entry(window)
location_entry.pack()

# Create Organism label and entry
organism_label = tk.Label(window, text="Organism:")
organism_label.pack()

organism_entry = tk.Entry(window)
organism_entry.pack()

# Create Output Path label and entry
output_label = tk.Label(window, text="Output Folder Name:")
output_label.pack()

output_entry = tk.Entry(window)
output_entry.pack()

# Create Interactive Mode checkbox

# Create Interactive Mode checkbox
interactive_var = tk.BooleanVar()
interactive_checkbox = tk.Checkbutton(window, text="Interactive Mode", variable=interactive_var)
interactive_checkbox.pack()


# Create Auto Start checkbox
auto_start_var = tk.BooleanVar()
auto_start_checkbox = tk.Checkbutton(window, text="Auto Start", variable=auto_start_var)
auto_start_checkbox.pack()

# Create Save Config File button
save_button = tk.Button(window, text="Save Config File", command=save_config_file)
save_button.pack()



# Create Run Experiment button
run_button = tk.Button(window, text="Run Experiment", command=run_experiment)
run_button.pack()

# Update the GUI elements with the initial values from the config dictionary
update_gui_elements()

# Run the main event loop
window.mainloop()
