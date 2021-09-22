# Funkin' Bot
<img src="images/funkin_gif.gif" alt="gif of bot playing a level"/>
For video tutorial click <a href="https://youtu.be/o1Z0mwdP1qE
">here.</a>

## Description
Funkin' Bot is a python script that plays any Friday Night Funkin' level in real time using a series of image captures.

## Strengths
* Ability to play most FNF levels and mods
* Supports any screen resolution
* Works on browser and installed versions of the game
## Limitations
* Struggle with very fast, consecutive notes  
  
  <img src="images/consecutive_notes.png" alt="image of arrow box position markers" width="300"/>
* Will not work with mods that have the same idle and note colors
  
  <img src="images/idle_notes.png" alt="image of arrow box position markers" width="300"/>
## Requirements
* Windows
* Python3
  * Program tested on python 3.7
## Installation
1. Download and extract the latest release to your chosen directory.
2. Open the directory inside the Windows Command Prompt. Performance will be more reliable if you create a Python 3.7 virtual environment.
3. Run **pip install -r requirements.txt** on the command-line.
## Usage
1. Run the game.
2. Run **funkin_bot.py** and enter the configuration you want in the terminal. Program comes with two configurations: **vanilla** and **netmods**.
3. Hover your cursor over each arrow's corresponding arrow position, starting with the leftmost arrow. Adequate positions look like this:

   <img src="images/arrow_box.png" alt="image of arrow box position markers" width="200"/>
4. Hit **shift** to confirm arrow location and repeat steps 3-4 for remaining arrows.
5. A window displaying the arrow box will appear. The bot can start any level now.
* To stop bot, select the arrow box window and press **"q"**.
* If the bot's inputs are delayed, you should select a lower point along the arrow, and viceversa if they are early.

## Creating Configurations
1. Start level and pause it. Make sure no notes are near the arrow box.
2. Run **make_config.py**.
3. Hover your cursor over each arrow's positition, similar to funkin_bot.py.
4. Hit **shift** to confirm each arrow. After the four arrows are defined, unpause the game and press **shift** once more.
5. Program will run until all arrow colors can be extracted.
6. Enter the name of the configuration in the terminal. The configuration will be be saved as a JSON file.