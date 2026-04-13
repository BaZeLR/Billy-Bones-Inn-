import re
from pathlib import Path
text = Path(r"c:/Users/blank/Documents/RenPy_Projects/Tractir/game/Inn/InitSandra.txt").read_text(encoding='utf-8')
pattern = re.compile(r"\$RealName\[$GirlName\]=\s*'([^']+)'")
print(pattern.findall(text))
