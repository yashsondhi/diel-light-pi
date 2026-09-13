import csv
import fcntl
import os
import time

# creates a script to save pi running time for each trial
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', 'logs'))
os.makedirs(LOG_DIR, exist_ok=True)
path = LOG_DIR + os.sep

lock_file = open(os.path.join(LOG_DIR, "save_run_time.lock"), "w")
try:
    fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
except BlockingIOError:
    lock_file.close()
    raise SystemExit("Runtime logger is already running")

frequency = 60

filename = "log_pi_time.txt"
log_pi_time_file = open(path + filename, 'a+')  # create a new file
localtime = time.asctime(time.localtime(time.time()))
line_header = ["Pi_on_time", localtime]

# write header file
with log_pi_time_file:
    writer = csv.writer(log_pi_time_file)
    writer.writerow(line_header)

# Record system time every x second
while True:
    localtime = time.asctime(time.localtime(time.time()))
    appendFile = open(path + filename, 'a+')
    with appendFile:
        writer = csv.writer(appendFile)
        line_content = ["Pi_run_time", localtime]
        writer.writerow(line_content)
    time.sleep(frequency)
