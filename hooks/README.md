# Hook Library — KimQ Video Pipeline

Thu vien 18 hook archetypes cho short-form video KimQ.
Moi hook co template tieng Viet, visual style, SFX guide, va content-type mapping.

---

## Cach dung nhanh

```powershell
$py = "C:\Users\admin\AppData\Local\Programs\Python\Python312\python.exe"
Set-Location "C:\Users\admin\onetake"

# Xem tat ca content type
& $py hooks/hook_selector.py --list-types

# Xem tat ca hook
& $py hooks/hook_selector.py --list-hooks

# Goi y hook cho loai noi dung
& $py hooks/hook_selector.py --content-type educational

# Lay them beat sheet starter
& $py hooks/hook_selector.py --content-type product_demo --beatsheet

# Goi y bang tu khoa mo ta
& $py hooks/hook_selector.py --suggest "AI giam thoi gian hop"

# Xem chi tiet 1 hook
& $py hooks/hook_selector.py --hook PROBLEM_AGITATION
```

---

## 18 Hook Archetypes

### Cognitive (nao phan tich)
| ID | Ten | Thoi luong | Tot nhat cho |
|----|-----|-----------|-------------|
| CONTRARIAN | Phan nghich / Dao lon su that | ~3s | educational, trend_opinion, comparison |
| CURIOSITY_GAP | Khoang trong to mo | ~3s | educational, case_study, trend_opinion |
| QUESTION | Cau hoi truc tiep | ~3s | educational, problem_solution, comparison |
| SECRET_INSIDER | Bi mat / Thong tin noi bo | ~3s | educational, trend_opinion, case_study |

### Visual (mat dung truoc)
| ID | Ten | Thoi luong | Tot nhat cho |
|----|-----|-----------|-------------|
| PATTERN_INTERRUPT | Ngat nhip / Gay soc thi giac | ~2s | product_demo, brand_story, trend_opinion |
| VISUAL_INTERRUPT | Cu hich thi giac thuan tuy | ~2s | product_demo, brand_story, trend_opinion |

### Emotional (tim cam xuc)
| ID | Ten | Thoi luong | Tot nhat cho |
|----|-----|-----------|-------------|
| FEAR_LOSS | So mat mat / FOMO | ~3s | problem_solution, trend_opinion, educational |
| TRANSFORMATION | Bien doi / Truoc - Sau | ~4s | case_study, product_demo, brand_story |
| MISTAKE_WARNING | Canh bao loi / Dung lai | ~2s | educational, problem_solution, how_to |
| PROBLEM_AGITATION | Khuech dai van de | ~5s | problem_solution, educational, comparison |
| EMPATHY | Dong cam / Nhan ra ban than | ~3s | brand_story, problem_solution, educational |

### Credibility (tin tuong ngay)
| ID | Ten | Thoi luong | Tot nhat cho |
|----|-----|-----------|-------------|
| SOCIAL_PROOF | Bang chung xa hoi | ~3s | case_study, product_demo, brand_story |
| BOLD_CLAIM | Tuyen bo tao bao | ~2s | product_demo, brand_story, trend_opinion |
| SHOCK_STAT | Thong ke gay soc | ~3s | educational, trend_opinion, comparison |

### Narrative (ke chuyen)
| ID | Ten | Thoi luong | Tot nhat cho |
|----|-----|-----------|-------------|
| STORY_OPEN | Mo dau bang cau chuyen | ~5s | brand_story, case_study, educational |

### Utility (huu ich ro rang)
| ID | Ten | Thoi luong | Tot nhat cho |
|----|-----|-----------|-------------|
| HOW_TO | Huong dan / Cach lam | ~2s | how_to, product_demo, educational |
| LIST_NUMBER | Danh sach / So diem | ~2s | educational, how_to, comparison |

### Engagement (tuong tac)
| ID | Ten | Thoi luong | Tot nhat cho |
|----|-----|-----------|-------------|
| CHALLENGE | Thu thach / Gamification | ~3s | how_to, educational, product_demo |

---

## Content Type Map

| Content Type | Mo ta | Best Hooks |
|-------------|-------|-----------|
| product_demo | Gioi thieu san pham/tinh nang | PATTERN_INTERRUPT, BOLD_CLAIM, TRANSFORMATION |
| educational | Giai thich khai niem, day kien thuc | CURIOSITY_GAP, SHOCK_STAT, CONTRARIAN |
| trend_opinion | Binh luan xu huong | CONTRARIAN, BOLD_CLAIM, SHOCK_STAT |
| brand_story | Cau chuyen thuong hieu KimQ | STORY_OPEN, EMPATHY, TRANSFORMATION |
| case_study | Chung minh ket qua | TRANSFORMATION, SOCIAL_PROOF, SHOCK_STAT |
| problem_solution | Van de + Giai phap | PROBLEM_AGITATION, FEAR_LOSS, MISTAKE_WARNING |
| comparison | So sanh A vs B | CONTRARIAN, SHOCK_STAT, QUESTION |
| how_to | Huong dan tung buoc | HOW_TO, LIST_NUMBER, CHALLENGE |

---

## Nguyen tac hook trong KimQ video

1. **Hook PHAI xay ra trong 3 giay dau** — neu nguoi xem chua bi cuon, ho da bam next
2. **Hook phai THAT** — khong overstate, noi dung phai backup duoc cam ket trong hook
3. **1 hook per video** — khong ket hop 2 hook kieu vao 1 opening (ro ren, mat focus)
4. **Hook va visual PHAI khop** — CONTRARIAN hook = text strike-through, khong phai logo animation
5. **SFX cung la mot phan cua hook** — am thanh trong 0-3s dinh huong cam xuc ngay lap tuc

---

## Tich hop vao pipeline

Hook selection la **Buoc 0** trong PIPELINE.md — truoc khi viet beat sheet.

Workflow:
```
1. Xac dinh content type cua video
2. Chay hook_selector.py --content-type <type> --beatsheet
3. Chon hook phu hop
4. Copy beat sheet starter vao README.md cua case
5. Viet vo_script.txt mo dau bang hook template
6. Tiep tuc pipeline nhu binh thuong (Buoc 1 tro di)
```

---

*Files: hook_library.json (du lieu), hook_selector.py (CLI tool)*
*Cap nhat lan cuoi: 2026-10-20*