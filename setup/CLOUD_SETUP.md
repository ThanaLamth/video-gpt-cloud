# Cloud Setup Guide

## VM Hien Tai (Production)

| Thanh phan | Thong so |
|-----------|---------|
| **Ten may** | Windows 10 - i7 - RTX 5060 Ti |
| **GPU** | NVIDIA RTX 5060 Ti — 16GB VRAM |
| **CPU** | Intel Core i7-12700K — 20 cores |
| **RAM** | 28 GB |
| **Storage** | 1600 GB NVMe SSD |
| **OS** | Windows 10 |

**Tieu chuan render voi may nay:**
- `--workers 14` (tu 20 cores)
- 30s video render: ~30-35 giay
- Voice clone (ref toi 30s): 2-3 phut (16GB VRAM, khong can trim ref)
- Toan bo pipeline 1 video: ~8-10 phut
- 6 video: ~50-60 phut

---

## Yeu cau toi thieu (cloud thue)

- GPU: RTX 3080 10GB+ (khuyen nghi RTX 4090 / A10G)
- RAM: 16GB+
- Storage: 50GB+ SSD
- CUDA 12.x

## Provider khuyen nghi

| Provider | GPU | Gia uoc tinh | Ghi chu |
|----------|-----|-------------|---------|
| RunPod | RTX 3090 | ~$0.34/hr | Spot instance, tot cho render |
| Vast.ai | RTX 4090 | ~$0.40/hr | Gia re nhat, on dinh |
| Lambda Labs | A10G | ~$0.75/hr | On dinh hon |
| AWS g4dn.xlarge | T4 16GB | ~$0.53/hr | De deploy, co spot |

---

## Cai dat (Ubuntu cloud)

### 1. Python environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r setup/requirements.txt
```

### 2. Node.js + Puppeteer (cho renderer)
```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
npm install puppeteer
```

### 3. ffmpeg
```bash
sudo apt-get install -y ffmpeg
ffmpeg -version | head -1
```

### 4. VoiceMC (AI Voice Clone)
```bash
git clone <voicemc-repo> ~/Tools/VoiceMC_App
cd ~/Tools/VoiceMC_App
pip install -r requirements.txt
# Download models vao models/hf/
```

> **Luu y VRAM:** May co 16GB VRAM khong can trim ref audio.
> Ref audio toi 30 giay chay on. May < 12GB VRAM nen trim ref xuong 8-10 giay.

### 5. Fonts tieng Viet
```bash
sudo apt-get install -y fonts-noto fonts-noto-cjk
fc-cache -fv
```

---

## Render 1 video

```bash
git clone https://github.com/ThanaLamth/video-gpt-cloud.git
cd video-gpt-cloud
CASE=superpowers-30s

# Render draft (14 workers cho may hien tai)
python scripts/render.py cases/$CASE/*.html \
    --out cases/$CASE/draft.mp4 \
    --width 1080 --height 1920 --dur 30 \
    --workers 14 --crf 22

# Render voice
python cases/$CASE/render_vo.py

# Speed-adjust VO de khop 30s
ffmpeg -i cases/$CASE/vo_raw.wav \
    -filter:a "atempo=1.15" \
    cases/$CASE/vo_fast.wav

# Mix VO + SFX
python cases/$CASE/sfx_score.py
ffmpeg -i cases/$CASE/vo_fast.wav \
       -i cases/$CASE/sfx.wav \
       -filter_complex "[0:a]volume=1.0[vo];[1:a]volume=0.32[sfx];[vo][sfx]amix=inputs=2:duration=longest[out]" \
       -map "[out]" -ar 48000 \
       cases/$CASE/audio_mix.wav

# Final render + burn subs
ffmpeg -i cases/$CASE/draft.mp4 \
    -vf "subtitles=cases/$CASE/subtitles.srt:force_style='FontName=Arial,FontSize=56,Bold=1,Outline=3,MarginV=120'" \
    -c:v libx264 -preset fast -crf 20 -pix_fmt yuv420p -c:a copy \
    cases/$CASE/${CASE}_FINAL.mp4

# Ghep KimQ outro
ffmpeg -y -f concat -safe 0 \
    -i cases/$CASE/concat_list.txt \
    -c:v libx264 -preset fast -crf 20 -pix_fmt yuv420p \
    -c:a aac -b:a 192k -movflags +faststart \
    cases/$CASE/${CASE}_with_outro.mp4
```

---

## Chi phi uoc tinh (cloud)

- 6 video x 10 phut = 60 phut GPU time
- RunPod RTX 3090: $0.34/hr x 1hr = ~$0.34
- Vast.ai RTX 4090: ~$0.40

*Render tat ca 6 video < $0.50 USD*