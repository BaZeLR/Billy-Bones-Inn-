# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def event_amanda_legare_create_dance():
        if DanceSponsor == 1:
            get_girl_drunk("amanda")

        Amanda.set_var_int("alberdanceadvance", Amanda.legare_dance_advance_level())

        watch_line = SexEvents.dance_watch_line
        legare_go_phrase = str(watch_line.get(6, "") or "")
        watch_line.clear()
        watch_line[1] = "Аманда весело болтает с импозантным виноторговцем."
        watch_line[2] = "Расторопный виноторговец галантно приглашает Аманду на танец. После секундных раздумий та берет его за руку и вот они уже кружатся в танце."
        watch_line[3] = "По ходу танца мессир Легаре как бы невзначай кладет руки на талию Аманды, что не вызывает с ее стороны никаких возражений."
        watch_line[4] = "Медленно но верно руки похотливого торгаша спускаются на попу Аманды. А чертовка как будто этого не замечает."
        watch_line[5] = "Однако Альберу мало и этого, его руки начинают гладить и мять попу Аманды, пока они продолжают кружится в танце. Девушка же и не думает возражать, наоборот, она улыбается и прижимается к своему партнеру всем телом."

        if Amanda.var_int("LegareGo", 0) == 0:
            watch_line[6] = "И вдруг женатый торговец наклоняется к губам Аманды и страстно ее целует. Аманда же не находит ничего лучшего, кроме как ответить ему со всем пылом юности."
        elif legare_go_phrase != "":
            watch_line[6] = legare_go_phrase

        watch_line[0] = "Аманда продолжает свой танец с мессиром Легаре."
        if Amanda.var_int("alberdanceadvance", 0) == 2:
            watch_line[0] += " Торгаш нежно обнимает ее за талию."
        if Amanda.var_int("alberdanceadvance", 0) == 3:
            watch_line[0] += " Альбер нежно но твердо держит Аманду за попу."
        if Amanda.var_int("alberdanceadvance", 0) >= 4:
            watch_line[0] += " Похотливые ручонки достопочтенного Альбера Легаре нежно сжимают упругую попку Аманды через тонкую ткань ее платья. А она трется своими грудками о его грудь, потихоньку возбуждаясь."
        if Amanda.var_int("alberdanceadvance", 0) == 5:
            watch_line[0] += " При этом он не забывает целовать малышку Аманду а та отвечает ему тем же, с трудом не сбиваясь с ритма танца."

        if Amanda.var_int("alberfriends", 0) < 12 and procedural_randint(1, 2, key="procedural:NPC/Girls/Amanda/EventAmandaLegareCreateDance.rpy:procedural_randint:35:1") == 1:
            Amanda.set_var_int("alberfriends", Amanda.var_int("alberfriends", 0) + 1)

        Amanda.apply_social_chance(0, 0, 0, 21, 2, 1, "legare_create_dance")

label EventAmandaLegareCreateDance:
    $ event_amanda_legare_create_dance()
    return
