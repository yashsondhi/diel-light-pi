---
title: Software Updates
parent: Raspberry Pi Setup
last_modified_date: 2026-10-10 07:42:26 +0000
nav_order: 4
---
# Updating Software and Verifying Hardware

## Update the Raspberry Pi

1. Open the terminal.
    <figure>
        <img src="{{ site.baseurl }}/assets/motion_setup/Open_Terminal.png" 
            alt="Image of a red box around the finish button">
        <figcaption>
            Open the Raspberry Pi's command terminal.
        </figcaption>
    </figure>

2. Update the Raspberry Pi and install motion using the command 
    ```bash
    sudo apt update && sudo apt upgrade -y && sudo apt autoremove -y
    ```
    <figure>
        <img src="{{ site.baseurl }}/assets/motion_setup/Update_System.png" 
            alt="Image of a red box around the finish button">
        <figcaption>
            This is the command that you enter to install motion and update the Raspberry Pi.
        </figcaption>
    </figure>

3. After the process finishes, the terminal should look like this:
    <figure>
        <img src="{{ site.baseurl }}/assets/motion_setup/Installed.png" 
            alt="Image of a red box around the finish button">
        <figcaption>
            What the terminal looks like after everything has installed.
        </figcaption>
    </figure>



## Verify the Camera Connection
1. Enter this command to check if the camera is detected.
    ```bash
    rpicam-still --list-camera
    ```
   - If no camera is detected, unplug and reconnect it.

    Make sure to turn off the Pi before disconnecting and reconnecting the camera.
    {: .warning}

    <figure>
        <img src="{{ site.baseurl }}/assets/motion_setup/Verify_Camera.png" 
            alt="Image of a red box around the finish button">s
        <figcaption>
            Enter this command to see a list of the connected cameras
        </figcaption>
    </figure>

2. The terminal should list the OV5647 camera.
    <figure>
        <img src="{{ site.baseurl }}/assets/motion_setup/Cameras.png" 
            alt="Image of a red box around the finish button">
        <figcaption>
            Enter this command to see a list of the connected cameras
        </figcaption>
    </figure>

3. To test that the camera works, enter this command.
    ```bash
    rpicam-still -t 0
    ```
   - Confirm the camera feed is visible.
   - To stop, go back to the terminal and press "CTRL+C" to quit
    <figure>
        <img src="{{ site.baseurl }}/assets/motion_setup/Preview.png" 
            alt="Image of a red box around the finish button">
        <figcaption>
            A video output of what the camera is seeing will show up.
        </figcaption>
    </figure>

4. Take an image using the following command, and make sure the terminal says "Still capture image received".
    ```bash
    rpicam-still -t 5000 -o test.jpg
    ```
    <figure>
        <img src="{{ site.baseurl }}/assets/motion_setup/Still_Image.png" 
            alt="Image of a red box around the finish button">
        <figcaption>
            What the terminal says after taking a single image.
        </figcaption>
    </figure>

5. To check that the image was saved, open the file storage and check that it shows up.
    <figure class="image-row">
        <div>
            <img src="{{ site.baseurl }}/assets/motion_setup/Open_Files.png" 
                alt="Image of a red box around the finish button">
            <figcaption>
                Click here to open the file system.
            </figcaption>
        </div>
        <div>
            <img src="{{ site.baseurl }}/assets/motion_setup/Test_Image.png" 
                alt="Image of a red box around the finish button">
            <figcaption>
                This is where test images will show up.
            </figcaption>
        </div>
    </figure>

Congrats! You've finished setting up the Raspberry Pi. Continue to [software installation][install software] to continue the guide.

[install software]: ../../software_installation/
