import os
import logging
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from yt_dlp import YoutubeDL

# ----------------------------------------------------------------------
# ตั้งค่า Logging
# ----------------------------------------------------------------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# ----------------------------------------------------------------------
# ค่าคอนฟิก
# ----------------------------------------------------------------------
# ใส่ Token ของ Bot ที่คุณได้จาก @BotFather
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # แนะนำให้ใช้ env variable
if not TOKEN:
    raise ValueError("กรุณากำหนดตัวแปรสภาพแวดล้อม TELEGRAM_BOT_TOKEN")

# ----------------------------------------------------------------------
# ฟังก์ชันดาวน์โหลด TikTok ด้วย yt-dlp
# ----------------------------------------------------------------------
def download_tiktok(url: str) -> str:
    """
    ดาวน์โหลดวิดีโอจาก TikTok และคืนที่อยู่ไฟล์ที่ถูกบันทึก
    """
    ydl_opts = {
        "outtmpl": "downloaded_%(id)s.%(ext)s",  # ชื่อไฟล์แบบอัตโนมัติ
        "format": "mp4",                       # บังคับให้ได้ mp4
        "quiet": True,
        "no_warnings": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
    return filename

# ----------------------------------------------------------------------
# คำสั่ง /start
# ----------------------------------------------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "สวัสดีครับ! ส่งลิงก์ TikTok มาให้ผม แล้วผมจะดาวน์โหลดวิดีโอให้คุณ"
    )

# ----------------------------------------------------------------------
# จัดการข้อความ (ลิงก์ TikTok)
# ----------------------------------------------------------------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if "tiktok.com" not in text:
        await update.message.reply_text("กรุณาส่งลิงก์ TikTok เท่านั้น")
        return

    msg = await update.message.reply_text("กำลังดาวน์โหลดวิดีโอ... ⏳")
    try:
        video_path = download_tiktok(text)
        # ส่งไฟล์กลับผู้ใช้
        with open(video_path, "rb") as video_file:
            await context.bot.send_video(chat_id=update.effective_chat.id, video=video_file)
        await msg.edit_text("ดาวน์โหลดเสร็จแล้ว ✅")
        # ลบไฟล์ชั่วคราว
        os.remove(video_path)
    except Exception as e:
        logger.exception("Error while downloading TikTok video")
        await msg.edit_text(f"เกิดข้อผิดพลาด: {e}")

# ----------------------------------------------------------------------
# เริ่ม Application
# ----------------------------------------------------------------------
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # เริ่ม Bot
    await app.start()
    logger.info("Bot กำลังทำงาน...")
    await app.updater.start_polling()
    await app.updater.idle()

if __name__ == "__main__":
    import asyncio

    asyncio.run(main())