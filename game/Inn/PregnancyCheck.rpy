# PregnancyCheck.rpy
# Converted from PregnancyCheck.txt
# Handles pregnancy logic for a given girl and event

# Default variable statements - only declare if not already declared elsewhere
default sexacts = {}
default ConceptionChance = {}
default cametoday_npc = {}
default sluttiness = {}
default cuminside = {}
# Remove duplicate pregnancy declaration - it's already declared in InitAmanda.rpy
# default pregnancy = {}
# default pregfather = {}

init python:
    import renpy

    def PregnancyCheck(girl_name, cum_place, repeat_count, dad_name='', is_dude_random=0, dad_name_type=''):
        """
        girl_name: str - name of the girl
        cum_place: str - where the cum landed (inside, mouth, tits, mouthface, face, outside)
        repeat_count: int - how many times to repeat the check
        dad_name: str - name of the father (optional)
        is_dude_random: int - if 1, randomize dad
        dad_name_type: str - type of dad (optional)
        """
        def lcase(s):
            return s.lower() if isinstance(s, str) else s
        def Min(a, b):
            return min(a, b)
        def Max(a, b):
            return max(a, b)
        
        # Argument normalization
        girl = girl_name
        dad = dad_name
        dad_type = dad_name_type
        is_random = is_dude_random
        cum_place = (cum_place or '').lower()
        
        if lcase(dad) == 'you':
            dad = 'Вы'
        if dad == 'вы':
            dad = 'Вы'
        if dad_name == '':
            is_random = 1
        if dad_type == '' and not is_random:
            dad_type = 'NPC'
        dad_type_reset = 1 if is_random and dad_type == '' else 0
        dad_name_reset = 1 if dad == '' else 0
        cum_place_reset = 1 if cum_place not in ['inside', 'mouth', 'tits', 'mouthface', 'face', 'outside'] else 0
        fun_awarded = 0
        
        for _unused_pregnancy_check in range(int(repeat_count)):
            # Randomize dad type if needed
            if dad_type_reset:
                randnum = renpy.random.randint(1, 7)
                dad_type = [
                    'Неизвестный моряк',
                    'Неизвестный грузчик',
                    'Неизвестный негр',
                    'Неизвестный стражник',
                    'Неизвестный горожанин',
                    'Неизвестный крестьянин',
                    'Неизвестный торговец',
                ][randnum-1]
            # Randomize dad name if needed
            if dad_name_reset:
                # Placeholder: replace with actual random name code
                dad = 'Случайный мужчина'
                if dad_type == 'Неизвестный негр':
                    dad = 'Случайный негр'
            # Randomize cum place if needed
            if cum_place_reset:
                randvar = renpy.random.randint(1, 6)
                if randvar <= 3:
                    cum_place = 'inside'
                elif randvar == 4:
                    cum_place = 'mouth'
                elif randvar == 5:
                    cum_place = 'tits'
                else:
                    cum_place = 'mouthface'
            # Stat changes
            sexacts[girl] = sexacts.get(girl, 0) + 1
            cur_conc = ConceptionChance.get(girl, 0)
            if dad == 'Вы':
                cur_conc *= 3
                HadSex[girl] = HadSex.get(girl, 0) + 1
                HadSex['You'] = HadSex.get('You', 0) + 1
                if fun_awarded == 0:
                    renpy.store.fun = max(0, min(100, int(getattr(renpy.store, "fun", 0) or 0) + 30))
                    fun_awarded = 1
                renpy.store.cametoday = int(getattr(renpy.store, 'cametoday', 0) or 0) + 1
                if cum_place == 'inside':
                    CumInsideYou[girl] = 1
                elif cum_place == 'tits':
                    CumTitsYou[girl] = 1
                elif cum_place in ['face', 'mouthface']:
                    CumFaceYou[girl] = 1
            else:
                if cum_place == 'inside':
                    CumInsideOthers[girl] = 1
                elif cum_place == 'tits':
                    CumTitsOthers[girl] = 1
                elif cum_place in ['face', 'mouthface']:
                    CumFaceOthers[girl] = 1
                if cum_place == '':
                    CumFaceOthers[girl] = 0
                    CumTitsOthers[girl] = 0
                if not isinstance(getattr(renpy.store, "cametoday_npc", None), dict):
                    renpy.store.cametoday_npc = {}
                renpy.store.cametoday_npc[dad] = int(renpy.store.cametoday_npc.get(dad, 0) or 0) + 1
            # Sluttiness increase
            Zalet = 0
            if renpy.random.randint(1, Max(sluttiness.get(girl, 1), 1)*3) <= 1 * (2 if cum_place == 'inside' else 1) and sluttiness.get(girl, 0) <= 70:
                sluttiness[girl] = sluttiness.get(girl, 0) + 1
            if is_random:
                cur_conc = cur_conc / 10
            if cum_place == 'inside':
                cuminside[girl] = cuminside.get(girl, 0) + 1
                if pregnancy.get(girl, 0) == 0:
                    cur_conc = Min(cur_conc, 800)
                    if renpy.random.randint(1, 1000) <= cur_conc:
                        pregnancy[girl] = 1
                        pregfather[girl] = dad
                        Zalet = 1
            # Dad name record normalization
            dad_record = dad
            if lcase(dad_record) == 'eddie' and dad_type == 'NPC':
                dad_record = 'Эдди'
            if lcase(dad_record) == 'legare' and dad_type == 'NPC':
                dad_record = 'Мессир Легаре'
            if lcase(dad_record) == 'месье легаре' and dad_type == 'NPC':
                dad_record = 'Мессир Легаре'

            repo = getattr(renpy.store, "sex_history_by_girl", {}) or {}
            next_ids = getattr(renpy.store, "sex_history_next_id", {}) or {}
            girl_rows = list(repo.get(girl, []) or [])
            row_id = int(next_ids.get(girl, 1) or 1)
            girl_rows.append({
                "RowId": row_id,
                "Day": int(dayspassed + 1),
                "GirlName": str(girl),
                "DudeName": str(dad_record),
                "DudeNameType": str(dad_type or ""),
                "IsDudeRandom": int(is_random or 0),
                "CumTarget": str(cum_place or ""),
                "Zalet": int(Zalet or 0),
            })
            repo[girl] = girl_rows
            next_ids[girl] = row_id + 1
            renpy.store.sex_history_by_girl = repo
            renpy.store.sex_history_next_id = next_ids

# Ren'Py label for script compatibility
label PregnancyCheck(girl_name, cum_place, repeat_count, dad_name='', is_dude_random=0, dad_name_type=''):
    python:
        PregnancyCheck(girl_name, cum_place, repeat_count, dad_name, is_dude_random, dad_name_type)
    return
