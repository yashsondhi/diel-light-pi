---
title: Repository Usage
last_modified_date: 2026-08-12 02:38:05 +0000
nav_order: 5
---
# Using the Repository
There are two sections to the repository, the activity monitoring scripts and the light emulation scripts. \

Here are some common commands and shortcuts (in caps):

Command     | Description
------------|---------------
cd ___      | Enters a folder
cd ..       | Go up one folder level
ls          | See everything in the current folder
python ___  | Run a python script 
CTRL + C    | Cancel a running command
TAB         | Autocomplete 

Ex: if you're in the home folder, typing cd folder brings you to home/folder. Typing cd .. brings you back to the home folder.

## Activity Monitoring
1. Go to the terminal and traverse into the diel-light-pi folder. The beginning of the terminal should say 
    ```bash
    username@hostname:~ $
    ```
    where username is the username you set for the account, and hostname is the name you set for the Raspberry Pi. 
    <figure>
        <img src="{{ site.baseurl }}/assets/usage/Initial_Terminal.png" 
            alt="Image of Arducam OV5647 package">
        <figcaption>
            A fresh terminal window on a Raspberry Pi with the "pi01" username and "raspberrypi" hostname.
        </figcaption>
    </figure>
    
    If the beginning of the terminal doesn't say that, close the terminal window and open another one. 
    
2. Go to the activity-monitoring folder in the diel-light-pi folder.
    ```bash
    cd diel-light-pi/activity-monitoring/
    ```
    <figure>
        <img src="{{ site.baseurl }}/assets/usage/Enter_AM_Folder.png" 
            alt="Image of Arducam OV5647 package">
        <figcaption>
            Type this command to enter the activity monitoring folder in the diel-light-pi repository.
        </figcaption>
    </figure>

3. Now the text before the cursor should be
    ```bash
    username@hostname:~/diel-light-pi/activity-monitoring $
    ```

4. To run the diel-light-pi program, type
    ```bash
    python gui_diel-light.py 
    ```
    <figure>
        <img src="{{ site.baseurl }}/assets/usage/GUI.png" 
            alt="Image of Arducam OV5647 package">
        <figcaption>
            The GUI of the activity monitoring program.
        </figcaption>
    </figure>

5. Select "Choose motion file" and pick the motion file that you want to use. "motion_best.conf" saves the image in a motion event with the most movement. "motion.conf" saves an image for every frame of movement.
    <figure>
        <img src="{{ site.baseurl }}/assets/usage/Motion_Conf.png" 
            alt="Image of Arducam OV5647 package">
        <figcaption>
            The configuration files for the activity monitoring system.
        </figcaption>
    </figure>

6. Change the filled in boxes to match your experiment. For the output folder name, create a descriptive name so that you can easily find where the photos are stored. For the trial name, enter a descriptive name for your trial (constants and changes). To manually enter a trial number, uncheck the "Auto trial numbering" checkbox.
    <figure>
        <img src="{{ site.baseurl }}/assets/usage/Filled_GUI.png" 
            alt="Image of Arducam OV5647 package">
        <figcaption>
            An example of experiment details.
        </figcaption>
    </figure>

7.  Keep interactive mode and auto start on. Click "Save project".
    <figure>
        <img src="{{ site.baseurl }}/assets/usage/Save_Project.png" 
            alt="Image of Arducam OV5647 package">
        <figcaption>
            Click this to save the project details.
        </figcaption>
    </figure>

8. Enter your preferred project configuration file name and press "Save".
    <figure>
        <img src="{{ site.baseurl }}/assets/usage/Proj_Conf.png" 
            alt="Image of Arducam OV5647 package">
        <figcaption>
            Enter your project configuration file name here.
        </figcaption>
    </figure>

8. Click "Run Experiment" to start gathering photos. 
    <figure>
        <img src="{{ site.baseurl }}/assets/usage/Run.png" 
            alt="Image of Arducam OV5647 package">
        <figcaption>
            Click this button to start taking images.
        </figcaption>
    </figure>

9.  To turn off the motion capture, in the terminal that pops up, type CTRL+C. To close the main terminal, close the diel-light-pi config application (grey box that popped up when you entered "--run" or type CTRL+C. The saved images should be in "/home/pi/diel-light-pi/activity-monitoring/<YOUR_FOLDER_NAME>/<TRIAL_NUMBER>", where <YOUR_FOLDER_NAME> is the output folder name you specified and <TRIAL_NUMBER> is the trial number.

### Editing config files
Currently, the motion imaging system is set to save a photo within a "motion" with the greatest difference in pixels. A single motion has a maximum length of one minute, where there is continuous movement in the frame at all times. 

If you want to configure the file, please look at the [documentation](https://motion-project.github.io/motion_config.html#OptTopic_Motion_Detection) and look into the Motion Detection General Info variables. After doing this, make sure to make a copy of the motion.conf file and rename it to a preferred name. 

To update this to your project, double click the "Open Motion File" and double click "<YOUR_NAME>.conf", where <YOUR_NAME> is the configuration file name that you just entered. 
