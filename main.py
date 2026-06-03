print("🔥 MAIN.PY IS RUNNING")

import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
FILE_NAME = "results.txt"


# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome!\n\n"
        "/add 1.25 - Add result\n"
        "/history - Show history\n"
        "/stats - Show statistics\n"
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

        text = "\n".join(f"{line}x" for line in clean_lines[-10:])
        await update.message.reply_text(text)

    except FileNotFoundError:
        await update.message.reply_text("No results saved.")


# ---------------- STATS ----------------
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        with open(FILE_NAME, "r") as f:
            lines = f.readlines()

        values = [float(line.strip()) for line in lines if line.strip()]

        if not values:
            await update.message.reply_text("No results saved.")
            return

        avg = sum(values) / len(values)
        highest = max(values)
        lowest = min(values)

        message = (
            f"📊 Statistics\n\n"
            f"Results saved: {len(values)}\n"
            f"Average: {avg:.2f}x\n"
            f"Highest: {highest:.2f}x\n"
            f"Lowest: {lowest:.2f}x"
        )

        await update.message.reply_text(message)

    except FileNotFoundError:
        await update.message.reply_text("No results saved.")


# ---------------- SCAN ----------------
async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        with open(FILE_NAME, "r") as f:
            lines = f.readlines()

        values = [float(line.strip()) for line in lines if line.strip()]

        if len(values) < 5:
            await update.message.reply_text(
                "Need at least 5 saved results.\nUse /add after each round."
            )
            return

        recent = values[-5:]
        avg = sum(recent) / len(recent)

        if avg >= 2:
            signal = "🟢 HIGH CHANCE\nTarget: 2x+"
        elif avg >= 1.5:
            signal = "🟡 MEDIUM CHANCE\nTarget: 1.5x - 2x"
        else:
            signal = "🔴 LOW CHANCE\nWait for next round"

        await update.message.reply_text(
            f"📊 Smart Signal\n\n"
            f"Last 5 Average: {avg:.2f}x\n\n"
            f"{signal}"
        )

    except FileNotFoundError:
        await update.message.reply_text("No results saved.")


# ---------------- BOT SETUP ----------------
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add", add))
app.add_handler(CommandHandler("history", history))
app.add_handler(CommandHandler("stats", stats))
app.add_handler(CommandHandler("scan", scan))


# ---------------- RUN BOT ----------------
async def main():
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
