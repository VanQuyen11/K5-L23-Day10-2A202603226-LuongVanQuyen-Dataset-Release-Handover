# Huỳnh Ngọc Gia Hân — 2A202603128

- GitHub: `suadaunanh`
- Phụ trách: P4 — bàn giao dataset v2.

## Công việc đã thực hiện

- Xây dựng quy trình tạo lô v2 từ kết quả QC v1.
- Tách 7 ảnh có lỗi detection sang `rework_queue.csv` và giữ 243 ảnh trong bản phát hành v2.
- Cập nhật hai hash sai sau khi kiểm tra ảnh còn nguyên vẹn, đồng bộ hai guideline mismatch theo `jobs.csv` và chuẩn hóa split của `scene_214`.
- Tạo manifest, checksum, thống kê nhãn, truy vết và README bàn giao.
- Đóng gói lô `lab250_95697c6d4612_v2` với 243 ảnh, 243 file nhãn, 486 dòng manifest và 1652 nhãn.

## File và đầu ra

- `validator/handover_trace.py`: logic sinh lô v2 và các tài liệu bàn giao.
- `submission/r3007/handover/lab250_95697c6d4612_v2/`: dataset v2 và tài liệu đi kèm.
- `submission/r3007/handover/lab250_95697c6d4612_v2.sha256`: checksum gói bàn giao.
