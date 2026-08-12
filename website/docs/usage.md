---
title: Using the Repository
last_modified_date: 2026-08-12 02:17:26 +0000
nav_order: 5
---
# **Motion** and **diel-light-pi** repository usage
---
### Ensure that the terminal is in the diel-light-pi folder
Go back to the terminal and make sure that you're in the "diel-light-pi" folder. The command line should say something like
```bash
pi@raspberrypi:~/diel-light-pi/
```
If not, type
```bash
cd ..
```
until the text before the cursor is
```bash 
pi@raspberrypi:/
```
Then type 
```bash
cd home
cd pi
cd diel-light-pi
ls
```
If nothing shows up underneath the command, try to redownload the library.
---
### Run diel-light-pi program
To run the diel-light-pi program, type
```bash
python gui_diel-light.py --run
```
1. In the box that pops up, click "Open Config File", double click configs, and then double click "project.conf".

2. Click "Open Motion File" and double click "motion_best.conf".

3. Change the filled in boxes to match your experiment. For the output folder name, create a descriptive name so that you can easily find where the photos are stored. For the trial name, enter a descriptive name for your trial (constants and changes). You can leave the trial number blank if doing multiple trials and the script will automatically count up for you. Or, you can manually enter a trial number. 

4. Keep interactive mode and auto start on. Click "Save Config File" and then click "Run Experiment" to start gathering photos. 

5. To turn off the motion capture, in the terminal that pops up, type CTRL+C. To close the main terminal, close the diel-light-pi config application (grey box that popped up when you entered "--run" or type CTRL+C. The saved images should be in "/home/pi/diel-light-pi/<YOUR_FOLDER_NAME>/<TRIAL_NUMBER>", where <YOUR_FOLDER_NAME> is the output folder name you specified and <TRIAL_NUMBER> is the trial number.

### Editing config files
Currently, the motion imaging system is set to save a photo within a "motion" with the greatest difference in pixels. A single motion has a maximum length of one minute, where there is continuous movement in the frame at all times. 

If you want to configure the file, please look at the [documentation](https://motion-project.github.io/motion_config.html#OptTopic_Motion_Detection) and look into the Motion Detection General Info variables. After doing this, make sure to make a copy of the motion.conf file and rename it to a preferred name. 

To update this to your project, double click the "Open Motion File" and double click "<YOUR_NAME>.conf", where <YOUR_NAME> is the configuration file name that you just entered. 
