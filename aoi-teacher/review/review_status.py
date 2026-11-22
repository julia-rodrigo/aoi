"""Which lessons and quizzes still need a fact-check?

reviewed.json records every Teacher lesson and Quiz set that has been fact-checked, with a
fingerprint (hash) of its content at the time. A lesson needs checking again only if it is new,
or if its words have changed since it was checked.

  python3 review/review_status.py            dump the app's current content, list what needs review
  python3 review/review_status.py --show     ...and print the text of each one, ready to check
  python3 review/review_status.py --mark "fantasy / Yokai of Japan" "quiz: fan / Yokai of Japan"
                                             record those as checked today (use after checking them)
  python3 review/review_status.py --mark-all-pending   record everything listed as checked

The dump (dump_content.cjs, needs Node + Playwright) writes content_now.json; --no-dump reuses it.
"""
import datetime, json, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEDGER = HERE / 'reviewed.json'

def load():
    now = json.loads((HERE / 'content_now.json').read_text(encoding='utf-8'))
    items = {}
    for k, v in now['lessons'].items():
        items[k] = {'kind': 'lesson', 'hash': v['hash'], 'what': v}
    for k, v in now['quizzes'].items():
        items[k] = {'kind': 'quiz', 'hash': v['hash'], 'what': v}
    return items

def main(argv):
    if '--no-dump' not in argv:
        subprocess.run(['node', str(HERE / 'dump_content.cjs')], check=True)
    items = load()
    ledger = json.loads(LEDGER.read_text(encoding='utf-8')) if LEDGER.exists() else {}
    new = [k for k in items if k not in ledger]
    changed = [k for k in items if k in ledger and ledger[k]['hash'] != items[k]['hash']]
    gone = [k for k in ledger if k not in items]
    today = datetime.date.today().isoformat()

    def mark(keys):
        for k in keys:
            if k not in items:
                sys.exit(f'not found in the app: {k!r}')
            ledger[k] = {'kind': items[k]['kind'], 'hash': items[k]['hash'], 'checked': today}
        LEDGER.write_text(json.dumps(dict(sorted(ledger.items())), ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
        print(f'recorded {len(keys)} as checked on {today}')

    if '--mark-all-pending' in argv:
        return mark(new + changed)
    if '--mark' in argv:
        return mark(argv[argv.index('--mark') + 1:])

    ok = len(items) - len(new) - len(changed)
    print(f'{ok} of {len(items)} lessons and quiz sets are checked and unchanged.')
    for title, keys in (('NEW, never checked', new), ('CHANGED since checked', changed)):
        if keys:
            print(f'\n{title} ({len(keys)}):')
            for k in keys:
                print('  ' + k)
                if '--show' in argv:
                    w = items[k]['what']
                    for t in w.get('text', []) + w.get('visualText', []):
                        print('      ' + t)
                    for q in w.get('questions', []):
                        print('      Q ' + json.dumps(q, ensure_ascii=False))
    if gone:
        print(f'\nNo longer in the app ({len(gone)}): ' + ', '.join(gone))
    if not new and not changed:
        print('Nothing needs checking.')

if __name__ == '__main__':
    main(sys.argv[1:])
