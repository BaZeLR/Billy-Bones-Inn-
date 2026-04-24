# BeckyInviteHome.rpy
# Converted from legacy script. Handles Becky inviting the player home after dancing.
# All logic, conditions, and dev notes preserved.

label BeckyInviteHome(girl_name="becky"):
    # girl_name: string from legacy flow (often "Becky" with capital B)
    python:
        _girl_key = str(girl_name or "becky")
        if _girl_key not in Friends and _girl_key.lower() in Friends:
            _girl_key = _girl_key.lower()
        BeckyVar.setdefault("danceinvitehome", 0)
        BeckyVar.setdefault("visitedhome", 0)
        Friends.setdefault(_girl_key, 0)
        sluttiness.setdefault(_girl_key, 0)
        HadSex.setdefault(_girl_key, 0)

    if Friends[_girl_key] >= 10 and sluttiness[_girl_key] > 20 and DanceStep >= 3 and DanceStep < DanceMaxIBD and BeckyVar['danceinvitehome'] == 0 and renpy.random.randint(1,5) == 1:
        if BeckyVar['visitedhome'] > 0 and HadSex[_girl_key] > 0 and sluttiness[_girl_key] > 48:
            "Стефан, милый, чем нам здесь танцевать, пойдем-ка лучше ко мне, я уже вся теку!" # развратная вдовушка
        elif BeckyVar['visitedhome'] > 0 and HadSex[_girl_key] > 0:
            "Стефан, милый, а может пойдем ко мне, ну, помнишь, как в прошлый раз?" # Бекки, глядя прямо в глаза
        else:
            "Стефан, а может ко мне в гости зайдешь, вина немного выпьем?" # неожиданно приглашает вдовушка
        $ BeckyVar['danceinvitehome'] = 1
    return
