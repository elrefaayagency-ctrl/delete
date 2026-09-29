import asyncio

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

from config import (
    TELEGRAM_BOT_TOKEN,
    ALLOWED_USER_ID
)

from database import (
    init_db,
    get_status,
    recent_logs,
    set_status
)

import worker


def allowed(update):

    user = update.effective_user

    return (
        user is not None
        and user.id == ALLOWED_USER_ID
    )


def keyboard():

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "▶️ Start",
                callback_data="start"
            ),
            InlineKeyboardButton(
                "⏸ Pause",
                callback_data="pause"
            )
        ],
        [
            InlineKeyboardButton(
                "▶️ Resume",
                callback_data="resume"
            ),
            InlineKeyboardButton(
                "⛔ Stop",
                callback_data="stop"
            )
        ],
        [
            InlineKeyboardButton(
                "📊 Status",
                callback_data="status"
            ),
            InlineKeyboardButton(
                "📋 Logs",
                callback_data="logs"
            )
        ]
    ])


def status_text():

    s = get_status()

    return (
        "🤖 *Facebook Cleaner*\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        f"🔵 الحالة: `{s['status']}`\n\n"
        "📊 الإحصائيات\n"
        f"• تمت المعالجة: `{s['completed']}`\n"
        f"• الأخطاء: `{s['failed']}`\n\n"
        f"🕐 آخر تحديث:\n"
        f"`{s['updated_at']}`\n"
    )


async def start_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not allowed(update):
        return

    await update.message.reply_text(
        status_text(),
        parse_mode="Markdown",
        reply_markup=keyboard()
    )


async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    if query.from_user.id != ALLOWED_USER_ID:
        return

    action = query.data

    if action == "start":

        if not worker.is_running():

            asyncio.create_task(
                worker.run_worker()
            )

        text = "▶️ تم تشغيل الـWorker."

    elif action == "pause":

        worker.pause()

        text = "⏸ تم إيقاف الـWorker مؤقتًا."

    elif action == "resume":

        worker.resume()

        text = "▶️ تم استئناف الـWorker."

    elif action == "stop":

        worker.stop()

        text = "⛔ تم إيقاف الـWorker."

    elif action == "status":

        text = status_text()

    elif action == "logs":

        logs = recent_logs(10)

        if not logs:

            text = "📋 لا توجد Logs."

        else:

            lines = [
                "📋 *آخر العمليات*\n"
            ]

            for level, message, created in logs:

                lines.append(
                    f"`{created}` "
                    f"*{level}*\n"
                    f"{message}\n"
                )

            text = "\n".join(lines)

    else:

        text = "Unknown command."

    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=keyboard()
    )


def main():

    init_db()

    application = (
        Application
        .builder()
        .token(TELEGRAM_BOT_TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler(
            "start",
            start_command
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            button_handler
        )
    )

    print(
        "Telegram bot is running..."
    )

    application.run_polling()


if __name__ == "__main__":
    main()
