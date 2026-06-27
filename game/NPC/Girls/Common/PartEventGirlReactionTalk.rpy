# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
default Result = ""

# PartEventGirlReactionTalk location - converted from legacy script
label PartEventGirlReactionTalk(GirlNamePEGRT1, GirlNamePEGRT2, FriendVarToChange, DefiniteAccept, FriendLimit, SlutLimit):
    $ BeleiveFriend = 0
    # Дополнительный шанс поверить, если подруги
    python:
        def _pegrt_int(value, default=0):
            try:
                return int(value)
            except Exception:
                try:
                    return int(float(value))
                except Exception:
                    return default

        def _pegrt_parse_ref(ref_expr):
            ref_expr = str(ref_expr or "").strip()
            if ref_expr == "":
                return "", ""

            if "[" not in ref_expr or not ref_expr.endswith("]"):
                return ref_expr, ""

            dict_name, key_part = ref_expr.split("[", 1)
            dict_name = dict_name.strip()
            dict_key = key_part[:-1].strip()
            if len(dict_key) >= 2 and dict_key[0] in ["'", '"'] and dict_key[-1] == dict_key[0]:
                dict_key = dict_key[1:-1]
            return dict_name, dict_key

        def _pegrt_get_ref_value(ref_expr):
            dict_name, dict_key = _pegrt_parse_ref(ref_expr)
            if dict_name.endswith(".var") and dict_key != "":
                info = getPersonInfo(dict_name[:-4])
                if info is not None and isinstance(getattr(info, "var", None), dict):
                    return _pegrt_int(info.var.get(dict_key, 0), 0)
            return 0

        def _pegrt_set_ref_value(ref_expr, value):
            dict_name, dict_key = _pegrt_parse_ref(ref_expr)
            if dict_name.endswith(".var") and dict_key != "":
                info = getPersonInfo(dict_name[:-4])
                if info is not None and isinstance(getattr(info, "var", None), dict):
                    info.var[dict_key] = value

        friend_var_value = _pegrt_get_ref_value(FriendVarToChange)
        DefiniteAccept = _pegrt_int(DefiniteAccept, 0)
        FriendLimit = _pegrt_int(FriendLimit, 0)
        SlutLimit = _pegrt_int(SlutLimit, 0)

        if friend_var_value > 0:
            if procedural_randint(1, max(2, int(FriendLimit / friend_var_value)), key="procedural:NPC/Girls/Common/PartEventGirlReactionTalk.rpy:procedural_randint:56:1") == 1:
                BeleiveFriend = 1
        
        result_text = ""
        girl_info = getPersonInfo(GirlNamePEGRT1)
        girl_slut = _pegrt_int(getattr(girl_info, "corruption", 0), 0)

        if girl_slut >= DefiniteAccept or procedural_randint(1,5, key="procedural:NPC/Girls/Common/PartEventGirlReactionTalk.rpy:procedural_randint:63:2") <= 3 or BeleiveFriend:
            result_text = f"\n{RealName.get(GirlNamePEGRT1, GirlNamePEGRT1)} внимательно слушает свою собеседницу, впитывая информацию."
            if friend_var_value < FriendLimit and procedural_randint(1,3, key="procedural:NPC/Girls/Common/PartEventGirlReactionTalk.rpy:procedural_randint:65:3") == 1:
                _pegrt_set_ref_value(FriendVarToChange, friend_var_value + 1)
                result_text += f"\nПохоже, {RealName.get(GirlNamePEGRT1, GirlNamePEGRT1)} и {RealName.get(GirlNamePEGRT2, GirlNamePEGRT2)} сдружились еще больше!"
            
            if girl_slut < SlutLimit and procedural_randint(1,2, key="procedural:NPC/Girls/Common/PartEventGirlReactionTalk.rpy:procedural_randint:69:4") == 1:
                if girl_info is not None:
                    girl_info.change_social(corruption_delta=1)
                result_text += f"\nВам показалось, что после этого разговора {RealName.get(GirlNamePEGRT1, GirlNamePEGRT1)} почуствовала себя чуть больше раскрепощенной."
        else:
            result_text = f'\n"Да врешь ты все!" воскликнула {RealName.get(GirlNamePEGRT1, GirlNamePEGRT1)} и пошла по своим делам, даже не удосужившись попрощаться.'
            if friend_var_value > (FriendLimit/4) and procedural_randint(1,5, key="procedural:NPC/Girls/Common/PartEventGirlReactionTalk.rpy:procedural_randint:75:5") == 1:
                _pegrt_set_ref_value(FriendVarToChange, friend_var_value - 1)
                result_text += f"\nПохоже, {RealName.get(GirlNamePEGRT1, GirlNamePEGRT1)} и {RealName.get(GirlNamePEGRT2, GirlNamePEGRT2)} малость поссорились!"
            
            if girl_slut > (SlutLimit/4) and girl_slut > (SlutLimit+15) and procedural_randint(1,5, key="procedural:NPC/Girls/Common/PartEventGirlReactionTalk.rpy:procedural_randint:79:6") == 1:
                if girl_info is not None:
                    girl_info.change_social(corruption_delta=-1)
                result_text += f"\nВам показалось, что после этого разговора {RealName.get(GirlNamePEGRT1, GirlNamePEGRT1)} почуствовала себя более гордой и неприступной."
        
        Result = result_text
    
    return
