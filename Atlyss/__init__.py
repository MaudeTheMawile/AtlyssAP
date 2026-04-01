from typing import Any, Dict, List, Set
from BaseClasses import ItemClassification
from worlds.AutoWorld import World, WebWorld
from .items import item_table, ItemData, ATLYSSItem
from .locations import location_table, LocationData, ATLYSSLocation
from .options import ATLYSSOptions
from .regions import create_regions
from .rules import set_rules, set_completion_rules, level_to_max_tier, REGION_MAX_TIER, get_menu_location_effective_level


class ATLYSSWeb(WebWorld):
    """Web configuration for ATLYSS."""
    theme = "stone"
    tutorials = []


class ATLYSSWorld(World):
    """
    ATLYSS is a 3D action RPG where you explore dungeons, complete quests, defeat bosses,
    and grow stronger. In Archipelago multiworld, items are scattered across all players'
    worlds, requiring cooperation to complete everyone's goals.
    """
    
    game = "ATLYSS"
    web = ATLYSSWeb()
    options_dataclass = ATLYSSOptions
    options: ATLYSSOptions
    
    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.code for name, data in location_table.items()}

    # Class filter value -> set of affinity chars that pass
    CLASS_FILTER_MAP = {
        0: None,  # all classes, no filtering
        1: {"F"},
        2: {"M"},
        3: {"B"},
        4: {"F", "M"},
        5: {"F", "B"},
        6: {"M", "B"},
    }

    def _item_passes_class_filter(self, item_name: str) -> bool:
        """Check if an item passes the current class filter.
        Items with no class_affinity (universal) always pass.
        Items with class_affinity pass if any of their affinities match the filter.
        """
        selected = self.CLASS_FILTER_MAP.get(self.options.class_filter.value)
        if selected is None:
            return True  # all classes mode

        item_data = item_table.get(item_name)
        if item_data is None:
            return True

        affinity = item_data.class_affinity
        if affinity is None:
            return True  # universal item

        # Check if any character in the affinity string matches selected classes
        # e.g. "FM" passes if "F" in selected or "M" in selected
        return bool(set(affinity) & selected)

    def create_regions(self):
        """Create all regions, locations, and entrances."""
        create_regions(self)
        
        # Set access rules and completion conditions
        set_rules(self)
        set_completion_rules(self)

    def _compute_tier_budgets(self) -> Dict[int, int]:
        """Compute cumulative tier budgets from location data.
        
        Returns a dict where tier_budgets[T] = max number of tier T+ items
        that can coexist in the pool without overflowing the fill algorithm.
        
        The constraint: items of tier T can only be placed at locations with
        max_tier >= T. So the total items of tier T or higher must not exceed
        the total locations with max_tier >= T.
        """
        tier_location_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        
        for loc_name, loc_data in location_table.items():
            # Skip junk-only locations — they only accept filler
            if (loc_name.startswith("Fishing Level ") or
                loc_name.startswith("Mining Level ") or
                loc_name in ("Reach Level 28", "Reach Level 30", "Reach Level 32")):
                continue
            
            region_name = loc_data.region
            if region_name == "Menu":
                effective_level = get_menu_location_effective_level(loc_name)
                max_tier = level_to_max_tier(effective_level)
            else:
                max_tier = REGION_MAX_TIER.get(region_name, 1)
            tier_location_counts[max_tier] += 1
        
        # Cumulative: tier_budgets[T] = count of locations with max_tier >= T
        cumulative = {}
        running = 0
        for t in range(5, 0, -1):
            running += tier_location_counts[t]
            cumulative[t] = running
        
        return cumulative

    def create_items(self):
        """Generate the item pool - must match FILLABLE location count exactly.
        
        UPDATED: In Gated mode, item selection is now tier-budget-aware.
        With 311 equipment items across 5 tiers but only 152 locations,
        naive random selection can pick more high-tier items than there
        are high-tier locations, causing a FillError.
        
        Fix: shuffle all items randomly but skip any tiered equipment that
        would exceed its tier's cumulative location budget. This preserves
        variety (trade items, cosmetics mixed in) while preventing overflow.
        Non-tiered items (cosmetics, trade, filler) have tier=None and can
        go in any location, so they don't contribute to tier constraints.
        
        ALSO: Junk-only locations (fishing/mining levels, high level milestones)
        are EXCLUDED and can only hold filler items. The pool must contain at
        least as many filler items as junk locations, or the fill will fail.
        A non-filler cap prevents useful items from consuming all slots.
        """
        total_locations = len(location_table)
        item_pool: List[ATLYSSItem] = []
        
        # --- PORTAL ITEMS ---
        individual_portals = [
            "Outer Sanctum Portal",
            "Arcwood Pass Portal",
            "Catacombs Portal",
            "Effold Terrace Portal",
            "Tull Valley Portal",
            "Crescent Road Portal",
            "Crescent Keep Portal",
            "Tull Enclave Portal",
            "Grove Portal",
            "Bularr Fortress Portal",
        ]
        
        random_portals = self.options.random_portals.value
        
        if random_portals:
            for portal_name in individual_portals:
                item = self.create_item(portal_name)
                item.classification = ItemClassification.progression
                item_pool.append(item)
        else:
            for _ in range(10):
                item = self.create_item("Progressive Portal")
                item_pool.append(item)
        
        # --- ALL OTHER ITEMS (equipment + non-equipment) ---
        excluded_items = set(individual_portals) | {"Progressive Portal"}
        equipment_progression = self.options.equipment_progression.value
        all_items = [name for name in item_table.keys() if name not in excluded_items]
        self.random.shuffle(all_items)
        
        # Compute how many junk-only locations exist (EXCLUDED — can only hold filler).
        # We must ensure the pool has enough filler items to fill these, or AP's fill
        # algorithm will fail with a FillError when it can't place useful items there.
        junk_location_names = [
            name for name in location_table
            if (name.startswith("Fishing Level ") or
                name.startswith("Mining Level ") or
                name in ("Reach Level 28", "Reach Level 30", "Reach Level 32"))
        ]
        junk_location_count = len(junk_location_names)
        
        # Non-filler items (progression + useful) can only go in non-junk locations.
        # Cap non-filler count so the filler loop can fill junk locations.
        max_non_filler = total_locations - junk_location_count
        non_filler_count = len(item_pool)  # portals already added are non-filler
        
        if equipment_progression == 0:
            # GATED MODE: Tier-budget-aware selection.
            # Shuffle all items randomly, but track tier counts and skip any
            # tiered equipment that would exceed the cumulative location budget.
            # Non-tiered items (tier=None) are always accepted since they can
            # go in any location without affecting tier constraints.
            
            tier_budgets = self._compute_tier_budgets()
            
            # Track how many items of each tier we've selected
            tier_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
            
            for item_name in all_items:
                if len(item_pool) >= total_locations:
                    break
                
                # Class filter: skip equipment not matching selected classes
                if not self._item_passes_class_filter(item_name):
                    continue
                
                item_data = item_table[item_name]
                is_filler = (item_data.classification == ItemClassification.filler)
                
                # Skip non-filler items if we've hit the cap — need room for
                # junk locations which can ONLY hold filler items
                if not is_filler and non_filler_count >= max_non_filler:
                    continue
                
                tier = item_data.tier
                if tier is not None and tier in tier_counts:
                    # Adding a tier T item increases cumulative counts at ALL
                    # tiers 1 through T (since tier T+ includes tier T).
                    # Check every affected cumulative constraint.
                    would_overflow = False
                    for check_tier in range(1, tier + 1):
                        cumul = sum(tier_counts[t] for t in range(check_tier, 6))
                        if cumul + 1 > tier_budgets[check_tier]:
                            would_overflow = True
                            break
                    
                    if would_overflow:
                        continue  # skip this item, would overflow
                    
                    tier_counts[tier] += 1
                
                if not is_filler:
                    non_filler_count += 1
                
                item_pool.append(self.create_item(item_name))
        
        else:
            # RANDOM MODE: No tier restrictions, select items freely.
            # Still enforces non-filler cap for junk-only locations.
            for item_name in all_items:
                if len(item_pool) >= total_locations:
                    break
                
                # Class filter: skip equipment not matching selected classes
                if not self._item_passes_class_filter(item_name):
                    continue
                
                is_filler = (item_table[item_name].classification == ItemClassification.filler)
                if not is_filler and non_filler_count >= max_non_filler:
                    continue
                
                if not is_filler:
                    non_filler_count += 1
                
                item_pool.append(self.create_item(item_name))
        
        # --- FILLER ITEMS ---
        filler_options = [
            ("Crowns (Small)", 20),
            ("Crowns (Medium)", 14),
            ("Crowns (Large)", 8),
            ("Crowns (Huge)", 4),
            ("Bunbag Pack", 4),
            ("Bunjar Pack", 3),
            ("Bunpot Pack", 2),
            ("Regen Vial Pack", 4),
            ("Regen Potion Pack", 2),
            ("Magiclove Pack", 3),
            ("Magiflower Pack", 2),
            ("Magileaf Pack", 2),
            ("Stamstar Pack", 3),
            ("Agility Vial Pack", 2),
            ("Agility Potion Pack", 1),
            ("Bolster Vial Pack", 2),
            ("Bolster Potion Pack", 1),
            ("Wisdom Vial Pack", 2),
            ("Wisdom Potion Pack", 1),
            ("Carrot Cake Pack", 2),
            ("Minchroom Juice Pack", 2),
            ("Spectral Powder Pack", 2),
            ("Tome of Lesser Experience", 2),
            ("Tome of Experience", 1),
            ("Tome of Greater Experience", 1),
        ]
        
        filler_names = [name for name, _ in filler_options]
        filler_weights = [weight for _, weight in filler_options]
        
        while len(item_pool) < total_locations:
            chosen = self.random.choices(filler_names, weights=filler_weights, k=1)[0]
            item_pool.append(self.create_item(chosen))
        
        item_pool = item_pool[:total_locations]
        self.multiworld.itempool += item_pool
        
        if not random_portals:
            self.multiworld.early_items[self.player]["Progressive Portal"] = 3

    def pre_fill(self):
        """Pre-place tiered equipment at valid locations before AP's main fill.
        
        In Gated mode, item_rules restrict tiered equipment to locations with
        a matching max_tier. But AP's fill also places non-tiered items (which
        pass all item_rules) at those same locations, consuming the slots.
        This displacement causes FillError when tiered items have no valid
        locations left.
        
        Fix: manually place all tiered equipment BEFORE AP's fill runs.
        This guarantees tiered items get valid slots. AP's fill then only
        handles non-tiered items and filler, which have no tier restrictions.
        """
        if self.options.equipment_progression.value != 0:
            return  # Only needed for Gated mode
        
        # Separate tiered items from the pool
        tiered_items: List[ATLYSSItem] = []
        remaining_pool: List[ATLYSSItem] = []
        
        for item in self.multiworld.itempool:
            if (item.player == self.player and
                item.name in item_table and
                item_table[item.name].tier is not None):
                tiered_items.append(item)
            else:
                remaining_pool.append(item)
        
        if not tiered_items:
            return
        
        # Build a list of (location, max_tier) for all unfilled non-junk locations
        junk_prefixes = ("Fishing Level ", "Mining Level ")
        junk_names = {"Reach Level 28", "Reach Level 30", "Reach Level 32"}
        
        location_slots: List[tuple] = []
        for loc in self.multiworld.get_unfilled_locations(self.player):
            if (loc.name.startswith(junk_prefixes) or loc.name in junk_names):
                continue  # skip junk-only locations
            
            loc_data = location_table.get(loc.name)
            if loc_data is None:
                continue
            
            region_name = loc_data.region
            if region_name == "Menu":
                effective_level = get_menu_location_effective_level(loc.name)
                max_tier = level_to_max_tier(effective_level)
            else:
                max_tier = REGION_MAX_TIER.get(region_name, 1)
            
            location_slots.append((loc, max_tier))
        
        # Shuffle locations for variety, then sort by max_tier DESCENDING.
        # This makes highest-tier slots fill first, preventing low-tier items
        # from consuming high-tier slots unnecessarily.
        self.random.shuffle(location_slots)
        location_slots.sort(key=lambda x: x[1], reverse=True)
        
        # Shuffle tiered items, then sort by tier DESCENDING.
        # Place hardest-to-place items (highest tier) first.
        self.random.shuffle(tiered_items)
        tiered_items.sort(key=lambda i: item_table[i.name].tier, reverse=True)
        
        # Place each tiered item at a valid location
        used_indices: Set[int] = set()
        placed_count = 0
        
        for item in tiered_items:
            tier = item_table[item.name].tier
            placed = False
            
            for i, (loc, max_tier) in enumerate(location_slots):
                if i in used_indices:
                    continue
                if max_tier >= tier:
                    loc.place_locked_item(item)
                    used_indices.add(i)
                    placed = True
                    placed_count += 1
                    break
            
            if not placed:
                # Shouldn't happen if tier budget is correct, but safety fallback
                remaining_pool.append(item)
        
        # Update the pool — only non-tiered items remain for AP's fill
        self.multiworld.itempool = remaining_pool

    def create_item(self, name: str) -> ATLYSSItem:
        """Create an item by name."""
        item_data = item_table[name]
        return ATLYSSItem(name, item_data.classification, item_data.code, self.player)

    def set_rules(self):
        """Set rules - handled in rules.py via set_rules() and set_completion_rules()."""
        pass

    def fill_slot_data(self) -> Dict[str, Any]:
        """Return slot data sent to the client mod."""
        return {
            "goal": self.options.goal.value,
            "random_portals": int(self.options.random_portals.value),
            "equipment_progression": self.options.equipment_progression.value,
            "shop_sanity": int(self.options.shop_sanity.value),
            "class_filter": self.options.class_filter.value,
        }