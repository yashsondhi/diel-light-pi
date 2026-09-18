---
title: Setting Up VNC 
parent: Booting Up
last_modified_date:
nav_order: 1
---
# Setting Up VNC on Raspberry Pi
If you need to change your screen size, go to [Changing the Raspberry Pi Screen Size][change screen size]. 

This method only works if the Raspberry Pi and your computer are on the same WiFi network. If you would like an easy way to access your Raspberry Pi from different networks, follow the [guide from Raspberry Pi][pi connect guide].

1. Open the Terminal by clicking the icon.
    <figure>
        <div>
            <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/boot/raspberry_pi/vnc/Select_Terminal_Icon.png" 
                alt="Image of a red box around the Raspberry Pi Terminal Icon">
            <figcaption>
                Click on this to open the terminal.
            </figcaption>
        </div>
    </figure>

2. Enter ```sudo raspi-config``` into the terminal and press ENTER. This opens the Configurations page of the Raspberry Pi.
    <figure>
        <div>
            <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/boot/raspberry_pi/vnc/raspi-config_Command.png" 
                alt="Image of a red box around 'sudo raspi-config'">
            <figcaption>
                Enter this command to open the configurations of the Raspberry Pi.
            </figcaption>
        </div>
    </figure>

3. Use your arrow keys to navigate to "Interface Options", and press ENTER.

    You can only use the keyboard to navigate in the terminal. 
    {: .important}
    <figure>
        <div>
            <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/boot/raspberry_pi/vnc/Select_Interface_Options.png" 
                alt="Image of a red box around the interface options in the raspberry config">
            <figcaption>
                Select this to view the interface settings.
            </figcaption>
        </div>
    </figure>

4. Select "VNC". 
    <figure class="image-row">
        <div>
            <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/boot/raspberry_pi/vnc/Select_VNC.png" 
                alt="Image of a red box around the VNC option in the raspberry config">
            <figcaption>
                Select this to Enable/Disable VNC.
            </figcaption>
        </div>
    </figure>

5. Select "Yes" to enable VNC. It should say "The VNC Server is enabled". Press ENTER to return to the configuration screen.
    <figure class="image-row">
        <div>
            <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/boot/raspberry_pi/vnc/Enable_VNC.png" 
                alt="Image of a red box around the yes to enable VNC">
            <figcaption>
                Select this to enable VNC
            </figcaption>
        </div>
        <div>
            <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/boot/raspberry_pi/vnc/VNC_Enabled.png" 
                alt="Image of a red box around the interface options in the raspberry config">
            <figcaption>
                This confirms that VNC is enabled.
            </figcaption>
        </div>
    </figure>

6. Now you will need to get the IP address of your Pi. Press ESC to leave the configurations page and enter ```hostname -I```.
    <figure>
        <div>
            <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/boot/raspberry_pi/vnc/hostname.png" 
                alt="Image of a red box around the interface options in the raspberry config">
            <figcaption>
                Enter this command to get the IP address of your Raspberry Pi. 
            </figcaption>
        </div>
    </figure>

7. An IP address should pop up underneath the command with the form xxx.xx.xxx.xx or xxx.xx.xx.xx. Write this down somewhere.
   
    This IP changes for every WiFi network that you join. For example, this IP address only applies to the university internet. If you want to do this at home, you have to get the Raspberry Pi's IP address on that network. 
    {: .warning}

Follow [this][change screen size] guide to change the size of your icons.

Return to the bootup guide [here][boot].

[change screen size]: ../change_screen_size
[pi connect guide]: https://www.raspberrypi.com/software/connect/
[boot]: ../../boot/#setting-up-the-raspberry-pi
