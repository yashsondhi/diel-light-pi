import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import yaml
import subprocess
import sys
import os
import re

# ── Resolve the directory this script lives in ──────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# ────────────────────────────────────────────────────────────────────────────

config = {}  # Global dictionary to store the configuration options

DEFAULT_MOTION_PATH  = os.path.join(SCRIPT_DIR, 'motion-configs', 'motion_best.conf')
DEFAULT_PROJECT_CONF = os.path.join(SCRIPT_DIR, 'project-configs', 'project.conf')
TEMPLATE_PROJECT_CONF = os.path.join(SCRIPT_DIR, 'project-configs', 'template_project.conf')
MAIN_SCRIPT          = os.path.join(SCRIPT_DIR, 'run_diel-light.py')

project_conf_path = DEFAULT_PROJECT_CONF  # updated when user opens/saves a config
config_dirty = False
run_button = None
status_var = None
status_label = None


class QuotedStringDumper(yaml.SafeDumper):
    pass


def represent_quoted_string(dumper, value):
    """Represent a Python string as a double-quoted YAML scalar."""
    return dumper.represent_scalar("tag:yaml.org,2002:str", value, style='"')


QuotedStringDumper.add_representer(str, represent_quoted_string)


def gui_text(value):
    """Convert a configuration value into text suitable for an Entry widget."""
    if value is None:
        return ""
    return str(value)


def normalize_input(value, folder_name=False):
    """Keep allowed characters and optionally convert whitespace to underscores."""
    value = str(value)
    if folder_name:
        value = re.sub(r"\s+", "_", value)
        return re.sub(r"[^A-Za-z0-9_-]", "", value)
    return re.sub(r"[^A-Za-z0-9_\- ]", "", value)


def handle_entry_change(event, entry, folder_name=False):
    """Normalize an edited field and mark the configuration as unsaved."""
    current_value = entry.get()
    updated_value = normalize_input(current_value, folder_name)
    if current_value != updated_value:
        cursor_position = entry.index(tk.INSERT)
        entry.delete(0, tk.END)
        entry.insert(0, updated_value)
        entry.icursor(min(cursor_position, len(updated_value)))
    mark_config_dirty()


def normalize_entry_spaces(entry):
    """Normalize the value of an existing Entry widget."""
    current_value = entry.get()
    updated_value = normalize_input(current_value, folder_name=True)
    if current_value != updated_value:
        entry.delete(0, tk.END)
        entry.insert(0, updated_value)


def mark_config_dirty():
    """Disable running until the current form values have been saved."""
    global config_dirty
    config_dirty = True
    if run_button is not None:
        run_button.config(state=tk.DISABLED)
    if status_var is not None:
        status_var.set("Unsaved changes - save the project before running")
    if status_label is not None:
        status_label.configure(style="Unsaved.Status.TLabel")


def mark_config_saved():
    """Mark the form as saved and allow the experiment to run."""
    global config_dirty
    config_dirty = False
    if run_button is not None:
        run_button.config(state=tk.NORMAL)
    if status_var is not None:
        status_var.set("Ready to run")
    if status_label is not None:
        status_label.configure(style="Ready.Status.TLabel")


def finish_save():
    """Complete deferred save-state updates after the file dialog closes."""
    mark_config_saved()
    save_button.focus_set()


def load_default_config():
    """Load project.conf or fall back to the starter project template."""
    # Use a saved project when available; otherwise load the starter template.
    default_path = DEFAULT_PROJECT_CONF
    if not os.path.exists(default_path):
        default_path = TEMPLATE_PROJECT_CONF

    if os.path.exists(default_path):
        with open(default_path, "r") as file:
            loaded_config = yaml.safe_load(file) or {}
        config.update(loaded_config)
        return default_path

    return DEFAULT_PROJECT_CONF


def open_config_file():
    """Open a project configuration and populate the form with its values."""
    file_path = filedialog.askopenfilename(
        filetypes=[("Conf Files", "*.conf")],
        initialdir=os.path.join(SCRIPT_DIR, 'project-configs'),
    )
    if file_path:
        with open(file_path, "r") as file:
            config.update(yaml.safe_load(file))
            update_gui_elements()
            mark_config_saved()

def open_motion_file():
    """Select the motion configuration used by the next experiment run."""
    file_path = filedialog.askopenfilename(
        filetypes=[("Conf Files", "*.conf")],
        initialdir=os.path.join(SCRIPT_DIR, 'motion-configs'),
    )
    if file_path:
        config["MOTIONPATH"] = file_path
        motion_file_label.config(text=file_path)
        global project_conf_path
        project_conf_path = file_path
        mark_config_dirty()

def save_config_file():
    """Collect, normalize, and save the current experiment configuration."""
    file_path = filedialog.asksaveasfilename(
        filetypes=[("Conf Files", "*.conf")],
        initialdir=os.path.join(SCRIPT_DIR, 'project-configs'),
    )
    if file_path:
        # Copy the current form values into the config before writing the file.
        config.update({
            "USER":        normalize_input(experimenter_entry.get()),
            "INITIALS":    normalize_input(initials_entry.get()),
            "PROJECT":     normalize_input(project_entry.get()),
            "LOCATION":    normalize_input(location_entry.get()),
            "ORGANISM":    normalize_input(organism_entry.get()),
            "OUTPATH":     normalize_input(output_entry.get(), folder_name=True),
            "TRIALNAME":   normalize_input(trial_name_entry.get(), folder_name=True),
            "TRIALNUM":    normalize_input(trial_num_entry.get(), folder_name=True),
            "INTERACTIVE": interactive_var.get(),
            "AUTOSTART":   auto_start_var.get(),
            "MOTIONPATH":  config.get("MOTIONPATH", DEFAULT_MOTION_PATH),
        })
        # Keep strings readable and typed values such as booleans unchanged.
        with open(file_path, "w") as file:
            yaml.dump(config, file, Dumper=QuotedStringDumper, sort_keys=False)
        global project_conf_path
        project_conf_path = file_path
        window.after_idle(finish_save)

def run_experiment():
    """Launch the experiment runner in a platform-appropriate terminal."""
    motion_path = config.get("MOTIONPATH", DEFAULT_MOTION_PATH)

    command = f"python3 {MAIN_SCRIPT} --run --projectconf {project_conf_path} --motionconf {motion_path}"

    # Open a terminal window and execute the command
    if sys.platform.startswith("win"):      # For Windows
        subprocess.Popen(["cmd.exe", "/c", "start", "cmd.exe", "/k", command])
    elif sys.platform.startswith("darwin"): # For macOS
        subprocess.Popen(["/usr/bin/open", "-n", "-F", "-a", "/Applications/Utilities/Terminal.app", command])
    elif sys.platform.startswith("linux"):  # For Linux
        subprocess.Popen(["x-terminal-emulator", "-e", command])

def update_gui_elements():
    """Refresh all form controls from the current configuration dictionary."""
    experimenter_entry.delete(0, tk.END)
    experimenter_entry.insert(tk.END, normalize_input(gui_text(config.get("USER", ""))))

    initials_entry.delete(0, tk.END)
    initials_entry.insert(tk.END, normalize_input(gui_text(config.get("INITIALS", ""))))

    project_entry.delete(0, tk.END)
    project_entry.insert(tk.END, normalize_input(gui_text(config.get("PROJECT", ""))))

    location_entry.delete(0, tk.END)
    location_entry.insert(tk.END, normalize_input(gui_text(config.get("LOCATION", ""))))

    organism_entry.delete(0, tk.END)
    organism_entry.insert(tk.END, normalize_input(gui_text(config.get("ORGANISM", ""))))

    trial_name_entry.delete(0, tk.END)
    trial_name_entry.insert(tk.END, gui_text(config.get("TRIALNAME", "")))
    normalize_entry_spaces(trial_name_entry)

    trial_num_entry.delete(0, tk.END)
    trial_num_entry.insert(tk.END, normalize_input(gui_text(config.get("TRIALNUM", "")), folder_name=True))

    output_entry.delete(0, tk.END)
    output_entry.insert(tk.END, normalize_input(gui_text(config.get("OUTPATH", "")), folder_name=True))

    interactive_var.set(config.get("INTERACTIVE", True))
    auto_start_var.set(config.get("AUTOSTART", True))

    motion_file_label.config(text=gui_text(config.get("MOTIONPATH", DEFAULT_MOTION_PATH)))


# Build the GUI

window = tk.Tk()
window.title("Activity Monitoring Experiment")
window.geometry("720x610")
window.minsize(640, 540)
window.configure(bg="#eef2f5")

style = ttk.Style(window)
style.configure("Title.TLabel", background="#17324d", foreground="white", font=("Segoe UI", 18, "bold"))
style.configure("Subtitle.TLabel", background="#17324d", foreground="#c9d8e5", font=("Segoe UI", 10))
style.configure("Section.TLabelframe", background="#ffffff", borderwidth=1)
style.configure("Section.TLabelframe.Label", background="#ffffff", foreground="#17324d", font=("Segoe UI", 10, "bold"))
style.configure("Body.TLabel", background="#ffffff", foreground="#273746", font=("Segoe UI", 9))
style.configure("Path.TLabel", background="#ffffff", foreground="#607385", font=("Segoe UI", 8))
style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"))
style.configure("Unsaved.Status.TLabel", background="#f8d7da", foreground="#8b1e2d", font=("Segoe UI", 9, "bold"))
style.configure("Ready.Status.TLabel", background="#d9f0df", foreground="#176b3a", font=("Segoe UI", 9, "bold"))

window.columnconfigure(0, weight=1)
window.rowconfigure(2, weight=1)

header = tk.Frame(window, bg="#17324d", padx=24, pady=18)
header.grid(row=0, column=0, sticky="ew")
ttk.Label(header, text="Activity Monitoring", style="Title.TLabel").pack(anchor="w")
ttk.Label(header, text="Configure an experiment, then launch it when the project is ready.", style="Subtitle.TLabel").pack(anchor="w", pady=(3, 0))

files_frame = ttk.LabelFrame(window, text="Configuration files", style="Section.TLabelframe", padding=12)
files_frame.grid(row=1, column=0, sticky="ew", padx=18, pady=(14, 8))
files_frame.columnconfigure(1, weight=1)

ttk.Label(files_frame, text="Project", style="Body.TLabel").grid(row=0, column=0, sticky="w", padx=(0, 12), pady=4)
open_button = ttk.Button(files_frame, text="Open project", command=open_config_file)
open_button.grid(row=0, column=2, sticky="e", padx=(12, 0), pady=2)
project_file_label = ttk.Label(files_frame, text=DEFAULT_PROJECT_CONF, style="Path.TLabel")
project_file_label.grid(row=0, column=1, sticky="ew", pady=4)

ttk.Label(files_frame, text="Motion", style="Body.TLabel").grid(row=1, column=0, sticky="w", padx=(0, 12), pady=4)
motion_button = ttk.Button(files_frame, text="Choose motion file", command=open_motion_file)
motion_button.grid(row=1, column=2, sticky="e", padx=(12, 0), pady=2)
motion_file_label = ttk.Label(files_frame, text=DEFAULT_MOTION_PATH, style="Path.TLabel")
motion_file_label.grid(row=1, column=1, sticky="ew", pady=4)

form_frame = ttk.LabelFrame(window, text="Experiment details", style="Section.TLabelframe", padding=14)
form_frame.grid(row=2, column=0, sticky="nsew", padx=18, pady=8)
form_frame.columnconfigure(1, weight=1)
form_frame.columnconfigure(3, weight=1)

ttk.Label(
    form_frame,
    text="Spaces are allowed in descriptive fields. Spaces in output folder, trial name, and trial number become underscores.",
    style="Path.TLabel",
).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 8))

def add_field(row, column, label, variable_name, folder_name=False):
    """Create a labeled form field and register its edit handler."""
    ttk.Label(form_frame, text=label, style="Body.TLabel").grid(row=row, column=column, sticky="w", padx=(0, 8), pady=7)
    entry = ttk.Entry(form_frame)
    entry.grid(row=row, column=column + 1, sticky="ew", padx=(0, 18 if column == 0 else 0), pady=7)
    entry.bind(
        "<KeyRelease>",
        lambda event: handle_entry_change(event, entry, folder_name),
    )
    globals()[variable_name] = entry

add_field(1, 0, "Experimenter name *", "experimenter_entry")
add_field(1, 2, "Initials *", "initials_entry")
add_field(2, 0, "Project name *", "project_entry")
add_field(2, 2, "Location *", "location_entry")
add_field(3, 0, "Organism *", "organism_entry")
add_field(3, 2, "Output folder *", "output_entry", folder_name=True)
add_field(4, 0, "Trial name *", "trial_name_entry", folder_name=True)
add_field(4, 2, "Trial number", "trial_num_entry", folder_name=True)

ttk.Label(form_frame, text="* Required", style="Path.TLabel").grid(
    row=6, column=0, columnspan=4, sticky="w", pady=(10, 0)
)
ttk.Label(
    form_frame,
    text="Allowed characters: letters (A-Z), numbers (0-9), spaces, hyphens (-), and underscores (_).",
    style="Path.TLabel",
).grid(row=7, column=0, columnspan=4, sticky="w", pady=(2, 0))

options_frame = ttk.Frame(form_frame)
options_frame.grid(row=5, column=0, columnspan=4, sticky="ew", pady=(12, 0))
options_frame.columnconfigure(1, weight=1)
interactive_var = tk.BooleanVar(value=True)
interactive_checkbox = ttk.Checkbutton(options_frame, text="Interactive mode", variable=interactive_var, command=mark_config_dirty)
interactive_checkbox.grid(row=0, column=0, sticky="w", padx=(0, 12), pady=3)
ttk.Label(
    options_frame,
    text="Ask for confirmation before starting the experiment.",
    style="Path.TLabel",
).grid(row=0, column=1, sticky="w", pady=3)
auto_start_var = tk.BooleanVar(value=True)
auto_start_checkbox = ttk.Checkbutton(options_frame, text="Auto start", variable=auto_start_var, command=mark_config_dirty)
auto_start_checkbox.grid(row=1, column=0, sticky="w", padx=(0, 12), pady=3)
ttk.Label(
    options_frame,
    text="Allow unattended runs and choose the next trial number; reboot startup also requires cron.",
    style="Path.TLabel",
).grid(row=1, column=1, sticky="w", pady=3)

footer = tk.Frame(window, bg="#eef2f5", padx=18, pady=14)
footer.grid(row=3, column=0, sticky="ew")
footer.columnconfigure(0, weight=1)
status_var = tk.StringVar(value="Ready to configure")
status_label = ttk.Label(footer, textvariable=status_var, style="Ready.Status.TLabel", padding=(10, 8))
status_label.grid(row=0, column=0, sticky="ew", padx=(0, 12))
save_button = ttk.Button(footer, text="Save project", command=save_config_file)
save_button.grid(row=0, column=1, padx=(0, 8))
run_button = ttk.Button(footer, text="Run experiment", command=run_experiment, state=tk.DISABLED, style="Primary.TButton")
run_button.grid(row=0, column=2)

project_conf_path = load_default_config()
project_file_label.config(text=project_conf_path)
update_gui_elements()
mark_config_saved()

# Start event loop
window.mainloop()