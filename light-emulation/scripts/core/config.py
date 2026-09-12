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
        return config