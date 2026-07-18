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
