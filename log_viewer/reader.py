# log_viewer/reader.py

def read_lines(path):
    """Read all lines from the file, return list of strings without trailing newlines."""
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        return [line.rstrip('\n') for line in f]