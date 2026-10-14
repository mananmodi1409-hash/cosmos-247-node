import subprocess
import sys
import os

# --- AUTOMATED PACKAGE INSTALLER ---
try:
    import discord
    from discord.ext import commands
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "discord.py"])
    import discord
    from discord.ext import commands

import urllib.request
import json

# --- CONFIGURATION LOGS ---
SLANG_BLACKLIST = ["toxic", "trash", "fool", "nonsense"]
user_xp_database = {}

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

def ask_cloud_brain(prompt_context):
    """Uses a free cloud infrastructure link to summarize text while your PC is off."""
    try:
        # We target a highly stable, free API endpoint cluster for cloud execution
        url = "https://pollinations.ai"
        payload = {
            "messages": [
                {"role": "system", "content": "You are C.O.S.M.O.S., an elite server operations AI. Provide a sharp summary under 3 sentences."},
                {"role": "user", "content": prompt_context}
            ],
            "stream": False
        }
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as res:
            # Clean up raw stream variables returned from the cluster
            return res.read().decode('utf-8').strip()
    except:
        return "The primary cloud repository matrix is busy. Standard protocols handling channel summary layouts."

@bot.event
async def on_ready():
    print(f"====================================================")
    print(f" 🎉 C.O.S.M.O.S. CLOUD MATRIX IS ACTIVE: {bot.user.name}")
    print(f"====================================================")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # 🛡️ MODULE 1: THE SLANG CENSOR FILTER
    message_content_lower = message.content.lower()
    if any(slang in message_content_lower for slang in SLANG_BLACKLIST):
        try:
            await message.delete()
            await message.channel.send(f"⚠️ {message.author.mention}, your transmission has been neutralized under community safety matrix parameters.")
            return
        except:
            return

    # 📈 MODULE 2: AUTOMATED LEVELING XP MATRIX
    user_id = str(message.author.id)
    if user_id not in user_xp_database:
        user_xp_database[user_id] = {"xp": 0, "level": 1}
    
    user_xp_database[user_id]["xp"] += 10
    needed_xp = user_xp_database[user_id]["level"] * 100
    
    if user_xp_database[user_id]["xp"] >= needed_xp:
        user_xp_database[user_id]["level"] += 1
        user_xp_database[user_id]["xp"] = 0
        await message.channel.send(f"⚡ **LEVEL UP**: {message.author.mention}! Your server placement matrix reached **Level {user_xp_database[user_id]['level']}**!")

    await bot.process_commands(message)

# 🎙️ MODULE 3: CHAT CHANNEL SUMMARY COMMAND
@bot.command(name="summary")
async def summarize_channel(ctx, limit: int = 25):
    try:
        await ctx.send("🔄 *Extracting data layers from channel text logs...*")
        gathered_text = ""
        async for msg in ctx.channel.history(limit=limit, oldest_first=False):
            if not msg.author.bot and msg.content:
                gathered_text += f"{msg.author.display_name}: {msg.content}\n"
                
        if not gathered_text.strip():
            await ctx.send("❌ Data stream empty. No valid text logs found.")
            return
            
        ai_summary = ask_cloud_brain(gathered_text)
        await ctx.send(f"📋 **[C.O.S.M.O.S. REPOSITORY SUMMARY]**:\n{ai_summary}")
    except Exception as e:
        await ctx.send(f"⚠️ Telemetry interrupt: {str(e)}")

# --- LAUNCH ENGINE FROM ENVIRONMENT ---
# Render will securely inject your token into your environment parameters automatically
TOKEN = os.environ.get("DISCORD_TOKEN")
if TOKEN:
    bot.run(TOKEN)
else:
    # Local fallback for testing inside Visual Studio
    bot.run("YOUR_DISCORD_BOT_TOKEN_HERE")
