init python:
    def amanda_birth_ready():
        return bool(Amanda.birth_ready())


label story_amanda_give_birth_0:
    call GiveBirth("amanda")
    return True
