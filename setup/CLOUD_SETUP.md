# Cloud Setup Guide

GPU cloud render cho KimQ video pipeline.

## Yeu cau toi thieu
- GPU: RTX 3080 10GB VRAM tro len (khuyen nghi A10G / RTX 4090)
- RAM: 16GB+
- Storage: 50GB+ SSD
- OS: Ubuntu 22.04 / Windows Server 2022
- CUDA 12.x

## Provider khuyen nghi

| Provider | GPU | Gia uoc tinh | Ghi chu |
|----------|-----|-------------|---------|
| RunPod | RTX 3090 | ~$0.34/hr | Spot instance, tot cho render |
| Vast.ai | RTX 4090 | ~$0.40/hr | Gia re nhat, on dinh |
| Lambda Labs | A10G | ~$0.75/hr | On dinh hon |
| AWS g4dn.xlarge | T4 16GB | ~$0.53/hr | De deploy, co spot |

**Thoi gian render uoc tinh:**
- 30s video (900 frames, 6 workers): 60-90 giay
- Voice clone (8 cau, ref 8s): 4-6 phut
- Toan bo pipeline 1 video: ~15 phut

---

## Cai dat (Ubuntu)

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
# Verify
ffmpeg -version | head -1
```

### 4. VoiceMC (AI Voice Clone)
VoiceMC yeu cau CUDA. Setup:
```bash
# Clone VoiceMC vao ~/Tools/VoiceMC_App
git clone <voicemc-repo> ~/Tools/VoiceMC_App
cd ~/Tools/VoiceMC_App
pip install -r requirements.txt
# Download models vao models/hf/
```

### 5. Fonts (cho tieng Viet render dung)
```bash
sudo apt-get install -y fonts-noto fonts-noto-cjk
fc-cache -fv
```

---

## Render 1 video

```bash
# 1. Clone repo
git clone https://github.com/ThanaLamth/video-gpt-cloud.git
cd video-gpt-cloud

# 2. Chon case (vi du: superpowers-30s)
CASE=superpowers-30s

# 3. Render draft
python scripts/render.py cases/$CASE/*.html \
    --out cases/$CASE/draft.mp4 \
    --width 1080 --height 1920 --dur 30 \
    --workers 6 --crf 22

# 4. Render voice
python cases/$CASE/render_vo.py

# 5. Speed-adjust VO de khop 30s
ffmpeg -i cases/$CASE/vo_raw.wav \
    -filter:a "atempo=1.15" \
    cases/$CASE/vo_fast.wav

# 6. Mix VO + SFX
python cases/$CASE/sfx_score.py
ffmpeg -i cases/$CASE/vo_fast.wav \
       -i cases/$CASE/sfx.wav \
       -filter_complex "[0:a]volume=1.0[vo];[1:a]volume=0.32[sfx];[vo][sfx]amix=inputs=2:duration=longest[out]" \
       -map "[out]" -ar 48000 \
       cases/$CASE/audio_mix.wav

# 7. Final render + burn subs
ffmpeg -i cases/$CASE/draft.mp4 \
    -vf "subtitles=cases/$CASE/subtitles.srt:force_style='FontName=Arial,FontSize=56,Bold=1,Outline=3,MarginV=120'" \
    -c:v libx264 -preset fast -crf 20 -pix_fmt yuv420p -c:a copy \
    cases/$CASE/${CASE}_FINAL.mp4

# 8. Ghep outro
ffmpeg -y -f concat -safe 0 \
    -i cases/$CASE/concat_list.txt \
    -c:v libx264 -preset fast -crf 20 -pix_fmt yuv420p \
    -c:a aac -b:a 192k -movflags +faststart \
    cases/$CASE/${CASE}_with_outro.mp4
```

## Download output
```bash
# Dung scp hoac rsync
scp user@cloud-ip:~/video-gpt-cloud/cases/superpowers-30s/*_FINAL.mp4 ./
```

## Chi phi uoc tinh
- 6 video x 15 phut = 90 phut GPU time
- RunPod RTX 3090: 90 phut x $0.34/hr = ~$0.51
- Vast.ai RTX 4090: ~$0.60

*Render tat ca 6 video < $1 USD*