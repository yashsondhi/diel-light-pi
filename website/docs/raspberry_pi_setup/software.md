---
title: Software Setup
parent: Raspberry Pi Setup
last_modified_date: 2026-09-01 14:56:20 +0000
nav_order: 2
---
# Installing Raspberry Pi Operating System
## Parts List
- a desktop environment
- a micro SD card
    <figure>
        <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/software/MicroSD.png" 
            alt="Image of a micro SD card">
        <figcaption>
            The front and back side of a micro SD card.
        </figcaption>
    </figure>

- a micro SD to usb adapter
    <figure>
        <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/software/MicroSD-USB_Adapter.png" 
            alt="Image of a micro SD to usb adapter">
        <figcaption>
            This allows you to access the SD card through USB.
        </figcaption>
    </figure>

Optional:
- a micro SD to SD adapter
    <figure>
        <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/software/MicroSD-SD_Adapter.png" 
            alt="Image of a micro SD adapter without the micro SD card">
        <figcaption>
            A micro SD adapter without the micro SD card.
        </figcaption>
    </figure>

### Download the Imager

1. Go to [Raspberry Pi Imager Download](https://www.raspberrypi.com/software/) and download the suggested version. 

2. Install the downloaded software (follow the instructions and say yes/accept agreement) and press next for each step. You can choose to make a desktop shortcut, but it isn't necessary. It just creates an icon on your homescreen.
    <figure>
        <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/software/Accept_Installer_Agreement.png" 
            alt="Image of the License Agreement page on the Raspberry Pi installer with the I Accept the Agreement checkbox checked">
        <figcaption>
            Click "I accept the agreement" to continue the installation.
        </figcaption>
    </figure>

3. After installing check the "Launch Raspberry Pi Imager" box after installing and press finish. 
    <figure>
        <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/software/Raspberry_Pi_Installer_Checkbox.png" 
            alt="Image of the completion screen of the Raspberry Pi Imager with the Launch Raspberry Pi Imager checkbox checked">
        <figcaption>
            Make sure to launch the Raspberry Pi imager after installation.
        </figcaption>
    </figure>

### Setting Up Download in Imager
Make sure the Raspberry Pi is turned off when plugging in and out the micro SD card. Taking out the SD card while the Raspberry Pi is still on could corrupt the SD card and damage the system.
{: .warning}

1. Double click Raspberry Pi 5.
    <figure>
        <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/software/Select_Raspberry_Pi_5.png" 
            alt="Image of a red box around Raspberry Pi 5">
        <figcaption>
            Select the option at the top of the menu.
        </figcaption>
    </figure>

2. Scroll down and click on "Raspberry Pi OS (other)"
    <figure>
        <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/software/Select_Other_OS.png" 
            alt="Image of a red box around Raspberry Pi OS (other)">
        <figcaption>
            Scroll down to find this option.
        </figcaption>
    </figure>
    
3. Scroll down and click on Raspberry Pi OS (Legacy, 64-bit) with a description that says "A port of Debian Bookworm..." and press next.
    <figure>
        <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/software/Select_Debian_x64.png" 
            alt="Image of a red box around Debian Bookworm 64-bit version">
        <figcaption>
            You might have to scroll a little to find this.
        </figcaption>
    </figure>

4. Make sure your SD card is inserted, click on it, and press next. It's okay if it has a little less storage than the stated amount on the micro SD card.
    <figure>
        <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/software/Select_Storage_Drive.png" 
            alt="Image of a red box around a removable storage drive">
        <figcaption>
            Make sure to select the correct SD card. It can help to rename the micro SD card in your preferred file system.
        </figcaption>
    </figure>

5. Enter the preferred name for the Raspberry Pi. You can only enter letters, numbers, and hyphens.
    <figure>
        <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/software/Choose_Hostname.png" 
            alt="Image of a red box around a removable storage drive">
        <figcaption>
            Make sure to select the correct SD card. It can help to rename the micro SD card in your preferred file system.
        </figcaption>
    </figure>
    
6. Choose your country's capital city and your timezone, and ensure the keyboard layout is "us".
    <figure>
        <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/software/Customize_Location.png" 
            alt="Image of a red box around a removable storage drive">
        <figcaption>
            Make sure to select the correct SD card. It can help to rename the micro SD card in your preferred file system.
        </figcaption>
    </figure>
    
7. Enter a username and password if needed. The username must be lowercase and contain only letters, numbers, underscores, and hyphens.
    <figure>
        <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/software/Choose_Login.png" 
            alt="Image of a red box around a removable storage drive">
        <figcaption>
            Make sure to select the correct SD card. It can help to rename the micro SD card in your preferred file system.
        </figcaption>
    </figure>
    
8. Press next on the WiFi screen, make sure SSH is disabled. If you want to enable remote access or just want to learn more, click [here][SSH Page].
    <figure>
        <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/software/SSH_Option.png" 
            alt="Image of Raspberry Pi 5 package">
        <figcaption>
            An unopened Raspberry Pi 5 package.
        </figcaption>
    </figure>
    
9.  Press "WRITE", and make sure that all the data that you want to save from the drive is saved elsewhere. This will delete everything on the SD card.
    <figure>
        <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/software/Write_OS.png" 
            alt="Image of a red box around the write button">
        <figcaption>
            Press this to start the installation process.
        </figcaption>
    </figure>

10. After moving your files off the drive, press "I UNDERSTAND, ERASE AND WRITE"
    <figure>
        <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/software/Wipe_Drive.png" 
            alt="Image of a red box around the I understand, erase and write button">
        <figcaption>
            Press this to allow the installation to continue.
        </figcaption>
    </figure>
    
11. Wait for the download to finish. When the button on the bottom right says "FINISH", press it and unplug the SD card.
    <figure>
        <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/software/Finish.png" 
            alt="Image of a red box around the finish button">
        <figcaption>
            You've now installed the Raspberry Pi operating system onto your micro SD card.
        </figcaption>
    </figure>
     
---

Continue to the [Booting Up][Boot] page to continue setting up the pLAM.

[SSH Page]: ../../ssh/ 
[Boot]: ../boot/ 
