import os
import logging

# حماية ضد نقص المكتبات
try:
    from telegram import Update
    from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
except ImportError:
    pass

# إعداد السجل
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update, context):
    update.message.reply_text('أهلاً بك في بوت التحميل الخاص بنور الدين! أرسل رابط تيك توك الآن وسأحمله لك.')

def echo(update, context):
    url = update.message.text
    if "tiktok.com" in url or "instagram.com" in url:
        update.message.reply_text('جاري التحميل... يرجى الانتظار.')
    else:
        update.message.reply_text('الرجاء إرسال رابط صحيح من تيك توك أو إنستقرام.')

def main():
    token = os.environ.get("BOT_TOKEN")
    if not token:
        print("خطأ: لم يتم العثور على BOT_TOKEN")
        return
        
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
