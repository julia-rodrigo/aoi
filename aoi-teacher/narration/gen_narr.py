"""Records every clip in clips.json that isn't in ../audio/narr/ yet, in Aoi's Fish Audio voice
(the aoi-fish preset in anime-explainer's kit). Needs network access to api.fish.audio."""
import json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'anime-explainer' / 'studio' / 'tools'))
os.environ.setdefault('FISH_API_KEY', 'set-by-proxy')
from common import KIT, load, write_wav
from speak import fish_tts
preset = load(KIT / 'voices' / 'voices.json')['aoi-fish']
clips = json.loads((HERE / 'clips.json').read_text(encoding='utf-8'))
out = HERE.parent / 'audio' / 'narr'; out.mkdir(exist_ok=True)
tmp = Path(os.environ.get('NARR_TMP', '/tmp/narr_wav')); tmp.mkdir(parents=True, exist_ok=True)
def work(c):
    mp3 = out / c['file']
    if mp3.exists(): return
    for attempt in range(4):
        try:
            pcm, _ = fish_tts(preset, c['tts'], 'ja')
            wav = tmp / c['file'].replace('.mp3', '.wav'); write_wav(wav, pcm)
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(wav), '-ac', '1', '-ar', '24000', '-b:a', '32k', str(mp3)], check=True)
            wav.unlink()
            print('ok', c['file'], c['tts'][:30], flush=True); return
        except Exception as e:
            print('retry', c['file'], e, flush=True)
    print('FAIL', c['file'], flush=True)
with ThreadPoolExecutor(4) as ex: list(ex.map(work, clips))
print('DONE', flush=True)
