---
title: Software Setup
parent: Raspberry Pi Setup
last_modified_date: 2026-08-12 02:38:05 +0000
nav_order: 2
---
# Installing Raspberry Pi Operating System
## Parts List
- a desktop environment
- a micro SD card
    <figure>
        <img src="{{ site.baseurl }}/assets/software/" 
            alt="Image of a micro SD card">
        <figcaption>
            Heatsinks attached to the Arducam IR light pads.
        </figcaption>
    </figure>

- a micro SD to usb adapter
    <figure>
        <img src="{{ site.baseurl }}/assets/software/" 
            alt="Image of ">
        <figcaption>
            Heatsinks attached to the Arducam IR light pads.
        </figcaption>
    </figure>

### Download the Imager

1. Go to [Raspberry Pi Imager Download](https://www.raspberrypi.com/software/) and download the suggested version. 

2. Install the downloaded software (follow the instructions and say yes/accept agreement) and press next for each step. You can choose to make a desktop shortcut, but it isn't necessary. It just creates an icon on your homescreen.
    <figure>
        <img src="{{ site.baseurl }}/assets/software/Accept_Installer_Agreement.png" 
            alt="Image of the License Agreement page on the Raspberry Pi installer with the I Accept the Agreement checkbox checked">
        <figcaption>
            Click "I accept the agreement" to continue the installation.
        </figcaption>
    </figure>

3. After installing check the "Launch Raspberry Pi Imager" box after installing and press finish. 
    <figure>
        <img src="{{ site.baseurl }}/assets/software/Raspberry_Pi_Installer_Checkbox.png" 
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
        <img src="{{ site.baseurl }}/assets/software/Select_Raspberry_Pi_5.png" 
            alt="Image of a red box around Raspberry Pi 5">
        <figcaption>
            Select the option at the top of the menu.
        </figcaption>
    </figure>

2. Scroll down and click on "Raspberry Pi OS (other)"
    <figure>
        <img src="{{ site.baseurl }}/assets/software/Select_Other_OS.png" 
            alt="Image of a red box around Raspberry Pi OS (other)">
        <figcaption>
            Scroll down to find this option.
        </figcaption>
    </figure>
    
3. Scroll down and click on Raspberry Pi OS (Legacy, 64-bit) with a description that says "A port of Debian Bookworm..." and press next.
    <figure>
        <img src="{{ site.baseurl }}/assets/software/Select_Debian_x64.png" 
            alt="Image of a red box around Debian Bookworm 64-bit version">
        <figcaption>
            You might have to scroll a little to find this.
        </figcaption>
    </figure>

4. Make sure your SD card is inserted, click on it, and press next. It's okay if it has a little less storage than the stated amount on the micro SD card.
    <figure>
        <img src="{{ site.baseurl }}/assets/software/Select_Storage_Drive.png" 
            alt="Image of a red box around a removable storage drive">
        <figcaption>
            Make sure to select the correct SD card. It can help to rename the micro SD card in your preferred file system.
        </figcaption>
    </figure>

5. Enter the preferred name for the Raspberry Pi. 
    <figure>
        <img src="{{ site.baseurl }}/assets/software/Choose_Hostname.png" 
            alt="Image of a red box around a removable storage drive">
        <figcaption>
            Make sure to select the correct SD card. It can help to rename the micro SD card in your preferred file system.
        </figcaption>
    </figure>
    
6. Choose your country's capital city and your timezone, and ensure the keyboard layout is "us".
    <figure>
        <img src="{{ site.baseurl }}/assets/software/Customize_Location.png" 
            alt="Image of a red box around a removable storage drive">
        <figcaption>
            Make sure to select the correct SD card. It can help to rename the micro SD card in your preferred file system.
        </figcaption>
    </figure>
    
7. Enter a username and password if needed. 
    <figure>
        <img src="{{ site.baseurl }}/assets/software/Choose_Login.png" 
            alt="Image of a red box around a removable storage drive">
        <figcaption>
            Make sure to select the correct SD card. It can help to rename the micro SD card in your preferred file system.
        </figcaption>
    </figure>
    
8. Press next on the WiFi screen, and enable SSH if you want to remote access the Raspberry Pi. Leave the checkbox on "Use Password Authentication". 
    <figure class="image-row">
        <div>
            <img src="#" 
                alt="Image of Raspberry Pi 5 package">
            <figcaption>
                An unopened Raspberry Pi 5 package.
            </figcaption>
        </div>
        <div>
            <img src="#" 
                alt="Image of Rasbperry Pi 5 Board">
            <figcaption>
                The Raspberry Pi 5 computer.
            </figcaption>
        </div>
    </figure>
    
9.  
    <figure class="image-row">
        <div>
            <img src="#" 
                alt="Image of Raspberry Pi 5 package">
            <figcaption>
                An unopened Raspberry Pi 5 package.
            </figcaption>
        </div>
        <div>
            <img src="#" 
                alt="Image of Rasbperry Pi 5 Board">
            <figcaption>
                The Raspberry Pi 5 computer.
            </figcaption>
        </div>
    </figure>
    
10. Wait for the download to finish, and press Finish.
    <figure>
        <img src="{{ site.baseurl }}/assets/software/" 
            alt="Image of a red box around a removable storage drive">
        <figcaption>
            Make sure to select the correct SD card. It can help to rename the micro SD card in your preferred file system.
        </figcaption>
    </figure>
    
11. Take out the SD card.
    <figure>
        <img src="{{ site.baseurl }}/assets/software/" 
            alt="Image of a red box around a removable storage drive">
        <figcaption>
            If you can't pull out the micro SD card, you need to push it in and release. The micro SD card will then pop out for you to grab. Otherwise, just pull it out. 
        </figcaption>
    </figure>
    
---
## Setting Up the Raspberry Pi Imaging System

**BEFORE YOU DO ANYTHING WITH THE CAMERA WIRING, MAKE SURE THE RASPBERRY PI IS TURNED OFF AND UNPLUGGED**

1. Put the SD card into the SD card reader of the Raspberry Pi (with the Pi logo facing toward you, you should see the black side of the SD card).

2. Plug the HDMI and power cable into the Pi. 

3. After plugging the Pi in, it should automatically turn on. 

4. Change the country to United States, langauge to American English, and timezone to Eastern. Check the "Use English language" and "Use US keyboard" boxes and press next.

5. If not already created, create a user for the Pi, and enter your preferred username and password. If working in a lab, consult your PI. And press OK if there is a popup. 

6. Skip the WiFi network selection and software update, and press restart.

7. After the Pi boots up again, in the top right click on the wifi symbol (The two red x's with grey lines coming vertically from them) and click on your desired wifi connection.

8. For univeristy networks that require a username and password, 
   1. change the Authentication to "Protected EAP (PEAP)"
   2. check the "No CA certificate is required" box
   3. enter your username and password  
   4. press enter
    - To confirm: a grey box should pop up in the top right saying that you've connected to (insert WiFi name). If not, repeat this step and ensure that you've entered your credentials correctly.

---
Continue to the [software installation page](https://github.com/yashsondhi/diel-light-pi/wiki/Software-installation-(includes-motion)) to continue setting up diel-light-pi.

