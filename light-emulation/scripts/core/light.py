# core/light.py
# ============================================================
#  NeoPixel LED strip controller.
# ============================================================

import math
import time
import numpy as np
import board
import neopixel
from datetime import datetime
from typing import Optional

from core.sensor import AutoRangingSensor

try:
    import lgpio
except ImportError:
    lgpio = None


class ExternalPwmLight:
    """Controls one external load through an lgpio PWM output."""

    def __init__(
        self,
        gpio: int = 18,
        chip: int = 15,
        frequency: float = 1000.0,
        min_duty: float = 0.0,
        max_duty: float = 100.0,
    ):
        if lgpio is None:
            raise ImportError(
                "lgpio is required for external PWM; install python3-lgpio "
                "and run with the matching Python environment"
            )
        if gpio < 0:
            raise ValueError("gpio must be zero or greater")
        if chip < 0:
            raise ValueError("chip must be zero or greater")
        if frequency <= 0:
            raise ValueError("frequency must be greater than zero")
        if not 0 <= min_duty <= 100:
            raise ValueError("min_duty must be between zero and 100")
        if not 0 <= max_duty <= 100:
            raise ValueError("max_duty must be between zero and 100")
        if min_duty > max_duty:
            raise ValueError("min_duty must not exceed max_duty")

        self.gpio = gpio
        self.chip_number = chip
        self.frequency = frequency
        self.min_duty = min_duty
        self.max_duty = max_duty
        lgpio_error = getattr(lgpio, "error", RuntimeError)
        try:
            self.chip = lgpio.gpiochip_open(chip)
            lgpio.gpio_claim_output(self.chip, gpio)
            lgpio.tx_pwm(self.chip, gpio, frequency, 0)
        except (OSError, lgpio_error) as error:
            if 'self.chip' in locals():
                lgpio.gpiochip_close(self.chip)
            raise RuntimeError(
                f"unable to initialise PWM on chip {chip}, GPIO {gpio}: {error}"
            ) from error
        self._closed = False

    def set_val(
        self,
        prop_val: float = 0,
        min_prop: float = 0,
        max_prop: float = 1,
    ) -> None:
        """Map a proportional light value onto the configured PWM duty range."""
        if not 0 <= prop_val <= 1:
            raise ValueError("prop_val must be in [0.0, 1.0]")
        if not 0 <= min_prop <= 1:
            raise ValueError("min_prop must be in [0.0, 1.0]")
        if not 0 <= max_prop <= 1:
            raise ValueError("max_prop must be in [0.0, 1.0]")
        if min_prop > max_prop:
            raise ValueError("min_prop must not exceed max_prop")
        if max_prop == min_prop:
            normalized = 0.0
        else:
            normalized = (prop_val - min_prop) / (max_prop - min_prop)
        normalized = max(0.0, min(1.0, normalized))
        duty_cycle = self.min_duty + (
            (self.max_duty - self.min_duty) * normalized
        )
        lgpio.tx_pwm(
            self.chip,
            self.gpio,
            self.frequency,
            duty_cycle,
        )

    def off(self) -> None:
        """Stop PWM and drive the GPIO low."""
        if self._closed:
            return
        lgpio.tx_pwm(self.chip, self.gpio, self.frequency, 0)
        lgpio.gpio_write(self.chip, self.gpio, 0)
        lgpio.gpiochip_close(self.chip)
        self._closed = True

    def test_sine(self, steps: int = 1000, step_seconds: float = 0.01) -> None:
        """Run a sine brightness sweep without closing the PWM channel."""
        for i in range(steps):
            angle = 5 * math.pi * i / (steps - 1)
            normalized = (math.sin(angle) + 1) / 2
            self.set_val(normalized)
            time.sleep(step_seconds)
        self.set_val(0)


class Light:
    """
    Controls a single NeoPixel LED strip.

    Brightness is distributed randomly across pixels to avoid hot spots.
    The strip is driven by a proportional value in [0.0, 1.0] or an
    absolute integer value.
    """

    def __init__(self, pin=board.D18, num_lights: int = 50):
        self.pin        = pin
        self.num_lights = num_lights
        self.pixels     = neopixel.NeoPixel(
            self.pin, self.num_lights, auto_write=False
        )
        self.pixels.fill(0)
        self.max_val  = num_lights * 255
        self.curr_val = (0, 0)

    def set_val(self, prop_val: float = 0, abs_val: Optional[int] = None) -> None:
        """
        Set strip brightness.

        Args:
            prop_val: proportional brightness in [0.0, 1.0].
            abs_val:  absolute brightness integer. Overrides prop_val if given.
        """
        update = False
        if abs_val is None:
            abs_val = round(prop_val * self.max_val)
        else:
            assert isinstance(abs_val, int), "type(abs_val) must be int"
            assert abs_val in range(self.max_val), "abs_val must be in range(self.max_val)"
            update = True

        base_val    = int(abs_val / self.num_lights)
        row_val     = int(abs_val % self.num_lights)
        row_change  = row_val  - self.curr_val[1]
        base_change = base_val - self.curr_val[0]
        change_val  = 1
        change_inds = np.random.choice(range(self.num_lights), row_val, replace=False)

        if abs_val != self.abs_val() or update:
            if base_change == 0 and self.curr_val[1] != 0:
                if row_change > 0:
                    free_inds = np.where(
                        np.round(np.mean(self.pixels, 1)).astype(int) - base_val == 0
                    )[0]
                    change_inds = np.random.choice(free_inds, row_change, replace=False)
                elif row_change < 0:
                    change_val  = 0
                    free_inds   = np.where(
                        np.round(np.mean(self.pixels, 1)).astype(int) - base_val == 1
                    )[0]
                    change_inds = np.random.choice(free_inds, -row_change, replace=False)
                elif row_change == 0:
                    return
            else:
                self.pixels.fill((base_val, base_val, base_val))
                change_inds = np.random.choice(
                    range(self.num_lights), row_val, replace=False
                )

            change_val += base_val
            for ind in change_inds:
                self.pixels[ind] = (change_val, change_val, change_val)
            self.curr_val = (base_val, row_val)
            self.pixels.show()

    def abs_val(self) -> int:
        """Return the current absolute brightness value."""
        return self.curr_val[0] * self.num_lights + self.curr_val[1]

    def off(self) -> None:
        """Turn off all pixels immediately."""
        self.pixels.fill((0, 0, 0))
        self.pixels.show()

    def test(
        self,
        sensor=None,
        writer=None,
        log_file=None,
        external_pwm=None,
    ) -> None:
        """
        Run a sine wave brightness sweep across the strip.
        Optionally logs sensor readings during the test.

        Args:
            sensor:   AutoRangingSensor instance or None.
            writer:   csv.writer instance or None.
            log_file: open file object for flushing, or None.
            external_pwm: ExternalPwmLight instance or None.
        """
        from core.helpers import read_sensor

        print("Starting light test...")
        vals  = np.sin(np.linspace(0, 5 * np.pi, 1000))
        vals += 1
        vals /= 2

        for i, val in enumerate(vals):
            self.set_val(val)
            if external_pwm is not None:
                external_pwm.set_val(val)

            if sensor is not None:
                lux_raw, vis, ir = read_sensor(sensor)
                lux_corr = (
                    sensor.corrected_lux(lux_raw)
                    if isinstance(sensor, AutoRangingSensor)
                    else lux_raw
                )
                if i % 10 == 0:
                    print(
                        f"  step {i:>4} | set_val={val:.4f} | "
                        f"lux_raw={lux_raw} | lux_corr={lux_corr} | "
                        f"vis={vis} | ir={ir}"
                    )
                if writer is not None:
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
                        datetime.now().isoformat(),
                        val,
                        lux_raw,
                        lux_corr,
                        vis,
                        ir,
                        settings,
                        dark_offset,
                    ])
                    if log_file:
                        log_file.flush()

            time.sleep(0.01)

        self.set_val()
        print("Light test complete.")