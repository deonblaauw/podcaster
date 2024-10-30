import argparse
from utility.script.script_generator import generate_conversation, summarize_dialog
from utility.script.prompts import create_host_prompt, create_guest_prompt, create_dialog_summary_prompt
from utility.audio.audio_generator import generate_combined_audio, add_music_with_tts
from utility.script.hashtag_generator import generate_hashtags
from utility.utils import save_episode_summary_to_file

import os
import asyncio
import random

# Usage: python gen_podcast.py "Your podcast topic"

if __name__ == "__main__":
    # Argument parsing to include landscape/portrait option and output filename
    parser = argparse.ArgumentParser(description="Generate a podcast interview between two AIs.")
    parser.add_argument("topic", type=str, help="The topic for the podcast")
    parser.add_argument("--tts", type=str, default="openai", help="Text to speech engine. Options are openai or edge. Default is openai")
    parser.add_argument("--landscape", action='store_true', help="Generate video in landscape mode (default is portrait)")
    parser.add_argument("--output_dir", type=str, default="generated_outputs", help="Folder where text files are stored. Default is generated_outputs")
    parser.add_argument("--duration", type=int, default=20, help="Length (roughly), in minutes, of the podcast. Default is 20 minutes")


    args = parser.parse_args()
    SAMPLE_TOPIC = args.topic
    OUTPUT_DIR = args.output_dir
    DURATION = args.duration

    print("Duration: " + str(DURATION) + " minutes")
    print("Output Directory: " + str(OUTPUT_DIR))
    print("Generating conversation on topic:", str(SAMPLE_TOPIC))

    # Ensure the output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    PROVIDER = "openai"
    MODEL = "gpt-4o"

    # Initialize conversation histories
    host_conversation = []
    guest_conversation = []

    # Continue the conversation (simulate 20-30 minutes worth of conversation)
    # conversation_turns == 4  is ~10 minutes
    # conversation_turns == 8  is ~20 minutes
    # conversation_turns == 16 is ~40 minutes
    conversation_turns = int(DURATION / 2.0)  # Adjust this number based on how long each response is

    guest_response = ""
    host_response = ""
    total_response = ""

    for i in range(conversation_turns):
        print("Conversation turn:", i + 1)  # To display the current turn number

        # Host responds based on the guest's last response
        temperature = random.uniform(0.5, 0.9)
        host_response = generate_conversation(guest_response, PROVIDER, MODEL, create_host_prompt.format(topic=SAMPLE_TOPIC), temperature)
        host_conversation.append(host_response)
        total_response += "Host: " + host_response + "\n"
        print("\nHost Temperature: {" + str(temperature) + "} Response: " + host_response)

        # Guest responds based on the host's last response
        temperature = random.uniform(0.5, 0.9)
        guest_response = generate_conversation(host_response, PROVIDER, MODEL, create_guest_prompt.format(topic=SAMPLE_TOPIC), temperature)
        guest_conversation.append(guest_response)
        total_response += "Guest: " + guest_response + "\n"
        print("\nGuest Temperature: {" + str(temperature) + "} Response: " + guest_response)

    # Save conversation histories to files
    host_file_path = os.path.join(OUTPUT_DIR, "host_conversation.txt")
    guest_file_path = os.path.join(OUTPUT_DIR, "guest_conversation.txt")
    total_chat_file_path = os.path.join(OUTPUT_DIR, "total_conversation.txt")

    with open(host_file_path, "w") as host_file:
        host_file.write("\n".join(host_conversation))

    with open(guest_file_path, "w") as guest_file:
        guest_file.write("\n".join(guest_conversation))

    with open(total_chat_file_path, "w") as total_chat_file:
        total_chat_file.write(total_response)

    print(f"Conversations saved to {OUTPUT_DIR}")

    # Video description
    dialog_summary = summarize_dialog(total_response, SAMPLE_TOPIC, PROVIDER, MODEL, create_dialog_summary_prompt.format(topic=SAMPLE_TOPIC))
    print("Dialog summary:")
    print(dialog_summary)
    vid_hashtags = generate_hashtags(total_response, PROVIDER, MODEL)
    print("trends: {}".format(vid_hashtags))

    # Save response and hashtags to a file
    save_episode_summary_to_file(SAMPLE_TOPIC, dialog_summary, vid_hashtags, OUTPUT_DIR)
    
    # Generate the combined audio file
    SAMPLE_FILE_NAME = "audio_tts.wav"
    TTS_ENGINE = args.tts

    if TTS_ENGINE == "openai":
        HOST_VOICE = "alloy"
        GUEST_VOICE = "onyx" #"onyx"
    elif TTS_ENGINE == "edge":
        HOST_VOICE = "en-AU-NatashaNeural"
        GUEST_VOICE = "en-AU-WilliamNeural"
    else:
        raise ValueError("No viable TTS engine option found, please provide a valid TTS engine option.")
    
        
    # Run the audio generation
    asyncio.run(generate_combined_audio(host_conversation, guest_conversation, SAMPLE_FILE_NAME, HOST_VOICE, GUEST_VOICE , TTS_ENGINE))


    # Add music
    intro_music_path = "utility/music/in-slow-motion-inspiring-ambient-lounge-219592.mp3"
    main_tts_path = SAMPLE_FILE_NAME
    outro_music_path = "utility/music/in-slow-motion-inspiring-ambient-lounge-219592.mp3"
    output_path = "final_output.mp3"
   
    add_music_with_tts(intro_music_path, main_tts_path, outro_music_path, output_path, fade_duration=2.0, music_intro_duration=20.0 , music_outro_duration=30.0)