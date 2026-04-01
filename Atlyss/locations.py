from typing import Dict, NamedTuple, Optional
from BaseClasses import Location

# Base location ID for ATLYSS
BASE_LOCATION_ID = 591000


class LocationData(NamedTuple):
    """Data for an ATLYSS location"""
    code: int
    region: str = "Menu"  # Default to Menu region


# All locations in ATLYSS
# UPDATED: Region assignments now reflect the actual game area each check is in,
# based on the Atlyss Logic Sheets spreadsheet (area level ranges and access paths).
# Previously everything was "Menu" which put everything in sphere 0/1.
# Catacombs split into 3 floors, Grove split into 2 floors.
location_table: Dict[str, LocationData] = {
    # Boss defeats - assigned to the region where the boss is fought
    "Defeat Slime Diva": LocationData(BASE_LOCATION_ID + 1, "Effold Terrace"),
    "Defeat Lord Zuulneruda": LocationData(BASE_LOCATION_ID + 2, "Catacombs Floor 2"),
    "Defeat Galius": LocationData(BASE_LOCATION_ID + 3, "Bularr Fortress"),
    "Defeat Colossus": LocationData(BASE_LOCATION_ID + 4, "Grove Floor 1"),
    "Defeat Lord Kaluuz": LocationData(BASE_LOCATION_ID + 5, "Catacombs Floor 3"),
    "Defeat Valdur": LocationData(BASE_LOCATION_ID + 6, "Grove Floor 2"),

    # Level milestones (Menu region - gated by rules requiring area access)
    "Reach Level 2": LocationData(BASE_LOCATION_ID + 10, "Menu"),
    "Reach Level 4": LocationData(BASE_LOCATION_ID + 11, "Menu"),
    "Reach Level 6": LocationData(BASE_LOCATION_ID + 12, "Menu"),
    "Reach Level 8": LocationData(BASE_LOCATION_ID + 13, "Menu"),
    "Reach Level 10": LocationData(BASE_LOCATION_ID + 14, "Menu"),
    "Reach Level 12": LocationData(BASE_LOCATION_ID + 15, "Menu"),
    "Reach Level 14": LocationData(BASE_LOCATION_ID + 16, "Menu"),
    "Reach Level 16": LocationData(BASE_LOCATION_ID + 17, "Menu"),
    "Reach Level 18": LocationData(BASE_LOCATION_ID + 18, "Menu"),
    "Reach Level 20": LocationData(BASE_LOCATION_ID + 19, "Menu"),
    "Reach Level 22": LocationData(BASE_LOCATION_ID + 20, "Menu"),
    "Reach Level 24": LocationData(BASE_LOCATION_ID + 21, "Menu"),
    "Reach Level 26": LocationData(BASE_LOCATION_ID + 22, "Menu"),
    "Reach Level 28": LocationData(BASE_LOCATION_ID + 23, "Menu"),
    "Reach Level 30": LocationData(BASE_LOCATION_ID + 24, "Menu"),
    "Reach Level 32": LocationData(BASE_LOCATION_ID + 25, "Menu"),

    # Tutorial/intro quests (Sanctum hub)
    "A Warm Welcome": LocationData(BASE_LOCATION_ID + 30, "Menu"),
    "Communing Catacombs": LocationData(BASE_LOCATION_ID + 31, "Menu"),

    # Catacombs Floor 1 quests (lv 1-6)
    "Dense Ingots": LocationData(BASE_LOCATION_ID + 100, "Catacombs Floor 1"),
    "Ghostly Goods": LocationData(BASE_LOCATION_ID + 101, "Catacombs Floor 1"),
    "Killing Tomb": LocationData(BASE_LOCATION_ID + 102, "Catacombs Floor 1"),
    "Night Spirits": LocationData(BASE_LOCATION_ID + 103, "Catacombs Floor 1"),
    "Ridding Slimes": LocationData(BASE_LOCATION_ID + 104, "Catacombs Floor 1"),
    "Summore' Spectral Powder!": LocationData(BASE_LOCATION_ID + 105, "Catacombs Floor 1"),

    # Outer Sanctum quests (lv 1-4)
    "Call of Fury": LocationData(BASE_LOCATION_ID + 110, "Outer Sanctum"),
    "Cold Shoulder": LocationData(BASE_LOCATION_ID + 111, "Outer Sanctum"),
    "Focusin' in": LocationData(BASE_LOCATION_ID + 112, "Outer Sanctum"),

    # Effold Terrace quests (lv 1-10)
    "Cleaning Terrace": LocationData(BASE_LOCATION_ID + 115, "Effold Terrace"),
    "Huntin' Hogs": LocationData(BASE_LOCATION_ID + 116, "Tull Valley"),

    # Arcwood Pass / Catacombs Floor 1 quests (lv 1-6)
    "Amberite Ingots": LocationData(BASE_LOCATION_ID + 120, "Arcwood Pass"),
    "Makin' a Mekspear": LocationData(BASE_LOCATION_ID + 121, "Menu"),
    "Makin' More Mekspears": LocationData(BASE_LOCATION_ID + 122, "Menu"),
    "Purging the Undead": LocationData(BASE_LOCATION_ID + 123, "Catacombs Floor 1"),
    "Rattlecage Rage": LocationData(BASE_LOCATION_ID + 124, "Catacombs Floor 1"),
    "Ancient Beings": LocationData(BASE_LOCATION_ID + 125, "Arcwood Pass"),

    # Tull Valley quests (lv 8-14)
    "Makin' a Vile Blade": LocationData(BASE_LOCATION_ID + 130, "Menu"),
    "Makin' a Wizwand": LocationData(BASE_LOCATION_ID + 131, "Menu"),
    "Makin' More Vile Blades": LocationData(BASE_LOCATION_ID + 132, "Menu"),
    "Makin' More Wizwands": LocationData(BASE_LOCATION_ID + 133, "Menu"),
    "Sapphite Ingots": LocationData(BASE_LOCATION_ID + 134, "Tull Valley"),

    # Crescent Road quests (lv 8-14)
    "Devious Pact": LocationData(BASE_LOCATION_ID + 140, "Crescent Road"),
    "Disciple of Magic": LocationData(BASE_LOCATION_ID + 141, "Crescent Road"),
    "Mastery of Dexterity": LocationData(BASE_LOCATION_ID + 142, "Crescent Road"),
    "Mastery of Mind": LocationData(BASE_LOCATION_ID + 143, "Crescent Road"),
    "Mastery of Strength": LocationData(BASE_LOCATION_ID + 144, "Crescent Road"),
    "Strength and Honor": LocationData(BASE_LOCATION_ID + 145, "Crescent Road"),
    "Wicked Wizboars": LocationData(BASE_LOCATION_ID + 146, "Crescent Road"),

    # Luvora Garden quests (lv 13-18)
    "Beckoning Foes": LocationData(BASE_LOCATION_ID + 150, "Luvora Garden"),
    "Blossom of Life": LocationData(BASE_LOCATION_ID + 151, "Luvora Garden"),
    "Consumed Madness": LocationData(BASE_LOCATION_ID + 152, "Catacombs Floor 2"),
    "Eradicating the Undead": LocationData(BASE_LOCATION_ID + 153, "Catacombs Floor 2"),
    "Makin' a Golem Chestpiece": LocationData(BASE_LOCATION_ID + 154, "Menu"),
    "Summore' Golem Chestpieces": LocationData(BASE_LOCATION_ID + 155, "Menu"),
    "Whatta' Rush!": LocationData(BASE_LOCATION_ID + 156, "Luvora Garden"),

    # Crescent Keep quests (lv 8-13)
    "Finding Ammagon": LocationData(BASE_LOCATION_ID + 160, "Crescent Keep"),
    "Reviling the Rageboars": LocationData(BASE_LOCATION_ID + 161, "Bularr Fortress"),
    "Reviling More Rageboars": LocationData(BASE_LOCATION_ID + 162, "Bularr Fortress"),

    # Tull Enclave quests (lv 13-16)
    "Makin' a Ragespear": LocationData(BASE_LOCATION_ID + 165, "Menu"),
    "Makin' More Ragespears": LocationData(BASE_LOCATION_ID + 166, "Menu"),
    "Purging the Grove": LocationData(BASE_LOCATION_ID + 167, "Tull Enclave"),
    "Searching for the Grove": LocationData(BASE_LOCATION_ID + 168, "Tull Enclave"),
    "Tethering Grove": LocationData(BASE_LOCATION_ID + 169, "Crescent Keep"),
    "Up and Over It": LocationData(BASE_LOCATION_ID + 170, "Crescent Keep"),

    # Bularr Fortress quests (lv 17-26)
    "Makin' a Monolith Chestpiece": LocationData(BASE_LOCATION_ID + 175, "Grove Floor 1"),
    "Summore' Monolith Chestpieces": LocationData(BASE_LOCATION_ID + 176, "Grove Floor 1"),

    # Additional combat quest
    "Facing Foes": LocationData(BASE_LOCATION_ID + 180, "Grove Floor 1"),

    # Crescent Grove Floor 1 quests (lv 15-20)
    "Cleansing the Grove": LocationData(BASE_LOCATION_ID + 200, "Grove Floor 1"),
    "Hell In The Grove": LocationData(BASE_LOCATION_ID + 201, "Grove Floor 1"),
    "Spiraling In The Grove": LocationData(BASE_LOCATION_ID + 202, "Grove Floor 1"),
    "Makin' a Firebreath Blade": LocationData(BASE_LOCATION_ID + 203, "Grove Floor 2"),
    "Nulversa Magica": LocationData(BASE_LOCATION_ID + 204, "Grove Floor 2"),
    "Nulversa Viscera": LocationData(BASE_LOCATION_ID + 205, "Grove Floor 2"),
    "Nulversa, Greenveras!": LocationData(BASE_LOCATION_ID + 206, "Grove Floor 2"),
    "Summore' Firebreath Blades": LocationData(BASE_LOCATION_ID + 207, "Grove Floor 2"),

    # Galius-related quest (Bularr Fortress, lv 17-26)
    "The Gall of Galius": LocationData(BASE_LOCATION_ID + 220, "Bularr Fortress"),

    # High-level crafting quests (Bularr Fortress area)
    "Makin' a Follycannon": LocationData(BASE_LOCATION_ID + 240, "Bularr Fortress"),
    "Makin' More Follycannons": LocationData(BASE_LOCATION_ID + 241, "Bularr Fortress"),
    "The Glyphik Booklet": LocationData(BASE_LOCATION_ID + 242, "Bularr Fortress"),

    # Shop Sanity - 50 total locations (all merchants in Sanctum hub)
    "Sally Shop Purchase 1": LocationData(591300, "Menu"),
    "Sally Shop Purchase 2": LocationData(591301, "Menu"),
    "Sally Shop Purchase 3": LocationData(591302, "Menu"),
    "Sally Shop Purchase 4": LocationData(591303, "Menu"),
    "Sally Shop Purchase 5": LocationData(591304, "Menu"),

    "Skrit Shop Purchase 1": LocationData(591305, "Menu"),
    "Skrit Shop Purchase 2": LocationData(591306, "Menu"),
    "Skrit Shop Purchase 3": LocationData(591307, "Menu"),
    "Skrit Shop Purchase 4": LocationData(591308, "Menu"),
    "Skrit Shop Purchase 5": LocationData(591309, "Menu"),

    "Frankie Shop Purchase 1": LocationData(591310, "Menu"),
    "Frankie Shop Purchase 2": LocationData(591311, "Menu"),
    "Frankie Shop Purchase 3": LocationData(591312, "Menu"),
    "Frankie Shop Purchase 4": LocationData(591313, "Menu"),
    "Frankie Shop Purchase 5": LocationData(591314, "Menu"),

    "Ruka Shop Purchase 1": LocationData(591315, "Menu"),
    "Ruka Shop Purchase 2": LocationData(591316, "Menu"),
    "Ruka Shop Purchase 3": LocationData(591317, "Menu"),
    "Ruka Shop Purchase 4": LocationData(591318, "Menu"),
    "Ruka Shop Purchase 5": LocationData(591319, "Menu"),

    "Fisher Shop Purchase 1": LocationData(591320, "Menu"),
    "Fisher Shop Purchase 2": LocationData(591321, "Menu"),
    "Fisher Shop Purchase 3": LocationData(591322, "Menu"),
    "Fisher Shop Purchase 4": LocationData(591323, "Menu"),
    "Fisher Shop Purchase 5": LocationData(591324, "Menu"),

    "Dye Merchant Shop Purchase 1": LocationData(591325, "Menu"),
    "Dye Merchant Shop Purchase 2": LocationData(591326, "Menu"),
    "Dye Merchant Shop Purchase 3": LocationData(591327, "Menu"),
    "Dye Merchant Shop Purchase 4": LocationData(591328, "Menu"),
    "Dye Merchant Shop Purchase 5": LocationData(591329, "Menu"),

    "Tesh Shop Purchase 1": LocationData(591330, "Menu"),
    "Tesh Shop Purchase 2": LocationData(591331, "Menu"),
    "Tesh Shop Purchase 3": LocationData(591332, "Menu"),
    "Tesh Shop Purchase 4": LocationData(591333, "Menu"),
    "Tesh Shop Purchase 5": LocationData(591334, "Menu"),

    "Nesh Shop Purchase 1": LocationData(591335, "Menu"),
    "Nesh Shop Purchase 2": LocationData(591336, "Menu"),
    "Nesh Shop Purchase 3": LocationData(591337, "Menu"),
    "Nesh Shop Purchase 4": LocationData(591338, "Menu"),
    "Nesh Shop Purchase 5": LocationData(591339, "Menu"),

    "Cotoo Shop Purchase 1": LocationData(591340, "Menu"),
    "Cotoo Shop Purchase 2": LocationData(591341, "Menu"),
    "Cotoo Shop Purchase 3": LocationData(591342, "Menu"),
    "Cotoo Shop Purchase 4": LocationData(591343, "Menu"),
    "Cotoo Shop Purchase 5": LocationData(591344, "Menu"),

    "Rikko Shop Purchase 1": LocationData(591345, "Menu"),
    "Rikko Shop Purchase 2": LocationData(591346, "Menu"),
    "Rikko Shop Purchase 3": LocationData(591347, "Menu"),
    "Rikko Shop Purchase 4": LocationData(591348, "Menu"),
    "Rikko Shop Purchase 5": LocationData(591349, "Menu"),

    # Fishing Level milestones (591400-591408)
    "Fishing Level 2": LocationData(591400, "Menu"),
    "Fishing Level 3": LocationData(591401, "Menu"),
    "Fishing Level 4": LocationData(591402, "Menu"),
    "Fishing Level 5": LocationData(591403, "Menu"),
    "Fishing Level 6": LocationData(591404, "Menu"),
    "Fishing Level 7": LocationData(591405, "Menu"),
    "Fishing Level 8": LocationData(591406, "Menu"),
    "Fishing Level 9": LocationData(591407, "Menu"),
    "Fishing Level 10": LocationData(591408, "Menu"),

    # Mining Level milestones (591409-591417)
    "Mining Level 2": LocationData(591409, "Menu"),
    "Mining Level 3": LocationData(591410, "Menu"),
    "Mining Level 4": LocationData(591411, "Menu"),
    "Mining Level 5": LocationData(591412, "Menu"),
    "Mining Level 6": LocationData(591413, "Menu"),
    "Mining Level 7": LocationData(591414, "Menu"),
    "Mining Level 8": LocationData(591415, "Menu"),
    "Mining Level 9": LocationData(591416, "Menu"),
    "Mining Level 10": LocationData(591417, "Menu"),

    # Achievement Triggers (591500+)
    "Smack Dat Azz": LocationData(591500, "Menu"),
}


class ATLYSSLocation(Location):
    """Custom location class for ATLYSS"""
    game: str = "ATLYSS"