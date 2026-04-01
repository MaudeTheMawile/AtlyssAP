from dataclasses import dataclass
from Options import Choice, Toggle, DefaultOnToggle, PerGameCommonOptions


class Goal(Choice):
    """
    What is required to complete the game.
    Slime Diva: Defeat the Slime Diva boss (level 10).
    Lord Zuulneruda: Defeat Lord Zuulneruda in the Catacombs (level 12).
    Colossus: Defeat the Colossus in Crescent Grove (level 20).
    Galius: Defeat Galius in Bularr Fortress (level 26) - DEFAULT.
    Lord Kaluuz: Defeat Lord Kaluuz in Catacombs Floor 3 (level 18).
    Valdur: Defeat Valdur the dragon (level 25+).
    All Bosses: Defeat all 6 major bosses.
    All Quests: Complete every quest in the game.
    Level 32: Reach the maximum level.
    """
    display_name = "Goal"
    option_slime_diva = 0
    option_lord_zuulneruda = 1
    option_colossus = 2
    option_galius = 3
    option_lord_kaluuz = 4
    option_valdur = 5
    option_all_bosses = 6
    option_all_quests = 7
    option_level_32 = 8
    default = 3


class RandomPortals(Toggle):
    """
    How area portals are unlocked.
    Off (default): Progressive Portals - find "Progressive Portal" items to unlock
    areas in a fixed sequence. Each portal found opens the next area in order.
    On: Random Portals - find individual portal items (e.g. "Outer Sanctum Portal",
    "Catacombs Portal") to unlock specific areas independently.
    """
    display_name = "Random Portals"


class EquipmentProgression(Choice):
    """
    How equipment is distributed.
    Gated (default): Equipment has level requirements. Higher tier gear only
    appears at locations accessible at appropriate levels. Tier 1 gear (lv 1-5)
    can appear anywhere; Tier 5 gear (lv 21-26) only at endgame locations.
    Random: Equipment can appear anywhere with no level gating. You may find
    endgame weapons in early spheres — chaotic but fun.
    """
    display_name = "Equipment Progression"
    option_gated = 0
    option_random = 1
    default = 0


class ShopSanity(DefaultOnToggle):
    """
    Whether shop items can contain Archipelago items from other worlds.
    When enabled, buying items from shops sends checks to other players.
    """
    display_name = "Shop Sanity"


class ClassFilter(Choice):
    """
    Filter equipment in the item pool to only include gear for specific classes.
    Weapons are filtered by scaling stat (STR=Fighter, MIND=Mystic, DEX=Bandit).
    Class-locked armor is filtered by its required class.
    Shields are included for Fighter and Mystic (one-handed weapon users).
    Universal armor (helms, capes, trinkets, cosmetics) is always included.

    All Classes (default): No filtering, all equipment is in the pool.
    Single class: Only that class's weapons and armor are included.
    Two classes: Both classes' equipment is included.
    """
    display_name = "Class Filter"
    option_all_classes = 0
    option_fighter = 1
    option_mystic = 2
    option_bandit = 3
    option_fighter_mystic = 4
    option_fighter_bandit = 5
    option_mystic_bandit = 6
    default = 0


@dataclass
class ATLYSSOptions(PerGameCommonOptions):
    goal: Goal
    random_portals: RandomPortals
    equipment_progression: EquipmentProgression
    shop_sanity: ShopSanity
    class_filter: ClassFilter