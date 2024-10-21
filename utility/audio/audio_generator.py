# import edge_tts
import requests
import os
import random
from moviepy.editor import AudioFileClip, concatenate_audioclips, CompositeAudioClip

def add_music_with_tts(intro_music_path, main_tts_path, outro_music_path, output_path, fade_duration=2.0, music_intro_duration=10.0, music_outro_duration=10.0):
    """Add background music with TTS audio, ensuring smooth transitions.
    
    Args:
        intro_music_path (str): Path to the intro music MP3 file.
        main_tts_path (str): Path to the main TTS audio MP3 file.
        outro_music_path (str): Path to the outro music MP3 file.
        output_path (str): Path to save the final output audio.
        fade_duration (float): Duration for fade in/out effects in seconds.
        music_intro_duration (float): Duration of the music-only intro section before TTS fades in.
        music_outro_duration (float): Duration of the music-only outro section after TTS fades out.
    """

    # Load intro music, make it fade out at the end
    intro_music = AudioFileClip(intro_music_path).volumex(0.1)
    intro_music = intro_music.subclip(0, music_intro_duration).audio_fadeout(fade_duration)

    # Load TTS audio at full volume
    main_tts_audio = AudioFileClip(main_tts_path).volumex(1.0)

    # Load outro music and make it fade in at the beginning
    outro_music = AudioFileClip(outro_music_path).volumex(0.1)
    outro_music = outro_music.subclip(0, music_outro_duration).audio_fadein(fade_duration)

    # Create the intro section (music fading out and TTS audio fading in)
    intro_with_tts = CompositeAudioClip([
        intro_music,
        main_tts_audio.set_start(music_intro_duration - fade_duration)  # Fade TTS in just before the intro music fades out
    ])

    # Outro: TTS audio fades out while outro music fades in
    tts_faded_out = main_tts_audio.audio_fadeout(fade_duration)
    outro_with_tts = CompositeAudioClip([
        tts_faded_out,
        outro_music.set_start(main_tts_audio.duration - fade_duration)  # Fade in outro music before TTS ends
    ])

    # Concatenate intro_with_tts (intro + full TTS) and outro_with_tts
    final_audio = concatenate_audioclips([intro_with_tts, outro_with_tts])

    # Write the result to a file
    final_audio.write_audiofile(output_path)















# async def generate_audio_edge(text, outputFilename, voice):
    
#     available_voices = [
#     "en-AU-NatashaNeural",
#     "en-AU-WilliamNeural",
#     "en-CA-ClaraNeural",
#     "en-CA-LiamNeural",
#     "en-HK-SamNeural",
#     "en-HK-YanNeural",
#     "en-IN-NeerjaNeural",
#     "en-IN-PrabhatNeural",
#     "en-IE-ConnorNeural",
#     "en-IE-EmilyNeural",
#     "en-KE-AsiliaNeural",
#     "en-KE-ChilembaNeural",
#     "en-NZ-MitchellNeural",
#     "en-NZ-MollyNeural",
#     "en-NG-AbeoNeural",
#     "en-NG-EzinneNeural",
#     "en-PH-JamesNeural",
#     "en-PH-RosaNeural",
#     "en-SG-LunaNeural",
#     "en-SG-WayneNeural",
#     "en-ZA-LeahNeural",
#     "en-ZA-LukeNeural",
#     "en-TZ-ElimuNeural",
#     "en-TZ-ImaniNeural",
#     "en-GB-LibbyNeural",
#     "en-GB-MaisieNeural",
#     "en-GB-RyanNeural",
#     "en-GB-SoniaNeural",
#     "en-GB-ThomasNeural",
#     "en-US-AriaNeural",
#     "en-US-AnaNeural",
#     "en-US-ChristopherNeural",
#     "en-US-EricNeural",
#     "en-US-GuyNeural",
#     "en-US-JennyNeural",
#     "en-US-MichelleNeural",
#     "en-US-RogerNeural",
#     "en-US-SteffanNeural"
#     ]

#     # Check if the provided voice is valid; if not, choose a random one
#     if voice not in available_voices:
#         voice = random.choice(available_voices)
#         print(f"No voice specified by user. Using random voice: {voice}")

    
#     communicate = edge_tts.Communicate(text, voice)


#     await communicate.save(outputFilename)

# Async function to generate audio using OpenAI TTS
async def generate_audio_openai(text, outputFilename, voice):
    api_key = os.getenv("OPENAI_API_KEY")  # Ensure your API key is stored in an environment variable
    url = "https://api.openai.com/v1/audio/speech"

    # List of available voices
    available_voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]

    # Check if the provided voice is valid; if not, choose a random one
    if voice not in available_voices:
        voice = random.choice(available_voices)
        print(f"No voice specified by user. Using random voice: {voice}")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "tts-1",
        "input": text,
        "voice": voice  # Use the validated or random voice
    }

    # Make a POST request to OpenAI API
    response = requests.post(url, headers=headers, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        # Save the audio to the output file
        with open(outputFilename, "wb") as audio_file:
            audio_file.write(response.content)
        print(f"Audio generated and saved as '{outputFilename}'")
    else:
        # Handle API errors
        print(f"Failed to generate audio. Status code: {response.status_code}")
        print(f"Response: {response.text}")



from moviepy.editor import concatenate_audioclips, AudioFileClip
import asyncio
import os



async def generate_combined_audio(host_responses, guest_responses, sample_file_name, host_voice, guest_voice):
    # List to hold the paths of temporary WAV files
    temp_wav_files = []

    # Generate audio for each response and save as temporary WAV files
    for index, (host_response, guest_response) in enumerate(zip(host_responses, guest_responses)):
        # Generate host audio
        host_file_name = f'temp_host_{index}.wav'
        await generate_audio_openai(host_response, host_file_name, host_voice)
        temp_wav_files.append(host_file_name)

        # Generate guest audio
        guest_file_name = f'temp_guest_{index}.wav'
        await generate_audio_openai(guest_response, guest_file_name, guest_voice)
        temp_wav_files.append(guest_file_name)

    # Concatenate all temporary audio files into a single output file
    concatenate_audio_moviepy(temp_wav_files, sample_file_name)

    # Clean up temporary files
    for file in temp_wav_files:
        os.remove(file)

def concatenate_audio_moviepy(audio_clip_paths, output_path):
    """Concatenates several audio files into one audio file using MoviePy
    and save it to `output_path`. Note that extension (mp3, etc.) must be added to `output_path`"""
    clips = [AudioFileClip(c) for c in audio_clip_paths]
    final_clip = concatenate_audioclips(clips)
    final_clip.write_audiofile(output_path)



