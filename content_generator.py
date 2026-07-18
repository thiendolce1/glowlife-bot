    # ──────────────────────────────────────────────────────
    # 3. KẾ HOẠCH 7 NGÀY
    # ──────────────────────────────────────────────────────
    async def generate_weekly_plan(self) -> str:
        self._require_model()
        today = datetime.now().strftime("ngày %d tháng %m năm %Y")
        prompt = f"""Lên kế hoạch nội dung TikTok 7 ngày cho kênh {CHANNEL_NAME}.
Niche: {CHANNEL_NICHE} | Bắt đầu từ: {today}
Quy tắc:
- Xen kẽ đều: 🌿 Sức khỏe / ✨ Skincare / 👗 Thời trang
- Ít nhất 2 video dạng series
- 1 video bắt trend đang hot
Format mỗi ngày:
📅 [Thứ X - DD/MM]
🎯 Chủ đề: [niche]
🎬 Tiêu đề: [tiêu đề hấp dẫn]
🎣 Hook: [1 câu mở đầu]
⏰ Đăng lúc: [giờ tốt nhất]
─────────────────
Cuối cùng thêm:
📊 CHIẾN LƯỢC TUẦN: [1 đoạn nhận xét ngắn]"""
        return await self._call_gemini(prompt)
    # ──────────────────────────────────────────────────────
    # 4. 10 Ý TƯỞNG VIDEO
    # ──────────────────────────────────────────────────────
    async def generate_ideas(self) -> str:
        self._require_model()
        prompt = f"""Tạo 10 ý tưởng video TikTok VIRAL cho kênh {CHANNEL_NAME} ({CHANNEL_NICHE}).
Đối tượng: {TARGET_AUDIENCE}
💡 10 Ý TƯỞNG VIDEO HOT TUẦN NÀY
🌿 SỨC KHỎE:
1. [Tiêu đề] → [Lý do viral ngắn]
2. [Tiêu đề] → [Lý do viral ngắn]
3. [Tiêu đề] → [Lý do viral ngắn]
✨ SKINCARE:
4. [Tiêu đề] → [Lý do viral ngắn]
5. [Tiêu đề] → [Lý do viral ngắn]
6. [Tiêu đề] → [Lý do viral ngắn]
👗 THỜI TRANG:
7. [Tiêu đề] → [Lý do viral ngắn]
8. [Tiêu đề] → [Lý do viral ngắn]
9. [Tiêu đề] → [Lý do viral ngắn]
🔥 TREND TUẦN NÀY:
10. [Tiêu đề bắt trend] → [Giải thích trend]
📌 NÊN LÀM TRƯỚC: Video số [X] vì [lý do cụ thể]"""
        return await self._call_gemini(prompt)
