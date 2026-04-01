from worlds.generic.Rules import set_rule, add_rule, add_item_rule
from BaseClasses import CollectionState, ItemClassification
from .items import ATLYSSItem, item_table
from .regions import can_grind_to_level
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
        "Devious Pact": 10,
        "Disciple of Magic": 10,
        "Strength and Honor": 10,
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
    for level in range(2, 33, 2):
        loc_name = f"Reach Level {level}"
        if level == 2:
            set_rule(
                world.multiworld.get_location(loc_name, player),
                lambda state: can_grind_to_level(state, 2, player)
            )
        else:
            prev_level = level - 2
            set_rule(
                world.multiworld.get_location(loc_name, player),
                lambda state, lv=level, plv=prev_level: (
                    state.has(f"Reach Level {plv}", player) and
                    can_grind_to_level(state, lv, player)
                )
            )
    
    # ================================================================
    # TUTORIAL / STORY QUEST RULES
    # ================================================================
    # Communing Catacombs: requires A Warm Welcome
    set_rule(world.multiworld.get_location("Communing Catacombs", player),
             lambda state: state.has("A Warm Welcome", player))
    
    # ================================================================
    # CLASS QUESTS (N/A area, level-gated only)
    # ================================================================
    set_rule(world.multiworld.get_location("Call of Fury", player),
             lambda state: has_level(state, player, 4))
    set_rule(world.multiworld.get_location("Cold Shoulder", player),
             lambda state: has_level(state, player, 4))
    set_rule(world.multiworld.get_location("Focusin' in", player),
             lambda state: has_level(state, player, 4))
    set_rule(world.multiworld.get_location("Devious Pact", player),
             lambda state: has_level(state, player, 10))
    set_rule(world.multiworld.get_location("Disciple of Magic", player),
             lambda state: has_level(state, player, 10))
    set_rule(world.multiworld.get_location("Strength and Honor", player),
             lambda state: has_level(state, player, 10))
    set_rule(world.multiworld.get_location("Mastery of Strength", player),
             lambda state: has_level(state, player, 10))
    set_rule(world.multiworld.get_location("Mastery of Dexterity", player),
             lambda state: has_level(state, player, 10))
    set_rule(world.multiworld.get_location("Mastery of Mind", player),
             lambda state: has_level(state, player, 10))
    set_rule(world.multiworld.get_location("Beckoning Foes", player),
             lambda state: has_level(state, player, 12))
    set_rule(world.multiworld.get_location("Whatta' Rush!", player),
             lambda state: has_level(state, player, 12))
    
    # ================================================================
    # MULTI-AREA KILL QUESTS
    # ================================================================
    set_rule(world.multiworld.get_location("Night Spirits", player),
             lambda state: (state.can_reach_region("Outer Sanctum", player) or
                           state.can_reach_region("Arcwood Pass", player) or
                           state.can_reach_region("Catacombs Floor 1", player) or
                           state.can_reach_region("Effold Terrace", player)))
    
    set_rule(world.multiworld.get_location("Ridding Slimes", player),
             lambda state: (state.can_reach_region("Outer Sanctum", player) or
                           state.can_reach_region("Arcwood Pass", player) or
                           state.can_reach_region("Effold Terrace", player)))
    
    set_rule(world.multiworld.get_location("Ghostly Goods", player),
             lambda state: (state.has("A Warm Welcome", player) and
                           (state.can_reach_region("Arcwood Pass", player) or
                            state.can_reach_region("Catacombs Floor 1", player))))
    
    set_rule(world.multiworld.get_location("Summore' Spectral Powder!", player),
             lambda state: (state.has("Ghostly Goods", player) and
                           (state.can_reach_region("Arcwood Pass", player) or
                            state.can_reach_region("Catacombs Floor 1", player))))
    
    set_rule(world.multiworld.get_location("Huntin' Hogs", player),
             lambda state: (has_level(state, player, 7) and
                           (state.can_reach_region("Tull Valley", player) or
                            state.can_reach_region("Crescent Keep", player))))
    
    set_rule(world.multiworld.get_location("Wicked Wizboars", player),
             lambda state: (has_level(state, player, 10) and
                           (state.can_reach_region("Tull Valley", player) or
                            state.can_reach_region("Tull Enclave", player) or
                            state.can_reach_region("Crescent Keep", player))))
    
    set_rule(world.multiworld.get_location("Ancient Beings", player),
             lambda state: (has_level(state, player, 8) and
                           state.has("The Keep Within", player) and
                           (state.can_reach_region("Crescent Road", player) or
                            state.can_reach_region("Crescent Keep", player))))
    
    # ================================================================
    # MINING TURN-IN QUESTS
    # ================================================================
    set_rule(world.multiworld.get_location("Dense Ingots", player),
             lambda state: (state.can_reach_region("Arcwood Pass", player) or
                           state.can_reach_region("Effold Terrace", player)))
    
    set_rule(world.multiworld.get_location("Amberite Ingots", player),
             lambda state: has_level(state, player, 6))
    
    set_rule(world.multiworld.get_location("Sapphite Ingots", player),
             lambda state: (has_level(state, player, 8) and
                           (state.can_reach_region("Tull Valley", player) or
                            state.can_reach_region("Crescent Keep", player))))
    
    # ================================================================
    # CATACOMBS QUEST CHAINS
    # ================================================================
    set_rule(world.multiworld.get_location("Purging the Undead", player),
             lambda state: (state.has("Killing Tomb", player) and
                           has_level(state, player, 6)))
    
    set_rule(world.multiworld.get_location("Rattlecage Rage", player),
             lambda state: (state.has("Killing Tomb", player) and
                           has_level(state, player, 6)))
    
    set_rule(world.multiworld.get_location("Consumed Madness", player),
             lambda state: (state.has("The Voice of Zuulneruda", player) and
                           has_level(state, player, 12)))
    
    set_rule(world.multiworld.get_location("Eradicating the Undead", player),
             lambda state: (state.has("The Voice of Zuulneruda", player) and
                           has_level(state, player, 12)))
    
    # ================================================================
    # EFFOLD TERRACE QUESTS
    # ================================================================
    set_rule(world.multiworld.get_location("Cleaning Terrace", player),
             lambda state: (state.has("Diva Must Die", player) and
                           has_level(state, player, 5)))
    
    # ================================================================
    # BOSS RULES (updated levels from v2 spreadsheet)
    # ================================================================
    set_rule(world.multiworld.get_location("Defeat Slime Diva", player),
             lambda state: has_level(state, player, 10))
    
    set_rule(world.multiworld.get_location("Defeat Lord Zuulneruda", player),
             lambda state: has_level(state, player, 12))
    
    set_rule(world.multiworld.get_location("Defeat Lord Kaluuz", player),
             lambda state: has_level(state, player, 18))
    
    set_rule(world.multiworld.get_location("Defeat Colossus", player),
             lambda state: has_level(state, player, 20))
    
    set_rule(world.multiworld.get_location("Defeat Valdur", player),
             lambda state: has_level(state, player, 25))
    
    set_rule(world.multiworld.get_location("Defeat Galius", player),
             lambda state: has_level(state, player, 26))
    
    # ================================================================
    # CRESCENT KEEP QUESTS
    # ================================================================
    set_rule(world.multiworld.get_location("Up and Over It", player),
             lambda state: has_level(state, player, 15))
    
    # ================================================================
    # TULL ENCLAVE QUESTS
    # ================================================================
    set_rule(world.multiworld.get_location("Searching for the Grove", player),
             lambda state: has_level(state, player, 15))
    
    # ================================================================
    # GROVE FLOOR 1 QUESTS
    # ================================================================
    set_rule(world.multiworld.get_location("Tethering Grove", player),
             lambda state: (state.has("The Keep Within", player) and
                           has_level(state, player, 15)))
    
    set_rule(world.multiworld.get_location("Spiraling In The Grove", player),
             lambda state: (state.has("Tethering Grove", player) and
                           has_level(state, player, 15)))
    
    set_rule(world.multiworld.get_location("Purging the Grove", player),
             lambda state: (state.has("The Colossus", player) and
                           has_level(state, player, 15)))
    
    # ================================================================
    # GROVE FLOOR 2 QUESTS
    # ================================================================
    set_rule(world.multiworld.get_location("Hell In The Grove", player),
             lambda state: (state.has("Tethering Grove", player) and
                           has_level(state, player, 20)))
    
    set_rule(world.multiworld.get_location("Cleansing the Grove", player),
             lambda state: (state.has("The Colossus", player) and
                           has_level(state, player, 20)))
    
    set_rule(world.multiworld.get_location("Nulversa Magica", player),
             lambda state: has_level(state, player, 20))
    set_rule(world.multiworld.get_location("Nulversa Viscera", player),
             lambda state: has_level(state, player, 20))
    set_rule(world.multiworld.get_location("Nulversa, Greenveras!", player),
             lambda state: has_level(state, player, 20))
    
    set_rule(world.multiworld.get_location("Makin' a Firebreath Blade", player),
             lambda state: has_level(state, player, 20))
    set_rule(world.multiworld.get_location("Summore' Firebreath Blades", player),
             lambda state: (state.has("Makin' a Firebreath Blade", player) and
                           has_level(state, player, 20)))
    
    # ================================================================
    # BULARR FORTRESS QUESTS
    # ================================================================
    set_rule(world.multiworld.get_location("Finding Ammagon", player),
             lambda state: has_level(state, player, 14))
    
    set_rule(world.multiworld.get_location("Reviling the Rageboars", player),
             lambda state: has_level(state, player, 14))
    
    set_rule(world.multiworld.get_location("Reviling More Rageboars", player),
             lambda state: (state.has("Reviling the Rageboars", player) and
                           has_level(state, player, 14)))
    
    set_rule(world.multiworld.get_location("Facing Foes", player),
             lambda state: has_level(state, player, 18))
    
    set_rule(world.multiworld.get_location("The Gall of Galius", player),
             lambda state: (state.has("Gatling Galius", player) and
                           has_level(state, player, 22)))
    
    set_rule(world.multiworld.get_location("Makin' a Follycannon", player),
             lambda state: has_level(state, player, 24))
    
    set_rule(world.multiworld.get_location("Makin' More Follycannons", player),
             lambda state: (state.has("Makin' a Follycannon", player) and
                           has_level(state, player, 24)))
    
    # ================================================================
    # CRAFTING QUESTS (Menu region, multi-area material requirements)
    # ================================================================
    set_rule(world.multiworld.get_location("Makin' a Mekspear", player),
             lambda state: (has_level(state, player, 7) and
                           state.can_reach_region("Effold Terrace", player) and
                           (state.can_reach_region("Tull Valley", player) or
                            state.can_reach_region("Crescent Keep", player))))
    set_rule(world.multiworld.get_location("Makin' More Mekspears", player),
             lambda state: (state.has("Makin' a Mekspear", player) and
                           has_level(state, player, 7) and
                           state.can_reach_region("Effold Terrace", player) and
                           (state.can_reach_region("Tull Valley", player) or
                            state.can_reach_region("Crescent Keep", player))))
    
    set_rule(world.multiworld.get_location("Makin' a Wizwand", player),
             lambda state: (has_level(state, player, 10) and
                           (state.can_reach_region("Crescent Keep", player) or
                            state.can_reach_region("Crescent Road", player)) and
                           (state.can_reach_region("Tull Valley", player) or
                            state.can_reach_region("Tull Enclave", player))))
    set_rule(world.multiworld.get_location("Makin' More Wizwands", player),
             lambda state: (state.has("Makin' a Wizwand", player) and
                           has_level(state, player, 10) and
                           (state.can_reach_region("Crescent Keep", player) or
                            state.can_reach_region("Crescent Road", player)) and
                           (state.can_reach_region("Tull Valley", player) or
                            state.can_reach_region("Tull Enclave", player))))
    
    set_rule(world.multiworld.get_location("Makin' a Vile Blade", player),
             lambda state: (has_level(state, player, 10) and
                           (state.can_reach_region("Crescent Keep", player) or
                            state.can_reach_region("Crescent Road", player)) and
                           state.can_reach_region("Effold Terrace", player) and
                           state.can_reach_region("Catacombs Floor 2", player)))
    set_rule(world.multiworld.get_location("Makin' More Vile Blades", player),
             lambda state: (state.has("Makin' a Vile Blade", player) and
                           has_level(state, player, 10) and
                           (state.can_reach_region("Crescent Keep", player) or
                            state.can_reach_region("Crescent Road", player)) and
                           state.can_reach_region("Effold Terrace", player) and
                           state.can_reach_region("Catacombs Floor 2", player)))
    
    set_rule(world.multiworld.get_location("Makin' a Golem Chestpiece", player),
             lambda state: (state.has("The Keep Within", player) and
                           has_level(state, player, 12) and
                           (state.can_reach_region("Crescent Road", player) or
                            state.can_reach_region("Crescent Keep", player))))
    set_rule(world.multiworld.get_location("Summore' Golem Chestpieces", player),
             lambda state: (state.has("Makin' a Golem Chestpiece", player) and
                           has_level(state, player, 12) and
                           (state.can_reach_region("Crescent Road", player) or
                            state.can_reach_region("Crescent Keep", player))))
    
    set_rule(world.multiworld.get_location("Makin' a Ragespear", player),
             lambda state: (state.has("Makin' a Mekspear", player) and
                           has_level(state, player, 15) and
                           state.can_reach_region("Effold Terrace", player) and
                           (state.can_reach_region("Tull Valley", player) or
                            state.can_reach_region("Crescent Keep", player)) and
                           state.can_reach_region("Bularr Fortress", player) and
                           state.can_reach_region("Catacombs Floor 3", player)))
    set_rule(world.multiworld.get_location("Makin' More Ragespears", player),
             lambda state: (state.has("Makin' a Ragespear", player) and
                           has_level(state, player, 15) and
                           state.can_reach_region("Effold Terrace", player) and
                           (state.can_reach_region("Tull Valley", player) or
                            state.can_reach_region("Crescent Keep", player)) and
                           state.can_reach_region("Bularr Fortress", player) and
                           state.can_reach_region("Catacombs Floor 3", player)))
    
    set_rule(world.multiworld.get_location("Makin' a Monolith Chestpiece", player),
             lambda state: (state.has("Makin' a Golem Chestpiece", player) and
                           has_level(state, player, 16) and
                           (state.can_reach_region("Crescent Road", player) or
                            state.can_reach_region("Crescent Keep", player)) and
                           state.can_reach_region("Grove Floor 1", player)))
    set_rule(world.multiworld.get_location("Summore' Monolith Chestpieces", player),
             lambda state: (state.has("Makin' a Monolith Chestpiece", player) and
                           has_level(state, player, 16) and
                           (state.can_reach_region("Crescent Road", player) or
                            state.can_reach_region("Crescent Keep", player)) and
                           state.can_reach_region("Grove Floor 1", player)))
    
    set_rule(world.multiworld.get_location("The Glyphik Booklet", player),
             lambda state: (state.has("Finding Ammagon", player) and
                           has_level(state, player, 24) and
                           state.can_reach_region("Luvora Garden", player) and
                           state.can_reach_region("Tull Enclave", player) and
                           state.can_reach_region("Grove Floor 2", player) and
                           state.can_reach_region("Bularr Fortress", player)))
    
    # ================================================================
    # SHOP LEVEL RULES
    # ================================================================
    for i in range(1, 6):
        set_rule(world.multiworld.get_location(f"Tesh Shop Purchase {i}", player),
                 lambda state: has_level(state, player, 6))
        set_rule(world.multiworld.get_location(f"Nesh Shop Purchase {i}", player),
                 lambda state: has_level(state, player, 6))
    
    for i in range(1, 6):
        set_rule(world.multiworld.get_location(f"Cotoo Shop Purchase {i}", player),
                 lambda state: has_level(state, player, 15))
        set_rule(world.multiworld.get_location(f"Rikko Shop Purchase {i}", player),
                 lambda state: has_level(state, player, 15))
    
    # ================================================================
    # PROFESSION LEVEL RULES
    # ================================================================
    # Fishing 4-6: need Arcwood Pass
    for fl in range(4, 7):
        set_rule(world.multiworld.get_location(f"Fishing Level {fl}", player),
                 lambda state: state.can_reach_region("Arcwood Pass", player))
    # Fishing 7-10: need Crescent Road
    for fl in range(7, 11):
        set_rule(world.multiworld.get_location(f"Fishing Level {fl}", player),
                 lambda state: state.can_reach_region("Crescent Road", player))
    
    # Mining 2: needs Arcwood or Effold
    set_rule(world.multiworld.get_location("Mining Level 2", player),
             lambda state: (state.can_reach_region("Arcwood Pass", player) or
                           state.can_reach_region("Effold Terrace", player)))
    # Mining 3: needs various mid-level areas
    set_rule(world.multiworld.get_location("Mining Level 3", player),
             lambda state: (state.can_reach_region("Arcwood Pass", player) or
                           state.can_reach_region("Effold Terrace", player) or
                           state.can_reach_region("Outer Sanctum", player) or
                           state.can_reach_region("Crescent Keep", player) or
                           state.can_reach_region("Tull Enclave", player)))
    # Mining 4-6: need Tull Valley or Crescent Keep
    for ml in range(4, 7):
        set_rule(world.multiworld.get_location(f"Mining Level {ml}", player),
                 lambda state: (state.can_reach_region("Tull Valley", player) or
                               state.can_reach_region("Crescent Keep", player)))
    # Mining 7-10: need Tull Enclave
    for ml in range(7, 11):
        set_rule(world.multiworld.get_location(f"Mining Level {ml}", player),
                 lambda state: state.can_reach_region("Tull Enclave", player))


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
        "Defeat Lord Kaluuz",
        "Defeat Valdur",
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
    
    boss_level_rules = {
        "Defeat Slime Diva": 10,
        "Defeat Lord Zuulneruda": 12,
        "Defeat Colossus": 20,
        "Defeat Galius": 26,
        "Defeat Lord Kaluuz": 18,
        "Defeat Valdur": 25,
    }
    for boss_name, req_level in boss_level_rules.items():
        try:
            set_rule(
                world.multiworld.get_location(f"Event: {boss_name}", player),
                lambda state, lv=req_level: has_level(state, player, lv)
            )
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
        world.multiworld.completion_condition[player] = lambda state: state.has("Defeat Lord Kaluuz", player)
    elif goal == 5:
        world.multiworld.completion_condition[player] = lambda state: state.has("Defeat Valdur", player)
    elif goal == 6:
        world.multiworld.completion_condition[player] = lambda state: (
            state.has("Defeat Slime Diva", player) and
            state.has("Defeat Lord Zuulneruda", player) and
            state.has("Defeat Colossus", player) and
            state.has("Defeat Galius", player) and
            state.has("Defeat Lord Kaluuz", player) and
            state.has("Defeat Valdur", player)
        )
    elif goal == 7:
        world.multiworld.completion_condition[player] = lambda state: state.has("Defeat Galius", player)
    elif goal == 8:
        world.multiworld.completion_condition[player] = lambda state: has_level(state, player, 32)