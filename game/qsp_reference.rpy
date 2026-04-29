# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# QSP to Ren'Py Reference Guide
# This file contains helpful information for converting QSP syntax to Ren'Py

init python:
    # Dictionary mapping QSP statements to Ren'Py equivalents
    qsp_to_renpy_statements = {
        "pl": "Equivalent to adding text in Ren'Py dialogue",
        "clear/clr": "Use 'scene' or 'window hide' in Ren'Py",
        "p": "Standard dialogue in Ren'Py",
        "nl": "Line break (\\n) in Ren'Py",
        "msg": "Use renpy.notify() in Ren'Py",
        "wait": "Use renpy.pause() in Ren'Py",
        "act": "Create menu options or buttons in Ren'Py",
        "delact": "Remove buttons or menu options in Ren'Py",
        "cla": "Clear all actions - use new screen or menu in Ren'Py",
        "cls": "Use 'scene' in Ren'Py",
        "menu": "Use Ren'Py's menu system",
        "settimer": "Schedule events with renpy.call_in_future()",
        "dynamic": "Execute Python code with the 'python:' or '$ ' syntax",
        "set/let": "Use standard assignment in Python blocks",
        "killvar": "Delete variables with 'del' in Python",
        "copyarr": "Copy lists with Python's copy methods",
        "addobj": "Add items to inventory in Ren'Py using Python dictionaries",
        "delobj": "Remove items from inventory",
        "jump": "Use Ren'Py's 'jump' command",
        "gosub/gs": "Use Ren'Py's 'call' command",
        "goto/gt": "Use Ren'Py's 'jump' command",
        "play": "Use Ren'Py's audio system: play music/sound"
    }
    
    # Dictionary mapping QSP expressions to Ren'Py equivalents
    qsp_to_renpy_expressions = {
        "and": "and in Python/Ren'Py",
        "or": "or in Python/Ren'Py",
        "obj": "Check item in inventory dictionary",
        "loc": "Check if label exists with renpy.has_label()",
        "no": "not in Python/Ren'Py",
        "mod": "% (modulo) in Python/Ren'Py",
        "iif": "x if condition else y in Python/Ren'Py",
        "input": "Use renpy.input() in Ren'Py",
        "rand": "Use renpy.random.randint() in Ren'Py",
        "rgb": "Use Ren'Py's color system",
        "arrsize": "Use len() in Python/Ren'Py",
        "instr": "Use 'in' or str.find() in Python/Ren'Py",
        "isnum": "Use str.isdigit() or try/except with int()",
        "trim": "Use str.strip() in Python/Ren'Py",
        "ucase": "Use str.upper() in Python/Ren'Py",
        "lcase": "Use str.lower() in Python/Ren'Py",
        "len": "Use len() in Python/Ren'Py",
        "mid": "Use string slicing in Python/Ren'Py",
        "replace": "Use str.replace() in Python/Ren'Py",
        "str": "Use str() in Python/Ren'Py",
        "val": "Use int() or float() in Python/Ren'Py"
    }

# Screen to display QSP to Ren'Py reference information
screen qsp_reference():
    tag menu
    
    frame:
        style_prefix "game_menu"
        xfill True
        yfill True
        
        vbox:
            spacing 20
            
            label "QSP to Ren'Py Reference":
                xalign 0.5
                text_size 30
            
            hbox:
                spacing 20
                
                # Statements column
                vbox:
                    spacing 10
                    label "QSP Statements" text_size 20
                    viewport:
                        mousewheel True
                        scrollbars "vertical"
                        yfill True
                        vbox:
                            for keyword, explanation in sorted(qsp_to_renpy_statements.items()):
                                hbox:
                                    spacing 10
                                    text keyword size 18 color "#88c"
                                    text explanation size 16
                                null height 5
                
                # Expressions column
                vbox:
                    spacing 10
                    label "QSP Expressions" text_size 20
                    viewport:
                        mousewheel True
                        scrollbars "vertical"
                        yfill True
                        vbox:
                            for keyword, explanation in sorted(qsp_to_renpy_expressions.items()):
                                hbox:
                                    spacing 10
                                    text keyword size 18 color "#8c8"
                                    text explanation size 16
                                null height 5
            
            textbutton "Return":
                action Return()
                xalign 0.5

# Label to access the reference screen
label qsp_reference:
    call screen qsp_reference
    return
