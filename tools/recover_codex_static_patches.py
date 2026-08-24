import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Call:
    timestamp: str
    call_id: str
    source: str
    patch: str
    output: str = ""


def flatten_output(value):
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "\n".join(
            str(item.get("text", "")) if isinstance(item, dict) else str(item)
            for item in value
        )
    return "" if value is None else str(value)


def decode_js_string(literal):
    try:
        return json.loads(literal)
    except json.JSONDecodeError:
        body = literal[1:-1]
        result = []
        index = 0
        simple = {
            "n": "\n", "r": "\r", "t": "\t", "b": "\b", "f": "\f",
            "v": "\v", "0": "\0", "\\": "\\", '"': '"', "'": "'", "/": "/",
        }
        while index < len(body):
            char = body[index]
            if char != "\\" or index + 1 >= len(body):
                result.append(char)
                index += 1
                continue
            escaped = body[index + 1]
            if escaped in simple:
                result.append(simple[escaped])
                index += 2
            elif escaped == "u" and index + 5 < len(body):
                result.append(chr(int(body[index + 2:index + 6], 16)))
                index += 6
            elif escaped == "x" and index + 3 < len(body):
                result.append(chr(int(body[index + 2:index + 4], 16)))
                index += 4
            elif escaped in "\r\n":
                if escaped == "\r" and index + 2 < len(body) and body[index + 2] == "\n":
                    index += 3
                else:
                    index += 2
            else:
                result.append(escaped)
                index += 2
        return "".join(result)


def decode_static_patch(source):
    patterns = (
        (r'const\s+patch\s*=\s*("(?:\\.|[^"\\])*")', "json"),
        (r'tools\.apply_patch\(\s*("(?:\\.|[^"\\])*")\s*\)', "json"),
    )
    for pattern, kind in patterns:
        match = re.search(pattern, source, re.DOTALL)
        if match:
            return decode_js_string(match.group(1)), kind

    match = re.search(r'const\s+patch\s*=\s*`(?P<body>(?:\\.|[^`])*)`', source, re.DOTALL)
    if match and "${" not in match.group("body"):
        body = match.group("body")
        body = body.replace(r"\`", "`").replace(r"\\", "\\")
        return body, "template"
    return None, None


def load_calls(log_path, cutoff):
    calls = []
    outputs = {}
    with log_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            timestamp = row.get("timestamp", "")
            payload = row.get("payload", {})
            call_id = payload.get("call_id", "")
            if payload.get("type") == "custom_tool_call_output" and call_id:
                outputs[call_id] = flatten_output(payload.get("output"))
                continue
            if timestamp >= cutoff:
                continue
            if payload.get("type") != "custom_tool_call" or payload.get("name") != "exec":
                continue
            source = payload.get("input", "")
            if "tools.apply_patch" not in source:
                continue
            patch, kind = decode_static_patch(source)
            if patch is not None:
                calls.append(Call(timestamp, call_id, kind, patch))
    for call in calls:
        call.output = outputs.get(call.call_id, "")
    return calls


def resolve_patch_path(raw_path, original_root, recovery_root):
    raw_path = raw_path.strip()
    candidate = Path(raw_path)
    if candidate.is_absolute():
        try:
            relative = candidate.relative_to(original_root)
        except ValueError as exc:
            raise ValueError(f"path outside original root: {candidate}") from exc
    else:
        relative = candidate
    resolved = (recovery_root / relative).resolve()
    try:
        resolved.relative_to(recovery_root.resolve())
    except ValueError as exc:
        raise ValueError(f"unsafe recovery path: {resolved}") from exc
    return resolved


def split_sections(patch):
    lines = patch.replace("\r\n", "\n").splitlines()
    sections = []
    current = None
    for line in lines:
        match = re.match(r"\*\*\* (Update|Add|Delete) File: (.+)$", line)
        if match:
            if current:
                sections.append(current)
            current = {"kind": match.group(1), "path": match.group(2), "lines": [], "move": None}
            continue
        if current is None:
            continue
        if line.startswith("*** Move to: "):
            current["move"] = line[len("*** Move to: "):]
            continue
        if line == "*** End Patch":
            sections.append(current)
            current = None
            continue
        current["lines"].append(line)
    if current:
        sections.append(current)
    return sections


def hunk_sequences(lines):
    hunks = []
    current = None
    for line in lines:
        if line.startswith("@@"):
            if current is not None:
                hunks.append(current)
            current = []
            continue
        if current is not None:
            current.append(line)
    if current is not None:
        hunks.append(current)

    result = []
    for hunk in hunks:
        before = []
        after = []
        for line in hunk:
            if line.startswith("-"):
                before.append(line[1:])
            elif line.startswith("+"):
                after.append(line[1:])
            elif line.startswith(" "):
                before.append(line[1:])
                after.append(line[1:])
            elif line == "\\ No newline at end of file":
                continue
            else:
                before.append(line)
                after.append(line)
        result.append(("\n".join(before), "\n".join(after)))
    return result


def replace_once(text, after, before):
    if before and before in text and after not in text:
        return text, True
    candidates = [(after, before)]
    if after and not after.endswith("\n"):
        candidates.append((after + "\n", before + ("\n" if before else "")))
    for needle, replacement in candidates:
        index = text.find(needle)
        if index >= 0:
            return text[:index] + replacement + text[index + len(needle):], True

    before_lines = before.split("\n") if before else []
    after_lines = after.split("\n") if after else []
    prefix = 0
    while prefix < min(len(before_lines), len(after_lines)) and before_lines[prefix] == after_lines[prefix]:
        prefix += 1
    suffix = 0
    while (
        suffix < min(len(before_lines) - prefix, len(after_lines) - prefix)
        and before_lines[-1 - suffix] == after_lines[-1 - suffix]
    ):
        suffix += 1

    trims = []
    for left in range(prefix + 1):
        for right in range(suffix + 1):
            if left == 0 and right == 0:
                continue
            trims.append((left + right, left, right))
    for _, left, right in sorted(trims):
        after_end = len(after_lines) - right if right else len(after_lines)
        before_end = len(before_lines) - right if right else len(before_lines)
        needle = "\n".join(after_lines[left:after_end])
        replacement = "\n".join(before_lines[left:before_end])
        if not needle:
            continue
        positions = [match.start() for match in re.finditer(re.escape(needle), text)]
        if len(positions) == 1:
            index = positions[0]
            return text[:index] + replacement + text[index + len(needle):], True

    removed = [line for line in before_lines if line not in after_lines]
    added = [line for line in after_lines if line not in before_lines]
    removed_block = "\n".join(removed)
    added_block = "\n".join(added)
    if added_block:
        positions = [match.start() for match in re.finditer(re.escape(added_block), text)]
        if len(positions) == 1:
            index = positions[0]
            return text[:index] + removed_block + text[index + len(added_block):], True
    if removed_block and removed_block in text:
        return text, True
    return text, False


def rollback_section(section, original_root, recovery_root):
    kind = section["kind"]
    path = resolve_patch_path(section["path"], original_root, recovery_root)
    move = section["move"]

    if kind == "Add":
        if path.exists():
            path.unlink()
        return []

    if kind == "Delete":
        content = []
        for line in section["lines"]:
            if line.startswith("-"):
                content.append(line[1:])
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(content) + ("\n" if content else ""), encoding="utf-8", newline="")
        return []

    source_path = path
    if move:
        moved_path = resolve_patch_path(move, original_root, recovery_root)
        if moved_path.exists() and not source_path.exists():
            source_path.parent.mkdir(parents=True, exist_ok=True)
            moved_path.replace(source_path)

    if not source_path.exists():
        return [f"missing file: {source_path}"]

    raw = source_path.read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    text = raw.decode("utf-8-sig").replace("\r\n", "\n")
    failures = []
    for before, after in reversed(hunk_sequences(section["lines"])):
        text, changed = replace_once(text, after, before)
        if not changed:
            failures.append(f"context not found: {source_path} :: {after[:160]!r}")
    encoded = text.encode("utf-8")
    if bom:
        encoded = b"\xef\xbb\xbf" + encoded
    source_path.write_bytes(encoded)
    return failures


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("log", type=Path)
    parser.add_argument("recovery_root", type=Path)
    parser.add_argument("--original-root", type=Path, required=True)
    parser.add_argument("--cutoff", required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()

    calls = load_calls(args.log, args.cutoff)
    # The nested apply_patch tool serializes a successful result as `{}` in this
    # session log. Failed/no-op patches are harmless here: exact reverse context
    # will not match and will be reported instead of changing a file.
    applied = calls
    failures = []
    section_count = 0
    for call in reversed(applied):
        sections = split_sections(call.patch)
        for section in reversed(sections):
            section_count += 1
            for failure in rollback_section(section, args.original_root, args.recovery_root):
                failures.append({
                    "timestamp": call.timestamp,
                    "call_id": call.call_id,
                    "path": section["path"],
                    "failure": failure,
                })

    report = {
        "static_calls_found": len(calls),
        "successful_static_calls": len(applied),
        "sections_processed": section_count,
        "failures": failures,
    }
    args.report.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({key: value if key != "failures" else len(value) for key, value in report.items()}))


if __name__ == "__main__":
    main()
