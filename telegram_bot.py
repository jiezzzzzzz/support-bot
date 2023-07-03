from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from environs import Env
from detect_intent import detect_intent_texts


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Здравствуйте\!',
        reply_markup=ForceReply(selective=True),
    )


def reply(update: Update, context: CallbackContext, project_id: str) -> None:
    chat_id = update.message.chat_id
    text = update.message.text
    intent = detect_intent_texts(
        project_id=project_id,
        session_id=chat_id,
        text=text,
        language_code='ru'
    )
    update.message.reply_text(text=intent.query_result.fulfillment_text)


def main() -> None:
    env = Env()
    env.read_env()
    lang = env('LANGUAGE')
    project_id = env('PROJECT_ID')

    updater = Updater(env('TELEGRAM_TOKEN'))

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))

    updater.start_polling()

    dispatcher.add_handler(MessageHandler(Filters.text, reply))

    updater.idle()


if __name__ == '__main__':
    main()