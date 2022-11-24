import discord
from discord import ui
from discord.ext import commands
from discord import Button, ButtonStyle
import api as api
import random 
import requests
import asyncio
import io

TOKEN = "MTAzNzYyOTMyMDIwMzYxNjI2Ng.GhpR78.NzFqeGnDD0IZdQCArpLiL5CSAmdLtPUZ0fvIuo"
client = discord.Client(intents=discord.Intents.all())
BOT_ROLE = "Bot"
ADMIN_ROLE = "Admin"
JACKPOT_ROLE = "Jackpot"

def getRaidsEmbed():
    embed=discord.Embed(title="Sample Embed", url="https://realdrewdata.medium.com/", description="This is an embed that will show how to build an embed and the different components", color=0x109319)
    embed.set_author(name="RealDrewData", url="https://twitter.com/RealDrewData", icon_url="https://pbs.twimg.com/profile_images/1327036716226646017/ZuaMDdtm_400x400.jpg")
    embed.set_thumbnail(url="https://i.imgur.com/axLm3p6.jpeg")
    embed.add_field(name="Field 1 Title", value="This is the value for field 1. This is NOT an inline field.", inline=False) 
    embed.add_field(name="Field 2 Title", value="It is inline with Field 3", inline=True)
    embed.add_field(name="Field 3 Title", value="It is inline with Field 2", inline=True)
    embed.set_footer(text="This is the footer. It contains text at the bottom of the embed")
    return embed
    
def getGettingStartedEmbed():
    embed=discord.Embed(title="Get Started 🚀", description="We take data privacy very seriously. To begin earning XP, you must opt-in and connect your Twitter.", color=0xff6969)
    embed.set_author(name="Jackpot", url="https://getjackpot.xyz", icon_url="https://static.wixstatic.com/media/cdc018_a8e52bee9e114aa9a11355686b703954~mv2.png")
    embed.set_thumbnail(url="https://static.wixstatic.com/media/cdc018_a8e52bee9e114aa9a11355686b703954~mv2.png")
    embed.add_field(name="Opt-In", value="Navigate to #opt-in and follow the relevant instructions to start earning XP. Once you do this, you will not have to do it again.", inline=False) 
    embed.add_field(name="First Tweet Raid", value="Navigate to #raids to engage with tweets and earn XP.", inline=False) 
    embed.set_footer(text="⚠️ Failing to Opt-In will mean you will not be able to earn XP.")
    return embed

def getUpcomingJackpotsEmbed():
    embed=discord.Embed(title="Upcoming Jackpot💰", description="** **💰 Current Jackpot Size: `1,000 USDC` | ⏱️ Time Until Next Drawing: `24 Days`\n✋ # of Community Participants: `65` | ✋ # of Global Participants: `195`\n🎟️ **1 XP = 1 Raffle Ticket**", color=0xe9e9e9)
    return embed

def getLeaderboardsEmbed():
    embed=discord.Embed(title="Leaderboards 📈", color=0xe9e9e9)
    embed.add_field(name="**Full Leaderboard on our website**", value="🌐 __[Community Leaderboard](https://getjackpot.xyz/leaderboard/doodles/)__\n🌐 __[Global Leaderboard](https://getjackpot.xyz/leaderboard/)__", inline=False) 
    return embed

def getIntroEmbed():
    embed = discord.Embed(title="**Welcome to Jackpot**", description="Earn XP to climb the leaderboard and have a chance at winning **The Jackpot**: a portion of our revenue. **1 XP = 1 Raffle Ticket.**", color=0xe9e9e9)
    return embed
    
def getXPEmbed():
    embed=discord.Embed(title="**🎟️ How to Earn XP 🎟️**", description="Here's a guide to all the ways you can get rewarded for your participation in this community.", color=0xe9e9e9)
    embed.add_field(name="**Discord:**", value="🎟️ Sending messages *(diminishing returns)* : `+40 xp`\n🎟️ Reacting to messages *(diminishing returns)* : `+15 xp`\n🎟️ Other people reacting to your messages: `+200 xp`\n🎟️ Other people replying to your messages: `+500 xp`\n🎟️ Being one of the first people to interact with a new member: `+800 xp`\n🎟️ Inviting real human people to the server: `+700 xp`\n🎟️ Visiting the server daily: `+150 xp`\n", inline=False) 
    embed.add_field(name="**Twitter:**", value = "🎟️ Retweeting a `#raids` tweet: `+600 xp`\n🎟️ Replying to a `#raids` tweet: `+400 xp`\n🎟️ Liking a `#raids` tweet: `+200 xp`\n🎟️ Following other community members: `+400 xp`\n🎟️ Being followed by other community members: `+1000 xp`\n", inline=False) 
    embed.add_field(name="**Missions:**", value = "🎟️ Successfully completing `#missions`: `xp varies`", inline=False)
    return embed

def getChannelsEmbed():
    embed=discord.Embed(title="**Channel Overview", color=0xe9e9e9)
    embed.add_field(name="Important channels to keep track of:", value="📍 `#opt-in` | Verify your Twitter and wallet address to begin earning XP.\n📍 `#leaderboard` | Find the community’s most valuable contributors.\n📍 `#raids` | Participate in Twitter raids to earn XP.\n📍 `#missions` | Choose from the available missions.\n📍 `#mission-complete` | Submit proof of mission completion to earn XP.\n📍 `#xp-log` | Receive notifications when you earn XP.")
    return embed

def getWelcomeEmbed():
    embed=discord.Embed(title="**Welcome to Jackpot**",description="Jackpot is a simple, no-brainer loyalty and rewards program architected in collaboration with 100+ web3 industry veterans including founders, community managers, mods, and core contributors across the Ethereum and Solana ecosystems.\n\nOpt in to immediately earn `1000 XP` 🎟️ and have a chance at winning the next the Jackpot.", color=0xe9e9e9)
    return embed

def getTwitterOAUTHEmbed():
    embed=discord.Embed(title="__**Verify Twitter Account Ownership**__", description="To opt-in, you must link your Twitter account. Follow the steps below to get your Twitter OAUTH code", color=0x1da1f2)
    embed.add_field(name="**Steps:**", value = "\n1. Go to the [Twitter OAuth Authorization](https://twitter.com/home) page and authorize the app using your Twitter account.\n2. Copy the *one-time pincode* provided and submit it via the ‘Link Twitter’ button below.", inline=False)
    return embed

def getMissionsEmbed():
    embed=discord.Embed(title="Missions 🗺️", description = "Missions are the easiest way to rack up XP.  Head over to `#missions` to view the available missions. Submit proof of your work in `#missions-complete`, and once approved by your community's admin, you'll receive XP for your contribution.", color=0xe9e9e9)
    return embed

def getCommandsEmbed():
    embed=discord.Embed(title="**🤖 Discord Commands 🤖**", description = "👉 *Type `!rank ` to see your own stats.*\n👉 *Type `!rank/username` to see someone else's stats.*\n👉 *Type `!leaderboard ` to preview the Community Leaderboard.*\n👉 *Type `!global ` to preview the Global Leaderboard.*\n👉 *Type `!jackpot ` to see the upcoming Jackpot.", color=0xe9e9e9)
    return embed

def getLeaderboardInformation():
    string = "** **\n** **📈 💰  __**[Doodles Community Leaderboard](https://getjackpot.xyz/leaderboard/doodles/)**__ 💰 📈\n🏘️  *[Community Leaderboard](https://getjackpot.xyz/leaderboard/doodles/)*   |   🌎  *[Global Leaderboard](https://getjackpot.xyz/leaderboard/)*\n*Last updated: 10/20/22 at 10:51 am EST*\n\n💰 Current Jackpot Size: `1,000 USDC`     ⏱️ Date of Next Drawing: `Nov. 4th @ 9:05pm EST`\n✋ # of Community Participants: `65`       ✋ # of Global Participants: `195`\n\n----------------\n\n        🏆   **__1.__**  🥇  **cryptobreaky    *[Twitter Profile](https://twitter.com/cryptobreaky)*   ~   🎟️ *[48800 XP](https://getjackpot.xyz/cryptobreaky)*\n\n        🏆   **__2.__**  🥈  **LanDAO Calrissian    (*[Twitter Profile](https://twitter.com/cryptobreaky)*)   ~   🎟️ *[46500 XP](https://getjackpot.xyz/cryptobreaky)***\n\n        🏆   **__3.__**  🥉  **Ashh    (*[Twitter Profile](https://twitter.com/cryptobreaky)*)   ~   🎟️ *[44700 XP](https://getjackpot.xyz/cryptobreaky)***\n\n        🏆   **__4.__**  ✨  **crypto_King    (*[Twitter Profile](https://twitter.com/cryptobreaky)*)   ~   🎟️ *[42800 XP](https://getjackpot.xyz/cryptobreaky)***\n\n        🏆   **__5.__**  ✨  **RatheSunGod    (*[Twitter Profile](https://twitter.com/cryptobreaky)*)   ~   🎟️ *[39500 XP](https://getjackpot.xyz/cryptobreaky)***\n\n        ✨   **Type *!rank* in any channel to see your current stats.**\n\n----------------\n\n👉 *Type `!rank ` to see your own stats.*\n👉 *Type `!rank/username` to see someone else's stats.*\n👉 *Type `!leaderboard ` to preview the Community Leaderboard.*\n👉 *Type `!global ` to preview the Global Leaderboard.*\n👉 *Type `!jackpot ` to see the upcoming Jackpot.*\n👉 *Go to [getjackpot.xyz](https://getjackpot.xyz/) to see the full leaderboards.*\n** **\n** **"
    return string

def getFullLeaderboardEmbed():
    embed = discord.Embed(title="Leaderboard", description=getLeaderboardInformation(), color=0xe9e9e9)
    return embed

def getLeaderboardEmbed():
    embed = discord.Embed(title="The Leaderboard", description="Check the leaderboard to see the most valuable contributors in your community and beyond.", color=0xe9e9e9)
    return embed

def getTwitterEmbed(link, boosted=False):
    if boosted:
        mcolor = 0xf21d6a
        message = "**Engage** with the **Tweet** below to earn up to **2400 XP**\n\n🚨 **THIS RAID IS BOOSTED -- EARN 200% XP!** 🚨\n\nLike = **400 XP**\nReply = **800 XP**\nRetweet = **1200 XP**\n\n⛓ __**" + link + "**__ ⛓"
    else:
        mcolor = 0x1da1f2
        message = "**Engage** with the **Tweet** below to earn up to **1200 XP**\n\nLike = **200 XP**\nReply = **400 XP**\nRetweet = **600 XP**\n\n⛓ __**" + link + "**__ ⛓"
    embed=discord.Embed(title="**RAID ALERT**", description=message, color=mcolor)
    embed.set_author(name="Twitter Raid Rewards", icon_url="https://img.icons8.com/color/344/twitter--v1.png")
    embed.set_footer(text="By Jackpot", icon_url="https://img.icons8.com/color/344/twitter--v1.png")
    return embed

def getMissionsEmbed():
    embed=discord.Embed(title="**🗺️ Missions 🗺️**", description="Click the **View Missions** button below to see your community's active missions and their respective XP rewards.", color=0xf21d6a)
    embed.add_field(name="**Submitting Mission Completion**", value="To get credit (XP) for completing a mission, head over to #mission-complete and follow the directions. All you'll need to do is select the appropriate quest and submit a screenshot or link to the completed work (proof should be contained on the same message).\n\n➡️ **Select an active mission from the dropdown to view its details.**", inline=False) 
    return embed

def getMissionsListEmbed(missions = "**🟢 visit_website**\nDEADLINE: Thurs, Nov 13\n\n**🟢 visit_website\n**DEADLINE: Thurs, Nov 13"):
    embed=discord.Embed(title="✅ **Mission Complete** ✅", description="In this channel, use `!verify [MISSION_NAME] [additional details or explaination]` to submit proof of a specific mission. If you are attaching a picture, attach it to the same message.", color=0xe9e9e9)
    embed.add_field(name="**Active Mission Names**", value=missions, inline=False)
    embed.set_footer(text="\n\nOnce submitted, a community admin will be able to approve/disapprove your submission. If approved, you'll receive XP for your effort and will be notified in #xp-log.") 
    return embed

def verifyMission(mission):
    return True
    
def getMissionXP(mission):
    return 100

@client.event
async def on_ready():
    print("Logged in")
    
    ## if the Jackpot role doesn't exist, create it
    if discord.utils.get(client.guilds[0].roles, name=JACKPOT_ROLE) == None:
        await client.guilds[0].create_role(name="Jackpot", color=discord.Color.from_rgb(219, 255, 51), hoist=False)
    
    guild = client.guilds[0]
    ## Make #opt-in, #guide avalible to everyone
    channels = ["opt-in", "guide"]
    for channel in channels:
        if discord.utils.get(guild.channels, name=channel) == None:
            await guild.create_text_channel(channel)
            await discord.utils.get(guild.channels, name=channel).set_permissions(guild.default_role, read_messages=True, send_messages=False)   
            await discord.utils.get(guild.channels, name=channel).set_permissions(discord.utils.get(guild.roles, name=BOT_ROLE), read_messages=True, send_messages=True)
    ## make the following channels visible to everyone in the "Jackpot" role they don't exist: #leaderboard, #raids, #missions, #mission-complete, #xp-log
    channels = ["leaderboard", "raids", "missions", "mission-complete", "xp-log"]
    for channel in channels:
        if discord.utils.get(guild.channels, name=channel) == None:
            await guild.create_text_channel(channel)
            await discord.utils.get(guild.channels, name=channel).set_permissions(guild.default_role, read_messages=False)
            await discord.utils.get(guild.channels, name=channel).set_permissions(discord.utils.get(guild.roles, name=BOT_ROLE), read_messages=True, send_messages=True)
            if channel != "mission-complete":
                await discord.utils.get(guild.channels, name=channel).set_permissions(discord.utils.get(guild.roles, name=JACKPOT_ROLE), read_messages=True)
            else:
                await discord.utils.get(guild.channels, name=channel).set_permissions(discord.utils.get(guild.roles, name=JACKPOT_ROLE), read_messages=False, send_messages=True)
    
    ## in the #opt-in channel, send a message with a button to opt-in
    class optInstructions(discord.ui.View):
            def __init__(self):
                super().__init__()
            @discord.ui.button(label="Opt-In", style=discord.ButtonStyle.green)
            async def optin(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
                class optIn(discord.ui.View):
                    def __init__(self):
                        super().__init__()
                    @discord.ui.button(label="Link Twitter", style=discord.ButtonStyle.green)
                    async def optin(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
                        await interaction.response.send_modal(optInModal())
                await interaction.response.send_message(embed=getTwitterOAUTHEmbed(), view=optIn(), ephemeral=True)
    
    class optInModal(ui.Modal, title = "Twitter OAuth Code"):
        tweeterHandle = ui.TextInput(label = "Verify and link your account", style=discord.TextStyle.short, placeholder="Copy and paste your OAuth code here", required = True)
        async def on_submit(self, interaction: discord.Interaction):
            ## DO API CALL HERE
            
            ## put on the xp-log channel that a user has opted in
            await discord.utils.get(guild.channels, name="xp-log").send("✅ **" + str(interaction.user) + "** has opted in!")
            ## assign the Jackpot role to the user
            await interaction.user.add_roles(discord.utils.get(guild.roles, name=JACKPOT_ROLE))
            await interaction.response.send_message(content="✅ **Success!**\n\nYou have now successfully opted in to Jackpot and have been awarded `1000 XP` 🎟️ as a token of our gratitude. You are now ready to begin earning XP for the value you bring to the table.\n\nHead over to #guide to see all of the ways you can earn XP 🎟️.", ephemeral=True)
            
    if discord.utils.get(guild.channels, name="opt-in").last_message == None or discord.utils.get(guild.channels, name="opt-in").last_message.author != client.user:
        await discord.utils.get(guild.channels, name="opt-in").send(embed = getWelcomeEmbed(), view = optInstructions())
        
    ## in the guide channel, set channel topic
    if discord.utils.get(guild.channels, name="guide").last_message == None or discord.utils.get(guild.channels, name="guide").last_message.author != client.user:
        await discord.utils.get(guild.channels, name="guide").edit(topic="\n__**Welcome to Jackpot**__ 👋\n**Jackpot is a simple, *no-brainer* community engagement solution architected in collaboration with 100+ web3 industry veterans: project founders, community managers, moderators, and core contributors across the Ethereum and Solana ecosystems.\nWe exist to organically motivate the human layer of the chain, empowering communities and their members to achieve more, together.**")
        ## send a message saying "intro message"
        ##await discord.utils.get(guild.channels, name="guide").send("__**Welcome to Jackpot**__ 👋\n**Jackpot is a simple, *no-brainer* community engagement solution architected in collaboration with 100+ web3 industry veterans: project founders, community managers, moderators, and core contributors across the Ethereum and Solana ecosystems.\nWe exist to organically motivate the human layer of the chain, empowering communities and their members to achieve more, together.**\n-----------------------------------------------------------------------------\n**Our goal is to amplify the intrinsic & extrinsic motivators already present in web3:**\n🎟️  __**1.** *Earn XP by organically adding value to your community (bots won't get very far).*__\n📈  __**2.** *Climb the Community & Global Leaderboards and prove that you're a community superstar.*__\n💰 __**3.** *Automatically enter the bi-weekly raffle where we give away a large portion of our revenue to one random winner. 1 XP = 1 Raffle ticket.*__")
        
        ## send getting started embed with a buttons
        class gettingStarted(discord.ui.View):
            def __init__(self):
                super().__init__()
            @discord.ui.button(label="Opt-In", style=discord.ButtonStyle.green)
            async def optin(self, interaction: discord.Interaction, button: discord.ui.Button):
                await interaction.response.send_message("Look's like you've already opted in! Go to #opt-in to confirm.", ephemeral=True)
                
            @discord.ui.button(label="Raid", style=discord.ButtonStyle.primary)
            async def raid(self, interaction: discord.Interaction, button: discord.ui.Button):
                await interaction.response.send_message("Ready to get some XP? Head over to #raids to start earning!", ephemeral=True)

        ##await discord.utils.get(guild.channels, name="guide").send(embed=getGettingStartedEmbed(), view=gettingStarted())
        ##await discord.utils.get(guild.channels, name="guide").send(embed=getUpcomingJackpotsEmbed())
        ##await discord.utils.get(guild.channels, name="guide").send(embed=getLeaderboardsEmbed())
        await discord.utils.get(guild.channels, name="guide").send(embed=getIntroEmbed())
        await discord.utils.get(guild.channels, name="guide").send(embed=getXPEmbed())
        ##await discord.utils.get(guild.channels, name="guide").send(embed=getMissionsEmbed())
        await discord.utils.get(guild.channels, name="guide").send(embed=getChannelsEmbed())
        await discord.utils.get(guild.channels, name="guide").send(embed=getCommandsEmbed())
    
    ## in the leaderboard channel, send a leaderboard message
    if discord.utils.get(guild.channels, name="leaderboard").last_message == None or discord.utils.get(guild.channels, name="leaderboard").last_message.author != client.user:
        class printLeaderboard(discord.ui.View):
            def __init__(self):
                super().__init__()
            @discord.ui.button(label="🏆 View Leaderboard 🏆", style=discord.ButtonStyle.green)
            async def optin(self, interaction: discord.Interaction, button: discord.ui.Button):
                await interaction.response.send_message(embed=getFullLeaderboardEmbed(), ephemeral=True)
        await discord.utils.get(guild.channels, name="leaderboard").send(embed = getLeaderboardEmbed(), view = printLeaderboard())
        
    ## in the raids channel, sent a twitter raid embed for both boosted and normal
    if discord.utils.get(guild.channels, name="raids").last_message == None or discord.utils.get(guild.channels, name="raids").last_message.author != client.user:
        await discord.utils.get(guild.channels, name="raids").send(embed=getTwitterEmbed("TEST", False))
        await discord.utils.get(guild.channels, name="raids").send(embed=getTwitterEmbed("TEST", True))
    
    ## in the missions channel, send an getMissionsEmbed() embed with a button 
    if discord.utils.get(guild.channels, name="missions").last_message == None or discord.utils.get(guild.channels, name="missions").last_message.author != client.user:
        
        class missions(discord.ui.View):
            def __init__(self):
                super().__init__()
            @discord.ui.button(label="View Missions", style=discord.ButtonStyle.green)
            async def optin(self, interaction: discord.Interaction, button: discord.ui.Button):
                await interaction.response.send_message("MISSIONS WILL FETCHED AND APPEAR HERE", ephemeral=True)
                
        await discord.utils.get(guild.channels, name="missions").send(embed=getMissionsEmbed(), view=missions())
        
    ## in the mission-complete, send an getMissionsListEmbed() embed
    ##if discord.utils.get(guild.channels, name="mission-complete").last_message == None or discord.utils.get(guild.channels, name="mission-complete").last_message.author != client.user:
    embedMessage = await discord.utils.get(guild.channels, name="mission-complete").send(embed=getMissionsListEmbed())
    ## pin the message
    await embedMessage.pin()
    
    ## make the following channels visible to only Admins if they don't exist: #mission-admin, #mission-approval, #launch-raid
    channels = ["mission-admin", "mission-approval", "launch-raid"]
    for channel in channels:
        if discord.utils.get(guild.channels, name=channel) == None:
            await guild.create_text_channel(channel)
            await discord.utils.get(guild.channels, name=channel).set_permissions(guild.default_role, read_messages=False)
            await discord.utils.get(guild.channels, name=channel).set_permissions(discord.utils.get(guild.roles, name=BOT_ROLE), read_messages=True, send_messages=True)
            await discord.utils.get(guild.channels, name=channel).set_permissions(discord.utils.get(guild.roles, name=ADMIN_ROLE), read_messages=True, send_messages=True)
    ## in the mission-admin, send a message and 3 buttons: Add Quest, Edit Quest, Delete Quest
    if discord.utils.get(guild.channels, name="mission-admin").last_message == None or discord.utils.get(guild.channels, name="mission-admin").last_message.author != client.user:
        
        class addQuest(ui.Modal, title = "Add Quest Form"):
            name = ui.TextInput(label = "Mission Name", style=discord.TextStyle.short, placeholder = "Mission Name", required = True)
            desc = ui.TextInput(label = "Mission Description", style=discord.TextStyle.short, placeholder = "Mission Description", required = True)
            reward = ui.TextInput(label = "Mission Reward (XP)", style=discord.TextStyle.short, placeholder = "e.g. 400", required = True)
            supply = ui.TextInput(label = "Mission Total Supply (Optional)", style=discord.TextStyle.short, placeholder = "Default: Unlimited", required = False)
            perperson = ui.TextInput(label = "Mission Supply Per Person (Optional)", style=discord.TextStyle.short, placeholder = "Default: Unlimited", required = False)
            
            async def on_submit(self, interaction: discord.Interaction):
                ## DO API CALL HERE
                
                await interaction.response.send_message(content="A Quest was successfully added: **" + str(self.name) + "**", ephemeral=False)
                
        class editQuest(ui.Modal, title = "Add Quest Form"):
            dropDown = ui.Select(custom_id = "Select Quest", placeholder = "Select Quest", options = [discord.SelectOption(label = "Quest 1", value = "1"), discord.SelectOption(label = "Quest 2", value = "2")])
            async def on_submit(self, interaction: discord.Interaction):
                ## DO API CALL HERE
                
                await interaction.response.send_message(content="A Quest has been modifed", ephemeral=False)
                
        class deleteQuest(ui.Modal, title = "Add Quest Form"):
            tweeterHandle = ui.TextInput(label = "Enter your Twitter Handle to verify tweets", style=discord.TextStyle.short, default = "@", required = True, max_length = 50)
            async def on_submit(self, interaction: discord.Interaction):
                ## DO API CALL HERE
                
                await interaction.response.send_message(content="You have successfully deleted a Quest", ephemeral=True)
                
        class editSelector(discord.ui.View):
            @discord.ui.select(placeholder="Select a Quest", options=[
                discord.SelectOption(label="Quest 1", default=True, description="This is your first quest", emoji="🟢"),
                discord.SelectOption(label="Quest 2", description="This is your second quest", emoji="🟢")])
            async def on_select(self, interaction: discord.Interaction, select: discord.ui.Select):
                ## API CALL TO GET DATA
                class editExistingQuest(ui.Modal, title = "EDIT TASK MODAL"):
                    desc = ui.TextInput(label = "Mission Description", style=discord.TextStyle.short, placeholder = "Mission Description will be populated here", required = True)
                    reward = ui.TextInput(label = "Mission Reward (XP)", style=discord.TextStyle.short, placeholder = "num will be populated here", required = True)
                    supply = ui.TextInput(label = "Mission Total Supply (Optional)", style=discord.TextStyle.short, placeholder = "num will be populated here", required = False)
                    perperson = ui.TextInput(label = "Mission Supply Per Person (Optional)", style=discord.TextStyle.short, placeholder = "num will be populated here", required = False)
                    
                    async def on_submit(self, interaction: discord.Interaction):
                        ## DO API CALL HERE
                        
                        await interaction.response.send_message(content="A Quest has been modifed", ephemeral=False)
                await interaction.response.send_modal(editExistingQuest())
                
        class deleteSelector(discord.ui.View):
            @discord.ui.select(placeholder="Select a Quest", options=[
                discord.SelectOption(label="Quest 1", default=True, description="This is your first quest", emoji="🟢"),
                discord.SelectOption(label="Quest 2", description="This is your second quest", emoji="🟢")])
            async def on_select(self, interaction: discord.Interaction, select: discord.ui.Select):
                ## API CALL TO GET DATA
                class deleteExistingQuest(ui.Modal, title = "⚠️ DELETE TASK ⚠️"):
                    deleteMe = ui.TextInput(label = "Type 'DELETE' below to confirm your decision.", style=discord.TextStyle.short, placeholder = "This action can not be reversed.", required = False)
                    
                    async def on_submit(self, interaction: discord.Interaction):
                        ## DO API CALL HERE
                        ## delete the empemeral message
                        await interaction.response.send_message(content="A Quest has been deleted", ephemeral=False)
                
                await interaction.response.send_modal(deleteExistingQuest())
            
        class quests(discord.ui.View):
            def __init__(self):
                super().__init__()
            @discord.ui.button(label="Add Quest", style=discord.ButtonStyle.green)
            async def but1(self, interaction: discord.Interaction, button: discord.ui.Button):
                await interaction.response.send_modal(addQuest())
            @discord.ui.button(label="Edit Quest", style=discord.ButtonStyle.primary)
            async def but2(self, interaction: discord.Interaction, button: discord.ui.Button):
                ##await interaction.response.send_modal(editQuest())
                await interaction.response.send_message(content="Select a Quest you would like to edit", ephemeral=True, view=editSelector())
            @discord.ui.button(label="Delete Quest", style=discord.ButtonStyle.red)
            async def but3(self, interaction: discord.Interaction, button: discord.ui.Button):
                await interaction.response.send_message(content="Select a Quest you would like to delete", ephemeral=True, view=deleteSelector())
                
        await discord.utils.get(guild.channels, name="mission-admin").send("🗺️ **Mission Admin** 🗺️\nClick the buttons below to interact with your **Missions**.\n\n1. **Add Mission:** Click \"Add Mission\" to activate a new mission for your community. You'll be able to specify the objective for the mission and set an appropriate XP reward for completion. The maximum possible reward for a single mission is 5,000 XP and the minimum is 50 XP. We suggest adding up to 15,000 XP of missions to maximize output from your community.\n\n2. **Edit Mission:** Click \"Edit Mission\" to change the details for any active mission.\n\n3. **Delete Mission:** Click \"Delete Mission\" to delete an active mission.", view = quests())
    
    ## in the launch-raid, send a message with 1 button: Launch Raid. Pressing the button will open a discord form to fill out
    if discord.utils.get(guild.channels, name="launch-raid").last_message == None or discord.utils.get(guild.channels, name="launch-raid").last_message.author != client.user:

        class raids(discord.ui.View):
            def __init__(self):
                super().__init__()
            @discord.ui.button(label="Add Raid", style=discord.ButtonStyle.green)
            async def addRaid(self, interaction: discord.Interaction, button: discord.ui.Button):
                class raidSelector(discord.ui.View):
                    @discord.ui.select(placeholder="Select a Quest", min_values = 1, max_values = 3, options=[
                        discord.SelectOption(label="Retweet", default=True, description="Check if someone retweets a target tweet", emoji="📩"),
                        discord.SelectOption(label="React", description="See if a user reacts to a Tweet", emoji="❤️"), 
                        discord.SelectOption(label="Comment", description="Award points to users who leave a comment", emoji="📝")
                        ])
                    async def on_select(self, interaction: discord.Interaction, select: discord.ui.Select):
                        ## API CALL TO GET DATA
                        class addRaid(ui.Modal, title = "Create a Twitter Raid | " + select.values[0]):
                            url = ui.TextInput(label = "Tweet URL", style=discord.TextStyle.short, placeholder = "What is the URL of a tweet", required = True)
                            boosted = ui.TextInput(label = "Boosted XP", style=discord.TextStyle.short, placeholder = "True/False (Boosted Tweets earn 200% XP)", required = True)
                            async def on_submit(self, interaction: discord.Interaction):
                                ## DO API CALL HERE
                                link = self.url.value
                                boosted, retweet, react, comment = False, False, False, False
                                if "t" in self.boosted.value.lower():
                                    boosted = True
                                
                                for value in select.values:
                                    if "retweet" in value.lower():
                                        retweet = True
                                    elif "react" in value.lower():
                                        react = True
                                    elif "comment" in value.lower():
                                        comment = True
                                
                                ## make a new view of 1 -3 buttons for retweeting, reacting, commenting
                                class raidView(discord.ui.View):
                                    @discord.ui.button(label="Check Retweet", style=discord.ButtonStyle.primary)
                                    async def retweet(self, interaction: discord.Interaction, button: discord.ui.Button):
                                        ## DO API CALL HERE
                                        await interaction.response.send_message(content="You have retweeted this tweet", ephemeral=True)
                        
                                    @discord.ui.button(label="Check React", style=discord.ButtonStyle.primary)
                                    async def react(self, interaction: discord.Interaction, button: discord.ui.Button):
                                        ## DO API CALL HERE
                                        await interaction.response.send_message(content="You have reacted to this tweet", ephemeral=True)
    
                                    @discord.ui.button(label="Check Comment", style=discord.ButtonStyle.primary)
                                    async def comment(self, interaction: discord.Interaction, button: discord.ui.Button):
                                        ## DO API CALL HERE
                                        await interaction.response.send_message(content="You have commented on this tweet", ephemeral=True)
                            
                                ## if link is blank, make an error message
                                if link == "":
                                    await interaction.response.send_message(content="You must provide a valid Tweet URL. Please try again.", ephemeral=True)
                                else:
                                    await interaction.response.send_message(content="A raid has been created", ephemeral=False)
                                    await discord.utils.get(guild.channels, name="raids").send(embed=getTwitterEmbed(str(self.url.value), boosted), view=raidView())
                        await interaction.response.send_modal(addRaid())
                await interaction.response.send_message(content="Select the type of Raid you want (multiple can be picked)", ephemeral=True, view=raidSelector())
            
        await discord.utils.get(guild.channels, name="launch-raid").send("⚔️ **Launch Twitter Raid** ⚔️\nClick the button below to **Launch a Twitter Raid**\n\n**You'll be asked to:**\n\n**__1.__ Specify Tweet:** Paste the URL of the Tweet that you'd like to raid.\n**__2.__ Choose Engagement Type:** Choose what type of engagement you'd like to incentivize.\n**__3.__ Apply a Boost:** Select whether or not you want to apply a Boost to your raid (increases XP earned by 200%). You can use a maximum of 4 Boosts/Month.", view = raids())
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    try:
        serverName = message.guild.name
    except:
        serverName = None
    username = message.author
    text = message.content
    
    ## if someone messages the #missions-complete channel with command !verify then send a message to #mission-approval
    if message.channel.name == "mission-complete" and message.content.lower().startswith("!verify"):
        missionName = message.content.split(" ")[1]
        textMessage = message.content.split(" ")[2:]
        textMessage = " ".join(textMessage)
        if verifyMission(missionName):
            attachmentString = ""
            if len(message.attachments) > 0:
                ##await discord.utils.get(message.guild.channels, name="mission-approval").last_message.add_file([discord.File(io.BytesIO(requests.get(message.attachments[0].url).content), filename=message.attachments[0].filename)])
                ## get a list of the URLs of the attachments and their names
                for attachment in message.attachments:
                    attachmentString += "**Attachment:**"
                    attachmentString += " ["+attachment.filename + "] (" + attachment.url + ") "
                    attachmentString += "\n\n"
            
            author = str(message.author)
            ## send a confirmation message to #mission-approval, delete it after 10 seconds: "mission submitted by " + str(message.author)
            newMessage = await discord.utils.get(message.guild.channels, name="mission-complete").send("🎉 Mission '"+missionName+"' submitted by " + author)
            ## delete newMessage after 10 seconds
            await message.delete()
            
            class approveButtons(discord.ui.View):
                def __init__(self):
                    super().__init__()
                @discord.ui.button(label="APPROVE", style=discord.ButtonStyle.green)
                async def approve(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
                    await interaction.response.send_message("MISSION APPROVED", ephemeral=True)
                    ## delete the main message the button was pressed on
                    await interaction.message.delete()
                    ## delete newMessage
                    await newMessage.delete()
                    ## send a message to #xp-log with the mission name, username, and XP
                    await discord.utils.get(message.guild.channels, name="xp-log").send("🎉 Mission '"+missionName+"' completed by " + author + " for " + str(getMissionXP(missionName)) + " XP")
                    
                @discord.ui.button(label="DENY", style=discord.ButtonStyle.red)
                async def deny(self, interaction2: discord.Interaction, button: discord.ui.Button) -> None:
                    class feedbackMission(ui.Modal, title = "Send feedback to " + author[:12] + "..."):
                        feedback = ui.TextInput(label = "Reason why mission declined", style=discord.TextStyle.long, default = "You have not completed the mission spec", required = True)
                        async def on_submit(self, interaction: discord.Interaction):
                            await newMessage.reply("MISSION WAS DENIED BY ADMINS: " + str(self.feedback.value))
                            await interaction.response.send_message("MISSION DENIED", ephemeral=True)
                    await interaction2.response.send_modal(feedbackMission())
                    await interaction2.message.delete()
            
            await discord.utils.get(message.guild.channels, name="mission-approval").send("📬 **New Mission Submission** 📬\n\nFrom: `" + str(username) + "`\nMission: `" + missionName + "`\nReward: `" + str(getMissionXP(missionName)) + " XP`\nText: `" + textMessage + "`\n\n" + attachmentString + "*Choose whether to **APPROVE** or **DISAPPROVE** by reacting below:*", view = approveButtons())
                
        else:
            ## if the mission name is invalid, send an error message, reply to the user
            await newMessage.reply("Invalid mission name. Please try again (Case Sensitive).")
    
    ## if someone DMs the bot '!rank' then send them their rank by calling api.getRank(username, serverName)
    if message.content.lower() == "!rank":
        ## see if user has role JACKPOT_ROLE
        if discord.utils.get(message.author.roles, name="JACKPOT_ROLE"):
            await message.channel.send(api.getRank(username, serverName))
        else: 
            await message.reply("To interact with me, opt-in via the `#opt-in` channel")
    ## if someone DMs the bot '!rank/username' then send them the rank of the user they specified by calling api.getRank(username, serverName)
    elif message.content.lower().startswith("!rank/"):
        await message.channel.send(api.getRank(message.content[6:], serverName))
    ## if someone DMs the bot '!leaderboard' then send them the leaderboard by calling api.getLeaderboard(serverName)
    elif message.content.lower() == "!leaderboard":
        await message.channel.send(api.getLeaderboard(serverName))
    ## if someone DMs the bot '!global` then send them the global leaderboard by calling api.getGlobalLeaderboard()
    elif message.content.lower() == "!global":
        await message.channel.send(api.getGlobalLeaderboard())
    ## if someone DMs the bot '!jackpot' then send them the jackpot message by calling api.getJackpot(serverName)
    elif message.content.lower() == "!jackpot":
        await message.channel.send(api.getJackpot(serverName))
    ## if someone DMs the bot '!help' then send them a list of commands they can use
    elif message.content.lower() == "!help":
        await message.channel.send("**📝 Here's a list of commands you can use 📝**\n\n**🏆 !rank** - get your rank\n**🎖️ !rank/{username}** - get the rank of a specific user\n**💯 !leaderboard** - get the leaderboard for this server\n**🌎 !global** - get the global leaderboard\n**💰 !jackpot** - get the jackpot for this server\n**💬 !help** - get a list of commands")
    
## create an event to see everytime a user reacts to a message
@client.event
async def on_raw_reaction_add(payload):
    serverName = payload.guild_id
    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    emoji = payload.emoji.name
    user = payload.member
    originalAuthor = message.author
    
    ## if reacted with a checkmark in opt-in channel, then send a form message in channel only visible to the reaction author asking for their Twitter handle
    ## wait for them to respond with their Twitter handle, then call api.recordTwitterHandle(user, serverName, twitterHandle)
    if emoji == "✅" and channel.name == "opt-in" and user != client.user:
        ## pop up a form message calling the Modal makeModal() function
        await user.send("Please enter your Twitter handle below. *Please note that once you do this, you will not have to do it again.*")
        def check(m):
            return m.author == user and m.channel == user.dm_channel
        try:
            msg = await client.wait_for('message', check=check, timeout=500.0)
        except asyncio.TimeoutError:
            await user.send('You did not respond in time.')
        else:
            twitterHandle = msg.content
            await user.send("Please wait while I verify your Twitter handle...")
            ## check if the user's twitter handle is valid
            if api.recordTwitterHandle(user, serverName, twitterHandle):
                await user.send("Twitter handle verified. You're all set!")
                await discord.utils.get(message.guild.channels, name="xp-log").send(user.mention + " just received `1000 XP` 🎟️ for successfully opting in to Jackpot! Onward and upward!")
            else:
                await user.send("Twitter handle not found. Please try again.")
    
    
    ##api.recordReaction(user, originalAuthor)

## get a list of everyone active in the last 24 hours, run this every 24 hours
@client.event
async def on_timer():
    await client.wait_until_ready()
    guild = client.guilds[0]
    while not client.is_closed():
        ## get a list of everyone active in the last 24 hours
        activeUsers = api.getActiveUsers()
        ## if the list is empty, then do nothing
        if len(activeUsers) == 0:
            pass
        ## if the list is not empty, then send a message to #opt-in with the list of active users
        else:
            await discord.utils.get(guild.channels, name="opt-in").send("**🏆 Here's a list of active users in the last 24 hours 🏆**\n\n" + activeUsers)
        ## wait 24 hours before checking again
        await asyncio.sleep(86400)
    
client.run(TOKEN)