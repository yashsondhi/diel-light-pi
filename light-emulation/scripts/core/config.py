# core/config.py
# ============================================================
#  Central configuration dataclass for the diel light system.
# ============================================================

from dataclasses import dataclass
import os


@dataclass
class LightSystemConfig:
    """
    Light-cycle configuration loaded from a text file.

    Strip selection, sensor enablement, and logging are selected interactively
    at startup and are deliberately not stored here.
    """
    # light cycle
    start_sunrise:     float = 7.0
    start_sunset:      float = 19.0
    twilight_duration: float = 1.5
    min_val:           float = 0.0
    max_val:           float = 0.2

    # hardware -- number of pixels on each interactively selected strip
    num_lights: int  = 50

    # optional GPIO PWM output
    external_pwm_enabled: bool = False
    external_pwm_gpio: int = 18
    external_pwm_chip: int = 15
    external_pwm_frequency: float = 1000.0
    external_pwm_max_duty: float = 100.0

    # calibration
    dark_calibration_samples: int = 30

    @classmethod
    def from_file(cls, path: str) -> 'LightSystemConfig':
        """Load supported settings from a simple ``key = value`` file."""
        values = {}
        supported = {
            'start_sunrise': float,
            'start_sunset': float,
            'twilight_duration': float,
            'min_val': float,
            'max_val': float,
            'num_lights': int,
            'external_pwm_enabled': lambda value: cls._parse_bool(value),
            'external_pwm_gpio': int,
            'external_pwm_chip': int,
            'external_pwm_frequency': float,
            'external_pwm_max_duty': float,
        }

        if not os.path.isfile(path):
            raise FileNotFoundError(f"Config file not found: {path}")

        with open(path, encoding='utf-8') as config_file:
            for line_number, raw_line in enumerate(config_file, start=1):
                line = raw_line.split('#', 1)[0].strip()
                if not line:
                    continue
                if '=' not in line:
                    raise ValueError(
                        f"{path}:{line_number}: expected 'key = value'"
                    )

                key, raw_value = (part.strip() for part in line.split('=', 1))
                if key not in supported:
                    raise ValueError(
                        f"{path}:{line_number}: unsupported setting '{key}'"
                    )
                try:
                    values[key] = supported[key](raw_value)
                except ValueError as error:
                    raise ValueError(
                        f"{path}:{line_number}: invalid value for '{key}'"
                    ) from error

        config = cls(**values)
        if config.twilight_duration <= 0:
            raise ValueError('twilight_duration must be greater than zero')
        if config.num_lights <= 0:
            raise ValueError('num_lights must be greater than zero')
        if not 0 <= config.min_val <= 1:
            raise ValueError('min_val must be between zero and one')
        if not 0 <= config.max_val <= 1:
            raise ValueError('max_val must be between zero and one')
        if config.min_val > config.max_val:
            raise ValueError('min_val must not exceed max_val')
        if config.external_pwm_gpio < 0:
            raise ValueError('external_pwm_gpio must be zero or greater')
        if config.external_pwm_chip < 0:
            raise ValueError('external_pwm_chip must be zero or greater')
        if config.external_pwm_frequency <= 0:
            raise ValueError('external_pwm_frequency must be greater than zero')
        if not 0 < config.external_pwm_max_duty <= 100:
            raise ValueError(
                'external_pwm_max_duty must be greater than zero '
                'and no more than 100'
            )
        return config

    @staticmethod
    def _parse_bool(value: str) -> bool:
        normalized = value.strip().lower()
        if normalized in ('true', 'yes', 'y', '1', 'on', 'enabled'):
            return True
        if normalized in ('false', 'no', 'n', '0', 'off', 'disabled'):
            return False
        raise ValueError('expected a boolean value')