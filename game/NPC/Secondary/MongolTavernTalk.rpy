label MongolTavernTalk:
    $ main_ui_begin_talk_state("Разговор с Монголом", "mongol")
    vscene "mongol portrait1"
    $ scene_runtime.text = "Монгол отрывается от сбруи. «Да, мастер? Коней я накормил. Карета тоже под рукой — только скажи, когда ехать»."
    $ scene_runtime.location_text = scene_runtime.text
    while True:
        menu:
            "Спросить о работе":
                $ scene_runtime.text = str(getattr(Mongol, "last_service_report", "") or "Первый рабочий день ещё впереди. Монгол уже осматривает конюшню и запас дров.")
                $ scene_runtime.location_text = scene_runtime.text
            "Взять Монгола на охоту" if "mongol" not in player.combat.party:
                $ player.add_party_member("mongol")
                $ scene_runtime.text = "«Сходим вместе, мастер. Я звериную тропу вижу даже там, где ты одну грязь разглядишь», — говорит Монгол и берёт дорожный нож."
                $ scene_runtime.location_text = scene_runtime.text
            "Попросить Монгола остаться при конюшне" if "mongol" in player.combat.party:
                $ player.remove_party_member("mongol")
                $ scene_runtime.text = "Монгол возвращается к лошадям: «Буду здесь. Только свистни, когда снова пойдём в лес»."
                $ scene_runtime.location_text = scene_runtime.text
            "Спросить о ночной лесной тропе" if story_event_available("talk_mongol", "moon_sabbath_guide"):
                call checkTriggers("talk_mongol", "moon_sabbath_guide", 0)
                vscene "mongol portrait1"
            "Закончить разговор":
                $ main_ui_end_talk_state()
                if str(rooms.current_code or "") == "TavernStable":
                    $ main_ui_runtime.action_items = tavern_stable_action_items()
                elif str(rooms.current_code or "") == "Forest":
                    $ main_ui_runtime.action_items = forest_action_items()
                return
