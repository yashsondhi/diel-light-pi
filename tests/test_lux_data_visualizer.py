import os
import sys
from pathlib import Path

import pandas as pd


def test_gui_dialog_initial_directories_point_at_config_folders():
    gui_path = Path(__file__).resolve().parents[1] / 'activity-monitoring' / 'gui_diel-light.py'
    gui_source = gui_path.read_text()

    assert "initialdir=os.path.join(SCRIPT_DIR, 'project-configs')" in gui_source
    assert "initialdir=os.path.join(SCRIPT_DIR, 'motion-configs')" in gui_source


def test_gui_update_elements_normalizes_yaml_none_into_empty_text():
    gui_path = Path(__file__).resolve().parents[1] / 'activity-monitoring' / 'gui_diel-light.py'
    gui_source = gui_path.read_text()

    assert "def gui_text" in gui_source
    assert 'trial_name_entry.insert(tk.END, gui_text(config.get("TRIALNAME", "")))' in gui_source

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'light-emulation' / 'scripts'))

import lux_data_visualizer as viz
from core.helpers import get_default_log_dir


def test_build_chart_output_path_uses_charts_folder():
    chart_path = viz.build_chart_output_path('data/raw/sample.csv')
    assert chart_path.endswith('charts\\sample.png') or chart_path.endswith('charts/sample.png')


def test_make_timestamp_axis_label_returns_day_range_with_year():
    timestamps = pd.to_datetime(
        [
            '2026-09-01 00:00:00',
            '2026-09-01 12:00:00',
        ]
    )

    label = viz.make_timestamp_axis_label(timestamps)
    assert label == 'Time — 09/01/26-09/01/26'

    timestamps = pd.to_datetime(
        [
            '2026-09-01 00:00:00',
            '2026-09-30 00:00:00',
        ]
    )

    label = viz.make_timestamp_axis_label(timestamps)
    assert label == 'Time — 09/01/26-09/30/26'


def test_get_default_log_dir_uses_light_emulation_data_raw_folder():
    expected = str(Path(__file__).resolve().parents[1] / 'light-emulation' / 'data' / 'raw')
    assert get_default_log_dir() == expected


def test_resolve_lux_plot_columns_supports_current_sensor_schema():
    df = pd.DataFrame(
        [
            {
                'timestamp': '2026-09-01T11:33:04.808873',
                'set_val': 0.2,
                'lux_raw': 437.63059200000004,
                'lux_corrected': 437.63059200000004,
                'visible': 3303,
                'ir': 971,
                'sensor_settings': 'MED  / 100ms',
                'dark_offset_lux': 0.0,
            }
        ]
    )

    columns = viz.resolve_lux_plot_columns(df)

    assert columns['series'] == ['lux_corrected']
    assert columns['labels'] == ['Lux Corrected']
