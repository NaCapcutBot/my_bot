import os
import logging
import sys

# خدعة برمجية لتجاهل imghdr تماماً ومنع الخطأ
sys.modules['imghdr'] = type('dummy', (object,), {'what': lambda *a: None})

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# إعداد السجل
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update, context):
    update.message.reply_text('أهلاً بك في بوت التحميل الخاص بنور الدين!')

def echo(update, context):
    update.message.reply_text('جاري التحميل...')

def main():
    token = os.environ.get("BOT_TOKEN")
    if not token:
        return
        
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
