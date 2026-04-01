# ATLYSS Archipelago

Archipelago randomizer implementation for ATLYSS. Enables multiworld randomizer gameplay with 137+ randomizable items, quest and level-based location checks, and configurable progression options.

## Installation

### Step 1: Install Archipelago
Download and install the latest Archipelago Release. Only required if you are hosting.

### Step 2: Install the World
Place the `atlyss.apworld` file in your Archipelago installation folder under the `custom_worlds/` folder.

### Step 2.5: Generate Yaml
Go to the AP Launcher and find `Generate Template Options`.  Click to generate the template options, then a yaml should be available for you to use in the `players/templates` subfolder.
You can edit the game options in "Options Creator" after making the edits to the game options, click export, you can find your yaml in the "Players" Folder

### Step 3: Install BepInEx
Download BepInEx 5.4.23.4 and extract it to your ATLYSS game directory.  Run the game once to initialize BepInEx.
A manual mod install is recommended.  Follow the BepInEx instructions on how to install it.

### Step 4: Install the Mod
Place the `.dll` files from the `AtlyssAP/Plugins` folder into `ATLYSS/BepInEx/plugins/`.

### Step 5: Connect In-Game
Launch Atlyss. Opening settings will present you with a new Archipelago tab. Enter the information there, then hit F5 to connect to your slot.

## Configuration

The mod supports several gameplay options configurable through your Archipelago YAML:

**Goal Options:** Boss Defeats (Zuulneruda, Slime Diva, Colossus, Galius), All Quests, and Level 32 are all goal options.

**Area Access:** Locked portals requiring Portal items, whether progressive or random.

**Shop Sanity:** Optional<sup>a</sup> randomization of shop inventories 

## Credits

This project was made possible with help from:

- AtlyssModdingCentral Discord server
- Mickemoose - Technical assistance and code contributions  
- Catman - Guidance and project support
- Nichologeam - Coding Partner (major help with this project)
- AzraeL0534 - Leader of this project
- Maude - Patching up the logic and tidying the apworld up
