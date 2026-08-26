# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================

label IntAlberTalk:
    $ renpy.dynamic("_alber_talk_new", "_alber_talk_picture", "_alber_talked", "_alber_relation", "_alber_provoked", "_int_alber_randvar")
    $ Alber.mark_known()
    $ _alber_provoked = 0
    $ _alber_talk_new = str(main_ui_runtime.mode or "") != "talk" or str(main_ui_runtime.selected_char or main_ui_runtime.girl_key or "").strip().lower() != "alber"
    $ main_ui_begin_talk_state("Разговор с Альбером", "alber")
    if _alber_talk_new:
        if str(rooms.current_code or "") == "WineStore":
            $ _alber_talk_picture = str(alber_random_portrait() or "").strip()
            if _alber_talk_picture:
                vscene _alber_talk_picture
    if _alber_talk_new:
        $ scene_runtime.text = "Альбер Легаре вопросительно смотрит на вас, ожидая продолжения разговора."
        $ scene_runtime.location_text = scene_runtime.text

    while True:
        $ _alber_talked = Alber.talk_count()
        $ _alber_relation = people_to_int(Alber.rel, 0)
        menu:
            "Поболтать со мессиром Легаре о разной всячине." if _alber_talked <= 2 and _alber_provoked == 0:
                $ scene_runtime.text = "Вы некоторое время болтаете со Альбером Легаре о несущественных вещах."
                if procedural_randint(1, 2, "alber_smalltalk_%s_%s" % (current_game_day(), _alber_talked)) == 1 and _alber_relation < 5:
                    $ scene_runtime.text += "\n\nВы немного сдружились с мессиром Легаре."
                    $ Alber.add_relation(1)
                $ Alber.finish_talk()
                $ scene_runtime.location_text = scene_runtime.text

            "Поболтать с мессиром Легаре о более личных вещах" if _alber_relation >= 6 and _alber_talked <= 2 and _alber_provoked == 0:
                $ scene_runtime.text = "Вы некоторое время болтаете с Альбером о его жизни, отношениях с семьей и прочем."
                if procedural_randint(1, 2, "alber_personal_%s_%s" % (current_game_day(), _alber_talked)) == 1 and _alber_relation <= 10:
                    $ scene_runtime.text += "\n\nВы немного сдружились с мессиром Легаре."
                    $ Alber.add_relation(1)
                $ Alber.finish_talk()
                $ scene_runtime.location_text = scene_runtime.text

            "Спросить мессира Легаре о Лизетте" if _alber_relation >= 5 and Alber.liza_encounter_seen and _alber_talked <= 2 and _alber_provoked == 0:
                if not Alber.talked_about_liza:
                    $ scene_runtime.text = "Набравшись смелости, вы говорите Альберу что видели как у него отсасывала Лизетта. Виноторговец сначала смущается, но потом говорит вам, что его жена постоянно занята по хозяйству и он не видит ничего плохого чтобы воспользоваться страстными губками похотливой мулатки. \"Кстати\", добавлят он: \"господин Стефан, вы, как владелец трактира, можете позвать этих двух достойных дам работать у вас. Вам будет доход, посетителей будет больше и нам,страждующим, хе-хе, будет поудобнее чем на улице\"."
                    $ Alber.add_relation(1)
                    $ Alber.talked_about_liza = True
                else:
                    $ scene_runtime.text = "Вы некоторое время болтаете с Альбером о жарких губках Лизетты. Он замечает вам, что хотя Лизетта не столь опытна как ее мать, он обычно предпочитает ее, а почему - сам не знает."
                $ Alber.finish_talk()
                $ scene_runtime.location_text = scene_runtime.text

            "Попробовать помириться" if Alber.amanda_conflict_stage > 0 and _alber_talked <= 2 and _alber_provoked == 0:
                $ scene_runtime.text = "\"Эй, Альбер, чего ты так надулся?\" примирительно сказали вы. \"Ну увидел я тебя с Амандой, ну вспылил. Ну подрались мы малость, бывает. Все, проехали. \" и вы протянули месье свою руку. Тот немного поколебался, но все-таки ее пожал. \"Ладно, проехали\" согласился он.\n\nВы развернулись, чтобы уйти, но услышали, как месье пробормотал сквозь зубы:"
                if Amanda.had_sex_with_legare:
                    $ scene_runtime.text += "\n\n\"А все таки я ее отымел.\""
                elif Amanda.performed_oral_with_legare:
                    $ scene_runtime.text += "\n\n\"И все таки я ее отымею, раз она у меня уже отсосала.\""
                else:
                    $ scene_runtime.text += "\n\n\"И все таки я ее отымею.\""
                $ Alber.finish_talk()
                $ Alber.add_relation(2, 10)
                $ Alber.amanda_conflict_stage = 0
                $ _alber_provoked = 1
                $ scene_runtime.location_text = scene_runtime.text

            "Проигнорировать" if _alber_provoked != 0:
                $ _alber_provoked = 0
                $ scene_runtime.text = "\"Да не мое это дело, Аманда уже достаточно взрослая,\" подумали вы."
                $ scene_runtime.location_text = scene_runtime.text

            "Обругать месье" if _alber_provoked != 0:
                $ scene_runtime.text = "\"Ах ты ублюдок,\" завелись вы от слов Легаре. \"На девочек молоденьких тебя, значит потянуло. Я тебе, дрищу расфранченному, яйца пообрываю и в глотку твою поганую затолкаю. Отымеет он ее, сволочь. Фантазер хренов, ебарь-неудачник блин нашелся.\"\n\nВыразив таким образом обуревавшие вас чувства невозмутимому Легаре, вы отправились восвояси. Похоже что попытка помириться не задалась."
                $ _alber_provoked = 0
                $ Alber.amanda_conflict_stage = 2
                $ Alber.rel = max(1, people_to_int(Alber.rel, 0) - 2)
                $ scene_runtime.location_text = scene_runtime.text
                $ main_ui_end_talk_state()
                $ apply_movement_time(5, "MarketPlace")
                jump MarketPlace

            "Заехать с правой" if _alber_provoked != 0:
                $ _int_alber_randvar = FightResult(fight_player_level(), 1, 0)
                $ scene_runtime.text = "Слова Альбера привели вас в бешенство. Так что вы, без особых прелюдий, развернулись и врезали месье по наглой морде."
                if _int_alber_randvar == 1:
                    $ scene_runtime.text += "\n\nНаваляв от души любителю девочек, вы напоследок еще раз стукнули его мордой лица о прилавок и довольно удалились восвояси."
                    call ShowImageSeq("alber", "fight", "housewon", 4)
                else:
                    $ scene_runtime.text += "\n\nНо торгаш знал о вашей несдержанности и был готов. Отбив ваш удар, он перехватил вашу руку и, дернув, развернул вас. Не успели вы сообразить что к чему, как смачным пинком виноторговец выкинул вас из своей лавки и захлопнул за вами дверь."
                    call ShowImageSeq("alber", "fight", "houselost", 3)
                $ _alber_provoked = 0
                $ Alber.amanda_conflict_stage = 1
                $ Alber.add_relation(-2)
                $ scene_runtime.location_text = scene_runtime.text
                $ main_ui_end_talk_state()
                $ apply_movement_time(5, "MarketPlace")
                jump MarketPlace

            "Закончить разговор":
                $ main_ui_end_talk_state()
                return
