# This example requires the 'message_content' privileged intent to function.
import discord
from riotwatcher import LolWatcher, ApiError
import random
import lolChamp
import nacl

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
    embed.add_field(name='`!checkRank <summoner name> [<type ranked>]`',
                    value='Vérifie le rang du pseudo entré. Exemples: `!checkRank Tobia` - `!checkRank Tobia TFT`',
                    inline=False)
    return embed

class MyClient(discord.Client):

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
        if len(self.guilds) == 1:
            activity_string = 'sur {} serveur.'.format(len(self.guilds))
        else:
            activity_string = 'sur {} serveurs.'.format(len(self.guilds))
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
            print(biboun_ranked)
            await message.reply("Bìboun : " + biboun_ranked[0]['tier'] + " " + biboun_ranked[0]['rank'] + " - " + str(biboun_ranked[0]['leaguePoints']) + " LP", mention_author=True)
            return

        if message.content.startswith('!checkTobia'):
            tobia = watcher.summoner.by_name(my_region, 'Tobia')
            tobia_ranked = watcher.league.by_summoner(my_region, tobia['id'])
            await message.reply("Tobia : " + tobia_ranked['tier'] + " " + tobia_ranked['rank'] + " - " + str(tobia_ranked['leaguePoints']) + " LP", mention_author=True)
            return

        if message.content.startswith('!checkRank'):
            msg_input = message.content[1:]
            if msg_input.count(' ') > 0:
                name = msg_input.split(' ')[1]
                summoner = watcher.summoner.by_name(my_region, name)
                if summoner is not None: 
                    summoner_rank = watcher.league.by_summoner(my_region, summoner['id'])
                    print(summoner_rank)
                    queueType = "RANKED_SOLO_5x5"
                    if msg_input.count(' ') > 1:
                        if msg_input.split(' ')[2] == "SOLO" or msg_input.split(' ')[2] == "Solo" or msg_input.split(' ')[2] == "solo":
                            queueType = "RANKED_SOLO_5x5"
                        else:
                            if msg_input.split(' ')[2] == "FLEX" or msg_input.split(' ')[2] == "Flex" or msg_input.split(' ')[2] == "flex":
                                queueType = "RANKED_FLEX_SR"
                            else:
                                if msg_input.split(' ')[2] == "TFT" or msg_input.split(' ')[2] == "Tft" or msg_input.split(' ')[2] == "tft":
                                    queueType = "RANKED_TFT_DOUBLE_UP"
                                else:
                                    await message.reply("Précise 'SOLO', 'TFT' ou 'FLEX' connard !", mention_author=True)
                                    return
                    for i in range(len(summoner_rank)):
                            if summoner_rank[i]['queueType'] == queueType:
                                rank_solo = summoner_rank[i]
                                await message.reply(name + " : " + rank_solo['tier'] + " " + rank_solo['rank'] + " - " + str(rank_solo['leaguePoints']) + " LP ", mention_author=True)
                                return
                            else:
                                await message.reply("Pas de classement dispo dans cette file !", mention_author=True)
                else:
                    await message.reply("Le nom d'invocateur est incorrect", mention_author=True) 
                    return

            else:
                await message.reply("Il manque le nom d'invocateur", mention_author=True)
                return

        if message.content.startswith('!test'):
            msg_input = message.content[1:]
            if msg_input.count(' ') > 0:
                argument = msg_input.split(' ')[1]
                summoner = watcher.summoner.by_name(my_region, argument)
                summoner_rank = watcher.league.by_summoner(my_region, summoner['id'])
                version = watcher.data_dragon.versions_for_region(my_region)['v']
                embed = discord.Embed(title='**'+summoner['name']+'**',description="Informations concernant le joueur "+ summoner['name'] +". Cliquez sur le nom d'invocateur ci-dessus afin d'accéder à ses données sur op.gg", url="https://euw.op.gg/summoners/euw/"+summoner['name'],colour=discord.Colour.blue() )
                url = "https://ddragon.leagueoflegends.com/cdn/" + str(version) + "/img/profileicon/" + str(summoner['profileIconId']) + ".png"
                embed.set_thumbnail(url = url)
                ranks = {}
                for i in range(len(summoner_rank)):
                    if summoner_rank[i]['queueType'] == 'RANKED_SOLO_5x5':
                        rank = summoner_rank[i]
                        ranks['solo'] = rank['tier'] + " " + rank['rank'] + " - " + str(rank['leaguePoints']) + " LP "
                    if summoner_rank[i]['queueType'] == 'RANKED_FLEX_SR':
                        rank = summoner_rank[i]
                        ranks['flex'] = rank['tier'] + " " + rank['rank'] + " - " + str(rank['leaguePoints']) + " LP "
                    if summoner_rank[i]['queueType'] == 'RANKED_TFT_DOUBLE_UP':
                        rank = summoner_rank[i]
                        ranks['double'] = rank['tier'] + " " + rank['rank'] + " - " + str(rank['leaguePoints']) + " LP "
                    
                    
                embed.add_field(name='Solo/duo',
                    value= ranks['solo'],
                    inline=False)
                embed.add_field(name='Flex',
                    value= ranks['flex'],
                    inline=False)
                embed.add_field(name='TFT Double Up',
                    value= ranks['double'],
                    inline=False)
                await message.channel.send(content=None, embed=embed)
                react = '✅'
                await message.add_reaction(react)
            else:
                await message.reply("Il manque le nom d'invocateur", mention_author=True)
                return

        if message.content.startswith('!join'):
            destination = message.author.voice.channel
            await destination.connect()
            return
        if message.content.startswith('!leave'):
            await message.guild.voice_client.disconnect()
            return
intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run('MTAxMjI5MjI0NzYzNjY4NDgyMA.GeE3F_.KRa9UdareJVjM1QOhY38Bl0UF9hW5-wCE2BHJs')