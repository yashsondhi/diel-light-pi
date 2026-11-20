#!/usr/bin/env python3

import math
import signal
import time
import lgpio


# Adjust these parameters directly in the code.
GPIO_PIN = 18
GPIO_CHIP = 15
PWM_FREQUENCY = 1000
CYCLE_SECONDS = 60.0
UPDATE_SECONDS = 0.05
MIN_BRIGHTNESS = 5.0
MAX_BRIGHTNESS = 100.0
BRIGHTNESS = 100.0
START_PHASE = -math.pi / 2
RUN_DURATION_SECONDS = 0  # 0 runs continuously.


def clamp(value, minimum=0.0, maximum=100.0):
    return max(minimum, min(maximum, value))


def main():
    if PWM_FREQUENCY <= 0:
        raise ValueError("PWM_FREQUENCY must be greater than zero")
    if CYCLE_SECONDS <= 0:
        raise ValueError("CYCLE_SECONDS must be greater than zero")
    if UPDATE_SECONDS <= 0:
        raise ValueError("UPDATE_SECONDS must be greater than zero")
    if clamp(MIN_BRIGHTNESS) > clamp(MAX_BRIGHTNESS):
        raise ValueError(
            "MIN_BRIGHTNESS must be less than or equal to MAX_BRIGHTNESS"
        )

    minimum = clamp(MIN_BRIGHTNESS)
    maximum = clamp(MAX_BRIGHTNESS)
    brightness = clamp(BRIGHTNESS)
    chip = lgpio.gpiochip_open(GPIO_CHIP)
    lgpio.gpio_claim_output(chip, GPIO_PIN)

    running = True
    start_time = time.monotonic()

    def stop(_signum=None, _frame=None):
        nonlocal running
        running = False

    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)

    try:
        print(
            f"GPIO {GPIO_PIN}: PWM {PWM_FREQUENCY:g} Hz, "
            f"cycle {CYCLE_SECONDS:g}s, "
            f"range {minimum:g}-{maximum:g}%"
        )

        while running:
            elapsed = time.monotonic() - start_time

            if RUN_DURATION_SECONDS > 0:
                if elapsed >= RUN_DURATION_SECONDS:
                    break

            sine = math.sin(
                (2.0 * math.pi * elapsed / CYCLE_SECONDS) + START_PHASE
            )
            normalized = (sine + 1.0) / 2.0

            duty_cycle = minimum + (maximum - minimum) * normalized
            duty_cycle *= brightness / 100.0
            duty_cycle = clamp(duty_cycle)

            lgpio.tx_pwm(chip, GPIO_PIN, PWM_FREQUENCY, duty_cycle)

            lgpio.tx_pwm(
                chip,
                GPIO_PIN,
                PWM_FREQUENCY,
                duty_cycle,
            )
            time.sleep(UPDATE_SECONDS)

    finally:
        lgpio.tx_pwm(chip, GPIO_PIN, PWM_FREQUENCY, 0)
        lgpio.gpiochip_close(chip)
        print("PWM stopped.")


if __name__ == "__main__":
    main()