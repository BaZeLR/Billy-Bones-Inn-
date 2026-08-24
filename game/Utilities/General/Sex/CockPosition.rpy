init python:
    COCK_POSITION_BY_ID = {
        0: "none",
        1: "pussy",
        2: "mouth",
        3: "tits",
        4: "ass",
    }

    def cock_position_normalize(position_=0):
        try:
            position_id = int(position_ or 0)
            return COCK_POSITION_BY_ID.get(position_id, "none")
        except Exception:
            position_key = str(position_ or "none").strip().lower()
            return position_key if position_key in ("none", "pussy", "mouth", "tits", "ass") else "none"

    def cock_position_target(target_id=""):
        key = str(target_id or "").strip().lower()
        if not key:
            return None
        return getPersonInfo(key)

    def cock_position_apply(girl_name, position_=0, other_dude_name=""):
        target_key = str(girl_name or "").strip().lower()
        if not target_key:
            return "none"
        actor_key = str(other_dude_name or "You").strip() or "You"
        position_key = cock_position_normalize(position_)

        target = cock_position_target(target_key)
        if target is not None and hasattr(target, "set_cock_position"):
            target.set_cock_position(position_key, actor_key)

        if actor_key.lower() in ("you", "mc", "stefan", "стефан"):
            player_obj = player
            player_obj.intimacy.set_cock_position(target_key, position_key)
        else:
            actor = getPersonInfo(actor_key)
            if actor is not None:
                actor.ensure_sex_state().setdefault("cock_positions", {})[target_key] = position_key
        return position_key


label CockPosition(girl_name="", position_=0, other_dude_name=""):
    $ cock_position_apply(girl_name, position_, other_dude_name)
    return


label cock_position(girl_name="", position_=0, other_dude_name=""):
    $ cock_position_apply(girl_name, position_, other_dude_name)
    return
