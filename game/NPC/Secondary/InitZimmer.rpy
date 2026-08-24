        def var_int(self, key, default=0):
            self.ensure_story_defaults()
            return people_to_int(self.var.get(key, default), default)

        def set_var_int(self, key, value):
            self.ensure_story_defaults()
            value = people_to_int(value, 0)
            self.var[key] = value
            self.promote_from_var(self.var)
            return value
            self.location = "CityGuard"            self.location = "CityGuard"        def story_value(self, key, default=0):
            self.ensure_story_defaults()
            self.promote_from_var(self.var)
            return self.var.get(key, default)

        def set_story_value(self, key, value):
            self.ensure_story_defaults()
            self.var[key] = value
            return value


label _auto_register_zimmer:
    call register_zimmer_secondary from _call_zimmer_reg
    return        def var_int(self, key, default=0):
            self.ensure_story_defaults()
            return people_to_int(self.var.get(key, default), default)

        def set_var_int(self, key, value):
            self.ensure_story_defaults()
            value = people_to_int(value, 0)
            self.var[key] = value
            self.promote_from_var(self.var)
            return value
            self.location = "CityGuard"            self.location = "CityGuard"        def story_value(self, key, default=0):
            self.ensure_story_defaults()
            self.promote_from_var(self.var)
            return self.var.get(key, default)

        def set_story_value(self, key, value):
            self.ensure_story_defaults()
            self.var[key] = value
            return value


label _auto_register_zimmer:
    call register_zimmer_secondary from _call_zimmer_reg
    return        def var_int(self, key, default=0):
            self.ensure_story_defaults()
            return people_to_int(self.var.get(key, default), default)

        def set_var_int(self, key, value):
            self.ensure_story_defaults()
            value = people_to_int(value, 0)
            self.var[key] = value
            self.promote_from_var(self.var)
            return value
            self.location = "CityGuard"            self.location = "CityGuard"        def story_value(self, key, default=0):
            self.ensure_story_defaults()
            self.promote_from_var(self.var)
            return self.var.get(key, default)

        def set_story_value(self, key, value):
            self.ensure_story_defaults()
            self.var[key] = value
            return value


label _auto_register_zimmer:
    call register_zimmer_secondary from _call_zimmer_reg
    returninit python:
    def zimmer_story_defaults():
        return {
            "ComplainHorse": 0,
            "SherwoodStory": 0,
            "ComplainRobin": 0,
            "RobinInvestigationDay": 0,
            "MissionUpdatedByPlayer": 0,
            "PlayerHandledRobin": 0,
            "ClaraFianceCaseSolved": 0,
        }

    class ZimmerData(PeopleData):
        code_name = "zimmer"

        def __init__(self):
            super().__init__(
                self.code_name,
                cname="Десятник Циммерман",
                fullname="Десятник Циммерман",
                genitive="Десятника Циммермана",
                dative="Десятнику Циммерману",
                default_location="CityGuard",
                description="Десятник Циммерман - старый начальник городской стражи, осторожный, носатый, кучерявый и всегда готовый объяснить, почему дело сложнее, чем кажется.",
                birth_date={"day": 1, "period": 1, "cycle": 1042},
                portrait="images/zimmer/portrait1.png",
            )

    class ZimmerInfo(BaseNPC):
        """Zimmer: city guard captain, Robin investigation, Blackwood mission."""
        unknown_name = "Десятник Циммерман"

        def __init__(self, name="zimmer", **kwargs):
            super().__init__(name, **kwargs)
            self.data = ZimmerStaticData
            self.known = False
            self.location = "CityGuard"
            self.var = {}
            self.ensure_story_defaults()

        def update(self):
            self.name = people_normalize_id(self.name)
            self.data = ZimmerStaticData
            self.location = "CityGuard"
            self.ensure_story_defaults()
            return self

        def ensure_story_defaults(self):
            if not isinstance(self.var, dict):
                self.var = {}
            for key, value in zimmer_story_defaults().items():
                self.var.setdefault(key, value)
            return self.var

        def story_value(self, key, default=0):
            self.ensure_story_defaults()
            return self.var.get(key, default)

        def set_story_value(self, key, value):
            self.ensure_story_defaults()
            self.var[key] = value
            return value

        def var_int(self, key, default=0):
            self.ensure_story_defaults()
            return people_to_int(self.var.get(key, default), default)

        def set_var_int(self, key, value):
            self.ensure_story_defaults()
            value = people_to_int(value, 0)
            self.var[key] = value
            self.promote_from_var(self.var)
            return value

        def story_value(self, key, default=0):
            self.ensure_story_defaults()
            return self.var.get(key, default)

        def set_story_value(self, key, value):
            self.ensure_story_defaults()
            self.var[key] = value
            return value

        def var_int(self, key, default=0):
            self.ensure_story_defaults()
            return people_to_int(self.var.get(key, default), default)

        def set_var_int(self, key, value):
            self.ensure_story_defaults()
            value = people_to_int(value, 0)
            self.var[key] = value
            self.promote_from_var(self.var)
            return value

        def story_value(self, key, default=0):
            self.ensure_story_defaults()
            return self.var.get(key, default)

        def set_story_value(self, key, value):
            self.ensure_story_defaults()
            self.var[key] = value
            return value

        def var_int(self, key, default=0):
            self.ensure_story_defaults()
            return people_to_int(self.var.get(key, default), default)

        def set_var_int(self, key, value):
            self.ensure_story_defaults()
            value = people_to_int(value, 0)
            self.var[key] = value
            self.promote_from_var(self.var)
            return value

define ZimmerStaticData = ZimmerData()
default Zimmer = ZimmerInfo()

label InitZimmer:
    call register_zimmer_secondary from _call_init_zimmer_register
    return


label InitZimmer:
    call register_zimmer_secondary from _call_init_zimmer_register
    return


label InitZimmer:
    call register_zimmer_secondary from _call_init_zimmer_register
    return


label register_zimmer_secondary:
    python:
        peopleData["zimmer"] = ZimmerStaticData
        Zimmer.update()
        peopleInfo["zimmer"] = Zimmer
        if Zimmer not in secondary_npcs:
            secondary_npcs.append(Zimmer)
    $ ZimmerProfile = "Десятник Циммерман — старый, низкий, носатый, кучерявый начальник городской стражи (десятник). Немного картавит. Любит 'порядок', но очень осторожен (семья, дети, любовницы). Принимает жалобы на конокрадов (лошади) и разбойников в Шервуде/Блэквуде (за деньги). Готов 'поиcкать' Робина, но не арестовывать (не наша земля, слишком опасно). Ключевой NPC для Zimmer mission в Blackwood arc."
    return
