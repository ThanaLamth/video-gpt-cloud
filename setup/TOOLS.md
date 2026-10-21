# Cong cu can thiet (Repos)

Cac repo cong cu duoc dung trong KimQ video pipeline.

## Core Rendering

### onetake — HTML to Video
- **Repo:** https://github.com/feitangyuan/onetake
- **Chuc nang:** Render HTML/canvas animation thanh MP4. Chinh la engine cua pipeline nay.
- **Cai dat:** `git clone https://github.com/feitangyuan/onetake && pip install -r requirements.txt`
- **Dung cho:** Buoc 4 (render draft) va Buoc 11 (final render)

### remotion — React to Video (alternative)
- **Repo:** https://github.com/remotion-dev/remotion (65k stars)
- **Chuc nang:** Dung React de tao video. Phu hop neu team quen React hon canvas.
- **Khi nao dung:** Neu can component-based animation phuc tap hon
- **Cai dat:** `npx create-video@latest`

### hyperframes — HTML to Video (Built for Agents)
- **Repo:** https://github.com/heygen-com/hyperframes (67k stars)
- **Chuc nang:** Cung concept voi onetake, optimize cho AI agent tu dong tao video.
- **Khi nao dung:** Khi muon AI tu viet HTML va tu render

---

## Audio & Voice

### VoiceMC — AI Voice Clone
- **Repo:** Private / local install tai `C:\Users\admin\Tools\VoiceMC_App`
- **Chuc nang:** Clone giong nguoi that tu file WAV reference. Support tieng Viet.
- **Dung cho:** Buoc 5 (render VO)
- **Yeu cau:** CUDA GPU, ref audio 3-10 giay

### ffmpeg
- **Trang chu:** https://ffmpeg.org
- **Chuc nang:** Mix audio, burn subtitles, concat video, speed adjust
- **Cai dat:** `sudo apt-get install ffmpeg` hoac winget/brew

---

## AI Content Frameworks (repo dung lam chu de video)

### n8n — Workflow Automation
- **Repo:** https://github.com/n8n-io/n8n (208k stars)
- **Mo ta:** Fair-code workflow automation platform voi native AI

### obra/superpowers — Agentic Skills Framework
- **Repo:** https://github.com/obra/superpowers (302k stars)
- **Mo ta:** Framework dinh nghia skills cho AI agent

### msitarzewski/agency-agents — Complete AI Agency
- **Repo:** https://github.com/msitarzewski/agency-agents (161k stars)
- **Mo ta:** 46 AI agents san sang: dev, marketing, legal, finance...

### FoundationAgents/MetaGPT — Multi-Agent Framework
- **Repo:** https://github.com/FoundationAgents/MetaGPT (70k stars)
- **Mo ta:** "First AI Software Company" — CEO, engineer, QA deu la AI

### langchain-ai/langchain — Agent Engineering Platform
- **Repo:** https://github.com/langchain-ai/langchain (148k stars)
- **Mo ta:** Nen tang xay dung AI agent voi memory, tools, chains

---

## Brand & Design Tools

### motion.js (built-in onetake)
- **Path:** `cases/mirofish-30s/motion.js` (copy vao moi case)
- **Chuc nang:** Animation primitives: popIn, maskRise, letterDrop, spring, flyThrough

### Hook Selector (built-in repo nay)
- **Path:** `hooks/hook_selector.py`
- **Chuc nang:** Chon hook phu hop theo content type
- **Dung:** `python hooks/hook_selector.py --content-type educational --beatsheet`