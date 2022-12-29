import discord
from discord import ui, app_commands, AppCommandOptionType
from discord.ext import commands
from discord import Button, ButtonStyle
import api as api
import random 
import requests
import asyncio
from multiprocessing import Process
import io
import logging
import re

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
TOKEN = "MTAzNzYyOTMyMDIwMzYxNjI2Ng.GhpR78.NzFqeGnDD0IZdQCArpLiL5CSAmdLtPUZ0fvIuo"
client = discord.Client(intents=discord.Intents.all())
BOT_ROLE = "Jackpot Official"
ADMIN_ROLE = "Admin"
JACKPOT_ROLE = "Jackpot"
JACKPOT_NON_OPT = "Jackpot (Not Opted In)"
VIEW_TIMEOUT = 1000000000000000000000000

REG_GUILD =   "┎----- 🎰 Jackpot 🎰 -----┒"
ADMIN_GUILD = "┎-- 💎 Jackpot Admin 💎 --┒"

def getRaidsEmbed():
    embed=discord.Embed(title="⚔️ **Launch Twitter Raid** ⚔️", description="Click the button below to **Launch a Twitter Raid**", color=0xFF3F33)
    embed.add_field(name="**You'll be asked to:**", value="**1. Choose Engagement Type:** Choose what type of engagement you'd like to incentivize.\n**2. Specify Tweet:** Paste the URL of the Tweet that you'd like to raid.\n", inline=False) 
    return embed

def getMissionAddEmbed():
    embed=discord.Embed(title="🗺️ **Mission Admin** 🗺️", description="Click the buttons below to interact with your **Missions**.", color=0xe9e9e9)
    embed.add_field(name="1. **Add Mission:**", value="Click \"Add Mission\" to activate a new mission for your community. \n\nYou'll be able to specify the objective for the mission and set an appropriate XP reward for completion. The maximum possible reward for a single mission is `5,000 XP 🎟️` and the minimum is `50 XP 🎟️`. We suggest adding up to `15,000 XP 🎟️` of missions per month to maximize output from your community.", inline=False)
    embed.add_field(name="2. **Edit Mission:**", value="Click \"Edit Mission\" to change the details for any active mission.", inline=False)
    embed.add_field(name="3. **Delete Mission:**", value="Click \"Delete Mission\" to delete an active mission.", inline=False)
    return embed
    
def getGettingStartedEmbed():
    embed=discord.Embed(title="Get Started 🚀", description="We take data privacy very seriously. To begin earning XP, you must opt-in and connect your Twitter.", color=0xff6969)
    embed.set_author(name="Jackpot", url="https://getjackpot.xyz", icon_url="https://static.wixstatic.com/media/cdc018_a8e52bee9e114aa9a11355686b703954~mv2.png")
    embed.set_thumbnail(url="https://static.wixstatic.com/media/cdc018_a8e52bee9e114aa9a11355686b703954~mv2.png")
    embed.add_field(name="Opt-In", value="Navigate to <#opt-in> and follow the relevant instructions to start earning XP. Once you do this, you will not have to do it again.", inline=False) 
    embed.add_field(name="First Tweet Raid", value="Navigate to <#raids> to engage with tweets and earn XP.", inline=False) 
    embed.set_footer(text="⚠️ Failing to Opt-In will mean you will not be able to earn XP.")
    return embed

def getReferalEmbed():
    embed=discord.Embed(title="Unique Referral Code", description="Share your code with friends to refer a new community to Jackpot! If they sign up as a paying customer, you will earn a substantial XP bonus for yourself and everyone in your community!", color=0x222222)
    return embed 

def getOptIn():
    embed=discord.Embed(title="Congratulations!", description="**You have now successfully joined Jackpot and are eligible to win the Jackpot raffle!** \n\n You are now ready to begin earning XP for all the value you add to your community. As a token of our gratitude, you have been awarded `1000 XP 🎟️`", color=0x33FF5C)
    return embed 

def getOptInNoWallet(getstarted):
    embed=discord.Embed(title="Congratulations!", description="**You have now successfully joined Jackpot. Until you add your ETH wallet address in the <#" + str(getstarted) + "> channel you are ineligible to win the Jackpot raffle.** \n\n In the meantime, you are now ready to begin earning XP for all the value you add to your community. As a token of our gratitude, you have been awarded `1000 XP 🎟️`", color=0xcffc03)
    return embed 

def getRankEmbed(memID, serverRank, globalRank, XP, globalXP, trend = 0):
    if str(serverRank) == "1":
        descp = memID + " is the top contributor in this server, with `" + str(XP) + "XP 🎟️`! Keep up the great work!"
    else:
        descp = memID + " has `" + str(XP) + "XP 🎟️` in this server! Keep earning XP to rank up!"
    emoji = ""
    if trend == 1:
        emoji = " 🔼"
    elif trend == -1:
        emoji = " 🔽"
    embed = discord.Embed(title="🎖️ " + memID + " is Rank " + str(serverRank) + " in this Server", description=descp, color=0xEBF900)
    embed.add_field(name="🌎 Global Stats 🌎", value="Rank: `" + str(globalRank) + "`\n🎟️ Total XP earned in this period: `" + str(globalXP) + emoji + "` \n\n", inline=True)
    embed.set_footer(text="Powered by Jackpot", icon_url="https://static.wixstatic.com/media/cdc018_603e1fc27c6a4c71b2c8c333f66c858b~mv2.png")
    return embed

def getMultiplierEmbed():
    embed=discord.Embed(title="Claim XP Multiplier", description="You're eligible to claim an XP Multiplier based on the length of time you've held your community's NFT.\n\nTo claim the XP Multiplier, click the button below and sign a message with the wallet that holds your NFT. Signing a message is different than signing a transaction. This will prove ownership without sharing your private key.", color=0x222222)
    return embed

def getUpdateEmbed():
    embed=discord.Embed(title="Update Your Information", description="Click on the button below to add or edit information linked to your Jackpot account.", color=0x222222)
    return embed

def getUpcomingJackpotsEmbed():
    embed=discord.Embed(title="Upcoming Jackpot💰", description="** **💰 Current Jackpot Size: `1,000 USDC` | ⏱️ Time Until Next Drawing: `24 Days`\n✋ # of Community Participants: `65` | ✋ # of Global Participants: `195`\n🎟️ **1 XP = 1 Raffle Ticket**", color=0xe9e9e9)
    return embed

def getLeaderboardsEmbed():
    embed=discord.Embed(title="Leaderboards 📈", color=0xe9e9e9)
    embed.add_field(name="**Full Leaderboard on our website**", value="🌐 __[Community Leaderboard](https://getjackpot.xyz/leaderboard/doodles/)__\n🌐 __[Global Leaderboard](https://getjackpot.xyz/leaderboard/)__", inline=False) 
    return embed

def getIntroEmbed():
    embed = discord.Embed(title="**Join Now!**", description="Opt-in to immediately earn `1000 XP 🎟️` and have a chance at winning the Jackpot Raffle.", color=0xf59b42)
    return embed
    
def getXPEmbed():
    embed=discord.Embed(title="**How to Earn XP**", description="Below is a guide to all the actions you can take in your community that will be automatically rewarded.", color=0xe9e9e9)
    embed.add_field(name="**Discord:**", value="🎟️ Sending messages *(diminishing returns)*\n🎟️ Reacting to messages *(diminishing returns)*\n🎟️ Other people reacting to your messages\n🎟️ Other people replying to your messages\n🎟️ Being one of the first people to interact with a new member\n🎟️ Inviting real people to the server\n🎟️ Visiting the server daily\n", inline=False) 
    embed.add_field(name="**Twitter:**", value = "🎟️ Retweeting a #raids tweet\n🎟️ Replying to a #raids tweet\n🎟️ Liking a #raids tweet\n🎟️ Following other community members\n🎟️ Being followed by other community members\n", inline=False) 
    embed.add_field(name="**Missions:**", value = "🎟️ Successfully completing <#missions>", inline=False)
    return embed

def getChannelsEmbed():
    embed=discord.Embed(title="**Channel Overview**", color=0xe9e9e9)
    embed.add_field(name="Important channels to keep track of:", value="📍 #user-settings | Review and change your personal details.\n📍 #leaderboard | Visit our website containing your community’s most valuable contributors.\n📍 #raids | Participate in Twitter raids to earn XP.\n📍 #missions | Choose from available missions and submit proof of completion.\n📍 #notifs | Get notified when you earn XP and your missions are approved.")
    return embed

def getWelcomeEmbed():
    embed=discord.Embed(title="**Welcome to Jackpot**",description="Jackpot is a simple, no-brainer loyalty and rewards program architected in collaboration with 100+ web3 industry veterans including founders, community managers, mods, and core contributors across the Ethereum and Solana ecosystems.\n\nEarn XP to climb the leaderboard and have a chance at winning the **Jackpot Raffle.**\n\n**1 XP = 1 Raffle Ticket**", color=0x33FF5C)
    return embed

def getWelcomeOptInEmbed():
    embed=discord.Embed(title="**Welcome to Jackpot!**",description="Jackpot is a simple, no-brainer loyalty and rewards program architected in collaboration with 100+ web3 industry veterans including founders, community managers, mods, and core contributors across the Ethereum and Solana ecosystems.\n\nEarn XP to climb the leaderboard and have a chance at winning the **Jackpot Raffle.**\n\n**1 XP = 1 Raffle Ticket**", color=0x33FF5C)
    return embed

def getTwitterOAUTHEmbed():
    embed=discord.Embed(title="**Verify Twitter Account Ownership**", description="To opt-in, you must link your Twitter account. Follow the steps below to get your Twitter OAUTH code", color=0x1da1f2)
    embed.add_field(name="**Steps:**", value = "\n1. Go to the [Twitter OAuth Authorization](https://twitter.com/home) page and authorize the app using your Twitter account.\n2. Copy the *one-time pincode* provided and submit it via the `Verify Twitter` button below.", inline=False)
    return embed

def getLeaderboardURL():
    embed=discord.Embed(title="**📈 View the leaderboard 📈**", description="\nClick [here](https://getjackpot.xyz) to view the live leaderboard!", color=0x1da1f2)
    return embed

def getMissionsEmbed():
    embed=discord.Embed(title="Missions 🗺️", description = "Missions are the easiest way to rack up XP. Head over to #missions to view the available missions and submit proof of your work. Once approved by your community's admin, you'll receive XP for your contribution.", color=0xe9e9e9)
    return embed

def getCommandsEmbed():
    embed=discord.Embed(title="**🤖 Discord Commands 🤖**", description = "👉 *Type `!rank` to see your XP earned and position on the leaderboard.*\n👉 *Type `!rank/username` to see someone else's position on the leaderboard.*\n👉 *Type `!leaderboard` to visit the Jackpot website.*\n👉 *Type `!jackpot` to see the upcoming Jackpot.*\n👉 *Type `!update` to edit your information and wallet ID.*", color=0xe9e9e9)
    return embed

def getLeaderboardInformation():
    string = "** **\n** **📈 💰  __**[Doodles Community Leaderboard](https://getjackpot.xyz/leaderboard/doodles/)**__ 💰 📈\n🏘️  *[Community Leaderboard](https://getjackpot.xyz/leaderboard/doodles/)*   |   🌎  *[Global Leaderboard](https://getjackpot.xyz/leaderboard/)*\n*Last updated: 10/20/22 at 10:51 am EST*\n\n💰 Current Jackpot Size: `1,000 USDC`     ⏱️ Date of Next Drawing: `Nov. 4th @ 9:05pm EST`\n✋ # of Community Participants: `65`       ✋ # of Global Participants: `195`\n\n----------------\n\n        🏆   **__1.__**  🥇  **cryptobreaky    *[Twitter Profile](https://twitter.com/cryptobreaky)*   ~   🎟️ *[48800 XP](https://getjackpot.xyz/cryptobreaky)*\n\n        🏆   **__2.__**  🥈  **LanDAO Calrissian    (*[Twitter Profile](https://twitter.com/cryptobreaky)*)   ~   🎟️ *[46500 XP](https://getjackpot.xyz/cryptobreaky)***\n\n        🏆   **__3.__**  🥉  **Ashh    (*[Twitter Profile](https://twitter.com/cryptobreaky)*)   ~   🎟️ *[44700 XP](https://getjackpot.xyz/cryptobreaky)***\n\n        🏆   **__4.__**  ✨  **crypto_King    (*[Twitter Profile](https://twitter.com/cryptobreaky)*)   ~   🎟️ *[42800 XP](https://getjackpot.xyz/cryptobreaky)***\n\n        🏆   **__5.__**  ✨  **RatheSunGod    (*[Twitter Profile](https://twitter.com/cryptobreaky)*)   ~   🎟️ *[39500 XP](https://getjackpot.xyz/cryptobreaky)***\n\n        ✨   **Type *!rank* in any channel to see your current stats.**\n\n----------------\n\n👉 *Type `!rank ` to see your own stats.*\n👉 *Type `!rank/username` to see someone else's stats.*\n👉 *Type `!leaderboard ` to preview the Community Leaderboard.*\n👉 *Type `!global ` to preview the Global Leaderboard.*\n👉 *Type `!jackpot ` to see the upcoming Jackpot.*\n👉 *Go to [getjackpot.xyz](https://getjackpot.xyz/) to see the full leaderboards.*\n** **\n** **"
    return string

def getFullLeaderboardEmbed():
    embed = discord.Embed(title="Leaderboard", description=getLeaderboardInformation(), color=0xe9e9e9)
    return embed

def getLeaderboardEmbed():
    embed = discord.Embed(title="📈 The Leaderboard 📈", description="Check the leaderboard to see the most valuable contributors in your community and beyond!", color=0xe9e9e9)
    return embed

def getTwitterEmbed(link, retweet, react, comment, boosted=False):
    xp = 0
    retweetStr, reactStr, commentStr = "`ineligible for this Raid`", "`ineligible for this Raid`", "`ineligible for this Raid`"
        
    if boosted:
        if retweet:
            xp += 600
            retweetStr = "`1200 XP 🎟️ (BOOSTED)`"
        if react:
            xp += 200
            reactStr = "`400 XP 🎟️ (BOOSTED)`"
        if comment:
            xp += 400
            commentStr = "`800 XP 🎟️ (BOOSTED)`"
    
        mcolor = 0xf21d6a
        message = "**Engage** with the **Tweet** below to earn up to **"+ str(xp * 2) +" XP**\n\n🚨 **THIS RAID IS BOOSTED -- EARN 200% XP!** 🚨\n\nLike = "+ reactStr + "\nReply = "+ commentStr +"\nRetweet = "+retweetStr+"\n\n⛓ __**" + link + "**__ ⛓"
    else:
        if retweet:
            xp += 600
            retweetStr = "`600 XP 🎟️`"
        if react:
            xp += 200
            reactStr = "`200 XP 🎟️`"
        if comment:
            xp += 400
            commentStr = "`400 XP 🎟️`"
            
        mcolor = 0x1da1f2
        message = "**Engage** with the **Tweet** below to earn up to **"+ str(xp) +"**\n\nLike = "+ reactStr + "\nReply = "+ commentStr +"\nRetweet = "+retweetStr+"\n\n⛓ __**" + link + "**__ ⛓\n"
    embed=discord.Embed(title="**RAID ALERT**", description=message, color=mcolor)
    embed.set_author(name="Twitter Raid Rewards", icon_url="https://img.icons8.com/color/344/twitter--v1.png")
    embed.set_footer(text="Powered by Jackpot", icon_url="https://static.wixstatic.com/media/cdc018_603e1fc27c6a4c71b2c8c333f66c858b~mv2.png")
    return embed

def getMissionsEmbed():
    embed=discord.Embed(title="**🗺️ Missions 🗺️**", description="Click the **View Missions** button below to see your community's active missions and their respective XP rewards.", color=0xf21d6a)
    embed.add_field(name="**Submitting Mission Completion**", value="To get credit (XP) for completing a mission, in the message section below, type `/complete` followed by the mission id and your description (proof) of completion. If you click +1 more, you can add a screenshot to supplement the proof of completion provided.\n\n➡️ **Select an active mission from the dropdown to view its details.**", inline=False) 
    return embed

def raidSuccessfulEmbed(name, link, typeRaid):
    embed = discord.Embed(title="**🎉 New raid created! 🎉**", description="`" + name + "` was launched successfully", color=0x1da1f2)
    embed.add_field(name="Details:", value="**Link:** `" + name + "`\n**Type:** " + typeRaid, inline=False)
    embed.set_footer(text="Powered by Jackpot", icon_url="https://static.wixstatic.com/media/cdc018_603e1fc27c6a4c71b2c8c333f66c858b~mv2.png")
    return embed
    
def getMissionDetailsEmbed(title, description, xp, count, supply, personLimit, timesSubmitted):
    embed=discord.Embed(title="**🗺️ " + title + " 🗺️**", description=description, color=0xf21d6a)
    embed.add_field(name="**Mission Information**", value="**PAYOUT:** `" + str(xp) + " XP 🎟️`", inline=False)
    ## THESE FIELDS ARE NOT NEEDED FOR NOW ##
    ##embed.add_field(name="**Mission Information**", value="**XP PAYOUT:** `" + str(xp) + "` \n **REWARDS DISTRIBUTED SO FAR:** `" + str(count) + " out of " + str(supply) + "` \n", inline=False) 
    ##embed.add_field(name="**Submissions**", value="`You earned XP for this mission " + str(timesSubmitted) + " of a maximum of " + str(personLimit) + " times`", inline=False) 
    embed.set_footer(text="Powered by Jackpot", icon_url="https://static.wixstatic.com/media/cdc018_603e1fc27c6a4c71b2c8c333f66c858b~mv2.png")
    return embed

def alreadyOptIn(userSettings):
    embed=discord.Embed(title="**You're all set!**", description="You have already successfully opted in to Jackpot!", color=0x33FF5C)
    embed.add_field(name="**Next Steps:**", value="Navigate to <#" + str(userSettings) + "> to update your profile and learn more about the rewards Jackpot offers.", inline=False) 
    embed.set_footer(text="Powered by Jackpot", icon_url="https://static.wixstatic.com/media/cdc018_603e1fc27c6a4c71b2c8c333f66c858b~mv2.png")
    return embed

def noOptIn(getStarted):
    embed = discord.Embed(title="**⛔ You haven't opted in yet ⛔**", description="The operation you are trying to do is restricted to opted-in members of Jackpot.", color=0xFF3333)
    embed.add_field(name="**How to opt-in:**", value="Navigate to <#" + str(getStarted) + "> to learn more about the rewards Jackpot offers and opt-in.", inline=False) 
    embed.set_footer(text="Powered by Jackpot", icon_url="https://static.wixstatic.com/media/cdc018_603e1fc27c6a4c71b2c8c333f66c858b~mv2.png")
    return embed

def errorEmbed(message):
    embed = discord.Embed(title="**Sorry, something went wrong on our end**", description=message, color=0xFF3333)
    embed.set_footer(text="Powered by Jackpot", icon_url="https://static.wixstatic.com/media/cdc018_603e1fc27c6a4c71b2c8c333f66c858b~mv2.png")
    return embed

def userErrorEmbed(title, message):
    embed = discord.Embed(title="**" + title + "**", description=message, color=0xFF3333)
    embed.set_footer(text="Powered by Jackpot", icon_url="https://static.wixstatic.com/media/cdc018_603e1fc27c6a4c71b2c8c333f66c858b~mv2.png")
    return embed

def getMissionsListEmbed(numMissions):
    embed=discord.Embed(title="✅ **Mission Complete** ✅", description="In this channel, use `!verify [MISSION_NAME] [additional details or explaination]` to submit proof of a specific mission. If you are attaching a picture, attach it to the same message.", color=0xe9e9e9)
    embed.add_field(name="**Use the dropdown to see Active Missions**", value=str(numMissions) + " missions are active", inline=False)
    embed.set_footer(text="\n\nOnce submitted, a community admin will be able to approve/deny your submission. If approved, you'll receive XP for your effort and will be notified in #notifs.") 
    return embed

def getMissionsDropdownOptions(serverID):
    optionsList = []
    allMissions = api.getMissions(serverID)
    
    for mission in allMissions:
        missionDis = mission[1]
        if len(missionDis) > 30:
            missionDis = missionDis[:27] + "..."
            
        optionsList.append(discord.SelectOption(label=mission[0], description=missionDis, emoji="🟢"))
        
    return optionsList, allMissions

def falseLink(link):
    ## check to see if the link follows the above format
    ## 1) Starts with twitter.com
    ## 2) Has any profile name
    ## 3) Has a /status/
    ## 4) Has a number at the end
    
    regexOpt = r"^https?:\/\/twitter\.com\/[a-zA-Z0-9_]+\/status\/[0-9]+$"
    if re.match(regexOpt, link):
        return False
    else:
        return True
    
@client.event
async def on_ready():
    print("Logged in")
    serverID = client.guilds[0].id
    serverName = client.guilds[0].name
    
    serverProfile = client.guilds[0].icon.url
    api.addServer(serverID, serverName, serverProfile)
    
    ## if the Jackpot role doesn't exist, create it
    if discord.utils.get(client.guilds[0].roles, name=JACKPOT_ROLE) == None: 
        await client.guilds[0].create_role(name=JACKPOT_ROLE, color=discord.Color.from_rgb(235, 249, 0), hoist=False)
        
    ## if the Jackpot Non Opt role doesn't exist, create it
    if discord.utils.get(client.guilds[0].roles, name=JACKPOT_NON_OPT) == None:
        await client.guilds[0].create_role(name=JACKPOT_NON_OPT, color=discord.Color.from_rgb(255, 110, 110), hoist=False)
    
    guild = client.guilds[0]
    
    ## give everyone the Jackpot Non Opt role if they dont have the Jackpot role already
    for member in guild.members:
        if discord.utils.get(member.roles, name=JACKPOT_NON_OPT) == None and discord.utils.get(member.roles, name=JACKPOT_ROLE) == None and discord.utils.get(member.roles, name=BOT_ROLE) == None:
            await member.add_roles(discord.utils.get(guild.roles, name=JACKPOT_NON_OPT))
            
    ## create Guild categories if they don't exist, REG_GUILD and ADMIN_GUILD
    if discord.utils.get(guild.categories, name=REG_GUILD) == None:
        await guild.create_category(REG_GUILD)
    if discord.utils.get(guild.categories, name=ADMIN_GUILD) == None:
        await guild.create_category(ADMIN_GUILD)
    
    ## if any of the channels in prepChannels exist, delete them
    prepChannels = ["get-started", "user-settings", "leaderboard", "raids", "missions", "add-mission", "mission-approval", "launch-raid", "notifs"]
    for channel in prepChannels:
        if discord.utils.get(guild.channels, name=channel) != None:
            if channel != "notifs":
                await discord.utils.get(guild.channels, name=channel).delete()
            else:
                ## send a messgae in notifs that the bot is restarting
                await discord.utils.get(guild.channels, name=channel).send("🤖 **Jackpot Bot is restarting, this event has been logged** 🤖")
    
    ## Make #opt-in, #guide avalible to everyone
    # channels = ["opt-in", "guide"]
    channels = ["get-started"]
    for channel in channels:
        if discord.utils.get(guild.channels, name=channel) == None:
            await guild.create_text_channel(channel, category=discord.utils.get(guild.categories, name=REG_GUILD))
            await discord.utils.get(guild.channels, name=channel).set_permissions(guild.default_role, read_messages=False, send_messages=False)   
            await discord.utils.get(guild.channels, name=channel).set_permissions(discord.utils.get(guild.roles, name=BOT_ROLE), read_messages=True, send_messages=True)
            await discord.utils.get(guild.channels, name=channel).set_permissions(discord.utils.get(guild.roles, name=ADMIN_ROLE), read_messages=True, send_messages=True)
            await discord.utils.get(guild.channels, name=channel).set_permissions(discord.utils.get(guild.roles, name=JACKPOT_NON_OPT), read_messages=True, send_messages=False)
    
    ## make the channel #user-settings visible to everyone in the "Jackpot" role
    channels = ["user-settings"]
    for channel in channels:
        if discord.utils.get(guild.channels, name=channel) == None:
            await guild.create_text_channel(channel, category=discord.utils.get(guild.categories, name=REG_GUILD))
            await discord.utils.get(guild.channels, name=channel).set_permissions(guild.default_role, read_messages=False)   
            await discord.utils.get(guild.channels, name=channel).set_permissions(discord.utils.get(guild.roles, name=BOT_ROLE), read_messages=True, send_messages=True)
            await discord.utils.get(guild.channels, name=channel).set_permissions(discord.utils.get(guild.roles, name=ADMIN_ROLE), read_messages=True, send_messages=True)
            await discord.utils.get(guild.channels, name=channel).set_permissions(discord.utils.get(guild.roles, name=JACKPOT_ROLE), read_messages=True, send_messages=False)
    
    ## make the following channels visible to everyone in the "Jackpot" role they don't exist: #leaderboard, #raids, #missions, #mission-complete, #notifs
    channels = ["leaderboard", "raids", "missions", "notifs"]
    for channel in channels:
        if discord.utils.get(guild.channels, name=channel) == None:
            await guild.create_text_channel(channel, category=discord.utils.get(guild.categories, name=REG_GUILD))
            await discord.utils.get(guild.channels, name=channel).set_permissions(guild.default_role, read_messages=False)
            await discord.utils.get(guild.channels, name=channel).set_permissions(discord.utils.get(guild.roles, name=BOT_ROLE), read_messages=True, send_messages=True)
            await discord.utils.get(guild.channels, name=channel).set_permissions(discord.utils.get(guild.roles, name=ADMIN_ROLE), read_messages=True, send_messages=True)
            if channel != "mission-complete":
                await discord.utils.get(guild.channels, name=channel).set_permissions(discord.utils.get(guild.roles, name=JACKPOT_ROLE), read_messages=True)
            else:
                await discord.utils.get(guild.channels, name=channel).set_permissions(discord.utils.get(guild.roles, name=JACKPOT_ROLE), read_messages=False, send_messages=True)
    
    ## Create a get-started channel
    class optInstructions(discord.ui.View):
        def __init__(self):
            super().__init__()
            self.value = None
            self.timeout = VIEW_TIMEOUT
        @discord.ui.button(label="Get Started", style=discord.ButtonStyle.green)
        async def optin(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
            class optIn(discord.ui.View):
                def __init__(self):
                    super().__init__()
                    self.value = None
                    self.timeout = VIEW_TIMEOUT
                @discord.ui.button(label="Verify Twitter", style=discord.ButtonStyle.green)
                async def optin(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
                    if discord.utils.get(guild.roles, name=JACKPOT_ROLE) in interaction.user.roles:
                        userSettings = discord.utils.get(guild.channels, name="user-settings").id
                        await interaction.response.send_message(embed=alreadyOptIn(userSettings), ephemeral=True)
                    else:
                        await interaction.response.send_modal(optInModal())
            if discord.utils.get(guild.roles, name=JACKPOT_ROLE) in interaction.user.roles:
                userSettings = discord.utils.get(guild.channels, name="user-settings").id
                await interaction.response.send_message(embed=alreadyOptIn(userSettings), ephemeral=True)
            else:
                await interaction.response.send_message(embed=getTwitterOAUTHEmbed(), view=optIn(), ephemeral=True)
    
    class optInModal(ui.Modal, title = "Twitter OAuth Code"):
        tweeterHandle = ui.TextInput(label = "Verify and link your account", style=discord.TextStyle.short, placeholder="Copy and paste your OAuth code here", required = True)
        walletID = ui.TextInput(label = "Enter your Ethereum wallet address (Optional)", style=discord.TextStyle.short, placeholder="Jackpot winnings won't be awarded if blank", required = False)
        async def on_submit(self, interaction: discord.Interaction):
            
            ## if JACKPOT ROLE, return
            if discord.utils.get(guild.roles, name=JACKPOT_ROLE) in interaction.user.roles:
                channelID = discord.utils.get(guild.channels, name="user-settings").id
                await interaction.response.send_message(embed=alreadyOptIn(channelID), ephemeral=True)
            
            else:
                ## DO TWITTER API CALL HERE
                handle = self.tweeterHandle.value
                ##
                
                walledID = self.walletID.value
                server = interaction.guild.id
                memberName = interaction.user.name
                profilePic = interaction.user.avatar
                if profilePic == None or profilePic == "":
                    profilePic = "None"
                else:
                    profilePic = interaction.user.avatar.url
                memIDNum = interaction.user.id
                memberID = interaction.user.name + "#" + interaction.user.discriminator
                if api.optInMember(server, memberID, memIDNum, memberName, profilePic, handle, walledID):
                    ## create an XP event
                    api.xpEvent(server, memberID, 0)
                    reward = api.getReward(server, memberName, 0)
                    ## put on the notifs channel that a user has opted in
                    await discord.utils.get(guild.channels, name="notifs").send("✅ **" + str(interaction.user) + "** has opted in and earned " + reward + "!")
                    
                    ## DEPRECATED: assign the Jackpot role to the user
                    ## await interaction.response.send_message(content="✅ **Success!**\n\nYou have now successfully opted in to Jackpot and have been awarded `1000 XP 🎟️` as a token of our gratitude. You are now ready to begin earning XP for the value you bring to the table.", ephemeral=True)
                    await interaction.user.add_roles(discord.utils.get(guild.roles, name=JACKPOT_ROLE))
                    await interaction.user.remove_roles(discord.utils.get(guild.roles, name=JACKPOT_NON_OPT))
                    
                    ## if user submits a wallet ID, show the getOptIn() embed
                    if walledID != "" and walledID != None:
                        await interaction.response.send_message(embed=getOptIn(), ephemeral=True)
                    else:
                        channelID = discord.utils.get(guild.channels, name="user-settings").id
                        await interaction.response.send_message(embed=getOptInNoWallet(channelID), ephemeral=True)
                else:
                    await interaction.response.send_message(embed=errorEmbed("We were unable to complete the opt-in process at this time. Please try again later."), ephemeral=True)
                    
    if discord.utils.get(guild.channels, name="get-started").last_message == None or discord.utils.get(guild.channels, name="get-started").last_message.author != client.user:
        ## in the get started channel, send the gif located at Assets/Get Started.gif
        await discord.utils.get(guild.channels, name="get-started").send(file=discord.File("Assets/Get Started.gif"))
        
        ## send other messages
        await discord.utils.get(guild.channels, name="get-started").send(embed=getWelcomeEmbed())
        await discord.utils.get(guild.channels, name="get-started").send(embed=getXPEmbed())
        await discord.utils.get(guild.channels, name="get-started").send(embed=getChannelsEmbed())
        await discord.utils.get(guild.channels, name="get-started").send(embed=getCommandsEmbed())
        await discord.utils.get(guild.channels, name="get-started").send(embed = getIntroEmbed(), view = optInstructions())
    
    
    ## in #user-settings channel, send information from #get-started along with user settings embeds
    class viewCode(discord.ui.View):
        def __init__(self):
            super().__init__()
            self.value = None
            self.timeout = VIEW_TIMEOUT
        @discord.ui.button(label="View your code", style=discord.ButtonStyle.green)
        async def referal(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
            ## defer the interaction
            await interaction.response.defer()
            memberID = interaction.user.name + "#" + interaction.user.discriminator
            memberObject = api.getMember(interaction.guild.id, memberID)
            refCode = memberObject.referal
            if refCode == None:
                refCode = api.createAlphaNumericCode(interaction.guild.id, memberID)
                memberObject.referal = refCode
            
            ## await interaction.response.send(content="Your referral code is: `" + refCode + "`", ephemeral=True)
            ## send the referral code to the defered interaction
            await interaction.followup.send(content="Your referral code is: `" + refCode + "`", ephemeral=True)
                
    class multipler(discord.ui.View):
        def __init__(self):
            super().__init__()
            self.value = None
            self.timeout = VIEW_TIMEOUT
        @discord.ui.button(label="Claim XP Multiplier", style=discord.ButtonStyle.green)
        async def referal(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
            memberID = interaction.user.name + "#" + interaction.user.discriminator
            memberObject = api.getMember(interaction.guild.id, memberID)
            
            await interaction.response.send_message(content="This interaction is not yet avalible", ephemeral=True)
       
    class updateInfo(discord.ui.View):
        def __init__(self):
            super().__init__()
            self.value = None
            self.timeout = VIEW_TIMEOUT
        @discord.ui.button(label="Update Information", style=discord.ButtonStyle.green)
        async def update(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
            memberID = interaction.user.name + "#" + interaction.user.discriminator
            userObject = api.getMember(interaction.guild.id, memberID)
            walletAddress = userObject.wallet
            if walletAddress == None or walletAddress == "":
                walletAddress = "NONE SET"
            handle = None
            class updateInfo(ui.Modal, title = "Update your profile"):
                walletID = ui.TextInput(label = "Update your Ethereum wallet address", style=discord.TextStyle.short, default=str(walletAddress), required = True)
                async def on_submit(self, interaction: discord.Interaction):
                    walletNum = self.walletID.value
                    userObject.updateInfo(handle, walletNum)
                    await interaction.response.send_message("Profile updated!", ephemeral=True)    
            await interaction.response.send_modal(updateInfo())      
           
    if discord.utils.get(guild.channels, name="user-settings").last_message == None or discord.utils.get(guild.channels, name="user-settings").last_message.author != client.user:
        await discord.utils.get(guild.channels, name="user-settings").send(embed=getWelcomeOptInEmbed())
        await discord.utils.get(guild.channels, name="user-settings").send(embed=getXPEmbed())
        await discord.utils.get(guild.channels, name="user-settings").send(embed=getChannelsEmbed())
        await discord.utils.get(guild.channels, name="user-settings").send(embed=getCommandsEmbed())
        await discord.utils.get(guild.channels, name="user-settings").send(embed = getReferalEmbed(), view = viewCode())
        ## Individual Multiplier offline 
        ## await discord.utils.get(guild.channels, name="user-settings").send(embed = getMultiplierEmbed(), view = multipler())
        await discord.utils.get(guild.channels, name="user-settings").send(embed = getUpdateEmbed(), view = updateInfo())
    
    ## in the leaderboard channel, send a leaderboard message
    if discord.utils.get(guild.channels, name="leaderboard").last_message == None or discord.utils.get(guild.channels, name="leaderboard").last_message.author != client.user:
        await discord.utils.get(guild.channels, name="leaderboard").send(file=discord.File("Assets/main.gif"))
        class printLeaderboard(discord.ui.View):
            def __init__(self):
                super().__init__()
                self.value = None
                self.timeout = VIEW_TIMEOUT
            @discord.ui.button(label="🏆 View Leaderboard 🏆", style=discord.ButtonStyle.green)
            async def optin(self, interaction: discord.Interaction, button: discord.ui.Button):
                await interaction.response.send_message(embed=getFullLeaderboardEmbed(), ephemeral=True)
        await discord.utils.get(guild.channels, name="leaderboard").send(embed = getLeaderboardEmbed(), view = printLeaderboard())
        
    ## DEPRECATED: in the raids channel, sent a twitter raid embed for both boosted and normal
    ##if discord.utils.get(guild.channels, name="raids").last_message == None or discord.utils.get(guild.channels, name="raids").last_message.author != client.user:
        ##await discord.utils.get(guild.channels, name="raids").send(file=discord.File("Assets/Raids.gif"))
        #await discord.utils.get(guild.channels, name="raids").send(embed=getTwitterEmbed("TEST", False))
        #await discord.utils.get(guild.channels, name="raids").send(embed=getTwitterEmbed("TEST", True))
    
    ## DEPRECATED: send the mission-complete gif
    ##if discord.utils.get(guild.channels, name="mission-complete").last_message == None or discord.utils.get(guild.channels, name="mission-complete").last_message.author != client.user:
    ##    await discord.utils.get(guild.channels, name="mission-complete").send(file=discord.File("Assets/Mission Approval.gif"))
    
    ## DEPRECATED: send the notifs gif
    ##if discord.utils.get(guild.channels, name="notifs").last_message == None or discord.utils.get(guild.channels, name="notifs").last_message.author != client.user:
    ##    await discord.utils.get(guild.channels, name="notifs").send(file=discord.File("Assets/XP Log.gif"))
    
    ## in the missions channel, send an getMissionsEmbed() embed with a button 
    if discord.utils.get(guild.channels, name="missions").last_message == None or discord.utils.get(guild.channels, name="missions").last_message.author != client.user:
        await discord.utils.get(guild.channels, name="missions").send(file=discord.File("Assets/Missions.gif"))
        class missions(discord.ui.View):
            def __init__(self):
                super().__init__()
                self.value = None
                self.timeout = VIEW_TIMEOUT
            @discord.ui.button(label="View Missions", style=discord.ButtonStyle.green)
            async def onButtonClick(self, interaction: discord.Interaction, button: discord.ui.Button):
                class viewMission(discord.ui.View):
                    def __init__(self):
                        super().__init__()
                        self.value = None
                        self.timeout = VIEW_TIMEOUT
                    theOptions, theValues = getMissionsDropdownOptions(serverID)
                    @discord.ui.select(placeholder="Select a Mission", options=theOptions)
                    async def on_select(self, interaction: discord.Interaction, select: discord.ui.Select):
                        userID = interaction.user.name + "#" + interaction.user.discriminator
                        selectedMission = select.values[0]
                        __, theValues = getMissionsDropdownOptions(serverID)
                        for missions in theValues:
                            if missions[0] == selectedMission:
                                numSub = api.getNumMissionSubmissions(serverID, missions[0], userID)
                                await interaction.response.send_message(embed=getMissionDetailsEmbed(missions[0], missions[1], missions[2], missions[4], missions[3], missions[6], numSub), ephemeral=True)
                                break

                await interaction.response.send_message("Select a mission to view:", view=viewMission(), ephemeral=True)
                
        await discord.utils.get(guild.channels, name="missions").send(embed=getMissionsEmbed(), view=missions())
        
    ## DEPRECATED: in the mission-complete, send an getMissionsListEmbed() embed
    ##if discord.utils.get(guild.channels, name="mission-complete").last_message == None or discord.utils.get(guild.channels, name="mission-complete").last_message.author != client.user:
    ##numCount = len(api.getMissions(serverID))
    ##embedMessage = await discord.utils.get(guild.channels, name="mission-complete").send(embed=getMissionsListEmbed(numCount))
    
    ## DEPRECATED: pin the message
    ## await embedMessage.pin()
    
    ## make the following channels visible to only Admins if they don't exist: #add-mission, #mission-approval, #launch-raid
    channels = ["add-mission", "mission-approval", "launch-raid"]
    for channel in channels:
        if discord.utils.get(guild.channels, name=channel) == None:
            await guild.create_text_channel(channel, category=discord.utils.get(guild.categories, name=ADMIN_GUILD))
            await discord.utils.get(guild.channels, name=channel).set_permissions(guild.default_role, read_messages=False)
            await discord.utils.get(guild.channels, name=channel).set_permissions(discord.utils.get(guild.roles, name=BOT_ROLE), read_messages=True, send_messages=True)
            await discord.utils.get(guild.channels, name=channel).set_permissions(discord.utils.get(guild.roles, name=ADMIN_ROLE), read_messages=True, send_messages=True)
    ## in the add-mission, send a message and 3 buttons: Add Quest, Edit Quest, Delete Quest
    if discord.utils.get(guild.channels, name="add-mission").last_message == None or discord.utils.get(guild.channels, name="add-mission").last_message.author != client.user:
        await discord.utils.get(guild.channels, name="add-mission").send(file=discord.File("Assets/Add Mission.gif"))
        
        class addQuest(ui.Modal, title = "Add Mission Form"):
            name = ui.TextInput(label = "Mission Name", style=discord.TextStyle.short, placeholder = "Mission Name", required = True)
            desc = ui.TextInput(label = "Mission Description", style=discord.TextStyle.large, placeholder = "Mission Description", required = True)
            reward = ui.TextInput(label = "Mission Reward (XP)", style=discord.TextStyle.short, placeholder = "e.g. 400", required = True)
            supply = ui.TextInput(label = "Mission Total Supply (Optional)", style=discord.TextStyle.short, placeholder = "Default: Unlimited", required = False)
            perperson = ui.TextInput(label = "Mission Supply Per Person (Optional)", style=discord.TextStyle.short, placeholder = "Default: Unlimited", required = False)
            
            async def on_submit(self, interaction: discord.Interaction):
                serverID = interaction.guild.id
                lowerCaseName = self.name.value.lower().strip().replace(" ", "_")
                randID = api.createMission(serverID, lowerCaseName, self.desc.value, self.reward.value, self.supply.value, self.perperson.value)
                
                await interaction.response.send_message(content="A Mission was successfully added: **" + str(self.name) + "**", ephemeral=False)
            
        class quests(discord.ui.View):
            def __init__(self):
                super().__init__()
                self.value = None
                self.timeout = VIEW_TIMEOUT
            @discord.ui.button(label="Add Mission", style=discord.ButtonStyle.green)
            async def but1(self, interaction: discord.Interaction, button: discord.ui.Button):
                await interaction.response.send_modal(addQuest())
            @discord.ui.button(label="Edit Mission", style=discord.ButtonStyle.primary)
            async def but2(self, interaction: discord.Interaction, button: discord.ui.Button):
                theOptions, __ = getMissionsDropdownOptions(serverID)
                
                class editSelector(discord.ui.View):
                    def __init__(self):
                        super().__init__()
                        self.value = None
                        self.timeout = VIEW_TIMEOUT
                    @discord.ui.select(placeholder="Select a Mission", options=theOptions)
                    async def on_select(self, interaction: discord.Interaction, select: discord.ui.Select):
                        selectedMission = select.values[0]
                        __, missionObject = api.getMission(serverID, selectedMission)
                        
                        class editExistingQuest(ui.Modal, title = "EDIT TASK MODAL"):
                            desc = ui.TextInput(label = "Mission Description", style=discord.TextStyle.short, default = str(missionObject.description), required = True)
                            reward = ui.TextInput(label = "Mission Reward (XP)", style=discord.TextStyle.short, default = str(missionObject.xp), required = True)
                            supply = ui.TextInput(label = "Mission Total Supply (Optional)", style=discord.TextStyle.short, default = str(missionObject.limit), required = False)
                            perperson = ui.TextInput(label = "Mission Supply Per Person (Optional)", style=discord.TextStyle.short, default = str(missionObject.personLimit), required = False)
                            
                            async def on_submit(self, interaction: discord.Interaction):
                                missionObject.description = self.desc.value
                                missionObject.xp = self.reward.value
                                if self.supply.value != "" and self.supply.value != None:
                                    missionObject.limit = self.supply.value
                                if self.perperson.value != "" and self.perperson.value != None:
                                    missionObject.personLimit = self.perperson.value
                                
                                await interaction.response.send_message(content="A Mission has been modifed", ephemeral=False)
                        await interaction.response.send_modal(editExistingQuest())
                        
                await interaction.response.send_message(content="Select a Mission you would like to edit", ephemeral=True, view=editSelector())
            
            @discord.ui.button(label="Delete Mission", style=discord.ButtonStyle.red)
            async def but3(self, interaction: discord.Interaction, button: discord.ui.Button):
                theOptions, theValues = getMissionsDropdownOptions(serverID)
                
                class deleteSelector(discord.ui.View):
                    def __init__(self):
                        super().__init__()
                        self.value = None
                        self.timeout = VIEW_TIMEOUT
                    @discord.ui.select(placeholder="Select a Mission to delete", options=theOptions)
                    async def on_select(self, interaction: discord.Interaction, select: discord.ui.Select):
                        selectedMission = select.values[0]
                        missionID, missionObject = api.getMission(serverID, selectedMission)
                        
                        class deleteExistingQuest(ui.Modal, title = "⚠️ DELETE MISSION ⚠️"):
                            deleteMe = ui.TextInput(label = "Type 'DELETE' below to permentantly delete " + selectedMission + ".", style=discord.TextStyle.short, placeholder = "This action can not be reversed.", required = False)
                            
                            async def on_submit(self, interaction: discord.Interaction):
                                if self.deleteMe.value == "DELETE":
                                    api.deleteMission(serverID, missionID)
                                    await interaction.response.send_message(content="A Mission has been deleted", ephemeral=True)
                                else:
                                    await interaction.response.send_message(content="The Mission has *not* been deleted. Please enter `DELETE` (case-sensitive) on the confirm pop-up.", ephemeral=True)
                                    await interaction.repsonse.send_embed(embed = userErrorEmbed("The Mission has *not* been deleted.", "Please enter `DELETE` (case-sensitive) on the delete pop-up to delete the **" + selectedMission + "** mission."), ephemeral = True)
                        
                        await interaction.response.send_modal(deleteExistingQuest())
                        
                await interaction.response.send_message(content="Select a Mission you would like to delete", ephemeral=True, view=deleteSelector())
                
        await discord.utils.get(guild.channels, name="add-mission").send(embed = getMissionAddEmbed(), view = quests())
    
    ## DEPRECATED: send a mission-approval gif in the mission-approval channel
    ##if discord.utils.get(guild.channels, name="mission-approval").last_message == None or discord.utils.get(guild.channels, name="mission-approval").last_message.author != client.user:
    ##    await discord.utils.get(guild.channels, name="mission-approval").send(file=discord.File("Assets/Mission Approval.gif"))
    
    ## in the launch-raid, send a message with 1 button: Launch Raid. Pressing the button will open a discord form to fill out
    if discord.utils.get(guild.channels, name="launch-raid").last_message == None or discord.utils.get(guild.channels, name="launch-raid").last_message.author != client.user:
        await discord.utils.get(guild.channels, name="launch-raid").send(file=discord.File("Assets/Launch Raid.gif"))
        class raids(discord.ui.View):
            def __init__(self):
                super().__init__()
                self.value = None
                self.timeout = VIEW_TIMEOUT
            @discord.ui.button(label="Launch Raid", style=discord.ButtonStyle.green)
            async def addRaid(self, interaction: discord.Interaction, button: discord.ui.Button):
                class raidSelector(discord.ui.View):
                    def __init__(self):
                        super().__init__()
                        self.value = None
                        self.timeout = VIEW_TIMEOUT
                    @discord.ui.select(placeholder="Select a Raid", min_values = 1, max_values = 3, options=[
                        discord.SelectOption(label="Retweet", default=True, description="Check if someone retweets a target tweet", emoji="📩"),
                        discord.SelectOption(label="React",default=True, description="See if a user reacts to a Tweet", emoji="❤️"), 
                        discord.SelectOption(label="Comment", default=True, description="Award points to users who leave a comment", emoji="📝")
                        ])
                    async def on_select(self, interaction: discord.Interaction, select: discord.ui.Select):
                        ## API CALL TO GET DATA
                        xpAwards = ""
                        class addRaid(ui.Modal, title = "Create a Twitter Raid"):
                            raidTitle = ui.TextInput(label = "Raid Title", style=discord.TextStyle.short, placeholder = "Name this Twitter Raid", required = True)
                            url = ui.TextInput(label = "Tweet URL", style=discord.TextStyle.short, placeholder = "What is the URL of a tweet", required = True)
                            #boosted = ui.TextInput(label = "Boosted XP", style=discord.TextStyle.short, placeholder = "True/False (Boosted Tweets earn 200% XP)", required = True)
                            async def on_submit(self, interaction: discord.Interaction):
                                ## DO API CALL HERE
                                link = self.url.value
                                raidTitle = self.raidTitle.value
                                boosted, retweet, react, comment = False, False, False, False
                                
                                #if "t" in self.boosted.value.lower():
                                #    boosted = True
                                
                                for value in select.values:
                                    if "retweet" in value.lower():
                                        retweet = True
                                        xpAwards += " `Retweet`"
                                    elif "react" in value.lower():
                                        react = True
                                        xpAwards += " `React`"
                                    elif "comment" in value.lower():
                                        comment = True
                                        xpAwards += " `Comment`"
                                
                                serverID = interaction.guild.id
                                tweetID = api.createTwitterRaid(serverID, raidTitle, link, boosted, retweet, react, comment)
                                
                                ## make a new view of 1 -3 buttons for retweeting, reacting, commenting
                                class raidView(discord.ui.View):
                                    def __init__(self):
                                        super().__init__()
                                        self.value = None
                                        self.timeout = VIEW_TIMEOUT
                                    @discord.ui.button(label="Claim Like XP", style=discord.ButtonStyle.primary)
                                    async def react(self, interaction: discord.Interaction, button: discord.ui.Button):
                                        serverName = interaction.guild.id
                                        userName = interaction.user.name
                                        userID = interaction.user.name + "#" + interaction.user.discriminator
                                        resp = api.tweetEventReact(serverName, userID, tweetID)
                                        if type(resp) == int:
                                            await discord.utils.get(interaction.guild.channels, name="notifs").send("🎉 " + userName + " reacted to " + api.getTweetTitle(serverName) + " and earned `" + str(resp) + " XP 🎟️`")
                                            await interaction.response.send_message(content="You have earned XP for reacting to this tweet", ephemeral=True)
                                        else:
                                            await interaction.response.send_message(content=resp, ephemeral=True)
    
                                    @discord.ui.button(label="Claim Reply XP", style=discord.ButtonStyle.green)
                                    async def comment(self, interaction: discord.Interaction, button: discord.ui.Button):
                                        serverName = interaction.guild.id
                                        userName = interaction.user.name
                                        userID = interaction.user.name + "#" + interaction.user.discriminator
                                        resp = api.tweetEventComment(serverName, userID, tweetID)
                                        if type(resp) == int:
                                            await discord.utils.get(interaction.guild.channels, name="notifs").send("🎉 " + userName + " commented to " + api.getTweetTitle(serverName) + " and earned " + str(resp) + " XP")
                                            await interaction.response.send_message(content="You have earned XP for commenting to this tweet", ephemeral=True)
                                        else:
                                            await interaction.response.send_message(content=resp, ephemeral=True)
                                            
                                    @discord.ui.button(label="Claim Retweet XP", style=discord.ButtonStyle.red)
                                    async def retweet(self, interaction: discord.Interaction, button: discord.ui.Button):
                                        serverName = interaction.guild.id
                                        userName = interaction.user.name
                                        userID = interaction.user.name + "#" + interaction.user.discriminator
                                        resp = api.tweetEventRetweet(serverName, userID, tweetID)
                                        if type(resp) == int:
                                            await discord.utils.get(interaction.guild.channels, name="notifs").send("🎉 " + userName + " retweeted " + api.getTweetTitle(serverName) + " and earned `" + str(resp) + " XP 🎟️`")
                                            await interaction.response.send_message(content="You have earned XP for retweeting this tweet", ephemeral=True)
                                        else:
                                            await interaction.response.send_message(content=resp, ephemeral=True)
                            
                                ## if link is blank, make an error message
                                if link == "" or falseLink(link):
                                    ## send a userErrorEmbed embed message
                                    await interaction.response.send_modal(userErrorEmbed("Raid Error: Tweet URL Not Valid", "Your new raid has not launched. To fix this issue, please enter a full valid tweet link, including `https://`"), ephemeral=True)
                                elif raidTitle == "":
                                    await interaction.response.send_modal(userErrorEmbed("Raid Error: Raid Title Not Valid", "Your new raid has not launched. To fix this issue, please enter a non-empty raid title"), ephemeral=True)
                                else:
                                    xpAwards = xpAwards.strip()
                                    await interaction.response.send_modal(raidSuccessfulEmbed(str(self.raidTitle.value), str(self.url.value), xpAwards), ephemeral=True)
                                    await discord.utils.get(guild.channels, name="raids").send(embed=getTwitterEmbed(str(self.url.value), retweet, react, comment, boosted), view=raidView())
                        await interaction.response.send_modal(addRaid())
                await interaction.response.send_message(content="Select the type of Raid you want (multiple can be picked)", ephemeral=True, view=raidSelector())
        
        await discord.utils.get(guild.channels, name="launch-raid").send(embed=getRaidsEmbed(), view = raids())
        
@client.event
async def on_message(message):
    try:
        serverName = message.guild.id
    except:
        serverName = None
    
    memberID = message.author.name + "#" + message.author.discriminator
    userName = message.author.name
    text = message.content
    
    if message.author == client.user:
        if serverName != None and message.content.startswith("FETCHING RANK..."):       
            try:
                memberID = messageData.split("#|#")[1].strip()
                serverRank, serverTrend, serverXP, globalRank, globalXP = api.getRank(serverName, memberID)
                await message.channel.send(embed=getRankEmbed(memberID, serverRank, globalRank, serverXP, globalXP))
            except:
                await message.channel.send("This user has not opted-in or does not exist. Make sure to enter the full username, ie `TheName#1234`")
        
        ## if a message is sent in the #missions channel, check if it starts with "MISSION SUBMITTED" 
        elif serverName != None and message.channel.name == "missions" and message.content.startswith("MISSION SUBMITTED"):
            messageData = message.content.split("#|#")
            memberID = messageData[1].strip()
            missionName = messageData[2].strip()
            textData = messageData[3].strip()
            if len(messageData) > 4:
                attachment = messageData[4].strip()
            else:
                attachment = "NO ATTACHMENT"
                
            activeMissions = api.getMissions(serverName)
            missionID = None
            
            def verifyMission(missionName):
                for mission in activeMissions:
                    if mission[0] == missionName:
                        missionID = mission[5]
                        return missionID
                return False
            
            missionID = verifyMission(missionName)
            eligible = api.checkMissionEligibility(serverName, memberID, missionID)
            
            if missionID != False and eligible:
                ## send a confirmation message to #mission-approval, delete it after 10 seconds: "mission submitted by " + str(message.author)
                newMessage = await discord.utils.get(message.guild.channels, name="notifs").send("🎉 Mission '"+missionName+"' submitted by " + memberID)
                await message.delete()
                
                class approveButtons(discord.ui.View):
                    def __init__(self):
                        super().__init__()
                        self.value = None
                        self.timeout = VIEW_TIMEOUT
                    @discord.ui.button(label="APPROVE", style=discord.ButtonStyle.green)
                    async def approve(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
                        missionReward = api.missionXPEvent(serverName, memberID, missionID)
                        if missionReward == False:
                            await interaction.response.send_message("MISSION **NOT** APPROVED \n Mission total limit or per person limit exceeded", ephemeral=True)
                            await newMessage.delete()
                        else:
                            await interaction.response.send_message("MISSION APPROVED", ephemeral=True)
                            ## delete the main message the button was pressed on
                            await interaction.message.delete()
                            ## delete newMessage
                            await newMessage.delete()
                            ## send a message to #notifs with the mission name, username, and XP
                            await discord.utils.get(message.guild.channels, name="notifs").send("🎉 Mission '"+missionName+"' completed by " + memberID + " for `" + str(missionReward) + " XP 🎟️`")
                        
                    @discord.ui.button(label="DENY", style=discord.ButtonStyle.red)
                    async def deny(self, interaction2: discord.Interaction, button: discord.ui.Button) -> None:
                        class feedbackMission(ui.Modal, title = "Send feedback to " + memberID[:12] + "..."):
                            feedback = ui.TextInput(label = "Reason why mission declined", style=discord.TextStyle.long, default = "You have not completed the mission spec", required = True)
                            async def on_submit(self, interaction: discord.Interaction):
                                await newMessage.reply("MISSION WAS DENIED BY ADMINS: " + str(self.feedback.value))
                                await interaction.response.send_message("MISSION DENIED", ephemeral=True)
                        await interaction2.response.send_modal(feedbackMission())
                        await interaction2.message.delete()
                
                missionReward = api.getMissionXP(serverName, missionID)
                await discord.utils.get(message.guild.channels, name="mission-approval").send("📬 **New Mission Submission** 📬\n\nFrom: `" + str(memberID) + "`\nMission: `" + missionName + "`\nReward: `" + str(missionReward) + " XP 🎟️`\nText: `" + textData + "`\n\n" + "Attachments: " + attachment + "\n\n" + "*Choose whether to **APPROVE** or **DENY** by reacting below:*", view = approveButtons())
                    
            else:
                if missionID == False:
                    await message.reply("Invalid mission name. Please try again (Case Sensitive).")
                else: 
                    await message.reply("You can no longer complete this mission. Either personal limit or global limit for XP rewards has been met. Please try again with a different mission.")
        else:
            return
    
    ## if the message is in a DM or in the bot channel, ignore it
    if api.checkOptIn(serverName, memberID) and message.guild != None and message.channel.name not in ["get-started", "leaderboard", "raids", "missions", "mission-complete", "notifs", "add-mission", "mission-approval", "launch-raid"] and text.startswith("!") == False:
        api.xpEvent(serverName, memberID, 1)
        if message.reference != None:
            originalAuthor = message.reference.resolved.author
            if api.checkOptIn(serverName, originalAuthor):
                api.xpEvent(serverName, originalAuthor, 6)        
        
    ## if someone messages the #missions-complete channel with command !verify then send a message to #mission-approval
    if message.channel.name == "mission-complete" and message.content.lower().startswith("!verify"):
        missionName = message.content.split(" ")[1]
        textMessage = message.content.split(" ")[2:]
        textMessage = " ".join(textMessage)
        
        activeMissions = api.getMissions(serverName)
        missionID = None
        
        def verifyMission(missionName):
            for mission in activeMissions:
                if mission[0] == missionName:
                    missionID = mission[5]
                    return missionID
            return False
        
        missionID = verifyMission(missionName)
        eligible = api.checkMissionEligibility(serverName, memberID, missionID)
        
        if missionID != False and eligible:
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
            newMessage = await discord.utils.get(message.guild.channels, name="notifs").send("🎉 Mission '"+missionName+"' submitted by " + author)
            ## delete newMessage after 10 seconds
            await message.delete()
            
            class approveButtons(discord.ui.View):
                def __init__(self):
                    super().__init__()
                    self.value = None
                    self.timeout = VIEW_TIMEOUT
                @discord.ui.button(label="APPROVE", style=discord.ButtonStyle.green)
                async def approve(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
                    missionReward = api.missionXPEvent(serverName, author, missionID)
                    if missionReward == False:
                        await interaction.response.send_message("MISSION **NOT** APPROVED \n Mission total limit or per person limit exceeded", ephemeral=True)
                        await newMessage.delete()
                    else:
                        await interaction.response.send_message("MISSION APPROVED", ephemeral=True)
                        ## delete the main message the button was pressed on
                        await interaction.message.delete()
                        ## delete newMessage
                        await newMessage.delete()
                        ## send a message to #notifs with the mission name, username, and XP
                        await discord.utils.get(message.guild.channels, name="notifs").send("🎉 Mission '"+missionName+"' completed by " + author + " for `" + str(missionReward) + " XP 🎟️`")
                    
                @discord.ui.button(label="DENY", style=discord.ButtonStyle.red)
                async def deny(self, interaction2: discord.Interaction, button: discord.ui.Button) -> None:
                    class feedbackMission(ui.Modal, title = "Send feedback to " + author[:12] + "..."):
                        feedback = ui.TextInput(label = "Reason why mission declined", style=discord.TextStyle.long, default = "You have not completed the mission spec", required = True)
                        async def on_submit(self, interaction: discord.Interaction):
                            await newMessage.reply("MISSION WAS DENIED BY ADMINS: " + str(self.feedback.value))
                            await interaction.response.send_message("MISSION DENIED", ephemeral=True)
                    await interaction2.response.send_modal(feedbackMission())
                    await interaction2.message.delete()
            
            missionReward = api.getMissionXP(serverName, missionID)
            await discord.utils.get(message.guild.channels, name="mission-approval").send("📬 **New Mission Submission** 📬\n\nFrom: `" + str(userName) + "`\nMission: `" + missionName + "`\nReward: `" + str(missionReward) + " XP 🎟️`\nText: `" + textMessage + "`\n\n" + attachmentString + "*Choose whether to **APPROVE** or **DENY** by reacting below:*", view = approveButtons())
                
        else:
            if missionID == False:
                await message.reply("Invalid mission name. Please try again (Case Sensitive).")
            else: 
                await message.reply("You can no longer complete this mission. Either personal limit or global limit for XP rewards has been met. Please try again with a different mission.")
            
    
    ## if someone DMs the bot '!rank' then send them their rank by calling api.getRank(username, serverName)
    if message.content.lower() == "!rank":
        ## see if user has role JACKPOT_ROLE
        if discord.utils.get(message.author.roles, name=JACKPOT_ROLE):
            serverRank, serverTrend, serverXP, globalRank, globalXP = api.getRank(serverName, memberID)
            await message.channel.send(embed=getRankEmbed(memberID, serverRank, globalRank, serverXP, globalXP))
        else: 
            await message.reply("To interact with me, opt-in via the `#opt-in` channel")
    ## if someone DMs the bot '!rank/username' then send them the rank of the user they specified by calling api.getRank(username, serverName)
    elif message.content.lower().startswith("!rank/"):
        try:
            await message.channel.send("`" + str(api.returnXP(serverName, message.content[6:])) + " XP`")
        except: 
            await message.channel.send("This user has not opted-in or does not exist. Make sure to enter the full username, ie `TheName#1234`")
    ## if someone DMs the bot '!leaderboard' then send them the leaderboard by calling api.getLeaderboard(serverName)
    elif message.content.lower() == "!leaderboard":
        await message.channel.send(api.getLeaderboard(serverName))
    ## if someone DMs the bot '!jackpot' then send them the jackpot message by calling api.getJackpot(serverName)
    elif message.content.lower() == "!jackpot":
        await message.channel.send(api.getJackpot(serverName))
    ## if someone DMs the bot '!help' then send them a list of commands they can use
    elif message.content.lower() == "!help":
        await message.channel.send("**📝 Here's a list of commands you can use 📝**\n\n**🏆 !rank** - get your rank\n**🎖️ !rank/{username}** - get the rank of a specific user\n**💯 !leaderboard** - get the leaderboard for this server\n**🌎 !global** - get the global leaderboard\n**💰 !jackpot** - get the jackpot for this server\n**💬 !help** - get a list of commands")
    elif message.content.lower() == "!update":
        if discord.utils.get(message.author.roles, name=JACKPOT_ROLE):
            userObject = api.getMember(serverName, memberID)
            walletAddress = userObject.wallet
            if walletAddress == None:
                walletAddress = "NONE SET"
            handle = None
            class updateInfr(ui.Modal, title = "Update your profile"):
                walletID = ui.TextInput(label = "Update your Ethereum wallet address", style=discord.TextStyle.short, placeholder=walletAddress, required = False)
                async def on_submit(self, interaction: discord.Interaction):
                    walletNum = self.walletID.value
                    userObject.updateInfo(handle, walletNum)
                    await interaction.response.send_message("Profile updated!", ephemeral=True)
            await message.reply("Update your profile", view = updateInfr())
        else: 
            await message.reply("To interact with me, opt-in via the `#opt-in` channel")
    
## create an event to see everytime a user reacts to a message
@client.event
async def on_raw_reaction_add(payload):
    serverName = payload.guild_id
    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    emoji = payload.emoji.name
    user = payload.member
    originalAuthor = message.author
    
    ## if the reaction is on a message in a bot channel and in a DM, ignore it
    if api.checkOptIn(serverName, user) and channel.name not in ["get-started", "leaderboard", "raids", "missions", "notifs", "add-mission", "mission-approval", "launch-raid"] and channel.type != discord.ChannelType.private:
        if originalAuthor != user:
            api.xpEvent(serverName, user, 2)
            if api.checkOptIn(serverName, originalAuthor):
                api.xpEvent(serverName, originalAuthor, 3)
    
## @client.event for when a member becomes active on the server
@client.event
async def on_member_update(before, after):
    serverName = after.guild.id
    userName = after.name
    
    ## if the user does not have the Jackpot role or the Jackpot Non-Opt-In role, then assign the Jackpot Non-Opt-In role and not a bot
    if not discord.utils.get(after.roles, name=JACKPOT_ROLE) and not discord.utils.get(after.roles, name=JACKPOT_NON_OPT) and discord.utils.get(after.roles, name=BOT_ROLE) == None:
        await after.add_roles(discord.utils.get(after.guild.roles, name=JACKPOT_NON_OPT))
    
    if api.checkOptIn(serverName, userName) and before.status != after.status:
        if after.status == discord.Status.online and api.serverVisit(serverName, userName):
            api.xpEvent(serverName, userName, 9)
            ## send a message in the notifs channel
            reward = api.getReward(serverName, userName, 9)
            await discord.utils.get(after.guild.channels, name="notifs").send("✅ **" + str(userName) + "** is active today and earned " + reward)
            
"""
DEPRECATED
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
"""

client.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)