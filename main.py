import os
import logging
import yt_dlp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)

CHANNEL_USERNAME = "@na_capcut" 

# --- الأزرار ---
def get_main_keyboard():
    keyboard = [
        [InlineKeyboardButton("📢 اشترك في القناة", url=f"https://t.me/{CHANNEL_USERNAME.replace('@', '')}")],
        [InlineKeyboardButton("🎨 مجموعة عالم المصممين", url="https://t.me/+Ls1IhPFuY2lhOTY8")],
        [InlineKeyboardButton("👨‍💻 تواصل مع المطور", url="https://t.me/nacapcut")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "🚀 **أهلاً بك في بوت نور الدين للتحميل | Na Capcut**\n\n"
        "أنا مساعدك الشخصي لتحميل فيديوهات التيك توك والإنستجرام بجودة عالية وبدون علامة مائية! ✨\n\n"
        "📌 **خطوة واحدة للبدء:**\n"
        "لضمان استمرار الخدمة، يرجى الاشتراك في القناة الرسمية.\n\n"
        "بعد الاشتراك، أرسل الرابط فقط واستمتع بالتحميل! ⚡"
    )
    await update.message.reply_text(welcome_text, parse_mode='Markdown', reply_markup=get_main_keyboard())

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        if member.status in ['left', 'kicked']:
            await update.message.reply_text(f'⚠️ **عذراً، يجب أن تكون مشتركاً في القناة أولاً:**\n{CHANNEL_USERNAME}', reply_markup=get_main_keyboard())
            return
    except Exception:
        await update.message.reply_text('⚠️ **خطأ:** يرجى التأكد من إضافة البوت كـ "مشرف" في القناة.')
        return

    url = update.message.text
    if url.startswith('/'): return
    
    status_msg = await update.message.reply_text('⏳ **جاري التحميل... يرجى الانتظار!**')
    
    try:
        ydl_opts = {'format': 'best', 'outtmpl': 'video.mp4', 'user_agent': 'Mozilla/5.0'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # إرسال الفيديو مع الأزرار
        await update.message.reply_video(video=open('video.mp4', 'rb'), reply_markup=get_main_keyboard())
        os.remove('video.mp4')
        await status_msg.delete()
    except Exception:
        await status_msg.edit_text('❌ **عذراً، تعذر التحميل.**\nتأكد أن الرابط صحيح.', reply_markup=get_main_keyboard())

def main():
    token = os.environ.get("BOT_TOKEN")
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == '__main__':
    main()
