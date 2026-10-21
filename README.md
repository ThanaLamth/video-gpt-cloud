# video-gpt-cloud

KimQ short-form video production pipeline — chay tren GPT cloud (GPU instance).

Render 1080x1920 vertical video (TikTok/Reels/Shorts) bang HTML animation + AI voice clone + SFX.

## Cau truc

```
video-gpt-cloud/
├── README.md              # file nay
├── SCENARIOS.md           # 6 kich ban video san sang dung
├── pipeline/
│   └── PIPELINE.md        # quy trinh day du 11 buoc
├── hooks/
│   ├── hook_library.json  # 18 hook archetypes
│   ├── hook_selector.py   # CLI chon hook theo content type
│   └── README.md
├── cases/
│   ├── n8n-30s/           # VIDEO 1 — da render xong (reference)
│   ├── superpowers-30s/   # VIDEO 2 — kich ban san
│   ├── agency-agents-30s/ # VIDEO 3 — kich ban san
│   ├── metagpt-30s/       # VIDEO 4 — kich ban san
│   ├── hyperframes-30s/   # VIDEO 5 — kich ban san
│   ├── langchain-30s/     # VIDEO 6 — kich ban san
│   └── kimc-brand/        # Brand intro/outro KimQ
└── setup/
    ├── CLOUD_SETUP.md     # Huong dan setup GPU instance
    ├── TOOLS.md           # Cac repo cong cu can thiet
    └── requirements.txt   # Python dependencies
```

## Bat dau nhanh

### 1. Chon kich ban
```bash
# Xem 6 kich ban san co
cat SCENARIOS.md

# Chon hook cho kich ban moi
python hooks/hook_selector.py --content-type educational --beatsheet
```

### 2. Setup moi truong (xem setup/CLOUD_SETUP.md)
```bash
pip install -r setup/requirements.txt
```

### 3. Render video
```bash
# Render draft
python scripts/render.py cases/<name>/<name>.html \
    --out cases/<name>/draft.mp4 \
    --width 1080 --height 1920 --dur 30 --workers 6 --crf 22

# Render VO
python cases/<name>/render_vo.py

# Mix + final
# (xem pipeline/PIPELINE.md buoc 7-11)
```

## Cong cu chinh

| Tool | Chuc nang | Repo |
|------|-----------|------|
| onetake | HTML-to-video renderer | github.com/feitangyuan/onetake |
| VoiceMC | AI voice clone (tieng Viet) | local install |
| ffmpeg | Mix audio, burn subs, concat | ffmpeg.org |
| hook_selector | Chon hook theo content type | hooks/hook_selector.py |

## Brand KimQ

- Background: `#080808` | Gold: `#C9A42A` | Gold light: `#E8D488`
- Font: Segoe UI / Arial
- Slogan: Ancient Wisdom · Modern Intelligence
- Contact: contact@kimq.tech | Facebook: KimQ

*VM: RTX 5060 Ti 16GB / i7-12700K 20 cores / 28GB RAM. 30s video ~ 30-35s render time (14 workers).*