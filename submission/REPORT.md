# Báo cáo nhóm — Seed 3007

## 1. Số liệu luyện tập
- F1 theo seed:
  - Seed `3007`: rule ≈ `1.0` / cross_check ≈ `0.6` / overall ≈ `0.8` (truy vết `tier_a` `1.0`, `tier_b` `1.0`, `notify` `1.0`; tổng 21 lỗi nộp)
  - Seed `11` (chỉ kiểm tra lỗi luật): rule ≈ `1.0` / overall ≈ `0.8` (13 lỗi luật)
- Số ứng viên trên lô sạch (`--no-faults`, seed `5`, 50 ảnh): `0` lỗi luật, `0` ứng viên; hàng đợi trên seed luyện tập `3007`: `10` ứng viên (`10` ảnh)
- Ngưỡng đã chọn và cách chọn (không dùng `_private`):
  - `duplicate_box`: cùng `class_id`, chênh lệch kích thước `<= 2.5 px` và độ lệch tâm `<= 3.0 px` (loại trừ các cặp box tự nhiên chồng nhau khác kích thước).
  - `instance_merge`: đếm pixel mask thật của segment (`area >= 300`), tìm ít nhất 2 box cùng lớp có `cover_box >= 0.45`, `cover_seg >= 0.15`, `box_iou < 0.35`, và tổng phủ `cov1 + cov2 >= 0.55`. Ban đầu khi chỉ dùng `cov >= 0.18` thì lô sạch bị nổ hơn 20 ứng viên giả; sau khi thêm `cover_box` và `box_iou` thì lô sạch giảm về `0`.
  - `class_swap` / `category_swap`: `iou >= 0.45` và `cover_seg >= 0.45` giữa box và segment khác lớp, không có box cùng lớp nào khác khớp tại segment đó.
  - `bbox_drift`: cặp 1-1 cùng lớp có `0.15 <= iou < 0.72` và `cover_seg < 0.80` (dùng `cover_seg` thay vì `cover_box` vì vật mảnh/chéo như `tie`, `kite` trên lô sạch có `cover_box` thấp dù box bao trọn vật).
  - `missing_box`: segment thing `iscrowd == 0` có `area >= 250` (hoặc `>= 0.2%` diện tích ảnh) nhưng không có box cùng lớp hay khác lớp khớp mạnh.

## 2. Vì sao báo hết ứng viên làm F1 giảm?
COCO vốn có độ lệch tự nhiên giữa detection và panoptic (vật bị che khuất, vật nhỏ, hoặc nhiều vật sát nhau bị gộp ở một nguồn). Nếu báo hết toàn bộ ứng viên thô không qua lọc ngưỡng và xem ảnh, số lượng **FP (báo thừa)** tăng vọt làm `precision = TP / (TP + FP)` giảm mạnh, kéo theo `F1 = 2 * precision * recall / (precision + recall)` giảm mạnh dù `recall` cao. Khi thử lọc chặt trên lô sạch `runs/clean` từ >20 ứng viên xuống `0` ứng viên, hàng đợi trên seed `3007` chỉ còn `10` ảnh để mở xem trực tiếp và phân loại chính xác `class_swap` vs `category_swap` (ví dụ `000000019742` và `000000023781` là `category_swap`, không phải `class_swap`), giữ `10` lỗi confirmed và `1` dòng rejected (`000000013291` `bbox_drift`).

## 3. Quyết định và lineage
- QC v1 (`lab250_95697c6d4612`): `21/250 = 8.4%` (> ngưỡng `2%`) ⇒ Kết luận **Hold**.
- Đã ghi `decision: HOLD` cho `lab250_95697c6d4612` và tạo bản sửa `lab250_95697c6d4612_v2` (243 ảnh, 1652 nhãn; tách 7 ảnh lỗi detection sang `rework_queue.csv`, giữ lại 9 ảnh chỉ lỗi panoptic và 2 ảnh `wrong_hash` đã mở kiểm còn nguyên vẹn, chuẩn hoá split cho `scene_214` và guideline theo `jobs.csv`).
- Khi chạy `lineage.py impact`, training run `R-021` báo `affected=True action=review_or_retrain`: vì việc phát hành lô `v2` không tự động sửa lại trọng số của model đã huấn luyện trên lô `v1` lỗi, nên cần xem lại kết quả đánh giá hoặc huấn luyện lại trên `v2`.

## 4. Hash chứng minh gì, không chứng minh gì?
- **Chứng minh:** tính toàn vẹn ở mức byte của file (file không bị hỏng, cắt xén hay thay đổi ngoài ý muốn so với lúc lập `manifest.csv` / `.sha256`).
- **Không chứng minh:** nội dung nhãn có đúng với vật thể trong ảnh hay không (một file nhãn sai lớp hoặc lệch box vẫn có mã sha256 hợp lệ nếu hash được tính trên chính file sai đó).

## 5. Truy vết
- **`tier_a`:** ảnh thuộc các `scene_id` do team AI báo trong `incoming/ticket.md` (`scene_197`, `scene_309`), nằm trong job dùng guideline cũ (`v1.2`), và có ít nhất 1 box detection lớp `bottle` trong `labels/` (`2` ảnh).
- **`tier_b`:** các ảnh khác cũng thuộc job guideline cũ (`v1.2`) và có box `bottle` nhưng chưa được nêu trong ticket (`4` ảnh).
- **`notify`:** mã người gán và người kiểm của các job chứa ảnh `tier_a` và `tier_b` (`5` người).
- Lấy phiên bản guideline theo `jobs.csv` (thay vì `metadata.json` của từng ảnh) vì `metadata.json` có thể bị lỗi `guideline_mismatch` làm sai lệch phạm vi truy vết.

## 6. Bug hoặc điểm chưa rõ trong lab (nếu có)
Không phát hiện bug trong các script chuẩn của lab.
