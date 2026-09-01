# smooth_light_control.py
# ============================================================
#  Entry point for the diel light control system.
#
#  All classes and functions are implemented in light_core.py.
#
#  Usage:
#    python3 smooth_light_control.py
#    python3 smooth_light_control.py --test
#    python3 smooth_light_control.py --setup
# ============================================================

import signal
import sys
import board
from datetime import datetime

from light_core import (
    LightSystemConfig,
    Light,
    AutoRangingSensor,
    get_args,
    prompt_strips,
    prompt_sensor,
    current_light_val,
    read_sensor,
    shutdown,
)


if __name__ == '__main__':

    args = get_args()
    cfg  = LightSystemConfig()

    # -- available pins (edit to match your wiring) ---------------------------
    AVAILABLE_PINS = [board.D12, board.D18, board.D21, board.D10]

    # -- hardware setup -------------------------------------------------------
    strip_pins = prompt_strips(AVAILABLE_PINS)

    lights = [Light(pin=pin, num_lights=cfg.num_lights) for pin in strip_pins]
    print(f"{len(lights)} strip(s) initialised.")

    sensor, logging_enabled, log_file, writer = prompt_sensor(cfg)
    log_filepath = log_file.name if log_file else None

    # -- signal handler -------------------------------------------------------
    signal.signal(
        signal.SIGTERM,
        lambda sig, frame: shutdown(lights, log_file, log_filepath) or sys.exit(0)
    )

    # -- setup mode -----------------------------------------------------------
    if args.setup:
        print(f"\n{'--' * 20}")
        print(f"  start sunrise:     {cfg.start_sunrise}")
        print(f"  start sunset:      {cfg.start_sunset}")
        print(f"  twilight duration: {cfg.twilight_duration}")
        print(f"  min light value:   {cfg.min_val}")
        print(f"  max light value:   {cfg.max_val}")
        print(f"  strips:            {len(lights)}")
        print(f"  sensor:            {'yes' if sensor else 'no'}")
        print(f"  logging:           {'yes' if logging_enabled else 'no'}")
        if sensor and isinstance(sensor, AutoRangingSensor):
            print(f"  dark offset:       {sensor.dark_offset:.4f} lux")
        print(f"{'--' * 20}")
        if input("Are these values correct? (y/n): ").strip().lower() == 'n':
            sys.exit("Update parameters in LightSystemConfig and rerun.")

    # -- test mode ------------------------------------------------------------
    if args.test:
        try:
            for i, light in enumerate(lights):
                print(f"\nTesting strip {i + 1} of {len(lights)}...")
                light.test(sensor=sensor, writer=writer, log_file=log_file)
        except KeyboardInterrupt:
            pass
        finally:
            shutdown(lights, log_file, log_filepath)
        sys.exit(0)

    # -- main loop ------------------------------------------------------------
    try:
        while True:
            now   = datetime.now()
            now_h = now.hour + now.minute / 60 + now.second / 3600
            val   = current_light_val(now_h, cfg)

            for light in lights:
                light.set_val(val)

            if logging_enabled:
                lux_raw, vis, ir = read_sensor(sensor)
                lux_corr = (
                    sensor.corrected_lux(lux_raw)
                    if isinstance(sensor, AutoRangingSensor)
                    else lux_raw
                )
                settings = (
                    sensor.current_settings_label
                    if isinstance(sensor, AutoRangingSensor)
                    else "manual"
                )
                dark_offset = (
                    sensor.dark_offset
                    if isinstance(sensor, AutoRangingSensor)
                    else 0.0
                )
                writer.writerow([
                    now.isoformat(),
                    val,
                    lux_raw,
                    lux_corr,
                    vis,
                    ir,
                    settings,
                    dark_offset,
                ])
                log_file.flush()

    except KeyboardInterrupt:
        pass

    finally:
        shutdown(lights, log_file, log_filepath)