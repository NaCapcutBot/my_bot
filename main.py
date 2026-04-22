import os
import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# إعداد السجل
logging.basicConfig(level=logging.INFO)

async def start(update, context):
    await update.message.reply_text('أهلاً بك في بوت التحميل الخاص بنور الدين! جاهز للعمل.')

async def echo(update, context):
    await update.message.reply_text('تم استلام الرابط، جاري المعالجة...')

def main():
    token = os.environ.get("BOT_TOKEN")
    if not token:
        print("BOT_TOKEN غير موجود في المتغيرات!")
        return

    # إنشاء التطبيق بالطريقة الحديثة
    app = Application.builder().token(token).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    print("البوت يعمل الآن...")
    app.run_polling()

if __name__ == '__main__':
    main()
