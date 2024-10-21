import argparse
from utility.script.script_generator import generate_conversation, summarize_dialog
from utility.script.prompts import create_host_prompt, create_guest_prompt, create_dialog_summary_prompt
from utility.audio.audio_generator import generate_combined_audio, add_music_with_tts
from utility.script.hashtag_generator import generate_hashtags
from utility.utils import save_episode_summary_to_file


# video generation
from utility.captions.timed_captions_generator import generate_timed_captions
from utility.video.video_search_query_generator import getVideoSearchQueriesTimed, merge_empty_intervals
from utility.video.background_video_generator import generate_video_url
from utility.render.render_engine import get_output_media

import os
import asyncio

if __name__ == "__main__":
    # Argument parsing to include landscape/portrait option and output filename
    parser = argparse.ArgumentParser(description="Generate a podcast interview between two AIs.")
    parser.add_argument("--landscape", action='store_false', help="Generate video in landscape mode (default is portrait)")
    parser.add_argument("--output_dir", type=str, default="generated_outputs", help="Folder where text files are stored. Default is generated_outputs")
    parser.add_argument("--input_file", type=str, default="final_output.mp3", help="Input audio file that this script will add a video to by analyzing the audio content and finding apporiate search keywords for Pexel videos")

    args = parser.parse_args()
    # SAMPLE_TOPIC = args.topic
    OUTPUT_DIR = args.output_dir
    INPUT_FILE = args.input_file

    # Ensure the output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    PROVIDER = "openai"
    MODEL = "gpt-4o"

    LANDSCAPE = args.landscape 
    print("LANDSCAPE: ", LANDSCAPE)

    # Video code
    total_response = ""
    total_chat_file_path = os.path.join(OUTPUT_DIR, "total_conversation.txt")
    with open(total_chat_file_path, "r") as total_chat_file:
        total_response = total_chat_file.read()


    # Get timed captions from the audio
    timed_captions = generate_timed_captions(INPUT_FILE)
    print(timed_captions)

    search_terms = getVideoSearchQueriesTimed(total_response, timed_captions, PROVIDER, MODEL)
    print(search_terms)

    # Video URL retrieval
    VIDEO_SERVER = "pexel"      
    LANDSCAPE = args.landscape 
    print("LANDSCAPE: ", LANDSCAPE)
    background_video_urls = None
    if search_terms is not None:
        background_video_urls = generate_video_url(search_terms, VIDEO_SERVER, orientation_landscape=LANDSCAPE)
        print(background_video_urls)
    else:
        print("No background video")

    # Video downloading ...
    MUSIC_VOLUME_MP3 = 0.08
    MUSIC_VOLUME_WAV = 0.5
    VOLUME_TTS = 1.0

    if background_video_urls is not None:
        background_video_urls = merge_empty_intervals(background_video_urls)
        if background_video_urls is not None:
            video = get_output_media(total_response, INPUT_FILE, timed_captions, background_video_urls, VIDEO_SERVER, LANDSCAPE, MUSIC_VOLUME_WAV, MUSIC_VOLUME_MP3, VOLUME_TTS, OUTPUT_DIR)
            print(video)
        else:
            print("No background video after merging intervals")
    else:
        print("No background video")    