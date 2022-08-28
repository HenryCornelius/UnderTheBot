import discord

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
                        description=blueObj[0]+" Drake / "+blueObj[1]+" Nash / "+blueObj[2]+" Herald", colour=discord.Colour.blue())
    for i in range(5):
        embed1.add_field(name=mates[i].name,
                    value=mates[i].solo_rank,
                    inline=True)
        embed1.add_field(name=mates[i].champ,
                    value=mates[i].champ_mastery,
                    inline=True)
        embed1.add_field(name=mates[i].gold,
	    		    value=mates[i].damage,
	    		    inline= True)
    return embed1
def create_mates_embed2(mates, redwin, redObj):
    embed2 = discord.Embed(title=redwin,
                        description=redObj[0]+" Drake / "+redObj[1]+" Nash / "+redObj[2]+" Herald", colour=discord.Colour.red())
    
    for i in range(5):
        embed2.add_field(name=mates[i+5].name,
                    value=mates[i+5].solo_rank,
                    inline=True)
        embed2.add_field(name=mates[i+5].champ,
                    value=mates[i+5].champ_mastery,
                    inline=True)
        embed2.add_field(name=mates[i+5].gold,
	    		    value=mates[i+5].damage,
	    		    inline= True)
    return embed2