# Overview
[![screenshot](https://github.com/escapecode/Blender-VSE_FPS_adjust/blob/master/screenshots/00.jpg)](https://raw.github.com/wiki/escapecode/Blender-VSE_FPS_adjust/blob/master/screenshots/00.jpg)

This Blender add-on automates  the Video Sequence Editor when adjusting each strip's FPS to match your output render's FPS.  If you change your output render FPS, all associated strips will be updated.

Using this add-on prevents movie strips playing too fast or slow, movies not synchronized with sounds, etc.  Also, audio and movie strips from an imported video are combined into a meta.  This makes it easier to do operations such as moving and cutting, since you only have to move a meta, not a movie and audio strip in unison.
 Video Sequence Editor automatically wrap selected strips into meta with movie speed adjust to scene FPS

## Why do I have to adjust all of my movie framerates
Blender is a renderer first before it is a video editor.  Renderers are **frame** based (eg "I want 50 frames rendered and I don't want to think about syncing the render with other videos").  Video editors are **time** based (eg "I have 5 videos at different framerates.  I want them to run them synchronously and have them run at the same speed....I don't care how many frames there are"). This add-on helps bridge the gap between renderers and video editors.

## Add-on Requirements
Exiftool is needed on your computer to use this add-on (e.g. apt-get install libimage-exiftool-perl_8.60-2), http://www.sno.phy.queensu.ca/~phil/exiftool/, https://smarnach.github.io/pyexiftool/ and rename to exiftool.exe or exiftool and put in C:\Windows or /usr/bin, etc. put exiftool.py in blender/2.7x/python/lib/ or other lib folder

# Quickstart
[![screenshot](https://github.com/escapecode/Blender-VSE_FPS_adjust/blob/master/screenshots/01.jpg)](https://raw.github.com/wiki/escapecode/Blender-VSE_FPS_adjust/blob/master/screenshots/01.jpg)

Download  the .py file that is the same version as your Blender, as well as the vse_fps_adjust.png file.  Put these in your Blender scripts/addons folder.  Bring up your user preferences and enable the add-on.

[![screenshot](https://github.com/escapecode/Blender-VSE_FPS_adjust/blob/master/screenshots/02.jpg)](https://raw.github.com/wiki/escapecode/Blender-VSE_FPS_adjust/blob/master/screenshots/02.jpg)

The add-on will add a panel under Render > Properties

[![screenshot](https://github.com/escapecode/Blender-VSE_FPS_adjust/blob/master/screenshots/03.jpg)](https://raw.github.com/wiki/escapecode/Blender-VSE_FPS_adjust/blob/master/screenshots/03.jpg)

When importing movies to the sequencer timeline, the FPS of the video, could be different from the FPS you will render out to.  In this case, you can see that the audio strip looks longer than the movie strip (since the movie strip is not synchronized with the FPS you will be rendering at)

[![screenshot](https://github.com/escapecode/Blender-VSE_FPS_adjust/blob/master/screenshots/04.jpg)](https://raw.github.com/wiki/escapecode/Blender-VSE_FPS_adjust/blob/master/screenshots/04.jpg)

Using the menu option the audio and movie strips will be combined in a meta, and have it's speed adjusted automatically and correctly

[![screenshot](https://github.com/escapecode/Blender-VSE_FPS_adjust/blob/master/screenshots/05.jpg)](https://raw.github.com/wiki/escapecode/Blender-VSE_FPS_adjust/blob/master/screenshots/05.jpg)

Instead of using the menu option, there is a button on the panel bar

[![screenshot](https://github.com/escapecode/Blender-VSE_FPS_adjust/blob/master/screenshots/06.jpg)](https://raw.github.com/wiki/escapecode/Blender-VSE_FPS_adjust/blob/master/screenshots/06.jpg)

After using either the menu entry or button, you can now see that all strips are wrapped in a meta, and will play back at correct speed

[![screenshot](https://github.com/escapecode/Blender-VSE_FPS_adjust/blob/master/screenshots/07.jpg)](https://raw.github.com/wiki/escapecode/Blender-VSE_FPS_adjust/blob/master/screenshots/07.jpg)

Looking inside the meta (by selecting the meta, and hitting the tab key), you can see a speed effect strip that handles making your movie play at the correct FPS.  Exit out of the meta by hitting Tab

[![screenshot](https://github.com/escapecode/Blender-VSE_FPS_adjust/blob/master/screenshots/08.jpg)](https://raw.github.com/wiki/escapecode/Blender-VSE_FPS_adjust/blob/master/screenshots/08.jpg)

Again notice the panel called "Meta matching Movie Speed to FPS".  It is located in the Render Properties section.  The "auto-adjust metas" checkbox is enabled.  So in this example, when the FPS value was changed from 23.98fps to 30fps, the meta you had created adjusted it's speed appropriately.  The real power of enabling this checkbox is when you have many movie strips with different speeds.  If you changed the FPS of your render, without this add-on, you would have to update all movie strips manually.

# Documentation

The [GitHub Wiki](https://github.com/escapecode/Blender-VSE_FPS_adjust/wiki) can serve as a central hub for all of
documentation, if there is a demand for this add-on, or if such is requested by the public.  This has not been done at this time, since Blender has an add-on section on it's website (which might be used). Possible Quick links:

* [Install](https://github.com/escapecode/Blender-VSE_FPS_adjust/wiki/Installation)
* [Configure](https://github.com/escapecode/Blender-VSE_FPS_adjust/wiki/Configuration-Settings)
* [User Configs](https://github.com/escapecode/Blender-VSE_FPS_adjust/wiki/User-Configs)
* [Frequently Asked Questions](https://github.com/escapecode/Blender-VSE_FPS_adjust/wiki/FAQ)

# Limitations
This add-on uses a Blender **Speed effect**, which has a granularity of only .00.  With long playing videos and extremely varying FPS values different from the output render, the output playback might be off.

# Notes
This script will opefully be updated on https://developer.blender.org/diffusion/BAC/repository/master/

# License

This add-on is licensed under the terms of the [GPLv3](LICENSE.GPL) and
[BSD](LICENSE.BSD) licenses.

# Contributing

To submit code changes, please open pull requests against [the GitHub repository](https://github.com/escapecode/Blender-VSE_FPS_adjust/edit/master/README.md). Patches submitted in issues, email, or elsewhere will likely be ignored. Here's some general guidelines when submitting PRs:

 * In your pull request, please:
   * Describe the changes, why they were necessary, etc
   * Describe how the changes affect existing behaviour
   * Describe how you tested and validated your changes
   * Include any relevant screenshots/evidence demonstrating that the changes work and have been tested
 * Any new source files should include a GPLv3 license header
 * Any contributed code must be GPLv3 licensed

[wiki]: https://github.com/escapecode/Blender-VSE_FPS_adjust/wiki
