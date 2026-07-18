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
