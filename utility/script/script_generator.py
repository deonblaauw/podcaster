import openai
import json
import os

def generate_conversation(topic, provider, model, prompt, temp):
    print("Generating conversation on topic:", topic)

    if provider == "openai":
        OPENAI_API_KEY = os.getenv('OPENAI_KEY')
        openai.api_key = OPENAI_API_KEY
    else:
        raise ValueError("Invalid provider")

    response = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": topic}
        ],
        temperature=temp
    )

    content = response.choices[0].message.content

    # Return the content as plain text
    return content

def summarize_dialog(dialog, topic, provider, model, prompt):

    if provider == "openai":
        OPENAI_API_KEY = os.getenv('OPENAI_KEY')
        openai.api_key = OPENAI_API_KEY
    else:
        raise ValueError("Invalid provider")

    response = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": dialog}
        ]
    )

    content = response.choices[0].message.content

    # Return the content as plain text
    return content