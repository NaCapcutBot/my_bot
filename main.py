import os
import logging
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)

CHANNEL_USERNAME = "@na_capcut" 

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "🚀 **أهلاً بك في بوت نور الدين للتحميل | Na Capcut**\n\n"
        "لتحميل الفيديوهات، يجب أن تكون مشتركاً في القناة أولاً! ✨\n\n"
        f"👉 اشترك هنا: {CHANNEL_USERNAME}\n\n"
        "بعد الاشتراك أرسل الرابط مباشرة! ⚡"
    )
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    try:
        # فحص الاشتراك
        member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        if member.status in ['left', 'kicked']:
            await update.message.reply_text(f'⚠️ **عذراً، يجب أن تشترك في القناة أولاً:**\n{CHANNEL_USERNAME}')
            return
    except:
        await update.message.reply_text('⚠️ **خطأ:** يرجى التأكد من إضافة البوت كمشرف في القناة.')
        return

    # إذا وصل لهنا فهو مشترك
    url = update.message.text
    status_msg = await update.message.reply_text('⏳ **جاري التحميل...**')
    try:
        ydl_opts = {'format': 'best', 'outtmpl': 'video.mp4'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        await update.message.reply_video(video=open('video.mp4', 'rb'))
        os.remove('video.mp4')
        await status_msg.delete()
    except:
        await status_msg.edit_text('❌ **لم أتمكن من تحميل الرابط.**')

def main():
    token = os.environ.get("BOT_TOKEN")
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == '__main__':
    main()
