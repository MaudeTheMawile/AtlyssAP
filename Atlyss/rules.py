from worlds.generic.Rules import set_rule, add_rule, add_item_rule
from BaseClasses import CollectionState, ItemClassification
from .items import ATLYSSItem, item_table
from .locations import location_table


# ================================================================
# EQUIPMENT TIER SYSTEM
# Tier 1: Levels 1-5   (starter gear)
# Tier 2: Levels 6-10  (mid-early gear)
# Tier 3: Levels 11-15 (mid gear)
# Tier 4: Levels 16-20 (late-mid gear)
# Tier 5: Levels 21-26 (endgame gear)
# ================================================================

def level_to_max_tier(level: int) -> int:
    """Convert an effective access level to the maximum equipment tier allowed."""
    if level <= 5:
        return 1
    if level <= 10:
        return 2
    if level <= 15:
        return 3
    if level <= 20:
        return 4
    return 5


# Max equipment tier for each non-Menu region, based on area max enemy level.
# e.g. Effold Terrace has enemies up to lv 10, so tier 2 gear is appropriate.
REGION_MAX_TIER = {
    "Outer Sanctum": 1,       # enemies lv 1-4
    "Arcwood Pass": 1,        # enemies lv 1-4
    "Effold Terrace": 2,      # enemies lv 1-10
    "Catacombs Floor 1": 2,   # enemies lv 1-6
    "Catacombs Floor 2": 3,   # enemies lv 6-12
    "Catacombs Floor 3": 4,   # enemies lv 12-18
    "Tull Valley": 3,         # enemies lv 8-14
    "Crescent Road": 3,       # enemies lv 8-14
    "Crescent Keep": 3,       # enemies lv 8-13
    "Luvora Garden": 4,       # enemies lv 13-18
    "Tull Enclave": 4,        # enemies lv 13-16
    "Grove Floor 1": 4,       # enemies lv 15-20
    "Grove Floor 2": 5,       # enemies lv 20-25
    "Bularr Fortress": 5,     # enemies lv 17-26
}


def get_menu_location_effective_level(loc_name: str) -> int:
    """Get the effective access level for a Menu-region location.
    Used to determine the max equipment tier that can be placed there.
    Based on the level requirements defined in set_rules()."""
    
    # Level milestones — tier matches the level itself
    if loc_name.startswith("Reach Level "):
        return int(loc_name.split()[-1])
    
    # Fishing profession levels (from Profession table)
    # Sanctum (1-3), Arcwood Pass (3-6), Crescent Road (6-10)
    if loc_name.startswith("Fishing Level "):
        fl = int(loc_name.split()[-1])
        if fl <= 3:
            return 1      # Sanctum fishing, no area needed
        if fl <= 6:
            return 4      # needs Arcwood Pass
        return 8          # needs Crescent Road (lv 8 access)
    
    # Mining profession levels (from Profession table)
    # Arcwood/Effold (1-2), various (3), Tull/Keep (4-6), Enclave (7-10)
    if loc_name.startswith("Mining Level "):
        ml = int(loc_name.split()[-1])
        if ml <= 3:
            return 1      # early mining areas
        if ml <= 6:
            return 8      # needs Tull Valley or Crescent Keep (lv 8 access)
        return 12         # needs Tull Enclave (lv 12 access)
    
    # Shop tiers by merchant
    shop_merchant_levels = {
        "Sally": 1, "Skrit": 1, "Frankie": 1, "Ruka": 1,
        "Fisher": 1, "Dye Merchant": 1,
        "Tesh": 6, "Nesh": 6,
        "Cotoo": 15, "Rikko": 15,
    }
    for merchant, level in shop_merchant_levels.items():
        if loc_name.startswith(f"{merchant} Shop"):
            return level
    
    # Named quests/locations — effective level based on their rules
    quest_effective_levels = {
        # Tutorial
        "A Warm Welcome": 1,
        "Communing Catacombs": 1,
        
        # Multi-area quests (level from their rules)
        "Night Spirits": 1,
        "Ridding Slimes": 1,
        "Ghostly Goods": 1,
        "Summore' Spectral Powder!": 1,
        "Huntin' Hogs": 7,
        "Wicked Wizboars": 10,
        "Ancient Beings": 8,
        
        # Class quests
        "Call of Fury": 4,
        "Cold Shoulder": 4,
        "Focusin' in": 4,
        # "Devious Pact": 10,
        # "Disciple of Magic": 10,
        # "Strength and Honor": 10,
        "Mastery of Strength": 10,
        "Mastery of Dexterity": 10,
        "Mastery of Mind": 10,
        "Beckoning Foes": 12,
        "Whatta' Rush!": 12,
        
        # Mining turn-in quests
        "Dense Ingots": 1,
        "Amberite Ingots": 6,
        "Sapphite Ingots": 8,
        
        # Crafting quests (level from their rules)
        "Makin' a Mekspear": 7,
        "Makin' More Mekspears": 7,
        "Makin' a Wizwand": 10,
        "Makin' More Wizwands": 10,
        "Makin' a Vile Blade": 10,
        "Makin' More Vile Blades": 10,
        "Makin' a Golem Chestpiece": 12,
        "Summore' Golem Chestpieces": 12,
        "Makin' a Ragespear": 15,
        "Makin' More Ragespears": 15,
        "Makin' a Monolith Chestpiece": 16,
        "Summore' Monolith Chestpieces": 16,
        
        # Endgame
        "The Glyphik Booklet": 24,

        # Achievement triggers
        "Smack Dat Azz": 1,
    }
    
    return quest_effective_levels.get(loc_name, 1)


def set_equipment_item_rules(world):
    """Apply item_rules to all locations restricting equipment by tier.
    Only called when equipment_progression == 0 (Gated mode).
    
    Each location gets an item_rule that allows:
    - All items from other players (always OK in multiworld)
    - All non-equipment items from this game
    - Equipment items only if their tier <= the location's max tier
    """
    player = world.player
    
    for loc_name in location_table:
        loc_data = location_table[loc_name]
        region_name = loc_data.region
        
        # Determine max tier for this location
        if region_name == "Menu":
            effective_level = get_menu_location_effective_level(loc_name)
            max_tier = level_to_max_tier(effective_level)
        else:
            max_tier = REGION_MAX_TIER.get(region_name, 1)
        
        # Skip tier 5 locations — everything is allowed there
        if max_tier >= 5:
            continue
        
        # Add item_rule: only allow equipment up to this tier
        location = world.multiworld.get_location(loc_name, player)
        add_item_rule(location,
            lambda item, mt=max_tier, p=player: (
                item.player != p or                    # other players' items always OK
                item.name not in item_table or         # safety: unknown items OK
                item_table[item.name].tier is None or  # non-equipment always OK
                item_table[item.name].tier <= mt        # equipment must be <= max tier
            )
        )


def set_profession_junk_rules(world):
    """Restrict Fishing/Mining levels and high-level milestones to filler only.
    
    These are passive grinds that shouldn't gate important progression.
    Only filler-classified items (crowns, consumables, trade items) can
    be placed here. Other players' items are always allowed (multiworld).
    
    Covers: Fishing Level 2-10, Mining Level 2-10, Reach Level 28/30/32.
    """
    player = world.player
    
    # High level milestones that should be junk-only
    junk_level_milestones = {"Reach Level 28", "Reach Level 30", "Reach Level 32"}
    
    for loc_name in location_table:
        is_junk_loc = (
            loc_name.startswith("Fishing Level ") or
            loc_name.startswith("Mining Level ") or
            loc_name in junk_level_milestones
        )
        if not is_junk_loc:
            continue
        
        location = world.multiworld.get_location(loc_name, player)
        add_item_rule(location,
            lambda item, p=player: (
                item.player != p or                                        # other players' items always OK
                item.classification == ItemClassification.filler            # only filler from this game
            )
        )


def has_level(state: CollectionState, player: int, level: int) -> bool:
    """Check if player has reached a specific character level.
    Rounds down to nearest even milestone (2, 4, 6, ... 32)."""
    if level < 2:
        return True
    milestone = level if level % 2 == 0 else level - 1
    return state.has(f"Reach Level {milestone}", player)


def set_rules(world):
    """Set access rules for all locations.
    
    UPDATED v2: Full quest prerequisite chains, multi-area requirements,
    equipment tier gating via item_rules, profession level gating.
    """
    player = world.player
    equipment_progression = world.options.equipment_progression.value
    
    # ================================================================
    # EQUIPMENT TIER GATING (Gated mode only)
    # Restricts WHERE equipment items can be placed based on tier.
    # In Random mode (1), equipment can appear anywhere.
    # ================================================================
    if equipment_progression == 0:  # Gated
        set_equipment_item_rules(world)
    
    # ================================================================
    # PROFESSION LEVEL JUNK RULES
    # Fishing and Mining level checks only receive filler/junk items.
    # These are passive grinds, so no important items should be gated
    # behind them — only crowns, consumable packs, trade items, etc.
    # ================================================================
    set_profession_junk_rules(world)
    
    # ================================================================
    # LEVEL MILESTONE RULES
    # Gate real "Reach Level X" locations behind area access + chaining
    # ================================================================
    # Finish non-progressive regions later

    set_rule(world.multiworld.get_location("Reach Level 2", player),
            lambda state: (state.has("Outer Sanctum Portal", player) or
                          state.has("Progressive Portal", player, 1)))
    set_rule(world.multiworld.get_location("Reach Level 4", player),
            lambda state: (state.has("Outer Sanctum Portal", player) or
                          state.has("Progressive Portal", player, 1)))
    set_rule(world.multiworld.get_location("Reach Level 6", player),
            lambda state: (state.has("Outer Sanctum Portal", player) or
                          state.has("Progressive Portal", player, 2)))
    set_rule(world.multiworld.get_location("Reach Level 8", player),
            lambda state: (state.has("Outer Sanctum Portal", player) or
                          state.has("Progressive Portal", player, 3)))
    set_rule(world.multiworld.get_location("Reach Level 10", player),
            lambda state: (state.has("Outer Sanctum Portal", player) or
                          state.has("Progressive Portal", player, 3)))
    set_rule(world.multiworld.get_location("Reach Level 12", player),
            lambda state: (state.has("Outer Sanctum Portal", player) or
                          state.has("Progressive Portal", player, 3)))
    set_rule(world.multiworld.get_location("Reach Level 14", player),
            lambda state: (state.has("Outer Sanctum Portal", player) or
                          state.has("Progressive Portal", player, 4)))
    set_rule(world.multiworld.get_location("Reach Level 16", player),
            lambda state: (state.has("Outer Sanctum Portal", player) or
                          state.has("Progressive Portal", player, 7)))
    set_rule(world.multiworld.get_location("Reach Level 18", player),
            lambda state: (state.has("Outer Sanctum Portal", player) or
                          state.has("Progressive Portal", player, 7)))
    set_rule(world.multiworld.get_location("Reach Level 20", player),
            lambda state: (state.has("Outer Sanctum Portal", player) or
                          state.has("Progressive Portal", player, 9)))
    set_rule(world.multiworld.get_location("Reach Level 22", player),
            lambda state: (state.has("Outer Sanctum Portal", player) or
                          state.has("Progressive Portal", player, 9)))
    set_rule(world.multiworld.get_location("Reach Level 24", player),
            lambda state: (state.has("Outer Sanctum Portal", player) or
                          state.has("Progressive Portal", player, 9)))
    set_rule(world.multiworld.get_location("Reach Level 26", player),
            lambda state: (state.has("Outer Sanctum Portal", player) or
                          state.has("Progressive Portal", player, 10)))
    set_rule(world.multiworld.get_location("Reach Level 28", player),
            lambda state: (state.has("Outer Sanctum Portal", player) or
                          state.has("Progressive Portal", player, 10)))
    set_rule(world.multiworld.get_location("Reach Level 30", player),
            lambda state: (state.has("Outer Sanctum Portal", player) or
                          state.has("Progressive Portal", player, 10)))
    set_rule(world.multiworld.get_location("Reach Level 32", player),
            lambda state: (state.has("Outer Sanctum Portal", player) or
                          state.has("Progressive Portal", player, 10)))

    # ================================================================
    # TUTORIAL / STORY QUEST RULES
    # ================================================================
    # Communing Catacombs: requires A Warm Welcome
    set_rule(world.multiworld.get_location("Communing Catacombs", player),
            lambda state: ((state.has("Outer Sanctum Portal", player) and
                          state.has("Arcwood Pass Portal", player) and
                          state.has("Catacombs Portal", player)) or
                          state.has("Progressive Portal", player, 3)))
    
    # ================================================================
    # CLASS QUESTS (N/A area, level-gated only)
    # ================================================================
    set_rule(world.multiworld.get_location("Call of Fury", player),
            lambda state: (state.has("Outer Sanctum Portal", player) or
                          state.has("Progressive Portal", player, 1)))
    set_rule(world.multiworld.get_location("Cold Shoulder", player),
            lambda state: (state.has("Outer Sanctum Portal", player) or
                          state.has("Progressive Portal", player, 1)))
    set_rule(world.multiworld.get_location("Focusin' in", player),
            lambda state: (state.has("Outer Sanctum Portal", player) or
                          state.has("Progressive Portal", player, 1)))
    
    # ================================================================
    # MULTI-AREA KILL QUESTS
    # ================================================================
    set_rule(world.multiworld.get_location("Night Spirits", player),
            lambda state: ((state.has("Outer Sanctum Portal", player) and
                          state.has("Arcwood Pass Portal", player))or
                          state.has("Progressive Portal", player, 2)))
    
    set_rule(world.multiworld.get_location("Ridding Slimes", player),
            lambda state: (state.has("Outer Sanctum Portal", player) or
                          state.has("Progressive Portal", player, 1)))
    
    set_rule(world.multiworld.get_location("Ghostly Goods", player),
            lambda state: ((state.has("Outer Sanctum Portal", player) and
                          state.has("Arcwood Pass Portal", player) and
                          state.has("Catacombs Portal", player)) or
                          state.has("Progressive Portal", player, 3)))

    set_rule(world.multiworld.get_location("Killing Tomb", player),
            lambda state: ((state.has("Outer Sanctum Portal", player) and
                          state.has("Arcwood Pass Portal", player) and
                          state.has("Catacombs Portal", player)) or
                          state.has("Progressive Portal", player, 3)))
    
    set_rule(world.multiworld.get_location("Summore' Spectral Powder!", player),
            lambda state: ((state.has("Outer Sanctum Portal", player) and
                          state.has("Arcwood Pass Portal", player) and
                          state.has("Catacombs Portal", player)) or
                          state.has("Progressive Portal", player, 3)))
    
    set_rule(world.multiworld.get_location("Huntin' Hogs", player),
            lambda state: (state.has("Tull Valley Portal", player) or
                          state.has("Progressive Portal", player, 5)))
    
    set_rule(world.multiworld.get_location("Wicked Wizboars", player),
            lambda state: (state.has("Tull Valley Portal", player) or
                          state.has("Progressive Portal", player, 5)))
    
    set_rule(world.multiworld.get_location("Ancient Beings", player),
            lambda state: ((state.has("Crescent Road Portal", player) and
                          state.has("Crescent Keep Portal", player)) or
                          state.has("Progressive Portal", player, 7)))
    
    # ================================================================
    # MINING TURN-IN QUESTS
    # ================================================================
    set_rule(world.multiworld.get_location("Dense Ingots", player),
            lambda state: ((state.has("Outer Sanctum Portal", player) and
                          state.has("Arcwood Pass Portal", player))or
                          state.has("Progressive Portal", player, 2)))
    
    set_rule(world.multiworld.get_location("Amberite Ingots", player),
            lambda state: (state.has("Tull Valley Portal", player) or
                          state.has("Progressive Portal", player, 5)))
    
    set_rule(world.multiworld.get_location("Sapphite Ingots", player),
            lambda state: ((state.has("Tull Valley Portal", player) and
                          state.has("Tull Enclave Portal", player)) or
                          state.has("Progressive Portal", player, 8)))
    
    # ================================================================
    # CATACOMBS QUEST CHAINS
    # ================================================================
    set_rule(world.multiworld.get_location("Purging the Undead", player),
            lambda state: ((state.has("Outer Sanctum Portal", player) and
                          state.has("Arcwood Pass Portal", player) and
                          state.has("Catacombs Portal", player)) or
                          state.has("Progressive Portal", player, 3)))
    
    set_rule(world.multiworld.get_location("Rattlecage Rage", player),
            lambda state: ((state.has("Outer Sanctum Portal", player) and
                          state.has("Arcwood Pass Portal", player) and
                          state.has("Catacombs Portal", player)) or
                          state.has("Progressive Portal", player, 3)))
    
    set_rule(world.multiworld.get_location("Consumed Madness", player),
            lambda state: ((state.has("Outer Sanctum Portal", player) and
                          state.has("Arcwood Pass Portal", player) and
                          state.has("Catacombs Portal", player)) or
                          state.has("Progressive Portal", player, 3)))
    
    set_rule(world.multiworld.get_location("Eradicating the Undead", player),
            lambda state: ((state.has("Outer Sanctum Portal", player) and
                          state.has("Arcwood Pass Portal", player) and
                          state.has("Catacombs Portal", player)) or
                          state.has("Progressive Portal", player, 3)))
    
    # ================================================================
    # BOSS RULES (updated levels from v2 spreadsheet)
    # ================================================================
    set_rule(world.multiworld.get_location("Defeat Slime Diva", player),
            lambda state: (state.has("Effold Terrace Portal", player) or
                          state.has("Progressive Portal", player, 4)))
    
    set_rule(world.multiworld.get_location("Defeat Lord Zuulneruda", player),
            lambda state: ((state.has("Outer Sanctum Portal", player) and
                          state.has("Arcwood Pass Portal", player) and
                          state.has("Catacombs Portal", player)) or
                          state.has("Progressive Portal", player, 3)))
    
    set_rule(world.multiworld.get_location("Defeat Colossus", player),
            lambda state: ((state.has("Grove Portal", player) and
                          state.has("Crescent Road Portal", player) and
                          state.has("Crescent Keep Portal", player)) or
                          state.has("Progressive Portal", player, 9)))

    
    set_rule(world.multiworld.get_location("Defeat Galius", player),
            lambda state: ((state.has("Tull Valley Portal", player) and
                          state.has("Tull Enclave Portal", player) and
                          state.has("Bularr Fortress Portal", player)) or
                          state.has("Progressive Portal", player, 10)))

    # ================================================================
    # GROVE FLOOR 1 QUESTS
    # ================================================================
    set_rule(world.multiworld.get_location("Tethering Grove", player),
            lambda state: ((state.has("Grove Portal", player) and
                          state.has("Crescent Road Portal", player) and
                          state.has("Crescent Keep Portal", player)) or
                          state.has("Progressive Portal", player, 9)))
    
    # ================================================================
    # BULARR FORTRESS QUESTS
    # ================================================================
    set_rule(world.multiworld.get_location("Finding Ammagon", player),
            lambda state: ((state.has("Tull Valley Portal", player) and
                          state.has("Tull Enclave Portal", player) and
                          state.has("Bularr Fortress Portal", player)) or
                          state.has("Progressive Portal", player, 10)))
    
    set_rule(world.multiworld.get_location("Reviling the Rageboars", player),
            lambda state: ((state.has("Tull Valley Portal", player) and
                          state.has("Tull Enclave Portal", player) and
                          state.has("Bularr Fortress Portal", player)) or
                          state.has("Progressive Portal", player, 10)))
    
    set_rule(world.multiworld.get_location("Reviling More Rageboars", player),
            lambda state: ((state.has("Tull Valley Portal", player) and
                          state.has("Tull Enclave Portal", player) and
                          state.has("Bularr Fortress Portal", player)) or
                          state.has("Progressive Portal", player, 10)))
    
    # ================================================================
    # CRAFTING QUESTS (Menu region, multi-area material requirements)
    # ================================================================
    set_rule(world.multiworld.get_location("Makin' a Mekspear", player),
            lambda state: ((state.has("Tuul Valley Portal", player) and
                          state.has("Effold Terrace Portal", player) and
                          state.has("Outer Sanctum Portal", player) and
                          state.has("Arcwood Pass Portal", player) and
                          state.has("Catacombs Portal", player)) or
                          state.has("Progressive Portal", player, 5)))
    set_rule(world.multiworld.get_location("Makin' More Mekspears", player),
            lambda state: ((state.has("Tuul Valley Portal", player) and
                          state.has("Effold Terrace Portal", player) and
                          state.has("Outer Sanctum Portal", player) and
                          state.has("Arcwood Pass Portal", player) and
                          state.has("Catacombs Portal", player)) or
                          state.has("Progressive Portal", player, 5)))
    
    set_rule(world.multiworld.get_location("Makin' a Wizwand", player),
            lambda state: ((state.has("Crescent Road Portal", player) and
                          state.has("Effold Terrace Portal", player) and
                          state.has("Outer Sanctum Portal", player) and
                          state.has("Arcwood Pass Portal", player) and
                          state.has("Catacombs Portal", player) and
                          state.has("Tuul Valley Portal", player)) or
                          state.has("Progressive Portal", player, 6)))
    set_rule(world.multiworld.get_location("Makin' More Wizwands", player),
            lambda state: ((state.has("Crescent Road Portal", player) and
                          state.has("Effold Terrace Portal", player) and
                          state.has("Outer Sanctum Portal", player) and
                          state.has("Arcwood Pass Portal", player) and
                          state.has("Catacombs Portal", player) and
                          state.has("Tuul Valley Portal", player)) or
                          state.has("Progressive Portal", player, 6)))
    
    set_rule(world.multiworld.get_location("Makin' a Vile Blade", player),
            lambda state: ((state.has("Crescent Road Portal", player) and
                          state.has("Effold Terrace Portal", player) and
                          state.has("Outer Sanctum Portal", player) and
                          state.has("Arcwood Pass Portal", player) and
                          state.has("Catacombs Portal", player)) or
                          state.has("Progressive Portal", player, 6)))
    set_rule(world.multiworld.get_location("Makin' More Vile Blades", player),
            lambda state: ((state.has("Crescent Road Portal", player) and
                          state.has("Effold Terrace Portal", player) and
                          state.has("Outer Sanctum Portal", player) and
                          state.has("Arcwood Pass Portal", player) and
                          state.has("Catacombs Portal", player)) or
                          state.has("Progressive Portal", player, 6)))
    
    set_rule(world.multiworld.get_location("Makin' a Golem Chestpiece", player),
            lambda state: ((state.has("Crescent Road Portal", player) and
                          state.has("Crescent Keep Portal", player) and
                          state.has("Effold Terrace Portal", player) and
                          state.has("Outer Sanctum Portal", player) and
                          state.has("Arcwood Pass Portal", player) and
                          state.has("Catacombs Portal", player)) or
                          state.has("Progressive Portal", player, 7)))
    set_rule(world.multiworld.get_location("Summore' Golem Chestpieces", player),
            lambda state: ((state.has("Crescent Road Portal", player) and
                          state.has("Crescent Keep Portal", player) and
                          state.has("Effold Terrace Portal", player) and
                          state.has("Outer Sanctum Portal", player) and
                          state.has("Arcwood Pass Portal", player) and
                          state.has("Catacombs Portal", player)) or
                          state.has("Progressive Portal", player, 7)))
    
    set_rule(world.multiworld.get_location("Makin' a Ragespear", player),
            lambda state: ((state.has("Bularr Fortress", player) and
                          state.has("Outer Sanctum Portal", player) and
                          state.has("Tuul Valley", player) and
                          state.has("Tuul Enclave", player)) or
                          state.has("Progressive Portal", player, 10)))
    set_rule(world.multiworld.get_location("Makin' More Ragespears", player),
            lambda state: ((state.has("Bularr Fortress", player) and
                          state.has("Outer Sanctum Portal", player) and
                          state.has("Tuul Valley", player) and
                          state.has("Tuul Enclave", player)) or
                          state.has("Progressive Portal", player, 10)))
    
    # ================================================================
    # SHOP LEVEL RULES
    # ================================================================

    # Dev note: I am hoenst to goodness debating having these be "accessible" with the Catacombs Portal,
    # even if they're available with just Arcwood Pass.
    # Mainly because with needing 40k Crowns at this point to buy out the shops,
    # and Catacombs being a good early-game farming spot, it just lines up well.
    # ...
    # Or you could hope for a bunch of junk items early and reload over and over to grind money.

    for i in range(1, 6):
        set_rule(world.multiworld.get_location(f"Frankie Shop Purchase {i}", player),
            lambda state: ((state.has("Outer Sanctum Portal", player) and
                          # state.has("Catacombs Portal", player) and
                          state.has("Arcwood Pass Portal", player)) or
                          state.has("Progressive Portal", player, 2)))

    for i in range(1, 6):
        set_rule(world.multiworld.get_location(f"Tesh Shop Purchase {i}", player),
            lambda state: ((state.has("Outer Sanctum Portal", player) and
                          # state.has("Catacombs Portal", player) and
                          state.has("Arcwood Pass Portal", player)) or
                          state.has("Progressive Portal", player, 2)))
        set_rule(world.multiworld.get_location(f"Nesh Shop Purchase {i}", player),
            lambda state: ((state.has("Outer Sanctum Portal", player) and
                          # state.has("Catacombs Portal", player) and
                          state.has("Arcwood Pass Portal", player)) or
                          state.has("Progressive Portal", player, 2)))
    
    # ================================================================
    # PROFESSION LEVEL RULES
    # ================================================================
    # Fishing 4-6: need Arcwood Pass
    for fl in range(4, 7):
        set_rule(world.multiworld.get_location(f"Fishing Level {fl}", player),
            lambda state: ((state.has("Outer Sanctum Portal", player) and
                          state.has("Arcwood Pass Portal", player) and
                          state.has("Catacombs Portal", player)) or
                          state.has("Progressive Portal", player, 2)))
    # Fishing 7-10: need Crescent Road
    for fl in range(7, 11):
        set_rule(world.multiworld.get_location(f"Fishing Level {fl}", player),
            lambda state: ((state.has("Crescent Road Portal", player) and
                          state.has("Effold Terrace Portal", player) and
                          state.has("Outer Sanctum Portal", player) and
                          state.has("Arcwood Pass Portal", player) and
                          state.has("Catacombs Portal", player)) or
                          state.has("Progressive Portal", player, 6)))
    
    # Mining 2: needs Arcwood or Effold
    set_rule(world.multiworld.get_location("Mining Level 2", player),
            lambda state: ((state.has("Outer Sanctum Portal", player) and
                          state.has("Arcwood Pass Portal", player)) or
                          state.has("Progressive Portal", player, 2)))
    # Mining 3: needs various mid-level areas
    set_rule(world.multiworld.get_location("Mining Level 3", player),
            lambda state: ((state.has("Outer Sanctum Portal", player) and
                          state.has("Arcwood Pass Portal", player)) or
                          state.has("Progressive Portal", player, 2)))
    # Mining 4-6: need Tull Valley or Crescent Keep
    for ml in range(4, 7):
        set_rule(world.multiworld.get_location(f"Mining Level {ml}", player),
            lambda state: ((state.has("Tull Valley Portal", player) and
                          state.has("Outer Sanctum Portal", player)) or
                          state.has("Progressive Portal", player, 5)))
    # Mining 7-10: need Tull Enclave
    for ml in range(7, 11):
        set_rule(world.multiworld.get_location(f"Mining Level {ml}", player),
            lambda state: ((state.has("Tull Valley Portal", player) and
                          state.has("Outer Sanctum Portal", player) and
                          state.has("Tull Enclave Portal", player)) or
                          state.has("Progressive Portal", player, 8)))


def set_completion_rules(world):
    """Set the victory condition based on the selected goal."""
    player = world.player
    goal = world.options.goal.value
    
    from BaseClasses import Location
    
    boss_events = [
        "Defeat Slime Diva",
        "Defeat Lord Zuulneruda",
        "Defeat Galius",
        "Defeat Colossus",
    ]
    
    for boss_name in boss_events:
        try:
            real_location = world.multiworld.get_location(boss_name, player)
            region = real_location.parent_region
            
            event_loc_name = f"Event: {boss_name}"
            event_location = Location(player, event_loc_name, None, region)
            region.locations.append(event_location)
            
            event_item = ATLYSSItem(boss_name, ItemClassification.progression, None, player)
            event_location.place_locked_item(event_item)
        except Exception:
            pass

    if goal == 0:
        world.multiworld.completion_condition[player] = lambda state: state.has("Defeat Slime Diva", player)
    elif goal == 1:
        world.multiworld.completion_condition[player] = lambda state: state.has("Defeat Lord Zuulneruda", player)
    elif goal == 2:
        world.multiworld.completion_condition[player] = lambda state: state.has("Defeat Colossus", player)
    elif goal == 3:
        world.multiworld.completion_condition[player] = lambda state: state.has("Defeat Galius", player)
    elif goal == 4:
        world.multiworld.completion_condition[player] = lambda state: (
            state.has("Defeat Slime Diva", player) and
            state.has("Defeat Lord Zuulneruda", player) and
            state.has("Defeat Colossus", player) and
            state.has("Defeat Galius", player)
        )
    elif goal == 5:
        world.multiworld.completion_condition[player] = lambda state: state.has("Defeat Galius", player)
    elif goal == 6:
        world.multiworld.completion_condition[player] = lambda state: state.has("Reach Level 32", player)