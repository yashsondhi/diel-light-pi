import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

if len(sys.argv) < 2:
    csvs = [f for f in os.listdir('data') if f.endswith('.csv')]
    if not csvs:
        sys.exit("No CSV files found in data/")
    filename = os.path.join('data', max(csvs, key=lambda f: os.path.getmtime(os.path.join('data', f))))
    print(f"Using most recent log: {filename}")
else:
    filename = sys.argv[1]

df = pd.read_csv(filename)
df['timestamp'] = pd.to_datetime(df['timestamp'])

has_set_val = 'set_val' in df.columns
if not has_set_val:
    print("Warning: no 'set_val' column found, skipping set value plot")

fig, ax1 = plt.subplots(figsize=(12, 5))

ax1.set_xlabel('Time')
ax1.set_ylabel('Lux', color='tab:blue')
ax1.plot(df['timestamp'], df['top_lux'], label='Top Lux', color='tab:blue')
ax1.plot(df['timestamp'], df['bottom_lux'], label='Bottom Lux', color='tab:cyan')
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

plt.title(f'Light Set Value vs Sensor Lux — {os.path.basename(filename)}')
plt.tight_layout()
plt.savefig(filename.replace('.csv', '.png'))
plt.show()
