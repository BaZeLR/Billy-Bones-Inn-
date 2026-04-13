# GetGirlDrunk.rpy
# Converted from legacy script. Handles getting a girl drunk and stat changes.
# All logic and conditions preserved.

init python:
    def get_girl_drunk(girl_name):
        if Drunk[girl_name] == 0:
            Drunk[girl_name] = 1
            sluttiness[girl_name] += 4
            Friends[girl_name] += 2

# Usage: call from python with get_girl_drunk(girl_name)


label get_girl_drunk(girl_name=""):
    $ get_girl_drunk(girl_name)
    return
