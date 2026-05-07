# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# AdjustOtkroven.rpy
# Converted from legacy script. Adjusts 'otkroven' stat for a given girl based on friendship and specific rules.
# All logic and conditions preserved.

init python:
    def adjust_otkroven(girl_name):
        otkroven[girl_name] = 0
        if girl_name == 'georgett':
            if Friends[girl_name] >= 5 and otkroven[girl_name] <= 3:
                otkroven[girl_name] = 3
            if Friends[girl_name] >= 8 and otkroven[girl_name] <= 5:
                otkroven[girl_name] = 5
            if Friends[girl_name] >= 9 and otkroven[girl_name] <= 6:
                otkroven[girl_name] = 6
            if Friends[girl_name] >= 10 and otkroven[girl_name] <= 7:
                otkroven[girl_name] = 7
        elif girl_name == 'liza':
            if Friends[girl_name] >= 4 and otkroven[girl_name] <= 3:
                otkroven[girl_name] = 3
            if Friends[girl_name] >= 7 and otkroven[girl_name] <= 5:
                otkroven[girl_name] = 5
            if Friends[girl_name] >= 6 and otkroven[girl_name] <= 6:
                otkroven[girl_name] = 6
            if Friends[girl_name] >= 8 and otkroven[girl_name] <= 7:
                otkroven[girl_name] = 7
        elif girl_name in ['amanda', 'melissa', 'sandra']:
            if Friends[girl_name] >= 6 and otkroven[girl_name] <= 3:
                otkroven[girl_name] = 3
            if Friends[girl_name] >= 8 and otkroven[girl_name] <= 5:
                otkroven[girl_name] = 5
            if Friends[girl_name] >= 11 and otkroven[girl_name] <= 6:
                otkroven[girl_name] = 6
            if Friends[girl_name] >= 13 and otkroven[girl_name] <= 7:
                otkroven[girl_name] = 7
        else:
            if Friends[girl_name] >= 6 and otkroven[girl_name] <= 3:
                otkroven[girl_name] = 3
            if Friends[girl_name] >= 8 and otkroven[girl_name] <= 5:
                otkroven[girl_name] = 5
            if Friends[girl_name] >= 11 and otkroven[girl_name] <= 6:
                otkroven[girl_name] = 6
            if Friends[girl_name] >= 13 and otkroven[girl_name] <= 7:
                otkroven[girl_name] = 7

# Usage: call from python with adjust_otkroven(girl_name)
