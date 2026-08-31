# game/Utilities/General/NPC/HouseholdAI_ren.rpy

init 5 python:

    def household_ai_float(value, default=0.0):
        try:
            return float(value)
        except Exception:
            return float(default)

    def household_ai_int(value, default=0):
        try:
            return int(value)
        except Exception:
            try:
                return int(float(value))
            except Exception:
                return int(default)

    def household_ai_clamp(value, low=0.0, high=1.0):
        return max(float(low), min(float(high), household_ai_float(value, low)))

    def household_ai_seen_key(event_code="", location_code=""):
        return "%s|%s|%s|%s" % (
            current_game_day(),
            household_ai_int(calendar_v2.time_slot(), 0),
            str(location_code or rooms.current_code or ""),
            str(event_code or ""),
        )

    def household_ai_seen(event_code="", location_code=""):
        return household_ai_int(household.seen.get(household_ai_seen_key(event_code, location_code), 0), 0) == 1

    def household_ai_mark_seen(event_code="", location_code=""):
        household.seen[household_ai_seen_key(event_code, location_code)] = 1
        household.meta["last_event_day"] = current_game_day()
        household.meta["last_event_slot"] = household_ai_int(calendar_v2.time_slot(), 0)
        household.meta["last_event_code"] = str(event_code or "")

    def household_ai_resource_pressure():
        """
        Scarcity pressure.
        Player success lowers pressure.
        Low money / dirty tavern / weak supplies raise it.
        """
        money_pressure = 1.0 if household_ai_int(player.economy.money, 0) < 150 else 0.65 if household_ai_int(player.economy.money, 0) < 500 else 0.25

        clean_value = household_ai_int(player.tavern_management.cleanliness, 0)
        dirt_pressure = 1.0 if clean_value < 20 else 0.55 if clean_value < 45 else 0.15

        food_value = household_ai_int(player.tavern_management.productnum, 0) + household_ai_int(tavern_kitchen_food_stock_count(), 0)
        fur_value = sum(
            household_ai_int(player.item_count(item_id), 0)
            for item_id in (
                "wolf_skin_001",
                "white_wolf_skin_001",
                "bear_fur_brown_001",
                "bear_fur_grizzly_001",
                "warm_fur_cloak_001",
                "fur_bedroll_001",
            )
        )
        cloth_value = household_ai_int(player.item_count("cloth_scrap_001"), 0)

        supply_pressure = 0.0
        if food_value <= 0:
            supply_pressure += 0.45
        if fur_value <= 0:
            supply_pressure += 0.15
        if cloth_value <= 0:
            supply_pressure += 0.15

        return household_ai_clamp((money_pressure * 0.45) + (dirt_pressure * 0.30) + supply_pressure)

    def household_ai_update_meta():
        pressure = household_ai_resource_pressure()
        meta = household.meta
        external = household_ai_clamp(meta.get("external_threat", 0.0), 0.0, 1.0)

        friction = household_ai_clamp(meta.get("friction", 0.2), 0.0, 1.0)
        convergence = household_ai_clamp(meta.get("convergence", 0.0), 0.0, 1.0)

        # Scarcity increases friction; stability lowers it.
        friction += pressure * 0.08
        friction += external * 0.04

        if pressure < 0.35:
            convergence += 0.05
            friction -= 0.04

        # External villains/threats should force cooperation instead of endless catfight.
        if external > 0.4:
            convergence += 0.06
            friction -= 0.03

        meta["pressure"] = household_ai_clamp(pressure)
        meta["friction"] = household_ai_clamp(friction)
        meta["convergence"] = household_ai_clamp(convergence)

        return meta

    def household_ai_update_npc_drive(npc_id):
        row = household_ai_npc_state(npc_id)
        meta = household.meta
        pressure = household_ai_clamp(meta.get("pressure", 0.0))
        friction = household_ai_clamp(meta.get("friction", 0.0))
        convergence = household_ai_clamp(meta.get("convergence", 0.0))
        external = household_ai_clamp(meta.get("external_threat", 0.0))

        resistance = household_ai_clamp(row.get("resistance", 0.5))
        drive = household_ai_clamp(row.get("drive", 0.0))

        drive += pressure * (1.0 - resistance) * 0.25
        drive += friction * 0.10
        drive += external * 0.08

        # Convergence calms them down.
        drive -= convergence * 0.10

        row["drive"] = household_ai_clamp(drive)
        return row

    def household_ai_npcs_present(location_code=""):
        loc = str(location_code or rooms.current_code or "")
        try:
            return list(people.ids_at(loc) or [])
        except Exception:
            return []

    def household_ai_context(location_code="", mode="room"):
        household_ai_update_meta()
        loc = str(location_code or rooms.current_code or "")
        present = household_ai_npcs_present(loc)

        for npc_id in ("amanda", "melissa", "sandra"):
            household_ai_update_npc_drive(npc_id)

        return {
            "location": loc,
            "mode": str(mode or "room"),
            "day": current_game_day(),
            "slot": household_ai_int(calendar_v2.time_slot(), 0),
            "hour": household_ai_int(calendar_v2.hour, 0),
            "present": present,
            "pressure": household_ai_clamp(household.meta.get("pressure", 0.0)),
            "friction": household_ai_clamp(household.meta.get("friction", 0.0)),
            "convergence": household_ai_clamp(household.meta.get("convergence", 0.0)),
            "external_threat": household_ai_clamp(household.meta.get("external_threat", 0.0)),
            "amanda": dict(household_ai_npc_state("amanda")),
            "melissa": dict(household_ai_npc_state("melissa")),
            "sandra": dict(household_ai_npc_state("sandra")),
        }

    def household_ai_pick_event(location_code="", mode="room"):
        ctx = household_ai_context(location_code, mode)
        loc = ctx["location"]
        present = ctx["present"]
        friction = ctx["friction"]
        pressure = ctx["pressure"]
        convergence = ctx["convergence"]

        amanda = ctx["amanda"]
        melissa = ctx["melissa"]
        sandra = ctx["sandra"]

        # Breakfast / kitchen chaos.
        if loc == "TavernKitchen":
            if "amanda" in present and "sandra" in present and friction >= 0.55:
                return "household_event_kitchen_amanda_sandra_spark"
            if "melissa" in present and "sandra" in present and pressure >= 0.50:
                return "household_event_kitchen_melissa_practical_complaint"
            if "amanda" in present and "melissa" in present and friction >= 0.45:
                return "household_event_breakfast_squirrel_mockery"

        # Player room / private pressure.
        if loc == "TavernMyRoom":
            if "amanda" in present and amanda.get("drive", 0.0) >= amanda.get("threshold", 0.6):
                return "household_event_amanda_private_pressure"
            if "sandra" in present and sandra.get("drive", 0.0) >= sandra.get("threshold", 0.58):
                return "household_event_sandra_private_check"

        # Convergence event: rare and good.
        if convergence >= 0.65 and pressure <= 0.35 and "amanda" in present and "melissa" in present and "sandra" in present:
            return "household_event_three_women_converge"

        return ""

    def household_ai_event_label(event_code=""):
        labels = {
            "household_event_kitchen_amanda_sandra_spark": "HouseholdEvent_KitchenAmandaSandraSpark",
            "household_event_kitchen_melissa_practical_complaint": "HouseholdEvent_KitchenMelissaPracticalComplaint",
            "household_event_breakfast_squirrel_mockery": "HouseholdEvent_BreakfastSquirrelMockery",
            "household_event_amanda_private_pressure": "HouseholdEvent_AmandaPrivatePressure",
            "household_event_sandra_private_check": "HouseholdEvent_SandraPrivateCheck",
            "household_event_three_women_converge": "HouseholdEvent_ThreeWomenConverge",
        }
        return labels.get(str(event_code or ""), "")

    def household_ai_reduce_drive(npc_id, amount=0.25):
        row = household_ai_npc_state(npc_id)
        row["drive"] = household_ai_clamp(row.get("drive", 0.0) - amount)

    def household_ai_raise_friction(amount=0.1):
        household.meta["friction"] = household_ai_clamp(household.meta.get("friction", 0.0) + amount)

    def household_ai_raise_convergence(amount=0.1):
        household.meta["convergence"] = household_ai_clamp(household.meta.get("convergence", 0.0) + amount)
    class HouseholdInfo(object):
        META_DEFAULTS = {
            "pressure": 0.0,
            "friction": 0.2,
            "convergence": 0.0,
            "external_threat": 0.0,
            "last_event_day": -1,
            "last_event_slot": -1,
            "last_event_code": "",
        }
        DICT_FIELDS = (
            "seen",
            "runtime_event_seen",
            "morning_state",
            "soap_request_last_day",
            "barber_request_last_day",
            "barber_appointments",
            "barber_visit_last_day",
            "warm_drink_last_day",
            "outfit_requests",
        )

        def __init__(self):
            self.meta = dict(self.META_DEFAULTS)
            for field_name in self.DICT_FIELDS:
                setattr(self, field_name, {})

        def repair(self):
            saved_meta = getattr(self, "meta", None)
            repaired_meta = dict(self.META_DEFAULTS)
            if isinstance(saved_meta, dict):
                repaired_meta.update(saved_meta)
            self.meta = repaired_meta
            for field_name in self.DICT_FIELDS:
                saved_value = getattr(self, field_name, None)
                if not isinstance(saved_value, dict):
                    saved_value = {}
                setattr(self, field_name, saved_value)
            return self

    HOUSEHOLD_NPC_DEFAULTS = {
        "amanda": {"drive": 0.0, "resistance": 0.75, "threshold": 0.62, "stability": 0.35, "rivalry": 0.65, "obedience": 0.45, "path": "undecided"},
        "melissa": {"drive": 0.0, "resistance": 0.45, "threshold": 0.50, "stability": 0.45, "rivalry": 0.35, "obedience": 0.50, "path": "adaptive"},
        "sandra": {"drive": 0.0, "resistance": 0.60, "threshold": 0.58, "stability": 0.65, "rivalry": 0.40, "obedience": 0.75, "path": "household_order"},
    }

    def household_ai_npc_state(npc_id):
        info = people.get_info(str(npc_id or "").lower())
        if info is None:
            return {}
        return info.var.setdefault("household_ai", dict(HOUSEHOLD_NPC_DEFAULTS.get(str(npc_id or "").lower(), {})))


default household = HouseholdInfo()
