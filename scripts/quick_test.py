#!/usr/bin/env python3
import os
import sys
from datetime import datetime
sys.path.insert(0, '.')

# Test per una data
os.environ.setdefault('BIBLE_API_KEY', os.environ.get('BIBLE_API_KEY', ''))

from fetch_gospel import fetch_gospel_day

result = fetch_gospel_day("2026-03-19")
print(f"Result keys: {result.keys() if result else 'None'}")
for k, v in (result or {}).items():
    if k.startswith('gospel_text'):
        print(f"{k}: {v[:100] if v else 'EMPTY'}...")
