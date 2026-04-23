import os
import logging
import yt_dlp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# إعدادات البوت
logging.basicConfig(level=logging.INFO)
CHANNEL_USERNAME = "@na_capcut" 

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "🚀 **أهلاً بك في بوت نور الدين للتحميل | Na Capcut**\n\n"
        "أنا مساعدك الشخصي لتحميل الفيديوهات والصور من تيك توك، إنستجرام، وبنتريست بدون علامة مائية! ✨\n\n"
        "📌 **خطوات التحميل:**\n"
        "1. اشترك في القناة الرسمية.\n"
        "2. أرسل رابط الفيديو أو الصورة مباشرة.\n\n"
        "استمتع بالخدمة! ⚡"
    )
    keyboard = [
        [InlineKeyboardButton("📢 اشترك في القناة", url=f"https://t.me/{CHANNEL_USERNAME.replace('@', '')}")],
        [InlineKeyboardButton("👨‍💻 تواصل مع المطور", url="https://t.me/nacapcut")]
    ]
    await update.message.reply_text(welcome_text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    url = update.message.text
    
    # 1. التحقق من الاشتراك
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        if member.status in ['left', 'kicked']:
            keyboard = [
                [InlineKeyboardButton("📢 اشترك في القناة للتحميل", url=f"https://t.me/{CHANNEL_USERNAME.replace('@', '')}")],
                [InlineKeyboardButton("👨‍💻 تواصل مع المطور", url="https://t.me/nacapcut")]
            ]
            await update.message.reply_text('⚠️ **عذراً، يجب أن تشترك في القناة أولاً:**', reply_markup=InlineKeyboardMarkup(keyboard))
            return
    except Exception:
        await update.message.reply_text('⚠️ **خطأ:** تأكد أن البوت مشرف في القناة.')
        return

    # 2. التحميل
    status_msg = await update.message.reply_text('⏳ **جاري التحميل من سيرفر نور الدين...**')
    try:
        ydl_opts = {
            'format': 'best', 
            'outtmpl': 'downloaded_file.%(ext)s',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        
        # الأزرار (رابط مجموعتك)
        keyboard = [
            [InlineKeyboardButton("🎨 انضم لمجموعة عالم المصممين", url="https://t.me/+Ls1IhPFuY2lhOTY8")],
            [InlineKeyboardButton("👨‍💻 تواصل مع المطور", url="https://t.me/nacapcut")]
        ]
        
        # إرسال الملف (صورة أو فيديو)
        if filename.endswith(('.jpg', '.png', '.jpeg')):
            await update.message.reply_photo(photo=open(filename, 'rb'), reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            await update.message.reply_video(video=open(filename, 'rb'), reply_markup=InlineKeyboardMarkup(keyboard))
        
        os.remove(filename)
        await status_msg.delete()
    except Exception:
        await status_msg.edit_text('❌ **تعذر التحميل.**\nتأكد أن الرابط عام وليس خاصاً.')

def main():
    token = os.environ.get("BOT_TOKEN")
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == '__main__':
    main()
