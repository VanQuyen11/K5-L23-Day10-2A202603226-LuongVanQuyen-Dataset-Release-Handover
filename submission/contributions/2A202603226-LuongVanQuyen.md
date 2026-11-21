# Lương Văn Quyến — 2A202603226

- GitHub: `VanQuyen11`
- Phụ trách: P0, P3 — leader, quyết định Release/Hold và lineage.

## Công việc đã thực hiện

- Chuẩn bị repository, thống nhất seed `3007` và phân công 5 thành viên.
- Tổng hợp 21 lỗi trên 250 ảnh, tính tỷ lệ lỗi `8.4%` và đưa ra quyết định Hold cho lô v1 vì vượt ngưỡng `2%`.
- Ghi chuỗi lineage gồm inject, training run `R-021`, quyết định HOLD và release v2 có liên kết parent.
- Đánh giá tác động: model `R-021` đã train trên v1 cần review hoặc retrain sau khi phát hành v2.
- Tổng hợp báo cáo cuối và theo dõi tiến độ các pha.

## File và đầu ra

- `submission/TEAM.md`: danh sách, seed và phân công thành viên.
- `submission/lineage.jsonl`: bốn sự kiện lineage của v1 và v2.
- `submission/REPORT.md`: quyết định Hold, giải thích lineage và tác động tới training run.
- `submission/prompts.md`: nhật ký sử dụng và kiểm chứng đầu ra AI của nhóm.
