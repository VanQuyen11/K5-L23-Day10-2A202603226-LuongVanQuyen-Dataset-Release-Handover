Release: lab250_95697c6d4612_v2
Parent: lab250_95697c6d4612
Số ảnh: 243
Số nhãn: 1652
Guideline: v1.2 (J01-J04), v1.3 (J05-J10)
QC v1: 21/250 = 8.4%
Kết luận v1: Hold — Tỉ lệ lỗi 8.4% vượt ngưỡng 2%.
Kết luận v2: Release — Đã tách 7 ảnh lỗi detection vào rework_queue.csv; sửa trực tiếp 2 wrong_hash, 2 guideline_mismatch, 1 scene_leak.
Ghi chú: Đã mở kiểm tra ảnh wrong_hash (000000006723, 000000020247) còn nguyên vẹn nên cập nhật sha256 mới; chuẩn hoá split cho scene_214; đồng bộ guideline theo jobs.csv cho 000000002157, 000000003553; ảnh rework giao lại cho người gán/kiểm theo jobs.csv; ảnh chỉ lỗi panoptic ở lại v2 và báo team panoptic: 000000019742 (category_swap), 000000023781 (category_swap), 000000007108 (instance_merge), 000000013291 (instance_merge), 000000016010 (instance_merge), 000000017182 (instance_merge), 000000017627 (instance_merge), 000000013659 (thing_overlap), 000000022192 (thing_overlap).
