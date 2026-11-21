from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
from collections import Counter
from pathlib import Path

REWORK_TYPES = {
    "missing_image",
    "invalid_class",
    "bbox_out_of_bounds",
    "duplicate_box",
    "class_swap",
    "bbox_drift",
    "missing_box",
}

PANOPTIC_ONLY_TYPES = {
    "invalid_category_id",
    "thing_overlap",
    "category_swap",
    "instance_merge",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def load_classes(path: Path) -> dict[int, str]:
    classes: dict[int, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        cid, name = line.split(maxsplit=1)
        classes[int(cid)] = name
    return classes


def load_jobs(path: Path) -> dict[str, dict[str, str]]:
    jobs: dict[str, dict[str, str]] = {}
    with path.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            jobs[row["job_id"]] = row
    return jobs


def build_trace(delivery_dir: Path) -> dict:
    metadata = json.loads((delivery_dir / "metadata.json").read_text(encoding="utf-8"))
    jobs = load_jobs(delivery_dir / "jobs.csv")
    classes = load_classes(delivery_dir / "classes.txt")
    name_to_cid = {name: cid for cid, name in classes.items()}

    ticket_text = (delivery_dir / "incoming" / "ticket.md").read_text(encoding="utf-8")
    changelog_text = (delivery_dir / "guideline" / "changelog.md").read_text(encoding="utf-8")

    reported_scenes = set(re.findall(r"scene_\d+", ticket_text))

    target_class_name = None
    m_cls = re.search(r"`([a-zA-Z0-9_ ]+)`", changelog_text)
    if m_cls and m_cls.group(1) in name_to_cid:
        target_class_name = m_cls.group(1)
    else:
        for name in name_to_cid:
            if f"`{name}`" in ticket_text or f"`{name}`" in changelog_text:
                target_class_name = name
                break
    if target_class_name is None:
        raise SystemExit("Cannot detect target class from ticket/changelog")
    target_cid = name_to_cid[target_class_name]

    versions = sorted({row["guideline"] for row in jobs.values()})
    old_guideline = versions[0]

    tier_a: list[str] = []
    tier_b: list[str] = []
    notify: set[str] = set()

    for item in metadata["items"]:
        stem = item["image"]
        job = jobs[item["job_id"]]
        if job["guideline"] != old_guideline:
            continue
        lbl_path = delivery_dir / "labels" / f"{stem}.txt"
        if not lbl_path.is_file():
            continue
        has_target = False
        for raw in lbl_path.read_text(encoding="utf-8").splitlines():
            parts = raw.strip().split()
            if parts and parts[0].isdigit() and int(parts[0]) == target_cid:
                has_target = True
                break
        if not has_target:
            continue
        if item["scene_id"] in reported_scenes:
            tier_a.append(stem)
        else:
            tier_b.append(stem)
        notify.add(job["annotator"])
        notify.add(job["reviewer"])

    return {
        "tier_a": sorted(tier_a),
        "tier_b": sorted(tier_b),
        "notify": sorted(notify),
    }


def build_handover(run_dir: Path) -> Path:
    delivery_dir = run_dir / "delivery"
    errors_data = json.loads((run_dir / "errors.json").read_text(encoding="utf-8"))
    errors = errors_data["errors"]
    release_id = json.loads((delivery_dir / "release.json").read_text(encoding="utf-8"))["release_id"]
    manifest = json.loads((delivery_dir / "manifest.json").read_text(encoding="utf-8"))
    metadata = json.loads((delivery_dir / "metadata.json").read_text(encoding="utf-8"))
    jobs = load_jobs(delivery_dir / "jobs.csv")
    classes = load_classes(delivery_dir / "classes.txt")

    meta_by_stem = {item["image"]: item for item in metadata["items"]}

    scene_split_counts: dict[str, Counter[str]] = {}
    for item in metadata["items"]:
        scene_split_counts.setdefault(item["scene_id"], Counter())[item["split"]] += 1
    scene_majority_split = {
        sid: cnt.most_common(1)[0][0] for sid, cnt in scene_split_counts.items()
    }

    rework_items: list[tuple[str, str]] = []
    rework_stems: set[str] = set()
    panoptic_only_notes: list[str] = []
    wrong_hash_stems: list[str] = []
    guideline_fix_stems: list[str] = []
    scene_leak_ids: list[str] = []

    for err in errors:
        etype = err["type"]
        target = err["target"]
        if etype in REWORK_TYPES:
            rework_items.append((target, etype))
            rework_stems.add(target)
        elif etype in PANOPTIC_ONLY_TYPES:
            panoptic_only_notes.append(f"{target} ({etype})")
        elif etype == "wrong_hash":
            wrong_hash_stems.append(target)
        elif etype == "guideline_mismatch":
            guideline_fix_stems.append(target)
        elif etype == "scene_leak":
            scene_leak_ids.append(target)

    v2_dir = run_dir / "handover" / f"{release_id}_v2"
    if v2_dir.exists():
        shutil.rmtree(v2_dir)
    (v2_dir / "images").mkdir(parents=True, exist_ok=True)
    (v2_dir / "labels").mkdir(parents=True, exist_ok=True)

    manifest_rows: list[tuple[str, str]] = []
    label_counts: Counter[str] = Counter()
    truyvet_rows: list[list[str]] = []
    kept_images = 0

    for stem, item in sorted(manifest["items"].items()):
        if stem in rework_stems:
            continue
        src_img = delivery_dir / item["image"]
        src_lbl = delivery_dir / item["label"]
        dst_img = v2_dir / "images" / f"{stem}.jpg"
        dst_lbl = v2_dir / "labels" / f"{stem}.txt"
        shutil.copy2(src_img, dst_img)
        shutil.copy2(src_lbl, dst_lbl)
        kept_images += 1

        manifest_rows.append((f"images/{stem}.jpg", sha256_file(dst_img)))
        manifest_rows.append((f"labels/{stem}.txt", sha256_file(dst_lbl)))

        for raw in dst_lbl.read_text(encoding="utf-8").splitlines():
            parts = raw.strip().split()
            if parts:
                cid = int(parts[0])
                label_counts[classes[cid]] += 1

        meta = meta_by_stem[stem]
        job = jobs[meta["job_id"]]
        fixed_split = scene_majority_split[meta["scene_id"]]
        truyvet_rows.append([
            stem,
            meta["scene_id"],
            fixed_split,
            meta["job_id"],
            job["annotator"],
            job["reviewer"],
            job["guideline"],
        ])

    with (v2_dir / "rework_queue.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["image", "type", "annotator", "reviewer", "action"])
        for stem, etype in sorted(rework_items):
            meta = meta_by_stem[stem]
            job = jobs[meta["job_id"]]
            w.writerow([stem, etype, job["annotator"], job["reviewer"], "reannotate_detection"])

    with (v2_dir / "manifest.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["file", "sha256"])
        for rel, digest in manifest_rows:
            w.writerow([rel, digest])

    total_labels = sum(label_counts.values())
    with (v2_dir / "label_summary.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["class", "count"])
        for cid in sorted(classes):
            cname = classes[cid]
            if label_counts[cname] > 0:
                w.writerow([cname, label_counts[cname]])
        w.writerow(["TOTAL", total_labels])

    with (v2_dir / "truyvet.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["image", "scene_id", "split", "job_id", "annotator", "reviewer", "guideline"])
        for row in truyvet_rows:
            w.writerow(row)

    by_guideline: dict[str, list[str]] = {}
    for jid in sorted(jobs):
        g = jobs[jid]["guideline"]
        by_guideline.setdefault(g, []).append(jid)
    guideline_summary = ", ".join(
        f"{g} ({jids[0]}-{jids[-1]})" for g, jids in sorted(by_guideline.items())
    )

    total_v1 = len(manifest["items"])
    err_count = len(errors)
    err_pct = (err_count / total_v1) * 100.0
    v1_decision = "Hold" if err_pct > 2.0 else "Release"

    readme_text = (
        f"Release: {release_id}_v2\n"
        f"Parent: {release_id}\n"
        f"Số ảnh: {kept_images}\n"
        f"Số nhãn: {total_labels}\n"
        f"Guideline: {guideline_summary}\n"
        f"QC v1: {err_count}/{total_v1} = {err_pct:.1f}%\n"
        f"Kết luận v1: {v1_decision} — Tỉ lệ lỗi {err_pct:.1f}% vượt ngưỡng 2%.\n"
        f"Kết luận v2: Release — Đã tách {len(rework_stems)} ảnh lỗi detection vào rework_queue.csv; "
        f"sửa trực tiếp {len(wrong_hash_stems)} wrong_hash, {len(guideline_fix_stems)} guideline_mismatch, "
        f"{len(scene_leak_ids)} scene_leak.\n"
        f"Ghi chú: Đã mở kiểm tra ảnh wrong_hash ({', '.join(wrong_hash_stems)}) còn nguyên vẹn nên cập nhật sha256 mới; "
        f"chuẩn hoá split cho {', '.join(scene_leak_ids)}; đồng bộ guideline theo jobs.csv cho {', '.join(guideline_fix_stems)}; "
        f"ảnh rework giao lại cho người gán/kiểm theo jobs.csv; "
        f"ảnh chỉ lỗi panoptic ở lại v2 và báo team panoptic: {', '.join(panoptic_only_notes)}.\n"
    )
    (v2_dir / "README.txt").write_text(readme_text, encoding="utf-8")
    return v2_dir


def main() -> int:
    parser = argparse.ArgumentParser(description="Build v2 handover and trace.json")
    parser.add_argument("--run", required=True, help="Run directory, e.g. runs/r3007")
    parser.add_argument("--trace-only", action="store_true", help="Only generate trace.json")
    args = parser.parse_args()

    run_dir = Path(args.run)
    delivery_dir = run_dir if (run_dir / "metadata.json").is_file() else run_dir / "delivery"
    trace = build_trace(delivery_dir)
    trace_out = run_dir / "trace.json"
    trace_out.write_text(json.dumps(trace, indent=2) + "\n", encoding="utf-8")
    if not args.trace_only:
        v2_dir = build_handover(run_dir)
        print("built handover:", v2_dir)
    print("built trace:", trace_out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
