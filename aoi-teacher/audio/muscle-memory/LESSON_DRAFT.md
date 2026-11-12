# Teacher lesson draft: "Muscle Memory" (how it really works + practical tips)

Status: content + real Japanese audio DONE for all 7 beats. **Not wired into `index.html`** —
that file is being worked on by another agent right now. This file has everything the next
engineering pass needs to add a `MUSCLE_MEMORY_LESSON` array (or similarly-named export) in the
same shape as `TUTOR_LESSON` / the Japanese Pronunciation lesson: `{ text, pose, eyes, audio,
visual }` per beat.

Audio: `aoi-teacher/audio/muscle-memory/beat1.mp3` ... `beat7.mp3` (7 of 7 planned beats; mono
44.1kHz MPEG-1 Layer III, same format as the other committed Teacher-mode clips, generated via
Fish Audio `aoi-fish` preset through `anime-explainer/studio/tools/speak.py::fish_tts`, same
pipeline as the Claude Code tutorial, Japanese Pronunciation lesson, and Aoi's Day clips).

Convention (matches the rest of the app): **Japanese voice narration + English on-screen
captions**, meaning-matched not word-for-word, Aoi's voice: warm, clear, a little playful.
`pose`/`eyes` values below are taken from the actual set already used in `TUTOR_LESSON`
(`present_r`, `present_l`, `point_r`, `point_l`, `null` / `eyes_happy`, `eyes_think`, `null`) so
they're guaranteed to exist in the sprite sheet already — no new poses needed.

---

## Fact-check notes (so this is checkable — not just "trust me")

This topic got extra scrutiny per the request ("fact check your answers over and over") because
it becomes permanent recorded audio. Checked against multiple independent sources via live web
search (not training-data recall alone) immediately before writing beat text:

1. **"Muscle memory" is actually two distinct, both-real phenomena — the central factual risk in
   this topic, and the one most explainer content oversimplifies or conflates:**
   - **(a) Neural/motor-learning "muscle memory"** (procedural memory): skill practice is encoded
     and refined in the nervous system — cerebellum, basal ganglia, and motor cortex circuits —
     not in muscle tissue. Repetition makes the movement require less conscious effort over time.
     Supported by: Shmuelof & Krakauer, *Neuron* (2011) review comparing cerebellar/basal
     ganglia/motor-cortex circuits across species, on basal ganglia's role in early acquisition of
     novel sequential actions; a 2021 *Frontiers in Neurology* review describing the same three
     regions as the circuit for motor learning; Wikipedia's "Muscle memory" article, which frames
     it as a form of procedural memory. I deliberately did **not** assert a specific myelination
     mechanism in the audio script — a web search for that turned up only a commercial fitness
     site's claim, not a peer-reviewed source, so "myelination" was left out of the beat text as
     unverified at the mechanistic-detail level, even though the broader "pathways in the nervous
     system get refined with repetition" framing is well supported.
   - **(b) Cellular/muscle-fiber "muscle memory"** (myonuclear domain theory): resistance training
     adds extra nuclei (myonuclei) to muscle fibers as they grow; a meaningful portion of those
     extra nuclei are retained even after a period of detraining, and this is hypothesized to let
     the fiber regrow to its earlier size faster on retraining. Supported by: Snijders et al.,
     *Acta Physiologica* (2020) review ("The concept of skeletal muscle memory: Evidence from
     animal and human studies", PubMed 32175681) — strong animal evidence, human evidence present
     but thinner (small sample sizes); an older-men retraining study showing myonuclei +13% and
     type II fiber hypertrophy +29% after a retraining period, consistent with the domain theory;
     a rat study (PMC6138296) showing retained myonuclei through detraining. The review explicitly
     flags that the human mechanism remains "largely ambiguous" — so the beat text says "training
     science shows" / "it's hypothesized that," not "it's proven," language chosen to match that
     caveat.
   - Both beats make clear these are **two different things that happen to share one nickname** —
     this was the single highest-priority thing to get right, since conflating "your brain learned
     it" with "your muscle literally remembers" (or vice-versa) is the most common factual error
     in casual explanations of this topic.

2. **Spaced/distributed practice beats cramming for motor-skill retention (general tip, beat 6):**
   Lee & Genovese (1988, a frequently-cited review) found massed practice depresses motor
   learning/retention relative to distributed practice; distributed-practice-over-massed-practice
   effects also replicated in discrete motor tasks like golf putting. Caveat found during
   checking: the effect can reverse for some continuous vs. discrete task types in at least one
   study, so the beat text keeps this general ("spread practice out") rather than citing a precise
   ratio or schedule.

3. **Sleep's role in motor memory consolidation (beat 6):** Multiple reviews (Nusbaum et al.;
   a 2017 *Neuroscience & Biobehavioral Reviews* paper, "Sleeping on the motor engram") support
   sleep helping consolidate and protect a newly learned motor skill from interference. Important
   caveat found during checking: this is an actively debated area — Pan & Rickard (2015,
   *Psychological Bulletin*) is a more skeptical/critical review questioning how much true
   "consolidation" (vs. simple fatigue recovery) sleep provides for motor tasks. Because of that
   live debate, the beat text keeps the sleep claim soft ("helps... lock the movement in") rather
   than making a strong, settled-science claim.

4. **Detraining timeline / how fast lost size and strength come back (beat 7):** Checked across
   multiple sources: short breaks (roughly 2–3 weeks) cause little real loss — much of the
   early visible "shrinkage" is water/glycogen, not tissue loss; losses become more measurable
   after ~3–4+ weeks off; retraining recovers lost strength and size markedly faster than it took
   to build originally (Halonen et al. 2024 in older men: strength restored within ~8 weeks and
   muscle cross-sectional area within ~12 weeks of retraining, after detraining — much faster than
   the original training time). Because exact weeks vary a lot by study population (age, prior
   training level) and most precise figures come from small or older-adult-specific studies, the
   beat text deliberately avoids citing a specific number of weeks and instead makes only the
   well-supported qualitative claim: a short break costs little, and rebuilding is faster than the
   original build.

5. **General "it's not literally in the muscle" framing (beat 1/intro):** Corroborated by
   ScienceAlert's explainer (citing procedural memory and prefrontal/fronto-parietal brain regions
   for the skill side) and multiple other secondary science-press sources; no contradicting source
   found. Used only as framing/hook language, not as a citation of a specific brain-region claim in
   beat 1 itself (the brain-region claim proper is reserved for beat 2, where it's sourced per #1).

Sources checked (via live search just before drafting, not relied on from training memory alone):
Shmuelof & Krakauer 2011 *Neuron*; 2021 *Frontiers in Neurology* review; Wikipedia "Muscle memory";
Snijders et al. 2020 *Acta Physiologica* (PubMed 32175681); PMC6138296 (rat myonuclear retention);
older-men retraining/myonuclei study; Lee & Genovese 1988 distributed-vs-massed-practice review;
golf-putting distributed-practice study; Nusbaum et al. (sleep/skill consolidation); 2017
*Neuroscience & Biobehavioral Reviews* "Sleeping on the motor engram"; Pan & Rickard 2015
*Psychological Bulletin* (critical counterpoint on sleep); Halonen et al. 2024 detraining/retraining
study; ScienceAlert "muscles have their own kind of memory" explainer. Anywhere the underlying
research was mixed, thin, or still debated, the beat text was written to make the **weaker, safely
qualitative** claim rather than the strongest-sounding one.

---

## Beats

### Beat 1 — Hook: one nickname, two real things
- **text:** "Hi again! Ever notice how a skill you haven't touched in years can suddenly feel easy again? That's what people call 'muscle memory' — and it's actually two completely different things happening at once."
- **pose:** `present_r` **eyes:** `eyes_happy`
- **visual spec:** Boxless, centered. Two labeled icons side by side, roughly equal size, no border/panel around either (matches the app's boxless redesign): a brain icon labeled "Nervous system" on the left, a muscle/bicep or muscle-fiber icon labeled "Muscle fibers" on the right, with a small "+" glyph floating between them. A short line underneath both, spanning the width: "One nickname. Two real things." New icons needed: brain, muscle/bicep (not in the existing `MOCK_ICONS` set, which only has cloud/laptop/phone/repo/send/check/pin/globe — add `brain` and `muscle` SVGs in the same stroke style).
- **audio:** `audio/muscle-memory/beat1.mp3`
- **Japanese narration (meaning-matched, not literal):** 「やっほー!何年もやってなかったことなのに、急にまたできるようになった経験ない?それが『マッスルメモリー』、筋肉の記憶って呼ばれるものなんだけど、実は全然違う2つの仕組みが同時に起きてるんだよ。」

### Beat 2 — The nervous-system piece
- **text:** "The first piece lives entirely in your brain and nervous system. Every time you repeat a movement, circuits in your cerebellum, basal ganglia, and motor cortex get better at driving it — so it takes less conscious effort each time."
- **pose:** `point_r` **eyes:** `null`
- **visual spec:** Boxless. Single central brain icon with three short labeled lines/nodes pointing out from it: "Cerebellum," "Basal ganglia," "Motor cortex" — arranged like simple labeled callouts around the brain shape, no panel/border. A small repeating-arrow icon (↻) near the brain with the label "Repeat → sharper circuit" underneath to show the repetition-strengthens-it idea.
- **audio:** `audio/muscle-memory/beat2.mp3`
- **Japanese narration:** 「ひとつ目は、完全に脳と神経の中で起きてること。同じ動きを繰り返すたびに、小脳と基底核、運動皮質が回路をどんどん磨いていくの。だから繰り返すほど、意識しなくても動けるようになるんだ。」

### Beat 3 — Why it feels "automatic"
- **text:** "That's why a well-practiced skill starts to feel automatic — it shifts from effortful, conscious thinking to fast, practiced instinct. Scientists call this procedural memory, and it barely fades, even after years away."
- **pose:** `present_l` **eyes:** `eyes_think`
- **visual spec:** Boxless, two-stage horizontal progression (left to right, connected by a simple arrow, no box around either stage): stage 1 icon = a head with a thought-bubble/gear icon, label "Thinking hard"; stage 2 icon = a lightning bolt or checkmark, label "Second nature." A faint dashed line continuing to the right fading out, labeled "...years later" to show durability.
- **audio:** `audio/muscle-memory/beat3.mp3`
- **Japanese narration:** 「練習した動きが自然にできるようになるのはそのせい。頭で必死に考える状態から、体がすっと覚えている状態に変わるの。これは手続き記憶って呼ばれていて、何年経ってもほとんど消えないんだよ。」

### Beat 4 — The muscle-cell piece
- **text:** "The second piece is real too, and it happens right inside your muscle fibers. When a fiber grows, it gains extra nuclei — and training science shows a lot of those nuclei stick around even after you stop training."
- **pose:** `point_l` **eyes:** `null`
- **visual spec:** Boxless. A single elongated muscle-fiber shape (simple rounded bar icon) with several small dot icons inside it labeled "nuclei," a couple of the dots styled slightly brighter/highlighted with a tiny "stays behind" label pointing at them, to visually show "most leave when the fiber shrinks, but some of these particular ones remain."
- **audio:** `audio/muscle-memory/beat4.mp3`
- **Japanese narration:** 「ふたつ目は、ちゃんと筋肉の中で本当に起きていること。筋肉を大きくすると、筋繊維の中に核が増えるの。トレーニングをやめても、その核の多くは残ったままなんだって。」

### Beat 5 — Why retraining is faster
- **text:** "That's the myonuclear domain theory: those leftover nuclei act like a head start, helping the fiber grow back toward its old size faster the second time around. It's a real biological memory — just not a thinking one."
- **pose:** `present_r` **eyes:** `eyes_happy`
- **visual spec:** Boxless. Two short horizontal bars stacked vertically, no border/panel: top bar labeled "Building it the first time" (longer bar, slower fill animation implied by label "takes longer"), bottom bar labeled "Rebuilding after a break" (shorter bar reaching the same height, label "comes back faster"). Simple up-arrow icon next to both reaching the same dotted "target size" line.
- **audio:** `audio/muscle-memory/beat5.mp3`
- **Japanese narration:** 「これが『ミオニュークリア・ドメイン説』。残った核が次のスタートダッシュになって、前と同じ大きさまで、前よりずっと早く戻れるってわけ。考える記憶じゃないけど、これもれっきとした体の記憶なんだよ。」

### Beat 6 — Practical tips
- **text:** "Want to build either kind of memory faster? Spread your practice out instead of cramming it into one long session, and don't skip sleep — both seem to help your nervous system lock the movement in."
- **pose:** `present_l` **eyes:** `eyes_think`
- **visual spec:** Boxless. Two labeled icons side by side: a simple calendar icon with a few evenly-spaced dots across it, labeled "Spread practice out" (vs. implied cramming, shown by contrast rather than a second negative icon, to keep it simple); a crescent-moon icon labeled "Sleep on it." No borders/panels around either icon, consistent with the rest of the app's boxless icon+label pattern (e.g. how the tutorial lesson's checklist beat lays out icon+label pairs without a bordered mockup).
- **audio:** `audio/muscle-memory/beat6.mp3`
- **Japanese narration:** 「どっちの記憶も早く育てたいなら、練習は一気にやらずに、ちょっとずつ日を分けてやるのがコツ。それと、しっかり寝ること!どっちも神経が動きを定着させるのを助けてくれるの。」

### Beat 7 — Recap / reassurance (outro)
- **text:** "And if life gets in the way? A short break costs you very little, and most of what you rebuild comes back faster than it took to learn the first time. So don't worry about starting over — you're not starting from zero!"
- **pose:** `present_r` **eyes:** `eyes_happy`
- **visual spec:** Boxless. A simple "pause" icon (⏸) on the left labeled "A few weeks off," connected by an arrow to a small rising bar/sparkline icon on the right labeled "Comes back fast" — echoing the recap-checklist style of the existing tutorial lesson's final beats (simple icon + short label pairs, no bordered panel), ending on an encouraging note to match Aoi's sign-off tone in the other lessons' final beats.
- **audio:** `audio/muscle-memory/beat7.mp3`
- **Japanese narration:** 「しばらく休んじゃっても大丈夫。数週間くらいならほとんど失わないし、取り戻すときも最初に覚えたときより早く戻ってくるから。また始めるときも、ゼロからじゃないんだよ!」

---

## Implementation notes for the next pass

- Follow the exact `TUTOR_LESSON` shape: `{ text, pose, eyes, audio, visual }` per beat, in an
  array (suggest `MUSCLE_MEMORY_LESSON` or similar, following whatever naming convention the
  Japanese Pronunciation lesson's array uses by the time this lands).
- New icons needed in whatever icon set backs the Teacher mode's boxless visuals: `brain`,
  `muscle`/bicep, a simple `calendar` with dots, a `moon`/sleep glyph, and a `pause` glyph. None of
  these exist in the current `MOCK_ICONS` object (`cloud`, `laptop`, `phone`, `repo`, `send`,
  `check`, `pin`, `globe`) — they'll need matching stroke-style SVGs added alongside those.
- Audio files are already real, final Japanese narration (not placeholders) — do not regenerate
  unless the English text or Japanese script changes.
- Fish Audio credit was already low (~$0.84 before this batch, from other concurrent audio work
  spending the same pool) — all 7 beats were generated successfully with no errors, and the
  wallet endpoint read the same cached balance before and after this batch's generation (it may
  not reflect usage in real time), so treat that figure as approximate, not a live meter.
