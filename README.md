# rogueEditor

**rogueEditor** is a simple Pokerogue.net save editor written in Python.

![cmd](https://i.imgur.com/jhZwPAf.png)
![dex](https://i.imgur.com/tOkmhfa.png)

## Requirements

- Python 3.10.x
- Requests library

## Running the program without Python

- Download rogueEditor.zip from the "Compiled" folder or [here](https://github.com/OnyxdevSoftware/rogueEditor/raw/main/Compiled/rogueEditor.zip)
- Unzip/extract it into your desired location (It's recommended to create a new folder)
- Run the program with "rogueEditor.exe"

## Warning

Some antivirus software may give false positives when running this program.
Feel free to decompile it and look at its content.
- Compiled with PyInstaller 

## Usage
(Refresh your pokerogue.net page after any modifications!)

Hatch all eggs
- This will make all your eggs hatch after you defeat 1 Pokemon.

Dump trainer data to json file
- This will download your trainer data and generate a file called trainer.json (This file contains data such as stats, gacha tickets, etc) -> Edit the file with notepad or notepad ++

Dump save data (slot 1-5) to json file
- This will download your session data from one of your saves (slot 1-5) (This file contains data such as money, wave, your pokemons level and stats, etc) -> Edit the file with notepad or notepad ++

Update trainer data from dumped json file
- This will reupload the trainer.json file to pokerouge.net's servers

Update save data (slot 1-5) from dumped json file
- This will reupload the slot(number).json file to pokerouge.net's servers

Add/Modify a starter Pokemon (Pokemon name or Pokedex Id)
- This allows you to unlock and/or modify a Pokemon by its name or id (Shiny, Nature, Individual ivs, Eggmoves, Candies, etc)

Modify the amount of egg gacha tickets you have
- This allows you to set the amount of egg gacha tickets you have of every tier

Unlock all starters with perfect ivs and all shiny variants
- This will unlock every single Pokemon in the Pokedex with Perfect IVs, All natures, All shiny variants, Random amount of eggmoves and lots of candies

Display all starter Pokemon names with their Ids
- This simply shows you all the available Pokemon in the game with their names and id (Useful when you want to modify specific Pokemon)
  
## Q & A

Will I get banned for using this?
- Unlikely, but use common sense.
  
Why did nothing happen after my modifications?
- Refresh pokerogue.net in your browser.

How can i use this on the local version of Pokerogue?
- You can modify the API endpoints in the source to point towards localhost:8000.

## Final Words

- I take no responsibility for your actions when using this script.
This is a proof of concept / educational project.
- Yes, the code is lazy. 
Feel free to improve it.

<!-- Metadata: keywords -->
<meta name="description" content="rogueEditor is a simple Pokerogue.net save editor written in Python.">
<meta name="keywords" content="pokerogue, pokerogue save editor, pokerogue hacks, pokerogue hack, pokerogue cheats, pokerogue cheat, pokerogue trainer, pokerogue cheat table, rogueEditor, free, gacha, ticket, tickets, egg, eggs, shiny, save, edit, pokemon, unlimited, hack, hacks, cheat, cheats, trainer, table, pokedex, dex, wave, money, level, levels, iv, ivs, stat, stats, item, items, api, mod, mods, tool, tools">
