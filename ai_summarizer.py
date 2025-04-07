import openai
from config import *
import os
from datetime import datetime

class AISummarizer:
    def __init__(self):
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)

    async def transcribe_audio(self, audio_file_path: str) -> str:
        """Transcribe audio file using OpenAI Whisper"""
        try:
            with open(audio_file_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
            return transcript.text
        except Exception as e:
            print(f"Error transcribing audio: {str(e)}")
            return None

    async def generate_summary(self, text: str) -> str:
        """Generate summary using GPT"""
        try:
            response = self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes conversations. Focus on key points, decisions, and action items."},
                    {"role": "user", "content": f"Please summarize the following conversation:\n\n{text}"}
                ],
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating summary: {str(e)}")
            return None

    def save_transcript(self, transcript: str, guild_id: str) -> str:
        """Save transcript to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{TRANSCRIPTS_DIR}/{guild_id}_{timestamp}.txt"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(transcript)
        
        return filename

    def format_summary_email(self, summary: str, transcript_path: str) -> str:
        """Format summary for email"""
        return f"""Here's your conversation summary:

{summary}

The full transcript is available at: {transcript_path}

Thank you for using Discord-Fathom!
""" 