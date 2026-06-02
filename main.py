from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

results = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome!\n\n"
        "/add 1.25 - Add result\n"
        "/history - Show history\n"
        "/scan - Generate signal"
    )

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        value = float(context.args[0])
        results.append(value)
        await update.message.reply_text(f"Saved: {value}x")
    except:
        await update.message.reply_text("Usage: /add 1.25")

async def history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not results:
        await update.message.reply_text("No results saved.")
        return

    text = "\n".join(f"{x}x" for x in results[-10:])
    await update.message.reply_text(text)

async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📊 Signal\n\n"
        "Custom signal generated."
    )

TOKEN = os.getenv("BOT_TOKEN")
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add", add))
app.add_handler(CommandHandler("history", history))
app.add_handler(CommandHandler("scan", scan))

app.run_polling()
