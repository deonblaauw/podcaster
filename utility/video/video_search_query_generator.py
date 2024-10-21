from openai import OpenAI
import os
import json
import re
from datetime import datetime
from utility.utils import log_response,LOG_TYPE_GPT , fix_json_content , fix_json , fix_quotes
from utility.script.prompts import timed_captions_prompt

log_directory = ".logs/gpt_logs"


def getVideoSearchQueriesTimed(script, captions_timed, provider, model):
    end = captions_timed[-1][0][1]
    try:
        out = [[[0, 0], ""]]  # Initialize output with a placeholder
        
        while out[-1][0][1] != end:
            content = call_OpenAI(script, captions_timed, provider, model)  # Fetch content
            
            # Step 1: Fix common JSON formatting issues
            content = fix_json(content)
            
            # Step 2: Handle additional content-specific issues
            content = fix_json_content(content)
            
            try:
                # Try parsing the content as JSON
                out = json.loads(content)
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
                print("Original content: \n", content, "\n\n")
                
                # Step 3: Remove formatting artifacts like markdown (```json blocks)
                content = content.replace("```json", "").replace("```", "")
                
                # Step 4: Attempt fixing problematic quotes again
                fixed_content = fix_quotes(content)
                print("Fixed content: \n", fixed_content, "\n\n")
                
                try:
                    # Try parsing the cleaned-up content again
                    out = json.loads(fixed_content)
                except json.JSONDecodeError as e_inner:
                    print(f"Still failing after fix: {e_inner}")
                    return None
        
        # If everything works, return the parsed JSON
        return out
    except Exception as e:
        # Generic error handler
        print(f"Error in response: {e}")
        return None




def call_OpenAI(script,captions_timed, provider, model):

    if provider == "groq":
        from groq import Groq
        client = Groq(
            api_key=os.environ.get("GROQ_API_KEY"),
            )
    elif provider == "openai":
        OPENAI_API_KEY = os.getenv('OPENAI_KEY')
        client = OpenAI(api_key=OPENAI_API_KEY)
    else:
        print("[ERROR] No valid provider specified")

    user_content = """Script: {}
Timed Captions:{}
""".format(script,"".join(map(str,captions_timed)))
    print("Content", user_content)
    
    response = client.chat.completions.create(
        model= model,
        temperature=1,
        messages=[
            {"role": "system", "content": timed_captions_prompt},
            {"role": "user", "content": user_content}
        ]
    )
    
    text = response.choices[0].message.content.strip()
    text = re.sub('\s+', ' ', text)
    print("Text", text)
    log_response(LOG_TYPE_GPT,script,text)
    return text

def merge_empty_intervals(segments):
    merged = []
    i = 0
    while i < len(segments):
        interval, url = segments[i]
        if url is None:
            # Find consecutive None intervals
            j = i + 1
            while j < len(segments) and segments[j][1] is None:
                j += 1
            
            # Merge consecutive None intervals with the previous valid URL
            if i > 0:
                prev_interval, prev_url = merged[-1]
                if prev_url is not None and prev_interval[1] == interval[0]:
                    merged[-1] = [[prev_interval[0], segments[j-1][0][1]], prev_url]
                else:
                    merged.append([interval, prev_url])
            else:
                merged.append([interval, None])
            
            i = j
        else:
            merged.append([interval, url])
            i += 1
    
    return merged
