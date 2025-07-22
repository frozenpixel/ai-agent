import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

try:
    prompt = sys.argv[1]
except Exception:
    sys.exit("No prompt given. Example: <file> <prompt>")

try:
    if sys.argv[2] == "--verbose":
        verbose = True
except Exception:
    verbose = False

messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),
]
    
response = client.models.generate_content(
    model='gemini-2.0-flash-001', 
    contents=messages,
    )

if verbose == True:
    print(f"User prompt: {response.text}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")