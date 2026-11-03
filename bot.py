import telebot
import yt_dlp
import os

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "أبعثلي اسم الأغنية 🎵")

@bot.message_handler(func=lambda m: True)
def search(m):
    try:
        bot.reply_to(m, "نحوس عليها... ⏳")
        ydl_opts = {'quiet': True, 'default_search': 'ytsearch1', 'format': 'bestaudio', 'noplaylist': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(m.text, download=False)
            if 'entries' in info:
                info = info['entries'][0]
            title = info.get('title')
            url = info.get('webpage_url')
            bot.send_message(m.chat.id, f"🎵 {title}\n{url}")
    except Exception as e:
        bot.reply_to(m, f"خطأ: {e}")

bot.infinity_polling()
