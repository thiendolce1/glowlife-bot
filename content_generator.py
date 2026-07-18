"""
content_generator.py - GlowLife TikTok Bot
Compatible with Python 3.10+ and google-generativeai
"""
import asyncio
import logging
from datetime import datetime
import google.generativeai as genai

logger = logging.getLogger(__name__)

CHANNEL_NAME    = "GlowLife"
CHANNEL_NICHE   = "sức khỏe, chăm sóc da và thời trang hiện đại"
TARGET_AUDIENCE = "người Việt Nam từ 18–35 tuổi, chủ yếu nữ"


class TikTokContentGenerator:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.model = None
        if api_key:
            try:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel("gemini-1.5-flash")
                logger.info("✅ Gemini AI khởi tạo thành công")
            except Exception as e:
                logger.error(f"❌ Lỗi khởi tạo Gemini: {e}")
        else:
            logger.warning("⚠️  Thiếu GEMINI_API_KEY")

    def _require_model(self):
        if not self.model:
            raise RuntimeError(
                "❌ Gemini AI chưa được khởi tạo.\n"
                "Kiểm tra GEMINI_API_KEY trong Railway Variables!"
            )

    async def _call_gemini(self, prompt: str) -> str:
        """Gọi Gemini API bất đồng bộ - compatible với Python 3.10+"""
        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(
            None, lambda: self.model.generate_content(prompt)
        )
        return response.text

    async def generate_video_content(self, topic: str) -> str:
        self._require_model()
        prompt = f"""Bạn là chuyên gia content TikTok hàng đầu Việt Nam, chuyên tạo video viral.
Kênh: {CHANNEL_NAME} | Niche: {CHANNEL_NICHE} | Đối tượng: {TARGET_AUDIENCE}

Tạo FULL CONTENT PACKAGE cho video TikTok về: "{topic}"
Viết bằng tiếng Việt, giọng trẻ trung, gần gũi.

🎬 TIÊU ĐỀ VIDEO (3 lựa chọn)
1. [Tiêu đề có số liệu]
2. [Tiêu đề gây tò mò]
3. [Tiêu đề chạm cảm xúc]

⏱ KỊCH BẢN (60 giây)
[0:00-0:03] HOOK: [câu mở đầu cực mạnh dừng ngón tay scroll]
[0:03-0:12] VẤN ĐỀ: [tạo đồng cảm]
[0:12-0:45] NỘI DUNG:
- Điểm 1: [cụ thể]
- Điểm 2: [cụ thể]
- Điểm 3: [cụ thể]
[0:45-0:55] KẾT: [tóm tắt + teaser]
[0:55-1:00] CTA: [kêu gọi follow/lưu/comment]

📱 CAPTION
[4-5 dòng emoji tự nhiên, kết bằng câu hỏi]

HASHTAG
[20 hashtag, 1 dòng]

🖼 TEXT THUMBNAIL
[2-4 chữ IN HOA gây chú ý]

⏰ GIỜ ĐĂNG TỐT NHẤT
Sáng: [giờ] | Trưa: [giờ] | Tối: [giờ]

🔥 2 MẸO VIRAL
- Mẹo 1: [cụ thể]
- Mẹo 2: [cụ thể]"""
        return await self._call_gemini(prompt)

    async def generate_caption_only(self, topic: str) -> str:
        self._require_model()
        prompt = f"""Tạo caption TikTok cho kênh {CHANNEL_NAME}, chủ đề: "{topic}"

📱 CAPTION [4-5 dòng, emoji, kết bằng câu hỏi kéo comment]

HASHTAG [20 hashtag phù hợp]

⏰ GIỜ ĐĂNG [3 khung giờ cụ thể]

Viết tiếng Việt, tự nhiên như bạn bè nhắn tin."""
        return await self._call_gemini(prompt)

    async def generate_weekly_plan(self) -> str:
        self._require_model()
        today = datetime.now().strftime("ngày %d tháng %m năm %Y")
        prompt = f"""Lên kế hoạch TikTok 7 ngày cho kênh {CHANNEL_NAME} từ {today}.
Xen kẽ: Sức khỏe / Skincare / Thời trang.
Có 2 video series, 1 video trend đang hot.

Mỗi ngày format:
[Thứ X - DD/MM]
- Tiêu đề:
- Hook:
- Giờ đăng:
---"""
        return await self._call_gemini(prompt)

    async def generate_ideas(self) -> str:
        self._require_model()
        prompt = f"""10 ý tưởng TikTok VIRAL cho kênh {CHANNEL_NAME} ({CHANNEL_NICHE}).
Đối tượng: {TARGET_AUDIENCE}

SỨC KHỎE (3 ý tưởng):
SKINCARE (3 ý tưởng):
THỜI TRANG (3 ý tưởng):
TREND TUẦN NÀY (1 ý tưởng):

Mỗi ý: [Tiêu đề] - [Lý do viral ngắn]
Cuối: NÊN LÀM TRƯỚC: Video số [X] vì [lý do]"""
        return await self._call_gemini(prompt)
