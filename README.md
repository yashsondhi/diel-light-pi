# diel-light-pi
Creates activity detector scripts for the Rasberry pi to monitor diel activity of small insects
# Setup
1.clone the git repository to your rasberry pi using git clone or download the files. 
2. `run python3 run_diel-light.py --time` to update time if required. 
3. `run python3 run_diel-light.py --project` to displat output parameters for project. If they require updating. Modify the `configs/project.conf`. 
4.run python3 run_diel-light.py --run

##Configuration files to modify
Files to modify configs/motion.conf for the motion detection files. 
Project configuration files to modify configs/project.conf. 
For a more detailed guide on modifying motion tracking parameters, refer to https://motion-project.github.io/
