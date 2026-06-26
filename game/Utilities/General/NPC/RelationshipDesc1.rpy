# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# RelationshipDesc1.rpy
# Converted from QSP-like script to Ren'Py

init python:
    def relationship_desc1(GirlNameRD1):
        """
        Returns a string describing the relationship for traktir harassment scenes.
        """
        if GirlNameRD1 == 'sandra':
            return 'твою экономку'
        elif GirlNameRD1 in ('amanda', 'melissa'):
            return 'твою сотрудницу'
        else:
            return 'меня'

# Usage example:
# result = relationship_desc1('amanda')
