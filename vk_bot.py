import random
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from environs import Env
from detect_intent import detect_intent_texts


def start_bot(events, api):
    user_id = events.user_id
    text = events.text
    intent = detect_intent_texts(project_id, user_id, text, 'ru')
    if not intent.query_result.intent.is_fallback:
        api.messages.send(
            user_id=events.user_id,
            message=intent.query_result.fulfillment_text,
            random_id=random.randint(1, 1000)
        )


if __name__ == "__main__":
    env = Env()
    env.read_env()

    token = env('VK_SECRET_TOKEN')
    project_id = env('PROJECT_ID')
    vk_session = vk.VkApi(token=env('VK_SECRET_TOKEN'))
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            start_bot(event, vk_api)
