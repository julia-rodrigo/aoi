"""Kana -> plain romaji and a loose romaji normaliser, shared by the phrasebook and grammar
checks: two spellings of the same sounds normalise to the same string (macrons, long vowels,
particles written は/へ but said wa/e), so a real typo is what's left to fail."""
import re

# --- kana -> plain romaji, only as strict as the comparison below needs ---
BASE = {
 'あ':'a','い':'i','う':'u','え':'e','お':'o','か':'ka','き':'ki','く':'ku','け':'ke','こ':'ko','が':'ga','ぎ':'gi','ぐ':'gu','げ':'ge','ご':'go',
 'さ':'sa','し':'shi','す':'su','せ':'se','そ':'so','ざ':'za','じ':'ji','ず':'zu','ぜ':'ze','ぞ':'zo','た':'ta','ち':'chi','つ':'tsu','て':'te','と':'to',
 'だ':'da','ぢ':'ji','づ':'zu','で':'de','ど':'do','な':'na','に':'ni','ぬ':'nu','ね':'ne','の':'no','は':'ha','ひ':'hi','ふ':'fu','へ':'he','ほ':'ho',
 'ば':'ba','び':'bi','ぶ':'bu','べ':'be','ぼ':'bo','ぱ':'pa','ぴ':'pi','ぷ':'pu','ぺ':'pe','ぽ':'po','ま':'ma','み':'mi','む':'mu','め':'me','も':'mo',
 'や':'ya','ゆ':'yu','よ':'yo','ら':'ra','り':'ri','る':'ru','れ':'re','ろ':'ro','わ':'wa','を':'o','ん':'n','ぁ':'a','ぃ':'i','ぅ':'u','ぇ':'e','ぉ':'o'}
YOON = {'ゃ':'a','ゅ':'u','ょ':'o'}

def to_hira(s):
    return ''.join(chr(ord(c) - 0x60) if 'ァ' <= c <= 'ヶ' else c for c in s)

def kana_romaji(kana):
    s = to_hira(kana); out = ''; i = 0
    while i < len(s):
        c = s[i]; nxt = s[i + 1] if i + 1 < len(s) else ''
        if c == 'っ':
            out += '*'; i += 1; continue
        if c == 'ー':
            i += 1; continue
        if nxt in YOON and c in BASE:
            b = BASE[c]
            b = b[:-1] if b in ('shi', 'chi', 'ji') else b[:-1] + 'y'
            out += b + YOON[nxt]; i += 2; continue
        if nxt == 'ぇ' and c in ('ち', 'し', 'じ'):
            out += BASE[c][:-1] + 'e'; i += 2; continue
        if nxt in ('ぁ', 'ぃ', 'ぇ', 'ぉ') and c == 'ふ':
            out += 'f' + BASE[nxt]; i += 2; continue
        out += BASE.get(c, ''); i += 1
    return re.sub(r'\*(.)', lambda m: ('t' if m.group(1) == 'c' else m.group(1)) + m.group(1), out)

def norm(r):
    r = r.lower()
    for a, b in (('ā', 'a'), ('ī', 'i'), ('ū', 'u'), ('ē', 'e'), ('ō', 'o')):
        r = r.replace(a, b)
    r = re.sub(r'[^a-z]', '', r)
    r = r.replace('tch', 'cch').replace('ha', 'wa').replace('he', 'e')
    prev = None
    while prev != r:
        prev = r
        r = re.sub(r'(a)a|(i)i|(u)u|(e)e|(o)o', lambda m: next(g for g in m.groups() if g), r).replace('ou', 'o')
    return r

