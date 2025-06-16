
import telebot
import yt_dlp
import os

TOKEN = '6520047119:AAG2LixKLKeuMK2B36u1vnj7KiO3L506kJs'
bot = telebot.TeleBot(TOKEN)

def download_video(url):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
        'outtmpl': 'video.%(ext)s',
        'merge_output_format': 'mp4',
        'noplaylist': True,
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Salom! Menga YouTube yoki Instagram havolasini yuboring, men sizga videoni jo‘nataman.")

@bot.message_handler(func=lambda message: True)
def handle_url(message):
    url = message.text.strip()
    if "youtu" in url or "instagram" in url:
        try:
            bot.send_message(message.chat.id, "🔄 Video yuklanmoqda, biroz kuting...")
            video_path = download_video(url)
            file_size = os.path.getsize(video_path)
            if file_size <= 2 * 1024 * 1024 * 1024:
                with open(video_path, 'rb') as video:
                    bot.send_document(message.chat.id, video)
            else:
                bot.send_message(message.chat.id, "❌ Video fayli juda katta, Telegram orqali jo‘natib bo‘lmaydi.")
            os.remove(video_path)
        except Exception as e:
            bot.send_message(message.chat.id, f"❗ Xatolik yuz berdi:\n{str(e)}")
    else:
        bot.send_message(message.chat.id, "Iltimos, faqat YouTube yoki Instagram havolasini yuboring.")

bot.polling(non_stop=True)
