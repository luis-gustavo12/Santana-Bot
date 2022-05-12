'''
Hi everyone, my name is Luís Gustavo, and this git repo is for the usage of Santa Bot, which is handled through Heroku to run the whole application 24/7.

The main idea came when I, as a League of Legends player, got kind of stressed when I was at champion select, and faced a hard-to-counter champion (specially
when I was off role) and had to go through all the steps of typing "op.gg", champion stats bar, typing the champion I was against, etc... This process takes so long,
and most of times, you don't have all this time to pick the champion while in champion select. Then, when I was studying Web Scraping and also watched a video about how
to create Bots on Discord using Python, I had the idea of making eveything so simpler, by linking these two ideas. Why not creating a Bot in Discord for LoL players, since
almost every player uses Discord?

The Bot uses the op.gg domain to look for the three best counter champions, not taking too much time to return the required information.

Additionally, as a disclaimer, my intention was never to make money out of the op.gg Website, it was just a project I came up with to show my coding skills, since op.gg also
uses Riot Games API to look for all the data, which is free.
'''


import discord as disc
import logging
import requests
import os
import traceback
from bs4 import BeautifulSoup



# simple log handler
logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="log.txt", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter(
    "%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(handler)


client = disc.Client()


# preffix used to call the bot when at a server
preffix = "?"


# couple of tuples that handle popular ways of typing the champion, which makes easier to the user, instead of typing the exact name of the champion
renekton = {"renek"}
katarina = {"kat"}
aurelion = {"aurelion", "ausol"}
bardo = {"bardo", "bard"}
kogmaw = {"kog", "kogmaw", "kow maw"}
jarvan4 = {"jarvan", "j4", "jarvan iv"}
cho = {"cho","chogat"}
tf = {"twisted fate", "tf", "twisted"}
tk = {"tahm kench", "tk"}
nunu = {"nunu", "willump"}

# how roles are set to put them on the search bar
roles = ["top", "jg", "mid", "bot", "sup"]


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):

    if message.author == client.user:
        return





    elif message.content.startswith(f"{preffix}"):

        # Here, it looks for the role in the message, for example: "lucian mid", it will look for 'mid' in roles list

        if any(champRoles in message.content for champRoles in roles):
            if roles[0] in message.content:
                roleVar = roles[0]
            elif roles[1] in message.content:
                roleVar = roles[1]
            elif roles[2] in message.content:
                roleVar = roles[2]
            elif roles[3] in message.content:
                roleVar = roles[3]
            else:
                roleVar = roles[4]
            roleCondition = True
            champion = message.content.replace("?", "").replace(str(roleVar), "")

        else:
            champion = str(message.content).replace("?", "")
            roleCondition = False


        # Now, it applies the name that we need to put in the search bar, in order to look for the required champion
        if champion in bardo:
            champion = "bard"

        elif champion in renekton:
            champion = "renekton"

        elif champion in aurelion:
            champion = "aurelionsol"

        elif champion in katarina:
            champion = "katarina"

        elif champion in kogmaw:
            champion = "kogmaw"

        elif champion in jarvan4:
            champion = "jarvaniv"

        elif champion in cho:
            champion = "chogat"

        elif champion in  tf:
            champion = "twistedfate"

        elif champion in tk:
            champion = "tahmkench"

        elif champion in nunu:
            champion = "nunu"


        # Simple handle exception, regarding cases where the user types the champion's name wrongly
        try:
            if roleCondition:
                url = f"https://br.op.gg/champion/{champion}/statistics/{roleVar}/build"

            else:
                url = f"https://br.op.gg/champion/{champion}/statistics/build"

            # Web scrapping processes to get the three champions the most fit against
            
            header = {'user-agent': 'your-own-user-agent/0.0.1'}
            res = requests.get(url, headers=header)
            

            soup = BeautifulSoup(res.content, "lxml")
            

            mainChampBody = soup.find("body")
            
            
            champID = mainChampBody.find(id="__next")
            
            champDiv = champID.select(class_="#css-5juhhx e1o9af6t2")
            print(champDiv)
            

            goodAgainst = []

            counters = champID.find_all("tr")
            for tr in counters:
                champTd = tr.find(
                    class_="champion-stats-header-matchup__table__champion")
                goodAgainst.append(str(champTd).split("/>")[1].split()[0])

            # Message that will appear to the source, where the bot was originally called
            consoleMessage = "Best champion's counters are: {t}".format(
                t=str(goodAgainst).replace('[', '').replace(']', '').replace("'", ""))

            await message.channel.send(consoleMessage)



        # exception for when the users types wrongly
        except AttributeError:
            traceback.print_exc()
            await message.channel.send(f"Unfortunately, the champion \"{str(champion).capitalize()}\" doesn't exist in our database. Please, try again!")


#client.run(os.getenv('DISCORD_BOT_TOKEN'))
client.run("ODU1MTQ1OTc0ODgwMDEwMzEx.YMuOwA.JE72Il27kqJQ4mVSDB73WAzXqf8")
