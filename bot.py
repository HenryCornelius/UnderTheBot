# This example requires the 'message_content' privileged intent to function.
from distutils.log import info
from importlib.metadata import metadata
import discord
from riotwatcher import LolWatcher, ApiError
import random
import lolChamp
import compte
import nacl

api_key = 'RGAPI-84d70ce7-80c8-44b7-b822-209762bc03ef'
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

def create_mates_embed1(mates, bluewin, blueObj):
    embed1 = discord.Embed(title=bluewin,
                        description='', colour=discord.Colour.blue())
    embed1.add_field(name=mates[0][0],
                    value=mates[0][1],
                    inline=False)
    embed1.add_field(name=mates[1][0],
                    value=mates[1][1],
                    inline=False)
    embed1.add_field(name=mates[2][0],
                    value=mates[2][1],
                    inline=False)
    embed1.add_field(name=mates[3][0],
                    value=mates[3][1],
                    inline=False)
    embed1.add_field(name=mates[4][0],
                    value=mates[4][1],
                    inline=False)
    embed1.add_field(name="Objectifs",
                    value=blueObj[0]+" Drake / "+blueObj[1]+" Nash / "+blueObj[2]+" Herald",
                    inline=False)
    return embed1
def create_mates_embed2(mates, redwin, redObj):
    embed2 = discord.Embed(title=redwin,
                        description='', colour=discord.Colour.red())
    embed2.add_field(name=mates[5][0],
                    value=mates[5][1],
                    inline=False)
    embed2.add_field(name=mates[6][0],
                    value=mates[6][1],
                    inline=False)
    embed2.add_field(name=mates[7][0],
                    value=mates[7][1],
                    inline=False)
    embed2.add_field(name=mates[8][0],
                    value=mates[8][1],
                    inline=False)
    embed2.add_field(name=mates[9][0],
                    value=mates[9][1],
                    inline=False)
    embed2.add_field(name="Objectifs",
                    value=redObj[0]+" Drake / "+redObj[1]+" Nash / "+redObj[2]+" Herald",
                    inline=True)
    return embed2

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
        ####################################################################################################################
        #                                                                                                                  #
        #                                          Commande !Help                                                          #
        #                                                                                                                  #
        ####################################################################################################################
        if message.content.startswith('!help'):
            await message.channel.send(content=None, embed=create_help_embed())
            return


        ####################################################################################################################
        #                                                                                                                  #
        #                                          Commande !1d                                                            #
        #                                                                                                                  #
        ####################################################################################################################
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


        ####################################################################################################################
        #                                                                                                                  #
        #                                          Commande !2d                                                            #
        #                                                                                                                  #
        ####################################################################################################################
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


        ####################################################################################################################
        #                                                                                                                  #
        #                                          Commande !randomChamp                                                   #
        #                                                                                                                  #
        ####################################################################################################################
        if message.content.startswith('!randomChamp') or message.content.startswith('!randomchamp'):
            retour = lolChamp.listeChampion[random.randrange(0,len(lolChamp.listeChampion),1)]
            await message.reply("Voici... Votre champion : " + retour.name + " en " + retour.role, mention_author=True)
            return


        ####################################################################################################################
        #                                                                                                                  #
        #                                          Commande !checkBiboun                                                   #
        #                                                                                                                  #
        ####################################################################################################################
        if message.content.startswith('!checkBiboun') or message.content.startswith('!checkbiboun'):
            biboun = watcher.summoner.by_name(my_region, 'Bìboun')
            biboun_ranked = watcher.league.by_summoner(my_region, biboun['id'])
            print(biboun_ranked)
            await message.reply("Bìboun : " + biboun_ranked[0]['tier'] + " " + biboun_ranked[0]['rank'] + " - " + str(biboun_ranked[0]['leaguePoints']) + " LP", mention_author=True)
            return


        ####################################################################################################################
        #                                                                                                                  #
        #                                          Commande !checkRank                                                     #
        #                                                                                                                  #
        ####################################################################################################################
        if message.content.startswith('!checkRank') or message.content.startswith('!checkrank'):
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
        

        ####################################################################################################################
        #                                                                                                                  #
        #                                          Commande !checkMate                                                     #
        #                                                                                                                  #
        ####################################################################################################################
        if message.content.startswith('!checkMate') or message.content.startswith('!checkmate'):
            msg_input = message.content[1:]
            if msg_input.count(' ') > 0:
                summonername = msg_input.split(' ')[1]
            else:
                summonername = ""
                print(message.author.name + " + " + compte.listeMembre[0].discordname)
                for i in range(len(compte.listeMembre)):
                    if message.author.name == compte.listeMembre[i].discordname:
                        summonername = compte.listeMembre[i].lolname
                if summonername == "": 
                    await message.reply("Le nom d'invocateur n'est pas configuré", mention_author=True) 
                    return
            try:
                summoner = watcher.summoner.by_name(my_region, summonername)
            except ApiError:
                await message.reply("Le nom d'invocateur n'est pas bon", mention_author=True) 
                return
            my_matches = watcher.match.matchlist_by_puuid(my_region, summoner['puuid'])
            # fetch last match detail
            match_detail = watcher.match.by_id(my_region, my_matches[0])
            print(match_detail)
            mates = []
            count = 0
            for j in match_detail['metadata']['participants']:
                mates_name = str(watcher.summoner.by_puuid(my_region, j)['name']) + " - " + str(match_detail['info']['participants'][count]['championName'])
                mates_rank = watcher.league.by_summoner(my_region, watcher.summoner.by_puuid(my_region, j)['id'])
                for k in range(len(mates_rank)):
                    if mates_rank[k]['queueType'] == "RANKED_SOLO_5x5":
                        rank_solo = mates_rank[k]
                        mates_solo_rank = rank_solo['tier'] + " " + rank_solo['rank'] + " - " + str(rank_solo['leaguePoints']) + " LP "
                mates.append([mates_name, mates_solo_rank])
                count= count + 1
            
            if match_detail['info']['teams'][0]['win']:
                bluewin = "**WINNERS**  :green_circle:"
                redwin = "**LOOSERS**  :red_circle:"
            else:
                bluewin = "**LOOSERS**  :red_circle:"
                redwin = "**WINNERS**  :green_circle:"

            blueDragons = match_detail['info']['teams'][0]['objectives']['dragon']['kills']
            blueBarons = match_detail['info']['teams'][0]['objectives']['baron']['kills']
            blueHeralds = match_detail['info']['teams'][0]['objectives']['riftHerald']['kills']
            blueObj = [blueDragons, blueBarons, blueHeralds]
            redDragons = match_detail['info']['teams'][1]['objectives']['dragon']['kills']
            redBarons = match_detail['info']['teams'][1]['objectives']['baron']['kills']
            redHeralds = match_detail['info']['teams'][1]['objectives']['riftHerald']['kills']
            redObj = [redDragons, redBarons, redHeralds]
            
            await message.channel.send(content=None, embed=create_mates_embed1(mates, bluewin, blueObj))
            
            await message.channel.send(content=None, embed=create_mates_embed2(mates, redwin, redObj))
            return
            


        ####################################################################################################################
        #                                                                                                                  #
        #                                          Commande !test                                                          #
        #                                                                                                                  #
        ####################################################################################################################
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
                ranks['solo'] = "Non classé"
                ranks['flex'] = "Non classé"
                ranks['double'] = "Non classé"
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


        ####################################################################################################################
        #                                                                                                                  #
        #                                      Commande !join and !leave                                                   #
        #                                                                                                                  #
        ####################################################################################################################
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