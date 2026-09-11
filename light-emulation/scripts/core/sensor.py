# core/sensor.py
# ============================================================
#  TSL2591 light sensor wrapper with automatic gain and
#  integration time ranging.
# ============================================================

import time
import numpy as np
from typing import Optional, Tuple

try:
    import adafruit_tsl2591
    TSL2591_AVAILABLE = True
except ImportError:
    TSL2591_AVAILABLE = False


class AutoRangingSensor:
    """
    Wraps a TSL2591 sensor and automatically adjusts gain and integration time
    to keep ADC counts in a safe working range.

    The TSL2591 has a 16-bit ADC so raw counts range from 0 to 65535. We
    target below 55000 counts to stay well clear of saturation, and above 100
    to stay clear of noise.

    Gain and integration time are treated as a single ordered sensitivity
    ladder. After each read the auto-ranger steps up (more sensitive) or down
    (less sensitive) depending on whether the reading was too low, too high,
    or comfortably in range.

    Ladder (least to most sensitive):
      Step 0  LOW  / 100ms  --  bright sunlight
      Step 1  LOW  / 200ms
      Step 2  MED  / 100ms  --  default start (indoor / moderate)
      Step 3  MED  / 200ms
      Step 4  HIGH / 100ms
      Step 5  HIGH / 300ms
      Step 6  MAX  / 100ms
      Step 7  MAX  / 600ms  --  near darkness / moonlight
    """

    COUNT_MIN = 100
    COUNT_MAX = 55000
    ABS_MAX   = 65535

    def __init__(self, i2c, name: str = "sensor"):
        if not TSL2591_AVAILABLE:
            raise RuntimeError("adafruit_tsl2591 is not installed.")

        self.sensor        = adafruit_tsl2591.TSL2591(i2c)
        self.name          = name
        self.step          = 2
        self._dark_offset: float = 0.0

        self._ladder = [
            (adafruit_tsl2591.GAIN_LOW,  adafruit_tsl2591.INTEGRATIONTIME_100MS, "LOW  / 100ms"),
            (adafruit_tsl2591.GAIN_LOW,  adafruit_tsl2591.INTEGRATIONTIME_200MS, "LOW  / 200ms"),
            (adafruit_tsl2591.GAIN_MED,  adafruit_tsl2591.INTEGRATIONTIME_100MS, "MED  / 100ms"),
            (adafruit_tsl2591.GAIN_MED,  adafruit_tsl2591.INTEGRATIONTIME_200MS, "MED  / 200ms"),
            (adafruit_tsl2591.GAIN_HIGH, adafruit_tsl2591.INTEGRATIONTIME_100MS, "HIGH / 100ms"),
            (adafruit_tsl2591.GAIN_HIGH, adafruit_tsl2591.INTEGRATIONTIME_300MS, "HIGH / 300ms"),
            (adafruit_tsl2591.GAIN_MAX,  adafruit_tsl2591.INTEGRATIONTIME_100MS, "MAX  / 100ms"),
            (adafruit_tsl2591.GAIN_MAX,  adafruit_tsl2591.INTEGRATIONTIME_600MS, "MAX  / 600ms"),
        ]

        self._int_seconds = {
            adafruit_tsl2591.INTEGRATIONTIME_100MS: 0.1,
            adafruit_tsl2591.INTEGRATIONTIME_200MS: 0.2,
            adafruit_tsl2591.INTEGRATIONTIME_300MS: 0.3,
            adafruit_tsl2591.INTEGRATIONTIME_400MS: 0.4,
            adafruit_tsl2591.INTEGRATIONTIME_500MS: 0.5,
            adafruit_tsl2591.INTEGRATIONTIME_600MS: 0.6,
        }

        self._apply_step()

    # -- private helpers ------------------------------------------------------

    def _apply_step(self) -> None:
        """Push the current ladder step's settings to the sensor hardware."""
        gain, integration, label = self._ladder[self.step]
        self.sensor.gain             = gain
        self.sensor.integration_time = integration
        print(f"  [{self.name}] sensitivity -> {label}")

    def _settle(self, previous_step: int) -> None:
        """
        Wait for the sensor to produce a valid reading after a gain or
        integration time change.

        The worst case occurs when a settings change happens at the very
        beginning of a slow integration cycle. The sensor must:
          - Complete the in-progress (old) integration cycle  [t_old]
          - Complete one full fresh (new) integration cycle   [t_new]

        Settling time = t_int_old + t_int_new + 100ms fixed margin.

        Using 2 * t_new would under-wait when stepping down to a faster
        integration time from a slower one. 
        """
        _, old_integration, _ = self._ladder[previous_step]
        _, new_integration, _ = self._ladder[self.step]

        t_old = self._int_seconds.get(old_integration, 0.1)
        t_new = self._int_seconds.get(new_integration, 0.1)

        time.sleep(t_old + t_new + 0.1)

    def _step_up(self) -> bool:
        """Increase sensitivity. Returns True if the step changed."""
        if self.step < len(self._ladder) - 1:
            self.step += 1
            self._apply_step()
            return True
        return False

    def _step_down(self) -> bool:
        """Decrease sensitivity. Returns True if the step changed."""
        if self.step > 0:
            self.step -= 1
            self._apply_step()
            return True
        return False

    # -- public methods -------------------------------------------------------

    def read(self) -> Tuple[Optional[float], Optional[float], Optional[float]]:
        """
        Read the sensor with auto-ranging.

        After each raw read:
        full >= ABS_MAX  -> hard saturation -> step down, return None tuple
                            (no settle — result is discarded, next call settles)
        full > COUNT_MAX -> near saturation -> step down, settle, re-read
        full < COUNT_MIN -> signal too weak -> step up,   settle, re-read
        otherwise        -> in range        -> return (lux, visible, ir)

        Returns:
            (lux_raw, visible, ir) or (None, None, None) on error/saturation.
        """
        try:
            full, ir = self.sensor.raw_luminosity

            # Hard saturation — sensor is pegged, step down and bail.
            # No settle here: the result will be discarded and the next
            # call to read() will trigger a fresh settle if needed.
            if full >= self.ABS_MAX or ir >= self.ABS_MAX:
                self._step_down()
                return None, None, None

            # Near saturation — step down and re-read after settling.
            if full > self.COUNT_MAX:
                previous_step = self.step
                if self._step_down():
                    self._settle(previous_step)

            # Signal too weak — step up and re-read after settling.
            elif full < self.COUNT_MIN:
                previous_step = self.step
                if self._step_up():
                    self._settle(previous_step)

            return self.sensor.lux, self.sensor.visible, self.sensor.infrared

        except Exception as e:
            print(f"  [{self.name}] read error: {e}")
            return None, None, None

    def calibrate_dark(self, n_samples: int = 30) -> None:
        """
        Estimate the dark-current offset by averaging n_samples readings.

        Should be called before the main loop with the sensor in the
        darkest available conditions. The result is stored in dark_offset
        and applied automatically by corrected_lux().

        Args:
            n_samples: number of readings to average (default 30,
                       giving ~15 seconds at 0.5 s intervals).
        """
        print(f"  [{self.name}] Collecting {n_samples} dark calibration samples...")
        readings = []
        for i in range(n_samples):
            lux, _, _ = self.read()
            if lux is not None:
                readings.append(lux)
            time.sleep(0.5)
            if (i + 1) % 10 == 0:
                print(f"    {i + 1}/{n_samples} samples collected...")

        if not readings:
            print(
                f"  [{self.name}] WARNING: all dark samples returned None "
                f"-- offset left at 0.0"
            )
            return

        self._dark_offset = float(np.mean(readings))
        std = float(np.std(readings))
        print(
            f"  [{self.name}] Dark offset: {self._dark_offset:.4f} lux "
            f"(std={std:.4f}, n={len(readings)})"
        )

    def corrected_lux(self, lux_raw: Optional[float]) -> Optional[float]:
        """
        Subtract the dark offset and clamp to zero.

        lux_corrected = max(0, lux_raw - dark_offset)

        Args:
            lux_raw: raw lux from read(), or None.

        Returns:
            Corrected lux as float, or None if lux_raw is None.
        """
        if lux_raw is None:
            return None
        return max(0.0, lux_raw - self._dark_offset)

    @property
    def dark_offset(self) -> float:
        """The stored dark-current offset in lux."""
        return self._dark_offset

    @property
    def current_settings_label(self) -> str:
        """Human-readable string of the current gain/integration step."""
        return self._ladder[self.step][2]