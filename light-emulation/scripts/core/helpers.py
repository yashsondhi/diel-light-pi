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
from datetime import datetime
from typing import Optional, Tuple

try:
    import board
except ImportError:
    class _BoardFallback:
        D12 = 12
        D18 = 18
        D21 = 21
        D10 = 10

    board = _BoardFallback()

from core.sensor import AutoRangingSensor, TSL2591_AVAILABLE
from core.config import LightSystemConfig


def get_bcm_pin_number(pin) -> int:
    """Return the BCM number for a CircuitPython board pin."""
    pin_name = getattr(pin, "id", str(pin))
    match = re.search(r'(\d+)$', str(pin_name))
    if match:
        return int(match.group(1))
    raise ValueError(f"Could not determine BCM pin number for {pin_name}")


def save_experiment_config(
    *,
    cfg: Optional[LightSystemConfig] = None,
    light_config_file: Optional[str] = None,
    external_pwm_enabled: bool,
    external_pwm_gpio: int,
    external_pwm_chip: int = 15,
    external_pwm_frequency: float = 1000.0,
    external_pwm_min_brightness: float = 0.0,
    external_pwm_max_brightness: float = 1.0,
    neopixel_pins: Optional[list] = None,
    sensor_enabled: bool = False,
    logging_enabled: bool = False,
    sensor_measurement_interval: float = 0.0,
    sensor_dark_offset: Optional[float] = None,
    log_file_path: Optional[str] = None,
) -> str:
    """Save all resolved experiment settings in a dated text file."""
    os.makedirs(EXPERIMENT_CONFIG_DIRECTORY, exist_ok=True)
    neopixel_names = (
        ','.join(str(pin) for pin in sorted(neopixel_pins or []))
        or 'none'
    )
    started_at = datetime.now()
    lines = [
        f'# Experiment configuration',
        f'experiment_started_at = {started_at.isoformat(timespec="seconds")}',
        'experiment_stopped_at = still_running',
        'experiment_status = running',
        f'light_config_file = {light_config_file or "default"}',
        f'start_sunrise = {cfg.start_sunrise:g}' if cfg else 'start_sunrise = 7.0',
        f'start_sunset = {cfg.start_sunset:g}' if cfg else 'start_sunset = 19.0',
        f'twilight_duration = {cfg.twilight_duration:g}' if cfg else 'twilight_duration = 1.5',
        f'neopixel_min_brightness = {cfg.min_val:g}' if cfg else 'neopixel_min_brightness = 0.0',
        f'neopixel_max_brightness = {cfg.max_val:g}' if cfg else 'neopixel_max_brightness = 0.2',
        f'neopixel_count = {cfg.num_lights}' if cfg else 'neopixel_count = 50',
        f'neopixel_dark_calibration_samples = {cfg.dark_calibration_samples}' if cfg else 'neopixel_dark_calibration_samples = 30',
        f'neopixel_enabled = {str(bool(neopixel_pins)).lower()}',
        f'neopixel_pins = {neopixel_names}',
        f'external_pwm_enabled = {str(external_pwm_enabled).lower()}',
        f'external_pwm_gpio = {external_pwm_gpio}',
        f'external_pwm_chip = {external_pwm_chip}',
        f'external_pwm_frequency = {external_pwm_frequency:g}',
        f'external_pwm_min_brightness = {external_pwm_min_brightness:g}',
        f'external_pwm_max_brightness = {external_pwm_max_brightness:g}',
        f'sensor_enabled = {str(sensor_enabled).lower()}',
        f'logging_enabled = {str(logging_enabled).lower()}',
        f'sensor_measurement_interval_seconds = {sensor_measurement_interval:g}',
        f'sensor_dark_offset_lux = '
        f'{sensor_dark_offset if sensor_dark_offset is not None else "not_calibrated"}',
        f'log_file = {log_file_path or "none"}',
        f'data_location = {log_file_path or "none"}',
    ]
    content = '\n'.join(lines) + '\n'

    date_tag = started_at.strftime('%Y-%m-%d_%H-%M-%S')
    dated_path = os.path.join(
        EXPERIMENT_CONFIG_DIRECTORY,
        f'experiment_{date_tag}.txt',
    )
    counter = 1
    while os.path.exists(dated_path):
        dated_path = os.path.join(
            EXPERIMENT_CONFIG_DIRECTORY,
            f'experiment_{date_tag}_{counter}.txt',
        )
        counter += 1

    with open(dated_path, 'w', encoding='utf-8') as config_file:
        config_file.write(content)
    return dated_path


def finalize_experiment_config(
    experiment_config_path: str,
    status: str = 'stopped',
    log_file_path: Optional[str] = None,
) -> None:
    """Record stop time and final data location for a dated experiment."""
    if not experiment_config_path or not os.path.isfile(experiment_config_path):
        return

    stopped_at = datetime.now().isoformat(timespec='seconds')
    replacements = {
        'experiment_stopped_at': stopped_at,
        'experiment_status': status,
        'log_file': log_file_path or 'none',
        'data_location': log_file_path or 'none',
    }

    if not os.path.isfile(experiment_config_path):
        return
    with open(experiment_config_path, 'r', encoding='utf-8') as config_file:
        lines = config_file.readlines()

    updated = []
    found = set()
    for line in lines:
        key = line.split('=', 1)[0].strip()
        if key in replacements:
            updated.append(f'{key} = {replacements[key]}\n')
            found.add(key)
        else:
            updated.append(line)

    for key, value in replacements.items():
        if key not in found:
            updated.append(f'{key} = {value}\n')

    with open(experiment_config_path, 'w', encoding='utf-8') as config_file:
        config_file.writelines(updated)

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

CSV_HEADER_NO_SET_VAL = [
    field for field in CSV_HEADER if field != 'set_val'
]

VISUALIZE_SCRIPT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lux_data_visualizer.py"
)

EXPERIMENT_CONFIG_DIRECTORY = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "configs",
)


def get_default_log_dir() -> str:
    """Return the repository's light-emulation raw-data log directory."""
    return os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "data",
        "raw",
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
    print("\nAvailable smooth-light pins:")
    for index, pin in enumerate(available_pins, start=1):
        print(f"  {index}. {str(pin)} (BCM {get_bcm_pin_number(pin)})")

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

    if n == 0:
        return []

    selected_pins = []
    while len(selected_pins) < n:
        strip_number = len(selected_pins) + 1
        answer = input(
            f"Pin for smooth-light strip {strip_number}: "
        ).strip()
        try:
            selection = int(answer)
        except ValueError:
            print("  Please enter a menu number or BCM GPIO number.")
            continue

        if 1 <= selection <= len(available_pins):
            pin = available_pins[selection - 1]
        else:
            matching_pins = [
                pin for pin in available_pins
                if get_bcm_pin_number(pin) == selection
            ]
            pin = matching_pins[0] if matching_pins else None

        if pin is None:
            print("  Please choose one of the available pins.")
            continue
        if pin in selected_pins:
            print("  That pin is already assigned to a smooth-light strip.")
            continue

        selected_pins.append(pin)
        print(
            f"  Strip {strip_number} assigned to "
            f"{str(pin)} (BCM {get_bcm_pin_number(pin)})."
        )

    return selected_pins


def prompt_uv(cfg: LightSystemConfig, neopixel_pins: list) -> tuple:
    """
    Ask whether to enable external UV lighting and choose its BCM GPIO pin.

    Returns:
        (enabled, gpio) where enabled is a bool and gpio is an integer.
    """
    default_choice = 'y' if cfg.external_pwm_enabled else 'n'
    answer = input(
        f"Use external UV lighting? (y/n, default {default_choice}): "
    ).strip().lower()
    if not answer:
        answer = default_choice
    if answer != 'y':
        return False, cfg.external_pwm_gpio

    conflicting_pins = set(neopixel_pins)
    while True:
        answer = input(
            f"UV PWM GPIO (BCM pin, default {cfg.external_pwm_gpio}): "
        ).strip()
        if not answer:
            gpio = cfg.external_pwm_gpio
        else:
            try:
                gpio = int(answer)
            except ValueError:
                print("  Please enter a valid BCM GPIO number.")
                continue
        if gpio < 0 or gpio > 54:
            print("  Please enter a BCM GPIO number between 0 and 54.")
            continue
        if gpio in conflicting_pins:
            print(
                f"  GPIO {gpio} is already assigned to a NeoPixel strip."
            )
            continue
        return True, gpio


def prompt_sample_interval() -> float:
    """Ask how often sensor measurements should be taken and logged."""
    recommendation = (
        "For more detail, use 1-2 seconds; for a week-long trial, 8 seconds is a reasonable compromise. The lights will still update every 0.5 seconds. As reference, a 3 day trial with a 0.5 second measurement spacing resulted in a 3 GB csv file."
    )
    print(f"\n{recommendation}")
    while True:
        answer = input(
            "Sensor measurement interval in seconds [2.0]: "
        ).strip()
        if not answer:
            return 2.0
        try:
            interval = float(answer)
            if interval > 0:
                return interval
        except ValueError:
            pass
        print("  Please enter a number greater than zero.")


def prompt_sensor(cfg: LightSystemConfig, num_lights: int = 0):
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
        num_lights: Number of strips currently configured. If zero,
            omit the set_val column from the emitted CSV schema.

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
                "min-max normalisation in lux_data_visualizer.py instead."
            )
            sensor.calibrate_dark(n_samples=cfg.dark_calibration_samples)
    else:
        print(
            "Skipping dark calibration -- lux_corrected will equal lux_raw.\n"
            "You can normalise post-hoc using lux_raw and dark_offset_lux "
            "in lux_data_visualizer.py."
        )

    # -- log file setup -------------------------------------------------------
    log_dir = get_default_log_dir()
    os.makedirs(log_dir, exist_ok=True)

    default_name = "sensor_log"
    user_input   = input(f"Log file name (enter for '{default_name}'): ").strip()
    base_name    = (
        re.sub(r'[<>:"/\\|?*]', '_', user_input) if user_input else default_name
    )
    log_filename = get_unique_filepath(log_dir, base_name)

    fieldnames = CSV_HEADER if num_lights else CSV_HEADER_NO_SET_VAL
    log_file = open(log_filename, 'w', newline='')
    writer = csv.DictWriter(log_file, fieldnames=fieldnames)
    writer.writeheader()
    print(f"Logging to: {log_filename}")

    return sensor, True, log_file, writer


def launch_visualizer(log_filepath: str) -> None:
    """
    Optionally launch lux_data_visualizer.py after the run, passing the log file
    as a command-line argument. Does nothing if lux_data_visualizer.py is not found.

    Args:
        log_filepath: absolute path to the CSV log file.
    """
    if not os.path.exists(VISUALIZE_SCRIPT):
        print(f"lux_data_visualizer.py not found at {VISUALIZE_SCRIPT} -- skipping.")
        return

    ans = input(
        "Open lux_data_visualizer.py to view the data? (y/n, default n): "
    ).strip().lower()
    if ans != 'y':
        return

    print(f"Launching visualizer for {log_filepath}...")
    subprocess.Popen([sys.executable, VISUALIZE_SCRIPT, log_filepath])


def shutdown(
    lights: list,
    log_file=None,
    log_filepath: Optional[str] = None,
    external_pwm=None,
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
        external_pwm: optional ExternalPwmLight to turn off.
    """
    print("\nShutting down...")
    for light in lights:
        light.off()
    if external_pwm is not None:
        external_pwm.off()
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
        --config: path to the text file containing light-system settings.

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
    default_config = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        'light_config.txt',
    )
    parser.add_argument(
        '--config', default=default_config,
        help=f'Path to light configuration file (default: {default_config})',
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