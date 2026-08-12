---
title: Hardware Requirements
parent: Requirements
last_modified_date: 2026-08-12 02:17:26 +0000
nav_order: 1
---
# Hardware Requirements
- Any desktop environment (ex. laptop running MacOS, Linux, or Windows)
- Raspberry Pi 4/5, 2/4/8GB versions (note that this guide is for the Pi 5 and there may be some discrepancies if using Pi 4) 
- USB C charger
- 64GB micro-sd card or greater
- Any Micro SD card to USB adapter (to connect to the desktop environment)
- HDMI cable + Monitor
  - HDMI to Micro HDMI adapter if the cable is only HDMI to HDMI
- USB Keyboard 
- USB mouse
- Some version of Arducam (NOIR cut filter is recommended)
 
Wireless keyboards and mouse may require additional setup.
{: .note}

# Required Parts 
(Prices are of July 2026)
{: .fs-3}

The links below are just the ones that this lab has used. You can source your parts from your preferred vendors.
{: .note}

Part                                        |   Link
:--------------------------------------------|:--------------------------------------------------------------------
Arducam IR and Visible Light Camera         |   [(Amazon) Arducam OV5647 with IR Cut ~$24](https://a.co/d/0dcKxz2u) 
Raspberry Pi 5                              |   [(CanaKit) Raspberry Pi 5 2GB ~$65](https://www.canakit.com/raspberry-pi-5-2gb.html)
Raspberry Pi 5 Charger[^1]                  |   [(CanaKit) Raspberry Pi 27W Charger ~$13](https://www.canakit.com/official-raspberry-pi-5-power-supply-27w-usb-c.html)
Micro SD Card[^2]                           |   [(B&H Photo Video) Sandisk High Endurance 128 GB SD Card ~$35](https://www.bhphotovideo.com/c/product/1466563-REG/sandisk_sdsqqnr_128g_an6ia_high_endurance_microsd_128gb.html)
HDMI to Micro HDMI[^3]                      |   [(Amazon) HDMI to Micro HDMI Cable ~$6](https://a.co/d/0cNaILoh)
Micro SD Card to USB A Adapter              |   [(Amazon) SD to USB A/USB C ~$8](https://a.co/d/0f78Kxmq)

# Optional Parts (July 2026):
**Raspberry Pi 5 Kits**

You can get kits to simplify the ordering process, but they typically come with a markup of ~$20. Here are two potential ones:
- [(CanaKit) Raspberry Pi 5 2GB Kit (Missing Arducam) ~$160](https://www.canakit.com/canakit-raspberry-pi-5-starter-kit-turbine-black.html)
- [(Virilos) Raspberry Pi 5 2GB Kit (Missing Arducam) ~$110](https://vilros.com/products/vilros-raspberry-pi-5-basic-starter-kit?variant=41114197688414)
  - We found that the Virilos case doesn't really work with the Arducam cable as the hole is not centered on the connector, which means you have to bend the camera cable in an awkward direction and put some stress on it.

**IR Floodlight**

The Arducam IR lights are dim, so using an IR floodlight usually makes dark environment images clearer. However, it's also important to not get one that's too bright since it can completely saturate the camera. The first one seems to be a good brightness from our testing.
- [(Amazon) IR Floodlight ~$28](https://a.co/d/0aOXjHkO)
- [(Amazon) IR LED Ring 2x ~$13](https://a.co/d/01oboP0Z)

**Heatsinks**

The Raspberry Pi heats up significantly with prolonged use, which can reduce performance in hot environments. Attaching heat sinks to critical areas can greatly improve heat dissapation.
- [(Amazon) Heatsinks 100x ~$12](https://a.co/d/01dLgAJX)

---

[^1]: Any USB C charger should work, but Raspberry Pi recommends using a 27W one to not damage the Pi
[^2]: Any card that can withstand many read/write operations is best for this, like SD cards made for dashcams
[^3]: An HDMI to Micro HDMI adapter works as well if you already have an HDMI to HDMI cable
