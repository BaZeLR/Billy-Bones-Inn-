import os
import re
import json
import csv
import xml.etree.ElementTree as ET

# === CONFIGURATION ===
base_dir = r"C:\Users\blank\Downloads\Traktir Wild Stallion 0.05\output"
locations_dir = base_dir
json_output_dir = os.path.join(base_dir, "json")
csv_output_dir = os.path.join(base_dir, "spreadsheet")
xml_keywords_file = os.path.join(base_dir, "keywords.xml")  # Updated path to use local file

# Ensure output folders exist
os.makedirs(json_output_dir, exist_ok=True)
os.makedirs(csv_output_dir, exist_ok=True)

# === PARSE XML KEYWORDS ===
movement_keywords = {"GOTO", "GT", "XGOTO", "XGT", "JUMP"}
dialog_keywords = {"PL", "P", "NL", "MSG"}
system_keywords = {"SET", "LET", "IF", "WAIT", "KILLVAR", "TIMER", "DYNAMIC"}
action_keywords = {"ACT", "DELACT", "MENU"}
visual_keywords = {"VIEW", "PLAY", "CLOSE"}

all_known_keywords = set()
print(f"📂 Loading XML from: {xml_keywords_file}")

tree = ET.parse(xml_keywords_file)
root = tree.getroot()

for elem in root.iter('Keyword'):
    keyword = elem.attrib.get('name')
    if keyword:
        all_known_keywords.add(keyword.upper())

print(f"✅ Loaded {len(all_known_keywords)} known keywords from XML.")

# === ANALYZE LOCATIONS ===
classified_locations = []

location_files = [f for f in os.listdir(locations_dir) if f.endswith('.txt')]
print(f"🔍 Found {len(location_files)} location files.\n")

for filename in location_files:
    filepath = os.path.join(locations_dir, filename)
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
    except UnicodeDecodeError:
        with open(filepath, 'r', encoding='utf-16') as file:
            content = file.read()

    location_name = os.path.splitext(filename)[0]
    content_upper = content.upper()
    name_lower = location_name.lower()

    detected_commands = []
    for keyword in all_known_keywords:
        if re.search(r'\b' + re.escape(keyword) + r'\b', content_upper):
            detected_commands.append(keyword)

    # === SCORING ===
    score = {
        "movement": sum(1 for k in detected_commands if k in movement_keywords),
        "dialog": sum(1 for k in detected_commands if k in dialog_keywords),
        "system": sum(1 for k in detected_commands if k in system_keywords),
        "action": sum(1 for k in detected_commands if k in action_keywords),
        "visual": sum(1 for k in detected_commands if k in visual_keywords),
    }

    # === NAME-BASED HEURISTICS ===
    guessed_type = "unknown"
    notes = []

    if re.search(r'(home|room|house|hall|kitchen|tavern|inn|shop|market|alley|bath|garden|cellar)', name_lower):
        guessed_type = "world_location"
        notes.append("semantic world name detected")
    elif re.search(r'^(amanda|melissa|sandra|becky|virgo|npc|name)', name_lower):
        guessed_type = "npc"
        notes.append("semantic npc name detected")
    elif re.search(r'(cutscene|scene|intro)', name_lower):
        guessed_type = "cutscene"
        notes.append("semantic cutscene name detected")
    elif re.search(r'(proc|system|timer|stat|logic)', name_lower):
        guessed_type = "system_logic"
        notes.append("semantic system name detected")
    elif re.search(r'(fight|event|encounter|trigger|molest|kiss)', name_lower):
        guessed_type = "event"
        notes.append("semantic event name detected")

    # === FALLBACK: SCORE-BASED TYPE INFERENCE ===
    if guessed_type == "unknown":
        if score["movement"] >= 1:
            guessed_type = "world_location"
            notes.append("movement commands detected")
        elif score["dialog"] >= 2:
            guessed_type = "dialog"
            notes.append("heavy dialog content detected")
        elif score["system"] >= 2:
            guessed_type = "system_logic"
            notes.append("heavy system commands detected")

    # === TABLE STRUCTURE DETECTION ===
    tables_detected = bool(re.search(r'^[A-Z0-9_]+ *= *.+$', content, flags=re.MULTILINE))
    if tables_detected:
        notes.append("table structure detected")

    # === SAVE ENTRY ===
    location_entry = {
        "filename": filename,
        "location_name": location_name,
        "type": guessed_type,
        "detected_keywords": detected_commands,
        "semantic_score": score,
        "notes": notes,
        "tables_detected": tables_detected
    }

    classified_locations.append(location_entry)
    print(f"📄 Processed: {filename} ➔ {guessed_type}")

# === SAVE JSON OUTPUT ===
json_path = os.path.join(json_output_dir, "classified_locations.json")
with open(json_path, 'w', encoding='utf-8') as json_file:
    json.dump(classified_locations, json_file, ensure_ascii=False, indent=2)

print(f"\n✅ JSON saved to: {json_path}")

# === SAVE CSV OUTPUT ===
csv_path = os.path.join(csv_output_dir, "classified_locations.csv")
with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ["filename", "location_name", "type", "detected_keywords", "semantic_score", "notes", "tables_detected"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for entry in classified_locations:
        writer.writerow({
            "filename": entry["filename"],
            "location_name": entry["location_name"],
            "type": entry["type"],
            "detected_keywords": json.dumps(entry["detected_keywords"], ensure_ascii=False),
            "semantic_score": json.dumps(entry["semantic_score"], ensure_ascii=False),
            "notes": "; ".join(entry["notes"]),
            "tables_detected": entry["tables_detected"]
        })

print(f"✅ CSV saved to: {csv_path}")
