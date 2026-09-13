import os
import tkinter as tk
from tkinter import ttk

from gui_helpers import (
    AppContext,
    config_path_text,
    handle_entry_change,
    load_default_config,
    mark_config_dirty,
    mark_config_saved,
    open_config_file,
    open_motion_file,
    run_experiment,
    save_config_file,
    update_wrap_lengths,
    update_trial_number_preview,
    update_gui_elements,
)

# ── Resolve the directory this script lives in ───────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

DEFAULT_MOTION_PATH   = os.path.join(SCRIPT_DIR, "motion-configs",  "motion_best.conf")
DEFAULT_PROJECT_CONF  = os.path.join(SCRIPT_DIR, "project-configs", "project.conf")
TEMPLATE_PROJECT_CONF = os.path.join(SCRIPT_DIR, "project-configs", "template_project.conf")
MAIN_SCRIPT           = os.path.join(SCRIPT_DIR, "run_diel-light.py")

# ── Shared application context ───────────────────────────────────────────────
ctx = AppContext()
ctx.project_conf_path = DEFAULT_PROJECT_CONF

# ── Window ───────────────────────────────────────────────────────────────────
window = tk.Tk()
window.title("Activity Monitoring Experiment")
window.geometry("720x610")
window.minsize(480, 540)
window.configure(bg="#eef2f5")
ctx.window = window

# ── Styles ───────────────────────────────────────────────────────────────────
style = ttk.Style(window)
style.configure("Title.TLabel",            background="#17324d", foreground="white",    font=("Segoe UI", 18, "bold"))
style.configure("Subtitle.TLabel",         background="#17324d", foreground="#c9d8e5",  font=("Segoe UI", 10))
style.configure("Section.TLabelframe",     background="#ffffff", borderwidth=1)
style.configure("Section.TLabelframe.Label", background="#ffffff", foreground="#17324d", font=("Segoe UI", 10, "bold"))
style.configure("Body.TLabel",             background="#ffffff", foreground="#273746",  font=("Segoe UI", 9))
style.configure("Path.TLabel",             background="#ffffff", foreground="#607385",  font=("Segoe UI", 8))
style.configure("Description.TLabel",      background="#ffffff", foreground="#38546a",  font=("Segoe UI", 9))
style.configure("Primary.TButton",         font=("Segoe UI", 10, "bold"))
style.configure("Unsaved.Status.TLabel",   background="#f8d7da", foreground="#8b1e2d", font=("Segoe UI", 9, "bold"))
style.configure("Ready.Status.TLabel",     background="#d9f0df", foreground="#176b3a", font=("Segoe UI", 9, "bold"))

window.columnconfigure(0, weight=1)
window.rowconfigure(2, weight=1)

# ── Header ───────────────────────────────────────────────────────────────────
header = tk.Frame(window, bg="#17324d", padx=24, pady=18)
header.grid(row=0, column=0, sticky="ew")
ttk.Label(header, text="Activity Monitoring",                                                          style="Title.TLabel").pack(anchor="w")
ttk.Label(header, text="Configure an experiment, then launch it when the project is ready.",           style="Subtitle.TLabel").pack(anchor="w", pady=(3, 0))

# ── Configuration files section ───────────────────────────────────────────────
files_frame = ttk.LabelFrame(window, text="Configuration files", style="Section.TLabelframe", padding=12)
files_frame.grid(row=1, column=0, sticky="ew", padx=18, pady=(14, 8))
files_frame.columnconfigure(1, weight=1)

ttk.Label(files_frame, text="Project", style="Body.TLabel").grid(row=0, column=0, sticky="w", padx=(0, 12), pady=4)
ttk.Button(
    files_frame, text="Open project",
    command=lambda: open_config_file(ctx, SCRIPT_DIR),
).grid(row=0, column=2, sticky="e", padx=(12, 0), pady=2)
project_file_label = ttk.Label(files_frame, text=DEFAULT_PROJECT_CONF, style="Path.TLabel")
project_file_label.grid(row=0, column=1, sticky="ew", pady=4)
ctx.project_file_label = project_file_label

ttk.Label(files_frame, text="Motion", style="Body.TLabel").grid(row=1, column=0, sticky="w", padx=(0, 12), pady=4)
ttk.Button(
    files_frame, text="Choose motion file",
    command=lambda: open_motion_file(ctx, SCRIPT_DIR, DEFAULT_MOTION_PATH),
).grid(row=1, column=2, sticky="e", padx=(12, 0), pady=2)
motion_file_label = ttk.Label(files_frame, text=DEFAULT_MOTION_PATH, style="Path.TLabel")
motion_file_label.grid(row=1, column=1, sticky="ew", pady=4)
ctx.motion_file_label = motion_file_label

# ── Experiment details section ────────────────────────────────────────────────
scroll_container = ttk.Frame(window)
scroll_container.grid(row=2, column=0, sticky="nsew", padx=18, pady=8)
scroll_container.columnconfigure(0, weight=1)
scroll_container.rowconfigure(0, weight=1)

form_canvas = tk.Canvas(scroll_container, background="#eef2f5", highlightthickness=0)
form_canvas.grid(row=0, column=0, sticky="nsew")
form_scrollbar = ttk.Scrollbar(scroll_container, orient="vertical", command=form_canvas.yview)
form_scrollbar.grid(row=0, column=1, sticky="ns")
form_canvas.configure(yscrollcommand=form_scrollbar.set)

scroll_frame = ttk.Frame(form_canvas)
scroll_frame.columnconfigure(0, weight=1)
form_window = form_canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
scroll_frame.bind(
    "<Configure>",
    lambda event: form_canvas.configure(scrollregion=form_canvas.bbox("all")),
)
form_canvas.bind(
    "<Configure>",
    lambda event: form_canvas.itemconfigure(form_window, width=event.width),
)


def scroll_form(event):
    """Scroll the form when the pointer is anywhere inside its canvas."""
    canvas_x = form_canvas.winfo_pointerx() - form_canvas.winfo_rootx()
    canvas_y = form_canvas.winfo_pointery() - form_canvas.winfo_rooty()
    if 0 <= canvas_x <= form_canvas.winfo_width() and 0 <= canvas_y <= form_canvas.winfo_height():
        form_canvas.yview_scroll(-1 * (event.delta // 120), "units")


window.bind_all("<MouseWheel>", scroll_form)

form_frame = ttk.LabelFrame(scroll_frame, text="Experiment details", style="Section.TLabelframe", padding=14)
form_frame.grid(row=0, column=0, sticky="ew")
form_frame.columnconfigure(1, weight=1)
form_frame.columnconfigure(3, weight=1)

intro_label = ttk.Label(
    form_frame,
    text="Spaces are allowed in descriptive fields. Spaces in output folder, trial name, and trial number become underscores.",
    style="Path.TLabel",
    justify="left",
)
intro_label.grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 8))


def add_field(row, col, label, attr, folder_name=False):
    """Create a labeled form field, wire its edit handler, and store it on ctx."""
    ttk.Label(form_frame, text=label, style="Body.TLabel").grid(
        row=row, column=col, sticky="w", padx=(0, 8), pady=7
    )
    entry = ttk.Entry(form_frame, width=6)
    entry.grid(row=row, column=col + 1, sticky="ew",
               padx=(0, 18 if col == 0 else 0), pady=7)
    entry.bind(
        "<KeyRelease>",
        lambda event, e=entry, fn=folder_name: (
            handle_entry_change(event, e, ctx, fn),
            update_trial_number_preview(ctx, SCRIPT_DIR),
        ),
    )
    setattr(ctx, attr, entry)


add_field(1, 0, "Experimenter name *", "experimenter_entry")
add_field(1, 2, "Initials *",          "initials_entry")
add_field(2, 0, "Project name *",      "project_entry")
add_field(2, 2, "Location *",          "location_entry")
add_field(3, 0, "Organism *",          "organism_entry")
add_field(3, 2, "Output folder *",     "output_entry",    folder_name=True)
add_field(4, 0, "Trial name *",        "trial_name_entry", folder_name=True)
ctx.trial_num_label = ttk.Label(form_frame, text="Trial number", style="Body.TLabel")
ctx.trial_num_label.grid(row=4, column=2, sticky="w", padx=(0, 8), pady=7)
ctx.trial_num_entry = ttk.Entry(form_frame, width=6)
ctx.trial_num_entry.grid(row=4, column=3, sticky="ew", pady=7)
ctx.trial_num_entry.bind(
    "<KeyRelease>",
    lambda event: handle_entry_change(event, ctx.trial_num_entry, ctx, True),
)

ttk.Label(form_frame, text="* Required", style="Path.TLabel").grid(
    row=6, column=0, columnspan=4, sticky="w", pady=(10, 0)
)
allowed_characters_label = ttk.Label(
    form_frame,
    text="Allowed characters: letters (A-Z), numbers (0-9), spaces, hyphens (-), and underscores (_).",
    style="Path.TLabel",
    justify="left",
)
allowed_characters_label.grid(row=7, column=0, columnspan=4, sticky="w", pady=(2, 0))

# ── Checkbox options ──────────────────────────────────────────────────────────
options_frame = ttk.Frame(form_frame)
options_frame.grid(row=5, column=0, columnspan=4, sticky="ew", pady=(12, 0))
options_frame.columnconfigure(1, weight=1)

ctx.interactive_var = tk.BooleanVar(value=True)
ttk.Checkbutton(
    options_frame, text="Interactive mode",
    variable=ctx.interactive_var,
    command=lambda: mark_config_dirty(ctx),
).grid(row=0, column=0, sticky="w", padx=(0, 12), pady=3)
interactive_description = ttk.Label(options_frame, text="Ask for confirmation before starting the experiment.", style="Description.TLabel", justify="left")
interactive_description.grid(row=0, column=1, sticky="ew", pady=3)

ctx.auto_start_var = tk.BooleanVar(value=True)
ttk.Checkbutton(
    options_frame, text="Auto start",
    variable=ctx.auto_start_var,
    command=lambda: mark_config_dirty(ctx),
).grid(row=1, column=0, sticky="w", padx=(0, 12), pady=3)
auto_start_description = ttk.Label(options_frame, text="Allow unattended runs; reboot startup also requires cron.", style="Description.TLabel", justify="left")
auto_start_description.grid(row=1, column=1, sticky="ew", pady=3)

ctx.auto_number_var = tk.BooleanVar(value=True)
ttk.Checkbutton(
    options_frame, text="Automatic trial numbering",
    variable=ctx.auto_number_var,
    command=lambda: (update_trial_number_preview(ctx, SCRIPT_DIR), mark_config_dirty(ctx)),
).grid(row=2, column=0, sticky="w", padx=(0, 12), pady=3)
auto_number_description = ttk.Label(options_frame, text="Use the next available trial number in the output folder.", style="Description.TLabel", justify="left")
auto_number_description.grid(row=2, column=1, sticky="ew", pady=3)


form_frame.bind(
    "<Configure>",
    lambda event: update_wrap_lengths(
        form_frame,
        intro_label,
        allowed_characters_label,
        (interactive_description, auto_start_description, auto_number_description),
    ),
)
options_frame.bind(
    "<Configure>",
    lambda event: update_wrap_lengths(
        form_frame,
        intro_label,
        allowed_characters_label,
        (interactive_description, auto_start_description, auto_number_description),
    ),
)

# ── Footer ────────────────────────────────────────────────────────────────────
footer = tk.Frame(window, bg="#eef2f5", padx=18, pady=14)
footer.grid(row=3, column=0, sticky="ew")
footer.columnconfigure(0, weight=1)

ctx.status_var = tk.StringVar(value="Ready to configure")
ctx.status_label = ttk.Label(footer, textvariable=ctx.status_var, style="Ready.Status.TLabel", padding=(10, 8))
ctx.status_label.grid(row=0, column=0, sticky="ew", padx=(0, 12))

ctx.save_button = ttk.Button(
    footer, text="Save project",
    command=lambda: save_config_file(ctx, SCRIPT_DIR, DEFAULT_MOTION_PATH),
)
ctx.save_button.grid(row=0, column=1, padx=(0, 8))

ctx.run_button = ttk.Button(
    footer, text="Run experiment",
    command=lambda: run_experiment(ctx, MAIN_SCRIPT, DEFAULT_MOTION_PATH),
    state=tk.DISABLED,
    style="Primary.TButton",
)
ctx.run_button.grid(row=0, column=2)

# ── Bootstrap ─────────────────────────────────────────────────────────────────
ctx.project_conf_path = load_default_config(ctx, DEFAULT_PROJECT_CONF, TEMPLATE_PROJECT_CONF)
project_file_label.config(text=config_path_text(ctx.project_conf_path, "project"))
update_gui_elements(ctx, DEFAULT_MOTION_PATH, SCRIPT_DIR)
mark_config_saved(ctx)

# ── Event loop ────────────────────────────────────────────────────────────────
window.mainloop()