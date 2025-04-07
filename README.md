# Discord-Fathom

A Discord bot that records, transcribes, and summarizes voice channel conversations, similar to Fathom AI.

## Features

- Join voice channels and record conversations
- Automatic transcription of voice recordings
- AI-powered summaries of conversations
- Message summarization
- Email notifications of summaries
- Direct Message notifications
- User account management
- Easy-to-use commands

## Setup

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your credentials:
```
DISCORD_TOKEN=your_discord_bot_token
OPENAI_API_KEY=your_openai_api_key
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_app_specific_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

4. Run the bot:
```bash
python bot.py
```

## Commands

- `!register <email>` - Register your email to receive summaries
- `!join` - Join the voice channel you're in
- `!leave` - Leave the current voice channel
- `!record` - Start recording the voice channel
- `!stop` - Stop recording and process the audio
- `!summarize [message_id]` - Summarize a specific message or the last recording

## Requirements

- Python 3.8+
- FFmpeg installed on your system
- Discord Bot Token
- OpenAI API Key
- Email account for notifications (Gmail recommended)

## Notes

- The bot requires proper permissions in your Discord server
- Make sure to install FFmpeg for audio processing
- The bot uses OpenAI's Whisper for transcription and GPT for summarization
- For Gmail, you'll need to use an App Password for email notifications
- Users must register their email to receive email notifications

## License

MIT License 