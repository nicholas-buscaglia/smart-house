import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

prompt = ''


def chat(text, convo):

    global prompt

    if convo == 'new':
        prompt = "The following is a conversation with an AI assistant (you). The assistant is helpful, creative, " \
                 "clever, and very friendly.\n\nYour name is Poppy and you exist to serve humans. Your data is private." \
                 "\nHuman: " + text + \
                 "\nAI: "
    else:
        prompt = prompt + text + "\nAI: "

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.9,
        max_tokens=150,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        # stop=[" Human:", " AI:"]
    )
    resp = response.choices[0].text.strip()

    print(f'Poppy: {resp}')

    prompt += (resp + "\nHuman: ")

    return resp
