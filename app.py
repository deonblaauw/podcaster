import argparse
from utility.script.script_generator import generate_conversation
from utility.script.prompts import create_host_prompt, create_guest_prompt
from utility.audio.audio_generator import generate_combined_audio
import os
import asyncio

if __name__ == "__main__":
    # Argument parsing to include landscape/portrait option and output filename
    parser = argparse.ArgumentParser(description="Generate a podcast interview between two AIs.")
    parser.add_argument("topic", type=str, help="The topic for the podcast")
    parser.add_argument("--tts", type=str, default="openai", help="Text to speech engine. Options are openai or edge. Default is openai")
    parser.add_argument("--output_dir", type=str, default="generated_outputs", help="Folder where text files are stored. Default is generated_outputs")

    args = parser.parse_args()
    SAMPLE_TOPIC = args.topic
    TTS_ENGINE = args.tts
    OUTPUT_DIR = args.output_dir

    # Ensure the output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    PROVIDER = "openai"
    MODEL = "gpt-4o"

    # Initialize conversation histories
    host_conversation = []
    guest_conversation = []

    # # Generate the host's opening statement
    # host_response = generate_conversation(SAMPLE_TOPIC, PROVIDER, MODEL, create_host_prompt.format(topic=SAMPLE_TOPIC))
    # host_conversation.append(host_response)
    # print("Host:", host_response)

    # # Generate the guest's response
    # guest_response = generate_conversation(SAMPLE_TOPIC, PROVIDER, MODEL, create_guest_prompt.format(topic=SAMPLE_TOPIC))
    # guest_conversation.append(guest_response)
    # print("Guest:", guest_response)

    # Continue the conversation (simulate 20-30 minutes worth of conversation)
    conversation_turns = 20  # Adjust this number based on how long each response is

    # # Start with the initial responses
    # print("Initial conversation:")
    # print("Host:", host_response)
    # print("Guest:", guest_response)

    # # Append initial responses to conversation histories
    # host_conversation.append(host_response)
    # guest_conversation.append(guest_response)

    guest_response = ""
    host_response = ""

    for i in range(conversation_turns):
        print("Conversation turn:", i + 1)  # To display the current turn number

        # Host responds based on the guest's last response
        host_response = generate_conversation(guest_response, PROVIDER, MODEL, create_host_prompt.format(topic=SAMPLE_TOPIC))
        host_conversation.append(host_response)
        print("Host:", host_response)

        # Guest responds based on the host's last response
        guest_response = generate_conversation(host_response, PROVIDER, MODEL, create_guest_prompt.format(topic=SAMPLE_TOPIC))
        guest_conversation.append(guest_response)
        print("Guest:", guest_response)

    # Save conversation histories to files
    host_file_path = os.path.join(OUTPUT_DIR, "host_conversation.txt")
    guest_file_path = os.path.join(OUTPUT_DIR, "guest_conversation.txt")

    with open(host_file_path, "w") as host_file:
        host_file.write("\n".join(host_conversation))

    with open(guest_file_path, "w") as guest_file:
        guest_file.write("\n".join(guest_conversation))

    print(f"Conversations saved to {OUTPUT_DIR}")



    # Generate the combined audio file
    SAMPLE_FILE_NAME = "audio_tts.wav"
    HOST_VOICE = "alloy"
    GUEST_VOICE = "onyx"

    # Run the audio generation
    asyncio.run(generate_combined_audio(host_conversation, guest_conversation, SAMPLE_FILE_NAME, HOST_VOICE, GUEST_VOICE))
