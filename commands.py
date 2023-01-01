import interactions
import time
import json

TOKEN = "MTAzNzYyOTMyMDIwMzYxNjI2Ng.GhpR78.NzFqeGnDD0IZdQCArpLiL5CSAmdLtPUZ0fvIuo"
bot = interactions.Client(token=TOKEN)

def getData():
    ## read in the JSON dict of missions in Cache/missions.json
    with open("./Cache/missions.json", "r") as f:
        data = json.load(f)
    
    if data == None or data == {}:
        data = {}
        data[1053902791321604217] = ["LOLLLLLL", "MYMISSION1", "MY MISSION 2"]
    
    refreshCommands(data)

def refreshCommands(data):
    def makeChoices(myID):
        choices = []
        for missions in data[myID]:
            choices.append(interactions.Choice(name=missions, value=missions))
        if len(choices) == 0:
            choices.append(interactions.Choice(name="No missions available", value="NULL"))
        return choices

    for ids in data.keys():

        @bot.command(
            name="complete",
            description="Verify a completed mission to earn XP",
            scope=ids,
            ## add 3 options, a mission ID (can either be "1", "2", "3"), a description (string), and a file attachment
            options = [
                interactions.Option(name="mission_id", description="Mission ID", type=interactions.OptionType.STRING, required=True, choices=makeChoices(ids)),
                interactions.Option(name="description", description="Description of the mission", type=interactions.OptionType.STRING, required=True),
                interactions.Option(name="file", description="Add an image (optional)", type=interactions.OptionType.ATTACHMENT, required=False)
            ]
        )
                        
        async def verifyMission(ctx: interactions.CommandContext, mission_id: str, description: str, file: interactions.File = None):
            stem = ""
            if file != None:
                stem = f"#|# {file.url}"
            fullName = ctx.author.name + "#" + ctx.author.discriminator
            await ctx.send(f"MISSION SUBMITTED #|# {fullName} #|# {mission_id} #|# {description} " + stem)
            
        ####### MORE COMMANDS HERE #######
        @bot.command(
            name="rank",
            description="Check your rank or someone else's rank in this Server",
            scope=ids,
            ## add 1 optional parameter, a user ID of the person you want to check the rank of
            options = [
                interactions.Option(name="user_id", description="OPTIONAL: Enter the full user ID of another person to view their rank", type=interactions.OptionType.USER, required=False)
            ]
        )
                        
        async def rankChecker(ctx: interactions.CommandContext, user_id: interactions.User = None):
            if user_id == None:
                user_id = ctx.author.name + "#" + ctx.author.discriminator
            else:
                user_id = user_id.name + "#" + user_id.discriminator
            await ctx.send(f"FETCHING RANK... #|# {user_id}")
            
        
        @bot.command(
            name="leaderboard",
            description="View the leaderboard for this Server",
            scope=ids,
        )  
        
        async def leaderboard(ctx: interactions.CommandContext):
            serverID = ctx.guild.id
            await ctx.send(f"GETTING THE LEADERBOARD... #|# {serverID}") 
            
        @bot.command(
            name="jackpot",
            description="View what's in the jackpot",
            scope=ids,
        )  
        
        async def jackpotRet(ctx: interactions.CommandContext):
            await ctx.send(f"FETCHING JACKPOT...") 
            

        bot.start()

getData()