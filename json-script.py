from google.cloud import dialogflow_v2 as dialogflow
import json
from environs import Env
from google.cloud.dialogflow_v2beta1 import IntentsClient

env = Env()
env.read_env()

project_id = env('PROJECT_ID')
env("GOOGLE_APPLICATION_CREDENTIALS")


def create_intent(project_id, display_name, training_phrases_parts,
                  message_texts):
    intents_client = dialogflow.IntentsClient()
    parent = IntentsClient.project_agent_path(project_id)
    # parent = intents_client.common_project_path(project_id)

    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.types.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.types.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.types.Intent.Message.Text(text=message_texts)
    message = dialogflow.types.Intent.Message(text=text)
    intent = dialogflow.types.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message])
    response = intents_client.create_intent(parent=parent, intent=intent)


def train_agent(project_id):
    from google.cloud import dialogflow_v2beta1
    client = dialogflow_v2beta1.AgentsClient()
    parent = IntentsClient.project_agent_path(project_id)
    client.train_agent(parent)


def main():

    with open('questions.json', 'r') as file:
        intents = json.load(file)

    for intent in intents:
        display_name = intent
        intent_body = intents[display_name]
        training_phrases_parts = intent_body['questions']
        message_texts = {intent_body['answer']}

        create_intent(project_id, display_name, training_phrases_parts,
                      message_texts)

    train_agent(project_id)


if __name__ == '__main__':
    main()
