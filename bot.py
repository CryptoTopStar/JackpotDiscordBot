import discord
from discord import ui, app_commands, AppCommandOptionType
from discord.ext import tasks, commands
from discord import Button, ButtonStyle
import api as api
import random 
from datetime import datetime
import asyncio
from multiprocessing import Process
import math
import pandas as pd
import twitterBridge as twitter
import logging
import re
import database

TIMMER = False
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
TOKEN = "MTAzNzYyOTMyMDIwMzYxNjI2Ng.GhpR78.NzFqeGnDD0IZdQCArpLiL5CSAmdLtPUZ0fvIuo"
client = discord.Client(intents=discord.Intents.all())
BOT_ROLE = "Jackpot Official"
ADMIN_ROLE = "Admin"
JACKPOT_ROLE = "Jackpot"
JACKPOT_NON_OPT = "Jackpot (Not Opted In)"
VIEW_TIMEOUT = 1000000000000000000000000
TASK_PATH = "./Cache/task.txt"

REG_GUILD =   "▬▬▬ Jackpot ▬▬▬"
ADMIN_GUILD = "▬▬▬ Jackpot Admin ▬▬▬"

def getRaidsEmbed():
    embed=discord.Embed(title="⚔️ **Launch Twitter Raid** ⚔️", description="Click the button below to **Launch a Twitter Raid**", color=0xFF3F33)
    embed.add_field(name="**You'll be asked to:**", value="**1. Choose Engagement Type:** Choose what type of engagement you'd like to incentivize.\n**2. Specify Tweet:** Paste the URL of the Tweet that you'd like to raid.\n", inline=False) 
    embed.set_footer(text="Powered by Jackpot", icon_url="https://static.wixstatic.com/media/cdc018_603e1fc27c6a4c71b2c8c333f66c858b~mv2.png")
    return embed

def getMissionAddEmbed():
    embed=discord.Embed(title="🗺️ **Quest Admin** 🗺️", description="Click the buttons below to interact with your **Quests**.", color=0xe9e9e9)
    embed.add_field(name="1. **Add Quest:**", value="Click \"Add Quest\" to activate a new quest for your community. \n\nYou'll be able to specify the objective for the quest and set an appropriate 🎟️'s reward for completion. The maximum possible reward for a single quest is `5,000 🎟️'s` and the minimum is `50 🎟️'s`. We suggest adding up to `15,000 🎟️'s` of quests to maximize output from your community.", inline=False)
    embed.add_field(name="2. **Edit Quest:**", value="Click \"Edit Quest\" to change the details for any active quest.", inline=False)
    embed.add_field(name="3. **Delete Quest:**", value="Click \"Delete Quest\" to delete an active quest.", inline=False)
    embed.set_footer(text="Powered by Jackpot", icon_url="https://static.wixstatic.com/media/cdc018_603e1fc27c6a4c71b2c8c333f66c858b~mv2.png")
    return embed

def getReferalEmbed():
    embed=discord.Embed(title="Unique Referral Code", description="Refer a new community to Jackpot to earn `15,000 🎟️’s` for yourself and `3,000 🎟️’s` for everyone else in your community.", color=0x222222)
    return embed 

def serverTweetLink(handle):
    embed=discord.Embed(title="🎉 Twitter Linked!", description="You can now use `Raid Last Tweet` to quickly create a Raid event on **"+handle+"'s** last tweet.", color=0x33FF5C)
    embed.set_footer(text="Powered by Jackpot", icon_url="https://static.wixstatic.com/media/cdc018_603e1fc27c6a4c71b2c8c333f66c858b~mv2.png")
    return embed 

def showReferalEmbed(referal):
    embed=discord.Embed(title=referal, description="Your unique referral code is above. Copy and paste to share!", color=0x222222)
    embed.set_footer(text="Powered by Jackpot", icon_url="https://static.wixstatic.com/media/cdc018_603e1fc27c6a4c71b2c8c333f66c858b~mv2.png")
    return embed

def getOptIn(handle):
    embed=discord.Embed(title="Congratulations!", description="**You have successfully joined Jackpot and are eligible to win the Jackpot raffle!** \n Your twitter handle `" + handle + "` has been linked! \n\n You are now ready to begin earning 🎟️'s for all the value you add to your community. As a token of our gratitude, you have been awarded `1000 🎟️'s`", color=0x33FF5C)
    embed.set_footer(text="Powered by Jackpot", icon_url="https://static.wixstatic.com/media/cdc018_603e1fc27c6a4c71b2c8c333f66c858b~mv2.png")
    return embed 

def getOptInNoWallet(getstarted, handle):
    embed=discord.Embed(title="Congratulations!", description="**You have successfully joined Jackpot. Until you add your ETH wallet address in the <#" + str(getstarted) + "> channel, you are ineligible to win the Jackpot raffle.** \n Your twitter handle `" + handle + "` has been linked! \n\n In the meantime, you are now ready to begin earning 🎟️'s for all the value you add to your community. As a token of our gratitude, you have been awarded `1000 🎟️'s`", color=0xcffc03)
    embed.set_footer(text="Powered by Jackpot", icon_url="https://static.wixstatic.com/media/cdc018_603e1fc27c6a4c71b2c8c333f66c858b~mv2.png")
    return embed

def outofseats():
    embed=discord.Embed(title="Upgrade Needed.", description="All available seats in this server have been claimed. Please upgrade your server’s subscription to allow more people to opt-in.", color=0xff3042)
    embed.set_footer(text="Powered by Jackpot", icon_url="https://static.wixstatic.com/media/cdc018_603e1fc27c6a4c71b2c8c333f66c858b~mv2.png")
    return embed

def getOptInInvalidWallet(getstarted, handle):
    embed=discord.Embed(title="Congratulations!", description="**You have successfully joined Jackpot. Until you add your ETH wallet address in the <#" + str(getstarted) + "> channel, you are ineligible to win the Jackpot raffle.** \n Your twitter handle `" + handle + "` has been linked! \n\n In the meantime, you are now ready to begin earning 🎟️'s for all the value you add to your community. As a token of our gratitude, you have been awarded `1000 🎟️'s`", color=0xcffc03)
    embed.add_field(name="⚠️ **Wallet ID Invalid**", value="Another user has already opted-in to Jackpot using the Wallet ID you specified.", inline=False)
    embed.set_footer(text="Powered by Jackpot", icon_url="https://static.wixstatic.com/media/cdc018_603e1fc27c6a4c71b2c8c333f66c858b~mv2.png")
    return embed

def getRankEmbed(memID, serverRank, globalRank, XP, globalXP, trend = 0):
    if str(serverRank) == "1":
        descp = memID + " is the top contributor in this server, with `" + str(XP) + " 🎟️'s`! Keep up the great work!"
    else:
        descp = memID + " has `" + str(XP) + " 🎟️'s` in this server! Keep earning 🎟️'s to rank up!"
    emoji = "🎟️"
    if trend == 1:
        emoji = " 🔼"
    elif trend == -1:
        emoji = " 🔽"
    embed = discord.Embed(title="🎖️ " + memID + " is Rank " + str(serverRank) + " in this Server", description=descp, color=0xEBF900)
    embed.add_field(name="🌎 Your Global Stats 🌎", value="Rank: `" + str(globalRank) + "`, Total 🎟️'s earned: `" + str(globalXP) + " 🎟️'s " + emoji + "` \n\n This message will delete in 10 seconds", inline=True)
    embed.set_footer(text="Powered by Jackpot", icon_url="https://static.wixstatic.com/media/cdc018_603e1fc27c6a4c71b2c8c333f66c858b~mv2.png")
    return embed

def getMultiplierEmbed():
    embed=discord.Embed(title="Claim 🎟️'s Multiplier", description="You're eligible to claim an 🎟️'s Multiplier based on the length of time you've held your community's NFT.\n\nTo claim the 🎟️'s Multiplier, click the button below and sign a message with the wallet that holds your NFT. Signing a message is different than signing a transaction. This will prove ownership without sharing your private key.", color=0x222222)
    return embed

def getUpdateEmbed():
    embed=discord.Embed(title="Update Your Information", description="Click on the button below to add or edit information linked to your Jackpot account.", color=0x222222)
    return embed

def getUpcomingJackpotsEmbed():
    embed=discord.Embed(title="Upcoming Jackpot💰", description="** **💰 Current Jackpot Size: `1,000 USDC` | ⏱️ Time Until Next Drawing: `24 Days`\n✋ # of Community Participants: `65` | ✋ # of Global Participants: `195`\n🎟️ **1 🎟️'s = 1 Raffle Ticket**", color=0xe9e9e9)
    return embed

def getLeaderboardsEmbed():
    embed=discord.Embed(title="Leaderboards 📈", color=0xe9e9e9)
    embed.add_field(name="**Full Leaderboard on our website**", value="🌐 __[Community Leaderboard](https://getjackpot.xyz/leaderboard/doodles/)__\n🌐 __[Global Leaderboard](https://getjackpot.xyz/leaderboard/)__", inline=False) 
    return embed

def getIntroEmbed():
    embed = discord.Embed(title="**Join Now!**", description="Opt-in to immediately earn `1000 🎟️'s` and have a chance at winning the Jackpot.", color=0xf59b42)
    return embed

def termsConditions():
    embed = discord.Embed(title="**Terms and Conditions 📝**", description="**Before we get started, you'll need to agree to the [terms and conditions](https://docs.google.com/document/d/1nXBXNLBbNplktyTITFMEEZvKZc8BKq2X/edit?usp=share_link&ouid=10337345930749).**\n\n By clicking on the `I Agree` button below, you agree to have read Jackpot's terms and conditions.", color=0x4299f5)
    embed.set_footer(text="Powered by Jackpot", icon_url="https://static.wixstatic.com/media/cdc018_603e1fc27c6a4c71b2c8c333f66c858b~mv2.png")
    return embed
    
def getXPEmbed(raids, quests):
    embed=discord.Embed(title="**How to Earn 🎟️'s**", description="Below is a guide to all of the ways you can earn tickets for the Jackpot.", color=0xe9e9e9)
    embed.add_field(name="**Discord:**", value="🎟️ Sending messages *(diminishing returns)*\n🎟️ Reacting to messages *(diminishing returns)*\n🎟️ Other people reacting to your messages\n🎟️ Other people replying to your messages\n🎟️ Being one of the first people to interact with a new member\n🎟️ Inviting real people to the server\n🎟️ Visiting the server daily\n🎟️ Catching a Crystal\n", inline=False) 
    embed.add_field(name="**Twitter:**", value = "🎟️ Retweeting a <#"+raids+"> tweet\n🎟️ Replying to a <#"+raids+"> tweet\n🎟️ Liking a <#"+raids+"> tweet\n", inline=False) 
    embed.add_field(name="**Quests:**", value = "🎟️ Successfully completing <#"+quests+">", inline=False)
    return embed

def getChannelsEmbed(userSettings, leaderboard, raids, quests, notifs):
    embed=discord.Embed(title="**Channel Overview**", color=0xe9e9e9)
    embed.add_field(name="Important channels to keep track of:", value="📍 <#"+userSettings+"> | Review and change your settings.\n📍 <#"+leaderboard+"> | See who has earned the most tickets.\n📍 <#"+raids+"> | Participate in Twitter raids to earn tickets.\n📍 <#"+quests+"> | Complete quests to earn tickets.\n📍 <#"+notifs+"> | See your notifications.")
    return embed

def getChannelsEmbedGetStarted(leaderboard, raids, quests, notifs):
    embed=discord.Embed(title="**Channel Overview**", color=0xe9e9e9)
    embed.add_field(name="Important channels to keep track of:", value="📍 <#"+leaderboard+"> | Visit our website containing your community’s most valuable contributors.\n📍 <#"+raids+"> | Participate in Twitter raids to earn 🎟️'s.\n📍 <#"+quests+"> | Choose from available quests and submit proof of completion.\n📍 <#"+notifs+"> | Get notified when you earn 🎟️'s and your quests are approved.")
    return embed

def getWelcomeEmbed():
    deadline, reward = api.getJackpotDeadline(), api.getJackpot()
    __, __, winners = api.getJackpotNumber()
    embed=discord.Embed(title="**Welcome to Jackpot!**",description="Jackpot is an incentive plugin for web3 communities that gamifies participation and engagement. Jackpot was architected in collaboration with 100+ web3 industry veterans including founders, community managers, mods, and core contributors across the Ethereum and Solana ecosystems.\n\nEarn tickets 🎟️ to climb the leaderboard and increase your chances of winning the Jackpot.", color=0x33FF5C)
    embed.add_field(name="**Next Drawing**", value="**Next Jackpot**: `"+str(reward)+" USDC`\n**Number of Winners**: `"+str(winners)+"`\n**Drawing on**: `"+str(deadline)+"`", inline=False)
    return embed

def getWelcomeOptInEmbed():
    return getWelcomeEmbed()

def getTwitterOAUTHEmbed(link):
    embed=discord.Embed(title="**Verify Twitter Account Ownership**", description="To opt-in, you must link your Twitter account. Follow the steps below to get your Twitter OAUTH code", color=0x1da1f2)
    embed.add_field(name="**Steps:**", value = "\n1. Go to the [**Twitter OAuth Authorization**]("+link+") page and authorize the app using your Twitter account.\n2. Copy the *one-time pincode* provided and submit it via the `Verify Twitter` button below.", inline=False)
    embed.set_footer(text="Powered by Jackpot", icon_url="https://static.wixstatic.com/media/cdc018_603e1fc27c6a4c71b2c8c333f66c858b~mv2.png")
    return embed

def linkCommunityTwitter(link):
    embed=discord.Embed(title="**Verify Twitter Account Ownership**", description="Make it easier to launch Raids by connecting your community Twitter account.", color=0x1da1f2)
    embed.add_field(name="**Steps:**", value = "\n1. Go to the [**Twitter OAuth Authorization**]("+link+") page and authorize the app using your Twitter account.\n2. Copy the *one-time pincode* provided and submit it via the `Verify Twitter` button below.", inline=False)
    embed.set_footer(text="Powered by Jackpot", icon_url="https://static.wixstatic.com/media/cdc018_603e1fc27c6a4c71b2c8c333f66c858b~mv2.png")
    return embed

def cmdJackpotEmbed():
    amount = api.getJackpot()
    deadline = api.getJackpotDeadline()
    serverNum, peopleNum, winnersNum = api.getJackpotNumber()
    embed=discord.Embed(title="**💰 The Next Jackpot is `" + amount + " USDC` 💰**", description="\nView [the Jackpot Website](https://getjackpot.xyz) for real-time updates.", color=0xEBF900)
    embed.add_field(name="**More Information**", value = "\nDrawing on: `" + deadline + "`\nWinners: `"+winnersNum+"`\nServers Participating: `" + serverNum + "` \nPeople Participating: `"+peopleNum+"`\n\n This message will delete in 10 seconds.", inline=False)
    embed.set_footer(text="Powered by Jackpot", icon_url="https://static.wixstatic.com/media/cdc018_603e1fc27c6a4c71b2c8c333f66c858b~mv2.png")
    return embed

def getMissionsEmbed():
    embed=discord.Embed(title="Missions 🗺️", description = "Missions are the easiest way to rack up 🎟️'s. Head over to #quests to view the available quests and submit proof of your work. Once approved by your community's admin, you'll receive 🎟️'s for your contribution.", color=0xe9e9e9)
    embed.set_footer(text="Powered by Jackpot", icon_url="https://static.wixstatic.com/media/cdc018_603e1fc27c6a4c71b2c8c333f66c858b~mv2.png")
    return embed

def getCommandsEmbed():
    embed=discord.Embed(title="**🤖 Discord Commands 🤖**", description = "👉 Type `/rank` to see your position on the leaderboard and how many tickets you've earned. \n*You can also view the rank of other users with this command*\n\n👉 Type `/leaderboard` to view the Jackpot leaderboard.\n\n👉 Type `/jackpot` to see information about the upcoming Jackpot.\n", color=0xe9e9e9)
    return embed

def getLeaderboardInformation():
    string = "** **\n** **📈 💰  __**[Doodles Community Leaderboard](https://getjackpot.xyz/leaderboard/doodles/)**__ 💰 📈\n🏘️  *[Community Leaderboard](https://getjackpot.xyz/leaderboard/doodles/)*   |   🌎  *[Global Leaderboard](https://getjackpot.xyz/leaderboard/)*\n*Last updated: 10/20/22 at 10:51 am EST*\n\n💰 Current Jackpot Size: `1,000 USDC`     ⏱️ Date of Next Drawing: `Nov. 4th @ 9:05pm EST`\n✋ # of Community Participants: `65`       ✋ # of Global Participants: `195`\n\n----------------\n\n        🏆   **__1.__**  🥇  **cryptobreaky    *[Twitter Profile](https://twitter.com/cryptobreaky)*   ~   🎟️ *[48800 XP](https://getjackpot.xyz/cryptobreaky)*\n\n        🏆   **__2.__**  🥈  **LanDAO Calrissian    (*[Twitter Profile](https://twitter.com/cryptobreaky)*)   ~   🎟️ *[46500 XP](https://getjackpot.xyz/cryptobreaky)***\n\n        🏆   **__3.__**  🥉  **Ashh    (*[Twitter Profile](https://twitter.com/cryptobreaky)*)   ~   🎟️ *[44700 XP](https://getjackpot.xyz/cryptobreaky)***\n\n        🏆   **__4.__**  ✨  **crypto_King    (*[Twitter Profile](https://twitter.com/cryptobreaky)*)   ~   🎟️ *[42800 XP](https://getjackpot.xyz/cryptobreaky)***\n\n        🏆   **__5.__**  ✨  **RatheSunGod    (*[Twitter Profile](https://twitter.com/cryptobreaky)*)   ~   🎟️ *[39500 XP](https://getjackpot.xyz/cryptobreaky)***\n\n        ✨   **Use */rank* in any channel to see your current stats.**\n\n----------------\n\n👉 *Type `!rank ` to see your own stats.*\n👉 *Type `!rank/username` to see someone else's stats.*\n👉 *Type `!leaderboard ` to preview the Community Leaderboard.*\n👉 *Type `!global ` to preview the Global Leaderboard.*\n👉 *Type `!jackpot ` to see the upcoming Jackpot.*\n👉 *Go to [getjackpot.xyz](https://getjackpot.xyz/) to see the full leaderboards.*\n** **\n** **"
    return string

def getFullLeaderboardEmbed():
    embed = discord.Embed(title="Leaderboard", description=getLeaderboardInformation(), color=0xe9e9e9)
    return embed

def getCrystalEmbed():
    embed = discord.Embed(title="💎💎 // CATCH THE CRYSTAL // 💎💎", description="First one to **Catch the Crystal** will earn `5000 🎟️'s`\n\n**Crystals appear once a day at a random time and in a random channel**", color=0x00D3F9)
    embed.set_footer(text="Powered by Jackpot", icon_url="https://static.wixstatic.com/media/cdc018_603e1fc27c6a4c71b2c8c333f66c858b~mv2.png")
    return embed

def getCaughtEmbed():
    embed = discord.Embed(title="💎💎 Crystal Caught! 💎💎", description="Congratulations! You caught today's crystal.", color=0x00D3F9)
    embed.set_footer(text="Powered by Jackpot", icon_url="https://static.wixstatic.com/media/cdc018_603e1fc27c6a4c71b2c8c333f66c858b~mv2.png")
    return embed

def cmdLeaderboardURL(top3):
    starter = ""
    if len(top3) <= 0:
        starter = "`Noone on this server has earned any 🎟️'s yet. Be the first to earn 🎟️'s!`"
    else:
        for member in top3:
            starter += "🏆 " + member[0] + " is `Rank " + str(member[1]) + "` in this server and has `" + str(member[2]) + " 🎟️'s`\n"   
    starter += "\n"
    embed = discord.Embed(title="Leaderboard", description=starter + "Click [here](https://getjackpot.com/leaderboard) to view the entire leaderboard, including the Global Leaderboard. \n\n This message will delete in 10 seconds.", color=0xe9e9e9)
    embed.set_footer(text="Powered by Jackpot", icon_url="https://static.wixstatic.com/media/cdc018_603e1fc27c6a4c71b2c8c333f66c858b~mv2.png")
    return embed

def getLeaderboardLink(top3):
    starter = ""
    if len(top3) <= 0:
        starter = "`Noone on this server has earned any 🎟️'s yet. Be the first to earn 🎟️'s!`"
    else:
        for member in top3:
            starter += "🏆 " + member[0] + " is `Rank " + str(member[1]) + "` in this server and has `" + str(member[2]) + " 🎟️'s`\n"   
    starter += "\n"
    embed = discord.Embed(title="Leaderboard", description=starter + "Click [here](https://getjackpot.com/leaderboard) to view the entire leaderboard, including the Global Leaderboard.", color=0xe9e9e9)
    embed.set_footer(text="Powered by Jackpot", icon_url="https://static.wixstatic.com/media/cdc018_603e1fc27c6a4c71b2c8c333f66c858b~mv2.png")
    return embed

def getLeaderboardEmbed():
    embed = discord.Embed(title="📈 The Leaderboard 📈", description="Check the leaderboard to see who holds the most 🎟️'s in your community and beyond", color=0xe9e9e9)
    embed.set_footer(text="Powered by Jackpot", icon_url="https://static.wixstatic.com/media/cdc018_603e1fc27c6a4c71b2c8c333f66c858b~mv2.png")
    return embed

def getTwitterEmbed(link, retweet, react, comment, boosted=False):
    xp = 0
    retweetStr, reactStr, commentStr = "`ineligible for this Raid`", "`ineligible for this Raid`", "`ineligible for this Raid`"
        
    if boosted:
        if retweet:
            xp += 1200
            retweetStr = "`1200 🎟️'s (BOOSTED)`"
        if react:
            xp += 400
            reactStr = "`400 🎟️'s (BOOSTED)`"
        if comment:
            xp += 800
            commentStr = "`800 🎟️'s (BOOSTED)`"
    
        mcolor = 0xf21d6a
        message = "**Engage** with the **Tweet** below to earn up to **"+ str(xp) +" 🎟️'s**\n\n🚨 **THIS RAID IS BOOSTED -- EARN 200% 🎟️'s!** 🚨\n\nLike = "+ reactStr + "\nReply = "+ commentStr +"\nRetweet = "+retweetStr+"\n\n⛓ __**" + link + "**__ ⛓"
    else:
        if retweet:
            xp += 600
            retweetStr = "`600 🎟️'s`"
        if react:
            xp += 200
            reactStr = "`200 🎟️'s`"
        if comment:
            xp += 400
            commentStr = "`400 🎟️'s`"
            
        mcolor = 0x1da1f2
        message = "**Engage** with the **Tweet** below to earn up to **"+ str(xp) +" 🎟️'s**\n\nLike = "+ reactStr + "\nReply = "+ commentStr +"\nRetweet = "+retweetStr+"\n\n⛓ __**" + link + "**__ ⛓\n"
    embed=discord.Embed(title="**RAID ALERT**", description=message, color=mcolor)
    embed.set_author(name="Twitter Raid Rewards", icon_url="https://img.icons8.com/color/344/twitter--v1.png")
    embed.set_footer(text="Powered by Jackpot", icon_url="https://static.wixstatic.com/media/cdc018_603e1fc27c6a4c71b2c8c333f66c858b~mv2.png")
    return embed

def getMissionsEmbed():
    embed=discord.Embed(title="**🗺️ Quests 🗺️**", description="Click the **View Quests** button below to see your community's active quests and their respective 🎟️ rewards.", color=0xf21d6a)
    embed.add_field(name="**Submitting Quest Completion**", value="To get credit (🎟️'s) for completing a quest, in the message section below, type `/complete` followed by the quest id and your description (proof) of completion. If you click +1 more, you can add a screenshot to supplement the proof of completion provided. Please note that all Quest submissions are approved or denied by the Jackpot team.\n\n➡️ **Select an active quest from the dropdown to view its details.**", inline=False) 
    embed.set_footer(text="Powered by Jackpot", icon_url="https://static.wixstatic.com/media/cdc018_603e1fc27c6a4c71b2c8c333f66c858b~mv2.png")
    return embed

def raidSuccessfulEmbed(link, typeRaid, name = None):
    embed = discord.Embed(title="**🎉 New raid created! 🎉**", description="Your raid was launched successfully", color=0x1da1f2)
    #embed.add_field(name="Details:", value="**Link:** [" + link + "](" + link + ") \n**Type:** " + typeRaid, inline=False)
    embed.add_field(name="Details:", value="**Link:** [" + link + "](" + link + ")", inline=False)
    embed.set_footer(text="Powered by Jackpot", icon_url="https://static.wixstatic.com/media/cdc018_603e1fc27c6a4c71b2c8c333f66c858b~mv2.png")
    return embed
    
def getMissionDetailsEmbed(title, description, xp, count, supply, personLimit, timesSubmitted):
    embed=discord.Embed(title="**🗺️ " + title + " 🗺️**", description=description, color=0xf21d6a)
    embed.add_field(name="**Quest Information**", value="**PAYOUT:** `" + str(xp) + " 🎟️'s`", inline=False)
    ## THESE FIELDS ARE NOT NEEDED FOR NOW ##
    ##embed.add_field(name="**Mission Information**", value="**🎟️'s PAYOUT:** `" + str(xp) + "` \n **REWARDS DISTRIBUTED SO FAR:** `" + str(count) + " out of " + str(supply) + "` \n", inline=False) 
    ##embed.add_field(name="**Submissions**", value="`You earned 🎟️'s for this quest " + str(timesSubmitted) + " of a maximum of " + str(personLimit) + " times`", inline=False) 
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

def noOptInMissions(getStarted, MemID):
    embed = discord.Embed(title="**⛔ " + MemID + ", you haven't opted in yet ⛔**", description="The operation you are trying to do is restricted to opted-in members of Jackpot.", color=0xFF3333)
    embed.add_field(name="**How to opt-in:**", value="Navigate to <#" + str(getStarted) + "> to learn more about the rewards Jackpot offers and opt-in.\n\nThis message will delete in 10 seconds.", inline=False) 
    embed.set_footer(text="Powered by Jackpot", icon_url="https://static.wixstatic.com/media/cdc018_603e1fc27c6a4c71b2c8c333f66c858b~mv2.png")
    return embed

def outOfSeats():
    embed = discord.Embed(title="**⛔ Upgrade Needed. ⛔**", description="All available seats in this server have been claimed. Please upgrade your server’s subscription to allow more people to opt-in.", color=0xFF3333)
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

def cmdErrorEmbed(title, message):
    embed = discord.Embed(title="**" + title + "**", description=message + "\n\n This message will delete in 10 seconds", color=0xFF3333)
    embed.set_footer(text="Powered by Jackpot", icon_url="https://static.wixstatic.com/media/cdc018_603e1fc27c6a4c71b2c8c333f66c858b~mv2.png")
    return embed

def raidCompleteEmbed(task):
    congratsMessages = ["Congrats!", "Nice Job!", "Well Done!", "You're all set!", "Nicely Done!"]
    randMessage = random.choice(congratsMessages)
    embed = discord.Embed(title="**"+randMessage+"**", description="✅ You've earned 🎟️'s for "+task+" this Raid.", color=0x33FF5C)
    embed.set_footer(text="Powered by Jackpot", icon_url="https://static.wixstatic.com/media/cdc018_603e1fc27c6a4c71b2c8c333f66c858b~mv2.png")
    return embed

def missionCompleteCommandInvalid(quests, title = "The `/complete` command is invalid in this channel"):
    embed = discord.Embed(title="**" + title + "**", description="Head over to the <#" + quests + "> channel to submit this quest. \n\n This message will delete in 10 seconds.", color=0xFF3333)
    embed.set_footer(text="Powered by Jackpot", icon_url="https://static.wixstatic.com/media/cdc018_603e1fc27c6a4c71b2c8c333f66c858b~mv2.png")
    return embed

def getMissionsListEmbed(numMissions):
    embed=discord.Embed(title="✅ **Quest Complete** ✅", description="In this channel, use `!verify [QUEST_NAME] [additional details or explaination]` to submit proof of a specific quest. If you are attaching a picture, attach it to the same message.", color=0xe9e9e9)
    embed.add_field(name="**Use the dropdown to see Active Missions**", value=str(numMissions) + " quests are active", inline=False)
    embed.set_footer(text="\n\nOnce submitted, a community admin will be able to approve/deny your submission. If approved, you'll receive 🎟️'s for your effort and will be notified in #notifs.") 
    return embed

def willBeExpired(numDays):
    embed = discord.Embed(title="**⛔ Your Jackpot subscription is up for renewal ⛔**", description="Your service will end in `" + str(numDays) + "` days if you do not add crypto to your custodial wallet or enter a valid credit card.’", color=0xFF3333)
    embed.set_footer(text="Powered by Jackpot", icon_url="https://static.wixstatic.com/media/cdc018_603e1fc27c6a4c71b2c8c333f66c858b~mv2.png")
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
    ## 5) if it has a "?" followed by any number of characters, that's fine
    
    regexOpt = r"^https:\/\/twitter\.com\/[a-zA-Z0-9_]+\/status\/[0-9]+(\?.*)?$"
    if re.match(regexOpt, link):
        return False
    else:
        return True
    
def isNum(num):
    try:
        int(num)
        return True
    except:
        return False
    
def find_invite_by_code(invite_list, code):
    for inv in invite_list:
        if inv.code == code:
            return inv
    
async def bot_set_up(myGuild):
    serverID = myGuild.id
    serverName = myGuild.name
    
    serverProfile = myGuild.icon.url
    invites = await myGuild.invites()
    api.addServer(serverID, serverName, serverProfile, invites)
    
    ## change the BOT_ROLE permissions to include view channels, manage channels, manage roles
    ##await myGuild.get_role(discord.utils.get(myGuild.roles, name=BOT_ROLE).id).edit(permissions=discord.Permissions(permissions=4398046511095))    
    ## if the Jackpot role doesn't exist, create it
    if discord.utils.get(myGuild.roles, name=JACKPOT_ROLE) == None: 
        await myGuild.create_role(name=JACKPOT_ROLE, color=discord.Color.from_rgb(235, 249, 0), hoist=False)
        
    ## if the Jackpot Non Opt role doesn't exist, create it ##DEPRECATED##
    # if discord.utils.get(myGuild.roles, name=JACKPOT_NON_OPT) == None:
    #    await myGuild.create_role(name=JACKPOT_NON_OPT, color=discord.Color.from_rgb(255, 110, 110), hoist=False)
        
    if discord.utils.get(myGuild.roles, name=ADMIN_ROLE) == None:
        await myGuild.create_role(name=ADMIN_ROLE, color=discord.Color.from_rgb(153, 170, 181), hoist=False)
        await myGuild.get_role(discord.utils.get(myGuild.roles, name=ADMIN_ROLE).id).edit(permissions=discord.Permissions(permissions=4398046511095))
        ## give this role to everyone with BOT_ROLE
    
    ## give this role to everyone who has the BOT_ROLE
    for member in myGuild.members:
        if discord.utils.get(member.roles, name=BOT_ROLE) != None and discord.utils.get(member.roles, name=ADMIN_ROLE) == None:
            await member.add_roles(discord.utils.get(myGuild.roles, name=ADMIN_ROLE))

    guild = myGuild
    
    ## give everyone the Jackpot Non Opt role if they dont have the Jackpot role already
    #for member in guild.members:
    #    try:
    #        if discord.utils.get(member.roles, name=JACKPOT_NON_OPT) == None and discord.utils.get(member.roles, name=JACKPOT_ROLE) == None and discord.utils.get(member.roles, name=BOT_ROLE) == None:
    #            await member.add_roles(discord.utils.get(guild.roles, name=JACKPOT_NON_OPT))
    #    except:
    #        pass
            
    ## create Guild categories if they don't exist, REG_GUILD and ADMIN_GUILD
    if discord.utils.get(guild.categories, name=REG_GUILD) == None:
        await guild.create_category(REG_GUILD)
    if discord.utils.get(guild.categories, name=ADMIN_GUILD) == None:
        await guild.create_category(ADMIN_GUILD)
    
    ## if any of the channels in prepChannels exist, delete them
    prepChannels = ["get-started", "user-settings", "leaderboard", "raids", "quests", "add-quests", "mission-approval", "launch-raid", "notifs"]
    for channel in prepChannels:
        channelName = api.getChannel(serverID, channel)
        if discord.utils.get(guild.channels, name=channelName) != None:
            if channel != "notifs":
                await discord.utils.get(guild.channels, name=channelName).delete()
            else:
                await discord.utils.get(guild.channels, name=channelName).delete()
                ## DEPRECATED: send a messgae in notifs that the bot is restarting
                ## await discord.utils.get(guild.channels, name=channel).send("🤖 **Jackpot Bot is restarting, this event has been logged** 🤖")
    
    ## Make #opt-in, #guide avalible to everyone
    # channels = ["opt-in", "guide"]
    channels = ["get-started"]
    for channel in channels:
        channelName = api.getChannel(serverID, channel)
        if discord.utils.get(guild.channels, name=channelName) == None:
            await guild.create_text_channel(channelName, category=discord.utils.get(guild.categories, name=REG_GUILD))
            await discord.utils.get(guild.channels, name=channelName).set_permissions(discord.utils.get(guild.roles, name=ADMIN_ROLE), read_messages=True, send_messages=True)
            ## deny access to the Jackpot role
            await discord.utils.get(guild.channels, name=channelName).set_permissions(discord.utils.get(guild.roles, name=JACKPOT_ROLE), read_messages=False, send_messages=False)
    
    ## make the channel #user-settings visible to everyone in the "Jackpot" role
    channels = ["user-settings"]
    for channel in channels:
        channelName = api.getChannel(serverID, channel)
        if discord.utils.get(guild.channels, name=channelName) == None:
            await guild.create_text_channel(channelName, category=discord.utils.get(guild.categories, name=REG_GUILD))
            await discord.utils.get(guild.channels, name=channelName).set_permissions(guild.default_role, read_messages=False)   
            #await discord.utils.get(guild.channels, name=channel).set_permissions(discord.utils.get(guild.roles, name=BOT_ROLE), read_messages=True, send_messages=True)
            await discord.utils.get(guild.channels, name=channelName).set_permissions(discord.utils.get(guild.roles, name=ADMIN_ROLE), read_messages=True, send_messages=True)
            await discord.utils.get(guild.channels, name=channelName).set_permissions(discord.utils.get(guild.roles, name=JACKPOT_ROLE), read_messages=True, send_messages=False)
    
    ## make the following channels visible to everyone in the "Jackpot" role they don't exist: #leaderboard, #raids, #missions, #mission-complete, #notifs
    channels = ["leaderboard", "raids", "quests", "notifs"]
    for channel in channels:
        channelName = api.getChannel(serverID, channel)
        if discord.utils.get(guild.channels, name=channelName) == None:
            await guild.create_text_channel(channelName, category=discord.utils.get(guild.categories, name=REG_GUILD))
            await discord.utils.get(guild.channels, name=channelName).set_permissions(guild.default_role, read_messages=False)
            #await discord.utils.get(guild.channels, name=channel).set_permissions(discord.utils.get(guild.roles, name=BOT_ROLE), read_messages=True, send_messages=True)
            await discord.utils.get(guild.channels, name=channelName).set_permissions(discord.utils.get(guild.roles, name=ADMIN_ROLE), read_messages=True, send_messages=True)
            if channel != "quests":
                await discord.utils.get(guild.channels, name=channelName).set_permissions(discord.utils.get(guild.roles, name=JACKPOT_ROLE), read_messages=True, send_messages=False)
            else:
                await discord.utils.get(guild.channels, name=channelName).set_permissions(discord.utils.get(guild.roles, name=JACKPOT_ROLE), read_messages=True, send_messages=True)
    
    ## Create a get-started channel
    class optInstructions(discord.ui.View):
        def __init__(self):
            super().__init__()
            self.value = None
            self.timeout = VIEW_TIMEOUT
        @discord.ui.button(label="Get Started", style=discord.ButtonStyle.green)
        async def optin(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
            url, token, secret = twitter.link()
            
            class optInModal(ui.Modal, title = "Twitter OAuth Code"):
                pin = ui.TextInput(label = "Verify and link your account", style=discord.TextStyle.short, placeholder="Copy and paste your OAuth pin-code here", required = True)
                walletID = ui.TextInput(label = "Enter your Ethereum wallet address (Optional)", style=discord.TextStyle.short, placeholder="Jackpot winnings won't be awarded if blank", required = False)
                async def on_submit(self, interaction: discord.Interaction):
                    
                    ## if JACKPOT ROLE, return
                    if discord.utils.get(guild.roles, name=JACKPOT_ROLE) in interaction.user.roles:
                        channelID = str(discord.utils.get(guild.channels, name=api.getChannel(serverID, "user-settings")).id)
                        await interaction.response.send_message(embed=alreadyOptIn(channelID), ephemeral=True)
                    
                    else:
                        pin = self.pin.value
                        tweeterOBJ = twitter.auth(token, secret, pin)
                        
                        if tweeterOBJ != None:
                            server = interaction.guild.id
                            handle = "@" + str(tweeterOBJ[3])
                            walledID = self.walletID.value
                            didEnter, walletSuccess = False, False
                            if walledID != "" or walledID != None:
                                didEnter = True
                                walletSuccess = api.checkWallet(walledID, server)
                            if walletSuccess == False:
                                walledID = ""
                            memberName = interaction.user.name
                            profilePic = interaction.user.avatar
                            if profilePic == None or profilePic == "":
                                profilePic = "None"
                            else:
                                profilePic = interaction.user.avatar.url
                            memIDNum = interaction.user.id
                            memberID = interaction.user.name + "#" + interaction.user.discriminator
                            optInRet = api.optInMember(server, memberID, memIDNum, memberName, profilePic, tweeterOBJ, walledID)
                            if optInRet != False:
                                ## create an 🎟️'s event
                                api.xpEvent(server, memberID, 0)
                                reward = api.getReward(server, memberName, 0)
                                ## put on the notifs channel that a user has opted in
                                await discord.utils.get(guild.channels, name=api.getChannel(serverID, "notifs")).send("✅ **" + str(interaction.user) + "** has opted in and earned `" + reward + "`!")
                                
                                ## DEPRECATED: assign the Jackpot role to the user
                                ## await interaction.response.send_message(content="✅ **Success!**\n\nYou have now successfully opted in to Jackpot and have been awarded `1000 🎟️'s` as a token of our gratitude. You are now ready to begin earning 🎟️'s for the value you bring to the table.", ephemeral=True)
                                await interaction.user.add_roles(discord.utils.get(guild.roles, name=JACKPOT_ROLE))
                                # await interaction.user.remove_roles(discord.utils.get(guild.roles, name=JACKPOT_NON_OPT))
                                
                                ## if user submits a wallet ID, show the getOptIn() embed
                                if walledID != "" and walledID != None:
                                    await interaction.response.send_message(embed=getOptIn(handle), ephemeral=True)
                                elif didEnter == True and walletSuccess == False:
                                    channelID = discord.utils.get(guild.channels, name=api.getChannel(serverID, "user-settings")).id
                                    await interaction.response.send_message(embed=getOptInInvalidWallet(channelID, handle), ephemeral=True)
                                else:
                                    channelID = discord.utils.get(guild.channels, name=api.getChannel(serverID, "user-settings")).id
                                    await interaction.response.send_message(embed=getOptInNoWallet(channelID, handle), ephemeral=True)
                                
                                if optInRet[0] == optInRet[1]:
                                    ctx = api.getJoin(server)
                                    await ctx.edit(embed = outOfSeats())
                                    
                            else:
                                await interaction.response.send_message(embed=errorEmbed("We were unable to complete the opt-in process at this time. Please try again later."), ephemeral=True)
                        else:
                            await interaction.response.send_message(embed=userErrorEmbed("We couldn't verify your Twitter", "The pin code you entered was incorrect. Please review the instructions above and try again."), ephemeral=True)
                            
            class optIn(discord.ui.View):
                def __init__(self):
                    super().__init__()
                    self.value = None
                    self.timeout = VIEW_TIMEOUT
                @discord.ui.button(label="Verify Twitter", style=discord.ButtonStyle.green)
                async def optin(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
                    if discord.utils.get(guild.roles, name=JACKPOT_ROLE) in interaction.user.roles:
                        userSettings = discord.utils.get(guild.channels, name=api.getChannel(serverID, "user-settings")).id
                        await interaction.response.send_message(embed=alreadyOptIn(userSettings), ephemeral=True)
                    else:
                        await interaction.response.send_modal(optInModal())
            if discord.utils.get(guild.roles, name=JACKPOT_ROLE) in interaction.user.roles:
                userSettings = discord.utils.get(guild.channels, name=api.getChannel(serverID, "user-settings")).id
                await interaction.response.send_message(embed=alreadyOptIn(userSettings), ephemeral=True)
            else:
                await interaction.response.send_message(embed=getTwitterOAUTHEmbed(url), view=optIn(), ephemeral=True)
                    
    if discord.utils.get(guild.channels, name=api.getChannel(serverID, "get-started")).last_message == None or discord.utils.get(guild.channels, name="get-started").last_message.author != client.user:
        ## in the get started channel, send the gif located at Assets/Get Started.gif
        await discord.utils.get(guild.channels, name=api.getChannel(serverID, "get-started")).send(file=discord.File("Assets/Get Started.gif"))
        
        userSettings = str(discord.utils.get(guild.channels, name=api.getChannel(serverID, "user-settings")).id)
        leaderboard = str(discord.utils.get(guild.channels, name=api.getChannel(serverID, "leaderboard")).id)
        raids = str(discord.utils.get(guild.channels, name=api.getChannel(serverID, "raids")).id)
        missions = str(discord.utils.get(guild.channels, name=api.getChannel(serverID, "quests")).id)
        notifs = str(discord.utils.get(guild.channels, name=api.getChannel(serverID, "notifs")).id)
        
        ## send other messages
        getStartedMes = await discord.utils.get(guild.channels, name=api.getChannel(serverID, "get-started")).send(embed=getWelcomeEmbed())
        await discord.utils.get(guild.channels, name=api.getChannel(serverID, "get-started")).send(embed=getXPEmbed(raids, missions))
        await discord.utils.get(guild.channels, name=api.getChannel(serverID, "get-started")).send(embed=getChannelsEmbedGetStarted(leaderboard, raids, missions, notifs))
        await discord.utils.get(guild.channels, name=api.getChannel(serverID, "get-started")).send(embed=getCommandsEmbed())
        joinNowMes = await discord.utils.get(guild.channels, name=api.getChannel(serverID, "get-started")).send(embed = getIntroEmbed(), view = optInstructions())
        api.storeGettingStarted(guild.id, getStartedMes)
        api.storeJoin(guild.id, joinNowMes)
    
    
    ## in #user-settings channel, send information from #get-started along with user settings embeds
    class viewCode(discord.ui.View):
        def __init__(self):
            super().__init__()
            self.value = None
            self.timeout = VIEW_TIMEOUT
        @discord.ui.button(label="View your code", style=discord.ButtonStyle.green)
        async def referal(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
            ## if the person has the JACKPOT ROLE
            if discord.utils.get(guild.roles, name=JACKPOT_ROLE) in interaction.user.roles:
                ## defer the interaction
                ## await interaction.response.defer()
                memberID = interaction.user.name + "#" + interaction.user.discriminator
                memberObject = api.getMember(interaction.guild.id, memberID)
                refCode = memberObject.referal
                if refCode == None:
                    refCode = api.createAlphaNumericCode(interaction.guild.id, memberID)
                    memberObject.referal = refCode
                
                ## await interaction.response.send(content="Your referral code is: `" + refCode + "`", ephemeral=True)
                ## send the referral code to the defered interaction
                await interaction.response.send_message(embed=showReferalEmbed(refCode), ephemeral=True)
            else:
                getStarted = str(discord.utils.get(guild.channels, name=api.getChannel(serverID, "get-started")).id)
                await interaction.response.send_message(embed=noOptIn(getStarted), ephemeral=True)
                
    class multipler(discord.ui.View):
        def __init__(self):
            super().__init__()
            self.value = None
            self.timeout = VIEW_TIMEOUT
        @discord.ui.button(label="Claim 🎟️'s Multiplier", style=discord.ButtonStyle.green)
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
            ## if user doesn't have the JACKPOT ROLE, send them the noOptIn embed
            if discord.utils.get(guild.roles, name=JACKPOT_ROLE) not in interaction.user.roles:
                getStarted = str(discord.utils.get(guild.channels, name=api.getChannel(serverID, "get-started")).id)
                await interaction.response.send_message(embed=noOptIn(getStarted), ephemeral=True)
            else:
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
                        database.add_wallet(memberID, interaction.guild.id, str(walletNum))
                        await interaction.response.send_message("Profile updated!", ephemeral=True)    
                await interaction.response.send_modal(updateInfo())      
           
    if discord.utils.get(guild.channels, name=api.getChannel(serverID, "user-settings")).last_message == None or discord.utils.get(guild.channels, name=api.getChannel(serverID, "user-settings")).last_message.author != client.user:
        userSettings = str(discord.utils.get(guild.channels, name=api.getChannel(serverID, "user-settings")).id)
        leaderboard = str(discord.utils.get(guild.channels, name=api.getChannel(serverID, "leaderboard")).id)
        raids = str(discord.utils.get(guild.channels, name=api.getChannel(serverID, "raids")).id)
        missions = str(discord.utils.get(guild.channels, name=api.getChannel(serverID, "quests")).id)
        notifs = str(discord.utils.get(guild.channels, name=api.getChannel(serverID, "notifs")).id)
        
        await discord.utils.get(guild.channels, name=api.getChannel(serverID, "user-settings")).send(file=discord.File("Assets/Get Started.gif"))
        userSetMes = await discord.utils.get(guild.channels, name=api.getChannel(serverID, "user-settings")).send(embed=getWelcomeOptInEmbed())
        await discord.utils.get(guild.channels, name=api.getChannel(serverID, "user-settings")).send(embed=getXPEmbed(raids, missions))
        await discord.utils.get(guild.channels, name=api.getChannel(serverID, "user-settings")).send(embed=getChannelsEmbed(userSettings, leaderboard, raids, missions, notifs))
        await discord.utils.get(guild.channels, name=api.getChannel(serverID, "user-settings")).send(embed=getCommandsEmbed())
        await discord.utils.get(guild.channels, name=api.getChannel(serverID, "user-settings")).send(embed = getReferalEmbed(), view = viewCode())
        ## Individual Multiplier offline 
        ## await discord.utils.get(guild.channels, name="user-settings").send(embed = getMultiplierEmbed(), view = multipler())
        await discord.utils.get(guild.channels, name=api.getChannel(serverID, "user-settings")).send(embed = getUpdateEmbed(), view = updateInfo())
        api.storeUserSettings(guild.id, userSetMes)
    
    ## in the leaderboard channel, send a leaderboard message
    if discord.utils.get(guild.channels, name=api.getChannel(serverID, "leaderboard")).last_message == None or discord.utils.get(guild.channels, name=api.getChannel(serverID, "leaderboard")).last_message.author != client.user:
        await discord.utils.get(guild.channels, name=api.getChannel(serverID, "leaderboard")).send(file=discord.File("Assets/main.gif"))
        class printLeaderboard(discord.ui.View):
            def __init__(self):
                super().__init__()
                self.value = None
                self.timeout = VIEW_TIMEOUT
            @discord.ui.button(label="🏆 View Leaderboard 🏆", style=discord.ButtonStyle.green)
            async def optin(self, interaction: discord.Interaction, button: discord.ui.Button):
                top3 = api.getTop3(interaction.guild.id)
                await interaction.response.send_message(embed=getLeaderboardLink(top3), ephemeral=True)
        await discord.utils.get(guild.channels, name=api.getChannel(serverID, "leaderboard")).send(embed = getLeaderboardEmbed(), view = printLeaderboard())
        
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
    if discord.utils.get(guild.channels, name=api.getChannel(serverID, "quests")).last_message == None or discord.utils.get(guild.channels, name=api.getChannel(serverID, "quests")).last_message.author != client.user:
        await discord.utils.get(guild.channels, name=api.getChannel(serverID, "quests")).send(file=discord.File("Assets/Quests.gif"))
        class missions(discord.ui.View):
            def __init__(self):
                super().__init__()
                self.value = None
                self.timeout = VIEW_TIMEOUT
            @discord.ui.button(label="View Quests", style=discord.ButtonStyle.green)
            async def onButtonClick(self, interaction: discord.Interaction, button: discord.ui.Button):
                class viewMission(discord.ui.View):
                    def __init__(self):
                        super().__init__()
                        self.value = None
                        self.timeout = VIEW_TIMEOUT
                    theOptions, theValues = getMissionsDropdownOptions(serverID)
                    @discord.ui.select(placeholder="Select a Quest", options=theOptions)
                    async def on_select(self, interaction: discord.Interaction, select: discord.ui.Select):
                        userID = interaction.user.name + "#" + interaction.user.discriminator
                        selectedMission = select.values[0]
                        __, theValues = getMissionsDropdownOptions(serverID)
                        for missions in theValues:
                            if missions[0] == selectedMission:
                                numSub = api.getNumMissionSubmissions(serverID, missions[0], userID)
                                await interaction.response.send_message(embed=getMissionDetailsEmbed(missions[0], missions[1], missions[2], missions[4], missions[3], missions[6], numSub), ephemeral=True)
                                break

                await interaction.response.send_message("Select a quest to view:", view=viewMission(), ephemeral=True)
                
        await discord.utils.get(guild.channels, name=api.getChannel(serverID, "quests")).send(embed=getMissionsEmbed(), view=missions())
        
    ## DEPRECATED: in the mission-complete, send an getMissionsListEmbed() embed
    ##if discord.utils.get(guild.channels, name="mission-complete").last_message == None or discord.utils.get(guild.channels, name="mission-complete").last_message.author != client.user:
    ##numCount = len(api.getMissions(serverID))
    ##embedMessage = await discord.utils.get(guild.channels, name="mission-complete").send(embed=getMissionsListEmbed(numCount))
    
    ## DEPRECATED: pin the message
    ## await embedMessage.pin()
    
    ## make the following channels visible to only Admins if they don't exist: #add-mission, #mission-approval, #launch-raid
    channels = ["add-quests", "launch-raid"]
    for channel in channels:
        channelName = api.getChannel(serverID, channel)
        if discord.utils.get(guild.channels, name=channelName) == None:
            await guild.create_text_channel(channelName, category=discord.utils.get(guild.categories, name=ADMIN_GUILD))
            await discord.utils.get(guild.channels, name=channelName).set_permissions(guild.default_role, read_messages=False)
            #await discord.utils.get(guild.channels, name=channel).set_permissions(discord.utils.get(guild.roles, name=BOT_ROLE), read_messages=True, send_messages=True)
            await discord.utils.get(guild.channels, name=channelName).set_permissions(discord.utils.get(guild.roles, name=ADMIN_ROLE), read_messages=True, send_messages=True)
    ## in the add-mission, send a message and 3 buttons: Add Quest, Edit Quest, Delete Quest
    if discord.utils.get(guild.channels, name=api.getChannel(serverID, "add-quests")).last_message == None or discord.utils.get(guild.channels, name=api.getChannel(serverID, "add-quests")).last_message.author != client.user:
        await discord.utils.get(guild.channels, name=api.getChannel(serverID, "add-quests")).send(file=discord.File("Assets/Add Quest.gif"))
        
        class addQuest(ui.Modal, title = "Add Quest Form"):
            name = ui.TextInput(label = "Quest Name", style=discord.TextStyle.short, placeholder = "Quest Name", required = True)
            desc = ui.TextInput(label = "Quest Description", style=discord.TextStyle.long, placeholder = "Quest Description", required = True)
            reward = ui.TextInput(label = "Quest 🎟️'s Reward (Max: 5000)", style=discord.TextStyle.short, placeholder = "e.g. 400", required = True)
            supply = ui.TextInput(label = "Quest Total Supply (Optional)", style=discord.TextStyle.short, placeholder = "Default: Unlimited", required = False)
            perperson = ui.TextInput(label = "Quest Supply Per Person (Optional)", style=discord.TextStyle.short, placeholder = "Default: Unlimited", required = False)
            
            async def on_submit(self, interaction: discord.Interaction):
                serverID = interaction.guild.id
                name = self.name.value.strip()
                if self.reward.value != None and isNum(self.reward.value):
                    if int(self.reward.value) > 5000:
                        rewXP = 5000
                    elif int(self.reward.value) <= 0:
                        rewXP = 1
                    else:
                        rewXP = int(self.reward.value)
                
                if self.supply.value != None and not isNum(self.supply.value):
                    supVal = ""
                elif self.supply.value != None and int(self.supply.value) <= 0:
                    supVal = "1"
                else:
                    supVal = self.supply.value
                    
                if self.perperson.value != None and not isNum(self.perperson.value):
                    perVal = ""
                elif self.perperson.value != None and int(self.perperson.value) <= 0:
                    perVal = "1"
                else:
                    perVal = self.perperson.value
                
                randID = api.createMission(serverID, name, self.desc.value, rewXP, supVal, perVal) 
                await interaction.response.send_message(content="A Quest was successfully added: **" + str(self.name) + "**", ephemeral=True)
            
        class quests(discord.ui.View):
            def __init__(self):
                super().__init__()
                self.value = None
                self.timeout = VIEW_TIMEOUT
            @discord.ui.button(label="Add Quest", style=discord.ButtonStyle.green)
            async def but1(self, interaction: discord.Interaction, button: discord.ui.Button):
                await interaction.response.send_modal(addQuest())
            @discord.ui.button(label="Edit Quest", style=discord.ButtonStyle.primary)
            async def but2(self, interaction: discord.Interaction, button: discord.ui.Button):
                theOptions, __ = getMissionsDropdownOptions(serverID)
                
                class editSelector(discord.ui.View):
                    def __init__(self):
                        super().__init__()
                        self.value = None
                        self.timeout = VIEW_TIMEOUT
                    @discord.ui.select(placeholder="Select a Quest", options=theOptions)
                    async def on_select(self, interaction: discord.Interaction, select: discord.ui.Select):
                        selectedMission = select.values[0]
                        __, missionObject = api.getMission(serverID, selectedMission)
                        
                        class editExistingQuest(ui.Modal, title = "EDIT TASK MODAL"):
                            desc = ui.TextInput(label = "Quest Description", style=discord.TextStyle.short, default = str(missionObject.description), required = True)
                            reward = ui.TextInput(label = "Quest 🎟️'s Reward (Max: 5000)", style=discord.TextStyle.short, default = str(missionObject.xp), required = True)
                            supply = ui.TextInput(label = "Quest Total Supply (Optional)", style=discord.TextStyle.short, default = str(missionObject.limit), required = False)
                            perperson = ui.TextInput(label = "Quest Supply Per Person (Optional)", style=discord.TextStyle.short, default = str(missionObject.personLimit), required = False)
                            
                            async def on_submit(self, interaction: discord.Interaction):
                                missionObject.description = self.desc.value
                                if self.reward.value != "" and self.reward.value != None and isNum(self.reward.value):
                                    if int(self.reward.value) <= 0:
                                        missionObject.xp = 1
                                    elif int(self.reward.value) > 5000:
                                        missionObject.xp = 5000
                                    else:
                                        missionObject.xp = int(self.reward.value)
                                if self.supply.value != "" and self.supply.value != None and isNum(self.supply.value) and int(self.supply.value) > 0:
                                    missionObject.limit = int(self.supply.value)
                                else:
                                    missionObject.limit = math.inf
                                if self.perperson.value != "" and self.perperson.value != None and isNum(self.perperson.value) and int(self.perperson.value) > 0:
                                    missionObject.personLimit = int(self.perperson.value)
                                else:
                                    missionObject.personLimit = math.inf
                                
                                await interaction.response.send_message(content="A Quest has been modifed", ephemeral=True)
                        await interaction.response.send_modal(editExistingQuest())
                        
                await interaction.response.send_message(content="Select a Quest you would like to edit", ephemeral=True, view=editSelector())
            
            @discord.ui.button(label="Delete Quest", style=discord.ButtonStyle.red)
            async def but3(self, interaction: discord.Interaction, button: discord.ui.Button):
                theOptions, __ = getMissionsDropdownOptions(serverID)
                
                class deleteSelector(discord.ui.View):
                    def __init__(self):
                        super().__init__()
                        self.value = None
                        self.timeout = VIEW_TIMEOUT
                    @discord.ui.select(placeholder="Select a Quest to delete", options=theOptions)
                    async def on_select(self, interaction: discord.Interaction, select: discord.ui.Select):
                        selectedMission = select.values[0]
                        missionID, missionObject = api.getMission(serverID, selectedMission)
                        
                        if (len(selectedMission) > 30):
                            titleMission = selectedMission[:27] + "..."
                        else:
                            titleMission = selectedMission
                        
                        class deleteExistingQuest(ui.Modal, title = "⚠️ DELETE "+titleMission+" ⚠️"):
                            deleteMe = ui.TextInput(label = "Type 'DELETE' below to finish.", style=discord.TextStyle.short, placeholder = "This action can not be reversed.", required = False)
                            
                            async def on_submit(self, interaction: discord.Interaction):
                                if self.deleteMe.value == "DELETE":
                                    api.deleteMission(serverID, missionID)
                                    await interaction.response.send_message(content="A Quest has been deleted", ephemeral=True)
                                else:
                                    await interaction.repsonse.send_message(embed = userErrorEmbed("The quest has *not* been deleted.", "Please enter `DELETE` (case-sensitive) on the delete pop-up to delete the **" + selectedMission + "** quest."), ephemeral = True)
                        
                        await interaction.response.send_modal(deleteExistingQuest())
                        
                await interaction.response.send_message(content="Select a Quest you would like to delete", ephemeral=True, view=deleteSelector())
                
        await discord.utils.get(guild.channels, name=api.getChannel(serverID, "add-quests")).send(embed = getMissionAddEmbed(), view = quests())
    
    ## DEPRECATED: send a mission-approval gif in the mission-approval channel
    ##if discord.utils.get(guild.channels, name="mission-approval").last_message == None or discord.utils.get(guild.channels, name="mission-approval").last_message.author != client.user:
    ##    await discord.utils.get(guild.channels, name="mission-approval").send(file=discord.File("Assets/Mission Approval.gif"))
    
    ## in the launch-raid, send a message with 1 button: Launch Raid. Pressing the button will open a discord form to fill out
    if discord.utils.get(guild.channels, name=api.getChannel(serverID, "launch-raid")).last_message == None or discord.utils.get(guild.channels, name=api.getChannel(serverID, "launch-raid")).last_message.author != client.user:
        await discord.utils.get(guild.channels, name=api.getChannel(serverID, "launch-raid")).send(file=discord.File("Assets/Launch Raid.gif"))
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
                        discord.SelectOption(label="Retweet", description="Award 🎟️'s for Retweets", emoji="🔁"),
                        discord.SelectOption(label="Like", description="Award 🎟️'s for Likes", emoji="❤️"), 
                        discord.SelectOption(label="Reply", description="Award 🎟️'s for Replies", emoji="📝")
                        ])
                    async def on_select(self, interaction: discord.Interaction, select: discord.ui.Select):
                        ## API CALL TO GET DATA
                        class addRaid(ui.Modal, title = "Create a Twitter Raid"):
                            ##raidTitle = ui.TextInput(label = "Raid Title", style=discord.TextStyle.short, placeholder = "Name this Twitter Raid", required = True)
                            url = ui.TextInput(label = "Tweet URL", style=discord.TextStyle.short, placeholder = "What is the URL of a tweet", required = True)
                            #boosted = ui.TextInput(label = "Boosted 🎟️'s", style=discord.TextStyle.short, placeholder = "True/False (Boosted Tweets earn 200% 🎟️'s)", required = True)
                            async def on_submit(self, interaction: discord.Interaction):
                                ## DO API CALL HERE
                                link = self.url.value
                                ##raidTitle = self.raidTitle.value
                                raidTitle = "A RAID"
                                boosted, retweet, react, comment = False, False, False, False
                                
                                #if "t" in self.boosted.value.lower():
                                #    boosted = True
                                xpAwards = ""
                                for value in select.values:
                                    if "retweet" in value.lower():
                                        retweet = True
                                        xpAwards += " `Retweet`"
                                    elif "like" in value.lower():
                                        react = True
                                        xpAwards += " `React`"
                                    elif "reply" in value.lower():
                                        comment = True
                                        xpAwards += " `Comment`"
                                
                                serverID = interaction.guild.id
                                ## make a new view of 1 -3 buttons for retweeting, reacting, commenting
                                class raidView(discord.ui.View):
                                    def __init__(self):
                                        super().__init__()
                                        self.value = None
                                        self.timeout = VIEW_TIMEOUT
                                    @discord.ui.button(label="Claim Like 🎟️'s", style=discord.ButtonStyle.primary)
                                    async def react(self, interaction: discord.Interaction, button: discord.ui.Button):
                                        serverName = interaction.guild.id
                                        userID = interaction.user.name + "#" + interaction.user.discriminator
                                        
                                        memberObj = api.getMember(serverName, userID)
                                        if memberObj == None:
                                            gettingStartedID = str(discord.utils.get(interaction.guild.channels, name=api.getChannel(serverID, "get-started")).id)
                                            await interaction.response.send_message(embed=noOptIn(gettingStartedID), ephemeral=True)
                                            return
                                        liked, retweeted = twitter.likedRetweeted(memberObj.twitterOBJ[0], memberObj.twitterOBJ[1], twitterID)
                                        if liked:
                                            resp = api.tweetEventReact(serverName, userID, tweetID)
                                            if type(resp) == int:
                                                await discord.utils.get(interaction.guild.channels, name=api.getChannel(serverID, "notifs")).send("✅ **" + userID + "** liked a raid tweet for `" + str(resp) + " 🎟️'s`!")
                                                await interaction.response.send_message(embed=raidCompleteEmbed("`reacting` to"), ephemeral=True)
                                            else:
                                                await interaction.response.send_message(embed=userErrorEmbed("You're not eligible to earn 🎟️'s for `liking` this Raid", resp), ephemeral=True)
                                        else:
                                            await interaction.response.send_message(embed=userErrorEmbed("No 🎟️'s Earned", "We weren't able to verify completion of **" + memberObj.handle + "** `liking` this raid."), ephemeral=True)
        
                                    @discord.ui.button(label="Claim Reply 🎟️'s", style=discord.ButtonStyle.green)
                                    async def comment(self, interaction: discord.Interaction, button: discord.ui.Button):
                                        serverName = interaction.guild.id
                                        userID = interaction.user.name + "#" + interaction.user.discriminator
                                        memberObj = api.getMember(serverName, userID)
                                        if memberObj == None:
                                            gettingStartedID = str(discord.utils.get(interaction.guild.channels, name=api.getChannel(serverID, "get-started")).id)
                                            await interaction.response.send_message(embed=noOptIn(gettingStartedID), ephemeral=True)
                                            return
                                        replied = twitter.hasCommented(memberObj.twitterOBJ[0], memberObj.twitterOBJ[1], twitterID)
                                        if replied:
                                            resp = api.tweetEventComment(serverName, userID, tweetID)
                                            if type(resp) == int:
                                                await discord.utils.get(interaction.guild.channels, name=api.getChannel(serverID, "notifs")).send("✅ **" + userID + "** replied to a raid tweet for `" + str(resp) + " 🎟️'s`!")
                                                await interaction.response.send_message(embed=raidCompleteEmbed("`replying` to"), ephemeral=True)
                                            else:
                                                await interaction.response.send_message(embed=userErrorEmbed("You're not eligible to earn 🎟️'s for `replying` to this Raid", resp), ephemeral=True)
                                        else:
                                            await interaction.response.send_message(embed=userErrorEmbed("No 🎟️'s Earned", "We weren't able to verify completion of **" + memberObj.handle + "** `replying` to this raid."), ephemeral=True)
        
                                            
                                    @discord.ui.button(label="Claim Retweet 🎟️'s", style=discord.ButtonStyle.red)
                                    async def retweet(self, interaction: discord.Interaction, button: discord.ui.Button):
                                        serverName = interaction.guild.id
                                        userID = interaction.user.name + "#" + interaction.user.discriminator
                                        
                                        memberObj = api.getMember(serverName, userID)
                                        if memberObj == None:
                                            gettingStartedID = str(discord.utils.get(interaction.guild.channels, name=api.getChannel(serverID, "get-started")).id)
                                            await interaction.response.send_message(embed=noOptIn(gettingStartedID), ephemeral=True)
                                            return
                                        liked, retweeted = twitter.likedRetweeted(memberObj.twitterOBJ[0], memberObj.twitterOBJ[1], twitterID)
                                        if retweeted:
                                            resp = api.tweetEventRetweet(serverName, userID, tweetID)
                                            if type(resp) == int:
                                                await discord.utils.get(interaction.guild.channels, name=api.getChannel(serverID, "notifs")).send("✅ **" + userID + "** retweeted a raid tweet for `" + str(resp) + " 🎟️'s`!")
                                                await interaction.response.send_message(embed=raidCompleteEmbed("`retweeting`"), ephemeral=True)
                                            else:
                                                await interaction.response.send_message(embed=userErrorEmbed("You're not eligible to earn 🎟️'s for `retweeting` this Raid", resp), ephemeral=True)
                                        else:
                                            await interaction.response.send_message(embed=userErrorEmbed("No 🎟️'s Earned", "We weren't able to verify completion of **" + memberObj.handle + "** `retweeting` this raid."), ephemeral=True)
                                
                                ## if link is blank, make an error message
                                if link == "" or falseLink(link):
                                    ## send a userErrorEmbed embed message
                                    await interaction.response.send_message(embed= userErrorEmbed("Raid Error: Tweet URL Not Valid", "Your new raid has not launched. To fix this issue, please enter a full valid tweet link, including `https://`"), ephemeral=True)
                                elif raidTitle == "":
                                    await interaction.response.send_message(embed=userErrorEmbed("Raid Error: Raid Title Not Valid", "Your new raid has not launched. To fix this issue, please enter a non-empty raid title"), ephemeral=True)
                                else:
                                    tweetID = api.createTwitterRaid(serverID, raidTitle, link, boosted, retweet, react, comment)
                                    twitterID = link.split("/")[-1].split("?")[0]
                                    
                                    xpAwards = xpAwards.strip()
                                    await interaction.response.send_message(embed = raidSuccessfulEmbed(str(self.url.value), xpAwards), ephemeral=True)
                                    await discord.utils.get(guild.channels, name=api.getChannel(serverID, "raids")).send(embed=getTwitterEmbed(str(self.url.value), retweet, react, comment, boosted), view=raidView())
                        await interaction.response.send_modal(addRaid())
                await interaction.response.send_message(content="Select the type of Raid you want (multiple can be picked)", ephemeral=True, view=raidSelector())
        
            @discord.ui.button(label="Raid Last Tweet", style=discord.ButtonStyle.primary)
            async def raidLastTweet(self, interaction: discord.Interaction, button: discord.ui.Button):
                ## check if the server has a "handle" set 
                serverID = interaction.guild.id
                if api.serverHandle(serverID) == None:
                    url, token, secret = twitter.link()
                    class linkTwitter(discord.ui.View):
                        def __init__(self):
                            super().__init__()
                            self.value = None
                            self.timeout = VIEW_TIMEOUT
                        @discord.ui.button(label="Verify Code", style=discord.ButtonStyle.green)
                        async def enterCode(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
                            class linkTwitterModal(ui.Modal, title = "Twitter OAuth Code"):
                                pin = ui.TextInput(label = "Verify and link your account", style=discord.TextStyle.short, placeholder="Copy and paste your OAuth pin-code here", required = True)
                                async def on_submit(self, interaction: discord.Interaction):
                                    pin = self.pin.value
                                    tweeterOBJ = twitter.auth(token, secret, pin)
    
                                    if tweeterOBJ != None:
                                        handle = "@" + str(tweeterOBJ[3])
                                        server = interaction.guild.id
                                        if api.storeTwitterHandle(server, tweeterOBJ):
                                            ## send a success embed serverTweetLink()
                                            await interaction.response.send_message(embed=serverTweetLink(handle), ephemeral=True)
                                        else:
                                            await interaction.response.send_message(embed=errorEmbed("We were unable to complete the opt-in process at this time. Please try again later."), ephemeral=True)
                                    else:
                                        await interaction.response.send_message(embed=userErrorEmbed("We couldn't verify this Twitter Account", "The pin code you entered was incorrect. Please review the instructions above and try again."), ephemeral=True)
                            await interaction.response.send_modal(linkTwitterModal())
                            
                    ## send the linkCommunityTwitter() embed with the linkTwitter() view
                    await interaction.response.send_message(embed=linkCommunityTwitter(url), view=linkTwitter(), ephemeral=True)
                    
                else:
                    twitterOBJ = api.serverTwitter(serverID)
                    if twitterOBJ != None:
                        access, seceret = twitterOBJ[0], twitterOBJ[1]
                        try:
                            lastCode = twitter.getLastTweetLink(access, seceret)
                            class raidSelector(discord.ui.View):
                                def __init__(self):
                                    super().__init__()
                                    self.value = None
                                    self.timeout = VIEW_TIMEOUT
                                @discord.ui.select(placeholder="Select a Raid", min_values = 1, max_values = 3, options=[
                                    discord.SelectOption(label="Retweet", description="Award 🎟️'s for Retweets", emoji="🔁"),
                                    discord.SelectOption(label="Like", description="Award 🎟️'s for Likes", emoji="❤️"), 
                                    discord.SelectOption(label="Reply", description="Award 🎟️'s for Replies", emoji="📝")
                                    ])
                                async def on_select(self, interaction: discord.Interaction, select: discord.ui.Select):
                                    xpAwards = ""
                                    serverID = interaction.guild.id
                                    link = lastCode
                                    boosted, retweet, react, comment = False, False, False, False
                                    for value in select.values:
                                        if "retweet" in value.lower():
                                            retweet = True
                                            xpAwards += " `Retweet`"
                                        elif "like" in value.lower():
                                            react = True
                                            xpAwards += " `React`"
                                        elif "reply" in value.lower():
                                            comment = True
                                            xpAwards += " `Comment`"
                                        
                                    xpAwards = xpAwards.strip()
                                    tweetID = api.createTwitterRaid(serverID, "Last Tweet Raid", link, boosted, retweet, react, comment)
                                    twitterID = link.split("/")[-1].split("?")[0]
                                                
                                    class raidView(discord.ui.View):
                                        def __init__(self):
                                            super().__init__()
                                            self.value = None
                                            self.timeout = VIEW_TIMEOUT
                                        @discord.ui.button(label="Claim Like 🎟️'s", style=discord.ButtonStyle.primary)
                                        async def react(self, interaction: discord.Interaction, button: discord.ui.Button):
                                            serverName = interaction.guild.id
                                            userID = interaction.user.name + "#" + interaction.user.discriminator
                                            
                                            memberObj = api.getMember(serverName, userID)
                                            if memberObj == None:
                                                gettingStartedID = str(discord.utils.get(interaction.guild.channels, name=api.getChannel(serverID, "get-started")).id)
                                                await interaction.response.send_message(embed=noOptIn(gettingStartedID), ephemeral=True)
                                                return
                                            liked, retweeted = twitter.likedRetweeted(memberObj.twitterOBJ[0], memberObj.twitterOBJ[1], twitterID)
                                            if liked:
                                                resp = api.tweetEventReact(serverName, userID, tweetID)
                                                if type(resp) == int:
                                                    await discord.utils.get(interaction.guild.channels, name=api.getChannel(serverID, "notifs")).send("✅ **" + userID + "** liked a raid tweet for `" + str(resp) + " 🎟️'s`!")
                                                    await interaction.response.send_message(embed=raidCompleteEmbed("`reacting` to"), ephemeral=True)
                                                else:
                                                    await interaction.response.send_message(embed=userErrorEmbed("You're not eligible to earn 🎟️'s for `liking` this Raid", resp), ephemeral=True)
                                            else:
                                                await interaction.response.send_message(embed=userErrorEmbed("No 🎟️'s Earned", "We weren't able to verify completion of **" + memberObj.handle + "** `liking` this raid."), ephemeral=True)
            
                                        @discord.ui.button(label="Claim Reply 🎟️'s", style=discord.ButtonStyle.green)
                                        async def comment(self, interaction: discord.Interaction, button: discord.ui.Button):
                                            serverName = interaction.guild.id
                                            userID = interaction.user.name + "#" + interaction.user.discriminator
                                            memberObj = api.getMember(serverName, userID)
                                            if memberObj == None:
                                                gettingStartedID = str(discord.utils.get(interaction.guild.channels, name=api.getChannel(serverID, "get-started")).id)
                                                await interaction.response.send_message(embed=noOptIn(gettingStartedID), ephemeral=True)
                                                return
                                            replied = twitter.hasCommented(memberObj.twitterOBJ[0], memberObj.twitterOBJ[1], twitterID)
                                            if replied:
                                                resp = api.tweetEventComment(serverName, userID, tweetID)
                                                if type(resp) == int:
                                                    await discord.utils.get(interaction.guild.channels, name=api.getChannel(serverID, "notifs")).send("✅ **" + userID + "** replied to a raid tweet for `" + str(resp) + " 🎟️'s`!")
                                                    await interaction.response.send_message(embed=raidCompleteEmbed("`replying` to"), ephemeral=True)
                                                else:
                                                    await interaction.response.send_message(embed=userErrorEmbed("You're not eligible to earn 🎟️'s for `replying` to this Raid", resp), ephemeral=True)
                                            else:
                                                await interaction.response.send_message(embed=userErrorEmbed("No 🎟️'s Earned", "We weren't able to verify completion of **" + memberObj.handle + "** `replying` to this raid."), ephemeral=True)
            
                                                
                                        @discord.ui.button(label="Claim Retweet 🎟️'s", style=discord.ButtonStyle.red)
                                        async def retweet(self, interaction: discord.Interaction, button: discord.ui.Button):
                                            serverName = interaction.guild.id
                                            userID = interaction.user.name + "#" + interaction.user.discriminator
                                            
                                            memberObj = api.getMember(serverName, userID)
                                            if memberObj == None:
                                                gettingStartedID = str(discord.utils.get(interaction.guild.channels, name=api.getChannel(serverID, "get-started")).id)
                                                await interaction.response.send_message(embed=noOptIn(gettingStartedID), ephemeral=True)
                                                return
                                            liked, retweeted = twitter.likedRetweeted(memberObj.twitterOBJ[0], memberObj.twitterOBJ[1], twitterID)
                                            if retweeted:
                                                resp = api.tweetEventRetweet(serverName, userID, tweetID)
                                                if type(resp) == int:
                                                    await discord.utils.get(interaction.guild.channels, name=api.getChannel(serverID, "notifs")).send("✅ **" + userID + "** retweeted a raid tweet for `" + str(resp) + " 🎟️'s`!")
                                                    await interaction.response.send_message(embed=raidCompleteEmbed("`retweeting`"), ephemeral=True)
                                                else:
                                                    await interaction.response.send_message(embed=userErrorEmbed("You're not eligible to earn 🎟️'s for `retweeting` this Raid", resp), ephemeral=True)
                                            else:
                                                await interaction.response.send_message(embed=userErrorEmbed("No 🎟️'s Earned", "We weren't able to verify completion of **" + memberObj.handle + "** `retweeting` this raid."), ephemeral=True)
                                                
                                    await interaction.response.send_message(embed = raidSuccessfulEmbed(str(link), xpAwards), ephemeral=True)
                                    await discord.utils.get(guild.channels, name=api.getChannel(serverID, "raids")).send(embed=getTwitterEmbed(str(self.url.value), retweet, react, comment, boosted), view=raidView())
                                    
                            await interaction.response.send_message(content="Select the type of Raid you want (multiple can be picked) for the Community's last tweet: [" + lastCode+"]("+lastCode+")", ephemeral=True, view=raidSelector())        
                            
                        except:
                            await interaction.response.send_message(embed=userErrorEmbed("Last Tweet Not Found", "Please make sure your Twitter account is public and has at least one tweet"), ephemeral=True)
                    else:
                        await interaction.response.send_message(embed=userErrorEmbed("We couldn't verify this Twitter Account", "Contact Jackpot Support to fix this problem"), ephemeral=True)
                
                
        await discord.utils.get(guild.channels, name=api.getChannel(serverID, "launch-raid")).send(embed=getRaidsEmbed(), view = raids())
    
@client.event
async def on_ready():
    print("Logged in")
    global TIMMER
    
    if TIMMER == False:
        billing.start()
        changeMessages.start()
        saveAssets.start()
        checkTasks.start()
        TIMMER = True
    
    for guild in client.guilds:
        await bot_set_up(guild)
        
## run when bot is in a new server
@client.event
async def on_guild_join(guild):
    await bot_set_up(guild)
        
@client.event
async def on_message(message):
    try:
        serverName = message.guild.id
    except:
        serverName = None
    
    memberID = message.author.name + "#" + message.author.discriminator
    userName = message.author.name
    text = message.content
    try:
        allChannels = api.getAllChannels(serverName)
    except:
        allChannels = []
    if message.author != client.user and message.channel.name in allChannels:
        ##warning = await message.channel.send(embed=userErrorEmbed("Your message has been deleted", "Please use other server channels to communicate."), ephemeral=True)
        await message.delete()
        return
    
    if message.author == client.user:
        if serverName != None and message.content.startswith("FETCHING RANK..."):       
            try:
                messageData = message.content
                memberID = messageData.split("#|#")[1].strip()
                serverRank, serverTrend, serverXP, globalRank, globalXP = api.getRank(serverName, memberID)
                newMes = await message.channel.send(embed=getRankEmbed(memberID, serverRank, globalRank, serverXP, globalXP))
                await message.delete()
                await asyncio.sleep(10)
                await newMes.delete()
            except:
                newMes = await message.channel.send(embed=cmdErrorEmbed("Unable to retrieve rank for " + memberID, "This user has not opted-in or does not exist. Make sure to enter the full username, i.e. `TheName#1234`"))
                await message.delete()
                await asyncio.sleep(10)
                await newMes.delete()
                
        if serverName != None and message.content.startswith("GETTING THE LEADERBOARD..."):
            try:
                messageData = message.content
                serverID = messageData.split("#|#")[1].strip()
                ## leaderboardID =  str(discord.utils.get(message.guild.channels, name="leaderboard").id)
                top3 = api.getTop3(int(serverID))
                newMes = await message.channel.send(embed=cmdLeaderboardURL(top3))
                await message.delete()
                await asyncio.sleep(10)
                await newMes.delete()
                
            except:
                newMes = await message.channel.send(embed=cmdErrorEmbed("Something went wrong.", "We're unable to retrieve this Server's leaderboard at this time. Please try again in a few minutes."))
                await message.delete()
                await asyncio.sleep(10)
                await newMes.delete()
                
        if serverName != None and message.content.startswith("FETCHING JACKPOT..."):
            try:
                messageData = message.content
                newMes = await message.channel.send(embed=cmdJackpotEmbed())
                await message.delete()
                await asyncio.sleep(10)
                await newMes.delete()
                
            except:
                newMes = await message.channel.send(embed=cmdErrorEmbed("Something went wrong.", "We're unable to retrieve the Jackpot at this time. Please try again in a few minutes."))
                await message.delete()
                await asyncio.sleep(10)
                await newMes.delete()
        
        ## if a message is sent in the #missions channel, check if it starts with "MISSION SUBMITTED" 
        elif serverName != None and message.channel.name == api.getChannel(serverName, "quests") and message.content.startswith("MISSION SUBMITTED"):
            messageData = message.content.split("#|#")
            memberID = messageData[1].strip()
            ## check if memberID is valid and has the Jackpot Role
            if api.checkOptIn(serverName, memberID) != False:
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
                    missionXP, missionDis = api.getMissionXP(serverName, missionID), api.getMissionDescription(serverName, missionID)
                    missionUID = api.genMissionID(serverName, memberID, missionID)
                    database.add_mission(missionUID, missionName, memberID, serverName, missionXP, missionDis, textData + "\n\n" + attachment)
                    newMessage = await discord.utils.get(message.guild.channels, name=api.getChannel(serverName, "notifs")).send("📨 **"+memberID+"** completed the quest **"+missionName+"**")
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
                                await interaction.response.send_message("QUEST **NOT** APPROVED \n Quest total limit or per person limit exceeded", ephemeral=True)
                            else:
                                await interaction.response.send_message("QUEST APPROVED", ephemeral=True)
                                ## delete the main message the button was pressed on
                                await interaction.message.delete()
                                ## delete newMessage
                                # await newMessage.delete()
                                ## send a message to #notifs with the mission name, username, and 🎟️'s
                                await discord.utils.get(message.guild.channels, name=api.getChannel(serverName, "notifs")).send("✅ **"+memberID+"'s** submission for **" + missionName + "** has been approved for `" + str(missionReward) + " 🎟️'s`!")
                            
                        @discord.ui.button(label="DENY", style=discord.ButtonStyle.red)
                        async def deny(self, interaction2: discord.Interaction, button: discord.ui.Button) -> None:
                            class feedbackMission(ui.Modal, title = "Send feedback to " + memberID[:12] + "..."):
                                feedback = ui.TextInput(label = "Reason why quest declined", style=discord.TextStyle.long, default = "You have not completed the quest's spec", required = True)
                                async def on_submit(self, interaction: discord.Interaction):
                                    await discord.utils.get(message.guild.channels, name=api.getChannel(serverName, "notifs")).send("❌ **"+memberID+"'s** submission for **" + missionName + "** has been denied. Reason: `" + self.feedback.value + "`")
                                    await interaction.response.send_message("QUEST DENIED", ephemeral=True)
                            await interaction2.response.send_modal(feedbackMission())
                            await interaction2.message.delete()
                    
                    missionReward = api.getMissionXP(serverName, missionID)
                        
                else:
                    if missionID == False:
                        resp = await message.reply(embed = userErrorEmbed("Invalid quest name.", "We were unable to find a quest with that name, it may have been recently deleted. Please try again (case sensitive)."))
                        await message.delete()
                        await asyncio.sleep(10)
                        await resp.delete()
                    else: 
                        resp = await message.reply(embed = userErrorEmbed("You are not eligible for this quest.", "Either a personal limit or global limit for 🎟️'s rewards has been met. Please try again with a different quest."))
                        await message.delete()
                        await asyncio.sleep(10)
                        await resp.delete()
            else:
                getStarted = str(discord.utils.get(message.guild.channels, name="get-started").id)
                ## send an embed in the missions channel noOptIn(getStarted)
                missionsMessage = await discord.utils.get(message.guild.channels, name=api.getChannel(serverName, "quests")).send(embed = noOptInMissions(getStarted, memberID))
                await message.delete()
                ## delete the replyMessage after 10 seconds
                await asyncio.sleep(10)
                await missionsMessage.delete()
                
        elif serverName != None and message.channel.name != api.getChannel(serverName, "quests") and message.content.startswith("MISSION SUBMITTED"):
            missions = str(discord.utils.get(message.guild.channels, name=api.getChannel(serverName, "quests")).id)
            ## get the channel message was sent in 
            channelN = message.channel.name
            await message.delete()
            ## in the channel the message was sent in, send an error embed
            missionMessgae = await discord.utils.get(message.guild.channels, name=channelN).send(embed = missionCompleteCommandInvalid(missions))
            await asyncio.sleep(10)
            await missionMessgae.delete()
        else:
            return
        
    ## if the message is in a DM or in the bot channel, ignore it
    channelNames = api.getAllChannels(serverName)
    if serverName != None and message.channel.name not in channelNames and text.startswith("/") == False:
        if api.checkOptIn(serverName, memberID) != False:
            ## see if the message mentions someone
            origAuthorID = ""
            receivedXP = False
            
            if message.reference != None:
                origAuthorID = message.reference.resolved.author.name + "#" + message.reference.resolved.author.discriminator
                if origAuthorID == memberID:
                    receivedXP = True
                    api.xpEvent(serverName, memberID, 1)
                else:
                    if origAuthorID != memberID and api.checkOptIn(serverName, origAuthorID) != False:
                        api.xpEvent(serverName, origAuthorID, 6) 
                    if origAuthorID != memberID and receivedXP == False and api.isNew(serverName, origAuthorID, memberID):
                        receivedXP = True
                        api.xpEvent(serverName, memberID, 4)
                
            for mention in message.mentions:
                mentionID = mention.name + "#" + mention.discriminator
                if mentionID != origAuthorID and receivedXP == False and api.isNew(serverName, mentionID, memberID):
                    receivedXP = True
                    api.xpEvent(serverName, memberID, 4)
                    
            if receivedXP == False:
                api.xpEvent(serverName, memberID, 1)
        
        elif message.reference != None:
            origAuthorID = message.reference.resolved.author.name + "#" + message.reference.resolved.author.discriminator
            if origAuthorID != memberID and api.checkOptIn(serverName, origAuthorID) != False:
                    api.xpEvent(serverName, origAuthorID, 6) 
            
## create an event to see everytime a user reacts to a message
@client.event
async def on_raw_reaction_add(payload):
    serverName = payload.guild_id
    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    emoji = payload.emoji.name
    user = payload.member.name + "#" + payload.member.discriminator
    originalAuthor = message.author.name + "#" + message.author.discriminator
    ## if the reaction is on a message in a bot channel and in a DM, ignore it
    channelNames = api.getAllChannels(serverName)
    if originalAuthor != user and channel.name not in channelNames and channel.type != discord.ChannelType.private:
        if api.checkOptIn(serverName, originalAuthor) != False:
            api.xpEvent(serverName, originalAuthor, 3)
        if api.checkOptIn(serverName, user) != False:
            api.xpEvent(serverName, user, 2)
                
## if a new user joins the server, assign them the Jackpot Non-Opt-In role
@client.event
async def on_member_join(member):
    valueNew = api.addNewMember(member.guild.id, member.name, member.name + "#" + member.discriminator)
    ## if the user does not have the Jackpot role or the Jackpot Non-Opt-In role, then assign the Jackpot Non-Opt-In role and not a bot
    # if not discord.utils.get(member.roles, name=JACKPOT_ROLE) and not discord.utils.get(member.roles, name=JACKPOT_NON_OPT) and discord.utils.get(member.roles, name=BOT_ROLE) == None:
    #    await member.add_roles(discord.utils.get(member.guild.roles, name=JACKPOT_NON_OPT))
    
    if valueNew != False:
        prev_invites = api.getInvites(member.guild.id)
        cur_invites = await member.guild.invites()
        
        for invite in prev_invites:
            if invite.uses < find_invite_by_code(cur_invites, invite.code).uses:
                inviter = invite.inviter
                if api.getMember(member.guild.id, str(inviter)) != None:
                    valueNew.referer = str(inviter)
                    api.xpEvent(member.guild.id, str(inviter), 5)
                    await discord.utils.get(member.guild.channels, name=api.getChannel(member.guild.id, "notifs")).send(f"❤️ **{str(inviter)}** just invited {member.mention} to the server and earned `"+ api.getReward(None, None, 5) +"`!")
    
    api.updateInvites(member.guild.id, cur_invites)
                    
## if a user leaves the server
@client.event
async def on_member_remove(member):
    try:
        memberID = member.name + "#" + member.discriminator
        memberObj = api.findNewMember(member.guild.id, memberID)
        
        if memberObj != None and memberObj.referer != None and api.getMember(member.guild.id, memberObj.referer) != None:
            api.xpEvent(member.guild.id, memberObj.referer, -5)
                        
        curInvites = await member.guild.invites()
        api.updateInvites(member.guild.id, curInvites)
    except:
        print("SERVER REMOVED")

## add an event whenever a channel name is changed
@client.event
async def on_guild_channel_update(before, after):
    serverID = before.guild.id
    berforeName = before.name
    afterName = after.name
    api.updateServers(serverID, berforeName, afterName)


#@client.event
#async def on_member_update(before, after):
## if the user does not have the Jackpot role or the Jackpot Non-Opt-In role, then assign the Jackpot Non-Opt-In role and not a bot
    #if not discord.utils.get(after.roles, name=JACKPOT_ROLE) and not discord.utils.get(after.roles, name=JACKPOT_NON_OPT) and discord.utils.get(after.roles, name=BOT_ROLE) == None:
    #    await after.add_roles(discord.utils.get(after.guild.roles, name=JACKPOT_NON_OPT))   
    
## @client.event for when a member becomes active on the server
@client.event
async def on_presence_update(before, after):
    serverName = after.guild.id
    userName = after.name + "#" + after.discriminator
    
    ## if the user does not have the Jackpot role or the Jackpot Non-Opt-In role, then assign the Jackpot Non-Opt-In role and not a bot
    # if not discord.utils.get(after.roles, name=JACKPOT_ROLE) and not discord.utils.get(after.roles, name=JACKPOT_NON_OPT) and discord.utils.get(after.roles, name=BOT_ROLE) == None:
    #     await after.add_roles(discord.utils.get(after.guild.roles, name=JACKPOT_NON_OPT))
    if api.checkOptIn(serverName, userName) and before.status != after.status:
        if str(after.status) == "online" and api.serverVisit(serverName, userName):
            api.xpEvent(serverName, userName, 9)
            
            ## send a message in the notifs channel
            reward = api.getReward(serverName, userName, 9)
            await discord.utils.get(after.guild.channels, name=api.getChannel(serverName, "notifs")).send("✅ **" + userName + "** visited the server today and got `" + str(reward) + "`!")

## create a function called "invited," so if I import this file, I can call this function and it will send a message to the notifs channel
async def invited(serverID, inviter):
    for guild in client.guilds:
        if guild.id == serverID:
            api.serverInvite(serverID, inviter)
            await discord.utils.get(guild.channels, name=api.getChannel(serverID, "notifs")).send(f"💎 **{inviter}** referred a new community to Jackpot for `15000 🎟️'s`!")
            await discord.utils.get(guild.channels, name=api.getChannel(serverID, "notifs")).send(f"🎁 **Everyone in your community** has been gifted `3000 🎟️'s` thanks to **{inviter}'s** referral!")
            break
        
async def crystalize(serverIDs):
    for guild in client.guilds:
        if guild.id in serverIDs:
            publicChannels = []
            ## append all public channels where guild.default_role can send and read messages
            for channel in guild.channels:
                if channel.type == discord.ChannelType.text and channel.permissions_for(guild.default_role).send_messages and channel.permissions_for(guild.default_role).read_messages:
                    publicChannels.append(channel)
            
            ## randomly select a channel from the public channels
            channel = random.choice(publicChannels)
            
            class getCr(discord.ui.View):
                def __init__(self):
                    super().__init__()
                    self.value = None
                    self.timeout = VIEW_TIMEOUT
                @discord.ui.button(label="Catch Crystal", style=discord.ButtonStyle.primary)
                async def catch(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
                    serverID = interaction.guild.id
                    isTrue = api.crystalCheck(serverID)
                    if isTrue:
                        ## send xp
                        api.xpEvent(serverID, interaction.user.name + "#" + interaction.user.discriminator, 20)
                        ## send a message in the notifs channel
                        await discord.utils.get(interaction.guild.channels, name=api.getChannel(serverID, "notifs")).send("💎 **" + interaction.user.name + "#" + interaction.user.discriminator + "** caught the Crystal and got `5000 🎟️'s`!")
                        await interaction.response.send_message(embed=getCaughtEmbed(), ephemeral=True)
                        ## delete the original message 
                        await interaction.message.delete()
                    else:
                        ## send the userErrorEmbed() as a response
                        await interaction.response.send_message(embed=userErrorEmbed("This Crystal was already caught!", "Try again next time!"), ephemeral=True)
            
            ## send the getCrystalEmbed() to the channel
            await channel.send(embed=getCrystalEmbed(), view=getCr())          
        
async def missionComplete(missionUID, feedback = None):
    serverID, memberID, missionID = api.readMissionID(missionUID)
    serverID = int(serverID)
    missionID = int(missionID)
    missionXP, missionName = api.getMissionXP(serverID, missionID), api.getMissionName(serverID, missionID)
    
    for guild in client.guilds:
        if guild.id == serverID:
            if feedback != None:
                await discord.utils.get(guild.channels, name=api.getChannel(serverID, "notifs")).send("❌ **"+memberID+"'s** submission for **" + missionName + "** has been denied. Reason: `" + feedback + "`")
            else:
                missionReward = api.missionXPEvent(int(serverID), memberID, missionID)
                if missionReward == False:
                    await discord.utils.get(guild.channels, name=api.getChannel(serverID, "notifs")).send("❌ **"+memberID+"'s** submission for **" + missionName + "** has been denied. Reason: `" + "Quest total limit or per person limit exceeded" + "`")
                else:
                    await discord.utils.get(guild.channels, name=api.getChannel(serverID, "notifs")).send("✅ **"+memberID+"'s** submission for **" + missionName + "** has been approved for `" + str(missionReward) + " 🎟️'s`!")
        

## run a scheduled task every 24 hours
@tasks.loop(hours=24)
async def billing():
    for guild in client.guilds:
        guidID = guild.id
        deadLine = api.getServerDeadline(guidID)
        ## deadline is a date object
        if deadLine != None and deadLine - datetime.now() < pd.Timedelta(days=21):
            numDays = (deadLine - datetime.now()).days
            missionMes = await discord.utils.get(guild.channels, name=api.getChannel(guidID, "add-quests")).send(embed = willBeExpired(numDays))
            raidMes = await discord.utils.get(guild.channels, name=api.getChannel(guidID, "launch-raid")).send(embed = willBeExpired(numDays))
            api.setServerEndMessage(guidID, [missionMes, raidMes])
        else:
            messObj = api.getServerEndMessage(guidID)
            if messObj != None:
                api.setServerEndMessage(guidID, None)
                for Objs in messObj:
                    await Objs.delete()
                    
@tasks.loop(hours=0.15)
async def changeMessages():
    for guild in client.guilds:
        guidID = guild.id
        ctx, ctx2 = api.gettingStarted(guidID), api.userSettings(guidID)
        ## ctx is a message id in the "get-started" channel
        if ctx != None:
            await ctx.edit(embed = getWelcomeEmbed())
        if ctx2 != None:
            await ctx2.edit(embed = getWelcomeOptInEmbed())
            
@tasks.loop(hours=0.05)
async def saveAssets():
    api.pickleAll()
    crystalServers = api.crystal()
    await crystalize(crystalServers)
            
@tasks.loop(hours=0.01)
async def checkTasks():
    print("checkingTasks")
    async def invite(syntax):
        serverID = syntax[1].strip()
        memberID = syntax[2].strip()
        await invited(int(serverID), memberID)
    
    async def jackpot(syntax):
        amount = syntax[1].strip()
        date = syntax[2].strip()
        winners = syntax[3].strip()
        api.newJackpot(amount, date, winners)
        return
    
    ## read the lines in TASK_PATH .txt file
    with open(TASK_PATH, "r") as f:
        lines = f.readlines()
    ## delete all the lines
    open(TASK_PATH, "w").close()
    
    ## for each command in the TASK_PATH .txt file, run the command
    for cmd in lines:
        syntax = cmd.split("|n|")
        command = syntax[0].strip()
        
        if command == "INVITE":
            await invite(syntax)
        
        if command == "JACKPOT":
            await jackpot(syntax)
            
        if command == "MISSION":
            await missionComplete(syntax[1].strip(), syntax[2].strip())
            
    ## create a file called tasklogs.txt and write the lines in it along with the current time
    ## make sure to append to the file
    with open("tasklogs.txt", "a") as f:
        f.write("==== " + str(datetime.now()) + " ===="  + "\n")
        f.writelines(lines)
        f.write("\n")

client.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)