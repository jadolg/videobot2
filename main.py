import os

import youtube_dl
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler
from telegram.ext.filters import ALL


async def download(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.text == "/start":
        await update.message.reply_text("Let's download some weejios")
        return
    await context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
    ydl_opts = {
        'outtmpl': '%(id)s.%(ext)s',
    }
    video_url = update.message.text
    if not video_url.startswith("https://"):
        await update.message.reply_text("This doesn't look like a URL")
        return
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(
                video_url,
            )
        except youtube_dl.utils.DownloadError:
            await update.message.reply_text(text=f"I could not download this 😅")
        output_file = f'{info.get("id")}.{info.get("ext")}'
        try:
            await update.message.reply_video(video=open(output_file, 'rb'))
        except:
            await update.message.reply_text(
                text=f"Looks like something went wrong uploading the video to telegram. It possibly is bigger than 50Mb.")
        os.remove(output_file)


if __name__ == '__main__':
    TOKEN = os.environ.get('TELEGRAM_TOKEN')
    WEBHOOK_URL = os.environ.get('WEBHOOK_URL')
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(callback=download, filters=ALL))
    app.run_webhook(listen='0.0.0.0', port=9991, webhook_url=WEBHOOK_URL)
