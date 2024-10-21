import openai
import json
import os

def generate_conversation(topic, provider, model, prompt):
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
        ]
    )

    content = response.choices[0].message.content

    # Return the content as plain text
    return content
