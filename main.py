import os
import logging
import yt_dlp
import requests
import instaloader
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)
CHANNEL_USERNAME = "@na_capcut"

# تهيئة instaloader
L = instaloader.Instaloader()

def try_multiple_apis(url):
    API_SOURCES = ["https://api.snapsave.app/api/v1/video/download?url="]
    for api_url in API_SOURCES:
        try:
            response = requests.get(api_url + url, timeout=8)
            if response.status_code == 200:
                data = response.json()
                return data.get('data', [{}])[0].get('video_url') or data.get('video_url')
        except: continue
    return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "🚀 **أهلاً بك في بوت نور الدين للتحميل | Na Capcut**\n\n"
        "أنا مساعدك الشخصي لتحميل الفيديوهات من تيك توك، إنستجرام، وبنتريست بدون علامة مائية! ✨\n\n"
        "📌 **خطوات التحميل:**\n1. اشترك في القناة.\n2. أرسل الرابط.\n\nاستمتع بالخدمة! ⚡"
    )
    keyboard = [
        [InlineKeyboardButton("📢 اشترك في القناة", url=f"https://t.me/{CHANNEL_USERNAME.replace('@', '')}")],
        [InlineKeyboardButton("👨‍💻 تواصل مع المطور", url="https://t.me/nacapcut")]
    ]
    await update.message.reply_text(welcome_text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    status_msg = await update.message.reply_text('⏳ **جاري التحميل من سيرفر نور الدين...**')
    keyboard = [
        [InlineKeyboardButton("🎨 انضم لمجموعة عالم المصممين", url="https://t.me/+Ls1IhPFuY2lhOTY8")],
        [InlineKeyboardButton("👨‍💻 تواصل مع المطور", url="https://t.me/nacapcut")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # 1. محاولة بـ Instaloader (لإنستجرام فقط)
    if "instagram.com" in url:
        try:
            shortcode = url.split("/")[-2]
            post = instaloader.Post.from_shortcode(L.context, shortcode)
            await update.message.reply_video(video=post.video_url, reply_markup=reply_markup)
            await status_msg.delete(); return
        except: pass

    # 2. محاولة بـ yt-dlp
    try:
        ydl_opts = {'format': 'best', 'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            await update.message.reply_video(video=info.get('url'), reply_markup=reply_markup)
            await status_msg.delete(); return
    except: pass

    # 3. محاولة بـ API
    api_video = try_multiple_apis(url)
    if api_video:
        await update.message.reply_video(video=api_video, reply_markup=reply_markup)
        await status_msg.delete()
    else:
        await status_msg.edit_text('❌ **تعذر التحميل.**\nالرابط قد يكون خاصاً.', reply_markup=reply_markup)

def main():
    token = os.environ.get("BOT_TOKEN")
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == '__main__':
    main()
