
# Portable Locomotion Activity monitor (pLAM)
Creates activity detector images for the Rasberry pi to monitor diel activity of small objects
# Setup
1. Clone the git repository to your rasberry pi using git clone or download the files.  Navigate to the folder diel-light-pi
2. Install YAML dependencies for python (pip install PyYAML or sudo apt install python3-yaml)k
3. Run `python run_diel-light.py --time` to update time if required.  
4. Run `python run_diel-light.py --setup` to display output parameters for project.   
5. If the project parameters require updating. Modify the `configs/project.conf`  
6. Run `python run_diel-light.py --run`
(Older versions of raspberry pi OS , may explicity need to call python3)

# Run the GUI to modify the config files
1. Open a terminal 
2. Navigate to diel-light-py
3. Run 'python gui_diel-light.py' to open the interface that sets up the experiment
4. Load an example config file from configs/project.conf
5. Modify the parameters and save
6. Run the experiment


# Modify config files 
Project config files : configs/project.conf
Motion tracking config files : configs/motion.conf  
For a more detailed guide on modifying motion tracking parameters, refer to https://motion-project.github.io/

#Analysis
To analyse data modify config/analysis.conf to match the input path of the folder you want to analyse log files
Ensure you are in the folder scripts/
1. Extract data run python3.5 analysis_pipeline.py --conf "path_to_analysis.conf" --extract
2. Plot data quickly python3.5 analysis_pipeline.py --conf "path_to_analysis.conf" --plot_test
3. Plot complete data (slow) python3.5 analysis_pipeline --conf "path_to_analysis.conf" --plot_all


# Other scripts
Bootable scripts
1. Control Neopixel LED light strips. Script: smooth_light_control.py
2. Custom temperature and humidity readings and control. Incubator_control.py
3. Save Light readings from TSL2691 light sensor: save_light_data.py
4. Save time every minute to the pi : save_run_time.py
5. Send IP address on boot : boot_email.py

### Light controller configuration
The light controller reads its cycle settings from
`light-emulation/light_config.txt` by default. Use `--config path/to/file.txt`
to select another file. Strip count, sensor use, logging, and measurement
interval are selected through terminal prompts. Lights continue updating every
0.5 seconds regardless of the measurement interval.

For more detail, use a 2-second measurement interval. For a week-long trial,
8 seconds is a reasonable compromise that greatly reduces CSV size.

## Auto booting Instructions: 
Load these commands in /etc/rc.local to boot from startup : python PATH_TO:smooth_light_control.py
 
For `boot_email.py` and activity-monitoring auto start, add the commands from
`examples/crontab_files.txt` to the Raspberry Pi user's crontab with `crontab -e`.
Update `/home/pi/diel-light-pi` in those commands if the repository is elsewhere.
The activity-monitoring command includes `--silent` because cron has no terminal
to answer the interactive confirmation prompt. It starts only when
`AUTOSTART: true` is set in `project-configs/project.conf`.

## Citation: 
Sondhi, Y., Jo, N. J., Alpizar, B., Markee, A., Dansby, H. E., Currea, J. P., Fabian, S. T., Ruiz, C., Barredo, E., Allen, P., DeGennaro, M., Kawahara, A. Y. & Theobald, J. C. (2022). Portable locomotion activity monitor (pLAM): A cost-effective setup for robust activity tracking in small animals. Methods in Ecology and Evolution, 13, 805–812. https://doi.org/10.1111/2041-210X.13809

