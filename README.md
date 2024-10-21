
___
# Podcaster

## Contents
- [Pocast Generator](#podcast-generator)
- [Pexel Video Generator](#pexel-video-generator)


Developed and tested on macOS Sequoia 15.0.1

![macos](https://img.shields.io/badge/mac%20os-000000?style=for-the-badge&logo=apple&logoColor=white)

Listen to our podcast on Spotify!

[![Spotify](https://img.shields.io/badge/Spotify-1ED760?style=for-the-badge&logo=spotify&logoColor=white)](https://podcasters.spotify.com/pod/deon-blaauw6/episodes/)

---

# Podcast Generator

This script generates a podcast episode featuring a conversation between two AI models. It creates both text and audio outputs, along with a summary and relevant hashtags based on the generated dialogue.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Arguments](#arguments)
- [Architecture](#architecture)
- [Functions Overview](#functions-overview)
- [License](#license)

## Features
- Generates a simulated conversation between a host and a guest AI based on a specified topic.
- Supports different Text-to-Speech (TTS) engines (OpenAI and Azure).
- Outputs audio files with background music, enhancing the listening experience.
- Summarizes the dialogue and generates hashtags for social media use.
- Saves all generated outputs to specified directories.

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

You need to set environment variables for the `OPENAI_KEY` and `PEXELS_KEY` API keys:

### Setting Environment Variables

To use the OpenAI and Pexels APIs, you'll need to set the following environment variables in your system:

1. **For macOS and Linux**:
   Open your terminal and add the following lines to your shell configuration file (e.g., `.bashrc`, `.bash_profile`, or `.zshrc`):

   ```bash
   export OPENAI_KEY='your_openai_api_key'
   export PEXELS_KEY='your_pexels_api_key'
   ```

   After adding these lines, run the following command to apply the changes:

   ```bash
   source ~/.bashrc   # or source ~/.zshrc, depending on your shell
   ```

2. **For Windows**:
   Open Command Prompt or PowerShell and set the environment variables using the following commands:

   ```powershell
   setx OPENAI_KEY "your_openai_api_key"
   setx PEXELS_KEY "your_pexels_api_key"
   ```

   After running these commands, restart your Command Prompt or PowerShell session.

## Usage
To run the script, use the following command in your terminal:
```bash
python gen_podcast.py "Your podcast topic" [options]
```

## Arguments
- `topic` (required): The subject matter for the podcast.
- `--tts`: Choose the TTS engine. Options are `openai` or `edge`. Default is `openai`.
- `--landscape`: Optional flag to generate video in landscape mode (default is portrait).
- `--output_dir`: Specify the folder where text files will be saved. Default is `generated_outputs`.
- `--duration`: Approximate length of the podcast in minutes. Default is `20`.

## Architecture
The script is organized into various modules under the `utility` directory, each responsible for specific functionalities:
- **Script Generation**: Contains functions for generating conversations and summarizing dialogues.
- **Audio Generation**: Responsible for creating combined audio files from generated text and adding music tracks.
- **Hashtag Generation**: Generates relevant hashtags based on the conversation content.
- **Utility Functions**: Contains helper functions for saving summaries and managing file paths.

### Flow of Execution
1. **Argument Parsing**: The script starts by parsing command-line arguments.
2. **Conversation Generation**: It generates a conversation by alternating responses between a host and a guest AI.
3. **File Saving**: The generated conversations are saved to text files for both the host and guest.
4. **Dialogue Summary**: A summary of the conversation is created and displayed.
5. **Hashtag Generation**: Relevant hashtags for social media are generated and displayed.
6. **Audio Generation**: Combines the generated text into an audio format using specified TTS engines.
7. **Adding Music**: Background music is added to the audio, creating a cohesive listening experience.

## Functions Overview
- **generate_conversation**: Creates AI-generated responses based on the previous turn's text.
- **summarize_dialog**: Summarizes the entire conversation.
- **create_host_prompt, create_guest_prompt, create_dialog_summary_prompt**: Templates for generating prompts for the host and guest AI.
- **generate_combined_audio**: Combines the host and guest conversations into a single audio file.
- **add_music_with_tts**: Adds background music to the generated audio and handles fade-in/out effects.
- **generate_hashtags**: Generates trending hashtags from the conversation text.
- **save_episode_summary_to_file**: Saves the summary and hashtags to a specified file.

## License
This project is licensed under the MIT License. See the LICENSE file for more information.

---


---

# Pexel Video Generator

This script is designed to generate a video based on a podcast episode, integrating timed captions and background footage sourced from Pexels. The project is experimental and still a work in progress, with ongoing improvements to enhance functionality and stability.

## Table of Contents
- [Features](#features-1)
- [Installation](#installation-1)
- [Usage](#usage-1)
- [Arguments](#arguments-1)
- [Architecture](#architecture-1)
- [Functions Overview](#functions-overview-1)
- [License](#license-1)

## Features
- Generates a video by analyzing audio content and extracting appropriate search keywords for Pexel videos.
- Supports both landscape and portrait video orientations.
- Integrates timed captions from the audio file into the video.
- Downloads background video clips based on generated search terms.

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Install ffmpeg

You need to set environment variables for the `OPENAI_KEY` and `PEXELS_KEY` API keys:

### Setting Environment Variables

To use the OpenAI and Pexels APIs, you'll need to set the following environment variables in your system:

1. **For macOS and Linux**:
   Open your terminal and add the following lines to your shell configuration file (e.g., `.bashrc`, `.bash_profile`, or `.zshrc`):

   ```bash
   export OPENAI_KEY='your_openai_api_key'
   export PEXELS_KEY='your_pexels_api_key'
   ```

   After adding these lines, run the following command to apply the changes:

   ```bash
   source ~/.bashrc   # or source ~/.zshrc, depending on your shell
   ```

2. **For Windows**:
   Open Command Prompt or PowerShell and set the environment variables using the following commands:

   ```powershell
   setx OPENAI_KEY "your_openai_api_key"
   setx PEXELS_KEY "your_pexels_api_key"
   ```

   After running these commands, restart your Command Prompt or PowerShell session.

## Usage
To run the script, use the following command in your terminal:
```bash
python gen_pexel_video.py [options]
```

## Arguments
- `--landscape`: Optional flag to generate video in landscape mode (default is portrait).
- `--output_dir`: Specify the folder where output files will be saved. Default is `generated_outputs`.
- `--input_file`: Input audio file (e.g., the output from `gen_podcast.py`) that this script will use to generate the video. Default is `final_output.mp3`.

## Architecture
The script is organized into various modules under the `utility` directory, each responsible for specific functionalities related to video generation:
- **Timed Captions**: Generates timed captions from the input audio.
- **Video Search Query Generation**: Extracts relevant search queries based on the conversation text and timed captions.
- **Background Video Generation**: Retrieves URLs for background videos from Pexels based on the search queries.
- **Render Engine**: Combines all elements (audio, captions, video) into the final output media.

### Flow of Execution
1. **Argument Parsing**: The script starts by parsing command-line arguments.
2. **Reading Previous Output**: It reads the total conversation from a specified file.
3. **Generating Timed Captions**: The script generates timed captions from the input audio file.
4. **Extracting Search Queries**: Based on the conversation and captions, it generates search terms for video retrieval.
5. **Retrieving Background Video URLs**: It fetches URLs for background videos from Pexels using the generated search terms.
6. **Merging Intervals**: If necessary, it merges empty intervals in the video URLs.
7. **Generating Output Video**: Combines the audio, captions, and background video into the final output.

## Functions Overview
- **generate_timed_captions**: Creates timed captions from the input audio file.
- **getVideoSearchQueriesTimed**: Extracts search terms based on conversation text and timed captions.
- **generate_video_url**: Retrieves background video URLs from Pexels based on search terms.
- **merge_empty_intervals**: Merges empty intervals in the list of video URLs for better coherence.
- **get_output_media**: Combines audio, captions, and video into the final media output.

## Experimental Note
This code is currently experimental and still a work in progress. Expect ongoing changes and updates as features are refined and new functionalities are implemented. Your feedback is appreciated!

## License
This project is licensed under the MIT License. See the LICENSE file for more information.

---

