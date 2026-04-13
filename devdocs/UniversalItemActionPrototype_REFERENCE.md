# Universal Item Action Prototype Reference

This file is kept for reference only.

It is **not** part of the live Ren'Py project load path.
The loadable prototype files were removed from:

- `game/Inn/UniversalItemActionPrototype.rpy`
- `game/Inn/UniversalItemActionPrototype.rpyc`

Below is the last prototype draft that was removed from the working project.

```renpy
init python:
    class ProtoGameItem(object):
        def __init__(
            self,
            item_id="",
            name="",
            desc="",
            picture=None,
            portable=False,
            stackable=False,
            actions=None,
            tags=None,
            data=None,
        ):
            self.item_id = str(item_id or "").strip()
            self.name = str(name or "").strip()
            self.desc = str(desc or "")
            self.picture = picture
            self.portable = bool(portable)
            self.stackable = bool(stackable)
            self.actions = list(actions or [])
            self.tags = list(tags or [])
            self.data = dict(data or {})

        def as_dict(self):
            return {
                "item_id": self.item_id,
                "name": self.name,
                "desc": self.desc,
                "picture": self.picture,
                "portable": self.portable,
                "stackable": self.stackable,
                "actions": list(self.actions),
                "tags": list(self.tags),
                "data": dict(self.data),
            }


default item_catalog = {
    "axe": ProtoGameItem(
        item_id="axe",
        name="Топор",
        desc="Старый, но еще крепкий топор. Таким удобно колоть дрова.",
        picture=None,
        portable=True,
        stackable=False,
        actions=["take", "examine"],
        tags=["tool"],
        data={},
    ).as_dict(),
    "beer": ProtoGameItem(
        item_id="beer",
        name="Пиво",
        desc="Простое пиво. Немного веселит и слегка отбивает голод.",
        picture=None,
        portable=True,
        stackable=True,
        actions=["drink", "examine"],
        tags=["drink"],
        data={
            "fun_delta": 1,
            "hunger_delta": -5,
        },
    ).as_dict(),
    "wood_log": ProtoGameItem(
        item_id="wood_log",
        name="Бревно",
        desc="Тяжелое бревно. Если у вас есть топор, его можно расколоть на дрова.",
        picture=None,
        portable=True,
        stackable=False,
        actions=["take", "examine", "chop"],
        tags=["wood"],
        data={
            "chop_yield_item": "chopped_wood",
            "chop_yield_qty": 10,
        },
    ).as_dict(),
    "chopped_wood": ProtoGameItem(
        item_id="chopped_wood",
        name="Колотые дрова",
        desc="Готовые дрова для растопки.",
        picture=None,
        portable=True,
        stackable=True,
        actions=["take", "examine"],
        tags=["wood", "fuel"],
        data={},
    ).as_dict(),
}


default inventory = {
    "beer": 1,
}


default locations = {
    "woodshed": {
        "name": "Сарай",
        "label": "loc_woodshed",
        "picture": None,
        "objects": ["axe", "wood_log"],
        "loot": {
            "chopped_wood": 0,
        },
        "search_text": "Вы внимательно осматриваете сарай. На стене висит топор, а рядом лежит бревно, которое можно расколоть. В углу можно сложить готовые дрова.",
    },
}


default current_location = "woodshed"
default action_result_text = ""
default action_result_picture = None
default fun = 0
default hunger = 50


init python:
    def add_to_inventory(item_id, qty=1):
        item_key = str(item_id or "").strip()
        amount = max(0, int(qty or 0))
        if item_key == "" or amount <= 0:
            return 0
        inventory[item_key] = int(inventory.get(item_key, 0) or 0) + amount
        return amount


    def remove_from_inventory(item_id, qty=1):
        item_key = str(item_id or "").strip()
        amount = max(0, int(qty or 0))
        if item_key == "" or amount <= 0:
            return 0
        current_qty = int(inventory.get(item_key, 0) or 0)
        removed = min(current_qty, amount)
        left_qty = current_qty - removed
        if left_qty > 0:
            inventory[item_key] = left_qty
        elif item_key in inventory:
            del inventory[item_key]
        return removed


    def has_item(item_id, qty=1):
        item_key = str(item_id or "").strip()
        amount = max(1, int(qty or 1))
        return int(inventory.get(item_key, 0) or 0) >= amount


    def _get_item(item_id):
        return dict(item_catalog.get(str(item_id or "").strip(), {}) or {})


    def _get_location(loc_id=None):
        loc_key = str(loc_id or current_location or "").strip()
        return locations.get(loc_key, None)


    def _location_has_object(loc_id, item_id):
        loc = _get_location(loc_id)
        if loc is None:
            return False
        item_key = str(item_id or "").strip()
        return item_key in list(loc.get("objects", []) or [])


    def _location_remove_object(loc_id, item_id):
        loc = _get_location(loc_id)
        if loc is None:
            return False
        item_key = str(item_id or "").strip()
        objects = list(loc.get("objects", []) or [])
        removed = False
        updated = []
        for row in objects:
            row_key = str(row or "").strip()
            if not removed and row_key == item_key:
                removed = True
                continue
            updated.append(row_key)
        loc["objects"] = updated
        return removed


    def _location_loot_qty(loc_id, item_id):
        loc = _get_location(loc_id)
        if loc is None:
            return 0
        return int(dict(loc.get("loot", {}) or {}).get(str(item_id or "").strip(), 0) or 0)


    def _location_add_loot(loc_id, item_id, qty=1):
        loc = _get_location(loc_id)
        if loc is None:
            return 0
        item_key = str(item_id or "").strip()
        amount = max(0, int(qty or 0))
        if item_key == "" or amount <= 0:
            return 0
        loot = dict(loc.get("loot", {}) or {})
        loot[item_key] = int(loot.get(item_key, 0) or 0) + amount
        loc["loot"] = loot
        return amount


    def _location_remove_loot(loc_id, item_id, qty=1):
        loc = _get_location(loc_id)
        if loc is None:
            return 0
        item_key = str(item_id or "").strip()
        amount = max(0, int(qty or 0))
        if item_key == "" or amount <= 0:
            return 0
        loot = dict(loc.get("loot", {}) or {})
        current_qty = int(loot.get(item_key, 0) or 0)
        removed = min(current_qty, amount)
        loot[item_key] = current_qty - removed
        loc["loot"] = loot
        return removed


    def _item_name(item_id):
        item = _get_item(item_id)
        return str(item.get("name", item_id) or item_id)


    def _item_desc(item_id):
        item = _get_item(item_id)
        return str(item.get("desc", "Описание отсутствует.") or "Описание отсутствует.")


    def take_action(item_id, qty=1):
        item_key = str(item_id or "").strip()
        amount = max(1, int(qty or 1))
        item = _get_item(item_key)
        if item_key == "" or not item:
            return {"text": "Непонятно, что именно вы пытаетесь взять.", "picture": None}

        if not bool(item.get("portable", False)):
            return {"text": "Этот предмет нельзя унести с собой.", "picture": item.get("picture", None)}

        if _location_has_object(current_location, item_key):
            _location_remove_object(current_location, item_key)
            add_to_inventory(item_key, 1)
            return {"text": "Вы берете {}.".format(_item_name(item_key)), "picture": item.get("picture", None)}

        available_loot = _location_loot_qty(current_location, item_key)
        if available_loot <= 0:
            return {"text": "Здесь этого нет.", "picture": item.get("picture", None)}

        taken = _location_remove_loot(current_location, item_key, amount)
        if taken <= 0:
            return {"text": "Взять ничего не удалось.", "picture": item.get("picture", None)}

        add_to_inventory(item_key, taken)
        return {
            "text": "Вы берете {} x{}.".format(_item_name(item_key), taken),
            "picture": item.get("picture", None),
        }


    def drink_action(item_id):
        global fun, hunger

        item_key = str(item_id or "").strip()
        item = _get_item(item_key)
        if item_key == "" or not item:
            return {"text": "Непонятно, что именно вы пытаетесь выпить.", "picture": None}

        if "drink" not in list(item.get("actions", []) or []):
            return {"text": "Это нельзя выпить.", "picture": item.get("picture", None)}

        if not has_item(item_key, 1):
            return {"text": "У вас нет этого предмета.", "picture": item.get("picture", None)}

        remove_from_inventory(item_key, 1)

        data = dict(item.get("data", {}) or {})
        fun += int(data.get("fun_delta", 1) or 1)
        hunger = max(0, int(hunger or 0) + int(data.get("hunger_delta", -5) or -5))

        return {
            "text": "Вы выпиваете {}.".format(_item_name(item_key)),
            "picture": item.get("picture", None),
        }


    def search_action(loc_id):
        loc_key = str(loc_id or "").strip()
        loc = _get_location(loc_key)
        if loc is None:
            return {"text": "Искать здесь нечего.", "picture": None}

        return {
            "text": str(loc.get("search_text", "Вы ничего не находите.") or "Вы ничего не находите."),
            "picture": loc.get("picture", None),
        }


    def examine_action(item_id):
        item_key = str(item_id or "").strip()
        item = _get_item(item_key)
        if item_key == "" or not item:
            return {"text": "Осматривать здесь нечего.", "picture": None}

        return {
            "text": _item_desc(item_key),
            "picture": item.get("picture", None),
        }


    def chop_action(item_id):
        item_key = str(item_id or "").strip()
        item = _get_item(item_key)
        if item_key == "" or not item:
            return {"text": "Непонятно, что именно вы собираетесь рубить.", "picture": None}

        if "chop" not in list(item.get("actions", []) or []):
            return {"text": "Сейчас это нельзя рубить.", "picture": item.get("picture", None)}

        if not has_item("axe", 1):
            return {"text": "Без топора колоть дрова не получится.", "picture": _get_item("axe").get("picture", None)}

        if not _location_has_object(current_location, item_key):
            return {"text": "В комнате больше нет подходящего бревна.", "picture": item.get("picture", None)}

        _location_remove_object(current_location, item_key)

        data = dict(item.get("data", {}) or {})
        yield_item = str(data.get("chop_yield_item", "chopped_wood") or "chopped_wood")
        yield_qty = max(1, int(data.get("chop_yield_qty", 10) or 10))
        _location_add_loot(current_location, yield_item, yield_qty)

        return {
            "text": "Вы раскалываете {} и получаете {} x{} в комнатном луте.".format(_item_name(item_key), _item_name(yield_item), yield_qty),
            "picture": _get_item(yield_item).get("picture", None),
        }


label take(item_id, qty=1):
    $ _action_result = take_action(item_id, qty)
    $ action_result_text = str(_action_result.get("text", "") or "")
    $ action_result_picture = _action_result.get("picture", None)
    jump show_action_result


label drink(item_id):
    $ _action_result = drink_action(item_id)
    $ action_result_text = str(_action_result.get("text", "") or "")
    $ action_result_picture = _action_result.get("picture", None)
    jump show_action_result


label search(loc_id):
    $ _action_result = search_action(loc_id)
    $ action_result_text = str(_action_result.get("text", "") or "")
    $ action_result_picture = _action_result.get("picture", None)
    jump show_action_result


label examine(item_id):
    $ _action_result = examine_action(item_id)
    $ action_result_text = str(_action_result.get("text", "") or "")
    $ action_result_picture = _action_result.get("picture", None)
    jump show_action_result


label chop(item_id):
    $ _action_result = chop_action(item_id)
    $ action_result_text = str(_action_result.get("text", "") or "")
    $ action_result_picture = _action_result.get("picture", None)
    jump show_action_result


label show_action_result:
    if action_result_picture:
        scene expression action_result_picture
    else:
        scene black

    "[action_result_text]"

    jump expression locations[current_location]["label"]


label loc_woodshed:
    $ current_location = "woodshed"
    $ _room = locations[current_location]

    if _room.get("picture", None):
        scene expression _room["picture"]
    else:
        scene black

    "[_room['name']]"
    "Здесь можно осмотреть сарай, взять инструменты и заготовки или расколоть бревно на дрова."

    if len(dict(inventory or {})) > 0:
        $ _inventory_rows = ["{} x{}".format(_item_name(_item_id), int(_qty or 0)) for _item_id, _qty in sorted(dict(inventory or {}).items()) if int(_qty or 0) > 0]
        if len(_inventory_rows) > 0:
            "У вас с собой: [', '.join(_inventory_rows)]."

    menu:
        "Осмотреть сарай":
            call search("woodshed")

        "Искать в сарае":
            call search("woodshed")

        "Взять топор" if _location_has_object(current_location, "axe"):
            call take("axe")

        "Осмотреть бревно" if _location_has_object(current_location, "wood_log"):
            call examine("wood_log")

        "Колоть бревно" if _location_has_object(current_location, "wood_log"):
            call chop("wood_log")

        "Взять 1 дрова" if _location_loot_qty(current_location, "chopped_wood") >= 1:
            call take("chopped_wood", 1)

        "Взять 5 дров" if _location_loot_qty(current_location, "chopped_wood") >= 5:
            call take("chopped_wood", 5)

        "Выпить пиво" if has_item("beer", 1):
            call drink("beer")

        "Уйти":
            return
```
