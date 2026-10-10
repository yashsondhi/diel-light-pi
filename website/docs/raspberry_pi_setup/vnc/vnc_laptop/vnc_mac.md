---
title: Set Up VNC on Mac/Linux
parent: Setting Up VNC
last_modified_date: 2026-10-10 07:42:26 +0000
nav_order: 2
---
# Setting Up VNC Viewer on Mac
As you can see from the lack of images on this page, I have a Windows computer. If you would like to contribute to the documentation, please do so [here][github]!
{: .note}

## Integrated VNC Viewer


1. Open Finder.
2. Press "Cmd + K".
3. Enter the Raspberry Pi's IP address using the following format (don't enter leading zeros): 
    ```bash
    vnc://xxx.xxx.xxx.xxx
    ```
4. Press Connect.
5. Enter the username and password for the Raspberry Pi.

## TigerVNC Viewer
1. Go to the [TigerVNC GitHub page][tiger vnc github] and click on the tar.gz source code. 
    <figure>
        <div>
            <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/boot/desktop_vnc/GitHub.png" 
                alt="Image of a red box around the Raspberry Pi Terminal Icon">
            <figcaption>
                Click on this link to download the current version of TigerVNC for Mac/Linux.
            </figcaption>
        </div>
    </figure>

2. Double click the tar.gz file.
3. Open the newly created folder.
4. Right click the vncviewer binary file and select open.
5. Click open on the security pop-up.

[tiger vnc github]: https://github.com/TigerVNC/tigervnc/releases
[github]: https://github.com/yashsondhi/diel-light-pi/tree/website-documentation
