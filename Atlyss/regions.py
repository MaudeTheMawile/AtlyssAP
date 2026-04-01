from typing import Dict, List
from BaseClasses import Region, Entrance, CollectionState, ItemClassification, Location
from .locations import location_table, ATLYSSLocation
from .items import ATLYSSItem


# === AREA LEVEL DATA (from Atlyss Logic Sheets spreadsheet) ===
# Each area has a minimum level (recommended to enter) and maximum level
# (highest you can grind to from enemies in that area).
# This data drives both region entrance rules and level milestone accessibility.
AREA_LEVEL_DATA = {
    #                     min  max
    "Outer Sanctum":      (1,   4),
    "Arcwood Pass":       (1,   4),
    "Effold Terrace":     (1,  10),
    "Catacombs Floor 1":  (1,   6),
    "Catacombs Floor 2":  (6,  12),
    "Catacombs Floor 3":  (12, 18),
    "Tull Valley":        (8,  14),
    "Crescent Road":      (8,  14),
    "Crescent Keep":      (8,  13),
    "Tull Enclave":       (13, 16),
    "Luvora Garden":      (13, 18),
    "Grove Floor 1":      (15, 20),
    "Grove Floor 2":      (20, 25),
    "Bularr Fortress":    (17, 26),
}


def can_grind_to_level(state: CollectionState, level: int, player: int) -> bool:
    """Check if the player has access to ANY area where enemies go high enough
    to grind to the given level. Based on max enemy levels from the spreadsheet.
    
    This is used for level EVENT locations so the AP solver knows you need
    access to appropriate areas before you can reach higher levels.
    Without this, 'Reach Level 32' would be sphere 0 (always accessible).
    """
    for area_name, (area_min, area_max) in AREA_LEVEL_DATA.items():
        if area_max >= level:
            if state.can_reach_region(area_name, player):
                return True
    
    # Levels beyond any area's max (28-32) require access to the highest areas
    # and heavy grinding. Allow if player can reach any lv 25+ area.
    if level > 26:
        return (state.can_reach_region("Grove Floor 2", player) or
                state.can_reach_region("Bularr Fortress", player))
    
    return False


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
    menu = create_region(world, "Menu", [
        # Tutorial/Story Quests (Sanctum hub)
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
        "Mining Level 2",
        "Mining Level 3",
        "Mining Level 4",
        "Mining Level 5",
        "Mining Level 6",
        "Mining Level 7",
        "Mining Level 8",
        "Mining Level 9",
        "Mining Level 10",
        
        # Shop Sanity (all merchants in Sanctum hub)
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
        "Frankie Shop Purchase 1",
        "Frankie Shop Purchase 2",
        "Frankie Shop Purchase 3",
        "Frankie Shop Purchase 4",
        "Frankie Shop Purchase 5",
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

        # Achievement Triggers (Sanctum hub)
        "Smack Dat Azz",
    ])
    
    # Outer Sanctum (lv 1-4, from Sanctum)
    outer_sanctum = create_region(world, "Outer Sanctum", [
        "Call of Fury",
        "Cold Shoulder",
        "Focusin' in",
    ])
    
    # Arcwood Pass (lv 1-4, from Outer Sanctum)
    arcwood_pass = create_region(world, "Arcwood Pass", [
        "Amberite Ingots",
        "Ancient Beings",
    ])
    
    # Effold Terrace (lv 1-10, from Outer Sanctum)
    # Has Slime Diva boss at level 10
    effold_terrace = create_region(world, "Effold Terrace", [
        "Defeat Slime Diva",
        "Cleaning Terrace",
    ])
    
    # SPLIT: Catacombs now has 3 separate floor regions
    # Floor 1 (lv 1-6, from Arcwood Pass)
    catacombs_f1 = create_region(world, "Catacombs Floor 1", [
        "Dense Ingots",
        "Night Spirits",
        "Ridding Slimes",
        "Killing Tomb",
        "Ghostly Goods",
        "Summore' Spectral Powder!",
        "Purging the Undead",
        "Rattlecage Rage",
    ])
    
    # Floor 2 (lv 6-12, from Floor 1 + Level 6)
    # Has Lord Zuulneruda boss
    catacombs_f2 = create_region(world, "Catacombs Floor 2", [
        "Defeat Lord Zuulneruda",
        "Consumed Madness",
        "Eradicating the Undead",
    ])
    
    # Floor 3 (lv 12-18, from Floor 2 + Level 12)
    # Has Lord Kaluuz boss
    catacombs_f3 = create_region(world, "Catacombs Floor 3", [
        "Defeat Lord Kaluuz",
    ])
    
    # Tull Valley (lv 8-14, from Outer Sanctum + Level 8)
    tull_valley = create_region(world, "Tull Valley", [
        "Sapphite Ingots",
        "Huntin' Hogs",
    ])
    
    # Crescent Road (lv 8-14, from Arcwood Pass + Level 8)
    crescent_road = create_region(world, "Crescent Road", [
        "Devious Pact",
        "Disciple of Magic",
        "Mastery of Dexterity",
        "Mastery of Mind",
        "Mastery of Strength",
        "Strength and Honor",
        "Wicked Wizboars",
    ])
    
    # Luvora Garden (lv 13-18, from Crescent Road + Level 13)
    luvora_garden = create_region(world, "Luvora Garden", [
        "Beckoning Foes",
        "Blossom of Life",
        "Whatta' Rush!",
    ])
    
    # Crescent Keep (lv 8-13, from Crescent Road + Level 8)
    crescent_keep = create_region(world, "Crescent Keep", [
        "Finding Ammagon",
        "Tethering Grove",
        "Up and Over It",
    ])
    
    # Tull Enclave (lv 13-16, from Tull Valley + Level 13)
    tull_enclave = create_region(world, "Tull Enclave", [
        "Searching for the Grove",
        "Purging the Grove",
    ])
    
    # SPLIT: Grove now has 2 separate floor regions
    # Grove Floor 1 / Crescent Grove lvl 1 (lv 15-20, from Crescent Keep + Level 15)
    # Has Colossus boss
    grove_f1 = create_region(world, "Grove Floor 1", [
        "Defeat Colossus",
        "Cleansing the Grove",
        "Spiraling In The Grove",
        "Hell In The Grove",
        "Makin' a Monolith Chestpiece",
        "Summore' Monolith Chestpieces",
        "Facing Foes",
    ])
    
    # Grove Floor 2 / Crescent Grove lvl 2 (lv 20-25, from Floor 1 + Level 20)
    # Has Valdur boss and Firebreath/Nulversa quests
    grove_f2 = create_region(world, "Grove Floor 2", [
        "Defeat Valdur",
        "Makin' a Firebreath Blade",
        "Summore' Firebreath Blades",
        "Nulversa Magica",
        "Nulversa Viscera",
        "Nulversa, Greenveras!",
    ])
    
    # Bularr Fortress (lv 17-26, from Tull Enclave + Level 17)
    # Has Galius boss
    bularr_fortress = create_region(world, "Bularr Fortress", [
        "Defeat Galius",
        "The Gall of Galius",
        "Reviling the Rageboars",
        "Reviling More Rageboars",
        "Makin' a Follycannon",
        "Makin' More Follycannons",
        "The Glyphik Booklet",
    ])
    
    # Add all regions to multiworld
    world.multiworld.regions.extend([
        menu,
        outer_sanctum,
        arcwood_pass,
        effold_terrace,
        catacombs_f1,
        catacombs_f2,
        catacombs_f3,
        tull_valley,
        crescent_road,
        luvora_garden,
        crescent_keep,
        tull_enclave,
        grove_f1,
        grove_f2,
        bularr_fortress,
    ])
    
    # Place event items at level milestone locations so has_level() works
    place_level_event_items(world)
    
    # --- PORTAL CONNECTIONS ---
    # The portal sequence matches the C# plugin's _progressivePortalOrder:
    # 1.Outer Sanctum  2.Arcwood Pass  3.Catacombs  4.Effold Terrace
    # 5.Tull Valley  6.Crescent Road  7.Luvora Garden  8.Crescent Keep
    # 9.Tull Enclave  10.Grove  11.Bularr Fortress
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
        
        # Sanctum hub -> Outer Sanctum (lv min 1, no level gate)
        menu.connect(
            outer_sanctum,
            "Enter Outer Sanctum",
            lambda state: state.has("Outer Sanctum Portal", player)
        )
        
        # Outer Sanctum branches
        outer_sanctum.connect(
            effold_terrace,
            "Enter Effold Terrace",
            lambda state: state.has("Effold Terrace Portal", player)
            # lv min 1, no level gate needed
        )
        outer_sanctum.connect(
            arcwood_pass,
            "Enter Arcwood Pass",
            lambda state: state.has("Arcwood Pass Portal", player)
            # lv min 1, no level gate needed
        )
        outer_sanctum.connect(
            tull_valley,
            "Enter Tull Valley",
            lambda state: (state.has("Tull Valley Portal", player) and
                          state.has("Reach Level 8", player))
        )
        
        # Arcwood Pass branches
        arcwood_pass.connect(
            catacombs_f1,
            "Enter Catacombs Floor 1",
            lambda state: state.has("Catacombs Portal", player)
            # lv min 1, no level gate needed
        )
        arcwood_pass.connect(
            crescent_road,
            "Enter Crescent Road",
            lambda state: (state.has("Crescent Road Portal", player) and
                          state.has("Reach Level 8", player))
        )
        
        # Catacombs sub-floor connections (from parent floor, not from menu)
        catacombs_f1.connect(
            catacombs_f2,
            "Enter Catacombs Floor 2",
            lambda state: state.has("Reach Level 6", player)
        )
        catacombs_f2.connect(
            catacombs_f3,
            "Enter Catacombs Floor 3",
            lambda state: state.has("Reach Level 12", player)
        )
        
        # Crescent Road branches
        crescent_road.connect(
            luvora_garden,
            "Enter Luvora Garden",
            lambda state: state.has("Reach Level 12", player)
            # Luvora Garden is always accessible from Crescent Road at level 12 (no portal needed)
        )
        crescent_road.connect(
            crescent_keep,
            "Enter Crescent Keep",
            lambda state: state.has("Crescent Keep Portal", player)
            # lv min 8, but Crescent Road already requires 8
        )
        
        # Tull Valley -> Tull Enclave
        tull_valley.connect(
            tull_enclave,
            "Enter Tull Enclave",
            lambda state: (state.has("Tull Enclave Portal", player) and
                          state.has("Reach Level 12", player))
        )
        
        # Crescent Keep -> Grove Floor 1
        crescent_keep.connect(
            grove_f1,
            "Enter Grove Floor 1",
            lambda state: (state.has("Grove Portal", player) and
                          state.has("Reach Level 14", player))
        )
        
        # Grove sub-floor connection
        grove_f1.connect(
            grove_f2,
            "Enter Grove Floor 2",
            lambda state: state.has("Reach Level 20", player)
        )
        
        # Tull Enclave -> Bularr Fortress
        tull_enclave.connect(
            bularr_fortress,
            "Enter Bularr Fortress",
            lambda state: (state.has("Bularr Fortress Portal", player) and
                          state.has("Reach Level 16", player))
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
        menu.connect(
            outer_sanctum,
            "Enter Outer Sanctum",
            lambda state: state.has("Progressive Portal", player, 1)
        )
        
        # Portal 2: Arcwood Pass (lv min 1)
        menu.connect(
            arcwood_pass,
            "Enter Arcwood Pass",
            lambda state: state.has("Progressive Portal", player, 2)
        )
        
        # Portal 3: Catacombs Floor 1 (lv min 1)
        menu.connect(
            catacombs_f1,
            "Enter Catacombs Floor 1",
            lambda state: state.has("Progressive Portal", player, 3)
        )
        
        # Portal 4: Effold Terrace (lv min 1)
        menu.connect(
            effold_terrace,
            "Enter Effold Terrace",
            lambda state: state.has("Progressive Portal", player, 4)
        )
        
        # Portal 5: Tull Valley (lv min 8)
        menu.connect(
            tull_valley,
            "Enter Tull Valley",
            lambda state: (state.has("Progressive Portal", player, 5) and
                          state.has("Reach Level 8", player))
        )
        
        # Portal 6: Crescent Road (lv min 8)
        menu.connect(
            crescent_road,
            "Enter Crescent Road",
            lambda state: (state.has("Progressive Portal", player, 6) and
                          state.has("Reach Level 8", player))
        )
        
        # Portal 7: Luvora Garden (lv min 12) - no portal needed, just level gate
        menu.connect(
            luvora_garden,
            "Enter Luvora Garden",
            lambda state: (state.has("Progressive Portal", player, 6) and
                          state.has("Reach Level 12", player))
            # Shares portal 6 (Crescent Road) since Luvora branches off it
        )
        
        # Portal 7: Crescent Keep (lv min 8)
        menu.connect(
            crescent_keep,
            "Enter Crescent Keep",
            lambda state: (state.has("Progressive Portal", player, 7) and
                          state.has("Reach Level 8", player))
        )
        
        # Portal 8: Tull Enclave (lv min 13)
        menu.connect(
            tull_enclave,
            "Enter Tull Enclave",
            lambda state: (state.has("Progressive Portal", player, 8) and
                          state.has("Reach Level 12", player))
        )
        
        # Portal 9: Grove Floor 1 (lv min 15)
        menu.connect(
            grove_f1,
            "Enter Grove Floor 1",
            lambda state: (state.has("Progressive Portal", player, 9) and
                          state.has("Reach Level 14", player))
        )
        
        # Portal 10: Bularr Fortress (lv min 17)
        menu.connect(
            bularr_fortress,
            "Enter Bularr Fortress",
            lambda state: (state.has("Progressive Portal", player, 10) and
                          state.has("Reach Level 16", player))
        )
        
        # --- Sub-floor connections (from parent floor, level-gated) ---
        # These don't need portal items, just access to the previous floor + level
        catacombs_f1.connect(
            catacombs_f2,
            "Enter Catacombs Floor 2",
            lambda state: state.has("Reach Level 6", player)
        )
        catacombs_f2.connect(
            catacombs_f3,
            "Enter Catacombs Floor 3",
            lambda state: state.has("Reach Level 12", player)
        )
        grove_f1.connect(
            grove_f2,
            "Enter Grove Floor 2",
            lambda state: state.has("Reach Level 20", player)
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
    
    for level in range(2, 33, 2):  # 2, 4, 6, ... 32 = 16 milestones
        event_loc_name = f"Event: Reach Level {level}"
        item_name = f"Reach Level {level}"
        
        # Create event location (code=None = internal to AP logic, never sent to client)
        event_location = Location(player, event_loc_name, None, menu_region)
        
        # ADDED: Require access to an area where you can grind to this level.
        # This is the key fix: it prevents level milestones from being sphere 0.
        # The previous level chain is also required (level 8 needs level 6 first).
        if level == 2:
            # Level 2 just requires access to Outer Sanctum (first area with enemies)
            event_location.access_rule = lambda state: can_grind_to_level(state, 2, player)
        else:
            prev_level = level - 2
            event_location.access_rule = (
                lambda state, lv=level, plv=prev_level: (
                    state.has(f"Reach Level {plv}", player) and
                    can_grind_to_level(state, lv, player)
                )
            )
        
        menu_region.locations.append(event_location)
        
        # Create event item and lock it to the event location
        event_item = ATLYSSItem(item_name, ItemClassification.progression, None, player)
        event_location.place_locked_item(event_item)


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