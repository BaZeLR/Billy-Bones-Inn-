# Русские рукописные шрифты

Четыре статических TTF-шрифта для использования в Ren'Py. Каждый содержит
все 33 буквы русского алфавита в верхнем и нижнем регистре, включая Ё/ё.

| Файл | Почерк |
| --- | --- |
| `BadScript-Regular.ttf` | Естественный рукописный; рекомендуемый вариант для писем и дневников |
| `MarckScript-Regular.ttf` | Размашистый наклонный почерк |
| `Caveat-Regular.ttf` | Небрежные короткие записки |
| `Neucha-Regular.ttf` | Неформальные печатные буквы от руки |

## Использование

Ren'Py загружает шрифты прямо из проекта. Для отдельной реплики или записки:

```renpy
"{font=fonts/BadScript-Regular.ttf}Жду тебя вечером у мельницы.{/font}"
"{font=fonts/MarckScript-Regular.ttf}Не забудь запереть трактир.{/font}"
```

Для текста внутри экрана:

```renpy
text "Записка на столе" font "fonts/Caveat-Regular.ttf"
```

Для нового персонажа:

```renpy
define note_author = Character("Автор записки", what_font="fonts/Neucha-Regular.ttf")
```

Чтобы применить почерк к существующему персонажу, добавьте `what_font` в его
текущее определение. Чтобы выбрать основной шрифт стандартного диалога,
измените существующую строку в `game/gui.rpy`:

```renpy
define gui.text_font = "fonts/BadScript-Regular.ttf"
```

Документация: [шрифты и текст](https://www.renpy.org/doc/html/text.html#fonts),
[настройка диалога](https://www.renpy.org/doc/html/gui.html#dialogue).

## Источники и лицензии

Все четыре шрифта распространяются по SIL Open Font License 1.1 и допускают
включение в коммерческую игру. При распространении сохраняйте файлы
авторских прав и лицензий из `licenses/` вместе со шрифтами.

Файлы шрифтов скопированы без изменения их содержимого 18 октября 2026 года:

| Шрифт | Исходный файл | Лицензия |
| --- | --- | --- |
| Bad Script | [Google Fonts](https://github.com/google/fonts/blob/main/ofl/badscript/BadScript-Regular.ttf) | [BadScript-OFL.txt](licenses/BadScript-OFL.txt) |
| Marck Script | [Google Fonts](https://github.com/google/fonts/blob/main/ofl/marckscript/MarckScript-Regular.ttf) | [MarckScript-OFL.txt](licenses/MarckScript-OFL.txt) |
| Caveat | [Caveat](https://github.com/googlefonts/caveat/blob/main/fonts/ttf/Caveat-Regular.ttf) | [Caveat-OFL.txt](licenses/Caveat-OFL.txt) |
| Neucha | [Google Fonts](https://github.com/google/fonts/blob/main/ofl/neucha/Neucha.ttf) | [Neucha-OFL.txt](licenses/Neucha-OFL.txt) |

Исходный `Neucha.ttf` сохранён под именем `Neucha-Regular.ttf`.
