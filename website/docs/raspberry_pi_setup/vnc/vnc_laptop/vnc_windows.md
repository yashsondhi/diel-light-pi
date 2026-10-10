---
title: Set Up VNC on Windows
parent: Setting Up VNC
last_modified_date: 2026-10-10 07:42:26 +0000
nav_order: 1
---
# Setting Up VNC Viewer on Windows

1. Click on this [link][tiger vnc download] to download TigerVNC Viewer version 1.16.2. Or, you can go [here][tiger vnc homepage], click on the latest version (the one at the top), and click on "vncviewer64-x.xx.x.exe".
    <figure>
        <div>
            <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/boot/desktop_vnc/Download.png" 
                alt="Image of a red box around the Raspberry Pi Terminal Icon">
            <figcaption>
                Click on this link to download the current version of TigerVNC viewer.
            </figcaption>
        </div>
    </figure>

2. After TigerVNC downloads, open it, enter the IP Address in the "VNC server" field, and press "connect".
    <figure>
        <div>
            <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/boot/desktop_vnc/TigerVNC_IP.png" 
                alt="Image of a red box around the Raspberry Pi Terminal Icon">
            <figcaption>
                Click on this to open the terminal.
            </figcaption>
        </div>
    </figure>

3. Two screens will pop up, one saying "Unknown certificate issuer" and the other saying "Certificate hostname mismatch". Click "Yes" on both.
    <figure class="image-row">
        <div>
            <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/boot/desktop_vnc/Unknown_Certificate_Issuer.png" 
                alt="Image of a red box around the Raspberry Pi Terminal Icon">
            <figcaption>
                Warning that the computer doesn't recognize the certificate issuer.
            </figcaption>
        </div>
        <div>
            <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/boot/desktop_vnc/Hostname_Mismatch.png" 
                alt="Image of a red box around the Raspberry Pi Terminal Icon">
            <figcaption>
                Warning that the hostname on the certificate and the typed IP address don't match.
            </figcaption>
        </div>
    </figure>

4. Enter the username and password information, and press "ok". You can also press keep password for reconnect to save time on logging back in.
    <figure>
        <div>
            <img src="{{ site.baseurl }}/assets/raspberry_pi_setup/boot/desktop_vnc/VNC_Login.png" 
                alt="Image of a red box around the Raspberry Pi Terminal Icon">
            <figcaption>
                Enter the login details of the Raspberry Pi here.
            </figcaption>
        </div>
    </figure>


[tiger vnc download]: https://sourceforge.net/projects/tigervnc/files/stable/1.16.2/vncviewer64-1.16.2.exe/download
[tiger vnc homepage]: https://sourceforge.net/projects/tigervnc/files/stable/
