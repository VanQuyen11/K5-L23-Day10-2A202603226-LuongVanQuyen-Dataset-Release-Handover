# Nguyễn Nhật Minh — 2A202603210

- GitHub: `nminnnnn`
- Phụ trách: P5, P6 — truy vết, bảo mật và đề ẩn.

## Công việc đã thực hiện

- Xây dựng truy vết hai tầng từ ticket, guideline theo job và nhãn `bottle`.
- Xác định `tier_a` gồm 2 ảnh, `tier_b` gồm 4 ảnh và danh sách `notify` gồm 5 mã annotator/reviewer.
- Viết nội dung bảo mật cho tình huống USB, chia sẻ dữ liệu/tài khoản, chatbot bên thứ ba và ảnh có khuôn mặt chưa làm mờ.
- Phối hợp kiểm tra định dạng trace và nội dung bảo mật trong gói bàn giao.

## File và đầu ra

- `validator/handover_trace.py`: hàm tạo trace theo ticket, guideline và job.
- `submission/r3007/trace.json`: kết quả `tier_a`, `tier_b` và `notify`.
- `submission/r3007/security.md`: tài liệu bảo mật ba phần.

## Đề ẩn `de_an_12`

- Truy vết ticket lớp `dog` theo guideline của job cho release `lab250_262995d8ee10`.
- Xác định `tier_a` gồm 2 ảnh, `tier_b` gồm 4 ảnh và `notify` gồm 3 mã người trong `submission/de_an/trace.json`.

## Trạng thái đề ẩn

Đã hoàn thành phần truy vết trong `submission/de_an/trace.json`. Các đầu ra `errors.json`, `candidates.json` và `review_log.csv` thuộc phần validator/review chung của nhóm.
