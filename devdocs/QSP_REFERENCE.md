# QSP To Ren'Py Reference Guide

This document is a conversion reference only. It does not belong in `game/` as an `.rpy` script because it is not runtime content.

## QSP Statements

| QSP | Ren'Py / Python equivalent |
| --- | --- |
| `pl` | Equivalent to adding text in Ren'Py dialogue |
| `clear/clr` | Use `scene` or `window hide` in Ren'Py |
| `p` | Standard dialogue in Ren'Py |
| `nl` | Line break `\n` in Ren'Py |
| `msg` | Use `renpy.notify()` in Ren'Py |
| `wait` | Use `renpy.pause()` in Ren'Py |
| `act` | Create menu options or buttons in Ren'Py |
| `delact` | Remove buttons or menu options in Ren'Py |
| `cla` | Clear all actions; use a new screen or menu in Ren'Py |
| `cls` | Use a new `scene` in Ren'Py; `cls` means clear screen |
| `menu` | Use Ren'Py's menu system |
| `settimer` | Schedule events with `renpy.call_in_future()` |
| `dynamic` | Execute Python code with a `python:` block or `$` statement |
| `set/let` | Use standard assignment in Python blocks |
| `killvar` | Delete variables with `del` in Python |
| `copyarr` | Copy lists with Python's copy methods |
| `addobj` | Add items to inventory in Ren'Py using Python dictionaries |
| `delobj` | Remove items from inventory |
| `jump` | Use Ren'Py's `jump` command |
| `gosub/gs` | Use Ren'Py's `call` command |
| `goto/gt` | Use Ren'Py's `jump` command |
| `play` | Use Ren'Py's audio system: `play music` or `play sound` |

## QSP Expressions

| QSP | Ren'Py / Python equivalent |
| --- | --- |
| `and` | `and` in Python/Ren'Py |
| `or` | `or` in Python/Ren'Py |
| `obj` | Check item in inventory dictionary |
| `loc` | Check if label exists with `renpy.has_label()` |
| `no` | `not` in Python/Ren'Py |
| `mod` | `%` modulo operator |
| `iif` | `x if condition else y` |
| `input` | Use `renpy.input()` in Ren'Py |
| `rand` | Use `renpy.random.randint()` in Ren'Py |
| `rgb` | Use Ren'Py's color system |
| `arrsize` | Use `len()` in Python/Ren'Py |
| `instr` | Use `in` or `str.find()` |
| `isnum` | Use `str.isdigit()` or `try/except` with `int()` |
| `trim` | Use `str.strip()` |
| `ucase` | Use `str.upper()` |
| `lcase` | Use `str.lower()` |
| `len` | Use `len()` |
| `mid` | Use string slicing |
| `replace` | Use `str.replace()` |
| `str` | Use `str()` |
| `val` | Use `int()` or `float()` |
