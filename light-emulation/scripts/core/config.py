# core/config.py
# ============================================================
#  Central configuration dataclass for the diel light system.
# ============================================================

from dataclasses import dataclass, field
from typing import Optional
import board


@dataclass
class LightSystemConfig:
    """
    Central configuration for the entire light system.
    Edit these defaults or override them at runtime via the setup prompt.
    """
    # light cycle
    start_sunrise:     float = 7.0
    start_sunset:      float = 19.0
    twilight_duration: float = 1.5
    min_val:           float = 0.0
    max_val:           float = 0.2

    # hardware -- list of board pins, one per strip (0-4 entries)
    strip_pins: list = field(default_factory=lambda: [board.D12])
    num_lights: int  = 50

    # logging
    logging_enabled: bool         = False
    log_filename:    Optional[str] = None

    # calibration
    dark_calibration_samples: int = 30