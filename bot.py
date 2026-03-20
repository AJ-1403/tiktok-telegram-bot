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

# ----------------------------------------------------------------------
# Logging configuration
# ----------------------------------------------------------------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------
# Bot token should be stored in an environment variable for safety.
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError(
        "❗️ Please set the TELEGRAM_BOT_TOKEN environment variable (you can obtain it from @BotFather)."
    )

# ----------------------------------------------------------------------
# TikTok download helper (yt‑dlp)
# ----------------------------------------------------------------------
def download_tiktok(url: str) -> str:
    """
    Download a TikTok video using yt‑dlp.
    Returns the absolute path of the downloaded file.
    """
    ydl_opts = {
        "outtmpl": "downloaded_%(id)s.%(ext)s",  # unique filename per video
        "format": "mp4",  # force MP4 output
        "quiet": True,
        "no_warnings": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
    return os.path.abspath(filename)


# ----------------------------------------------------------------------
# /start command
# ----------------------------------------------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "👋 สวัสดีครับ! ส่งลิงก์ TikTok มาให้ผม แล้วผมจะดาวน์โหลดวิดีโอให้คุณ 🎥"
    )


# ----------------------------------------------------------------------
# Message handler – expects a TikTok URL
# ----------------------------------------------------------------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text.strip()

    if "tiktok.com" not in text.lower():
        await update.message.reply_text("⚠️ กรุณาส่งลิงก์ TikTok เท่านั้น")
        return

    status_msg = await update.message.reply_text("🔄 กำลังดาวน์โหลดวิดีโอ...")

    try:
        video_path = download_tiktok(text)

        # Send the video back to the user
        with open(video_path, "rb") as video_file:
            await context.bot.send_video(
                chat_id=update.effective_chat.id,
                video=video_file,
                caption="✅ ดาวน์โหลดสำเร็จ",
            )

        await status_msg.edit_text("✅ เสร็จสิ้น")
    except Exception as e:
        logger.exception("Failed to download TikTok video")
        await status_msg.edit_text(f"❌ เกิดข้อผิดพลาด: {e}")
    finally:
        # Clean up the temporary file if it exists
        if os.path.exists(video_path):
            try:
                os.remove(video_path)
            except Exception:
                pass


# ----------------------------------------------------------------------
# Main entry point
# ----------------------------------------------------------------------
async def main() -> None:
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    logger.info("🤖 Bot started – listening for messages")
    await app.run_polling()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())