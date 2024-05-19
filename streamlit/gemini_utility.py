import os
import json
from PIL import Image
import google.generativeai as genai

# working directory path
working_dir = os.path.dirname(os.path.abspath(__file__))

# path of config_data file
config_file_path = os.path.join(working_dir, 'config.json')

# Ensure the config file exists
if not os.path.exists(config_file_path):
    raise FileNotFoundError(f"Config file not found: {config_file_path}")

# Load config data
with open(config_file_path, 'r') as config_file:
    config_data = json.load(config_file)

# loading the GOOGLE_API_KEY
GOOGLE_API_KEY = config_data.get("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in the config file")

# configuring google.generativeai with API key
genai.configure(api_key=GOOGLE_API_KEY)

# get response from Gemini-Pro model - text to text
def gemini_pro_response(user_prompt):
    gemini_pro_model = genai.GenerativeModel("gemini-pro")
    response = gemini_pro_model.generate_content(user_prompt)
    result = response.text
    return result
