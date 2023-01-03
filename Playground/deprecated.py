## if someone DMs the bot '!rank' then send them their rank by calling api.getRank(username, serverName)
if message.content.lower() == "!rank":
    ## see if user has role JACKPOT_ROLE
    if discord.utils.get(message.author.roles, name=JACKPOT_ROLE):
        serverRank, serverTrend, serverXP, globalRank, globalXP = api.getRank(serverName, memberID)
        await message.channel.send(embed=getRankEmbed(memberID, serverRank, globalRank, serverXP, globalXP))
    else: 
        await message.reply("To interact with me, opt-in via the `#get-started` channel")
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
        await message.reply("To interact with me, opt-in via the `#get-started` channel")
        
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