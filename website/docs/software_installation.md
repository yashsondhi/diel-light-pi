---
title: Install Software
last_modified_date: 
nav_order: 4
---
# Setting Up the Software Libraries

## Cloning the Diel-Light-Pi Repository
In order to access the code that we've created, you need to "clone" all the files that we've stored online through GitHub. 

1. Clone the repository using this command:
    ```bash
    git clone https://github.com/yashsondhi/diel-light-pi.git
    cd diel-light-pi
    ```
    <figure>
        <img src="{{ site.baseurl }}/assets/github_setup/Clone.png" 
            alt="Image of a red box around the finish button">
        <figcaption>
            Use this command to clone the GitHub repository.
        </figcaption>
    </figure>

2. This is what the terminal will say after successfully cloning the repository.
    <figure>
        <img src="{{ site.baseurl }}/assets/github_setup/Success.png" 
            alt="Image of a red box around the finish button">
        <figcaption>
            The terminal text after successfully cloning the repository.
        </figcaption>
    </figure>

## Install Required Libraries
1. Enter the following command to install Motion and YAML libraries to use the repository.
    ```bash
    sudo apt-get install python3-yaml && sudo apt install motion
    ```
    <figure>
        <img src="{{ site.baseurl }}/assets/github_setup/Install_Yaml.png" 
            alt="Image of a red box around the finish button">
        <figcaption>
            Use this command to install the Motion and YAML libraries.
        </figcaption>
    </figure>

2. The terminal will look like this when it's done. 
    <figure>
        <img src="{{ site.baseurl }}/assets/github_setup/Installed_Yaml.png" 
            alt="Image of a red box around the finish button">
        <figcaption>
            Successful terminal installation of Motion and YAML libraries looks like this.
        </figcaption>
    </figure>

Continue to the [usage page][usage] to continue the guide.

[usage]: ../usage/