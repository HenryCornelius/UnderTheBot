# This example requires the 'message_content' privileged intent to function.
from distutils.log import info
from importlib.metadata import metadata
import discord
from riotwatcher import LolWatcher, ApiError
import random
import lolChamp
import compte
import my_embed
import datetime
import nacl

api_key = 'RGAPI-84d70ce7-80c8-44b7-b822-209762bc03ef'
watcher = LolWatcher(api_key)
my_region = 'euw1'

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
            await message.channel.send(content=None, embed=my_embed.create_help_embed())
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
            blue_golds = 0
            red_golds = 0
            for j in match_detail['info']['participants']:
                mate = watcher.summoner.by_id(my_region, j["summonerId"])
                mates_champ_mastery = watcher.champion_mastery.by_summoner_by_champion(my_region, j["summonerId"], j['championId'])
                # mate_last_game = datetime.datetime.fromtimestamp(mates_champ_mastery['lastPlayTime'] / 1000)
                if j['teamId'] == "100":
                    blue_golds = blue_golds + j['goldEarned']
                else:
                    red_golds = red_golds + j['goldEarned']
                mates_role = j['lane']
                if j['lane'] == "BOTTOM": 
                    mates_role = j['role']
                mates_name = str(mate['name']) + " - " + str(mates_role) 
                mates_champ = str(j['championName']) + " - " + str(j['kills']) + "/" + str(j['deaths']) + "/" + str(j['assists']) + " - " + str(j['totalMinionsKilled'] + j['neutralMinionsKilled']) + "cs"
                mates_mastery = "Points de maitrise : " + str(mates_champ_mastery['championPoints'])
                mates_rank = watcher.league.by_summoner(my_region, mate['id'])
                for k in range(len(mates_rank)):
                    if mates_rank[k]['queueType'] == "RANKED_SOLO_5x5":
                        rank_solo = mates_rank[k]
                        mates_solo_rank = rank_solo['tier'] + " " + rank_solo['rank'] + " - " + str(rank_solo['leaguePoints']) + " LP "
                mates.append([mates_name, mates_solo_rank, mates_champ, mates_mastery])
            
            if match_detail['info']['teams'][0]['win']:
                bluewin = "**WINNERS**  :green_circle:  " + blue_golds + ":moneybag:"
                redwin = "**LOOSERS**  :red_circle:  " + red_golds + ":moneybag:"
            else:
                bluewin = "**LOOSERS**  :red_circle:  " + blue_golds + ":moneybag:"
                redwin = "**WINNERS**  :green_circle:  " + red_golds + ":moneybag:"

            blueDragons = str(match_detail['info']['teams'][0]['objectives']['dragon']['kills'])
            blueBarons = str(match_detail['info']['teams'][0]['objectives']['baron']['kills'])
            blueHeralds =str(match_detail['info']['teams'][0]['objectives']['riftHerald']['kills'])
            blueObj = [blueDragons, blueBarons, blueHeralds]
            redDragons = str(match_detail['info']['teams'][1]['objectives']['dragon']['kills'])
            redBarons = str(match_detail['info']['teams'][1]['objectives']['baron']['kills'])
            redHeralds = str(match_detail['info']['teams'][1]['objectives']['riftHerald']['kills'])
            redObj = [redDragons, redBarons, redHeralds]
            
            await message.channel.send(content=None, embed=my_embed.create_mates_embed1(mates, bluewin, blueObj))
            
            await message.channel.send(content=None, embed=my_embed.create_mates_embed2(mates, redwin, redObj))
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