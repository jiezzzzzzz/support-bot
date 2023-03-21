import logging
from google.cloud import dialogflow
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from environs import Env


env = Env()
env.read_env
def detect_intent_texts(project_id, session_id, text, language_code):

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))

    text_input = dialogflow.TextInput(text=text, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return 'Я могу сказать: {}'.format(response.query_result.fulfillment_text)


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Здравствуйте\!',
        reply_markup=ForceReply(selective=True),
    )


def reply(update: Update, context: CallbackContext) -> None:
    text = detect_intent_texts(env('PROJECT_ID'), update.message.from_user['id'], update.message.text, env('LANGUAGE'))
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