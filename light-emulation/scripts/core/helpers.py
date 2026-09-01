# core/helpers.py
# ============================================================
#  Standalone helper functions for the diel light system.
#
#  Functions:
#    read_sensor         -- unified sensor read dispatcher
#    get_unique_filepath -- safe file path generator
#    prompt_strips       -- interactive strip setup
#    prompt_sensor       -- interactive sensor + calibration setup
#    launch_visualizer   -- post-run visualizer launcher
#    shutdown            -- central cleanup
#    get_args            -- command-line argument parser
#    current_light_val   -- diel brightness calculator
# ============================================================

import os
import re
import csv
import sys
import subprocess
import argparse
import board
from typing import Optional, Tuple

from core.sensor import AutoRangingSensor, TSL2591_AVAILABLE
from core.config import LightSystemConfig

CSV_HEADER = [
    'timestamp',
    'set_val',
    'lux_raw',
    'lux_corrected',
    'visible',
    'ir',
    'sensor_settings',
    'dark_offset_lux',
]

VISUALIZE_SCRIPT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lux_data_visualizer.py"
)


def read_sensor(sensor) -> Tuple[Optional[float], Optional[float], Optional[float]]:
    """
    Unified sensor read dispatcher.

    Accepts either an AutoRangingSensor (calls .read()) or a raw TSL2591
    object (reads attributes directly) for backwards compatibility.

    Args:
        sensor: AutoRangingSensor or raw TSL2591 object.

    Returns:
        (lux_raw, visible, ir) or (None, None, None) on error.
    """
    try:
        if isinstance(sensor, AutoRangingSensor):
            return sensor.read()
        return sensor.lux, sensor.visible, sensor.infrared
    except Exception as e:
        print(f"Sensor read error: {e}")
        return None, None, None


def get_unique_filepath(directory: str, base_name: str) -> str:
    """
    Return a file path that does not already exist.
    Appends _1, _2 etc. until a free name is found.

    Args:
        directory: target directory.
        base_name: desired file name without extension.

    Returns:
        Full file path string ending in .csv.
    """
    path    = os.path.join(directory, f"{base_name}.csv")
    counter = 1
    while os.path.exists(path):
        path = os.path.join(directory, f"{base_name}_{counter}.csv")
        counter += 1
    return path


def prompt_strips(available_pins: list) -> list:
    """
    Interactively ask the user how many LED strips to use and which
    pins to assign them to.

    Args:
        available_pins: ordered list of board pin objects.

    Returns:
        Subset of available_pins selected by the user.
    """
    print("\nAvailable pins:", [str(p) for p in available_pins])
    while True:
        try:
            n = int(
                input(f"How many LED strips? (0-{len(available_pins)}): ").strip()
            )
            if 0 <= n <= len(available_pins):
                break
            print(f"  Please enter a number between 0 and {len(available_pins)}.")
        except ValueError:
            print("  Please enter a valid integer.")
    return available_pins[:n]


def prompt_sensor(cfg: LightSystemConfig):
    """
    Interactively initialise an AutoRangingSensor, optionally run dark
    calibration, and optionally enable CSV logging.

    Dark calibration flow:
      1. Ask if the user wants to run dark calibration.
      2. If yes, ask whether total darkness is available.
         - Yes: prompt to cover the sensor, collect samples, uncover.
         - No:  collect samples from current conditions with a warning.
      3. The dark_offset is stored on the sensor and written to every
         CSV row for full traceability.

    Args:
        cfg: LightSystemConfig providing dark_calibration_samples.

    Returns:
        (sensor, logging_enabled, log_file, writer)
        sensor is None if initialisation fails or logging is declined.
    """
    if not TSL2591_AVAILABLE:
        print("adafruit_tsl2591 not installed -- sensor unavailable.")
        return None, False, None, None

    ans = input("Enable sensor logging? (y/n, default n): ").strip().lower()
    if ans != 'y':
        return None, False, None, None

    # -- init sensor ----------------------------------------------------------
    try:
        i2c    = board.I2C()
        sensor = AutoRangingSensor(i2c, name="sensor")
        print("Auto-ranging sensor initialised.")
    except Exception as e:
        print(f"Sensor init failed: {e}")
        return None, False, None, None

    # -- dark calibration -----------------------------------------------------
    cal_ans = input(
        "Run dark calibration now? Recommended for accurate lux values. "
        "(y/n, default n): "
    ).strip().lower()

    if cal_ans == 'y':
        dark_ans = input(
            "Do you have access to total darkness (e.g. cover the sensor)? "
            "(y/n): "
        ).strip().lower()

        if dark_ans == 'y':
            input(
                "Cover the sensor completely, then press Enter to begin "
                "calibration..."
            )
            print("Collecting dark calibration samples (total darkness)...")
            sensor.calibrate_dark(n_samples=cfg.dark_calibration_samples)
            input("Uncover the sensor and press Enter to continue...")
        else:
            print(
                "No total darkness available -- collecting baseline from "
                "current conditions.\n"
                "WARNING: This is an approximate baseline. For best results "
                "calibrate at the darkest point of your diel cycle or use "
                "min-max normalisation in visualize.py instead."
            )
            sensor.calibrate_dark(n_samples=cfg.dark_calibration_samples)
    else:
        print(
            "Skipping dark calibration -- lux_corrected will equal lux_raw.\n"
            "You can normalise post-hoc using lux_raw and dark_offset_lux "
            "in visualize.py."
        )

    # -- log file setup -------------------------------------------------------
    log_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"
    )
    os.makedirs(log_dir, exist_ok=True)

    default_name = "sensor_log"
    user_input   = input(f"Log file name (enter for '{default_name}'): ").strip()
    base_name    = (
        re.sub(r'[<>:"/\\|?*]', '_', user_input) if user_input else default_name
    )
    log_filename = get_unique_filepath(log_dir, base_name)

    log_file = open(log_filename, 'w', newline='')
    writer = csv.DictWriter(log_file, fieldnames=CSV_HEADER)
    writer.writeheader()
    print(f"Logging to: {log_filename}")

    return sensor, True, log_file, writer


def launch_visualizer(log_filepath: str) -> None:
    """
    Optionally launch visualize.py after the run, passing the log file
    as a command-line argument. Does nothing if visualize.py is not found.

    Args:
        log_filepath: absolute path to the CSV log file.
    """
    if not os.path.exists(VISUALIZE_SCRIPT):
        print(f"visualize.py not found at {VISUALIZE_SCRIPT} -- skipping.")
        return

    ans = input(
        "Open visualize.py to view the data? (y/n, default n): "
    ).strip().lower()
    if ans != 'y':
        return

    print(f"Launching visualizer for {log_filepath}...")
    subprocess.Popen([sys.executable, VISUALIZE_SCRIPT, log_filepath])


def shutdown(
    lights: list,
    log_file=None,
    log_filepath: Optional[str] = None,
) -> None:
    """
    Central cleanup routine. Always called on exit regardless of how
    the script terminates.

    Turns off all LED strips, closes the log file, and optionally
    launches the visualizer.

    Args:
        lights:       list of Light instances to turn off.
        log_file:     open log file to close, or None.
        log_filepath: path to the log file for the visualizer, or None.
    """
    print("\nShutting down...")
    for light in lights:
        light.off()
    print(f"{len(lights)} strip(s) turned off.")
    if log_file and not log_file.closed:
        log_file.close()
        print("Log file closed.")
        if log_filepath:
            launch_visualizer(log_filepath)
    print("Goodbye!")


def get_args() -> argparse.Namespace:
    """
    Parse and return command-line arguments.

    Flags:
        --test:  run sine wave brightness test on all strips then exit.
        --setup: print current LightSystemConfig values and confirm before
                 starting the main loop.

    Returns:
        argparse.Namespace with attributes test and setup.
    """
    parser = argparse.ArgumentParser(
        usage='%(prog)s [options]',
        description="Run diel light control"
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        '--test',  default=False, action="store_true",
        help='Run sine wave brightness test'
    )
    mode.add_argument(
        '--setup', default=False, action="store_true",
        help='Print and confirm light cycle parameters'
    )
    return parser.parse_args()


def current_light_val(now_h: float, cfg: LightSystemConfig) -> float:
    """
    Calculate the target proportional brightness for a given time of day.

    Implements a five-phase diel cycle:
      1. Night before sunrise  -> min_val
      2. Sunrise twilight      -> linear ramp from min_val to max_val
      3. Full daytime          -> max_val
      4. Sunset twilight       -> linear ramp from max_val to min_val
      5. Night after sunset    -> min_val

    Args:
        now_h: current time as decimal hours (e.g. 13.5 = 13:30).
        cfg:   LightSystemConfig providing all cycle parameters.

    Returns:
        Proportional brightness as a float in [min_val, max_val].
    """
    if now_h < cfg.start_sunrise:
        return cfg.min_val
    elif now_h < cfg.start_sunrise + cfg.twilight_duration:
        prop = (now_h - cfg.start_sunrise) / cfg.twilight_duration
        return prop * cfg.max_val
    elif now_h < cfg.start_sunset:
        return cfg.max_val
    elif now_h < cfg.start_sunset + cfg.twilight_duration:
        prop = (now_h - cfg.start_sunset) / cfg.twilight_duration
        return (1 - prop) * cfg.max_val
    else:
        return cfg.min_val