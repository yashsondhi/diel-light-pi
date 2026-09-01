---
title: Booting Up 
parent: Raspberry Pi Setup
last_modified_date: 2026-09-01 14:56:20 +0000
nav_order: 3
---
# Booting Up the Raspberry Pi 5
## Parts List
- An Arducam and Raspberry Pi completely assembled
- The micro SD card with the installed Raspberry Pi OS 
- Raspberry Pi USB C charger
- Micro HDMI to HDMI cable (or micro HDMI to HDMI adapter and then HDMI to HDMI cable) 

## Plugging in the Hardware
Before doing changing anything physical (hardware) with the Raspberry Pi, make sure it is turned **OFF**. Also, be careful when handling the orange ribbon cable.
{: .warning}

1. Put the micro SD card into the micro SD card reader of the Raspberry Pi, on the bottom side of the Pi. 
    <figure class="image-row">
        <div>
            <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/boot/RPi_MicroSD.png" 
                alt="Image of the micro SD slot on the Raspberry Pi">
            <figcaption>
                The micro SD slot on a Raspberry Pi. The Raspberry Pi runs off the micro SD card that is inserted here.
            </figcaption>
        </div>
        <div>
            <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/boot/MicroSD_Inserted.png" 
                alt="Image of the micro SD card inserted in the Raspberry Pi">
            <figcaption>
                A micro SD card correctly and fully inserted into the Raspberry Pi.
            </figcaption>
        </div>
    </figure>

2. Plug in the USB keyboard and mouse into any of the USB ports.
    <figure class="image-row">
        <div>
            <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/boot/USB_Ports.png" 
                alt="Image of a red box around the USB ports on a Raspberry Pi 5">
            <figcaption>
                Plug in any USB devices here.
            </figcaption>
        </div>
        <div>
            <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/boot/USB_Port_with_Dongle.png" 
                alt="Image of two usb devices plugged into the Raspberry Pi 5">
            <figcaption>
                A USB keyboard and mouse pair plugged into the Raspberry Pi.
            </figcaption>
        </div>
    </figure>

3. Plug the USB C power cable into the bottom left port of the Raspberry Pi (left red box), and the micro HDMI cable into the middle metal connector (right red box). 
    <figure class="image-row">
        <div>
            <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/boot/USBC_MicroHDMI_Connectors.png" 
                alt="Image of a red box around the USBC and micro HDMI connectors on the Raspbery Pi">
            <figcaption>
                TThe Raspberry Pi gets its power from the USB C port. The Raspbery Pi outputs a display through the micro HDMI port. 
            </figcaption>
        </div>
        <div>
            <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/boot/Plugged.png" 
                alt="Image of a USB C and micro HDMI cable plugged into the Raspberry Pi">
            <figcaption>
                The power and display cables properly plugged in.
            </figcaption>
        </div>
    </figure>
    
4. After plugging the Pi in, the LED should first be red briefly, and then turn to green. It is okay if the green light flickers.  
    <figure>
        <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/boot/LED_On.png" 
            alt="Image of the LED indicator on the Raspberry Pi as Green">
        <figcaption>
            A green light here means that the Raspberry Pi succesfully turned on.
        </figcaption>
    </figure>
    
5. Change the country to United States, langauge to American English, and timezone to Eastern. Check the "Use English language" and "Use US keyboard" boxes and press next.
    <figure>
        <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/boot/Final_Assembly.png" 
            alt="Image of Raspberry Pi and Arducam connected by orange ribbon cable">
        <figcaption>
            Completed setup of an Arducam connected to a Raspberry Pi 5.
        </figcaption>
    </figure>
    
6. If not already created, create a user for the Pi, and enter your preferred username and password. If working in a lab, consult your PI. And press OK if there is a popup. 
    <figure>
        <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/boot/Final_Assembly.png" 
            alt="Image of Raspberry Pi and Arducam connected by orange ribbon cable">
        <figcaption>
            Completed setup of an Arducam connected to a Raspberry Pi 5.
        </figcaption>
    </figure>
    
7. Skip the WiFi network selection and software update, and press restart.
    <figure>
        <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/boot/Final_Assembly.png" 
            alt="Image of Raspberry Pi and Arducam connected by orange ribbon cable">
        <figcaption>
            Completed setup of an Arducam connected to a Raspberry Pi 5.
        </figcaption>
    </figure>
    
8. After the Pi boots up again, in the top right click on the wifi symbol (The two red x's with grey lines coming vertically from them) and click on your desired wifi connection.
    <figure>
        <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/hardware/Final_Assembly.png" 
            alt="Image of Raspberry Pi and Arducam connected by orange ribbon cable">
        <figcaption>
            Completed setup of an Arducam connected to a Raspberry Pi 5.
        </figcaption>
    </figure>
    
9.  For univeristy networks that require a username and password, 
   1. change the Authentication to "Protected EAP (PEAP)"
   2. check the "No CA certificate is required" box
   3. enter your username and password  
   4. press enter
    - To confirm: a grey box should pop up in the top right saying that you've connected to (insert WiFi name). If not, repeat this step and ensure that you've entered your credentials correctly.
    <figure>
        <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/hardware/Final_Assembly.png" 
            alt="Image of Raspberry Pi and Arducam connected by orange ribbon cable">
        <figcaption>
            Completed setup of an Arducam connected to a Raspberry Pi 5.
        </figcaption>
    </figure>
    
