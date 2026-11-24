# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Prints the statistics the option rules ask for, for the practice bank and the deck checkpoints:
questions per outcome, key positions, true/false keys, and how often the key is the longest or
shortest option.

  uv run labs/_tools/bank_stats.py
"""
import json, re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def report(name, items):
    singles = [i for i in items if i['type'] == 'single']
    tf = [i for i in items if i['type'] == 'tf']
    ext = 0
    for i in singles:
        lens = [len(o) for o in i['options']]
        k = lens[i['key']]
        ext += k in (max(lens), min(lens))
    print(f'{name}: {len(items)} items, {len(singles)} single, {len(tf)} true/false')
    print('  per outcome', dict(sorted(Counter(i['lo'] for i in items).items())))
    print('  key positions', dict(sorted(Counter(i['key'] for i in singles).items())))
    print('  true/false keys (0 true, 1 false)', dict(sorted(Counter(i['key'] for i in tf).items())))
    print(f'  key longest or shortest in {ext} of {len(singles)}')


bank = json.loads((ROOT / 'assessments/bank.json').read_text(encoding='utf-8'))['questions']
report('bank', [dict(type=q['type'], options=q['options'], key=q['correct'][0], lo=q['lo'][0]) for q in bank])

deck = []
for f in sorted((ROOT / 'slides').glob('day*.html')):
    html = f.read_text(encoding='utf-8')
    for kind, quiz in re.findall(r'<div class="quiz" data-type="(\w+)"[^>]*>(.*?)<div class="callout', html, re.S):
        opts = re.findall(r'<div class="opt"([^>]*)>(.*?)</div>', quiz, re.S)
        texts = [re.sub(r'<[^>]+>', '', t).strip() for _, t in opts]
        key = next(n for n, (a, _) in enumerate(opts) if 'data-ok' in a)
        deck.append(dict(type=kind, options=texts, key=key, lo=f.stem))
report('deck checkpoints (by deck)', deck)
