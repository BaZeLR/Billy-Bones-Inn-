# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# ShowImage.rpy
# Converted from legacy script. Utility to show an image based on arguments.
# Handles GraphicsOn flag and builds the image path dynamically.

init python:
    import os
    import re
    import renpy as renpy_module
    import renpy.display.video as renpy_video
    import renpy.exports as renpy
    from renpy.loader import loadable

    MEDIA_IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".webp", ".gif")
    MEDIA_VIDEO_EXTENSIONS = (".webm", ".mkv", ".ogv", ".ogg", ".avi", ".mp4", ".m4v", ".mpg", ".mpeg")
    MEDIA_EXTENSIONS = MEDIA_IMAGE_EXTENSIONS + MEDIA_VIDEO_EXTENSIONS
    MEDIA_ASSET_CASE_INDEX = {
        str(asset_path or "").replace("\\", "/").lower(): str(asset_path or "").replace("\\", "/")
        for asset_path in renpy.list_files()
        if str(asset_path or "").replace("\\", "/").lower().startswith("images/")
    }
    def _normalize_media_ref(media_ref):
        if media_ref is None:
            return ""
        try:
            return str(media_ref or "").strip().replace("\\", "/")
        except Exception:
            return ""

    def _media_asset_exists(media_ref):
        ref = _normalize_media_ref(media_ref)
        if not ref:
            return False
        canonical_ref = MEDIA_ASSET_CASE_INDEX.get(ref.lower(), ref)
        return bool(loadable(canonical_ref))

    def _media_canonical_asset_ref(media_ref):
        ref = _normalize_media_ref(media_ref)
        return MEDIA_ASSET_CASE_INDEX.get(ref.lower(), ref)

    def _media_has_extension(media_ref):
        return bool(os.path.splitext(_normalize_media_ref(media_ref))[1])

    def _media_underscore_digit_variant(media_ref):
        ref = _normalize_media_ref(media_ref)
        if not ref:
            return ""
        root, ext = os.path.splitext(ref)
        match = re.match(r"^(.*?)(\d+)$", root)
        if not match:
            return ""
        variant = match.group(1) + "_" + match.group(2) + ext
        return variant if variant != ref else ""

    def _media_drop_subfolder_variant(media_ref):
        ref = _normalize_media_ref(media_ref)
        if not ref:
            return ""
        parts = ref.split("/")
        if len(parts) < 4 or parts[0].lower() != "images":
            return ""
        return "/".join([parts[0], parts[1], parts[-1]])

    def _media_prefixed_basename_variant(media_ref):
        ref = _normalize_media_ref(media_ref)
        if not ref:
            return ""
        parts = ref.split("/")
        if len(parts) < 3 or parts[0].lower() != "images":
            return ""
        folder_name = str(parts[1] or "").strip()
        basename = str(parts[-1] or "").strip()
        if not folder_name or not basename:
            return ""
        if basename.lower().startswith(folder_name.lower() + "_"):
            return ""
        return "/".join([parts[0], folder_name, folder_name + "_" + basename])

    def _media_candidate_variants(media_ref):
        ref = _normalize_media_ref(media_ref)
        if not ref:
            return []
        variants = [ref]
        underscore_variant = _media_underscore_digit_variant(ref)
        if underscore_variant:
            variants.append(underscore_variant)
        dropped_variant = _media_drop_subfolder_variant(ref)
        if dropped_variant:
            variants.append(dropped_variant)
            dropped_underscore = _media_underscore_digit_variant(dropped_variant)
            if dropped_underscore:
                variants.append(dropped_underscore)
        prefixed_variant = _media_prefixed_basename_variant(ref)
        if prefixed_variant:
            variants.append(prefixed_variant)

        seen = set()
        unique = []
        for variant in variants:
            key = str(variant or "").strip().lower()
            if not key or key in seen:
                continue
            seen.add(key)
            unique.append(variant)
        return unique

    def _has_registered_image(image_name):
        has_image_fn = getattr(renpy, "has_image", None)
        if callable(has_image_fn):
            try:
                return bool(has_image_fn(image_name))
            except Exception:
                return False
        return False

    def _media_is_alias(media_ref):
        ref = _normalize_media_ref(media_ref)
        return bool(ref) and "/" not in ref and not _media_has_extension(ref) and (" " in ref or _has_registered_image(ref))

    def media_is_video_ref(media_ref):
        ref = _normalize_media_ref(media_ref)
        return bool(ref) and os.path.splitext(ref)[1].lower() in MEDIA_VIDEO_EXTENSIONS

    def resolve_media_ref(media_ref):
        ref = _normalize_media_ref(media_ref)
        if not ref:
            return ""
        for variant in _media_candidate_variants(ref):
            if _media_is_alias(variant):
                return variant
            if _media_has_extension(variant):
                if _media_asset_exists(variant) or variant == ref:
                    return _media_canonical_asset_ref(variant)
                continue
            if "/" in variant:
                for ext in MEDIA_EXTENSIONS:
                    candidate = variant + ext
                    if _media_asset_exists(candidate):
                        return _media_canonical_asset_ref(candidate)
        return ref

    def build_media_ref(folder1="", folder2="", image_name=""):
        image_ref = _normalize_media_ref(image_name)
        if not image_ref:
            return ""
        folder1_ref = _normalize_media_ref(folder1)
        folder2_ref = _normalize_media_ref(folder2)

        if "/" in image_ref or _media_has_extension(image_ref):
            return resolve_media_ref(image_ref)
        if not folder1_ref and not folder2_ref and _media_is_alias(image_ref):
            return resolve_media_ref(image_ref)

        path_parts = ["images"]
        if folder1_ref:
            path_parts.append(folder1_ref)
        if folder2_ref:
            path_parts.append(folder2_ref)
        path_parts.append(image_ref)
        return resolve_media_ref("/".join(path_parts))

    def _room_picture_time_key(time_value=None):
        try:
            slot = int(calendar_v2.time_slot() if time_value is None else time_value or 0)
        except Exception:
            slot = 0
        return "night" if slot >= 4 else "day"

    def _bg_declare_location_key(location_code=""):
        raw_key = _normalize_media_ref(location_code or rooms.current_code)
        raw_key = raw_key.replace("’", "").replace("'", "")
        parts = re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)|\d+", raw_key.replace("_", " ").replace("-", " "))
        if parts:
            return "_".join([str(part or "").lower() for part in parts if str(part or "").strip()])
        return raw_key.lower().replace(" ", "_")

    def BGDeclare(location_code="", time_value=None):
        base = _bg_declare_location_key(location_code)
        if not base:
            return ""
        time_key = _room_picture_time_key(time_value)
        for candidate in (
            "images/bg/{}_{}.png".format(base, time_key),
            "images/bg/{}_{}.jpg".format(base, time_key),
            "images/bg/{}_{}.webp".format(base, time_key),
            "images/locations/{}_{}.png".format(base, time_key),
            "images/locations/{}_{}.jpg".format(base, time_key),
            "images/locations/{}_{}.webp".format(base, time_key),
        ):
            if _media_asset_exists(candidate):
                return candidate
        return ""

    def _room_time_variant_ref(base_ref, time_key):
        ref = _normalize_media_ref(base_ref)
        if not ref:
            return ""
        if _media_is_alias(ref):
            alias_variant = ref + "_" + str(time_key or "")
            if _has_registered_image(alias_variant):
                return alias_variant
            return ""

        ext = os.path.splitext(ref)[1].lower()
        if ext:
            path_variant = ref[: -len(ext)] + "_" + str(time_key or "") + ext
            if _media_asset_exists(path_variant):
                return path_variant
            return ""

        for candidate_ext in MEDIA_EXTENSIONS:
            path_variant = ref + "_" + str(time_key or "") + candidate_ext
            if _media_asset_exists(path_variant):
                return path_variant
        return ""

    def resolve_room_background_media(room_obj=None, time_value=None):
        if room_obj is None:
            return ""

        props = getattr(room_obj, "custom_properties", {}) or {}
        time_key = _room_picture_time_key(time_value)
        try:
            slot_key = int(calendar_v2.time_slot() if time_value is None else time_value or 0)
        except Exception:
            slot_key = 0

        candidates = []
        declared_bg = BGDeclare(str(getattr(room_obj, "code_name", "") or ""), time_value)
        if declared_bg:
            candidates.append(declared_bg)

        by_time = props.get("bg_picture_by_time", None)
        if isinstance(by_time, dict):
            for lookup_key in (slot_key, str(slot_key), time_key, "default"):
                candidate = by_time.get(lookup_key, "")
                if candidate:
                    candidates.append(candidate)

        direct_time_picture = props.get("bg_picture_" + time_key, "")
        if direct_time_picture:
            candidates.append(direct_time_picture)

        for fallback_key in ("bg_picture",):
            fallback_candidate = props.get(fallback_key, "")
            if fallback_candidate:
                candidates.append(fallback_candidate)

        base_picture = getattr(room_obj, "bg_picture", "")
        time_variant = _room_time_variant_ref(base_picture, time_key)
        if time_variant:
            candidates.append(time_variant)
        if base_picture:
            candidates.append(base_picture)

        for candidate in candidates:
            resolved = resolve_media_ref(candidate)
            if resolved:
                return resolved
        return ""

    def media_displayable(media_ref):
        resolved = resolve_media_ref(media_ref)
        if not resolved:
            return ""
        if media_is_video_ref(resolved):
            try:
                return renpy_video.Movie(play=resolved, channel="movie", loop=True)
            except Exception:
                return resolved
        return resolved

    def resolve_main_ui_picture(room_obj=None):
        room_base_picture = _normalize_media_ref(getattr(room_obj, "bg_picture", "") if room_obj is not None else "")
        explicit_picture = _normalize_media_ref(scene_runtime.picture)
        current_object_picture = ""

        current_object_key = str(main_ui_runtime.object_id or "").strip()
        if current_object_key:
            current_object = get_game_object(current_object_key)
            if current_object is None:
                current_object = get_game_item(current_object_key)
            current_object_picture = _normalize_media_ref(getattr(current_object, "picture", "") if current_object is not None else "")
            if current_object_picture:
                return media_displayable(current_object_picture)

        uses_room_seed = bool(room_base_picture) and (
            not explicit_picture or explicit_picture == room_base_picture
        )

        if room_obj is not None and uses_room_seed:
            resolved_room_picture = resolve_room_background_media(room_obj)
            if resolved_room_picture:
                return media_displayable(resolved_room_picture)

        return media_displayable(explicit_picture or room_base_picture)

    def show_image(folder1, folder2, image_name):
        try:
            graphics_on = int(GraphicsOn)
        except Exception:
            graphics_on = 1

        if not graphics_on:
            return

        img_path = build_media_ref(folder1, folder2, image_name)
        if not img_path:
            return
        scene_runtime.picture = img_path

        if graphics_on == 1:
            # Main UI mode: image is rendered in the picture viewport from scene_runtime.picture.
            # Avoid duplicate render on master (picture-in-picture effect).
            if renpy.get_screen("main_ui") is not None:
                return
            renpy.scene()
            renpy.show("_layout_black_bg", what=renpy.easy.displayable("#000"), layer="master")
            renpy.show(
                img_path,
                what=renpy.easy.displayable(img_path),
                at_list=[master],
                layer="master",
            )
        else:
            renpy.say(None, "Изображение: " + img_path)

    def show_image_seq(folder1="", folder2="", image_name="", variants=0):
        try:
            n = int(variants or 0)
        except Exception:
            n = 0
        if n > 0:
            pick = procedural_randint(1, n, key="procedural:Utilities/General/Screens/ShowImage.rpy:procedural_randint:430:1")
            return show_image(folder1, folder2, str(image_name) + str(pick))
        return show_image(folder1, folder2, image_name)

# Usage: show_image('irma', 'portraits', 'smile')
# This will show 'images/irma/portraits/smile.jpg' if GraphicsOn is enabled.


label ShowImage(args0="", args1="", args2=""):
    $ show_image(args0, args1, args2)
    return


label ShowImageSeq(args0="", args1="", args2="", args3=0):
    $ show_image_seq(args0, args1, args2, args3)
    return
