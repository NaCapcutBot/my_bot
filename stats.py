# stats.py
async def update_bot_description(context, count):
    new_about = (
        f"Na Downloader | بوت التحميل 📥\n"
        f"📥 تيك توك | إنستجرام (بدون حقوق)\n"
        f"👥 المشتركون: {count} مشتركاً\n"
        f"🎬 قوالب CapCut: @na_capcut\n"
        f"👤 المطور: @nacapcut"
    )
    # استخدام مكتبة python-telegram-bot لتحديث الوصف
    await context.bot.set_my_description(new_about)
