import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Email configuration
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
EMAIL_USERNAME = os.getenv('EMAIL_USERNAME')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

# Bot settings
COMMAND_PREFIX = '!'
MAX_RECORDING_DURATION = 3600  # Maximum recording duration in seconds (1 hour)
RECORDINGS_DIR = 'recordings'
TRANSCRIPTS_DIR = 'transcripts'

# OpenAI settings
MODEL_NAME = "gpt-4-turbo-preview"  # or "gpt-3.5-turbo" for faster/cheaper
MAX_TOKENS = 2000
TEMPERATURE = 0.7

# Create directories if they don't exist
os.makedirs(RECORDINGS_DIR, exist_ok=True)
os.makedirs(TRANSCRIPTS_DIR, exist_ok=True) 