# Overview
In Blender's Video Sequence Editor automatically wrap selected strips into meta with movie speed adjust to scene FPS

Blender is FPS based not seconds based (like movies are).  This add-on handles the conversion.

# Features
## Video Editor
### Strips Menu Option
In the Blender's Video Sequence Editor, there will be an option called **Adjust Video's Speed to Render FPS via Meta**
### Toolbar Button
new button

## Render Panel Parameter
Also panel put under 'Render' properties section called **Auto-adjust VSE FPS**.  Enabling this feature will have Blender automatically update respective meta strip's speed when you update the FPS settings for the overall render.

## Search lookup
Search on **Meta Adjust Video Speed to Render**

# Enabling Add-on
Make sure to download the .py script applicable to your version of Blender, and put it in your Blender add-ons folder

In Blender, the add-on is located in the **Sequencer** section and is named **Meta Adjust Video Speed to Render**

# Requirements
Exiftool is needed on your computer to use this add-on (e.g. apt-get install libimage-exiftool-perl_8.60-2), http://www.sno.phy.queensu.ca/~phil/exiftool/, https://smarnach.github.io/pyexiftool/ and rename to exiftool.exe or exiftool and put in C:\Windows or /usr/bin, etc. put exiftool.py in blender/2.7x/python/lib/ or other lib folder

# Limitations
This meta uses a Blender **Speed effect**, which has a multiply speed argument with only a precision to .00

# Notes
This script will opefully be updated on https://developer.blender.org/diffusion/BAC/repository/master/