#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KimQ Hook Selector — chon hook phu hop cho noi dung video

Usage:
    python hook_selector.py --content-type product_demo
    python hook_selector.py --content-type educational --top 3
    python hook_selector.py --list-types
    python hook_selector.py --list-hooks
    python hook_selector.py --hook CONTRARIAN
    python hook_selector.py --suggest "bai viet ve AI trong doanh nghiep"
"""

import json
import argparse
import os
import sys

HOOK_LIB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hook_library.json")

CATEGORY_ICONS = {
    "cognitive":    "[COG]",
    "visual":       "[VIS]",
    "emotional":    "[EMO]",
    "credibility":  "[CRD]",
    "narrative":    "[NAR]",
    "engagement":   "[ENG]",
    "utility":      "[UTL]",
}

def load_data():
    with open(HOOK_LIB, encoding="utf-8") as f:
        data = json.load(f)
    return data["hooks"], data["content_type_map"]

def get_hook_by_id(hooks, hook_id):
    for h in hooks:
        if h["id"].upper() == hook_id.upper():
            return h
    return None

def rank_hooks_for_type(hooks, ct_map, content_type):
    if content_type not in ct_map:
        return []
    best = ct_map[content_type]["best_hooks"]
    backup = ct_map[content_type]["backup_hooks"]
    result = []
    for hid in best:
        h = get_hook_by_id(hooks, hid)
        if h:
            result.append(("best", h))
    for hid in backup:
        h = get_hook_by_id(hooks, hid)
        if h:
            result.append(("backup", h))
    return result

def divider(char="-", width=62):
    return char * width

def print_hook_card(h, rank_label="", idx=None):
    icon = CATEGORY_ICONS.get(h["category"], "[?]")
    prefix = f"{idx}. " if idx else ""
    tag = f" ({rank_label})" if rank_label else ""
    print(f"\n  {prefix}{icon} {h['id']} — {h['name_vi']}{tag}")
    print(f"     Thoi luong hook: ~{h['hook_duration_s']}s  |  Category: {h['category']}")
    print(f"     {h['description_vi']}")
    print(f"     Template: {h['template_vi'][:120]}")
    if h.get("examples_vi"):
        print(f"     Vi du: \"{h['examples_vi'][0]}\"")

def print_hook_detail(h):
    icon = CATEGORY_ICONS.get(h["category"], "[?]")
    print(f"\n{divider('=')}")
    print(f" {icon} {h['id']} — {h['name_vi']}")
    print(f" Category: {h['category']}   |   Hook duration: ~{h['hook_duration_s']}s")
    print(divider())
    print(f"\n Mo ta:\n   {h['description_vi']}")
    print(f"\n Template script (Tieng Viet):\n   {h['template_vi']}")
    print(f"\n Visual style:\n   {h['visual_style']}")
    print(f"\n SFX style:\n   {h['sfx_style']}")
    print(f"\n Opening frame:\n   {h['opening_frame']}")
    print(f"\n Tot nhat cho:  {', '.join(h['best_for'])}")
    print(f" Backup cho:   {', '.join(h['backup_for'])}")
    if h.get("examples_vi"):
        print(f"\n Vi du (context KimQ):")
        for i, ex in enumerate(h["examples_vi"], 1):
            print(f"   {i}. {ex}")
    print(f"\n{divider('=')}")

def print_beat_sheet_starter(h, content_type):
    """In ra beat sheet starter cho hook duoc chon"""
    dur = h["hook_duration_s"]
    print(f"\n{divider()}")
    print(f" BEAT SHEET STARTER — {h['id']} hook cho '{content_type}'")
    print(divider())
    print(f"\n | t_start - t_end | beat          | motion type  | ghi chu              |")
    print(f" |-----------------|---------------|--------------|----------------------|")
    print(f" | 0.00 - {dur:.2f}s    | HOOK          | {h['visual_style'][:14]:<14}| {h['opening_frame'][:22]} |")
    print(f" | {dur:.2f} - {dur+1.0:.2f}s   | Bridge/carry  | fade / cut           | chuyen sang noi dung |")
    print(f" | {dur+1.0:.2f} - ...s   | [Main content]| theo beat sheet      | dien vao noi dung    |")
    print(f"\n SFX hook: {h['sfx_style']}")
    print(f"\n Tiep theo: viet vo_script.txt mo dau bang hook nay, roi dien main content.")

def suggest_by_keyword(hooks, ct_map, keyword):
    """Goi y content type dua tren tu khoa don gian"""
    kw = keyword.lower()
    scores = {}
    mappings = {
        "ai": ["educational", "trend_opinion", "product_demo"],
        "cong cu": ["product_demo", "how_to"],
        "tool": ["product_demo", "how_to"],
        "ket qua": ["case_study", "social_proof"],
        "khuyen cao": ["educational", "problem_solution"],
        "van de": ["problem_solution"],
        "so sanh": ["comparison"],
        "vs": ["comparison"],
        "cach lam": ["how_to"],
        "huong dan": ["how_to"],
        "thuong hieu": ["brand_story"],
        "cong ty": ["brand_story", "case_study"],
        "thu thuat": ["how_to", "educational"],
        "loi": ["mistake_warning", "problem_solution"],
        "bao cao": ["product_demo", "case_study"],
        "hop": ["problem_solution", "product_demo"],
        "marketing": ["trend_opinion", "educational"],
        "startup": ["brand_story", "case_study"],
    }
    for kw_key, cts in mappings.items():
        if kw_key in kw:
            for ct in cts:
                scores[ct] = scores.get(ct, 0) + 1

    if not scores:
        return None, None

    best_ct = max(scores, key=lambda x: scores[x])
    ranked = rank_hooks_for_type(hooks, ct_map, best_ct)
    return best_ct, ranked

def main():
    parser = argparse.ArgumentParser(
        description="KimQ Hook Selector — chon hook phu hop cho video",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Vi du:
  python hook_selector.py --list-types
  python hook_selector.py --content-type educational
  python hook_selector.py --content-type product_demo --top 5
  python hook_selector.py --hook CONTRARIAN
  python hook_selector.py --suggest "video ve AI trong doanh nghiep"
  python hook_selector.py --content-type case_study --beatsheet
        """
    )
    parser.add_argument("--content-type", "-c", metavar="TYPE",
                        help="Loai noi dung video (dung --list-types de xem danh sach)")
    parser.add_argument("--top", "-n", type=int, default=3,
                        help="So hook goi y (default: 3)")
    parser.add_argument("--list-types", "-T", action="store_true",
                        help="Liet ke tat ca content type")
    parser.add_argument("--list-hooks", "-L", action="store_true",
                        help="Liet ke tat ca hook trong thu vien")
    parser.add_argument("--hook", metavar="ID",
                        help="Xem chi tiet 1 hook theo ID (vi du: CONTRARIAN)")
    parser.add_argument("--suggest", "-s", metavar="KEYWORD",
                        help="Goi y content type dua tren tu khoa mo ta noi dung")
    parser.add_argument("--beatsheet", "-b", action="store_true",
                        help="In beat sheet starter sau khi chon hook (dung voi --content-type)")
    args = parser.parse_args()

    hooks, ct_map = load_data()

    # --list-types
    if args.list_types:
        print(f"\n{divider()}")
        print(f" CONTENT TYPES ({len(ct_map)} loai)")
        print(divider())
        for ct, meta in ct_map.items():
            print(f"  {ct:<22} — {meta['desc']}")
        print(f"\n Cach dung: python hook_selector.py --content-type <TYPE>")
        return

    # --list-hooks
    if args.list_hooks:
        print(f"\n{divider()}")
        print(f" THU VIEN HOOK ({len(hooks)} loai)")
        print(divider())
        by_cat = {}
        for h in hooks:
            by_cat.setdefault(h["category"], []).append(h)
        for cat, hs in sorted(by_cat.items()):
            icon = CATEGORY_ICONS.get(cat, "[?]")
            print(f"\n  {icon} {cat.upper()}")
            for h in hs:
                print(f"    {h['id']:<22} ~{h['hook_duration_s']}s   {h['name_vi']}")
        print(f"\n Xem chi tiet: python hook_selector.py --hook <ID>")
        return

    # --hook DETAIL
    if args.hook:
        h = get_hook_by_id(hooks, args.hook)
        if h:
            print_hook_detail(h)
        else:
            print(f"\n  Khong tim thay hook '{args.hook}'.")
            print(f"  Dung --list-hooks de xem danh sach.")
        return

    # --suggest
    if args.suggest:
        detected_ct, ranked = suggest_by_keyword(hooks, ct_map, args.suggest)
        if detected_ct:
            print(f"\n  Phan tich tu khoa: '{args.suggest}'")
            print(f"  Goi y content type: {detected_ct} — {ct_map[detected_ct]['desc']}")
            top_n = ranked[:args.top]
            print(f"\n{divider()}")
            print(f" TOP {len(top_n)} HOOK GOI Y")
            print(divider())
            for i, (label, h) in enumerate(top_n, 1):
                print_hook_card(h, label, i)
        else:
            print(f"\n  Khong the phan tich tu khoa '{args.suggest}'.")
            print(f"  Vui long dung --content-type de chon truc tiep.")
        return

    # --content-type (main mode)
    if not args.content_type:
        parser.print_help()
        print(f"\n\n{divider()}")
        print(f" CONTENT TYPES HIEN CO")
        print(divider())
        for ct, meta in ct_map.items():
            print(f"  {ct:<22} — {meta['desc']}")
        return

    if args.content_type not in ct_map:
        print(f"\n  Content type '{args.content_type}' khong hop le.")
        print(f"  Dung --list-types de xem danh sach.")
        sys.exit(1)

    ranked = rank_hooks_for_type(hooks, ct_map, args.content_type)
    top_n = ranked[:args.top]

    print(f"\n{divider()}")
    print(f" TOP {len(top_n)} HOOK CHO '{args.content_type}'")
    print(f" ({ct_map[args.content_type]['desc']})")
    print(divider())
    for i, (label, h) in enumerate(top_n, 1):
        print_hook_card(h, label, i)

    if args.beatsheet and top_n:
        best_h = top_n[0][1]
        print_beat_sheet_starter(best_h, args.content_type)
        print(f"\n Xem chi tiet hook nay: python hook_selector.py --hook {best_h['id']}")
    else:
        print(f"\n  Xem chi tiet: python hook_selector.py --hook <ID>")
        print(f"  Beat sheet:   python hook_selector.py --content-type {args.content_type} --beatsheet")
        print(f"  Xem tat ca:   python hook_selector.py --list-hooks")

if __name__ == "__main__":
    main()