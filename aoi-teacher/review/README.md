# Fact-check record

`reviewed.json` lists every Teacher lesson and every Quiz set that has been fact-checked,
with the date and a fingerprint of its words at that moment. When a lesson's text, cards or
questions change, its fingerprint changes and it shows up as needing a new check. Lessons that
haven't changed are never checked twice.

```
python3 review/review_status.py          # what still needs checking
python3 review/review_status.py --show   # same, with the text to check
python3 review/review_status.py --mark "fantasy / Yokai of Japan"   # after checking it
```

Covered: every lesson that plays in Teacher (including PPL and General Knowledge parts) and
every Quiz set. Not covered: the interactive players (Piano by Ear, J-pop Chords & Aoi Song),
the phrasebook, and the Japanese wording of Aoi's narration (the facts in it come from the
English lesson lines, which are covered).
