"""Second opinion on every kanji reading in the Japanese lessons and the phrasebook: compares
each reading with a dictionary's (pykakasi; pip install pykakasi). A dictionary reads words out of
context, so differences need a human look; reviewed ones are kept in kanji_reviewed.json and only
new differences are reported."""
import json, os, re, sys
import pykakasi
sys.path.insert(0, '/home/user/Aoi/aoi-teacher/phrasebook')
from kana import to_hira
K = pykakasi.kakasi()
KANJI = re.compile(r'[一-鿿々ヶ]')
def hira(s): return to_hira(re.sub(r'[^぀-ヿー一-鿿々ヶ]', '', s))
def dict_reading(jp): return to_hira(''.join(x['hira'] for x in K.convert(re.sub(r'[、。！？「」『』…\s]', '', jp))))
items = []
src = open('/home/user/Aoi/aoi-teacher/grammar/japanese.js', encoding='utf-8').read()
D = json.loads(src[src.index('=') + 1:].rstrip().rstrip(';'))
def walk(o, where):
    if isinstance(o, dict):
        if 's' in o and isinstance(o['s'], list):
            for w in o['s']:
                if KANJI.search(w[0]): items.append((where, w[0], w[1]))
        if 'jp' in o and 'kana' in o and isinstance(o.get('jp'), str) and o.get('kana'):
            if KANJI.search(o['jp']): items.append((where, o['jp'], o['kana']))
        if 'words' in o and o['words'] and isinstance(o['words'][0], list):
            for w in o['words']:
                if KANJI.search(w[0]) and w[1]: items.append((where + '.words', w[0], w[1]))
        for k, v in o.items(): walk(v, where + '.' + str(k) if len(where) < 40 else where)
    elif isinstance(o, list):
        for i, v in enumerate(o): walk(v, where)
walk(D, 'jp')
pb = open('/home/user/Aoi/aoi-teacher/phrasebook/phrasebook.js', encoding='utf-8').read()
P = json.loads(pb[pb.index('=') + 1:].rstrip().rstrip(';'))
for sec in P:
    for ph in sec['phrases']:
        for k, v in ph['v'].items():
            if v['kana'] and KANJI.search(v['jp']): items.append(('pb.' + ph['id'] + '.' + k, v['jp'], v['kana']))
seen, bad = set(), []
for where, jp, kana in items:
    key = (jp, kana)
    if key in seen: continue
    seen.add(key)
    mine, theirs = hira(kana), dict_reading(jp)
    if mine != theirs: bad.append((where, jp, kana, theirs))
HERE = os.path.dirname(os.path.abspath(__file__))
rv = os.path.join(HERE, 'kanji_reviewed.json')
reviewed = set(json.load(open(rv, encoding='utf-8'))) if os.path.exists(rv) else set()
if '--accept' in sys.argv:
    json.dump(sorted(reviewed | {b[1] + '|' + b[2] for b in bad}), open(rv, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print('recorded', len(bad), 'differences as reviewed'); sys.exit(0)
new = [b for b in bad if b[1] + '|' + b[2] not in reviewed]
print('checked', len(seen), 'distinct kanji words/phrases;', len(bad) - len(new), 'reviewed differences;', len(new), 'new')
for b in new: print(' | '.join(b) + '   (dictionary says: ' + b[3] + ')')
sys.exit(1 if new else 0)
