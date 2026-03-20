import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from yt_dlp import YoutubeDL

# -------------------------------------------------
# Logging
# -------------------------------------------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# -------------------------------------------------
# Configuration
# -------------------------------------------------
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError(
        "❗️ Please set the TELEGRAM_BOT_TOKEN environment variable (obtain it from @BotFather)."
    )

# -------------------------------------------------
# Download helper (yt‑dlp)
# -------------------------------------------------
def download_tiktok(url: str) -> str:
    """Download a TikTok video and return the saved file path."""
    ydl_opts = {
        "outtmpl": "downloaded_%(id)s.%(ext)s",
        "format": "mp4",
        "quiet": True,
        "no_warnings": True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return os.path.abspath(ydl.prepare_filename(info))

# -------------------------------------------------
# /start command
# -------------------------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 สวัสดีครับ! ส่งลิงก์ TikTok มาให้ผม แล้วผมจะดาวน์โหลดวิดีโอให้คุณ 🎥"
    )

# -------------------------------------------------
# Message handler – expects a TikTok URL
# -------------------------------------------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if "tiktok.com" not in text.lower():
        await update.message.reply_text("⚠️ กรุณาส่งลิงก์ TikTok เท่านั้น")
        return

    status_msg = await update.message.reply_text("🔄 กำลังดาวน์โหลดวิดีโอ... ⏳")
    try:
        video_path = download_tiktok(text)
        with open(video_path, "rb") as video_file:
            await context.bot.send_video(
                chat_id=update.effective_chat.id,
                video=video_file,
                caption="✅ ดาวน์โหลดสำเร็จ",
            )
        await status_msg.edit_text("✅ เสร็จสิ้น")
    except Exception as e:
        logger.exception("Error while downloading TikTok video")
        await status_msg.edit_text(f"❌ เกิดข้อผิดพลาด: {e}")
    finally:
        if os.path.exists(video_path):
            try:
                os.remove(video_path)
            except Exception:
                pass

# -------------------------------------------------
# Main entry point
# -------------------------------------------------
async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("🤖 Bot started – listening for messages")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio

    asyncio.run(main())