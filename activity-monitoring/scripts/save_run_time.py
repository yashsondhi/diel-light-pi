import csv
import time
import os

# creates a script to save pi running time for each trial
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', 'logs'))
os.makedirs(LOG_DIR, exist_ok=True)
path = LOG_DIR + os.sep

frequency = 60

filename = "log_pi_time.txt"
log_pi_time_file = open(path + filename, 'a+')  # create a new file
localtime = time.asctime(time.localtime(time.time()))  # Saves local time in a specific format
line_header = ["Pi_on_time", localtime]

# write header file
with log_pi_time_file:
    writer = csv.writer(log_pi_time_file)
    writer.writerow(line_header)

# Record system time every x second
while True:
    # Saves local time in file
    appendFile = open(path + filename, 'a+')
    with appendFile:
        writer = csv.writer(appendFile)
        line_content = ["Pi_run_time", localtime]
        writer.writerow(line_content)
