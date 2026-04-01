from dataclasses import dataclass
from Options import Choice, Toggle, DefaultOnToggle, PerGameCommonOptions


class Goal(Choice):
    """
    What is required to complete the game.
    Slime Diva: Complete the "Diva Must Die" quest from Angela after attaining the Catacombs sigil (Effold Terrace, Lv10).
    Lord Zuulneruda: Complete the "The Voice of Vuulneruda" quest from Zuula (Catacombs Lv6-12).
    Colossus: Complete the "The Colossus" quest from Enok after gaining access to Crescent Keep & Grove (Grove Lv15-20).
    Galius: Complete the "Gatling Galius" quest from Ammagon after finding him at Enok's request (Lv22-26).
    All Bosses: Complete all 4 of the above Boss Defeat quests.
    All Quests: Complete every quest in the game.
    Level 32: Reach the maximum level.
    """
    display_name = "Goal"
    option_slime_diva = 0
    option_lord_zuulneruda = 1
    option_colossus = 2
    option_galius = 3
    option_all_bosses = 4
    option_all_quests = 5
    option_level_32 = 6
    default = 3


class RandomPortals(Toggle):
    """
    How area portals are unlocked.
    Off (default): Progressive Portals - find "Progressive Portal" items to unlock
    areas in a fixed sequence. Each portal found opens the next area in order.
    On: Random Portals - find individual portal items (e.g. "Outer Sanctum Portal",
    "Catacombs Portal") to unlock specific areas independently.

    Dev Note: It is highly recommended to leave disabled, as Angela gates all the Sanctum portals progressively anyways.
    Tuul Valley is the only string not gated by any NPCs/Quests.
    Your only benefit is gaining access to Tuul Valley earlier if you find that portal.
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
    
    Dev Note: Do not disable until further notice. Need to find out how to remove locations based on settings.
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