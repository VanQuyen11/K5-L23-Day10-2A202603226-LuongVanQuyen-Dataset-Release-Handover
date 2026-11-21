# Dùng AI

| # | Ai dùng | Công cụ | Prompt (tóm tắt) | AI sai ở đâu | Nhóm kiểm lại thế nào |
|---|---|---|---|---|---|
| 1 | Nguyễn Nhật Minh / nhóm | OpenAI Codex | Đọc hồ sơ đóng góp P5–P6, viết công cụ tạo `trace.json` từ ticket, guideline theo job và nhãn detection; hoàn thiện trace seed 3007, trace đề ẩn và tài liệu bảo mật | Phiên bản đầu in thông báo tiếng Việt ra console nên gặp `UnicodeEncodeError` trên PowerShell dùng code page cp1252 | Chạy công cụ trên `runs/r3007/delivery`, so sánh JSON sinh ra với file nộp (khớp hoàn toàn 2 tier A, 4 tier B, 5 notify); đổi thông báo console sang ASCII và chạy lại thành công |
