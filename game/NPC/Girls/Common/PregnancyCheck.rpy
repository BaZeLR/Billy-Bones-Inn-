# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
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

    def pregnancy_conception_bonus(girl_name=""):
        girl = str(girl_name or "").strip().lower()
        if girl not in ("sandra", "melissa", "amanda"):
            return 0
        try:
            if callable(tavern_kitchen_fertility_bonus_active) and tavern_kitchen_fertility_bonus_active():
                base_chance = int(ConceptionChance.get(girl, 0) or 0)
                return max(4, int(base_chance * 0.5))
        except Exception:
            return 0
        return 0

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
        girl = str(girl_name or "").strip().lower()
        girl_info = getPersonInfo(girl)
        if girl_info is None:
            return 0
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
            girl_info.add_sex_stat("sexacts", 1)
            cur_conc = girl_info.sex_stat("ConceptionChance", 0)
            if dad == 'Вы':
                cur_conc *= 3
                girl_info.mark_fucked(1)
                if fun_awarded == 0:
                    player_state(False).condition.change("fun", 30)
                    player_state(False).condition.apply_to_store()
                    fun_awarded = 1
                player_state(False).intimacy.record_cum(dayspassed)
                player_state(False).intimacy.apply_to_store()
                if cum_place == 'inside':
                    girl_info.set_cum_state("cum_inside_you", 1)
                elif cum_place == 'tits':
                    girl_info.set_cum_state("cum_tits_you", 1)
                elif cum_place in ['face', 'mouthface']:
                    girl_info.set_cum_state("cum_face_you", 1)
                elif cum_place == 'mouth':
                    girl_info.set_cum_state("cum_mouth_you", 1)
            else:
                if cum_place == 'inside':
                    girl_info.set_cum_state("cum_inside_others", 1)
                elif cum_place == 'tits':
                    girl_info.set_cum_state("cum_tits_others", 1)
                elif cum_place in ['face', 'mouthface']:
                    girl_info.set_cum_state("cum_face_others", 1)
                elif cum_place == 'mouth':
                    girl_info.set_cum_state("cum_mouth_others", 1)
                if cum_place == '':
                    girl_info.clear_cum("cum_face_others", "cum_tits_others")
                dad_info = getPersonInfo(dad)
                if dad_info is not None:
                    dad_state = dad_info.ensure_sex_state()
                    dad_state["came_today"] = int(dad_state.get("came_today", 0) or 0) + 1
            # Sluttiness increase
            Zalet = 0
            if renpy.random.randint(1, Max(getattr(girl_info, "corruption", 1), 1)*3) <= 1 * (2 if cum_place == 'inside' else 1) and getattr(girl_info, "corruption", 0) <= 70:
                girl_info.change_social(corruption_delta=1)
            if is_random:
                cur_conc = cur_conc / 10
            if cum_place == 'inside':
                girl_info.add_sex_stat("cuminside", 1)
                if girl_info.pregnancy_days() == 0:
                    cur_conc += int(pregnancy_conception_bonus(girl) or 0)
                    cur_conc = Min(cur_conc, 800)
                    if renpy.random.randint(1, 1000) <= cur_conc:
                        girl_info.set_sex_stat("pregnancy", 1)
                        girl_info.set_sex_stat("pregfather", dad)
                        Zalet = 1
            # Dad name record normalization
            dad_record = dad
            if lcase(dad_record) == 'eddie' and dad_type == 'NPC':
                dad_record = 'Эдди'
            if lcase(dad_record) == 'legare' and dad_type == 'NPC':
                dad_record = 'Мессир Легаре'
            if lcase(dad_record) == 'месье легаре' and dad_type == 'NPC':
                dad_record = 'Мессир Легаре'

            if not isinstance(getattr(girl_info, "detailed_sex_history", None), list):
                girl_info.detailed_sex_history = []
            row_id = len(girl_info.detailed_sex_history) + 1
            girl_info.detailed_sex_history.append({
                "RowId": row_id,
                "Day": int(dayspassed + 1),
                "GirlName": str(girl),
                "DudeName": str(dad_record),
                "DudeNameType": str(dad_type or ""),
                "IsDudeRandom": int(is_random or 0),
                "CumTarget": str(cum_place or ""),
                "Zalet": int(Zalet or 0),
            })
        return 0

# Ren'Py label for script compatibility
label PregnancyCheck(girl_name, cum_place, repeat_count, dad_name='', is_dude_random=0, dad_name_type=''):
    python:
        PregnancyCheck(girl_name, cum_place, repeat_count, dad_name, is_dude_random, dad_name_type)
    return
