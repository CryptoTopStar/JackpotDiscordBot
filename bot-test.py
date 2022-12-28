import discord
from discord.ui import Modal, InputText
import logging

discord.http.API_VERSION = 9
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
TOKEN = "MTAzNzYyOTMyMDIwMzYxNjI2Ng.GhpR78.NzFqeGnDD0IZdQCArpLiL5CSAmdLtPUZ0fvIuo"
client = discord.Client(intents=discord.Intents.all())
BOT_ROLE = "Jackpot Official"
ADMIN_ROLE = "Admin"
JACKPOT_ROLE = "Jackpot"
JACKPOT_NON_OPT = "Jackpot (Not Opted In)"

def getRaidsEmbed():
    embed=discord.Embed(title="⚔️ **Launch Twitter Raid** ⚔️", description="Click the button below to **Launch a Twitter Raid**", color=0xFF3F33)
    embed.add_field(name="**You'll be asked to:**", value="**1. Specify Tweet:** Paste the URL of the Tweet that you'd like to raid.\n**2. Choose Engagement Type:** Choose what type of engagement you'd like to incentivize.", inline=False) 
    return embed

def getMissionAddEmbed():
    embed=discord.Embed(title="🗺️ **Mission Admin** 🗺️", description="Click the buttons below to interact with your **Missions**.", color=0xe9e9e9)
    embed.add_field(name="1. **Add Mission:**", value="Click \"Add Mission\" to activate a new mission for your community. \n\nYou'll be able to specify the objective for the mission and set an appropriate XP reward for completion. The maximum possible reward for a single mission is 5,000 XP and the minimum is 50 XP. We suggest adding up to 15,000 XP of missions to maximize output from your community.", inline=False)
    embed.add_field(name="2. **Edit Mission:**", value="Click \"Edit Mission\" to change the details for any active mission.", inline=False)
    embed.add_field(name="3. **Delete Mission:**", value="Click \"Delete Mission\" to delete an active mission.", inline=False)
    return embed
    
def getGettingStartedEmbed():
    embed=discord.Embed(title="Get Started 🚀", description="We take data privacy very seriously. To begin earning XP, you must opt-in and connect your Twitter.", color=0xff6969)
    embed.set_author(name="Jackpot", url="https://getjackpot.xyz", icon_url="https://static.wixstatic.com/media/cdc018_a8e52bee9e114aa9a11355686b703954~mv2.png")
    embed.set_thumbnail(url="https://static.wixstatic.com/media/cdc018_a8e52bee9e114aa9a11355686b703954~mv2.png")
    embed.add_field(name="Opt-In", value="Navigate to #opt-in and follow the relevant instructions to start earning XP. Once you do this, you will not have to do it again.", inline=False) 
    embed.add_field(name="First Tweet Raid", value="Navigate to #raids to engage with tweets and earn XP.", inline=False) 
    embed.set_footer(text="⚠️ Failing to Opt-In will mean you will not be able to earn XP.")
    return embed

def getReferalEmbed():
    embed=discord.Embed(title="Unique Referral Code", description="Share your code with friends to refer a new community to Jackpot! If they sign up as a paying customer, you will earn a substantial XP bonus for yourself and everyone in your community!", color=0x222222)
    return embed 

def getOptIn():
    embed=discord.Embed(title="Congratulations!", description="**You have now successfully joined Jackpot and are eligible to win the Jackpot raffle!** \n\n You are now ready to begin earning XP for all the value you add to your community. As a token of our gratitude, you have been awarded `1000 XP 🎟️`", color=0x33FF5C)
    return embed 

def getOptInNoWallet():
    embed=discord.Embed(title="Congratulations!", description="**You have now successfully joined Jackpot. Until you add your ETH wallet address in the #user-settings channel you are ineligible to win the Jackpot raffle.** \n\n In the meantime, you are now ready to begin earning XP for all the value you add to your community. As a token of our gratitude, you have been awarded `1000 XP 🎟️`", color=0xcffc03)
    return embed 

def getRankEmbed(memID, serverRank, globalRank, XP, trend):
    if str(serverRank) == "1":
        descp = "You're the top contributor in this server! Keep up the great work!"
    else:
        descp = "Keep earning XP to rank up!"
    emoji = ""
    if trend == 1:
        emoji = " 🔼"
    elif trend == -1:
        emoji = " 🔽"
    embed = discord.Embed(title="🎖️ " + memID + " is Rank " + str(serverRank) + " in this Server", description=descp, color=0xEBF900)
    embed.add_field(name="More Stats:", value="🌎 Rank on the global leaderboard: `" + str(globalRank) + "`\n🎟️ Total XP earned in this period: `" + str(XP) + emoji + "` \n\n___", inline=True)
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
    embed = discord.Embed(title="**Join Now!**", description="Opt-in to immediately earn `1000 XP` 🎟️ and have a chance at winning the Jackpot Raffle.", color=0xf59b42)
    return embed
    
def getXPEmbed():
    embed=discord.Embed(title="**How to Earn XP**", description="Below is a guide to all the actions you can take in your community that will be automatically rewarded.", color=0xe9e9e9)
    embed.add_field(name="**Discord:**", value="🎟️ Sending messages *(diminishing returns)*\n🎟️ Reacting to messages *(diminishing returns)*\n🎟️ Other people reacting to your messages\n🎟️ Other people replying to your messages\n🎟️ Being one of the first people to interact with a new member\n🎟️ Inviting real people to the server\n🎟️ Visiting the server daily\n", inline=False) 
    embed.add_field(name="**Twitter:**", value = "🎟️ Retweeting a #raids tweet\n🎟️ Replying to a #raids tweet\n🎟️ Liking a #raids tweet\n🎟️ Following other community members\n🎟️ Being followed by other community members\n", inline=False) 
    embed.add_field(name="**Missions:**", value = "🎟️ Successfully completing #missions", inline=False)
    return embed

def getChannelsEmbed():
    embed=discord.Embed(title="**Channel Overview**", color=0xe9e9e9)
    embed.add_field(name="Important channels to keep track of:", value="📍 #user-settings | Review and change your personal details.\n📍 #leaderboard | Visit our website containing your community’s most valuable contributors.\n📍 #raids | Participate in Twitter raids to earn XP.\n📍 #missions | Choose from available missions and submit proof of completion.\n📍 #notifs | Get notified when you earn XP and your missions are approved.")
    return embed

def getWelcomeEmbed():
    embed=discord.Embed(title="**Welcome to Jackpot**",description="Jackpot is a simple, no-brainer loyalty and rewards program architected in collaboration with 100+ web3 industry veterans including founders, community managers, mods, and core contributors across the Ethereum and Solana ecosystems.\n\nEarn XP to climb the leaderboard and have a chance at winning the **Jackpot Raffle.**\n\n**1 XP = 1 Raffle Ticket**", color=0xe9e9e9)
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

def getTwitterEmbed(link, boosted=False):
    if boosted:
        mcolor = 0xf21d6a
        message = "**Engage** with the **Tweet** below to earn up to **2400 XP**\n\n🚨 **THIS RAID IS BOOSTED -- EARN 200% XP!** 🚨\n\nLike = **400 XP**\nReply = **800 XP**\nRetweet = **1200 XP**\n\n⛓ __**" + link + "**__ ⛓"
    else:
        mcolor = 0x1da1f2
        message = "**Engage** with the **Tweet** below to earn up to **1200 XP**\n\nLike = **200 XP**\nReply = **400 XP**\nRetweet = **600 XP**\n\n⛓ __**" + link + "**__ ⛓\n"
    embed=discord.Embed(title="**RAID ALERT**", description=message, color=mcolor)
    embed.set_author(name="Twitter Raid Rewards", icon_url="https://img.icons8.com/color/344/twitter--v1.png")
    embed.set_footer(text="Powered by Jackpot", icon_url="https://static.wixstatic.com/media/cdc018_603e1fc27c6a4c71b2c8c333f66c858b~mv2.png")
    return embed

def getMissionsEmbed():
    embed=discord.Embed(title="**🗺️ Missions 🗺️**", description="Click the **View Missions** button below to see your community's active missions and their respective XP rewards.", color=0xf21d6a)
    embed.add_field(name="**Submitting Mission Completion**", value="To get credit (XP) for completing a mission, in the message section below, type `/verify` followed by the mission id and your description (proof) of completion. If you click +1 more, you can add a screenshot to supplement the proof of completion provided.\n\n➡️ **Select an active mission from the dropdown to view its details.**", inline=False) 
    return embed

def getMissionDetailsEmbed(title, description, xp, count, supply, personLimit, timesSubmitted):
    embed=discord.Embed(title="**🗺️ " + title + " 🗺️**", description=description, color=0xf21d6a)
    embed.add_field(name="**Mission Information**", value="**XP PAYOUT:** `" + str(xp) + "` \n **REWARDS DISTRIBUTED SO FAR:** `" + str(count) + " out of " + str(supply) + "` \n", inline=False) 
    embed.add_field(name="**Submissions**", value="`You earned XP for this mission " + str(timesSubmitted) + " of a maximum of " + str(personLimit) + " times`", inline=False) 
    return embed

def getMissionsListEmbed(numMissions):
    embed=discord.Embed(title="✅ **Mission Complete** ✅", description="In this channel, use `!verify [MISSION_NAME] [additional details or explaination]` to submit proof of a specific mission. If you are attaching a picture, attach it to the same message.", color=0xe9e9e9)
    embed.add_field(name="**Use the dropdown to see Active Missions**", value=str(numMissions) + " missions are active", inline=False)
    embed.set_footer(text="\n\nOnce submitted, a community admin will be able to approve/disapprove your submission. If approved, you'll receive XP for your effort and will be notified in #notifs.") 
    return embed

@client.event
async def on_ready():
    print("Logged in")
    serverID = client.guilds[0].id
    serverName = client.guilds[0].name
    
    serverProfile = client.guilds[0].icon.url
    ##api.addServer(serverID, serverName, serverProfile)
    
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
    
    ## if any of the channels in prepChannels exist, delete them
    prepChannels = ["get-started", "user-settings", "leaderboard", "raids", "missions", "add-mission", "mission-approval", "launch-raid", "notifs"]
    for channel in prepChannels:
        if discord.utils.get(guild.channels, name=channel) != None:
            if channel != "notifs":
                await discord.utils.get(guild.channels, name=channel).delete()
            else:
                ## send a messgae in notifs that the bot is restarting
                await discord.utils.get(guild.channels, name=channel).send("🤖 **Jackpot Bot is restarting, this event has been logged** 🤖")
    
    channels = ["get-started"]
    for channel in channels:
        if discord.utils.get(guild.channels, name=channel) == None:
            await guild.create_text_channel(channel)
            await discord.utils.get(guild.channels, name=channel).set_permissions(guild.default_role, read_messages=False, send_messages=False)   
            await discord.utils.get(guild.channels, name=channel).set_permissions(discord.utils.get(guild.roles, name=BOT_ROLE), read_messages=True, send_messages=True)
            await discord.utils.get(guild.channels, name=channel).set_permissions(discord.utils.get(guild.roles, name=ADMIN_ROLE), read_messages=True, send_messages=True)
            await discord.utils.get(guild.channels, name=channel).set_permissions(discord.utils.get(guild.roles, name=JACKPOT_NON_OPT), read_messages=True, send_messages=False)
      
      
    ## PYCORD IMPLEMENTATION ####
    class optInModal(Modal):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            
            self.add_item(InputText(
                label = "Verify and link your account",
                placeholder="Copy and paste your OAuth code"
            ))
            
            self.add_item(InputText(
                label = "Wallet",
                placeholder="Wallet ID"
            ))
            
        async def callback(self, interaction: discord.Interaction):
            await interaction.response.send_message("Thanks for verifying your account!", ephemeral=True)
    
            
    primaryButton = discord.ui.Button(label="Get Started", style=discord.ButtonStyle.green)
    secondaryButton = discord.ui.Button(label="Verify Twitter", style=discord.ButtonStyle.green)
    
    async def callback1(interaction):
        await interaction.response.send_modal(optInModal(title = "Verify and Link your account"))
        
    secondaryButton.callback = callback1
    view = discord.ui.View(timeout = None)
    view.add_item(secondaryButton)
    
    async def callback0(interaction):
        await interaction.response.send_message(embed=getTwitterOAUTHEmbed(), view=view, ephemeral=True)
    
    primaryButton.callback = callback0
    viewP = discord.ui.View(timeout = None)
    viewP.add_item(primaryButton)
    
    
            
    if discord.utils.get(guild.channels, name="get-started").last_message == None or discord.utils.get(guild.channels, name="get-started").last_message.author != client.user:
        await discord.utils.get(guild.channels, name="get-started").send(file=discord.File("Assets/Get Started.gif"))
        await discord.utils.get(guild.channels, name="get-started").send(embed=getWelcomeEmbed())
        await discord.utils.get(guild.channels, name="get-started").send(embed=getXPEmbed())
        await discord.utils.get(guild.channels, name="get-started").send(embed=getChannelsEmbed())
        await discord.utils.get(guild.channels, name="get-started").send(embed=getCommandsEmbed())
        await discord.utils.get(guild.channels, name="get-started").send(embed = getIntroEmbed(), view = viewP)
"""
    class optInModal2(ui.Modal):
        tweeterHandle = ui.InputText(label = "Verify and link your account", placeholder="Copy and paste your OAuth code here", required = True)
        walletID = ui.InputText(label = "Enter your Ethereum wallet address (Optional)", placeholder="Jackpot winnings won't be awarded if blank", required = False)
        async def on_submit(self, interaction: discord.Interaction):
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
            ##if api.optInMember(server, memberID, memIDNum, memberName, profilePic, handle, walledID):
            if True:
                ## create an XP event
                ##api.xpEvent(server, memberID, 0)
                ##reward = api.getReward(server, memberName, 0)
                reward = 1
                ## put on the notifs channel that a user has opted in
                await discord.utils.get(guild.channels, name="notifs").send("✅ **" + str(interaction.user) + "** has opted in and earned " + reward + "!")
                
                ## DEPRECATED: assign the Jackpot role to the user
                ## await interaction.response.send_message(content="✅ **Success!**\n\nYou have now successfully opted in to Jackpot and have been awarded `1000 XP` 🎟️ as a token of our gratitude. You are now ready to begin earning XP for the value you bring to the table.", ephemeral=True)
                await interaction.user.add_roles(discord.utils.get(guild.roles, name=JACKPOT_ROLE))
                await interaction.user.remove_roles(discord.utils.get(guild.roles, name=JACKPOT_NON_OPT))
                
                ## if user submits a wallet ID, show the getOptIn() embed
                if walledID != "" and walledID != None:
                    await interaction.response.send_message(embed=getOptIn(), ephemeral=True)
                else:
                    await interaction.response.send_message(embed=getOptInNoWallet(), ephemeral=True)
                
            else:
                await interaction.response.send_message(content="✅ **You're already opted-in!**\n\nHead over to #guide to see all of the ways you can earn XP 🎟️.", ephemeral=True)
                await interaction.user.add_roles(discord.utils.get(guild.roles, name=JACKPOT_ROLE))
"""
        
client.run(TOKEN)