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
    
    ##refreshCommands(data)
    data = {"1053902791321604217":["TEST1"], "1060683867935223869":["TEST2"]}
    refreshCommands(data)

def refreshCommands(data):
    def makeChoices(myID):
        choices = []
        for missions in data[myID]:
            choices.append(interactions.Choice(name=missions, value=missions))
        if len(choices) == 0:
            choices.append(interactions.Choice(name="No missions available", value="NULL"))
        return choices
    
    @bot.command(
        name="complete1000",
        description="Verify a completed mission to earn XP.",
        scope="1060683867935223869",
        ## add 3 options, a mission ID (can either be "1", "2", "3"), a description (string), and a file attachment
        options = [
            interactions.Option(name="quest_id", description="Quest ID", type=interactions.OptionType.STRING, required=True, choices=makeChoices("1060683867935223869")),
            interactions.Option(name="description", description="Description of the mission", type=interactions.OptionType.STRING, required=True),
            interactions.Option(name="file", description="Add an image (optional)", type=interactions.OptionType.ATTACHMENT, required=False)
        ]
    )
                    
    async def verifyMission(ctx: interactions.CommandContext, quest_id: str, description: str, file: interactions.File = None):
        stem = ""
        if file != None:
            stem = f"#|# {file.url}"
        fullName = ctx.author.name + "#" + ctx.author.discriminator
        await ctx.send(f"MISSION SUBMITTED #|# {fullName} #|# {quest_id} #|# {description} " + stem)

    @bot.command(
        name="complete",
        description="Verify a completed mission to earn XP.",
        scope="1053902791321604217",
        ## add 3 options, a mission ID (can either be "1", "2", "3"), a description (string), and a file attachment
        options = [
            interactions.Option(name="quest_id", description="Quest ID", type=interactions.OptionType.STRING, required=True, choices=makeChoices("1053902791321604217")),
            interactions.Option(name="description", description="Description of the mission", type=interactions.OptionType.STRING, required=True),
            interactions.Option(name="file", description="Add an image (optional)", type=interactions.OptionType.ATTACHMENT, required=False)
        ]
    )
                    
    async def verifyMission(ctx: interactions.CommandContext, quest_id: str, description: str, file: interactions.File = None):
        stem = ""
        if file != None:
            stem = f"#|# {file.url}"
        fullName = ctx.author.name + "#" + ctx.author.discriminator
        await ctx.send(f"MISSION SUBMITTED #|# {fullName} #|# {quest_id} #|# {description} " + stem)
            

    bot.start()

getData()