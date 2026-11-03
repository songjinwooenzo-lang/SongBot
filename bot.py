import os
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎵 أبعثلي اسم الأغنية")

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    await update.message.reply_text(f"نحوس على: {query}... ⏳")
    ydl_opts = {'format': 'bestaudio/best', 'quiet': True, 'noplaylist': True, 'default_search': 'ytsearch'}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)
            if 'entries' in info:
                info = info['entries'][0]
            title = info.get('title', 'Unknown')
            url = info.get('webpage_url', '')
            await update.message.reply_text(f"🎵 {title}\n🔗 {url}")
            ydl_opts2 = {'format': 'bestaudio/best', 'outtmpl': '/tmp/%(title)s.%(ext)s', 'quiet': True}
            with yt_dlp.YoutubeDL(ydl_opts2) as ydl2:
                info2 = ydl2.extract_info(url, download=True)
                filename = ydl2.prepare_filename(info2)
                await update.message.reply_audio(audio=open(filename, 'rb'), title=title)
                os.remove(filename)
    except Exception as e:
        await update.message.reply_text(f"خطأ: {e}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search))
    app.run_polling()

if __name__ == '__main__':
    main()
