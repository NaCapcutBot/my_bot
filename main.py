import os
import logging
import yt_dlp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)
CHANNEL_USERNAME = "@na_capcut"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "🚀 **أهلاً بك في بوت نور الدين للتحميل | Na Capcut**\n\n"
        "أنا مساعدك الشخصي لتحميل الفيديوهات من تيك توك وإنستجرام بدون علامة مائية! ✨\n\n"
        "📌 **خطوات التحميل:**\n1. اشترك في القناة.\n2. أرسل الرابط.\n\nاستمتع بالخدمة! ⚡"
    )
    keyboard = [
        [InlineKeyboardButton("📢 اشترك في القناة", url=f"https://t.me/{CHANNEL_USERNAME.replace('@', '')}")],
        [InlineKeyboardButton("👨‍💻 تواصل مع المطور", url="https://t.me/nacapcut")]
    ]
    await update.message.reply_text(welcome_text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    url = update.message.text
    
    # التحقق من الاشتراك
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        if member.status in ['left', 'kicked']:
            await update.message.reply_text('⚠️ **اشترك في القناة أولاً للتحميل.**')
            return
    except:
        pass

    status_msg = await update.message.reply_text('⏳ **جاري التحميل...**')
    
    keyboard = [
        [InlineKeyboardButton("🎨 انضم لمجموعة عالم المصممين", url="https://t.me/+Ls1IhPFuY2lhOTY8")],
        [InlineKeyboardButton("👨‍💻 تواصل مع المطور", url="https://t.me/nacapcut")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        ydl_opts = {'format': 'best', 'outtmpl': 'file.%(ext)s', 'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        await update.message.reply_video(video=open(filename, 'rb'), reply_markup=reply_markup)
        os.remove(filename)
        await status_msg.delete()
    except:
        await status_msg.edit_text('❌ **عذراً، تعذر التحميل.**\nتأكد أن الرابط عام وليس خاصاً.')

def main():
    token = os.environ.get("BOT_TOKEN")
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == '__main__':
    main()
