---
title: Installing Software
last_modified_date: 2026-08-12 02:22:26 +0000
nav_order: 4
---
# Motion & diel-light-pi Setup on Debian (ARM64 Bookworm)

This guide walks you through setting up **Motion** and the **diel-light-pi** repository on a Debian-based ARM64 system (e.g., Raspberry Pi running Bookworm) and is recommended for Pi5 and up. 

---

## Update the System
Update and upgrade all installed packages:
```bash
sudo apt update && sudo apt upgrade -y 
```

---

##  Install Motion

### Install Motion Package
```bash
sudo apt install motion -y
```
<u>If this does not work, follow the steps below. Otherwise, continue to the next section.</u>
### 1. Download the Motion Package
Download the `motion` package for **ARM64 Bookworm** from the official or trusted source.

### 2. Install the Package with `gdebi`


```bash
sudo gdebi <motion-package>.deb
```
*Replace `<motion-package>.deb` with the actual filename.*

You may need to download gedbi with apt
and make sure you use the correct build.
For Pi5's it is usually bookworm arm64


### 3. Install Build Dependencies (Optional, for source builds)
```bash

sudo apt-get install autoconf automake autopoint build-essential pkgconf libtool libzip-dev libjpeg-dev git libavformat-dev libavcodec-dev libavutil-dev libswscale-dev libavdevice-dev libwebp-dev gettext libmicrohttpd-dev libcamera-tools libcamera-dev libcamera-v4l2

Double check the motion page (https://motion-project.github.io/motion_build.html)

```
Adjust the list based on your build requirements.

---

## 🔍 Verify the Camera
### Ensure the USB or CSI camera is connected.
```bash
rpicam-still --list-camera
```
- If no camera is detected, unplug and reconnect it.
- MAKE SURE TO TURN OFF THE PI BEFORE DISCONNECTING AND RECONNECTING

### Test camera with `rpicam`
```bash
rpicam-still -t 0
```
- Confirm the camera feed is visible.
- To stop, go back to the terminal and press CTRL+C to quit

### Take an image with a 5 second preview
```bash
rpicam-still -t 5000 -o test.jpg
```

---

## Set Up `diel-light-pi`

### 1. Clone the Repository
```bash
git clone https://github.com/yashsondhi/diel-light-pi.git
cd diel-light-pi
```

### 2. Install YAML Support
```bash
sudo apt-get install python3-yaml
```

> `pip install pyyaml` may not work on this platform, so use `apt`.

---

### 3. Verify installation
Go back to the terminal and make sure that you're in the "diel-light-pi" folder. If not, type
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

**You're Done!**
- Motion is installed and tested.
- `diel-light-pi` is cloned.
- YAML dependencies are in place.

You can now begin configuring and using the diel-light-pi scripts for light tracking and automation.

---

🛠 *Need help?* Open an issue on the GitHub repository or post to the relevant community forums.
