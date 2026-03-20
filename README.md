# TikTok Downloader Telegram Bot

A minimal Telegram bot that downloads TikTok videos and sends them back to the user.  
The project is ready to be pushed to **GitHub** and deployed on any platform that can run Python (Railway, Render, Fly.io, Heroku, Docker, etc.).

## Features
- ✅ Accepts a TikTok URL and returns the video as an MP4 file.  
- 📦 Uses `yt‑dlp` (a fast fork of `youtube‑dl`) for reliable downloading.  
- 🛡️ Bot token is read from the environment variable `TELEGRAM_BOT_TOKEN`.  
- 🔧 Simple code base – easy to extend (quality selection, GIF conversion, etc.).

## Prerequisites
1. **Python 3.9+** (tested with 3.11).  
2. A Telegram bot token from **@BotFather**.  

## Quick Start (local)

```bash
# 1️⃣ Clone the repo
git clone https://github.com/<your‑username>/tiktok-telegram-bot.git
cd tiktok-telegram-bot

# 2️⃣ Create a virtual environment & install deps
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3️⃣ Set the bot token (replace <TOKEN> with the one from @BotFather)
export TELEGRAM_BOT_TOKEN=<TOKEN>   # Linux/macOS
# set TELEGRAM_BOT_TOKEN=<TOKEN>   # Windows PowerShell

# 4️⃣ Run the bot
python bot.py
```

The bot will start polling. Open Telegram, find your bot, send `/start` and then a TikTok link.

## Deploying to Railway (free tier)

1. Sign in to **[Railway.app](https://railway.app)** and link your GitHub repository.  
2. Railway will auto‑detect the `requirements.txt` file and install dependencies.  
3. Add a **Variable** named `TELEGRAM_BOT_TOKEN` with your token value.  
4. Deploy – Railway will run `python bot.py` automatically.  

## Deploying to Render (free tier)

1. Create a new **Web Service** on Render and connect your GitHub repo.  
2. In the **Build Command** leave it empty (Render will run `pip install -r requirements.txt`).  
3. Set **Start Command** to: `python bot.py`  
4. Add an environment variable `TELEGRAM_BOT_TOKEN`.  
5. Deploy.

## Deploying with Docker

A `Dockerfile` is provided for containerised deployment.

```bash
docker build -t tiktok-bot .
docker run -e TELEGRAM_BOT_TOKEN=<YOUR_TOKEN> tiktok-bot
```

## Extending the Bot

- **Choose video quality** – modify `ydl_opts["format"]` (e.g., `"best"`).  
- **Add /help command** – similar to `/start`.  
- **Support batch download** – handle multiple URLs in one message.  

Feel free to open issues or pull‑requests if you improve the bot. Happy coding! 🎉

## License

MIT – you may use, modify, and distribute this code as you wish.  

---  

*Disclaimer*: This bot is for personal use and educational purposes.  
Make sure you respect TikTok’s terms of service and local copyright laws when downloading content.