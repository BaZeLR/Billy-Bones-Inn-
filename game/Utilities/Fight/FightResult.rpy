# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# Converted from FightResult.txt legacy script

init python:
    def FightResult(Enemy1, Enemy2, DrawPossible=0):
        """
        Determines the winner of a fight between two opponents.
        
        Parameters:
        Enemy1 (int): First opponent's strength level
        Enemy2 (int): Second opponent's strength level
        DrawPossible (int): Whether a draw is possible (0=no, 1=yes)
        
        Returns:
        int: 1 if strongest wins, 2 if weakest wins, 0 for a draw
        """
        Winner = 0
        # 1 = strongest, 2 = weakest, 0 = draw
        LevelDiff = Enemy1 - Enemy2
        if LevelDiff < 0:
            LevelDiff = -LevelDiff
        if DrawPossible != 0:
            DrawPossible = 1
        
        # Use the project RNG so rollback/replay produces the same outcome.
        RandVar = procedural_randint(
            1,
            1 + DrawPossible * 3 + 1 + LevelDiff * 3,
            key="fight_result:%s:%s:%s:%s" % (Enemy1, Enemy2, DrawPossible, calendar_v2.clock_minutes()),
        )
        
        if RandVar == 1:
            Winner = 2  # Weaker opponent wins (upset)
        elif DrawPossible == 1 and RandVar <= 4:
            Winner = 0  # Draw
        else:
            Winner = 1  # Stronger opponent wins
        
        # If Enemy2 is actually stronger, flip the result
        if Enemy2 > Enemy1:
            if Winner == 1:
                Winner = 2
            elif Winner == 2:
                Winner = 1
        
        return Winner
