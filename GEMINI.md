# Antigravity Project Instructions: ORC K2 Robot - Sắc Hoa Tri Ân

## Zero-Bloat Main Thread & Subagent Delegation Architecture (Giảm >90% Token)

1. **Nguyên lý tiết kiệm Token Luồng Chính (Orchestrator Role)**:
   - Luồng chat chính chỉ giữ vai trò Kiến trúc sư & Điều phối viên (Orchestrator).
   - Tuyệt đối không đọc file dài, không xả log terminal lớn, không trực tiếp viết code/script dài ở luồng chính.

2. **Ủy thác 100% việc thực thi cho Subagent Flash (`Model: "flash"`, `TypeName: "self"`)**:
   - Tác vụ nhẹ / đơn luồng: Gọi 1 Subagent `flash` tự đọc, viết, chạy lệnh và kiểm tra trong bộ nhớ riêng.
   - Tác vụ nặng / đa nhánh: Chia Master Plan tối đa 4 nhánh độc lập, kích hoạt 2-4 Subagents `flash` chạy song song.

3. **Báo cáo tinh gọn (Compact Return)**:
   - Subagent chỉ trả về bản tóm tắt xác thực và liên kết file `file:///...`.
   - Luồng chính phản hồi người dùng ngắn gọn, chính xác.

