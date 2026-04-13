init -115 python:
    import renpy.exports as renpy

    def dyneval(target, *args):
        """
        Legacy QSP-compatible dynamic evaluator.
        Accepts a callable, label name, or function name string.
        """
        if target is None:
            return 0

        if callable(target):
            return target(*args)

        target_name = str(target).strip()
        if target_name == "":
            return 0

        if renpy.has_label(target_name):
            rv = renpy.call(target_name, *args)
            if rv is not None:
                return rv
            return Result

        if renpy.has_label(target_name.lower()):
            rv = renpy.call(target_name.lower(), *args)
            if rv is not None:
                return rv
            return Result

        return 0
