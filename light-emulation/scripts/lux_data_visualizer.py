import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
RAW_DIR = os.path.join(DATA_DIR, 'raw')
CHART_DIR = os.path.join(DATA_DIR, 'charts')


def build_chart_output_path(filename):
    """Return the data/charts path for the generated PNG artifact."""
    os.makedirs(CHART_DIR, exist_ok=True)
    stem = os.path.splitext(os.path.basename(filename))[0]
    return os.path.join(CHART_DIR, f'{stem}.png')


def choose_timestamp_axis_format(timestamps):
    """Return a Matplotlib date format string from the span of the timestamps.

    The formatter intentionally carries the month in the output so the axis
    shows the calendar month, and then narrows the time display when the data
    span is short enough to benefit from seconds/minutes.
    """
    timestamps = pd.to_datetime(timestamps, errors='coerce')
    timestamps = timestamps.dropna()
    if timestamps.empty:
        return '%b %d %Y %H:%M:%S'

    start = timestamps.min()
    end = timestamps.max()
    span = end - start

    if span <= pd.Timedelta(minutes=10):
        return '%H:%M:%S'
    if span <= pd.Timedelta(hours=12):
        return '%H:%M'
    if span <= pd.Timedelta(days=31):
        return '%b %d %H:%M'
    if span <= pd.Timedelta(days=365):
        return '%b %d'
    return '%b %Y'


def make_timestamp_axis_label(timestamps):
    """Return a compact day-by-day range label like 8/1/26-9/1/26.

    The label always carries the year, but stays focused on the date range
    rather than printing the month and hour stragglers behind a long axis title.
    """
    timestamps = pd.to_datetime(timestamps, errors='coerce')
    timestamps = timestamps.dropna()
    if timestamps.empty:
        return 'Time — 00/00/00-00/00/00'

    start = timestamps.min()
    end = timestamps.max()

    return f'Time — {start:%m/%d/%y}-{end:%m/%d/%y}'


def resolve_lux_plot_columns(df):
    """Return a plotting-ready series/label map for the current and legacy lux schemas.

    Current schema example:
        timestamp,set_val,lux_raw,lux_corrected,visible,ir,sensor_settings,dark_offset_lux

    Legacy schema example:
        timestamp,set_val,top_lux,top_visible,top_ir,bottom_lux,bottom_visible,bottom_ir
    """
    if 'lux_corrected' in df.columns:
        return {
            'series': ['lux_corrected'],
            'labels': ['Lux Corrected'],
        }

    if 'lux_raw' in df.columns:
        return {
            'series': ['lux_raw'],
            'labels': ['Lux Raw'],
        }

    if {'top_lux', 'bottom_lux'}.issubset(df.columns):
        return {
            'series': ['top_lux', 'bottom_lux'],
            'labels': ['Top Lux', 'Bottom Lux'],
        }

    return {
        'series': [],
        'labels': [],
    }


def resolve_sensor_plot_columns(df, sensor_name):
    """Return plotting columns for a current or legacy visible/IR sensor."""
    if sensor_name in df.columns:
        return {
            'series': [sensor_name],
            'labels': [sensor_name.title()],
        }

    legacy_series = [f'top_{sensor_name}', f'bottom_{sensor_name}']
    if set(legacy_series).issubset(df.columns):
        return {
            'series': legacy_series,
            'labels': [f'Top {sensor_name.title()}', f'Bottom {sensor_name.title()}'],
        }

    return {
        'series': [],
        'labels': [],
    }


def main():
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(CHART_DIR, exist_ok=True)

    if len(sys.argv) < 2:
        if not os.path.exists(RAW_DIR):
            sys.exit(f"Data directory not found: {RAW_DIR}")
        csvs = [f for f in os.listdir(RAW_DIR) if f.endswith('.csv')]
        if not csvs:
            sys.exit("No CSV files found in data/raw/")
        filename = os.path.join(RAW_DIR, max(csvs, key=lambda f: os.path.getmtime(os.path.join(RAW_DIR, f))))
        print(f"Using most recent log: {filename}")
    else:
        raw_argument = sys.argv[1]
        if os.path.exists(raw_argument) and os.path.isfile(raw_argument):
            filename = raw_argument
        elif os.path.exists(os.path.join(RAW_DIR, raw_argument)) and os.path.isfile(os.path.join(RAW_DIR, raw_argument)):
            filename = os.path.join(RAW_DIR, raw_argument)
        elif raw_argument.endswith('.csv'):
            filename = os.path.join(RAW_DIR, raw_argument)
        else:
            filename = raw_argument

    df = pd.read_csv(filename)
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'], format='mixed', errors='coerce')

    df = df.dropna(subset=['timestamp'])

    has_set_val = 'set_val' in df.columns
    if not has_set_val:
        print("Warning: no 'set_val' column found, skipping set value plot")

    fig, (ax1, ax_visible) = plt.subplots(
        2, 1, figsize=(12, 8), sharex=True
    )

    if 'timestamp' in df.columns:
        timestamp_format = choose_timestamp_axis_format(df['timestamp'])
        ax1.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax1.xaxis.set_major_formatter(mdates.DateFormatter(timestamp_format))
        plt.setp(ax1.get_xticklabels(), rotation=45, ha='right')
        ax1.set_xlabel(make_timestamp_axis_label(df['timestamp']))
    else:
        ax1.set_xlabel('Time')

    ax1.set_ylabel('Lux', color='tab:blue')

    series_columns = resolve_lux_plot_columns(df)
    for series_name, label in zip(series_columns['series'], series_columns['labels']):
        if series_name in df.columns:
            ax1.plot(df['timestamp'], df[series_name], label=label, color='tab:blue')

    ax1.tick_params(axis='y', labelcolor='tab:blue')

    ax2 = ax1.twinx()
    if has_set_val:
        ax2.set_ylabel('Set Value (0-1)', color='tab:orange')
        ax2.plot(df['timestamp'], df['set_val'], label='Set Val', color='tab:orange', linestyle='--')
        ax2.tick_params(axis='y', labelcolor='tab:orange')
        lines2, labels2 = ax2.get_legend_handles_labels()
    else:
        lines2, labels2 = [], []

    lines1, labels1 = ax1.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='lower right')

    visible_columns = resolve_sensor_plot_columns(df, 'visible')
    for series_name, label in zip(visible_columns['series'], visible_columns['labels']):
        ax_visible.plot(
            df['timestamp'],
            df[series_name],
            label=label,
            color='tab:green',
        )
    ax_visible.set_ylabel('Visible', color='tab:green')
    ax_visible.tick_params(axis='y', labelcolor='tab:green')

    ax_ir = ax_visible.twinx()
    ir_columns = resolve_sensor_plot_columns(df, 'ir')
    for series_name, label in zip(ir_columns['series'], ir_columns['labels']):
        ax_ir.plot(
            df['timestamp'],
            df[series_name],
            label=label,
            color='tab:red',
        )
    ax_ir.set_ylabel('IR', color='tab:red')
    ax_ir.tick_params(axis='y', labelcolor='tab:red')

    visible_lines, visible_labels = ax_visible.get_legend_handles_labels()
    ir_lines, ir_labels = ax_ir.get_legend_handles_labels()
    ax_visible.legend(
        visible_lines + ir_lines,
        visible_labels + ir_labels,
        loc='lower right',
    )

    fig.suptitle(f'Light Set Value vs Sensor Data — {os.path.basename(filename)}')
    plt.tight_layout()
    save_path = build_chart_output_path(filename)
    plt.savefig(save_path)
    plt.show()


if __name__ == '__main__':
    main()

