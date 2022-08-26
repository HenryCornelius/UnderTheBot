# This example requires the 'message_content' privileged intent to function.

import discord
import random
import lolChamp
from riotwatcher import LolWatcher, ApiError

api_key = 'RGAPI-b0046366-a360-4dd9-b191-54a876fd14b7'
watcher = LolWatcher(api_key)
my_region = 'euw1'

def create_help_embed():
    embed = discord.Embed(title='**COMMANDS**',
                        description='', colour=discord.Colour.green())
    embed.add_field(name='`!1d<chiffre>`',
                    value='Lance un dé. Exemple: `!1d6`',
                    inline=False)
    embed.add_field(name='`!2d<chiffre> [<chiffre>]`',
                    value='Lance deux dés. Exemples: `!2d6` - `!2d6 8`',
                    inline=False)
    embed.add_field(name='`!randomChamp`',
                    value='Selectionne un champion de manière aléatoire sur son rôle principal.',
                    inline=False)
    return embed

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
        activity_string = 'sur {} servers.'.format(len(self.guilds))
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=activity_string))

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content.startswith('!help'):
            await message.channel.send(content=None, embed=create_help_embed())
            return

        if message.content.startswith('!1d'):
            msg_array =  message.content.split('d')
            input = msg_array[1]
            # on recupere l'id du channel dans lequel le message à été envoyé puis le channel lui même
                # channel_id = message.channel.id
                # channel = self.get_channel(channel_id)
            if input.find(' ') != -1:
                chiffre = input[0:input.find(' ')]
            else:
                chiffre = input
            if chiffre.isdigit():
                await message.add_reaction('\N{THUMBS UP SIGN}')
                await message.reply(":8ball:" + " : " + str(random.randrange(1,int(chiffre),1)), mention_author=True)
            else:
                await message.add_reaction('\N{THUMBS DOWN SIGN}')
                await message.reply("Something went wrong...", mention_author=True)
            return
        
        if message.content.startswith('!2d'):
            # on recupere l'id du channel dans lequel le message à été envoyé puis le channel lui même
                # channel_id = message.channel.id
                # channel = self.get_channel(channel_id)
            chiffre = None
            msg_input = message.content[3:]
            if msg_input.count(' ') > 0:
                chiffres = msg_input.split(' ')
            else:
                if msg_input.isdigit():
                    chiffre = msg_input
                else:
                    await message.reply("L'argument n'est pas un chiffre", mention_author=True)
            if chiffre is None:
                for i in range(2):
                    if chiffres[i].isdigit() != True:
                        await message.reply("L'argument n°"+str(i+1)+" n'est pas un chiffre", mention_author=True)
                await message.reply(":8ball: "+str(random.randrange(1,int(chiffres[0]),1))+", :8ball: "+str(random.randrange(1,int(chiffres[1]),1)), mention_author=True)
            else:
                await message.reply(":8ball: "+str(random.randrange(1,int(chiffre),1))+", :8ball: "+str(random.randrange(1,int(chiffre),1)), mention_author=True)
            return

        if message.content.startswith('!randomChamp'):
            retour = lolChamp.listeChampion[random.randrange(0,len(lolChamp.listeChampion),1)]
            await message.reply("Voici... Votre champion : " + retour.name + " en " + retour.role, mention_author=True)
            return

        if message.content.startswith('!checkBiboun'):
            biboun = watcher.summoner.by_name(my_region, 'Bìboun')
            biboun_ranked = watcher.league.by_summoner(my_region, biboun['id'])
            await message.reply("Bìboun : " + biboun_ranked["tier"] + " " + biboun_ranked["rank"] + " - " + biboun_ranked["leaguePoints"] + " LP", mention_author=True)
            return

        if message.content.startswith('!checkTobia'):
            tobia = watcher.summoner.by_name(my_region, 'Tobia')
            tobia_ranked = watcher.league.by_summoner(my_region, tobia['id'])
            await message.reply("Tobia : " + tobia_ranked["tier"] + " " + tobia_ranked["rank"] + " - " + tobia_ranked["leaguePoints"] + " LP", mention_author=True)
            return
        
        

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run('MTAxMjI5MjI0NzYzNjY4NDgyMA.GeE3F_.KRa9UdareJVjM1QOhY38Bl0UF9hW5-wCE2BHJs')