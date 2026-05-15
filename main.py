import os
import logging
import yt_dlp
import uuid
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
        "🚀 **أهلاً بك في بوت التحميل | Na Capcut**\n\n"
        "أرسل رابط لأي فيديو تيك توك أو انستجرام أو بنترست أو يوتيوب وسيتم تحميله مباشرة! ✨\n\n"
        "📌 **برجاء الاشتراك في القناة لاستمرار الخدمة:**"
    )
    await update.message.reply_text(
        welcome_text,
        parse_mode='Markdown',
        reply_markup=get_main_keyboard()
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        if member.status in ['left', 'kicked']:
            await update.message.reply_text(f'⚠️ **يجب عليك الاشتراك في القناة:**\n{CHANNEL_USERNAME}', reply_markup=get_main_keyboard())
            return
    except Exception:
        await update.message.reply_text('⚠️ **خطأ:** يجب وضع البوت كمشرف في القناة.', reply_markup=get_main_keyboard())
        return

    url = update.message.text
    if url.startswith('/'):
        return

    status_msg = await update.message.reply_text('⏳ **جاري التحميل... انتظر.**')
    filename = f"video_{uuid.uuid4().hex}.mp4"
    ydl_opts = {
        'format': 'best',
        'outtmpl': filename,
        'user_agent': 'Mozilla/5.0'
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        await update.message.reply_video(video=open(filename, 'rb'), reply_markup=get_main_keyboard())
        await status_msg.delete()
        os.remove(filename)
    except Exception as e:
        await status_msg.edit_text('❌ **تعذر التحميل. تأكد أن الرابط صحيح وصيغة الفيديو مدعومة!**', reply_markup=get_main_keyboard())
        if os.path.exists(filename):
            os.remove(filename)

def main():
    token = "8709764403:AAGYvZ6NAvB4IFI5UfVgJI8cH4uqfW7n4lA"
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == '__main__':
    main()
