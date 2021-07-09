
# Diel-light activity detector
Creates activity detector images for the Rasberry pi to monitor diel activity of small objects
# Setup
1. Clone the git repository to your rasberry pi using git clone or download the files.  
2. Run `python3 run_diel-light.py --time` to update time if required.  
3. Run `python3 run_diel-light.py --setup` to display output parameters for project.   
4. If the project parameters require updating. Modify the `configs/project.conf`  
5. Run `python3 run_diel-light.py --run --autorun --out output_dir_path`

# Modify config files 
Project config files : configs/project.conf.  
Motion tracking config files : configs/motion.conf  
For a more detailed guide on modifying motion tracking parameters, refer to https://motion-project.github.io/

# Other scripts
Bootable scripts
1. Control Neopixel LED light strips. Sript: smooth_light_control.py
2. Custom temperature and humidity readings and control. Incubator_control.py
3. Save Light readings from TSL2691 light sensor: save_light_data.py
4. Save time every minute to the pi : save_run_time.py
5. Send IP address on boot : boot_email.py

## Instructions: 
Load these files in /etc/rc.local to boot from startup
For boot_email.py and auto start put the commands in example/crontab_files.files.txt in your own cronfile.
Use crontab -e and add the lines of code, taking care to use the directory where your files are loaded. 
If you have not installed diel-light-pi in the home directory, then change the cd command in @reboot sleep 60 && cd diel-light-pi && python3 run_diel-light_2.py --run


