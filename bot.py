"""
GlowLife AI TikTok Bot - bot.py
Compatible with Python 3.10+
"""

import logging
import os
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    filters, ContextTypes
)
from content_generator import TikTokContentGenerator

logging.basicConfig(
    format='%(asctime)s | %(levelname)s | %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
generator = TikTokContentGenerator(GEMINI_API_KEY)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "✨ Chào mừng đến GlowLife AI Bot!\n\n"
        "Tôi sẽ tạo toàn bộ nội dung TikTok cho bạn 🚀\n\n"
        "📋 CÁC LỆNH:\n"
        "🎬 /video skincare — Full video package\n"
        "📱 /caption outfit — Caption + hashtag\n"
        "📅 /tuan — Kế hoạch 7 ngày\n"
        "💡 /idea — 10 ý tưởng hot\n"
        "❓ /help — Hướng dẫn\n\n"
        "⚡ Hoặc chỉ cần nhắn: skincare / outfit / sức khỏe\n\n"
        "GlowLife • Sức khỏe • Da đẹp • Phong cách 🌿"
    )
    await update.message.reply_text(text)


async def video_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "💡 Nhập chủ đề sau lệnh nhé!\n"
            "Ví dụ: /video skincare buổi sáng"
        )
        return
    topic = ' '.join(context.args)
    await _generate_and_send_video(update, topic)


async def caption_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("💡 Ví dụ: /caption outfit công sở")
        return
    topic = ' '.join(context.args)
    msg = await update.message.reply_text(f"⏳ Đang tạo caption cho '{topic}'...")
    try:
        content = await generator.generate_caption_only(topic)
        await msg.delete()
        for chunk in split_message(content):
            await update.message.reply_text(chunk)
    except Exception as e:
        logger.error(f"Caption error: {e}")
        await msg.edit_text(f"❌ Lỗi: {str(e)[:200]}")


async def weekly_plan_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text("📅 Đang lên kế hoạch 7 ngày...")
    try:
        plan = await generator.generate_weekly_plan()
        await msg.delete()
        for chunk in split_message(plan):
            await update.message.reply_text(chunk)
    except Exception as e:
        logger.error(f"Weekly plan error: {e}")
        await msg.edit_text(f"❌ Lỗi: {str(e)[:200]}")


async def ideas_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text("💡 Đang tìm 10 ý tưởng hot...")
    try:
        ideas = await generator.generate_ideas()
        await msg.delete()
        for chunk in split_message(ideas):
            await update.message.reply_text(chunk)
    except Exception as e:
        logger.error(f"Ideas error: {e}")
        await msg.edit_text(f"❌ Lỗi: {str(e)[:200]}")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🤖 HƯỚNG DẪN GLOWLIFE AI BOT\n\n"
        "🎬 TẠO VIDEO ĐẦY ĐỦ:\n"
        "/video skincare da dầu\n"
        "/video outfit đi biển\n"
        "/video review kem chống nắng\n\n"
        "📱 CHỈ LẤY CAPTION:\n"
        "/caption outfit công sở\n\n"
        "📅 KẾ HOẠCH TUẦN:\n"
        "/tuan\n\n"
        "💡 Ý TƯỞNG:\n"
        "/idea\n\n"
        "⚡ NHẮN NHANH:\n"
        "skincare / outfit / mụn / glow / diet\n\n"
        "Powered by Gemini AI ✨"
    )
    await update.message.reply_text(text)


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if text.startswith('/'):
        return
    await _generate_and_send_video(update, text)


async def _generate_and_send_video(update: Update, topic: str):
    msg = await update.message.reply_text(
        f"🎬 Đang tạo nội dung cho '{topic}'...\n"
        "Chờ mình 10-15 giây nhé ⏳"
    )
    try:
        content = await generator.generate_video_content(topic)
        await msg.delete()
        for chunk in split_message(content):
            await update.message.reply_text(chunk)
    except Exception as e:
        logger.error(f"Video generation error: {e}")
        await msg.edit_text(
            f"❌ Có lỗi xảy ra:\n{str(e)[:300]}\n\n"
            "Vui lòng thử lại sau ít phút!"
        )


def split_message(text: str, max_len: int = 4000) -> list:
    if len(text) <= max_len:
        return [text]
    parts = []
    while text:
        if len(text) <= max_len:
            parts.append(text)
            break
        split_at = text.rfind('\n\n', 0, max_len)
        if split_at == -1:
            split_at = text.rfind('\n', 0, max_len)
        if split_at == -1:
            split_at = max_len
        parts.append(text[:split_at])
        text = text[split_at:].strip()
    return parts


def main():
    token = os.environ.get("TELEGRAM_TOKEN")
    if not token:
        raise ValueError("❌ Thiếu TELEGRAM_TOKEN!")

    logger.info(f"🤖 GlowLife Bot khởi động...")
    logger.info(f"🔑 Gemini Key: {'✅ Có' if GEMINI_API_KEY else '❌ Không có'}")

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start",   start))
    app.add_handler(CommandHandler("video",   video_command))
    app.add_handler(CommandHandler("caption", caption_command))
    app.add_handler(CommandHandler("tuan",    weekly_plan_command))
    app.add_handler(CommandHandler("idea",    ideas_command))
    app.add_handler(CommandHandler("help",    help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    logger.info("✅ Bot sẵn sàng nhận tin nhắn!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
