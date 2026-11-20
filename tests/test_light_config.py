import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'light-emulation' / 'scripts'))

from core.config import LightSystemConfig
from core.helpers import (
    get_args,
    prompt_uv,
    save_experiment_config,
    finalize_experiment_config,
)


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


@pytest.mark.parametrize('setting', [
    'external_pwm_enabled',
    'external_pwm_gpio',
    'external_pwm_chip',
])
def test_light_config_rejects_terminal_hardware_settings(tmp_path, setting):
    config_path = tmp_path / 'light_config.txt'
    config_path.write_text(f'{setting} = 18\n', encoding='utf-8')

    with pytest.raises(ValueError, match='unsupported setting'):
        LightSystemConfig.from_file(str(config_path))


def test_light_config_loads_external_pwm_cycle_settings(tmp_path):
    config_path = tmp_path / 'light_config.txt'
    config_path.write_text(
        'external_pwm_frequency = 750\n'
        'external_pwm_min_brightness = 0.1\n'
        'external_pwm_max_brightness = 0.8\n',
        encoding='utf-8',
    )

    config = LightSystemConfig.from_file(str(config_path))

    assert config.external_pwm_frequency == 750.0
    assert config.external_pwm_min_brightness == 0.1
    assert config.external_pwm_max_brightness == 0.8


def test_prompt_uv_can_disable_external_light(monkeypatch):
    config = LightSystemConfig()
    config.external_pwm_enabled = True
    monkeypatch.setattr('builtins.input', lambda prompt='': 'n')

    enabled, gpio = prompt_uv(config, [])

    assert enabled is False
    assert gpio == 18


def test_prompt_uv_accepts_available_gpio(monkeypatch):
    config = LightSystemConfig()
    answers = iter(['y', '21'])
    monkeypatch.setattr(
        'builtins.input',
        lambda prompt='': next(answers),
    )

    enabled, gpio = prompt_uv(config, [18])

    assert enabled is True
    assert gpio == 21


def test_save_experiment_config_creates_dated_full_record(tmp_path, monkeypatch):
    import core.helpers as helpers

    config_directory = tmp_path / 'configs'
    monkeypatch.setattr(
        helpers,
        'EXPERIMENT_CONFIG_DIRECTORY',
        str(config_directory),
    )
    cfg = LightSystemConfig(
        start_sunrise=6.5,
        start_sunset=20.0,
        twilight_duration=2.0,
        min_val=0.01,
        max_val=0.3,
        num_lights=60,
        external_pwm_frequency=750.0,
        external_pwm_min_brightness=0.1,
        external_pwm_max_brightness=0.8,
    )
    saved_path = save_experiment_config(
        cfg=cfg,
        light_config_file='/tmp/light_config.txt',
        external_pwm_enabled=True,
        external_pwm_gpio=21,
        external_pwm_chip=15,
        external_pwm_frequency=750.0,
        external_pwm_min_brightness=0.1,
        external_pwm_max_brightness=0.8,
        neopixel_pins=[18],
        sensor_enabled=True,
        logging_enabled=True,
        sensor_measurement_interval=2.0,
        sensor_dark_offset=1.25,
        log_file_path='/tmp/light.csv',
    )

    path = Path(saved_path)
    content = path.read_text(encoding='utf-8')
    assert path.name.startswith('experiment_')
    assert path.suffix == '.txt'
    assert 'start_sunrise = 6.5' in content
    assert 'neopixel_pins = 18' in content
    assert 'external_pwm_gpio = 21' in content
    assert 'sensor_measurement_interval_seconds = 2' in content
    assert 'sensor_dark_offset_lux = 1.25' in content
    assert 'log_file = /tmp/light.csv' in content


def test_finalize_experiment_config_records_stop_and_data(tmp_path):
    experiment_path = tmp_path / 'experiment_2026-11-20_14-00-00.txt'
    experiment_path.write_text(
        'experiment_started_at = 2026-11-20T14:00:00\n'
        'experiment_stopped_at = still_running\n'
        'experiment_status = running\n'
        'data_location = none\n',
        encoding='utf-8',
    )

    finalize_experiment_config(
        str(experiment_path),
        status='stopped_by_user',
        log_file_path='/tmp/light.csv',
    )

    content = experiment_path.read_text(encoding='utf-8')
    assert 'experiment_stopped_at = ' in content
    assert 'still_running' not in content
    assert 'experiment_status = stopped_by_user' in content
    assert 'data_location = /tmp/light.csv' in content