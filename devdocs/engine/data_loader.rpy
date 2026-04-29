init -10 python:
    import json
    import renpy as renpy_module
    from pathlib import Path
    from renpy.loader import loadable, transfn

    _cache = {}

    def load_json(relative_path):
        """Load JSON from the game directory with simple caching."""
        if relative_path in _cache:
            return _cache[relative_path]
        if not loadable(relative_path):
            raise IOError("File not found in archive: %s" % relative_path)
        full_path = transfn(relative_path)
        with open(full_path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        _cache[relative_path] = data
        return data

    def load_locations_data():
        return load_json("game/data/locations.json")

    def load_people_dataset():
        base_dir = "json/npcs"
        full_dir = None
        try:
            full_dir = Path(transfn(base_dir))
        except Exception:
            full_dir = None
        people = []
        if full_dir and full_dir.exists():
            for npc_file in sorted(full_dir.glob("*.json")):
                with npc_file.open("r", encoding="utf-8") as fh:
                    people.append(json.load(fh))
            return people

        # Fallback: try game dir directly.
        try:
            game_dir = Path(renpy_module.config.gamedir)
            alt_dir = game_dir / base_dir
            if alt_dir.exists():
                for npc_file in sorted(alt_dir.glob("*.json")):
                    with npc_file.open("r", encoding="utf-8") as fh:
                        people.append(json.load(fh))
                return people
        except Exception:
            pass

        # Final fallback: scan packed files (web/archives).
        try:
            prefix = base_dir + "/"
            for filename in renpy_module.list_files():
                if filename.startswith(prefix) and filename.endswith(".json"):
                    people.append(load_json(filename))
        except Exception:
            pass
        return people

    def load_items_dataset():
        return load_json("game/data/items.json")

    def load_tavern_events_config():
        try:
            return load_json("game/json/tavern_events.json")
        except IOError:
            return {"defaults": {}, "categories": {}}

    def clear_data_cache():
        _cache.clear()
