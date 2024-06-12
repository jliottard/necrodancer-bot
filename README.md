# CryptOfTheNecroDancerBot

## Description

CryptOfTheNecroDancerBot is a project for implementing a player bot of the game Crypt of the Necrodancer.
From screenshots taken in real time, the bot is meant to analyze what is on screen and find its way to the downstairs.

## Requirements

Using Python, this project requires to have as pip packages:
- numpy
- opencv-python
- Pillow
- pywin32

## How to use

First, launch the game Crypt of the NecroDancer in windowed mod. This windows must have "Crypt of the NecroDancer" as its title.
Then, execute the main.py file:
`py main.py`

If debug mod is actived, a debug window will appear to see what images are detected with colored rectangles.
Exit the program, press 'q' while having the debug window active.

## References

The computer vision part is based on the [Youtube playlist named "OpenCV Object Detection in Games"](https://youtube.com/playlist?list=PL1m2M8LQlzfKtkKq2lK5xko4X-8EZzFPI) by Learn Code By Gaming.
The path finding part is based on ["Path Planning - A* (A-Star)" video](https://youtu.be/icZj67PTFhc) made by javidx9.

Game's website : [Brace Yourself Games](https://braceyourselfgames.com/crypt-of-the-necrodancer/)