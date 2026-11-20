import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'light-emulation' / 'scripts'))

from core.config import LightSystemConfig
from core.helpers import get_args


def test_light_config_loads_supported_settings(tmp_path):
    config_path = tmp_path / 'light_config.txt'
    config_path.write_text(
        '# comments are allowed\n'
        'start_sunrise = 6.5\n'
        'start_sunset = 20\n'
        'twilight_duration = 2\n'
        'min_val = 0.01\n'
        'max_val = 0.3\n'
        'num_lights = 60\n',
        encoding='utf-8',
    )

    config = LightSystemConfig.from_file(str(config_path))

    assert config.start_sunrise == 6.5
    assert config.start_sunset == 20.0
    assert config.twilight_duration == 2.0
    assert config.min_val == 0.01
    assert config.max_val == 0.3
    assert config.num_lights == 60


def test_default_light_config_path_is_above_scripts_directory(monkeypatch):
    monkeypatch.setattr(sys, 'argv', ['smooth_light_control.py'])

    args = get_args()

    expected = Path(__file__).resolve().parents[1] / 'light-emulation' / 'light_config.txt'
    assert Path(args.config) == expected


@pytest.mark.parametrize('setting', ['strip_pins', 'sensor', 'logging_enabled'])
def test_light_config_rejects_interactive_settings(tmp_path, setting):
    config_path = tmp_path / 'light_config.txt'
    config_path.write_text(f'{setting} = enabled\n', encoding='utf-8')

    with pytest.raises(ValueError, match='unsupported setting'):
        LightSystemConfig.from_file(str(config_path))


def test_light_config_loads_external_pwm_settings(tmp_path):
    config_path = tmp_path / 'light_config.txt'
    config_path.write_text(
        'external_pwm_enabled = true\n'
        'external_pwm_gpio = 18\n'
        'external_pwm_chip = 15\n'
        'external_pwm_frequency = 1000\n'
        'external_pwm_max_duty = 80\n',
        encoding='utf-8',
    )

    config = LightSystemConfig.from_file(str(config_path))

    assert config.external_pwm_enabled is True
    assert config.external_pwm_gpio == 18
    assert config.external_pwm_chip == 15
    assert config.external_pwm_frequency == 1000.0
    assert config.external_pwm_max_duty == 80.0