import random
import os
import discord
from discord.ext import commands
from discord import app_commands

# ================= TOKEN =================

TOKEN = os.getenv("BOT_TOKEN")

# ================= INTENTS =================

intents = discord.Intents.default()
intents.message_content = True

# ================= BOT SETUP =================

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# ================= RESPONSE LISTS =================

yes_responses = [
    "Yes",
    "✨ The universe says yes.",
    "Yeah sure why not.",
    "DO IT.",
    "Absolutely.",
    "100% yes.",
    "Honestly? Yeah."
]

no_responses = [
    "No",
    "💀 Absolutely not.",
    "The spirits are screaming no.",
    "This is a terrible idea.",
    "Nope.",
    "Definitely not.",
    "I would not recommend that."
]

choose_styles = [
    lambda choice: f"🎲 {choice}",
    lambda choice: f"⚠️ Fate has chosen: {choice.upper()}",
    lambda choice: f"🌀 The universe demands: {choice}",
    lambda choice: f"Honestly? {choice} sounds funniest.",
    lambda choice: f"✨ Your destiny: {choice}"
]

# ================= READY EVENT =================

@bot.event
async def on_ready():

    print(f"Logged in as {bot.user}")

    # Prevent repeated slash command syncing
    if not hasattr(bot, "synced"):

        try:
            synced = await bot.tree.sync()

            print(f"Synced {len(synced)} command(s)")

            bot.synced = True

        except Exception as e:
            print(f"Sync failed: {e}")

    print("Randall is online.")

# ================= /YESNO =================

@bot.tree.command(
    name="yesno",
    description="Get a random yes or no answer."
)
async def yesno(interaction: discord.Interaction):

    all_responses = yes_responses + no_responses

    response = random.choice(all_responses)

    await interaction.response.send_message(response)

# ================= /CHOOSE =================

@bot.tree.command(
    name="choose",
    description="Choose randomly from comma separated choices."
)
@app_commands.describe(
    choices="Separate choices with commas"
)
async def choose(
    interaction: discord.Interaction,
    choices: str
):

    split_choices = [
        choice.strip()
        for choice in choices.split(",")
        if choice.strip()
    ]

    if len(split_choices) == 0:

        await interaction.response.send_message(
            "You need to provide valid choices.",
            ephemeral=True
        )

        return

    selected_choice = random.choice(split_choices)

    style = random.choice(choose_styles)

    response = style(selected_choice)

    await interaction.response.send_message(response)

# ================= ERROR HANDLING =================

@bot.event
async def on_command_error(ctx, error):

    print(f"Command error: {error}")

# ================= RUN BOT =================

bot.run(TOKEN)