"""Checks the Japanese lessons and writes the data the app embeds, plus the voice clip list.

    python3 build.py      check, then write japanese.js and clips.json

Checks: every word with kanji has a kana reading, kana readings are only kana, every romaji
matches its kana (same checker as the phrasebook), every lesson example exists, every quiz
answer index is valid. Exit status is non-zero on any failure.
"""
import hashlib, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'phrasebook'))
from kana import kana_romaji, norm
from grammar import EX, CHARTS, LESSONS
from words import TOPICS, DIALECT
from stories import STORIES, SONGS

errors = []
KANJI = re.compile(r'[一-鿿々〆ヵヶ]')
NONKANA = re.compile(r'[^぀-ヿー]')
PUNCT_TTS = '、。！？'
clips = {}

def kana_of(jp, kana, where):
    if kana:
        if NONKANA.sub('', kana) != kana:
            errors.append(f"{where}: reading has non-kana characters: {kana}")
        return kana
    if KANJI.search(jp):
        errors.append(f"{where}: '{jp}' has kanji but no reading")
    return NONKANA.sub('', jp)

def same(kana, ro):
    return norm(kana_romaji(kana)) == norm(ro)

def clip(tts):
    tts = tts.strip()
    if tts[-1] not in PUNCT_TTS: tts += '。'
    name = hashlib.sha1(tts.encode('utf-8')).hexdigest()[:12] + '.mp3'
    clips[name] = tts
    return name

ROLE_BY_PARTICLE = {'は': 'topic', 'が': 'subject', 'を': 'object', 'に': 'place', 'で': 'place', 'へ': 'place'}

def make_sentence(segs, ro, en, where, note=""):
    """segs: [[jp, kana, role|None]]. Returns {s: [[jp, kana, role, ro]], ro, en, a, note}."""
    # fold punctuation-only segments into the one before
    merged = []
    for jp, kana, role in segs:
        if merged and not NONKANA.sub('', jp) and not KANJI.search(jp):
            merged[-1][0] += jp
        else:
            merged.append([jp, kana_of(jp, kana, where), role])
    whole = ''.join(k for _, k, _ in merged)
    if not same(whole, ro):
        errors.append(f"{where}: romaji '{ro}' doesn't match '{whole}' ({norm(kana_romaji(whole))} vs {norm(ro)})")
        return None
    # split the romaji across the words
    words = ro.split()
    wi, out = 0, []
    for n, (jp, kana, role) in enumerate(merged):
        target = norm(kana_romaji(kana))
        acc = []
        while wi < len(words) and norm(' '.join(acc)) != target:
            acc.append(words[wi]); wi += 1
        while wi < len(words) and acc and norm(' '.join(acc + [words[wi]])) == target:
            acc.append(words[wi]); wi += 1
        if norm(' '.join(acc)) != target:
            errors.append(f"{where}: couldn't line up romaji with '{jp}'"); return None
        if role is None:
            last = n == len(merged) - 1
            role = 'verb' if last else ROLE_BY_PARTICLE.get(kana[-1:], '') if len(kana) > 1 else ''
        out.append([jp, kana, role, ' '.join(acc)])
    if wi != len(words):
        errors.append(f"{where}: romaji left over: {' '.join(words[wi:])}")
    # what Aoi says: the kana, with the topic は and direction へ written as they sound
    tts = ''
    for jp, kana, role, r in out:
        k = kana
        if len(k) > 1 and role in ('topic', 'place') and k[-1] in 'はへ':
            k = k[:-1] + ('わ' if k[-1] == 'は' else 'え')
        tail = re.sub(r'[^、。！？]', '', jp[len(jp.rstrip('、。！？」』）)')):])
        tts += k + tail
    return {"s": out, "ro": ro, "en": en, "a": clip(tts), "note": note}

def parse(text):
    segs = []
    for tok in text.split():
        m = re.match(r'^(.+?)(?:\[(.+?)\])?(?:/(\w+))?$', tok)
        segs.append([m.group(1), m.group(2) or '', m.group(3)])
    return segs

def sent(d, where):
    return make_sentence(parse(d['t']), d['ro'], d['en'], where, d.get('note', ''))

def form(f, where):
    jp, kana, ro = f
    k = kana_of(jp, kana, where)
    if not same(k, ro): errors.append(f"{where}: romaji '{ro}' doesn't match '{k}'")
    return {"jp": jp, "kana": k if k != jp else "", "ro": ro, "a": clip(k)}

def quiz(qs, where):
    for i, q in enumerate(qs):
        if len(q) != 4 or not (0 <= q[2] < len(q[1])):
            errors.append(f"{where}.quiz[{i}]: bad answer index")
    return [{"q": q[0], "c": q[1], "a": q[2], "x": q[3]} for q in qs]

# --- grammar examples, charts, lessons ---
ex = {}
for k, v in EX.items():
    ex[k] = make_sentence([[a, b, c or ''] for a, b, c in v['segs']], v['ro'], v['en'], 'EX.' + k)

charts = {}
for k, c in CHARTS.items():
    rows = []
    for i, r in enumerate(c['rows']):
        rows.append({"label": r[0], "gloss": r[1], "c": form(r[2], f"{k}[{i}].casual"), "p": form(r[3], f"{k}[{i}].polite")})
    charts[k] = {"title": c['title'], "kana": c['kana'], "en": c['en'], "kind": c['kind'],
                 "cols": c.get('cols', ["Casual", "Polite"]), "rows": rows}

def beat_list(beats, where, local=None):
    out = []
    for i, b in enumerate(beats):
        o = {"say": b['say']}
        e = b.get('ex')
        if isinstance(e, dict):
            o['ex'] = sent(e, f"{where}.beat{i}")
        elif e:
            if e not in ex: errors.append(f"{where}.beat{i}: no example '{e}'")
            else: o['ex'] = ex[e]
        if b.get('particle'): o['particle'] = b['particle']
        if b.get('chart'):
            name, rows, cols = b['chart']
            if name not in charts or max(rows) >= len(charts[name]['rows']):
                errors.append(f"{where}.beat{i}: bad chart {b['chart']}")
            o['chart'] = {"name": name, "rows": rows, "cols": cols}
        out.append(o)
    return out

grammar = [{"id": L['id'], "title": L['title'], "icon": L['icon'], "blurb": L['blurb'],
            "beats": beat_list(L['beats'], L['id']), "quiz": quiz(L['quiz'], L['id'])} for L in LESSONS]

# --- word topics ---
topics = []
for T in TOPICS:
    words = []
    for i, w in enumerate(T['words']):
        jp, kana, ro, en = w
        f = form([jp, kana, ro], f"{T['id']}.word{i}")
        f['en'] = en
        words.append(f)
    topics.append({"id": T['id'], "title": T['title'], "icon": T['icon'], "blurb": T['blurb'], "words": words,
                   "sents": [sent(s, f"{T['id']}.sent{i}") for i, s in enumerate(T['sents'])],
                   "rhyme": sent(T['rhyme'], T['id'] + '.rhyme'), "quiz": quiz(T['quiz'], T['id'])})
dialect = {"id": DIALECT['id'], "title": DIALECT['title'], "icon": DIALECT['icon'], "blurb": DIALECT['blurb'],
           "beats": beat_list(DIALECT['beats'], DIALECT['id']), "quiz": quiz(DIALECT['quiz'], DIALECT['id'])}

# --- stories and songs ---
reads = []
for R in STORIES + SONGS:
    reads.append({"id": R['id'], "title": R['title'], "jp": R['jp'], "icon": R['icon'], "kind": R['kind'], "blurb": R['blurb'],
                  "intro": R.get('intro', ''), "lines": [sent(s, f"{R['id']}.line{i}") for i, s in enumerate(R['lines'])],
                  "quiz": quiz(R['quiz'], R['id'])})

ids = [x['id'] for x in grammar + topics + reads] + [dialect['id']]
if len(ids) != len(set(ids)): errors.append('duplicate lesson ids')

if errors:
    print('\n'.join(errors)); sys.exit(1)

data = {"charts": charts, "grammar": grammar, "topics": topics, "dialect": dialect, "reads": reads}
with open(os.path.join(HERE, 'japanese.js'), 'w', encoding='utf-8') as f:
    f.write('/* Generated by grammar/build.py from grammar.py, words.py and stories.py; edit those, not this. */\n')
    f.write('var JP_LEARN = ' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n')
with open(os.path.join(HERE, 'clips.json'), 'w', encoding='utf-8') as f:
    json.dump([{"file": k, "tts": v} for k, v in sorted(clips.items())], f, ensure_ascii=False, indent=1)
nq = sum(len(x['quiz']) for x in grammar + topics + reads) + len(dialect['quiz'])
print(f"OK: {len(grammar)} grammar lessons, {len(charts)} charts, {len(topics)} word topics + dialects, "
      f"{len(reads)} stories/songs, {nq} quiz questions; {len(clips)} voice clips")
