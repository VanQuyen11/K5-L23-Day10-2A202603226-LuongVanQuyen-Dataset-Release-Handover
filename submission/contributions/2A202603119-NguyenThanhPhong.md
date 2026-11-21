# Nguyễn Thanh Phong — 2A202603119

- GitHub: `Tphong27`
- Phụ trách: P1 — validator lỗi luật.

## Công việc đã thực hiện

- Xây dựng phần kiểm tra lỗi luật trong `validator/validate.py`.
- Kiểm tra hash, file thiếu, class không hợp lệ, box vượt biên, box trùng, guideline không khớp job, scene leak và chồng lấn thing.
- Bảo đảm validator chỉ đọc thư mục delivery được truyền vào và dùng thư viện chuẩn cùng `scripts/pngutil.py`.
- Chạy đánh giá seed `3007` và seed `11`; phần lỗi luật đạt F1 xấp xỉ `1.0` theo báo cáo nhóm.

## File và đầu ra

- `validator/validate.py`: logic kiểm tra lỗi luật và giao diện dòng lệnh.
- `submission/r3007/errors.json`: 21 lỗi cuối của seed `3007`.
- `submission/REPORT.md`: số liệu F1 lỗi luật và kết quả kiểm tra lô sạch.

## Đề ẩn `de_an_12`

- Validator phát hiện 11 lỗi luật trong release `lab250_262995d8ee10`, gồm lỗi file, hash, class, box, guideline, scene và panoptic overlap.
- Kết quả sau khi gộp 14 review đã xác nhận gồm 25 lỗi trong `submission/de_an/errors.json`.
