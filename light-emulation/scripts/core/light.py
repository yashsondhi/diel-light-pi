# core/light.py
# ============================================================
#  NeoPixel LED strip controller.
# ============================================================

import time
import numpy as np
import board
import neopixel
from datetime import datetime
from typing import Optional

from core.sensor import AutoRangingSensor


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
        return self.curr_val[0] * 60 + self.curr_val[1]

    def off(self) -> None:
        """Turn off all pixels immediately."""
        self.pixels.fill((0, 0, 0))
        self.pixels.show()

    def test(
        self,
        sensor=None,
        writer=None,
        log_file=None,
    ) -> None:
        """
        Run a sine wave brightness sweep across the strip.
        Optionally logs sensor readings during the test.

        Args:
            sensor:   AutoRangingSensor instance or None.
            writer:   csv.writer instance or None.
            log_file: open file object for flushing, or None.
        """
        from core.helpers import read_sensor

        print("Starting light test...")
        vals  = np.sin(np.linspace(0, 5 * np.pi, 1000))
        vals += 1
        vals /= 2

        for i, val in enumerate(vals):
            self.set_val(val)

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