import os
import logging
import yt_dlp
import random, string
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)

CHANNEL_USERNAME = "@na_capcut"

def get_main_keyboard():
    keyboard = [
        [InlineKeyboardButton("📢 اشترك في القناة", url=f"https://t.me/{CHANNEL_USERNAME.replace('@', '')}")],
        [InlineKeyboardButton("🎨 مجموعة عالم المصممين", url="https://t.me/+Ls1IhPFuY2lhOTY8")],
        [InlineKeyboardButton("👨‍💻 تواصل مع المطور", url="https://t.me/nacapcut")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    with open("users.txt", "a+") as f:
        f.seek(0)
        if user_id not in f.read().splitlines():
            f.write(user_id + "\n")
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
    except Exception as e:
        await update.message.reply_text('⚠️ **خطأ:** يرجى التأكد من إضافة البوت مشرف في القناة.')
        return

    url = update.message.text.strip()
    if url.startswith('/'): return

    status_msg = await update.message.reply_text('⏳ **جاري التحميل... يرجى الانتظار!**')
    # اسم ملف عشوائي
    rnd = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    filename = f'video_{rnd}.mp4'
    try:
        ydl_opts = {'format': 'best[ext=mp4]/best', 'outtmpl': filename, 'user_agent': 'Mozilla/5.0'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # تحقق من حجم الملف (تيليجرام حد 2GB)
        file_size = os.path.getsize(filename)
        if file_size > 2*1024*1024*1024:
            await status_msg.edit_text("❌ الفيديو أكبر من الحد المسموح في تيليجرام (2GB).")
            os.remove(filename)
            return

        await update.message.reply_video(video=open(filename, 'rb'), reply_markup=get_main_keyboard())
        await status_msg.delete()
    except Exception as e:
        await status_msg.edit_text(f'❌ **عذراً، تعذر التحميل.**\nتفاصيل: {e}', reply_markup=get_main_keyboard())
    finally:
        if os.path.exists(filename):
            os.remove(filename)

def main():
    token = os.environ.get("BOT_TOKEN")
    if not token:
        print("يرجى ضبط متغير البيئة BOT_TOKEN")
        return
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == '__main__':
    main()
