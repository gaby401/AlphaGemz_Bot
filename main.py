from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import config
import asyncio
from eth_scanner import scan_eth_tokens
from sol_scanner import scan_sol_tokens

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to AlphaGemz — sniper alerts loading...")

async def run_scanner(application):
    while True:
        try:
            eth_alerts = await scan_eth_tokens()
            sol_alerts = await scan_sol_tokens()
            all_alerts = eth_alerts + sol_alerts
            for alert in all_alerts:
                await application.bot.send_message(chat_id=config.TELEGRAM_CHAT_ID, text=alert)
        except Exception as e:
            print(f"[Scanner Error] {e}")
        await asyncio.sleep(60)

async def on_startup(application):
    application.create_task(run_scanner(application))

if __name__ == "__main__":
    app = ApplicationBuilder().token(config.TELEGRAM_BOT_TOKEN).post_init(on_startup).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
