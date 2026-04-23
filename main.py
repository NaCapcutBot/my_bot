import os
import logging
import yt_dlp
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- الإعدادات ---
logging.basicConfig(level=logging.INFO)
CHANNEL_USERNAME = "@na_capcut"

# --- دالة التحميل عبر API ---
def get_video_via_api(url):
    try:
        api_url = f"https://api.snapsave.app/api/v1/video/download?url={url}"
        response = requests.get(api_url, timeout=10)
        if response.status_code == 200:
            return response.json()['data']['video_url']
    except:
        return None
    return None

# --- دالة الترحيب ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = "🚀 **أهلاً بك في بوت نور الدين للتحميل | Na Capcut**\n\nأنا مساعدك الشخصي لتحميل الفيديوهات والصور من تيك توك، إنستجرام، وبنتريست بدون علامة مائية! ✨"
    keyboard = [
        [InlineKeyboardButton("📢 اشترك في القناة", url=f"https://t.me/{CHANNEL_USERNAME.replace('@', '')}")],
        [InlineKeyboardButton("👨‍💻 تواصل مع المطور", url="https://t.me/nacapcut")]
    ]
    await update.message.reply_text(welcome_text, reply_markup=InlineKeyboardMarkup(keyboard))

# --- دالة المعالجة ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    url = update.message.text
    
    # 1. التحقق من الاشتراك
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        if member.status in ['left', 'kicked']:
            await update.message.reply_text('⚠️ **اشترك في القناة أولاً للتحميل.**')
            return
    except:
        pass

    status_msg = await update.message.reply_text('⏳ **جاري المعالجة من سيرفر نور الدين...**')
    
    # 2. أزرار المجموعة
    keyboard = [[InlineKeyboardButton("🎨 انضم لمجموعة عالم المصممين", url="https://t.me/+Ls1IhPFuY2lhOTY8")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        # المحاولة الأولى: yt-dlp
        ydl_opts = {'format': 'best', 'outtmpl': 'file.%(ext)s', 'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        await update.message.reply_video(video=open(filename, 'rb'), reply_markup=reply_markup)
        os.remove(filename)
        await status_msg.delete()
    except:
        # المحاولة الثانية: الـ API
        api_video = get_video_via_api(url)
        if api_video:
            await update.message.reply_video(video=api_video, caption="✅ **تم التحميل بنجاح عبر سيرفر الـ API**", reply_markup=reply_markup)
            await status_msg.delete()
        else:
            await status_msg.edit_text('❌ **تعذر التحميل.**\nتأكد أن الرابط عام وليس خاصاً.')

def main():
    token = os.environ.get("BOT_TOKEN")
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == '__main__':
    main()
