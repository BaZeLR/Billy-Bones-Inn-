# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def event_amanda_legare_create_dance():
        if DanceSponsor == 1:
            get_girl_drunk("amanda")

        alber_friends = int(AmandaVar.get("alberfriends", 0) or 0)
        amanda_slut = int(sluttiness.get("amanda", 0) or 0)

        if alber_friends >= 10 and amanda_slut >= 18:
            AmandaVar["alberdanceadvance"] = 5
        elif alber_friends >= 9 and amanda_slut >= 15:
            AmandaVar["alberdanceadvance"] = 4
        elif alber_friends >= 7 and amanda_slut >= 10:
            AmandaVar["alberdanceadvance"] = 3
        elif alber_friends >= 6 and amanda_slut >= 6:
            AmandaVar["alberdanceadvance"] = 2
        elif alber_friends >= 5 and amanda_slut >= 3:
            AmandaVar["alberdanceadvance"] = 1
        else:
            AmandaVar["alberdanceadvance"] = 0

        legare_go_phrase = str(DanceWatchLine.get(6, "") or "")
        DanceWatchLine.clear()
        DanceWatchLine[1] = "Аманда весело болтает с импозантным виноторговцем."
        DanceWatchLine[2] = "Расторопный виноторговец галантно приглашает Аманду на танец. После секундных раздумий та берет его за руку и вот они уже кружатся в танце."
        DanceWatchLine[3] = "По ходу танца мессир Легаре как бы невзначай кладет руки на талию Аманды, что не вызывает с ее стороны никаких возражений."
        DanceWatchLine[4] = "Медленно но верно руки похотливого торгаша спускаются на попу Аманды. А чертовка как будто этого не замечает."
        DanceWatchLine[5] = "Однако Альберу мало и этого, его руки начинают гладить и мять попу Аманды, пока они продолжают кружится в танце. Девушка же и не думает возражать, наоборот, она улыбается и прижимается к своему партнеру всем телом."

        if int(AmandaVar.get("LegareGo", 0) or 0) == 0:
            DanceWatchLine[6] = "И вдруг женатый торговец наклоняется к губам Аманды и страстно ее целует. Аманда же не находит ничего лучшего, кроме как ответить ему со всем пылом юности."
        elif legare_go_phrase != "":
            DanceWatchLine[6] = legare_go_phrase

        DanceWatchLine[0] = "Аманда продолжает свой танец с мессиром Легаре."
        if AmandaVar["alberdanceadvance"] == 2:
            DanceWatchLine[0] += " Торгаш нежно обнимает ее за талию."
        if AmandaVar["alberdanceadvance"] == 3:
            DanceWatchLine[0] += " Альбер нежно но твердо держит Аманду за попу."
        if AmandaVar["alberdanceadvance"] >= 4:
            DanceWatchLine[0] += " Похотливые ручонки достопочтенного Альбера Легаре нежно сжимают упругую попку Аманды через тонкую ткань ее платья. А она трется своими грудками о его грудь, потихоньку возбуждаясь."
        if AmandaVar["alberdanceadvance"] == 5:
            DanceWatchLine[0] += " При этом он не забывает целовать малышку Аманду а та отвечает ему тем же, с трудом не сбиваясь с ритма танца."

        if int(AmandaVar.get("alberfriends", 0) or 0) < 12 and renpy.random.randint(1, 2) == 1:
            AmandaVar["alberfriends"] = int(AmandaVar.get("alberfriends", 0) or 0) + 1

        slut_friends_increase("amanda", 0, 0, 0, 21, 2, 1)

label EventAmandaLegareCreateDance:
    $ event_amanda_legare_create_dance()
    return
