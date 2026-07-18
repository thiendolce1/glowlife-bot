"""
content_generator.py - GlowLife TikTok Bot
Dùng google-genai SDK (tương thích với API key AQ. mới nhất)
"""
import asyncio
import logging
from datetime import datetime
from google import genai

logger = logging.getLogger(__name__)

CHANNEL_NAME    = "GlowLife"
CHANNEL_NICHE   = "sức khỏe, chăm sóc da và thời trang hiện đại"
TARGET_AUDIENCE = "người Việt Nam từ 18-35 tuổi, chủ yếu nữ"
MODEL           = "gemini-1.5-flash-8b"


class TikTokContentGenerator:
    def __init__(self, api_key: str):
        self.client = None
        if api_key:
            try:
                self.client = genai.Client(api_key=api_key)
                logger.info("✅ Gemini AI khởi tạo thành công")
            except Exception as e:
                logger.error(f"❌ Lỗi khởi tạo Gemini: {e}")
        else:
            logger.warning("⚠️  Thiếu GEMINI_API_KEY")

    def _require_client(self):
        if not self.client:
            raise RuntimeError(
                "❌ Gemini AI chưa sẵn sàng.\n"
                "Kiểm tra GEMINI_API_KEY trong Railway Variables!"
            )

    async def _call_gemini(self, prompt: str) -> str:
        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.client.models.generate_content(
                model=MODEL,
                contents=prompt
            )
        )
        return response.text

    async def generate_video_content(self, topic: str) -> str:
        self._require_client()
        prompt = f"""Bạn là chuyên gia content TikTok hàng đầu Việt Nam, chuyên tạo video viral.
Kênh: {CHANNEL_NAME} | Niche: {CHANNEL_NICHE} | Đối tượng: {TARGET_AUDIENCE}

Tạo FULL CONTENT PACKAGE cho video TikTok về: "{topic}"
Viết bằng tiếng Việt, giọng trẻ trung, gần gũi, tự nhiên.

🎬 TIÊU ĐỀ VIDEO (3 lựa chọn)
1. [Tiêu đề có số liệu gây chú ý]
2. [Tiêu đề câu hỏi gây tò mò]
3. [Tiêu đề chạm cảm xúc]

⏱ KỊCH BẢN 60 GIÂY
[0:00-0:03] HOOK: [câu mở đầu cực mạnh, dừng ngay ngón tay scroll]
[0:03-0:12] VẤN ĐỀ: [tạo đồng cảm với người xem]
[0:12-0:45] NỘI DUNG CHÍNH:
- Điểm 1: [cụ thể, áp dụng được ngay]
- Điểm 2: [cụ thể, áp dụng được ngay]
- Điểm 3: [cụ thể, áp dụng được ngay]
[0:45-0:55] KẾT: [tóm tắt + teaser phần tiếp]
[0:55-1:00] CTA: [kêu gọi follow/lưu/comment tự nhiên]

📱 CAPTION
[4-5 dòng, có emoji, kết bằng câu hỏi kéo comment]

HASHTAG
[20 hashtag 1 dòng, mix trending và niche]

🖼 TEXT THUMBNAIL
[2-4 chữ IN HOA, ngắn, gây tò mò]

⏰ GIỜ ĐĂNG TỐT NHẤT
Sáng: [giờ] | Trưa: [giờ] | Tối: [giờ]

🔥 2 MẸO VIRAL
- Mẹo 1: [cụ thể về cách quay/dựng]
- Mẹo 2: [cụ thể về tương tác 1h đầu]"""
        return await self._call_gemini(prompt)

    async def generate_caption_only(self, topic: str) -> str:
        self._require_client()
        prompt = f"""Tạo caption TikTok cho kênh {CHANNEL_NAME}, chủ đề: "{topic}"
Đối tượng: {TARGET_AUDIENCE}

📱 CAPTION [4-5 dòng, emoji, kết bằng câu hỏi]

HASHTAG [20 hashtag phù hợp, 1 dòng]

⏰ GIỜ ĐĂNG [3 khung giờ tốt nhất]

Viết tiếng Việt tự nhiên như bạn bè nhắn tin."""
        return await self._call_gemini(prompt)

    async def generate_weekly_plan(self) -> str:
        self._require_client()
        today = datetime.now().strftime("ngày %d tháng %m năm %Y")
        prompt = f"""Lên kế hoạch nội dung TikTok 7 ngày cho kênh {CHANNEL_NAME} từ {today}.
Xen kẽ đều: Sức khỏe / Skincare / Thời trang.
Có 2 video dạng series, 1 video bắt trend đang hot.

Format mỗi ngày:
[Thứ X - DD/MM]
Tiêu đề: [tiêu đề hấp dẫn]
Hook: [1 câu mở đầu]
Giờ đăng: [giờ tốt nhất]
---

Cuối: CHIẾN LƯỢC TUẦN: [1 đoạn nhận xét ngắn và mục tiêu follow]"""
        return await self._call_gemini(prompt)

    async def generate_ideas(self) -> str:
        self._require_client()
        prompt = f"""Tạo 10 ý tưởng video TikTok VIRAL cho kênh {CHANNEL_NAME}.
Niche: {CHANNEL_NICHE} | Đối tượng: {TARGET_AUDIENCE}

SỨC KHỎE (3 ý tưởng):
1. [Tiêu đề] - [Lý do viral ngắn]
2. [Tiêu đề] - [Lý do viral ngắn]
3. [Tiêu đề] - [Lý do viral ngắn]

SKINCARE (3 ý tưởng):
4. [Tiêu đề] - [Lý do viral ngắn]
5. [Tiêu đề] - [Lý do viral ngắn]
6. [Tiêu đề] - [Lý do viral ngắn]

THỜI TRANG (3 ý tưởng):
7. [Tiêu đề] - [Lý do viral ngắn]
8. [Tiêu đề] - [Lý do viral ngắn]
9. [Tiêu đề] - [Lý do viral ngắn]

TREND TUẦN NÀY (1 ý tưởng):
10. [Tiêu đề bắt trend] - [Giải thích tại sao hot]

NÊN LÀM TRƯỚC: Video số [X] vì [lý do cụ thể]"""
        return await self._call_gemini(prompt)
