"""Validate delivery against the supplied expression/pose/gesture checklist."""
import ast
import hashlib
import json
from pathlib import Path
import re
import unittest

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
EXPRESSIONS = {"neutral", "happy", "smiling", "wink", "laughing", "playful", "seductive", "lip_bite",
               "licking_lips", "surprised", "angry", "annoyed", "sad", "crying", "terrified", "disgusted",
               "talking", "arguing", "drunk", "nervous"}
HOME = {"standing_neutral", "hand_on_hip", "arms_crossed", "leaning_forward", "sitting_chair"}
BOUDOIR = {"sitting_legs_crossed", "kneeling", "lying_front", "lying_side", "over_shoulder"}
GESTURES = {"invite", "tease", "think", "shy", "point", "stop", "explain", "dismiss", "welcome", "goodbye"}


class NPCSpriteLibraryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((ROOT/"game/images/npc_sprites/v1/manifest.json").read_text(encoding="utf-8"))
        cls.rpy = (ROOT/"game/Utilities/General/NPC/NPCSpriteLibrary.rpy").read_text(encoding="utf-8")

    def test_inventory_accounts_for_the_exact_reference_list_and_known_gaps(self):
        self.assertFalse(self.manifest["complete"])
        expected_gaps = {("amanda", "boudoir", "kneeling"), ("amanda", "boudoir", "lying_front"),
                         ("clara", "boudoir", "lying_side"), ("sandra", "boudoir", "lying_front"),
                         ("sandra", "boudoir", "over_shoulder")}
        gaps = {(s["npc_id"], s["group"], s["state"]) for s in self.manifest["missing"]}
        self.assertEqual(gaps, expected_gaps)
        sprites = self.manifest["sprites"]
        self.assertEqual(len(sprites), 155)
        self.assertEqual(len({s["path"] for s in sprites}), 155)
        for npc in ("amanda", "clara", "melissa", "sandra"):
            entries = [s for s in sprites if s["npc_id"] == npc]
            self.assertEqual(len(entries)+sum(1 for n, _, _ in gaps if n == npc), 40)
            self.assertEqual(len({s["sha256"] for s in entries}), len(entries))
            for group, expected in (("expressions", EXPRESSIONS), ("home", HOME), ("boudoir", BOUDOIR), ("gestures", GESTURES)):
                delivered = {s["state"] for s in entries if s["group"] == group}
                missing = {state for n, g, state in gaps if n == npc and g == group}
                self.assertFalse(delivered & missing)
                self.assertEqual(delivered | missing, expected)

    def test_pngs_have_valid_alpha_fixed_canvas_clear_border_and_matching_hash(self):
        for sprite in self.manifest["sprites"]:
            with self.subTest(sprite=sprite["path"]):
                path = ROOT/"game"/sprite["path"]
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), sprite["sha256"])
                with Image.open(path) as image:
                    self.assertEqual(image.mode, "RGBA")
                    self.assertEqual(list(image.size), sprite["canvas"])
                    alpha = image.getchannel("A")
                    self.assertEqual(alpha.getextrema(), (0, 255))
                    bounds = alpha.getbbox()
                    self.assertIsNotNone(bounds)
                    self.assertGreaterEqual(bounds[0], 4)
                    self.assertGreaterEqual(bounds[1], 4)
                    self.assertLessEqual(bounds[2], image.width-4)
                    self.assertLessEqual(bounds[3], image.height-4)
                    histogram = alpha.histogram()
                    self.assertEqual(sum(histogram[1:9]), 0)
                    self.assertGreater(histogram[255], 5000)

    def test_all_standalone_images_and_preview_paths_exist(self):
        declarations = re.findall(r'^image (npc_\w+ \w+ \w+) = "([^"]+)"$', self.rpy, re.M)
        self.assertEqual(set(declarations), {(s["image_name"], s["path"]) for s in self.manifest["sprites"]})
        self.assertEqual(len(declarations), 155)
        preview = ast.literal_eval(self.rpy.split("define NPC_SPRITE_PREVIEW = ", 1)[1])
        paths = [path for groups in preview.values() for entries in groups.values() for _, path in entries]
        self.assertEqual(set(paths), {s["path"] for s in self.manifest["sprites"]})

    def test_dialogue_portraits_are_bound_and_embedded_in_all_regular_text_windows(self):
        side_images = re.findall(r'^image side npcface_(\w+) (\w+) = Transform\("([^"]+)"', self.rpy, re.M)
        self.assertEqual(len(side_images), 80)
        self.assertEqual({(npc, expression) for npc, expression, _ in side_images},
                         {(npc, expression) for npc in ("amanda", "clara", "melissa", "sandra") for expression in EXPRESSIONS})
        for npc in ("amanda", "clara", "melissa", "sandra"):
            self.assertIn('define npc_{}_voice = Character('.format(npc), self.rpy)
            self.assertIn('image="npcface_{}"'.format(npc), self.rpy)
        screens = (ROOT/"game/screens.rpy").read_text(encoding="utf-8")
        layout = (ROOT/"game/Utilities/General/Screens/main_layout.rpy").read_text(encoding="utf-8")
        component = (ROOT/"game/Utilities/General/Screens/NPCSpriteDialogue.rpy").read_text(encoding="utf-8")
        self.assertIn('use npc_sprite_dialogue_line(who, what)', screens)
        self.assertIn('use npc_sprite_dialogue_line(who, desc, 20)', layout)
        self.assertIn('use npc_sprite_dialogue_line(who, _text, 20)', layout)
        self.assertIn('SideImage()', component)
        self.assertIn('text what id "what"', component)
        self.assertIn('text who id "who"', component)
        # The lower-left legacy SideImage must not draw a second copy over the
        # integrated portraits used by the new Character aliases.
        self.assertIn('not str(renpy.get_say_image_tag() or "").startswith("npcface_")', screens)

    def test_all_body_poses_have_existing_main_ui_overlay_images(self):
        overlays = re.findall(r'^image (npc_overlay_\w+) = Composite\(\(1536, 1024\), \(448, 224\), "([^"]+)"\)', self.rpy, re.M)
        body = [s for s in self.manifest["sprites"] if s["group"] in ("home", "boudoir")]
        self.assertEqual(len(overlays), 35)
        self.assertEqual(set(overlays), {(s["overlay_name"], s["path"]) for s in body})


if __name__ == "__main__":
    unittest.main()
