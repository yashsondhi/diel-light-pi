---
title: Software Setup
parent: Raspberry Pi Setup
last_modified_date: 
nav_order: 2
---
_Last updated: August 9, 2026_ 
{: .fs-2 .text-grey-dk-000 }

#Installing and Setting up the Raspberry Pi Software
## Installing Software

### Download the Imager

1. Go to [Raspberry Pi Imager Download](https://www.raspberrypi.com/software/) and click on "Download for Windows".

2. Install the downloaded software (follow the instructions and say yes/accept agreement) and press next for each step

3. After installing check the "launch imager" box after installing and press finish. 

---
### Setting Up Download in Imager

1. Double click Raspberry Pi 5.

2. Scroll down and click on "Raspberry Pi OS (other)"

3. Scroll down and click on Raspberry Pi OS (Legacy, 64-bit) with a description that says "A port of Debian Bookworm..." and press next.

4. Make sure your SD card is inserted, click on it (it should have a few GB less than the stated amount on your SD card), and press next.

5. Enter the Pi number with three digits. (Ex: Pi 1 would be 001)

6. Choose Washington, D.C. as the capital and make sure that the time zone is America/New_York and the keyboard layout is "us".

7. Enter your preferred username and password. If working in a lab, consult your PI.

8. Press skip customization and then "write", and then "I understand, Erase and Write".

9. Wait for the download to finish, and press Finish.

10. Take out the SD card.

---
## Setting Up the Raspberry Pi Imaging System

**BEFORE YOU DO ANYTHING WITH THE CAMERA WIRING, MAKE SURE THE RASPBERRY PI IS TURNED OFF AND UNPLUGGED**

1. Put the SD card into the SD card reader of the Raspberry Pi (with the Pi logo facing toward you, you should see the black side of the SD card).

2. Plug the HDMI and power cable into the Pi. 

3. After plugging the Pi in, it should automatically turn on. 

4. Change the country to United States, langauge to American English, and timezone to Eastern. Check the "Use English language" and "Use US keyboard" boxes and press next.

5. If not already created, create a user for the Pi, and enter your preferred username and password. If working in a lab, consult your PI. And press OK if there is a popup. 

6. Skip the WiFi network selection and software update, and press restart.

7. After the Pi boots up again, in the top right click on the wifi symbol (The two red x's with grey lines coming vertically from them) and click on CaseWireless.

8. Change the Authentication to "Protected EAP (PEAP)", check the "No CA certificate is required" box, and enter your case id for the username and case password for the password.  
    - There should be a grey box that pops up in the top right saying that you've connected to Case Wireless. If not, repeat this step and ensure that you've entered your credentials correctly.

---
Continue to the [software installation page](https://github.com/yashsondhi/diel-light-pi/wiki/Software-installation-(includes-motion)) to continue setting up diel-light-pi.

