print("🔥 MAIN.PY IS RUNNING")

import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Load token from Render environment variables
TOKEN = os.getenv("BOT_TOKEN")

# Simple file storage (better than in-memory list on Render)
FILE_NAME = "results.txt"


# ---------------- START COMMAND ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome!\n\n"
        "/add 1.25 - Add result\n"
        "/history - Show history\n"
        "/scan - Generate signal"
    )


# ---------------- ADD RESULT ----------------
async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        value = float(context.args[0])

        with open(FILE_NAME, "a") as f:
            f.write(f"{value}\n")

        await update.message.reply_text(f"Saved: {value}x")

    except:
        await update.message.reply_text("Usage: /add 1.25")


# ---------------- HISTORY ----------------
async def history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        with open(FILE_NAME, "r") as f:
            lines = f.readlines()

        clean_lines = [line.strip() for line in lines if line.strip()]

        if not clean_lines:
            await update.message.reply_text("No results saved.")
            return

        text = "\n".join(f"{x}x" for x in clean_lines[-10:])
        await update.message.reply_text(text)

    except FileNotFoundError:
        await update.message.reply_text("No results saved.")


# ---------------- SCAN ----------------
async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📊 Signal\n\n"
        "Custom signal generated."
    )


# ---------------- BOT SETUP ----------------
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add", add))
app.add_handler(CommandHandler("history", history))
app.add_handler(CommandHandler("scan", scan))


# ---------------- RUN BOT ----------------
async def main():
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
