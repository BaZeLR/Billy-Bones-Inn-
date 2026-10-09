# Legacy pickle symbol only. The live room-share event is a normal tuple in
# melissaThreadList, so hour, location, and story conditions remain visible to
# the event framework and story board.
init -24 python:
    class MelissaAmandaRoomShareEvent(Event):
        pass
