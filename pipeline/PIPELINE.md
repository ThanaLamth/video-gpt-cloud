# OneTake Video Pipeline — KimQ

Quy trinh day du de tao mot video short-form theo chuan **onetake**.
Ghi lai tu case `mirofish-30s`. Canvas: **1080x1920 px**, 30 fps, dinh dang xuat MP4.

---

## Tong quan cac buoc

```
0. Hook Selection (chon hook truoc khi viet beat sheet)
1. Brief & Beat Sheet
2. Scene HTML (animation)
3. SFX Score
4. Render draft
5. VO Script + Voice Clone
6. Word-align VO
7. Audio Mix (VO + SFX)
8. Generate SRT subtitles
9. SRT -> ASS
10. QC & Fix (cursor, typo)
11. Final Render + Burn subs
```

---

## Buoc 0 - Hook Selection (`hooks/hook_selector.py`)

**Chay truoc khi viet beat sheet.** Hook quyet dinh 3-5 giay dau video — neu hook sai, nguoi xem bam next.

```powershell
Set-Location "C:\Users\admin\onetake"
$py = "C:\Users\admin\AppData\Local\Programs\Python\Python312\python.exe"

# Goi y hook + beat sheet starter
& $py hooks/hook_selector.py --content-type <type> --beatsheet

# Cac type: product_demo | educational | trend_opinion | brand_story
#           case_study   | problem_solution | comparison | how_to

# Goi y bang tu khoa
& $py hooks/hook_selector.py --suggest "mo ta noi dung"

# Xem chi tiet 1 hook
& $py hooks/hook_selector.py --hook <HOOK_ID>

# Xem tat ca hook (18 loai)
& $py hooks/hook_selector.py --list-hooks
```

**Output buoc nay:** Hook ID da chon, beat sheet starter (paste vao README.md), opening line cho vo_script.

**5 nguyen tac:**
1. Hook PHAI xay ra trong 3 giay dau
2. 1 hook per video — ghep 2 kieu = mat focus
3. Hook va visual PHAI khop (CONTRARIAN = strike-through text, khong phai logo)
4. SFX la mot phan cua hook — am thanh 0-3s dat tone ngay lap tuc
5. Hook phai that — noi dung video backup duoc cam ket trong hook

Thu vien day du: `hooks/README.md` | Du lieu: `hooks/hook_library.json`

---

## Buoc 1 - Brief & Beat Sheet (`README.md`)

Viet `cases/<name>/README.md` voi:

- **Concept** - 1 cau mo ta spine cua video
- **Hook** - Hook ID tu Buoc 0, template script, visual plan
- **Carry chain** - danh sach cac transition "carry" giua scene
- **Beat sheet** - bang timestamp: `| t_start - t_end | beat name | length | motion type | carry |`
- **Kiem tra CV** - do lech chuan do dai cac shot ~ trung binh; muc tieu CV ~ 0.25 (tranh deu don dieu)
- **Still frames** — 33% tong thoi luong

> Cong cu tham khao: `motion.js` catalogue `references/motion-library.md`

---

## Buoc 2 - Scene HTML (`<name>.html`)

File duy nhat chua toan bo animation, chay offline, khong import module.

Cau truc bat buoc:
```html
<script src="../../scripts/motion.js"></script>

<script>
// 1. Khai bao timeline constants (copy sang sfx_score.py)
const W_T = [0.18, 0.58, 1.05];
const AG_IN = 1.55; // ...

// 2. __seek(t) - ham render 1 frame tai thoi diem t
function __seek(t) { /* ... */ }

// 3. Cursor knots (HAND type)
// Format: {t, x, y} - toa do pixel tren canvas 1080x1920
// Quy tac can chinh cursor:
//   - Run button center: x=274, y=892
//   - Bar tracks: y = 675 + i*134  (i = 0..4)
//   - Kiem tra bang cach inspect element trong browser truoc khi hardcode

// 4. __motion export (dung boi render.py)
window.__motion = { seek: __seek, dur: 30, w: 1080, h: 1920 };
</script>
```

**Rule cursor quan trong:**
Truoc khi hardcode toa do HAND knots, mo HTML trong browser > DevTools > inspect element > lay `getBoundingClientRect()` cua target element. Dung uoc chung.

---

## Buoc 3 - SFX Score (`sfx_score.py` -> `sfx.wav`)

```python
# Import tu scripts/sfx_palette.py
from sfx_palette import Score, air, glass, wood, sub, bubble, wobble, pan_of

s = Score(dur=30.0, T60=1.1)   # T60 = reverb tail
p = s.place

# Dat SFX theo timeline (dung constants tu buoc 2)
p(glass(523, 0.7, 0.6), W_T[0], 0.14, 0.0, 0.45)
# ...
s.write("sfx.wav")   # 48 kHz, peak -8 dBFS
```

Chay:
```powershell
$py = "C:\Users\admin\AppData\Local\Programs\Python\Python312\python.exe"
& $py cases/<name>/sfx_score.py
```

**SFX cua hook (Buoc 0):** Am thanh 0-3s phai khop voi hook type da chon.
Xem `hooks/hook_library.json` -> truong `sfx_style` cua hook da chon.

---

## Buoc 4 - Render draft (`draft.mp4`)

```powershell
$py = "C:\Users\admin\AppData\Local\Programs\Python\Python312\python.exe"
& $py scripts/render.py cases/<name>/<name>.html `
    --out cases/<name>/draft.mp4 `
    --width 1080 --height 1920 --dur 30 --workers 6 --crf 22
```

> Render ~158s cho 900 frames voi 6 workers.
> Kiem tra output: mo `draft.mp4`, xem cursor co tro dung element khong, animation flow khop beat sheet khong.

---

## Buoc 5 - VO Script + Voice Clone

### 5a. Chuan bi reference voice
```
ref_voice.wav        clip giong mau (15-60s)
ref_transcript.txt   transcript chinh xac cua clip tren (UTF-8, khong dau viet tat)
ref_ascii.txt        ban ASCII fallback (dung khi engine can)
```

Source giong mau hien tai:
`C:\Users\admin\Downloads\Repo GitHub 116k stars giup AI coding len tam cao moi.mp3`

### 5b. Viet VO script (`vo_script.txt`)
- Viet bang **tieng Viet thuan** (khong tron Anh-Viet)
- Khong dung thuat ngu chuyen nganh — ai cung hieu duoc
- Dung cum noi giua cac cau (vi du: "Va ket qua la...", "Khong dung o day...")
- Tranh lap tu (dac biet cac cum nhu "rat ro", "chinh xac")
- Do dai: khop voi thoi luong video (30s ~ 100-130 chu tieng Viet)
- **Dong mo dau phai la hook** tu Buoc 0 — copy template tu hook_selector

### 5c. Render voice (`render_vo.py` -> `vo_raw.wav`)
```python
# render_vo.py
import sys, os
sys.path.insert(0, r"C:\Users\admin\Tools\VoiceMC_App")
os.environ["HF_HOME"]              = r"C:\Users\admin\Tools\VoiceMC_App\models\hf"
os.environ["HF_HUB_OFFLINE"]       = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"
import engine

engine.render(
    raw_text = open("vo_script.txt", encoding="utf-8").read(),
    ref_wav  = "ref_voice.wav",
    ref_text = open("ref_transcript.txt", encoding="utf-8").read(),
    out_path = "vo_raw.wav",
    speed    = 1.08,       # tang nhe de khop timing video
    pause_scale = 0.60,    # rut ngan khoang lang giua cau
    qc       = False,
    log      = print,
)
```

Chay qua **VoiceMC runtime** (khong dung system Python):
```powershell
$voicePy = "C:\Users\admin\Tools\VoiceMC_App\runtime\Scripts\python.exe"
& $voicePy cases/<name>/render_vo.py
```

**Loi thuong gap voi VoiceMC:**
- Tieng Viet co dau phai luu file UTF-8 (khong phai UTF-8-BOM)
- Neu co am la dau cau -> them 0.1s silence padding bang ffmpeg truoc khi su dung
- Engine doc text theo sentence boundary — dung "." va "," dung cho

---

## Buoc 6 - Word-align VO

Su dung Montreal Forced Aligner (MFA) hoac WhisperX de lay word-level timestamps:

```python
# align_vo.py - su dung whisperx
import whisperx, json

model = whisperx.load_model("base", device="cpu")
result = model.transcribe("vo_raw.wav", language="vi")
model_a, metadata = whisperx.load_align_model("vi", device="cpu")
result = whisperx.align(result["segments"], model_a, metadata, "vo_raw.wav", device="cpu")

with open("vo_aligned.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
```

Output `vo_aligned.json` chua word timestamps de tao SRT chinh xac.

---

## Buoc 7 - Audio Mix (VO + SFX)

```python
# mix_audio.py
from pydub import AudioSegment

sfx  = AudioSegment.from_wav("sfx.wav")
vo   = AudioSegment.from_wav("vo_raw.wav")

# VO level: -3 dBFS, SFX ducked -12 dB khi VO active
sfx_ducked = sfx - 12
mix = sfx_ducked.overlay(vo)
mix.export("audio_mix.wav", format="wav")
```

**Kiem tra:** Nghe mix.wav — VO phai ro rang, SFX o nen.

---

## Buoc 8 - Generate SRT subtitles

```python
# make_srt.py
# Doc vo_aligned.json -> xuat subtitles.srt
# Rule: max 2 dong / subtitle, max 35 ky tu / dong
# Sync voi vo timestamps tu whisperx
```

---

## Buoc 9 - SRT -> ASS

```python
# make_ass.py
# Chuyen .srt sang .ass voi KimQ style:
# - Font: "Segoe UI", size 52px
# - Position: center, bottom (y = 1700/1920)
# - Outline: 2px den
# - Bold: yes
# Kiem tra sub size: khong qua 30% chieu cao man hinh
```

---

## Buoc 10 - QC & Fix

```python
# fix_cursor_subs.py
# Kiem tra:
# 1. Cursor knots co tro dung element khong (so sanh voi getBoundingClientRect)
# 2. Spelling: ten brand (KimQ, MiroFish) - khong phai KimC, MiroFix
# 3. Subtitle: khong qua lon, khong che noi dung chinh
# 4. Tieng Viet co dau hien dung trong sub
```

---

## Buoc 11 - Final Render + Burn Subs

```powershell
$py = "C:\Users\admin\AppData\Local\Programs\Python\Python312\python.exe"
$ff = "C:\Users\admin\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffmpeg.exe"

# 1. Final render voi audio mix
& $py scripts/render.py cases/<name>/<name>.html `
    --out cases/<name>/<name>_nosub.mp4 `
    --width 1080 --height 1920 --dur 30 --workers 6 --crf 22 `
    --sfx cases/<name>/audio_mix.wav

# 2. Burn subtitles
& $ff -y -i cases/<name>/<name>_nosub.mp4 `
    -vf "ass=cases/<name>/subtitles.ass" `
    -c:v libx264 -preset fast -crf 20 -pix_fmt yuv420p `
    -c:a copy `
    cases/<name>/<name>_FINAL.mp4
```

---

## Brand Pipeline (Intro / Outro KimQ)

Xem chi tiet day du o `SKILL.md` hoac `cases/kimc-brand/`.
Tom tat quy trinh nhanh:

### A. Logo rules

| File | Dung cho |
|------|---------|
| `logo.png` | **File nay duy nhat** — wordmark + icon |
| `logo 300x300.png` | Icon badge — **khong dung song song voi wordmark** |

**Rule:** Chi show **1 logo asset** moi frame.

### B. Tao HTML - `gen.py`

```powershell
$py = "C:\Users\admin\AppData\Local\Programs\Python\Python312\python.exe"
& $py cases/kimc-brand/gen.py
```

`gen.py` doc `logo.png` -> xoa nen trang bang PIL threshold (> 238) -> base64 embed -> ghi HTML.

**Layout chuan (1080x1920):**
```
LCY  = 840   # logo center Y
SLY  = 990   # slogan baseline
SEY  = 1013  # separator line Y
CTAY = 1080  # CTA text Y (outro only)
```

**Intro beat sheet (3s):**
| t | beat |
|---|------|
| 0.00-0.48s | seed dot + ambient glow + particles converge |
| 0.40-1.28s | wordmark popIn (spring backOut) |
| 1.28-2.00s | slogan maskRise |
| 1.95-2.38s | separator grow |
| 2.72-3.00s | hold glow |

**Outro beat sheet (6s):**
| t | beat |
|---|------|
| 0.00-0.55s | full logo fadeIn |
| 0.55-1.42s | shimmer sweep LR |
| 1.42-2.12s | CTA text maskRise |
| 2.06-2.55s | company name popIn |
| 2.55-4.30s | contact typeOn (cps=22) |
| 4.30-4.80s | hold - de thoi gian doc |
| 4.80-6.00s | fade to black |

### C. SFX

**Intro (`sfx_intro.py`):**
- Ascending crystal triad (C5E5G5B5) tai seed dot, mark, wordmark, slogan
- Air whoosh luc mark pop
- Sub warmth (body pulse)

**Outro (`sfx_outro.py`):**
- Sub pad entry + shimmer glass tones
- Typing clicks sync voi typeOn:

```python
# Typing SFX — phai khop hoan toan voi HTML
TEXT    = 'Facebook: KimQ  \u2022  contact@kimq.tech'
T_START = 2.55   # khop typeOn start time trong HTML
CPS     = 22     # khop cps= trong HTML

for i, ch in enumerate(TEXT):
    if ch in (' ', '\u2022'):
        continue           # khoang trong + bullet = im lang
    t_ch = T_START + i / CPS
    freq = random.randint(162, 218)
    gain = 0.10 + random.random() * 0.06
    p(wood(freq, 0.07), t_ch, gain, 0.0, 0.03)
```

> **Rule:** Khi doi text, cps, hoac t_start trong HTML -> cap nhat sfx_outro.py cho khop.

```powershell
$py = "C:\Users\admin\AppData\Local\Programs\Python\Python312\python.exe"
& $py cases/kimc-brand/sfx_intro.py
& $py cases/kimc-brand/sfx_outro.py
```

### D. Render intro + outro (tuan tu, khong song song)

> !! **Khong render 2 file song song trong cung case dir** — ca 2 dung chung `_frames/`, intro xong se xoa truoc khi outro viet xong.

```powershell
Set-Location "C:\Users\admin\onetake"
$env:PYTHONUTF8 = "1"
$py = "C:\Users\admin\AppData\Local\Programs\Python\Python312\python.exe"

# Intro 3s
& $py scripts/render.py cases/kimc-brand/kimc-intro.html `
    --out cases/kimc-brand/draft_intro.mp4 `
    --width 1080 --height 1920 --dur 3 --workers 6 --crf 22 `
    --sfx cases/kimc-brand/sfx_intro.wav

# Outro 6s (sau khi intro xong)
& $py scripts/render.py cases/kimc-brand/kimc-outro.html `
    --out cases/kimc-brand/draft_outro.mp4 `
    --width 1080 --height 1920 --dur 6 --workers 6 --crf 22 `
    --sfx cases/kimc-brand/sfx_outro.wav
```

### E. Ghep outro vao video chinh

**Buoc 1 - Tao concat list (ASCII, khong BOM):**
```powershell
$list = "file 'C:/path/to/main_video_FINAL.mp4'`nfile 'C:/path/to/draft_outro.mp4'"
[System.IO.File]::WriteAllText("C:\Users\admin\onetake\concat_list.txt", $list, [System.Text.Encoding]::ASCII)
```

**Buoc 2 - Re-encode khi ghep (timestamp sach, faststart):**
```powershell
$ff = "C:\Users\admin\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffmpeg.exe"

& $ff -y -f concat -safe 0 `
    -i "C:\Users\admin\onetake\concat_list.txt" `
    -c:v libx264 -preset fast -crf 22 -pix_fmt yuv420p `
    -c:a aac -b:a 192k `
    -movflags +faststart `
    "output_FINAL.mp4"
```

> **Dung `-c copy` se nhanh hon nhung gay Non-monotonic DTS warning.**
> **Re-encode (`libx264`) mat ~5s nhung timestamp hoan toan sach — dung cai nay khi upload.**

### F. Checklist khi update brand info

Khi doi text trong outro (ten, email, social handle):

1. Patch `kimc-outro.html` — doi string trong `typeOn()` va `fillText()`
2. Patch `sfx_outro.py` — doi `TEXT`, giu nguyen `T_START` va `CPS`
3. Re-render sfx: `& $py sfx_outro.py`
4. Re-render outro: lenh render o muc D
5. Ghep lai: lenh concat o muc E

### G. Cau truc thu muc brand case

```
cases/kimc-brand/
+-- gen.py              # Generator — chay de tao lai HTML tu logo moi
+-- kimc-intro.html     # Intro animation (3s)
+-- kimc-outro.html     # Outro animation (6s)
+-- sfx_intro.py        # SFX intro
+-- sfx_outro.py        # SFX outro (co typing sync)
+-- sfx_intro.wav       # SFX render
+-- sfx_outro.wav       # SFX render
+-- draft_intro.mp4     # Output intro *
+-- draft_outro.mp4     # Output outro *
```

---

## Loi thuong gap

| Loi | Nguyen nhan | Fix |
|-----|-------------|-----|
| Logo xuat hien 2 lan | Dung ca mark + wordmark | Chi dung `logo.png` |
| `FileNotFoundError _frames/` | 2 render song song xoa nhau | Render tuan tu |
| Non-monotonic DTS khi concat | `-c copy` | Dung `-c:v libx264` |
| Typing SFX khong khop | TEXT/CPS/T_START khong dong bo | Copy tu HTML sang sfx |
| White bg logo tren dark bg | PNG chua transparent | PIL threshold > 238 |
| Am la dau cau trong VO | VoiceMC bat dau segment moi | Them 0.1s silence padding |
| Sub qua lon | Font size qua cao | Kiem tra max 30% chieu cao |
| Cursor point sai vi tri | Hardcode khong dung getBoundingClientRect | Inspect element truoc |
| VO doc "MiroFix" thay vi "MiroFish" | Spelling sai trong script | QC spelling trong vo_script.txt |

---

*Pipeline ghi lai tu case `mirofish-30s` va `kimc-brand`. Cap nhat lan cuoi: 2026-10-20.*