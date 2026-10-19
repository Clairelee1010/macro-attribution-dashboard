"""Keep buildless entry scripts self-contained, with one canonical navigation source."""
from pathlib import Path
root=Path(__file__).resolve().parent.parent
core=(root/'assets/navigation-core.js').read_text()
marker='/* NAV-003-END */'
for name in ['assets/fieldwork.js','assets/research-bridge.js','learn/lab.js']:
 path=root/name
 text=path.read_text()
 if marker in text:text=text.split(marker,1)[1].lstrip('\n')
 path.write_text(core.rstrip()+'\n\n'+text)
