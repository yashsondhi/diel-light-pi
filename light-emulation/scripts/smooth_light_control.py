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
import time
from datetime import datetime

from light_core import (
    LightSystemConfig,
    Light,
    ExternalPwmLight,
    AutoRangingSensor,
    get_args,
    get_bcm_pin_number,
    save_experiment_config,
    finalize_experiment_config,
    prompt_strips,
    prompt_uv,
    prompt_sample_interval,
    prompt_sensor,
    current_light_val,
    read_sensor,
    shutdown,
)


if __name__ == '__main__':

    args = get_args()
    cfg  = LightSystemConfig.from_file(args.config)

    # -- available pins (edit to match your wiring) ---------------------------
    AVAILABLE_PINS = [board.D12, board.D18, board.D21, board.D10]

    # -- hardware setup -------------------------------------------------------
    strip_pins = prompt_strips(AVAILABLE_PINS)

    lights = [Light(pin=pin, num_lights=cfg.num_lights) for pin in strip_pins]
    print(f"{len(lights)} strip(s) initialised.")

    external_pwm = None
    neopixel_pins = {get_bcm_pin_number(pin) for pin in strip_pins}
    cfg.external_pwm_enabled = False
    cfg.external_pwm_gpio = 18
    cfg.external_pwm_chip = 15
    uv_enabled, uv_gpio = prompt_uv(cfg, sorted(neopixel_pins))
    cfg.external_pwm_enabled = uv_enabled
    cfg.external_pwm_gpio = uv_gpio

    if cfg.external_pwm_enabled:
        if cfg.external_pwm_gpio in neopixel_pins:
            conflicting_pins = ", ".join(
                str(pin) for pin in sorted(neopixel_pins)
                if pin == cfg.external_pwm_gpio
            )
            shutdown(lights, log_file=None, log_filepath=None)
            sys.exit(
                f"External PWM GPIO {cfg.external_pwm_gpio} conflicts with "
                f"selected NeoPixel GPIO(s): {conflicting_pins}"
            )
        try:
            external_pwm = ExternalPwmLight(
                gpio=cfg.external_pwm_gpio,
                chip=cfg.external_pwm_chip,
                frequency=cfg.external_pwm_frequency,
                min_duty=cfg.external_pwm_min_brightness * 100,
                max_duty=cfg.external_pwm_max_brightness * 100,
            )
            print(
                f"External PWM initialised on chip {cfg.external_pwm_chip}, "
                f"GPIO {cfg.external_pwm_gpio}."
            )
        except (ImportError, OSError, RuntimeError, ValueError) as error:
            print(f"External PWM initialisation failed: {error}")
            shutdown(lights, log_file=None, log_filepath=None)
            sys.exit(1)

    sensor, logging_enabled, log_file, writer = prompt_sensor(cfg, len(lights))
    measurement_interval = (
        prompt_sample_interval()
        if logging_enabled
        else 0.0
    )
    log_filepath = log_file.name if log_file else None
    experiment_config_path = save_experiment_config(
        cfg=cfg,
        light_config_file=args.config,
        external_pwm_enabled=cfg.external_pwm_enabled,
        external_pwm_gpio=cfg.external_pwm_gpio,
        external_pwm_chip=cfg.external_pwm_chip,
        external_pwm_frequency=cfg.external_pwm_frequency,
        external_pwm_min_brightness=cfg.external_pwm_min_brightness,
        external_pwm_max_brightness=cfg.external_pwm_max_brightness,
        neopixel_pins=sorted(neopixel_pins),
        sensor_enabled=sensor is not None,
        logging_enabled=logging_enabled,
        sensor_measurement_interval=measurement_interval,
        sensor_dark_offset=(
            sensor.dark_offset
            if sensor is not None
            and isinstance(sensor, AutoRangingSensor)
            else None
        ),
        log_file_path=log_filepath,
    )

    # -- signal handler -------------------------------------------------------
    signal.signal(
        signal.SIGTERM,
        lambda sig, frame: (
            finalize_experiment_config(
                experiment_config_path,
                status='stopped_by_sigterm',
                log_file_path=log_filepath,
            ),
            shutdown(
                lights,
                log_file,
                log_filepath,
                external_pwm,
            ),
            sys.exit(0),
        )
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
        print(f"  experiment config:  {experiment_config_path}")
        print(f"  external PWM:        {'enabled' if cfg.external_pwm_enabled else 'disabled'}")
        if cfg.external_pwm_enabled:
            print(f"  PWM chip/GPIO:       {cfg.external_pwm_chip}/{cfg.external_pwm_gpio}")
            print(f"  PWM frequency:      {cfg.external_pwm_frequency:g} Hz")
            print(f"  PWM min brightness: {cfg.external_pwm_min_brightness:g}")
            print(f"  PWM max brightness: {cfg.external_pwm_max_brightness:g}")
        print(f"  sensor:              {'yes' if sensor else 'no'}")
        print(f"  logging:           {'yes' if logging_enabled else 'no'}")
        if sensor and isinstance(sensor, AutoRangingSensor):
            print(f"  dark offset:       {sensor.dark_offset:.4f} lux")
        print(f"{'--' * 20}")
        if input("Are these values correct? (y/n): ").strip().lower() == 'n':
            finalize_experiment_config(
                experiment_config_path,
                status='cancelled_in_setup',
                log_file_path=log_filepath,
            )
            shutdown(lights, log_file, log_filepath, external_pwm)
            sys.exit("Update the config file and rerun.")

    # -- test mode ------------------------------------------------------------
    if args.test:
        try:
            if lights:
                for i, light in enumerate(lights):
                    print(f"\nTesting strip {i + 1} of {len(lights)}...")
                    light.test(
                        sensor=sensor,
                        writer=writer,
                        log_file=log_file,
                        external_pwm=external_pwm,
                    )
            elif external_pwm is not None:
                print("Testing external UV PWM...")
                external_pwm.test_sine()
        except KeyboardInterrupt:
            pass
        finally:
            finalize_experiment_config(
                experiment_config_path,
                status='test_completed',
                log_file_path=log_filepath,
            )
            shutdown(lights, log_file, log_filepath, external_pwm)
        sys.exit(0)

    # -- main loop ------------------------------------------------------------
    try:
        next_measurement = time.monotonic()
        while True:
            time.sleep(0.5)
            now   = datetime.now()
            now_h = now.hour + now.minute / 60 + now.second / 3600
            val   = current_light_val(now_h, cfg)

            for light in lights:
                light.set_val(val)
            if external_pwm is not None:
                external_pwm.set_val(val, cfg.min_val, cfg.max_val)

            if logging_enabled and time.monotonic() >= next_measurement:
                next_measurement = time.monotonic() + measurement_interval
                lux_raw, vis, ir = read_sensor(sensor)
                lux_corrected = (
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

                # Only emit a set_val column when the controller is indeed
                # driving the light strips. This keeps the CSV shape honest.
                row = {
                    'timestamp':      now.isoformat(),
                    'lux_raw':        lux_raw,
                    'lux_corrected':  lux_corrected,
                    'visible':        vis,
                    'ir':             ir,
                    'sensor_settings': settings,
                    'dark_offset_lux': dark_offset,
                }
                if lights or external_pwm is not None:
                    row['set_val'] = val
                writer.writerow(row)
                log_file.flush()

    except KeyboardInterrupt:
        pass

    finally:
        finalize_experiment_config(
            experiment_config_path,
            status='stopped_by_user',
            log_file_path=log_filepath,
        )
        shutdown(lights, log_file, log_filepath, external_pwm)