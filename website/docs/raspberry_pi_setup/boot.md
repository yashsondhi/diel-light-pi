---
title: Booting Up 
parent: Raspberry Pi Setup
last_modified_date: 2026-10-10 07:42:26 +0000
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
            <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/boot/hardware/RPi_MicroSD.png" 
                alt="Image of the micro SD slot on the Raspberry Pi">
            <figcaption>
                The micro SD slot on a Raspberry Pi. The Raspberry Pi runs off the micro SD card that is inserted here.
            </figcaption>
        </div>
        <div>
            <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/boot/hardware/MicroSD_Inserted.png" 
                alt="Image of the micro SD card inserted in the Raspberry Pi">
            <figcaption>
                A micro SD card correctly and fully inserted into the Raspberry Pi.
            </figcaption>
        </div>
    </figure>

2. Plug in the USB keyboard and mouse into any of the USB ports.
    <figure class="image-row">
        <div>
            <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/boot/hardware/USB_Ports.png" 
                alt="Image of a red box around the USB ports on a Raspberry Pi 5">
            <figcaption>
                Plug in any USB devices here.
            </figcaption>
        </div>
        <div>
            <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/boot/hardware/USB_Port_with_Dongle.png" 
                alt="Image of two usb devices plugged into the Raspberry Pi 5">
            <figcaption>
                A USB keyboard and mouse pair plugged into the Raspberry Pi.
            </figcaption>
        </div>
    </figure>

3. Plug the USB C power cable into the bottom left port of the Raspberry Pi (left red box), and the micro HDMI cable into the middle metal connector (right red box). 
    <figure class="image-row">
        <div>
            <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/boot/hardware/USBC_MicroHDMI_Connectors.png" 
                alt="Image of a red box around the USBC and micro HDMI connectors on the Raspbery Pi">
            <figcaption>
                TThe Raspberry Pi gets its power from the USB C port. The Raspbery Pi outputs a display through the micro HDMI port. 
            </figcaption>
        </div>
        <div>
            <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/boot/hardware/Plugged.png" 
                alt="Image of a USB C and micro HDMI cable plugged into the Raspberry Pi">
            <figcaption>
                The power and display cables properly plugged in.
            </figcaption>
        </div>
    </figure>
    
4. After plugging the Pi in, the LED should first be red briefly, and then turn to green. It is okay if the green light flickers.  
    <figure>
        <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/boot/hardware/LED_On.png" 
            alt="Image of the LED indicator on the Raspberry Pi as Green">
        <figcaption>
            A green light here means that the Raspberry Pi succesfully turned on.
        </figcaption>
    </figure>

5. You should see a "Welcome to the Raspberry Pi Desktop" screen, and it should automatically jump into the desktop screen.
    <figure>
        <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/boot/raspberry_pi/Loading.png" 
            alt="Image of Raspberry Pi and Arducam connected by orange ribbon cable">
        <figcaption>
            Completed setup of an Arducam connected to a Raspberry Pi 5.
        </figcaption>
    </figure>
    
## Setting Up the Raspberry Pi
If you would like to control the Raspberry Pi without a separate monitor from your own computer, go to [Using VNC][vnc page] and then come back here to continue setting up the Raspberry Pi.
{: .note}

1. If the system gives you a welcome screen to set up the Raspberry Pi, make sure you didn't press "skip customization" in the Raspberry Pi Imager. Create the image on the SD card again. [Software Setup][software page]
    <figure>
        <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/boot/raspberry_pi/Welcome.png" 
            alt="Image of Raspberry Pi and Arducam connected by orange ribbon cable">
        <figcaption>
            You don't want to see this page. This means you skipped the customizations instead of continuing to press next/continue.
        </figcaption>
    </figure>
    
2. After the Pi boots up again, in the top right click on the wifi symbol.
    <figure>
        <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/boot/raspberry_pi/wifi/Select_No_WiFi_Icon.png" 
            alt="Image of Raspberry Pi and Arducam connected by orange ribbon cable">
        <figcaption>
            Click here to see the WiFi menu.
        </figcaption>
    </figure>

3. Select the option to turn on the WiFi.
    <figure>
        <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/boot/raspberry_pi/wifi/Turn_On_WiFi.png" 
            alt="Image of Raspberry Pi and Arducam connected by orange ribbon cable">
        <figcaption>
            Click on this to turn on the WiFi.
        </figcaption>
    </figure>

4. Select your preferred network address.
    <figure>
        <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/boot/raspberry_pi/wifi/Select_WiFi_Network.png" 
            alt="Image of Raspberry Pi and Arducam connected by orange ribbon cable">
        <figcaption>
            Select the wifi connection that you want to connect to.
        </figcaption>
    </figure>
    
5. For univeristy networks that require a username and password, 
    - Change the Authentication to "Protected EAP (PEAP)"
    - Check the "No CA certificate is required" box
    - Enter your username and password  
    - Press enter
    <figure>
        <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/boot/raspberry_pi/wifi/WiFi_Settings.png" 
            alt="Image of Raspberry Pi and Arducam connected by orange ribbon cable">
        <figcaption>
            The boxes that you need to change/fill out are highlighted.
        </figcaption>
    </figure>

6. A grey box should pop up confirming that you connected to the network.
    <figure>
        <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/boot/raspberry_pi/wifi/WiFi_Confirmation.png" 
            alt="Image of Raspberry Pi and Arducam connected by orange ribbon cable">
        <figcaption>
            The confirmation message that the Pi gives after the connection succeeds.
        </figcaption>
    </figure>


You've now set up the Raspberry Pi! Continue to the [software installation page][install software] to continue setting up the Raspberry Pi.
    
[vnc page]: ../vnc/vnc
[software page]: ../boot/
[install software]: ../../software_installation/
