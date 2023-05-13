import discord
from discord import ui, app_commands, AppCommandOptionType
from discord.ext import commands

TOKEN = "MTAzNzYyOTMyMDIwMzYxNjI2Ng.GhpR78.NzFqeGnDD0IZdQCArpLiL5CSAmdLtPUZ0fvIuo"
bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())

@bot.event
async def on_ready():
    synced = await bot.tree.sync()
    print("NUM SYNCED: " + str(len(synced)))
    

@bot.tree.command(name="complete", description="Submit verification of a completed mission to earn XP")
@app_commands.choices(choices=[app_commands.Choice(name="quest_id", value="quest_id")])
@app_commands
@app_commands.option(name="file", description="File of the mission", type=AppCommandOptionType.attachment, required=True)
## the complete command takes in a mission ID and a description of the mission, and upload file
async def mission(interaction: discord.Interaction, choices:app_commands.Choice[str], description:app_commands.Option[str], file:app_commands.Option[discord.File]):
    ## add a command option, mission ID, from a list of mission IDs
    ## send a message in the mission-complete channel with the mission ID, description, and file
    await discord.utils.get(interaction.guild.channels, name="mission-complete").send("Mission ID: " + choices + "\nDescription: " + description + "\nFile: " + file.url)
    

bot.run(TOKEN) 