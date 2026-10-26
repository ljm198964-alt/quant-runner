"""Read-only reporting of existing M3 shadow events."""
import json
from pathlib import Path

def summarize(path):
    counts = {}
    for line in Path(path).open():
        if line.strip():
            event = json.loads(line)
            key = event.get('protocol', 'UNKNOWN')
            counts[key] = counts.get(key, 0) + 1
    return counts
