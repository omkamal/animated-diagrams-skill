# Voice-over sync — SRT-driven animation beats

Mode of operation: the user supplies a narration script with timestamps (SRT
or VTT) — optionally with an audio file and/or a diagram idea. **Each cue
drives exactly one animation beat**: the element/camera action for cue N
fires AT `cue.start` (never before), holds the focus while its narration
plays (until `cue.end`), and the next part appears only at the next cue's
start. The narration owns the clock.

## Workflow

### 1. Parse the script

```bash
python3 $SKILL_DIR/scripts/srt_to_cues.py narration.srt
# prints a cue table (start/end/dur/text) + a ready `const CUES = [...]` snippet
# --json cues.json for machine use; --js for the snippet alone
```

### 2. Plan the beat map (before writing any code)

Make a table mapping every cue to ONE beat — element(s) + action type:

| cue | narration says | beat (element + action) |
|---|---|---|
| 1 | "Users hit our CDN first…" | entrance `#node-browser` + `#node-cdn`, draw `#edge-browser-cdn` |
| 2 | "the load balancer spreads…" | entrance `#node-alb`, camera `camFit(#node-alb)` |
| 3 | "Lambda writes every order…" | pulse rides to `#node-db`, emphasis glow |

Action types: **entrance** (element pops/draws in), **focus** (camFit +
others dim to 0.35), **flow** (pulse rides an edge), **emphasis** (glow/scale
on an existing element). If the user gave only an SRT (no diagram), derive
the scene FROM the cue texts — one node/visual per noun-phrase cluster.

### 3. Author the timeline as beats

Paste the CUES constant into the inline script and build every beat from it —
**never hardcode cue times**:

```js
const CUES = [{"i":1,"start":0.0,"end":3.2},{"i":2,"start":3.6,"end":7.1}, …];
const LEAD = 0.15;   // animation starts a touch after the voice begins

// beat 1 — entrance
tl.from(["#node-browser", "#node-cdn"], { opacity: 0, y: 26, stagger: 0.15,
  duration: 0.5, ease: "back.out(1.4)" }, CUES[0].start + LEAD)
  .from("#edge-browser-cdn", { drawSVG: "0%", duration: 0.6 }, CUES[0].start + 0.9);
// …then HOLD: nothing else until CUES[1].start.

// beat 2 — entrance + focus, held for the whole cue
tl.from("#node-alb", { opacity: 0, y: 26, duration: 0.5 }, CUES[1].start + LEAD);
camFit(tl, "#node-alb", { at: CUES[1].start + 0.5, dur: 0.9 });
// release the focus only when the cue's narration is done:
camHome(tl, { at: CUES[1].end, dur: 0.8 });
```

Hard rules:

- Beat N's first tween starts at `CUES[N-1].start` (+ small LEAD ≤ 0.2s) —
  **never earlier**.
- All of beat N's motion fits inside its cue: last tween ends by
  `CUES[N-1].end`; a camera/dim release may run in the gap to the next cue.
- A focus (camera zoom, dim) HOLDS until `cue.end` — releasing early
  orphans the narration; releasing late steps on the next beat.
- Long cue, short action? Add bounded "alive" motion (pulse repeats, dotted
  drift) that ends by `cue.end` — don't freeze for 6 s of narration.
- `data-duration` = last cue end + 1–2s outro hold (`srt_to_cues.py` prints
  the minimum). Total timeline must match.

### 4. Embed the narration audio (if provided)

Place the file in the project (e.g. `audio/narration.mp3`) and add inside
`#root` (after the `</svg>`):

```html
<audio id="narration" class="clip" src="./audio/narration.mp3"
       data-start="0" data-duration="<total>" data-track-index="2"></audio>
```

**`id` is mandatory** — without it the renderer silently drops the audio
(verified; lint catches it). The rendered MP4 then carries the voice-over
(h264 + aac). `data-volume="0.9"` to trim level. No audio file? Render
silent video timed to the SRT — it will sync when the user muxes later.

If the user has text but NO timestamps: generate the narration first with a
TTS skill (omnivoice-tts / kokoro-tts produce audio; WhisperX or the TTS's
own timestamps give the SRT), then run this workflow.

### 5. Verify against the cues (mandatory)

Snapshot at every beat boundary — the moment BEFORE a cue starts must NOT
show that cue's content:

```bash
# one frame just before each cue start, one mid-cue:
node $SKILL_DIR/scripts/render.mjs --project . --output renders/x.mp4 \
  --at "$(python3 -c "
import json; c=json.load(open('cues.json'))
ts=[]
for q in c: ts += [max(0,q['start']-0.1), (q['start']+q['end'])/2]
print(','.join(f'{t:.2f}' for t in ts))")" --probe
```

Read the contact sheet: frame `start−0.1` of cue N must show beats 1…N−1
only; frame mid-cue N shows beat N active/focused. Fix and re-render until
every boundary is clean. Then probe must show the audio stream
(`audio: aac`) when narration was embedded.
