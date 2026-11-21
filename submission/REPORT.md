# Báo cáo nhóm <<XX>>

## 1. Số liệu luyện tập
- F1 theo seed (rule / cross_check / overall): <<seed: ... / ... / ...>>
- Số ứng viên trên lô sạch (`--no-faults`): <<...>>; hàng đợi trên seed luyện tập: <<... ảnh>>
- Ngưỡng đã chọn và cách chọn (không dùng `_private`): <<...>>

## 2. Vì sao báo hết ứng viên làm F1 giảm?
<<Trả lời bằng số của nhóm.>>

## 3. Quyết định và lineage
<<QC v1 a/b, kết luận, vì sao R-021 phải xem lại hoặc train lại.>>

## 4. Hash chứng minh gì, không chứng minh gì?
<<>>

## 5. Truy vết
- **`tier_a`:** ảnh trong các cảnh được team AI nêu ở `incoming/ticket.md`, thuộc job dùng guideline cũ (`v1.2`) và có ít nhất một box detection lớp `bottle` (`2` ảnh).
- **`tier_b`:** các ảnh khác cùng dùng guideline cũ và có box `bottle`, nhưng chưa được nêu trong ticket (`4` ảnh).
- **`notify`:** mã người gán và người kiểm của các job chứa ảnh thuộc hai tầng (`5` người).
- Phiên bản guideline được lấy từ `jobs.csv`, không lấy từ `metadata.json` của từng ảnh, vì metadata có thể chính là nơi chứa lỗi `guideline_mismatch` và làm sai phạm vi truy vết.

## 6. Bug hoặc điểm chưa rõ trong lab (nếu có)
<<>>
