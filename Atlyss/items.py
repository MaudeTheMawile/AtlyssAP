from typing import Dict, NamedTuple, Optional
from BaseClasses import Item, ItemClassification


class ATLYSSItem(Item):
    game: str = "ATLYSS"


class ItemData(NamedTuple):
    code: Optional[int]
    classification: ItemClassification
    tier: Optional[int] = None  # For equipment level gating (1-5)
    class_affinity: Optional[str] = None  # "F"=Fighter, "M"=Mystic, "B"=Bandit, "FM"=Fighter+Mystic, None=universal


item_table: Dict[str, ItemData] = {
    # Consumables - Status Effect Packs (FILLER except exp tomes)
    "Bunbag Pack": ItemData(592000, ItemClassification.filler),
    "Bunjar Pack": ItemData(592001, ItemClassification.filler),
    "Bunpot Pack": ItemData(592002, ItemClassification.filler),
    "Regen Potion Pack": ItemData(592003, ItemClassification.filler),
    "Regen Vial Pack": ItemData(592004, ItemClassification.filler),
    "Magiclove Pack": ItemData(592005, ItemClassification.filler),
    "Magiflower Pack": ItemData(592006, ItemClassification.filler),
    "Magileaf Pack": ItemData(592007, ItemClassification.filler),
    "Stamstar Pack": ItemData(592008, ItemClassification.filler),
    "Agility Potion Pack": ItemData(592009, ItemClassification.filler),
    "Agility Vial Pack": ItemData(592010, ItemClassification.filler),
    "Bolster Potion Pack": ItemData(592011, ItemClassification.filler),
    "Bolster Vial Pack": ItemData(592012, ItemClassification.filler),
    "Wisdom Potion Pack": ItemData(592013, ItemClassification.filler),
    "Wisdom Vial Pack": ItemData(592014, ItemClassification.filler),
    "Tome of Greater Experience": ItemData(592015, ItemClassification.useful),
    "Tome of Experience": ItemData(592016, ItemClassification.useful),
    "Tome of Lesser Experience": ItemData(592017, ItemClassification.useful),
    "Carrot Cake Pack": ItemData(592018, ItemClassification.filler),
    "Minchroom Juice Pack": ItemData(592019, ItemClassification.filler),
    "Spectral Powder Pack": ItemData(592020, ItemClassification.filler),


    # Weapons - Tier 1 (Levels 1-5)
    "Crypt Blade": ItemData(591801, ItemClassification.useful, 1, "F"),
    "Femur Club": ItemData(591802, ItemClassification.useful, 1, "F"),
    "Ironbark Sword": ItemData(591803, ItemClassification.useful, 1, "F"),
    "Slimecrust Blade": ItemData(591804, ItemClassification.useful, 1, "F"),
    "Gilded Sword": ItemData(591805, ItemClassification.useful, 1, "F"),
    "Splitbark Club": ItemData(591806, ItemClassification.useful, 1, "F"),

    # Weapons - Tier 2 (Levels 6-10)
    "Demicrypt Blade": ItemData(591807, ItemClassification.useful, 2, "F"),
    "Dense Mace": ItemData(591808, ItemClassification.useful, 2, "F"),
    "Iron Sword": ItemData(591809, ItemClassification.useful, 2, "F"),
    "Dawn Mace": ItemData(591810, ItemClassification.useful, 2, "F"),
    "Rude Blade": ItemData(591811, ItemClassification.useful, 2, "F"),
    "Vile Blade": ItemData(591812, ItemClassification.useful, 2, "F"),

    # Weapons - Tier 3 (Levels 11-15)
    "Amberite Sword": ItemData(591813, ItemClassification.useful, 3, "F"),
    "Nethercrypt Blade": ItemData(591814, ItemClassification.useful, 3, "F"),

    # Weapons - Tier 4 (Levels 16-20)
    "Coldgeist Blade": ItemData(591815, ItemClassification.useful, 4, "F"),
    "Mithril Sword": ItemData(591816, ItemClassification.useful, 4, "F"),
    "Serrated Blade": ItemData(591817, ItemClassification.useful, 4, "F"),
    "Nulrok Mace": ItemData(591818, ItemClassification.useful, 4, "F"),

    # Weapons - Tier 5 (Levels 21-26)
    "Firebreath Blade": ItemData(591819, ItemClassification.useful, 5, "F"),
    "Valdur Blade": ItemData(591820, ItemClassification.useful, 5, "F"),
    "Fier Blade": ItemData(591821, ItemClassification.useful, 5, "F"),

    # Weapons - Tier 1 (Levels 1-5)
    "Slimek Axehammer": ItemData(591823, ItemClassification.useful, 1, "F"),

    # Weapons - Tier 2 (Levels 6-10)
    "Dense Hammer": ItemData(591824, ItemClassification.useful, 2, "F"),
    "Iron Axehammer": ItemData(591825, ItemClassification.useful, 2, "F"),
    "Crypt Pounder": ItemData(591826, ItemClassification.useful, 2, "F"),

    # Weapons - Tier 4 (Levels 16-20)
    "Quake Pummeler": ItemData(591827, ItemClassification.useful, 4, "F"),

    # Weapons - Tier 1 (Levels 1-5)
    "Mini Geist Scythe": ItemData(591828, ItemClassification.useful, 1, "F"),

    # Weapons - Tier 2 (Levels 6-10)
    "Geist Scythe": ItemData(591829, ItemClassification.useful, 2, "F"),
    "Stone Greatblade": ItemData(591830, ItemClassification.useful, 2, "F"),

    # Weapons - Tier 3 (Levels 11-15)
    "Amberite Warstar": ItemData(591831, ItemClassification.useful, 3, "F"),
    "Dolkin's Axe": ItemData(591832, ItemClassification.useful, 3, "F"),
    "Poltergeist Scythe": ItemData(591833, ItemClassification.useful, 3, "F"),

    # Weapons - Tier 4 (Levels 16-20)
    "Coldgeist Punisher": ItemData(591834, ItemClassification.useful, 4, "F"),
    "Deadwood Axe": ItemData(591835, ItemClassification.useful, 4, "F"),
    "Mithril Greatsword": ItemData(591836, ItemClassification.useful, 4, "F"),

    # Weapons - Tier 5 (Levels 21-26)
    "Deathknight Runeblade": ItemData(591837, ItemClassification.useful, 5, "F"),
    "Ryzer Greataxe": ItemData(591838, ItemClassification.useful, 5, "F"),

    # Weapons - Tier 1 (Levels 1-5)

    # Weapons - Tier 2 (Levels 6-10)
    "Dense Spear": ItemData(591840, ItemClassification.useful, 2, "F"),
    "Iron Spear": ItemData(591841, ItemClassification.useful, 2, "F"),
    "Cryptsinge Halberd": ItemData(591842, ItemClassification.useful, 2, "F"),
    "Mekspear": ItemData(591843, ItemClassification.useful, 2, "F"),

    # Weapons - Tier 3 (Levels 11-15)
    "Amberite Halberd": ItemData(591844, ItemClassification.useful, 3, "F"),
    "Necroroyal Halberd": ItemData(591845, ItemClassification.useful, 3, "F"),
    "Sinner Bardiche": ItemData(591846, ItemClassification.useful, 3, "F"),

    # Weapons - Tier 4 (Levels 16-20)
    "Mithril Halberd": ItemData(591847, ItemClassification.useful, 4, "F"),
    "Ragespear": ItemData(591848, ItemClassification.useful, 4, "F"),
    "Serrated Spear": ItemData(591849, ItemClassification.useful, 4, "F"),
    "Sapphite Spear": ItemData(591850, ItemClassification.useful, 4, "F"),
    "Nulrok Spear": ItemData(591851, ItemClassification.useful, 4, "F"),

    # Weapons - Tier 5 (Levels 21-26)
    "Cryotribe Spear": ItemData(591852, ItemClassification.useful, 5, "F"),
    "Flametribe Spear": ItemData(591853, ItemClassification.useful, 5, "F"),

    # Weapons - Tier 1 (Levels 1-5)
    "Marrow Bauble": ItemData(591855, ItemClassification.useful, 1, "M"),
    "Splitbark Scepter": ItemData(591856, ItemClassification.useful, 1, "M"),

    # Weapons - Tier 2 (Levels 6-10)
    "Demicrypt Bauble": ItemData(591857, ItemClassification.useful, 2, "M"),
    "Iron Scepter": ItemData(591858, ItemClassification.useful, 2, "M"),
    "Cryo Cane": ItemData(591859, ItemClassification.useful, 2, "M"),
    "Slime Diva Baton": ItemData(591860, ItemClassification.useful, 2, "M"),

    # Weapons - Tier 3 (Levels 11-15)
    "Pyre Cane": ItemData(591861, ItemClassification.useful, 3, "M"),
    "Wizwand": ItemData(591862, ItemClassification.useful, 3, "M"),
    "Nethercrypt Bauble": ItemData(591863, ItemClassification.useful, 3, "M"),

    # Weapons - Tier 4 (Levels 16-20)
    "Aquapetal Staff": ItemData(591864, ItemClassification.useful, 4, "M"),
    "Flamepetal Staff": ItemData(591865, ItemClassification.useful, 4, "M"),
    "Mithril Scepter": ItemData(591866, ItemClassification.useful, 4, "M"),
    "Sapphite Scepter": ItemData(591867, ItemClassification.useful, 4, "M"),

    # Weapons - Tier 5 (Levels 21-26)
    "Voalstark Wand": ItemData(591868, ItemClassification.useful, 5, "M"),

    # Weapons - Tier 1 (Levels 1-5)

    # Weapons - Tier 2 (Levels 6-10)
    "Cryptcall Bell": ItemData(591870, ItemClassification.useful, 2, "M"),
    "Iron Bell": ItemData(591871, ItemClassification.useful, 2, "M"),

    # Weapons - Tier 4 (Levels 16-20)
    "Coldgeist Frostcaller": ItemData(591872, ItemClassification.useful, 4, "M"),
    "Mithril Bell": ItemData(591873, ItemClassification.useful, 4, "M"),
    "Colossus Tone": ItemData(591874, ItemClassification.useful, 4, "M"),
    "Sapphite Bell": ItemData(591875, ItemClassification.useful, 4, "M"),

    # Weapons - Tier 1 (Levels 1-5)
    "Slimecrust Katars": ItemData(591877, ItemClassification.useful, 1, "B"),
    "Cryptsinge Katars": ItemData(591878, ItemClassification.useful, 1, "B"),
    "Slimek Shivs": ItemData(591879, ItemClassification.useful, 1, "B"),

    # Weapons - Tier 2 (Levels 6-10)
    "Deathgel Shivs": ItemData(591880, ItemClassification.useful, 2, "B"),
    "Dense Katars": ItemData(591881, ItemClassification.useful, 2, "B"),
    "Iron Katars": ItemData(591882, ItemClassification.useful, 2, "B"),
    "Runic Katars": ItemData(591883, ItemClassification.useful, 2, "B"),

    # Weapons - Tier 3 (Levels 11-15)
    "Geistlord Claws": ItemData(591884, ItemClassification.useful, 3, "B"),
    "Hellsludge Shivs": ItemData(591885, ItemClassification.useful, 3, "B"),
    "Mithril Katars": ItemData(591886, ItemClassification.useful, 3, "B"),

    # Weapons - Tier 4 (Levels 16-20)
    "Frostbite Claws": ItemData(591887, ItemClassification.useful, 4, "B"),
    "Serrated Knuckles": ItemData(591888, ItemClassification.useful, 4, "B"),
    "Rummok Bladerings": ItemData(591889, ItemClassification.useful, 4, "B"),
    "Sapphite Katars": ItemData(591890, ItemClassification.useful, 4, "B"),
    "Golemfist Katars": ItemData(591891, ItemClassification.useful, 4, "B"),

    # Weapons - Tier 1 (Levels 1-5)
    "Crypt Bow": ItemData(591893, ItemClassification.useful, 1, "B"),

    # Weapons - Tier 2 (Levels 6-10)
    "Demicrypt Bow": ItemData(591894, ItemClassification.useful, 2, "B"),
    "Iron Bow": ItemData(591895, ItemClassification.useful, 2, "B"),
    "Mekspike Bow": ItemData(591896, ItemClassification.useful, 2, "B"),
    "Menace Bow": ItemData(591897, ItemClassification.useful, 2, "B"),

    # Weapons - Tier 3 (Levels 11-15)
    "Petrified Bow": ItemData(591898, ItemClassification.useful, 3, "B"),
    "Mithril Bow": ItemData(591899, ItemClassification.useful, 3, "B"),
    "Necroroyal Bow": ItemData(591900, ItemClassification.useful, 3, "B"),

    # Weapons - Tier 4 (Levels 16-20)
    "Coldgeist Bow": ItemData(591901, ItemClassification.useful, 4, "B"),
    "Serrated Longbow": ItemData(591902, ItemClassification.useful, 4, "B"),

    # Weapons - Tier 5 (Levels 21-26)
    "Torrentius Longbow": ItemData(591903, ItemClassification.useful, 5, "B"),

    # Weapons - Tier 3 (Levels 11-15)
    "Amberite Boomstick": ItemData(591904, ItemClassification.useful, 3, "B"),

    # Weapons - Tier 4 (Levels 16-20)
    "Magitek Burstgun": ItemData(591905, ItemClassification.useful, 4, "B"),

    # Weapons - Tier 5 (Levels 21-26)
    "Follycannon": ItemData(591906, ItemClassification.useful, 5, "B"),


    # Armor - Helms - Tier 1 (Levels 1-5)
    "Agility Ears": ItemData(592100, ItemClassification.useful, 1),
    "Festive Hat": ItemData(592101, ItemClassification.filler),
    "Fishin Hat": ItemData(592102, ItemClassification.filler),
    "Leather Cap": ItemData(592103, ItemClassification.useful, 1),
    "Newfold Halo": ItemData(592104, ItemClassification.useful, 1),
    "Orefinder Hat": ItemData(592105, ItemClassification.filler),
    "Spooky Hat": ItemData(592106, ItemClassification.filler),
    "Top Hat": ItemData(592107, ItemClassification.filler),
    "Wizard Hat": ItemData(592108, ItemClassification.filler),
    "Acolyte Hood": ItemData(592109, ItemClassification.useful, 1),
    "Cryptsinge Halo": ItemData(592110, ItemClassification.useful, 1),
    "Initiate Spectacles": ItemData(592111, ItemClassification.useful, 1),

    # Armor - Helms - Tier 2 (Levels 6-10)
    "Demicrypt Halo": ItemData(592112, ItemClassification.useful, 2),
    "Dense Helm": ItemData(592113, ItemClassification.useful, 2),
    "Diva Crown": ItemData(592114, ItemClassification.useful, 2),
    "Iron Halo": ItemData(592115, ItemClassification.useful, 2),
    "Necromancer Hood": ItemData(592116, ItemClassification.useful, 2),
    "Geistlord Crown": ItemData(592117, ItemClassification.useful, 2),
    "Journeyman Spectacles": ItemData(592118, ItemClassification.useful, 2),

    # Armor - Helms - Tier 3 (Levels 11-15)
    "Amberite Helm": ItemData(592119, ItemClassification.useful, 3),
    "Focus Circlet": ItemData(592120, ItemClassification.useful, 3, "M"),
    "Magistrate Circlet": ItemData(592121, ItemClassification.useful, 3),
    "Rage Circlet": ItemData(592122, ItemClassification.useful, 3),
    "Focusi Glasses": ItemData(592123, ItemClassification.useful, 3, "M"),
    "Nethercrypt Halo": ItemData(592124, ItemClassification.useful, 3),

    # Armor - Helms - Tier 4 (Levels 16-20)
    "Carbuncle Hat": ItemData(592125, ItemClassification.useful, 4),
    "Geistlord Eye": ItemData(592126, ItemClassification.useful, 4),
    "Glyphgrift Halo": ItemData(592127, ItemClassification.useful, 4),
    "Jestercast Memory": ItemData(592128, ItemClassification.useful, 4),
    "Knightguard Halo": ItemData(592129, ItemClassification.useful, 4),
    "Mithril Halo": ItemData(592130, ItemClassification.useful, 4),
    "Sapphite Mindhat": ItemData(592131, ItemClassification.useful, 4, "M"),

    # Armor - Helms - Tier 5 (Levels 21-26)
    "Dire Helm": ItemData(592132, ItemClassification.useful, 5),
    "Druidic Halo": ItemData(592133, ItemClassification.useful, 5),
    "Guardel Helm": ItemData(592134, ItemClassification.useful, 5),
    "Leathen Cap": ItemData(592135, ItemClassification.useful, 5),
    "Boarus Helm": ItemData(592136, ItemClassification.useful, 5),
    "Deathknight Helm": ItemData(592137, ItemClassification.useful, 5),
    "Emerock Halo": ItemData(592138, ItemClassification.useful, 5),
    "Wizlad Hood": ItemData(592139, ItemClassification.useful, 5, "M"),
    "Boarus Torment": ItemData(592140, ItemClassification.useful, 5),


    # Armor - Capes - Tier 1 (Levels 1-5)
    "Initiate Cloak": ItemData(592400, ItemClassification.useful, 1),
    "Slimewoven Cloak": ItemData(592401, ItemClassification.useful, 1),

    # Armor - Capes - Tier 2 (Levels 6-10)
    "Nokket Cloak": ItemData(592402, ItemClassification.useful, 2),
    "Rugged Cloak": ItemData(592403, ItemClassification.useful, 2),
    "Regazuul Cape": ItemData(592404, ItemClassification.useful, 2),

    # Armor - Capes - Tier 3 (Levels 11-15)
    "Flux Cloak": ItemData(592405, ItemClassification.useful, 3),
    "Cozy Cloak": ItemData(592406, ItemClassification.useful, 3),
    "Nethercrypt Cloak": ItemData(592407, ItemClassification.useful, 3),

    # Armor - Capes - Tier 4 (Levels 16-20)
    "Cobblerage Cloak": ItemData(592408, ItemClassification.useful, 4),
    "Deathward Cape": ItemData(592409, ItemClassification.useful, 4),
    "Forlorn Cloak": ItemData(592410, ItemClassification.useful, 4),
    "Meshlink Cape": ItemData(592411, ItemClassification.useful, 4),
    "Sagecaller Cape": ItemData(592412, ItemClassification.useful, 4),
    "Roudon Cape": ItemData(592413, ItemClassification.useful, 4),
    "Blueversa Cape": ItemData(592414, ItemClassification.useful, 4),
    "Greenversa Cape": ItemData(592415, ItemClassification.useful, 4),
    "Nulversa Cape": ItemData(592416, ItemClassification.useful, 4),
    "Redversa Cape": ItemData(592417, ItemClassification.useful, 4),

    # Armor - Capes - Tier 5 (Levels 21-26)
    "Windgolem Cloak": ItemData(592418, ItemClassification.useful, 5),
    "Mekwar Drape": ItemData(592419, ItemClassification.useful, 5),


    # Armor - Chestpieces - Tier 1 (Levels 1-5)
    "Aero Top": ItemData(592200, ItemClassification.useful, 1),
    "Bunhost Garb": ItemData(592201, ItemClassification.filler),
    "Festive Coat": ItemData(592202, ItemClassification.filler),
    "Fisher Overalls": ItemData(592203, ItemClassification.filler),
    "Leather Top": ItemData(592204, ItemClassification.useful, 1),
    "Necro Marrow": ItemData(592205, ItemClassification.useful, 1),
    "Noble Shirt": ItemData(592206, ItemClassification.filler),
    "Nutso Top": ItemData(592207, ItemClassification.useful, 1),
    "Orefinder Vest": ItemData(592208, ItemClassification.filler),
    "Ritualist Garb": ItemData(592209, ItemClassification.filler),
    "Sagecloth Top": ItemData(592210, ItemClassification.useful, 1),
    "Silken Top": ItemData(592211, ItemClassification.filler),
    "Spooky Garment": ItemData(592212, ItemClassification.filler),
    "Vampiric Coat": ItemData(592213, ItemClassification.filler),
    "Ghostly Tabard": ItemData(592214, ItemClassification.useful, 1),
    "Poacher Cloth": ItemData(592215, ItemClassification.useful, 1),
    "Ragged Shirt": ItemData(592216, ItemClassification.useful, 1),
    "Slimecrust Chest": ItemData(592217, ItemClassification.useful, 1),
    "Worn Robe": ItemData(592218, ItemClassification.useful, 1),
    "Cryptsinge Chest": ItemData(592219, ItemClassification.useful, 1),
    "Journeyman Vest": ItemData(592220, ItemClassification.useful, 1),
    "Slimek Chest": ItemData(592221, ItemClassification.useful, 1),

    # Armor - Chestpieces - Tier 2 (Levels 6-10)
    "Dense Chestpiece": ItemData(592222, ItemClassification.useful, 2),
    "Trodd Tunic": ItemData(592223, ItemClassification.useful, 2),
    "Iron Chestpiece": ItemData(592224, ItemClassification.useful, 2),
    "Tattered Battlerobe": ItemData(592225, ItemClassification.useful, 2),
    "Apprentice Robe": ItemData(592226, ItemClassification.useful, 2),
    "Duelist Garb": ItemData(592227, ItemClassification.useful, 2),
    "Skywrill Tabard": ItemData(592228, ItemClassification.useful, 2),
    "Sleeper's Robe": ItemData(592229, ItemClassification.useful, 2),
    "Warrior Chest": ItemData(592230, ItemClassification.useful, 2),

    # Armor - Chestpieces - Tier 3 (Levels 11-15)
    "Amberite Breastplate": ItemData(592231, ItemClassification.useful, 3),
    "Golem Chestpiece": ItemData(592232, ItemClassification.useful, 3),
    "Lord Breastplate": ItemData(592233, ItemClassification.useful, 3, "F"),
    "Nethercrypt Tabard": ItemData(592234, ItemClassification.useful, 3),
    "Reapsow Garb": ItemData(592235, ItemClassification.useful, 3, "B"),
    "Witchlock Robe": ItemData(592236, ItemClassification.useful, 3, "M"),
    "Chainmail Guard": ItemData(592237, ItemClassification.useful, 3),
    "Ornamented Battlerobe": ItemData(592238, ItemClassification.useful, 3),

    # Armor - Chestpieces - Tier 4 (Levels 16-20)
    "Carbuncle Robe": ItemData(592239, ItemClassification.useful, 4),
    "Chainscale Chest": ItemData(592240, ItemClassification.useful, 4),
    "Gemveil Raiment": ItemData(592241, ItemClassification.useful, 4),
    "King Breastplate": ItemData(592242, ItemClassification.useful, 4, "F"),
    "Mercenary Vestment": ItemData(592243, ItemClassification.useful, 4),
    "Mithril Chestpiece": ItemData(592244, ItemClassification.useful, 4),
    "Reaper Gi": ItemData(592245, ItemClassification.useful, 4, "B"),
    "Witchwizard Robe": ItemData(592246, ItemClassification.useful, 4, "M"),
    "Berserker Chestpiece": ItemData(592247, ItemClassification.useful, 4, "F"),
    "Fuguefall Duster": ItemData(592248, ItemClassification.useful, 4, "B"),
    "Magilord Overalls": ItemData(592249, ItemClassification.useful, 4, "M"),
    "Monolith Chestpiece": ItemData(592250, ItemClassification.useful, 4),
    "Sapphite Guard": ItemData(592251, ItemClassification.useful, 4),
    "Druidic Robe": ItemData(592252, ItemClassification.useful, 4),
    "Emerock Chestpiece": ItemData(592253, ItemClassification.useful, 4),
    "Fortified Vestment": ItemData(592254, ItemClassification.useful, 4),
    "Roudon Chestpiece": ItemData(592255, ItemClassification.useful, 4),

    # Armor - Chestpieces - Tier 5 (Levels 21-26)
    "Earthbind Tabard": ItemData(592256, ItemClassification.useful, 5),
    "Gemveil Breastplate": ItemData(592257, ItemClassification.useful, 5),
    "Roudon Robe": ItemData(592258, ItemClassification.useful, 5),
    "Ruggrok Vest": ItemData(592259, ItemClassification.useful, 5),
    "Executioner Vestment": ItemData(592260, ItemClassification.useful, 5, "F"),
    "Fender Garb": ItemData(592261, ItemClassification.useful, 5, "B"),
    "Wizlad Robe": ItemData(592262, ItemClassification.useful, 5, "M"),


    # Armor - Leggings - Tier 1 (Levels 1-5)
    "Aero Pants": ItemData(592300, ItemClassification.useful, 1),
    "Bunhost Leggings": ItemData(592301, ItemClassification.filler),
    "Festive Trousers": ItemData(592302, ItemClassification.filler),
    "Leather Britches": ItemData(592303, ItemClassification.useful, 1),
    "Necro Caustics": ItemData(592304, ItemClassification.useful, 1),
    "Noble Pants": ItemData(592305, ItemClassification.filler),
    "Nutso Pants": ItemData(592306, ItemClassification.useful, 1),
    "Orefinder Trousers": ItemData(592307, ItemClassification.filler),
    "Ritualist Straps": ItemData(592308, ItemClassification.filler),
    "Sagecloth Shorts": ItemData(592309, ItemClassification.useful, 1),
    "Silken Loincloth": ItemData(592310, ItemClassification.filler),
    "Vampiric Leggings": ItemData(592311, ItemClassification.filler),
    "Ghostly Legwraps": ItemData(592312, ItemClassification.useful, 1),
    "Journeyman Shorts": ItemData(592313, ItemClassification.useful, 1),
    "Slimecrust Leggings": ItemData(592314, ItemClassification.useful, 1),
    "Journeyman Leggings": ItemData(592315, ItemClassification.useful, 1),
    "Slimek Leggings": ItemData(592316, ItemClassification.useful, 1),

    # Armor - Leggings - Tier 2 (Levels 6-10)
    "Dense Leggings": ItemData(592317, ItemClassification.useful, 2),
    "Sash Leggings": ItemData(592318, ItemClassification.useful, 2),
    "Warrior Leggings": ItemData(592319, ItemClassification.useful, 2),

    # Armor - Leggings - Tier 3 (Levels 11-15)
    "Amberite Leggings": ItemData(592320, ItemClassification.useful, 3),
    "Chainmail Leggings": ItemData(592321, ItemClassification.useful, 3),
    "Darkcloth Pants": ItemData(592322, ItemClassification.useful, 3),
    "Lord Greaves": ItemData(592323, ItemClassification.useful, 3, "F"),
    "Reapsow Pants": ItemData(592324, ItemClassification.useful, 3, "B"),
    "Witchlock Loincloth": ItemData(592325, ItemClassification.useful, 3, "M"),

    # Armor - Leggings - Tier 4 (Levels 16-20)
    "King Greaves": ItemData(592326, ItemClassification.useful, 4, "F"),
    "Mercenary Leggings": ItemData(592327, ItemClassification.useful, 4),
    "Reaper Leggings": ItemData(592328, ItemClassification.useful, 4, "B"),
    "Stridebond Pants": ItemData(592329, ItemClassification.useful, 4),
    "Witchwizard Garterbelt": ItemData(592330, ItemClassification.useful, 4, "M"),
    "Berserker Leggings": ItemData(592331, ItemClassification.useful, 4, "F"),
    "Fuguefall Pants": ItemData(592332, ItemClassification.useful, 4, "B"),
    "Magilord Boots": ItemData(592333, ItemClassification.useful, 4, "M"),
    "Sapphite Leggings": ItemData(592334, ItemClassification.useful, 4),
    "Jadewail Trousers": ItemData(592335, ItemClassification.useful, 4),
    "Temrak Britches": ItemData(592336, ItemClassification.useful, 4),

    # Armor - Leggings - Tier 5 (Levels 21-26)
    "Eschek Greaves": ItemData(592337, ItemClassification.useful, 5),
    "Gemveil Leggings": ItemData(592338, ItemClassification.useful, 5),
    "Executioner Leggings": ItemData(592339, ItemClassification.useful, 5, "F"),
    "Fender Leggings": ItemData(592340, ItemClassification.useful, 5, "B"),


    # Armor - Shields - Tier 1 (Levels 1-5)
    "Wooden Shield": ItemData(592500, ItemClassification.useful, 1, "FM"),
    "Crypt Buckler": ItemData(592501, ItemClassification.useful, 1, "FM"),
    "Slimek Shield": ItemData(592502, ItemClassification.useful, 1, "FM"),

    # Armor - Shields - Tier 2 (Levels 6-10)
    "Demicrypt Buckler": ItemData(592503, ItemClassification.useful, 2, "FM"),
    "Dense Shield": ItemData(592504, ItemClassification.useful, 2, "FM"),
    "Iron Shield": ItemData(592505, ItemClassification.useful, 2, "FM"),
    "Iris Shield": ItemData(592506, ItemClassification.useful, 2, "FM"),
    "Omen Shield": ItemData(592507, ItemClassification.useful, 2, "FM"),

    # Armor - Shields - Tier 3 (Levels 11-15)
    "Amberite Shield": ItemData(592508, ItemClassification.useful, 3, "FM"),
    "Slabton Shield": ItemData(592509, ItemClassification.useful, 3, "FM"),
    "Mithril Shield": ItemData(592510, ItemClassification.useful, 3, "FM"),
    "Nethercrypt Shield": ItemData(592511, ItemClassification.useful, 3, "FM"),

    # Armor - Shields - Tier 4 (Levels 16-20)
    "Rustweary Shield": ItemData(592512, ItemClassification.useful, 4, "FM"),
    "Rustwise Shield": ItemData(592513, ItemClassification.useful, 4, "FM"),
    "Sapphite Shield": ItemData(592514, ItemClassification.useful, 4, "FM"),
    "Rigor Buckler": ItemData(592515, ItemClassification.useful, 4, "FM"),

    # Armor - Shields - Tier 5 (Levels 21-26)
    "Daemon Shield": ItemData(592516, ItemClassification.useful, 5, "FM"),
    "Irisun Shield": ItemData(592517, ItemClassification.useful, 5, "FM"),


    # Accessories - Trinkets - Tier 1 (Levels 1-5)
    "Old Ring": ItemData(592600, ItemClassification.useful, 1),
    "Ring Of Ambition": ItemData(592601, ItemClassification.useful, 1),
    "Nograd's Amulet": ItemData(592602, ItemClassification.useful, 1),
    "The One Ring": ItemData(592603, ItemClassification.useful, 1),

    # Accessories - Trinkets - Tier 2 (Levels 6-10)
    "Ambersquire Ring": ItemData(592604, ItemClassification.useful, 2),
    "Emeraldfocus Ring": ItemData(592605, ItemClassification.useful, 2),
    "Sapphireweave Ring": ItemData(592606, ItemClassification.useful, 2),
    "Edon's Pendant": ItemData(592607, ItemClassification.useful, 2),

    # Accessories - Trinkets - Tier 3 (Levels 11-15)
    "Geistlord Ring": ItemData(592608, ItemClassification.useful, 3),
    "Students Ring": ItemData(592609, ItemClassification.useful, 3),
    "Pearlpond Ring": ItemData(592610, ItemClassification.useful, 3),
    "Slitherwraith Ring": ItemData(592611, ItemClassification.useful, 3),

    # Accessories - Trinkets - Tier 4 (Levels 16-20)
    "Geistlord Band": ItemData(592612, ItemClassification.useful, 4),
    "Jadetrout Ring": ItemData(592613, ItemClassification.useful, 4),
    "Orbos Ring": ItemData(592614, ItemClassification.useful, 4),
    "Valor Ring": ItemData(592615, ItemClassification.useful, 4),
    "Earthwoken Ring": ItemData(592616, ItemClassification.useful, 4),
    "Noji Talisman": ItemData(592617, ItemClassification.useful, 4),

    # Accessories - Trinkets - Tier 5 (Levels 21-26)
    "Valdur Effigy": ItemData(592618, ItemClassification.useful, 5),
    "Glyphik Booklet": ItemData(592619, ItemClassification.useful, 5),
    "Tessellated Drive": ItemData(592620, ItemClassification.useful, 5),

    # Currency (FILLER)
    "Crowns (Small)": ItemData(591490, ItemClassification.filler),
    "Crowns (Medium)": ItemData(591491, ItemClassification.filler),
    "Crowns (Large)": ItemData(591492, ItemClassification.filler),
    "Crowns (Huge)": ItemData(591493, ItemClassification.filler),

    # Portal Unlocks (ALL PROGRESSION - 11 total, used in Random Portals mode)
    "Outer Sanctum Portal": ItemData(591500, ItemClassification.progression),
    "Effold Terrace Portal": ItemData(591501, ItemClassification.progression),
    "Arcwood Pass Portal": ItemData(591502, ItemClassification.progression),
    "Tull Valley Portal": ItemData(591503, ItemClassification.progression),
    "Crescent Road Portal": ItemData(591504, ItemClassification.progression),
    "Catacombs Portal": ItemData(591505, ItemClassification.progression),
    "Crescent Keep Portal": ItemData(591507, ItemClassification.progression),
    "Tull Enclave Portal": ItemData(591508, ItemClassification.progression),
    "Bularr Fortress Portal": ItemData(591509, ItemClassification.progression),
    "Grove Portal": ItemData(591510, ItemClassification.progression),

    # Progressive Portal (used in default progressive mode)
    "Progressive Portal": ItemData(591700, ItemClassification.progression),

    # REMOVED: "Progressive Equipment" (591701) — equipment is now gated by
    # level requirements instead of progressive unlocks.

    # Trade Items - Monster Drops (FILLER)
    "Aqua Muchroom Cap": ItemData(591600, ItemClassification.filler),
    "Barknaught Face": ItemData(591601, ItemClassification.filler),
    "Blightwood Log": ItemData(591602, ItemClassification.filler),
    "Blightwood Stick": ItemData(591603, ItemClassification.filler),
    "Blue Minchroom Cap": ItemData(591604, ItemClassification.filler),
    "Boomboar Gear": ItemData(591605, ItemClassification.filler),
    "Boomboar Head": ItemData(591606, ItemClassification.filler),
    "Boomboar Pouch": ItemData(591607, ItemClassification.filler),
    "Burnrose": ItemData(591608, ItemClassification.filler),
    "Carbuncle Foot": ItemData(591609, ItemClassification.filler),
    "Cursed Note": ItemData(591610, ItemClassification.filler),
    "Deadwood Log": ItemData(591611, ItemClassification.filler),
    "Deathgel Core": ItemData(591612, ItemClassification.filler),
    "Deathknight Gauntlet": ItemData(591613, ItemClassification.filler),
    "Demigolem Core": ItemData(591614, ItemClassification.filler),
    "Demigolem Gem": ItemData(591615, ItemClassification.filler),
    "Diva Necklace": ItemData(591616, ItemClassification.filler),
    "Firebreath Gland": ItemData(591617, ItemClassification.filler),
    "Fluxfern": ItemData(591618, ItemClassification.filler),
    "Gale Muchroom Cap": ItemData(591619, ItemClassification.filler),
    "Geist Collar": ItemData(591620, ItemClassification.filler),
    "Ghostdust": ItemData(591621, ItemClassification.filler),
    "Golem Core": ItemData(591622, ItemClassification.filler),
    "Golem Gem": ItemData(591623, ItemClassification.filler),
    "Green Lipstick": ItemData(591624, ItemClassification.filler),
    "Hellsludge Core": ItemData(591625, ItemClassification.filler),
    "Maw Eye": ItemData(591626, ItemClassification.filler),
    "Mekboar Head": ItemData(591627, ItemClassification.filler),
    "Mekboar Spear": ItemData(591628, ItemClassification.filler),
    "Mekboar Nail": ItemData(591629, ItemClassification.filler),
    "Mekboar Nosering": ItemData(591630, ItemClassification.filler),
    "Mekboar Spine": ItemData(591631, ItemClassification.filler),
    "Monolith Core": ItemData(591632, ItemClassification.filler),
    "Monolith Gem": ItemData(591633, ItemClassification.filler),
    "Mouth Bittertooth": ItemData(591634, ItemClassification.filler),
    "Mouth Eye": ItemData(591635, ItemClassification.filler),
    "Rageboar Head": ItemData(591636, ItemClassification.filler),
    "Rageboar Spear": ItemData(591637, ItemClassification.filler),
    "Red Minchroom Cap": ItemData(591638, ItemClassification.filler),
    "Rock": ItemData(591639, ItemClassification.filler),
    "Slime Core": ItemData(591640, ItemClassification.filler),
    "Slime Diva Ears": ItemData(591641, ItemClassification.filler),
    "Slime Ears": ItemData(591642, ItemClassification.filler),
    "Slimek Core": ItemData(591643, ItemClassification.filler),
    "Slimek Ears": ItemData(591644, ItemClassification.filler),
    "Slimek Eye": ItemData(591645, ItemClassification.filler),
    "Vinethorn": ItemData(591646, ItemClassification.filler),
    "Vout Antennae": ItemData(591647, ItemClassification.filler),
    "Vout Wing": ItemData(591648, ItemClassification.filler),
    "Warboar Axe": ItemData(591649, ItemClassification.filler),
    "Warboar Head": ItemData(591650, ItemClassification.filler),
    "Wizboar Head": ItemData(591651, ItemClassification.filler),
    "Wizboar Scepter": ItemData(591652, ItemClassification.filler),
    "Geistlord Nails": ItemData(591653, ItemClassification.filler),

    # Trade Items - Ores/Ingots (FILLER)
    "Amberite Ingot": ItemData(591654, ItemClassification.filler),
    "Amberite Ore": ItemData(591655, ItemClassification.filler),
    "Dense Ingot": ItemData(591656, ItemClassification.filler),
    "Dense Ore": ItemData(591657, ItemClassification.filler),
    "Copper Cluster": ItemData(591658, ItemClassification.filler),
    "Iron Cluster": ItemData(591659, ItemClassification.filler),
    "Mithril Cluster": ItemData(591660, ItemClassification.filler),
    "Sapphite Ingot": ItemData(591661, ItemClassification.filler),
    "Sapphite Ore": ItemData(591662, ItemClassification.filler),
    "Coal": ItemData(591663, ItemClassification.filler),

    # Trade Items - Fish (FILLER)
    "Big Wan": ItemData(591664, ItemClassification.filler),
    "Bittering Katfish": ItemData(591665, ItemClassification.filler),
    "Bonefish": ItemData(591666, ItemClassification.filler),
    "Smiling Wrellfish": ItemData(591667, ItemClassification.filler),
    "Squangfish": ItemData(591668, ItemClassification.filler),
    "Sugeel": ItemData(591669, ItemClassification.filler),
    "Sugshrimp": ItemData(591670, ItemClassification.filler),
    "Windtail Fish": ItemData(591671, ItemClassification.filler),
    "Old Boot": ItemData(591672, ItemClassification.filler),
    "Bronze Arrows": ItemData(591673, ItemClassification.filler),

    # Trade Items - Special (Badges are USEFUL, rest vary)
    "Agility Stone": ItemData(591674, ItemClassification.filler),
    "Angela's Tear": ItemData(591675, ItemClassification.filler),
    "Coldgeist Badge": ItemData(591676, ItemClassification.useful),
    "Earthcore Badge": ItemData(591677, ItemClassification.useful),
    "Epic Carrot": ItemData(591678, ItemClassification.filler),
    "Experience Bond": ItemData(591679, ItemClassification.useful),
    "Flux Stone": ItemData(591680, ItemClassification.filler),
    "Geistlord Badge": ItemData(591681, ItemClassification.useful),
    "Illusion Stone": ItemData(591682, ItemClassification.filler),
    "Might Stone": ItemData(591683, ItemClassification.filler),
    "Soul Pearl": ItemData(591684, ItemClassification.useful),
    "Windcore Badge": ItemData(591685, ItemClassification.useful),
    "Starlight Gem": ItemData(591686, ItemClassification.filler),
}