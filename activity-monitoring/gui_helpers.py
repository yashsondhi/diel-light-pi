# gui_helpers.py
import os
import re
import subprocess
import sys
import tkinter as tk
import yaml


# ── Quoted-string YAML dumper ────────────────────────────────────────────────

class QuotedStringDumper(yaml.SafeDumper):
    pass


def represent_quoted_string(dumper, value):
    """Represent a Python string as a double-quoted YAML scalar."""
    return dumper.represent_scalar("tag:yaml.org,2002:str", value, style='"')


QuotedStringDumper.add_representer(str, represent_quoted_string)


# ── App context (shared mutable state + widget references) ───────────────────

class AppContext:
    """
    Holds all shared mutable state and widget references so that helper
    functions do not rely on module-level globals in the main file.
    """
    def __init__(self):
        self.config: dict = {}
        self.config_dirty: bool = False
        self.project_conf_path: str = ""
        self.project_config_selected: bool = False
        self.motion_config_selected: bool = False

        # Widget references — assigned after the GUI is built
        self.run_button        = None
        self.save_button       = None
        self.status_var        = None
        self.status_label      = None
        self.motion_file_label = None
        self.project_file_label = None
        self.window            = None

        # Form entry widgets
        self.experimenter_entry = None
        self.initials_entry     = None
        self.project_entry      = None
        self.location_entry     = None
        self.organism_entry     = None
        self.output_entry       = None
        self.trial_name_entry   = None
        self.trial_num_entry    = None
        self.trial_num_label    = None

        # Checkbox variables
        self.interactive_var  = None
        self.auto_start_var   = None
        self.auto_number_var  = None


# ── String helpers ───────────────────────────────────────────────────────────

def gui_text(value):
    """Convert a configuration value into text suitable for an Entry widget."""
    if value is None:
        return ""
    return str(value)


def config_path_text(path, config_type):
    """Return a useful label for a selected or missing configuration path."""
    return gui_text(path) or f"No {config_type} config file selected"


def normalize_input(value, folder_name=False):
    """Keep allowed characters and optionally convert whitespace to underscores."""
    value = str(value)
    if folder_name:
        value = re.sub(r"\s+", "_", value)
        return re.sub(r"[^A-Za-z0-9_-]", "", value)
    return re.sub(r"[^A-Za-z0-9_\- ]", "", value)


# ── Entry / dirty-state helpers ──────────────────────────────────────────────

def handle_entry_change(event, entry, ctx: AppContext, folder_name=False):
    """Normalize an edited field and mark the configuration as unsaved."""
    current_value = entry.get()
    updated_value = normalize_input(current_value, folder_name)
    if current_value != updated_value:
        cursor_position = entry.index(tk.INSERT)
        entry.delete(0, tk.END)
        entry.insert(0, updated_value)
        entry.icursor(min(cursor_position, len(updated_value)))
    mark_config_dirty(ctx)


def normalize_entry_spaces(entry):
    """Normalize the value of an existing Entry widget."""
    current_value = entry.get()
    updated_value = normalize_input(current_value, folder_name=True)
    if current_value != updated_value:
        entry.delete(0, tk.END)
        entry.insert(0, updated_value)


def update_wrap_lengths(form_frame, intro_label, allowed_characters_label, description_labels):
    """Match wrapped label widths to their current layout widths."""
    full_width = max(form_frame.winfo_width() - 28, 1)
    intro_label.configure(wraplength=full_width)
    allowed_characters_label.configure(wraplength=full_width)
    for label in description_labels:
        label.configure(wraplength=max(label.winfo_width(), 1))


def scroll_form(event, form_canvas):
    """Scroll the form when the pointer is anywhere inside its canvas."""
    canvas_x = form_canvas.winfo_pointerx() - form_canvas.winfo_rootx()
    canvas_y = form_canvas.winfo_pointery() - form_canvas.winfo_rooty()
    if 0 <= canvas_x <= form_canvas.winfo_width() and 0 <= canvas_y <= form_canvas.winfo_height():
        form_canvas.yview_scroll(-1 * (event.delta // 120), "units")


def add_field(form_frame, ctx, script_dir, row, col, label, attr, folder_name=False):
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
            update_trial_number_preview(ctx, script_dir),
        ),
    )
    setattr(ctx, attr, entry)


def get_next_trial_number(output_path):
    """Return the next number using the runner's existing trial-directory rule."""
    if not os.path.isdir(output_path):
        return 1
    trial_pattern = re.compile(r"_trial\d+$")
    trial_count = sum(
        bool(os.path.isdir(os.path.join(output_path, name)) and trial_pattern.search(name))
        for name in os.listdir(output_path)
    )
    return trial_count + 1


def update_trial_number_preview(ctx: AppContext, script_dir: str):
    """Show the next automatic number and disable manual input when selected."""
    output_path = normalize_input(ctx.output_entry.get(), folder_name=True)
    output_path = os.path.expanduser(output_path)
    if not os.path.isabs(output_path):
        output_path = os.path.join(script_dir, output_path)

    if ctx.auto_number_var.get():
        trial_number = str(get_next_trial_number(output_path))
        ctx.trial_num_entry.config(state=tk.NORMAL)
        ctx.trial_num_entry.delete(0, tk.END)
        ctx.trial_num_entry.insert(0, trial_number)
        ctx.trial_num_entry.config(state=tk.DISABLED)
    else:
        ctx.trial_num_entry.config(state=tk.NORMAL)


def manual_trial_conflicts(ctx: AppContext, script_dir: str):
    """Return whether the selected manual trial number already has a directory."""
    if ctx.auto_number_var.get():
        return False

    output_path = normalize_input(ctx.output_entry.get(), folder_name=True)
    output_path = os.path.expanduser(output_path)
    if not os.path.isabs(output_path):
        output_path = os.path.join(script_dir, output_path)
    trial_name = normalize_input(ctx.trial_name_entry.get(), folder_name=True)
    trial_number = normalize_input(ctx.trial_num_entry.get(), folder_name=True)
    if not trial_name or not trial_number:
        return False
    trial_dir = os.path.join(output_path, trial_name + "_trial" + trial_number.zfill(2))
    return os.path.isdir(trial_dir)


def mark_config_dirty(ctx: AppContext):
    """Disable running until the current form values have been saved."""
    ctx.config_dirty = True
    if ctx.run_button is not None:
        ctx.run_button.config(state=tk.DISABLED)
    if ctx.status_var is not None:
        ctx.status_var.set("Unsaved changes - save the project before running")
    if ctx.status_label is not None:
        ctx.status_label.configure(style="Unsaved.Status.TLabel")


def configs_selected(ctx: AppContext):
    """Return whether both configuration files were explicitly selected."""
    return ctx.project_config_selected and ctx.motion_config_selected


def mark_config_saved(ctx: AppContext):
    """Mark the form as saved and allow running only with both configs selected."""
    ctx.config_dirty = False
    if ctx.run_button is not None:
        ctx.run_button.config(state=tk.NORMAL if configs_selected(ctx) else tk.DISABLED)
    if ctx.status_var is not None:
        ctx.status_var.set("Ready to run" if configs_selected(ctx) else "Select project and motion config files")
    if ctx.status_label is not None:
        ctx.status_label.configure(style="Ready.Status.TLabel")


def finish_save(ctx: AppContext):
    """Complete deferred save-state updates after the file dialog closes."""
    mark_config_saved(ctx)
    ctx.save_button.focus_set()


# ── File I/O helpers ─────────────────────────────────────────────────────────

def load_default_config(ctx: AppContext, default_path: str, template_path: str) -> str:
    """Load project.conf or fall back to the starter project template."""
    path = default_path
    if not os.path.exists(path):
        path = template_path

    if os.path.exists(path):
        with open(path, "r") as fh:
            loaded = yaml.safe_load(fh) or {}
        ctx.config.update(loaded)
        return path

    return default_path


def open_config_file(ctx: AppContext, script_dir: str):
    """Open a project configuration and populate the form with its values."""
    from tkinter import filedialog
    file_path = filedialog.askopenfilename(
        filetypes=[("Conf Files", "*.conf")],
        initialdir=os.path.join(script_dir, "project-configs"),
    )
    if file_path:
        with open(file_path, "r") as fh:
            ctx.config.update(yaml.safe_load(fh) or {})
        ctx.project_conf_path = file_path
        ctx.project_config_selected = True
        if ctx.project_file_label is not None:
            ctx.project_file_label.config(text=config_path_text(file_path, "project"))
        update_gui_elements(ctx)
        mark_config_saved(ctx)


def open_motion_file(ctx: AppContext, script_dir: str, default_motion_path: str):
    """Select the motion configuration used by the next experiment run."""
    from tkinter import filedialog
    file_path = filedialog.askopenfilename(
        filetypes=[("Conf Files", "*.conf")],
        initialdir=os.path.join(script_dir, "motion-configs"),
    )
    if file_path:
        ctx.config["MOTIONPATH"] = file_path
        ctx.motion_config_selected = True
        ctx.motion_file_label.config(text=config_path_text(file_path, "motion"))
        mark_config_dirty(ctx)


def save_config_file(ctx: AppContext, script_dir: str, default_motion_path: str):
    """Collect, normalize, and save the current experiment configuration."""
    from tkinter import filedialog
    file_path = filedialog.asksaveasfilename(
        filetypes=[("Conf Files", "*.conf")],
        initialdir=os.path.join(script_dir, "project-configs"),
    )
    if file_path:
        if manual_trial_conflicts(ctx, script_dir):
            ctx.status_var.set("That trial number already exists - choose another number")
            ctx.status_label.configure(style="Unsaved.Status.TLabel")
            return
        ctx.config.update({
            "USER":        normalize_input(ctx.experimenter_entry.get()),
            "INITIALS":    normalize_input(ctx.initials_entry.get()),
            "PROJECT":     normalize_input(ctx.project_entry.get()),
            "LOCATION":    normalize_input(ctx.location_entry.get()),
            "ORGANISM":    normalize_input(ctx.organism_entry.get()),
            "OUTPATH":     normalize_input(ctx.output_entry.get(),     folder_name=True),
            "TRIALNAME":   normalize_input(ctx.trial_name_entry.get(), folder_name=True),
            "TRIALNUM":    normalize_input(ctx.trial_num_entry.get(),  folder_name=True),
            "INTERACTIVE": ctx.interactive_var.get(),
            "AUTOSTART":   ctx.auto_start_var.get(),
            "AUTONUMBER":  ctx.auto_number_var.get(),
            "MOTIONPATH":  ctx.config.get("MOTIONPATH", default_motion_path),
        })
        with open(file_path, "w") as fh:
            yaml.dump(ctx.config, fh, Dumper=QuotedStringDumper, sort_keys=False)
        ctx.project_conf_path = file_path
        ctx.project_config_selected = True
        ctx.window.after_idle(lambda: finish_save(ctx))


# ── Experiment runner ────────────────────────────────────────────────────────

def run_experiment(ctx: AppContext, main_script: str, default_motion_path: str):
    """Launch the experiment runner in a platform-appropriate terminal."""
    if ctx.config_dirty or not configs_selected(ctx):
        return
    motion_path = ctx.config.get("MOTIONPATH", default_motion_path)
    command = (
        f"python3 {main_script} --run "
        f"--projectconf {ctx.project_conf_path} "
        f"--motionconf {motion_path}"
    )
    if sys.platform.startswith("win"):
        subprocess.Popen(["cmd.exe", "/c", "start", "cmd.exe", "/k", command])
    elif sys.platform.startswith("darwin"):
        subprocess.Popen(["/usr/bin/open", "-n", "-F", "-a",
                          "/Applications/Utilities/Terminal.app", command])
    elif sys.platform.startswith("linux"):
        subprocess.Popen([
            "x-terminal-emulator",
            "-e",
            "python3",
            main_script,
            "--run",
            "--projectconf",
            ctx.project_conf_path,
            "--motionconf",
            motion_path,
        ])


# ── GUI refresh ──────────────────────────────────────────────────────────────

def update_gui_elements(ctx: AppContext, default_motion_path: str = "", script_dir: str = ""):
    """Refresh all form controls from the current configuration dictionary."""
    def fill(entry, key, fn=normalize_input, **kw):
        entry.delete(0, tk.END)
        entry.insert(tk.END, fn(gui_text(ctx.config.get(key, "")), **kw))

    fill(ctx.experimenter_entry, "USER")
    fill(ctx.initials_entry,     "INITIALS")
    fill(ctx.project_entry,      "PROJECT")
    fill(ctx.location_entry,     "LOCATION")
    fill(ctx.organism_entry,     "ORGANISM")
    fill(ctx.trial_num_entry,    "TRIALNUM",   folder_name=True)
    fill(ctx.output_entry,       "OUTPATH",    folder_name=True)

    # Trial name gets a two-step normalization
    ctx.trial_name_entry.delete(0, tk.END)
    ctx.trial_name_entry.insert(tk.END, gui_text(ctx.config.get("TRIALNAME", "")))
    normalize_entry_spaces(ctx.trial_name_entry)

    ctx.interactive_var.set(ctx.config.get("INTERACTIVE", True))
    ctx.auto_start_var.set(ctx.config.get("AUTOSTART", True))
    ctx.auto_number_var.set(ctx.config.get("AUTONUMBER", ctx.config.get("AUTOSTART", True)))
    update_trial_number_preview(ctx, script_dir or os.path.dirname(os.path.abspath(__file__)))
    ctx.motion_file_label.config(
        text=config_path_text(ctx.config.get("MOTIONPATH", default_motion_path), "motion")
    )