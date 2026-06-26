# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================

init 6 python:
    def _amanda_dynamic_roll(self, low_value=1, high_value=1, key=""):
        return procedural_randint(low_value, high_value, "amanda_dynamic_%s_%s_%s_%s" % (
            str(key or ""),
            people_to_int(dayspassed, 0),
            people_to_int(time, 0),
            self.var_int("dynamic_roll_salt", 0),
        ))

    def _amanda_happy_confirm_text(self):
        roll_one = self.dynamic_roll(1, 4, "happy_confirm_1_%s" % self.var_int("warnnotwork", 0))
        if roll_one == 1:
            p1 = '"Вот Стефанчик, и ты можешь быть разумным. Если захочешь," '
        elif roll_one == 2:
            p1 = '"Ну вот теперь ты говоришь дело," '
        elif roll_one == 3:
            p1 = '"Это ты мудро сказал, не то что прошлый раз," '
        else:
            p1 = '"Вот теперь сразу видно, то все обдумал и говоришь серьезно, а не истеришь как тогда," '

        roll_two = self.dynamic_roll(1, 3, "happy_confirm_2_%s" % self.var_int("warnnotwork", 0))
        if roll_two == 1:
            p2 = "радостно ответила вам Аманда. "
        elif roll_two == 2:
            p2 = "обрадованно воскликнула Аманда. "
        else:
            p2 = "сказала Аманда, довольная своей маленькой победой. "
        return p1 + p2

    def _amanda_sex_offer_reaction(self):
        reaction = 0
        rel = people_to_int(self.rel, 0)
        corr = people_to_int(self.corruption, 0)

        if self.var_int("prohibitliza", 0) or (self.var_int("alberprohibit", 0) and self.var_int("alberfriends", 0) >= 5) or self.var_int("gloryscold", 0):
            if self.var_int("suckyou", 0) or self.var_int("fuckyou", 0):
                if (rel >= 12 and corr >= 40) or corr >= 50:
                    reaction = 4
                    if corr >= 55 and self.dynamic_roll(1, 3, "sex_offer_warned_you") == 1:
                        reaction = 3
                elif corr <= 25 and rel <= 10:
                    reaction = 2
                elif corr <= 30 and rel <= 5:
                    reaction = 2
                else:
                    reaction = 3
            else:
                if (rel >= 14 and corr >= 45) or corr >= 55:
                    reaction = 4
                    if corr >= 55 and self.dynamic_roll(1, 3, "sex_offer_warned_no_you") == 1:
                        reaction = 3
                elif corr <= 30 and rel <= 12:
                    reaction = 2
                elif corr <= 35 and rel <= 8:
                    reaction = 2
                else:
                    reaction = 3
        else:
            if self.var_int("suckyou", 0) or self.var_int("fuckyou", 0):
                if rel >= 2 and corr >= 45:
                    reaction = 4
                elif rel >= 5 and corr >= 35:
                    reaction = 4
                elif rel >= 10 and corr >= 25:
                    reaction = 4
                elif rel >= 15 and corr >= 21:
                    reaction = 4
                elif rel >= 2 and corr >= 35:
                    reaction = 1
                elif rel >= 5 and corr >= 25:
                    reaction = 1
                elif rel >= 10 and corr >= 21:
                    reaction = 1
            else:
                if rel >= 5 and corr >= 45:
                    reaction = 4
                elif rel >= 10 and corr >= 35:
                    reaction = 4
                elif rel >= 15 and corr >= 25:
                    reaction = 4
                elif rel >= 5 and corr >= 35:
                    reaction = 1
                elif rel >= 10 and corr >= 25:
                    reaction = 1
        return reaction

    def _amanda_legare_sex_type(self):
        if self.var_int("sucklegare", 0) == 0:
            sex_type = 0
        elif self.var_int("fucklegare", 0) == 0:
            if self.stats.get("virginity", True):
                if self.var_int("alberfriends", 0) >= 15 and self.corruption >= 35 and people_to_int(self.stats.get("sexacts", 0), 0) >= 5:
                    sex_type = 2
                else:
                    sex_type = 1
            else:
                if self.var_int("alberfriends", 0) >= 12 and self.corruption >= 32 and people_to_int(self.stats.get("sexacts", 0), 0) >= 4:
                    sex_type = 3
                else:
                    sex_type = 1
        elif (self.var_int("alberfriends", 0) >= 10 and self.corruption >= 30) or (self.var_int("alberfriends", 0) >= 5 and self.corruption >= 40):
            sex_type = 4
        else:
            sex_type = 1

        if people_to_int(self.stats.get("pregnancy", 0), 0) >= 120 and sex_type == 3:
            sex_type = 4
        return sex_type

    def _amanda_nesluh_value(self):
        bonus = 0
        if self.var_int("glorydeflower", 0) > 0 or self.var_int("fuckyou", 0) > 0:
            bonus += 6
        if self.var_int("gloryscold", 0) > 0:
            bonus -= 3
        if self.var_int("glorysuck", 0) > 0 or self.var_int("suckyou", 0) > 0:
            bonus += 3
        if self.var_int("glorywalkout", 0) > 0:
            bonus += 2
        if self.var_int("alberfriends", 0) >= 7:
            bonus += 1
        if self.var_int("alberfriends", 0) >= 9:
            bonus += 1
        if self.var_int("alberfriends", 0) >= 12:
            bonus += 2
        if self.corruption >= 23:
            bonus += 1
        if self.corruption >= 30:
            bonus += 2
        if self.corruption >= 40:
            bonus += 4
        if self.corruption >= 50:
            bonus += 3
        if self.var_int("sucklegare", 0) > 0:
            bonus += 2
        if self.var_int("fucklegare", 0) > 0:
            bonus += 3
        if self.var_int("deflowerlegare", 0) > 0:
            bonus += 3

        bonus = min(14, max(1, bonus))
        nesluh = 1 if self.dynamic_roll(1, 15, "nesluh_%s_%s" % (self.var_int("alberfriends", 0), self.corruption)) <= bonus else 0
        if (self.var_int("glorydeflower", 0) or self.var_int("fuckyou", 0)) and nesluh == 1 and self.dynamic_roll(1, 4, "nesluh_deflower") <= 3:
            nesluh = 2
        elif (self.var_int("glorysuck", 0) or self.var_int("suckyou", 0)) and nesluh == 1 and self.dynamic_roll(1, 4, "nesluh_suck") <= 1:
            nesluh = 2
        return nesluh

    def _amanda_lover_sex_calc(self, guy_name="", forced_type=0):
        guy = str(guy_name or "")
        if not guy:
            guy = RandomNameCode("male")

        sex_type = 0
        if self.corruption >= 57:
            sex_type = 2
        elif people_to_int(self.stats.get("pregnancy", 0), 0) > 120:
            if self.corruption >= 42:
                sex_type = 2
            elif self.corruption >= 40:
                sex_type = 1
        elif self.corruption >= 45:
            if self.dynamic_roll(1, 3, "lover_calc_45") == 1:
                sex_type = 1
            elif self.dynamic_roll(1, 9, "lover_calc_45_alt") <= 4:
                sex_type = 2
        elif self.corruption >= 40:
            sex_type = 1

        if people_to_int(forced_type, 0) > 0:
            sex_type = people_to_int(forced_type, 0)
        if sex_type == 2 and self.dynamic_roll(1, 2, "lover_calc_variant") == 1:
            sex_type = 3

        if sex_type == 3:
            self.pregnancy_check("outside", 1, guy, 0, "Соседский парень")
            self.change_social(corruption_delta=1)
        elif sex_type == 2:
            self.pregnancy_check("inside", 1, guy, 0, "Соседский парень")
            self.change_social(corruption_delta=1)
        elif sex_type == 1:
            self.pregnancy_check("mouth", 1, guy, 0, "Соседский парень")
            self.change_social(corruption_delta=1)
        return sex_type

    def _amanda_yell_not_work(self):
        renpy.say(None, "Не стерпев что Аманда отлынивает от работы, вы подскочили к ней, взяли за плечо и начали орать:")
        if self.var_int("warnnotwork", 0):
            renpy.say(None, "\"Опять ты шляешься по улице вместо того, чтобы работать! А я ведь тебя предупреждал!\"")
            renpy.say(None, "\"Но перерыв...\" попыталась оправдаться Аманда.")
        else:
            renpy.say(None, "\"Ты что это по улице шляешься? У нас, между прочим, посетители есть.\"")
            renpy.say(None, "\"А что такого? У меня перерыв.\" ответила вам она.")
        renpy.say(None, "\"Не выдумывай! Нет у тебя никакого перерыва. А даже если бы и был, то считай что он уже закончился. Марш на работу!\"")

        self.set_var_int("warnnotwork", 1)
        if self.dynamic_roll(1, 3, "yell_not_work") == 1:
            renpy.say(None, "\"Нет так нет,\" недобро ответила вам она. \"Работать я работаю, как умею.\"")
            renpy.say(None, "И, напевая себе под нос: \"Так чего же нам стараться, поработаем с прохладцей,\" она пошла обратно.")
            self.skills["cooking"] = max(10, people_to_int(self.skills.get("cooking", 0), 0) - 3)
            self.skills["cleaning"] = max(10, people_to_int(self.skills.get("cleaning", 0), 0) - 3)
            self.skills["waitress"] = max(10, people_to_int(self.skills.get("waitress", 0), 0) - 3)
        else:
            renpy.say(None, "Расстроившись, но не найдя что вам возразить, Аманда пошлепала обратно в трактир.")

        self.change_social(friend_delta=(1 if self.rel >= 6 else -2))
        return 0

    AmandaInfo.dynamic_roll = _amanda_dynamic_roll
    AmandaInfo.happy_confirm_text = _amanda_happy_confirm_text
    AmandaInfo.sex_offer_reaction = _amanda_sex_offer_reaction
    AmandaInfo.legare_sex_type = _amanda_legare_sex_type
    AmandaInfo.nesluh_value = _amanda_nesluh_value
    AmandaInfo.lover_sex_calc = _amanda_lover_sex_calc
    AmandaInfo.yell_not_work = _amanda_yell_not_work

label AmandaDynamicCommonBlocks:
    return
