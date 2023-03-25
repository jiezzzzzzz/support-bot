from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from environs import Env
from detect_intent import detect_intent_texts


env = Env()
env.read_env()
lang = env('LANGUAGE')
project_id = env('PROJECT_ID')


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Здравствуйте\!',
        reply_markup=ForceReply(selective=True),
    )


def reply(update: Update, context: CallbackContext) -> None:
    text = detect_intent_texts(project_id, update.message.from_user['id'], update.message.text, lang)
    update.message.reply_text(text)


def main() -> None:
    updater = Updater(env('TELEGRAM_TOKEN'))

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))

    updater.start_polling()

    dispatcher.add_handler(MessageHandler(Filters.text, reply))

    updater.idle()


if __name__ == '__main__':
    main()