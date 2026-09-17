from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import yt_dlp
import os

TOKEN = os.environ["TOKEN"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎵 Music Bot အဆင်သင့်ပါပြီ!")

async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("သီချင်းနာမည် ရိုက်ပေးပါ 🎵")
        return

    query = " ".join(context.args)
    await update.message.reply_text(f"🔎 ရှာနေပါတယ်: {query}")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "%(title)s.%(ext)s",
        "noplaylist": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{query}", download=True)
            file = ydl.prepare_filename(info["entries"][0])

        await update.message.reply_audio(audio=open(file, "rb"))
        os.remove(file)

    except Exception:
        await update.message.reply_text("❌ သီချင်းရှာ/Download မအောင်မြင်ပါဘူး။")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("play", play))
app.run_polling()