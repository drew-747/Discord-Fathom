import discord
from discord.ext import commands
import asyncio
import os
from datetime import datetime
import openai
from config import *
from user_manager import UserManager
from ai_summarizer import AISummarizer

# Initialize services
user_manager = UserManager()
ai_summarizer = AISummarizer()

# Initialize bot with intents
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

# Store active recordings
active_recordings = {}

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='register')
async def register(ctx, email: str):
    """Register your email for summaries"""
    try:
        success = user_manager.register_user(str(ctx.author.id), email, ctx.author.name)
        if success:
            await ctx.send("Registration successful! You'll receive summaries via email.")
        else:
            await ctx.send("You're already registered or the email is in use.")
    except Exception as e:
        await ctx.send(f"Registration failed: {str(e)}")

@bot.command(name='join')
async def join(ctx):
    """Join the voice channel the user is in"""
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f'Joined {channel.name}')
    else:
        await ctx.send("You need to be in a voice channel!")

@bot.command(name='leave')
async def leave(ctx):
    """Leave the current voice channel"""
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Left the voice channel")
    else:
        await ctx.send("I'm not in a voice channel!")

@bot.command(name='record')
async def record(ctx):
    """Start recording the voice channel"""
    if not ctx.voice_client:
        await ctx.send("I need to be in a voice channel first! Use !join")
        return
    
    if ctx.guild.id in active_recordings:
        await ctx.send("Already recording in this server!")
        return
    
    # Create recording filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{RECORDINGS_DIR}/{ctx.guild.id}_{timestamp}.wav"
    
    # Start recording
    voice_client = ctx.voice_client
    voice_client.start_recording(
        discord.sinks.WaveSink(),
        finished_callback,
        ctx.channel
    )
    
    active_recordings[ctx.guild.id] = {
        'filename': filename,
        'start_time': datetime.now(),
        'channel_id': ctx.channel.id
    }
    
    await ctx.send("Started recording!")

@bot.command(name='stop')
async def stop(ctx):
    """Stop recording and process the audio"""
    if ctx.guild.id not in active_recordings:
        await ctx.send("No active recording in this server!")
        return
    
    if ctx.voice_client:
        ctx.voice_client.stop_recording()
        del active_recordings[ctx.guild.id]
        await ctx.send("Stopped recording! Processing audio...")
    else:
        await ctx.send("I'm not in a voice channel!")

async def finished_callback(sink, channel):
    """Callback when recording is finished"""
    try:
        # Save the recording
        filename = active_recordings[channel.guild.id]['filename']
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Process the audio and generate transcript
        await process_recording(filename, channel)
    except Exception as e:
        await channel.send(f"Error processing recording: {str(e)}")

async def process_recording(filename, channel):
    """Process the recording and generate transcript"""
    try:
        # Transcribe audio
        transcript = await ai_summarizer.transcribe_audio(filename)
        if not transcript:
            await channel.send("Failed to transcribe audio")
            return

        # Save transcript
        transcript_path = ai_summarizer.save_transcript(transcript, str(channel.guild.id))

        # Generate summary
        summary = await ai_summarizer.generate_summary(transcript)
        if not summary:
            await channel.send("Failed to generate summary")
            return

        # Send summary to channel
        await channel.send(f"**Summary:**\n{summary}")

        # Send summary to users via DM and email
        for member in channel.members:
            if not member.bot:
                # Send DM
                try:
                    await member.send(f"**Summary of {channel.name}:**\n{summary}")
                except discord.Forbidden:
                    print(f"Could not send DM to {member.name}")

                # Send email
                user_email = user_manager.get_user_email(str(member.id))
                if user_email:
                    email_content = ai_summarizer.format_summary_email(summary, transcript_path)
                    user_manager.send_email(
                        user_email,
                        f"Summary of {channel.name}",
                        email_content
                    )

    except Exception as e:
        await channel.send(f"Error processing recording: {str(e)}")

@bot.command(name='summarize')
async def summarize(ctx, message_id: int = None):
    """Summarize a specific message or the last recording"""
    if message_id:
        # Summarize specific message
        try:
            message = await ctx.channel.fetch_message(message_id)
            summary = await ai_summarizer.generate_summary(message.content)
            if summary:
                await ctx.send(f"**Summary:**\n{summary}")
            else:
                await ctx.send("Failed to generate summary")
        except discord.NotFound:
            await ctx.send("Message not found!")
    else:
        # Summarize last recording
        await ctx.send("Please specify a message ID to summarize")

# Run the bot
if __name__ == "__main__":
    bot.run(DISCORD_TOKEN) 