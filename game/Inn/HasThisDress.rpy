# HasThisDress.rpy
# QSP parity: checks whether dress code exists in an array variable by name.
# Example from TXT: Func('HasThisDress', 'MyDresses', 'citydress')

init python:
    def _dress_key_sort(value):
        s = str(value)
        return (0, int(s)) if s.isdigit() else (1, s)

    def _dress_list_attr_name(array_var_name):
        key = str(array_var_name or "").strip()
        if key.startswith("$"):
            key = key[1:]
        return key

    def _normalize_dress_list_var(array_var_name):
        key = _dress_list_attr_name(array_var_name)
        data = getattr(renpy.store, key, [])

        if isinstance(data, list):
            normalized = list(data)
        elif isinstance(data, tuple):
            normalized = list(data)
        elif isinstance(data, set):
            normalized = list(data)
        elif isinstance(data, dict):
            sorted_items = sorted(data.items(), key=lambda kv: _dress_key_sort(kv[0]))
            if all(str(k).isdigit() for k, _dress_value in sorted_items):
                normalized = [v for _dress_key, v in sorted_items]
            elif all(isinstance(v, (int, bool)) for _dress_key, v in sorted_items):
                normalized = [k for k, v in sorted_items if bool(v)]
            else:
                normalized = []
                for k, v in sorted_items:
                    if isinstance(v, str) and v.strip():
                        normalized.append(v)
                    elif bool(v):
                        normalized.append(k)
        elif isinstance(data, str):
            normalized = [data] if data else []
        else:
            normalized = []

        out = []
        for item in normalized:
            val = str(item or "").strip()
            if val and val not in out:
                out.append(val)

        setattr(renpy.store, key, out)
        return out

    def HasThisDress(array_var_name="MyDresses", dress_code=""):
        dress = str(dress_code or "").strip()
        if not dress:
            return 0
        wardrobe = _normalize_dress_list_var(array_var_name)
        return 1 if dress in wardrobe else 0

    def has_this_dress(array_var_name="MyDresses", dress_code=""):
        return HasThisDress(array_var_name, dress_code)

    def has_this_dress_for_character(character_name, dress_code):
        key = str(character_name or "").strip() + "Dresses"
        return HasThisDress(key, dress_code)


label HasThisDress(array_var_name="MyDresses", dress_code=""):
    $ Result = HasThisDress(array_var_name, dress_code)
    return Result


label has_this_dress(array_var_name="MyDresses", dress_code=""):
    $ Result = HasThisDress(array_var_name, dress_code)
    return Result
