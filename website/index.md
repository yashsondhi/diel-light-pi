---
title: Home
layout: home
nav_order: 1
description: "The portable locomotion activity monitor is a low cost DIY activity monitor using Raspberry Pi's motion library and an Arducam."
permalink: /
last_modified_date: 2026-08-12 02:38:05 +0000
---
# diel-light-pi
diel-light-pi is a low-cost, open-source portable locomotion activity monitor (pLAM) for tracking the diel activity of small animals using a Raspberry Pi, using camera-based motion detection and programmable LED light control to automatically record when and how much your study animals are moving — under any light condition, in the lab or the field.

All the Pi scripts, configuration files, and analysis pipeline are **provided free and open source**, so you can build, share, and improve on these designs yourself!

We believe **studying the daily activity rhythms of small animals is fundamental to understanding life on earth**, and simply want this technology in the hands of as many researchers as possible.


{: .important-title }
> Stay in Touch
>
> Are you using diel-light-pi in your research? Building your own setup? Please reach out and let us know! **Email us at yxs1621@case.edu** with subject "diel-light-pi."


{: .important-title }
> Cite This Work
>
> If you use diel-light-pi in your research, please cite our paper: Sondhi et al. (2022). Portable locomotion activity monitor (pLAM): A cost-effective setup for robust activity tracking in small animals. *Methods in Ecology and Evolution*, 13, 805–812. [https://doi.org/10.1111/2041-210X.13809][paper]


Read [the blog post about how and why pLAM was built.][blog]
Or [read the scientific paper][paper] describing the system and its validation!

![A Raspberry Pi camera-based pLAM setup monitoring a moth in a cage](#)

# Set it Up Yourself!

This documentation will walk you through everything you need to source, install, configure, and run your own pLAM setup on a Raspberry Pi.

[Get started setting up diel-light-pi!][building]

After following these guides, you should be able to deploy your own activity monitors and begin collecting diel data for your study animals!

## Why Study Diel Activity?

An animal's diel activity pattern — whether it is diurnal, nocturnal, crepuscular, or cathemeral — is one of the most fundamental windows into its biology, and tracking these patterns with a pLAM can reveal how animals respond to their environment in real time.

### Activity Patterns Vary Enormously, Even Within a Single Group

We often think of butterflies as day-flying and moths as night-flying, but there is a whole spectrum of variation — some butterflies fly at night, some moths fly during the day, and many species are only active at dusk or dawn — and understanding **why** this variation exists requires measuring the exact times and light conditions when each species is active, which is precisely what diel-light-pi was designed to do.

### Small Animals Are Difficult to Track With Existing Tools

Commercial camera traps and existing motion-capture systems are optimised for larger animals and fail to reliably detect the small, subtle movements of insects or spiders, while the few commercial solutions that do handle small animals are expensive, closed-source, and designed only for lab use — diel-light-pi fills this gap as an open-source, portable, low-cost system that works under any light condition, including complete darkness using infrared illumination invisible to most insects.

### Diel Data Unlocks Ecological Insights

Because insects tend to have short lives and limited ranges, their activity patterns provide super-localised data about environmental conditions, and combining activity data from dozens of species with climate, acoustic, or soil data can provide deep insights into how environments are changing — with a single pLAM running overnight capturing data that would otherwise require a researcher to sit up all night manually logging observations.


## What it Does

diel-light-pi runs on a Raspberry Pi and uses the open-source [Motion][motion] library to continuously compare camera frames, logging a motion event and saving a photo or video clip whenever two consecutive images differ enough to indicate an animal has moved.

![A pLAM activity plot showing motion events over a 24-hour period](#)

For experiments that require controlled light environments, diel-light-pi also drives NeoPixel LED strips via `smooth_light_control.py`, letting you program gradual light/dark cycles that mimic natural dawn and dusk — or add artificial light pollution to study its effects on behaviour.

Once your experiment is complete, the built-in analysis pipeline extracts all motion events from the logs, bins them into activity counts, and generates actogram-style plots so you can immediately visualise your animal's diel rhythm.

![Example actogram output from the diel-light-pi analysis pipeline](#)

# pLAM in the Field

The pLAM was field-tested in Monteverde, Costa Rica, where six units ran simultaneously over two weeks at a biological station, collecting activity data for approximately 15 species over 10 nights despite fluctuating power, wind, and an abundance of moths.

The system has also been validated against a commercial $4,000 infrared beam-based activity detector — and in some cases the pLAM was found to be *more* sensitive.

![The research team deploying pLAMs at CIEE Monteverde](#)


[blog]: https://methodsblog.com/2022/03/03/how-do-you-measure-the-movement-of-tiny-insects/
[paper]: https://doi.org/10.1111/2041-210X.13809
[motion]: https://motion-project.github.io/
[building]: docs/requirements/requirements/