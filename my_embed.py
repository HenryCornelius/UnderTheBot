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
                        description='', colour=discord.Colour.blue())
    embed1.add_field(name=mates[0][0],
                    value=mates[0][1],
                    inline=True)
    embed1.add_field(name=mates[0][2],
                    value="test",
                    inline=True)
    embed1.add_field(name=mates[1][0],
                    value=mates[1][1],
                    inline=True)
    embed1.add_field(name=mates[1][2],
                    value="test",
                    inline=True)
    embed1.add_field(name=mates[2][0],
                    value=mates[2][1],
                    inline=True)
    embed1.add_field(name=mates[2][2],
                    value="test",
                    inline=True)
    embed1.add_field(name=mates[3][0],
                    value=mates[3][1],
                    inline=True)
    embed1.add_field(name=mates[3][2],
                    value="test",
                    inline=True)
    embed1.add_field(name=mates[4][0],
                    value=mates[4][1],
                    inline=True)
    embed1.add_field(name=mates[4][2],
                    value="test",
                    inline=True)
    embed1.set_footer(text=blueObj[0]+" Drake / "+blueObj[1]+" Nash / "+blueObj[2]+" Herald")
    return embed1
def create_mates_embed2(mates, redwin, redObj):
    embed2 = discord.Embed(title=redwin,
                        description='', colour=discord.Colour.red())
    embed2.add_field(name=mates[5][0],
                    value=mates[5][1],
                    inline=True)
    embed2.add_field(name=mates[5][2],
                    value="test",
                    inline=True)
    embed2.add_field(name=mates[6][0],
                    value=mates[6][1],
                    inline=False)
    embed2.add_field(name=mates[6][2],
                    value="test",
                    inline=True)
    embed2.add_field(name=mates[7][0],
                    value=mates[7][1],
                    inline=True)
    embed2.add_field(name=mates[7][2],
                    value="test",
                    inline=True)
    embed2.add_field(name=mates[8][0],
                    value=mates[8][1],
                    inline=True)
    embed2.add_field(name=mates[8][2],
                    value="test",
                    inline=True)
    embed2.add_field(name=mates[9][0],
                    value=mates[9][1],
                    inline=True)
    embed2.add_field(name=mates[9][2],
                    value="test",
                    inline=True)
    embed2.set_footer(text=redObj[0]+" Drake / "+redObj[1]+" Nash / "+redObj[2]+" Herald")
    return embed2