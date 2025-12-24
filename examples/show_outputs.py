from log_viewer import searcher
from log_viewer.formatters import text as text_fmt, json_fmt
from pathlib import Path
p = Path(__file__).parent / 'sample.log'
rep = searcher.search(str(p), 'keyword', context=1)
print('--- ENHANCED (TEXT) ---')
print(text_fmt.format(rep))
print('--- ENHANCED (JSON) ---')
print(json_fmt.format(rep))
