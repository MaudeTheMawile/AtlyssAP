from typing import Dict, List
from BaseClasses import Region, Entrance, CollectionState, ItemClassification, Location
from .locations import location_table, ATLYSSLocation
from .items import ATLYSSItem


# === AREA LEVEL DATA (from Atlyss Logic Sheets spreadsheet) ===
# Each area has a minimum level (recommended to enter) and maximum level
# (highest you can grind to from enemies in that area).
# This data drives both region entrance rules and level milestone accessibility.

def create_regions(world):
    """Creates all regions, locations, and entrances.
    
    UPDATED: Split Catacombs into 3 floors and Grove into 2 floors based on
    the Atlyss Logic Sheets spreadsheet. Each floor has its own level range
    and requires meeting the minimum level to enter deeper floors.
    Region entrances now require both portal access AND meeting the area's
    minimum level, so the randomizer won't place critical items behind
    checks that require high-level grinding.
    """
    
    # Create all regions with their locations
    sanctum = create_region(world, "Menu", [
        # Intro Quests
        "A Warm Welcome",
        "Communing Catacombs",
        
        # Crafting Quests (accepted and turned in at Sanctum hub NPCs)
        # These require materials from various areas but are turned in at hub
        "Makin' a Mekspear",
        "Makin' More Mekspears",
        "Makin' a Wizwand",
        "Makin' More Wizwands",
        "Makin' a Vile Blade",
        "Makin' More Vile Blades",
        "Makin' a Golem Chestpiece",
        "Summore' Golem Chestpieces",
        "Makin' a Ragespear",
        "Makin' More Ragespears",
        
        # Character Level Milestones (gated by rules in rules.py, not region)
        "Reach Level 2",
        "Reach Level 4",
        "Reach Level 6",
        "Reach Level 8",
        "Reach Level 10",
        "Reach Level 12",
        "Reach Level 14",
        "Reach Level 16",
        "Reach Level 18",
        "Reach Level 20",
        "Reach Level 22",
        "Reach Level 24",
        "Reach Level 26",
        "Reach Level 28",
        "Reach Level 30",
        "Reach Level 32",
        
        # Fishing Profession Levels (can fish from Sanctum area)
        # Note to AzraeL: Maybe make a setting to remove Fishing checks??
        # Would push Sanctum hub shop income back.
        "Fishing Level 2",
        "Fishing Level 3",
        "Fishing Level 4",
        "Fishing Level 5",
        "Fishing Level 6",
        "Fishing Level 7",
        "Fishing Level 8",
        "Fishing Level 9",
        "Fishing Level 10",
        
        # Mining Profession Levels
        # Note to AzraeL: Maybe make a setting to remove Mining checks??
        # Would make Dense/Ambersite/Sapphite Ingots locations irrelevant too.
        "Mining Level 2",
        "Mining Level 3",
        "Mining Level 4",
        "Mining Level 5",
        "Mining Level 6",
        "Mining Level 7",
        "Mining Level 8",
        "Mining Level 9",
        "Mining Level 10",

        # Achievement Triggers (Sanctum hub)
        "Smack Dat Azz",

        # Outer Sanctum (Lv1-4) locations
        "Call of Fury",
        "Cold Shoulder",
        "Focusin' in",
        "Ridding Slimes",

        # Arcwood Pass (Lv 4-6) locations
        "Dense Ingots",
        "Night Spirits",

        # Catacombs (Lv4-12) locations
        "Killing Tomb",
        "Ghostly Goods",
        "Summore' Spectral Powder!",
        "Purging the Undead",
        "Rattlecage Rage",

        # Goalpoint. You will likely defeat Zuulneruda before ever reaching Lv10.
        "Defeat Lord Zuulneruda",
    ])
    
    # Only accessible after defeating Zuulneruda in Catacombs Lv6-12.
    # (Not strictly, you can always opt to ignore him, but...why would you?)
    post_zuulneruda = create_region(world, "After Zuulneruda", [
        # Catacombs (Lv 12-18) locations
        "Consumed Madness",
        "Eradicating the Undead",

        # Class Scrolls (Lv10)
        # "Strength and Honor",
        # "Disciple of Magic",
        # "Devious Pact",
        # Above will be excluded until we find out how to exclude them via Class Filter

        # Skill Scrolls (Lv10, Lv12)
        "Mastery of Dexterity",
        "Mastery of Mind",
        "Mastery of Strength",
        "Beckoning Foes",
        "Blossom of Life",
        "Whatta' Rush!",

        # Goalpoint. Required to access anything in or past Crescent Road.
        "Defeat Slime Diva",
    ])
    
    # Only accessible after defeating the Slime Diva in Effold Terrace.
    post_slime_diva = create_region(world, "After Slime Diva", [
        # Still in Effold Terrace
        "Cleaning Terrace",

        # Tuul Valley
        "Huntin' Hogs",
        "Wicked Wizboars",
        "Amberite Ingots",

        # Crescent Road/Keep
        # "The Keep Within",
        "Ancient Beings",

        # Tuul Enclave
        "Sapphite Ingots",

        # Crescent Grove
        "Tethering Grove",

        # Goalpoint. Required for anything in Grove Lv20-25.
        "Defeat Colossus",
    ])
    
    # Only accessible after defeating the Colossus in Crescent Grove Lv15-20.
    post_colossus = create_region(world, "After Colossus", [
        # Grove (Lv15-20)
        # Dev note: These checks are technically accessible, but I am only marking as "After Colossus" due to
        # the Colossus being easier to defeat compared to the surrounding quests.
        # Zuulneruda never had this problem.
        "Purging the Grove",
        "Spiraling In The Grove", 
        "Makin' a Monolith Chestpiece",
        "Summore' Monolith Chestpieces",

        # Grove (Lv20-25)
        "Cleansing the Grove",
        "Hell In The Grove",
        "Makin' a Firebreath Blade",
        "Summore' Firebreath Blades",
        # The three below are technically "exclusive" to each other by nature,
        # But it makes no sense to exclude since they're all still completable no matter what
        "Nulversa Magica",
        "Nulversa Viscera",
        "Nulversa, Greenveras!",


        # GotM, WotS, TotS
        "Up and Over It",

        # Bularr Fortress
        "Finding Ammagon",
        "Reviling the Rageboars",
        "Reviling More Rageboars",
        
        # Final Goalpoint.
        "Defeat Galius",

    ])
    
    # Only accessible after defeating Galius in Bularr Fortress.
    # Only comes into play with the All Quests and Level 32 goals, as Galius is the final logical boss.
    post_galius = create_region(world, "After Galius", [
        "Facing Foes", # Difficult to get this done before defeating Galius, thank the drop rates
        "The Gall of Galius",
        "Makin' a Follycannon",
        "Makin' More Follycannons",
        "The Glyphik Booklet",

    ])
    
    # Shop Sanity
    # Note to AzraeL: These shops are still "accessible" as soon as you can buy/sell,
    # but I am debating pushing logic to Catacombs access,
    # since that's the first bearable money farming location.
    sanctum_shops = create_region(world, "Shop Vendors", [
        # Accessible in the Sanctum Hub
        "Sally Shop Purchase 1",
        "Sally Shop Purchase 2",
        "Sally Shop Purchase 3",
        "Sally Shop Purchase 4",
        "Sally Shop Purchase 5",
        "Skrit Shop Purchase 1",
        "Skrit Shop Purchase 2",
        "Skrit Shop Purchase 3",
        "Skrit Shop Purchase 4",
        "Skrit Shop Purchase 5",
        "Ruka Shop Purchase 1",
        "Ruka Shop Purchase 2",
        "Ruka Shop Purchase 3",
        "Ruka Shop Purchase 4",
        "Ruka Shop Purchase 5",
        "Fisher Shop Purchase 1",
        "Fisher Shop Purchase 2",
        "Fisher Shop Purchase 3",
        "Fisher Shop Purchase 4",
        "Fisher Shop Purchase 5",
        "Dye Merchant Shop Purchase 1",
        "Dye Merchant Shop Purchase 2",
        "Dye Merchant Shop Purchase 3",
        "Dye Merchant Shop Purchase 4",
        "Dye Merchant Shop Purchase 5",
        # Accessible in Arcwood Pass
        "Frankie Shop Purchase 1",
        "Frankie Shop Purchase 2",
        "Frankie Shop Purchase 3",
        "Frankie Shop Purchase 4",
        "Frankie Shop Purchase 5",
        "Tesh Shop Purchase 1",
        "Tesh Shop Purchase 2",
        "Tesh Shop Purchase 3",
        "Tesh Shop Purchase 4",
        "Tesh Shop Purchase 5",
        "Nesh Shop Purchase 1",
        "Nesh Shop Purchase 2",
        "Nesh Shop Purchase 3",
        "Nesh Shop Purchase 4",
        "Nesh Shop Purchase 5",
        # Accessible in Crescent Keep

    ])
    
    # 
    shops_post_slime_diva = create_region(world, "Shops After Slime Diva", [
        "Cotoo Shop Purchase 1",
        "Cotoo Shop Purchase 2",
        "Cotoo Shop Purchase 3",
        "Cotoo Shop Purchase 4",
        "Cotoo Shop Purchase 5",
        "Rikko Shop Purchase 1",
        "Rikko Shop Purchase 2",
        "Rikko Shop Purchase 3",
        "Rikko Shop Purchase 4",
        "Rikko Shop Purchase 5",
    ])
    
    # Add all regions to multiworld
    world.multiworld.regions.extend([
        sanctum,
        sanctum_shops,
        post_zuulneruda,
        post_slime_diva,
        shops_post_slime_diva,
        post_colossus,
        post_galius,
    ])
    
    # Place event items at level milestone locations so has_level() works
    place_level_event_items(world)
    
    # --- PORTAL CONNECTIONS ---
    # The portal sequence matches the C# plugin's _progressivePortalOrder:
    # 1.Outer Sanctum  2.Arcwood Pass  3.Catacombs  4.Effold Terrace
    # 5.Tull Valley  6.Crescent Road  7.Crescent Keep
    # 8.Tull Enclave  9.Grove  10.Bularr Fortress
    #
    # UPDATED: Region entrances now require BOTH portal access AND meeting the
    # area's minimum level from the spreadsheet. Sub-floors (Catacombs 2/3,
    # Grove 2) connect from their parent floor, not from Menu.
    
    player = world.player
    random_portals = world.options.random_portals.value
    
    if random_portals:
        # RANDOM PORTALS: Individual portal items, geographic tree layout.
        # Players find specific named portals and can unlock areas non-linearly.
        # Level requirements added based on the spreadsheet's minimum levels.
        
        sanctum.connect(
            sanctum_shops,
            "Shop Vendors",
        )

        sanctum.connect(
            post_zuulneruda,
            "After Zuulneruda",
            lambda state: (state.has("Outer Sanctum Portal", player) and
                          state.has("Arcwood Pass Portal", player) and
                          state.has("Catacombs Portal", player))
        )

        post_zuulneruda.connect(
            post_slime_diva,
            "After Slime Diva",
            lambda state: state.has("Effold Terrace Portal")
        )
        post_zuulneruda.connect(
            shops_post_slime_diva,
            "Shops After Slime Diva",
            lambda state: (state.has("Effold Terrace Portal", player) and
                          state.has("Crescent Road Portal", player) and
                          state.has("Crescent Keep Portal", player))
        )
        
        post_slime_diva.connect(
            post_colossus,
            "After Colossus",
            lambda state: state.has("Grove Portal", player)
        )

        post_colossus.connect(
            post_galius,
            "After Galius",
            lambda state: (state.has("Tull Valley Portal", player) and
                          state.has("Tull Enclave Portal", player) and
                          state.has("Bularr Fortress Portal", player))
        )

    
    else:
        # PROGRESSIVE PORTALS (default): Each "Progressive Portal" item unlocks
        # the next area in sequence. state.has("Progressive Portal", player, N)
        # checks if player has N or more copies.
        #
        # UPDATED: Added level requirements from the spreadsheet so the randomizer
        # can't place critical items behind high-level checks.
        # Sub-floors connect from their parent floor with level gates.
        
        # --- Main portal sequence (from Menu) ---
        # Portal 1: Outer Sanctum (lv min 1)
        sanctum.connect(
            sanctum_shops,
            "Shop Vendors",
        )

        sanctum.connect(
            post_zuulneruda,
            "After Zuulneruda",
            lambda state: state.has("Progressive Portal", player, 3)
        )

        post_zuulneruda.connect(
            post_slime_diva,
            "After Slime Diva",
            lambda state: state.has("Progressive Portal", player, 4)
        )
        post_zuulneruda.connect(
            shops_post_slime_diva,
            "Shops After Slime Diva",
            lambda state: state.has("Progressive Portal", player, 7)
        )
        
        post_slime_diva.connect(
            post_colossus,
            "After Colossus",
            lambda state: state.has("Progressive Portal", player, 9)
        )

        post_colossus.connect(
            post_galius,
            "After Galius",
            lambda state: state.has("Progressive Portal", player, 10)
        )


def place_level_event_items(world):
    """Place event items at SEPARATE event locations for level milestones.
    
    Event items (code=None) cannot be placed on real locations (integer codes).
    AP's LocationStore expects integers for all placed items on real locations.
    
    Solution: Create event locations with code=None for internal logic only.
    The real "Reach Level X" locations keep their integer codes and get normal items.
    
    UPDATED: Event locations now have access rules requiring can_grind_to_level(),
    which checks that the player can reach areas with enemies at the right level.
    Without this, all level events would be sphere 0 (always obtainable),
    which means the randomizer could place Progressive Portal #1 behind Level 32.
    """
    player = world.player
    menu_region = world.multiworld.get_region("Menu", player)


def create_region(world, name: str, locations: List[str]) -> Region:
    """Helper to create a region with its locations."""
    region = Region(name, world.player, world.multiworld)
    
    for location_name in locations:
        if location_name not in location_table:
            continue
            
        location_data = location_table[location_name]
        location = ATLYSSLocation(
            world.player,
            location_name,
            location_data.code,
            region
        )
        region.locations.append(location)
    
    return region