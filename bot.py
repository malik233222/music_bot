import os
import asyncio
from aiogram import Bot, Dispatcher, types
from yt_dlp import YoutubeDL

# Heroku / Railway-də Config Vars-da əlavə olunmuş token
TOKEN = os.environ.get("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()  # Aiogram 3.x-də boş Dispatcher yaradılır

# YouTube musiqi yükləyən funksiya
def download_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'song.%(ext)s',
        'noplaylist': True,
        'quiet': True
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        return filename, info.get("title", "No title")

# Mesaj handler
@dp.message()
async def handle_message(message: types.Message):
    url = message.text.strip()
    if "youtube.com" not in url and "youtu.be" not in url:
        await message.reply("📎 Xahiş edirəm YouTube link göndər.")
        return
    try:
        await message.reply("⏳ Musiqi yüklənir...")
        file_path, title = download_audio(url)
        await message.reply_audio(audio=open(file_path, "rb"), title=title)
        os.remove(file_path)
    except Exception as e:
        await message.reply(f"❌ Xəta baş verdi: {str(e)}")

# Botu polling ilə işə salmaq
if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))