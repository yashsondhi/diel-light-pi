"""
Data Visualization Tool for Motion Data

Author: Pavan Kumar Kaushik
Twitter: @pvnkmrksk
Email: pkaushik@ab.mpg.de

License: MIT License

Description: This tool provides a Command Line Interface (CLI) for visualizing motion data from a CSV file.
"""

import pandas as pd
import seaborn as sns
from clize import run  # for rapid CLI development
import matplotlib.pyplot as plt


def visualize_data(
    filename: str,
    freq: str = "10Min",
    offsetTime: str = "00:00:00",
) -> None:
    """
    Visualizes motion data from a CSV file.

    Parameters:
    - filename (str): Path to the input CSV file.
    - freq (str): Frequency for grouping timestamps. Default is '10Min'.
    - offsetTime (str): Time offset to be added to timestamps. Default is '00:00:00'.
    # - xtick_labels (list): List of labels for xticks. Default is ["Midnight", "Noon", "Midnight"].
    - show_plot (bool): Whether to display the plot or not. Default is True.

    Returns:
    - None
    """

    # Reading the CSV file and preprocessing the timestamp data
    df = pd.read_csv(
        filename, index_col=0, parse_dates=["timestamp"], infer_datetime_format=True
    )

    # Convert motion intervals to seconds for easier aggregation
    df["motion_int"] = pd.to_timedelta(df["motion_int"]).dt.total_seconds()

    # Apply the time offset to timestamps
    df["timestamp"] = df["timestamp"] + pd.to_timedelta(offsetTime)

    # Extract date from timestamp for grouping purposes
    df["date"] = df["timestamp"].dt.date

    # Group by date and the specified frequency, then sum motion intervals
    df = (
        df.groupby(["date", pd.Grouper(key="timestamp", freq=freq)])["motion_int"]
        .sum()
        .reset_index()
    )

    # Reindex dataframe to ensure all time intervals are represented (filling gaps with zeros)
    df = (
        df.set_index("timestamp")
        .reindex(
            pd.date_range(
                df["timestamp"].min().date(), df["timestamp"].max(), freq=freq
            ),
            fill_value=0,
        )
        .reset_index()
    )

    # Extract date information after reindexing
    df["date"] = df["index"].dt.date

    # Rename columns for clarity
    df.columns = ["timestamp", "date", "motion_int"]

    # Convert timestamp back to time format for plotting
    df["timestamp"] = df["timestamp"].dt.time

    # Assign sequential numbers to each unique date for plotting purposes
    df["day_number"] = df["date"].astype("category").cat.codes + 1

    xtick_labels = ["Midnight", "Noon", "Midnight"]

    # Calculate xtick positions dynamically based on frequency for robustness
    total_ticks = 24 * 60 // int(freq.replace("Min", ""))
    xtick_positions = [0, total_ticks // 2, total_ticks - 1]

    # Visualize the data using seaborn
    g = sns.catplot(
        x="timestamp",
        y="motion_int",
        row="day_number",
        kind="bar",
        data=df,
        height=1,
        aspect=8,
    )
    g.set(xticks=xtick_positions, xticklabels=xtick_labels)
    g.set(yticks=[])
    g.set_titles("")
    g.set_ylabels(label="Day", fontsize=12)
    g.set_axis_labels("", "Day")
    # Set y-labels for each subplot
    for ax, day_number in zip(g.axes.flat, df["day_number"].unique()):
        ax.set_ylabel(day_number)

    sns.despine(trim=True, left=True)
    plt.tight_layout()
    # Save the plots as SVG and PNG
    g.savefig(f"{filename}_plot.svg")
    g.savefig(f"{filename}_plot.png")
    # Export the processed data to CSV with a suffix
    df.to_csv(f"{filename}_processed.csv", index=False)

    print("Data visualization complete!")
    print(f"Processed data saved to {filename}_processed.csv")
    # plt.show()


if __name__ == "__main__":
    run(visualize_data)
