import opensea
import discord
import config
import time
import matplotlib.pyplot as plt
from datetime import datetime
from discord.ext import commands

client = commands.Bot(command_prefix = '?')
api = opensea.OpenseaAPI(apikey=config.keys['OPENSEA_API_KEY'])

@client.event
async def on_ready():
    print("Online")

@client.command()
async def nfts(ctx, wallet):
    result = api.assets(owner=wallet, export_file_name="asset.json")
    embed = discord.Embed(
        title="{}'s NFTs".format(ctx.author.display_name),
        url="https://opensea.io/{}".format(wallet),
        description="Here is a list of your NFTs!",
        color=discord.Color.blue())
    
    for i in result['assets']:
        try:
            collection = api.collection(collection_slug=i['collection']['slug'])['collection']
            embed.add_field(name=i['name'], value="Collection Floor Price: {} ETH".format(collection['stats']['floor_price']))
        except:
            embed.add_field(name='No Name Found', value="Collection Floor Price: {} ETH".format(collection['stats']['floor_price']))

    await ctx.send(embed=embed)
 
@client.command()
async def combinedfloor(ctx, wallet):

    listComplete = False
    offset = 0
    floorPrice = 0
    collectionList = {}
    totalETHPerCollection = {}
    username = None
    while listComplete == False:
        result = api.assets(owner=wallet, offset=offset)
        
        if username is None:
            username = result['assets'][0]['owner']['user']['username']

        for i in result['assets']:
            if i['collection']['slug'] in collectionList:
                floorPrice += collectionList[i['collection']['slug']]
                totalETHPerCollection[i['collection']['slug']] += collectionList[i['collection']['slug']]
            else:
                time.sleep(.5)     
                collection = api.collection(collection_slug=i['collection']['slug'])['collection']
                try:
                    floorPrice += collection['stats']['floor_price']
                    collectionList[i['collection']['slug']] = collection['stats']['floor_price']
                    totalETHPerCollection[i['collection']['slug']] = collection['stats']['floor_price']
                except:
                    floorPrice += 0
                    collectionList[i['collection']['slug']] = 0
        if len(result['assets']) < 50:
            listComplete = True
        else:
            offset += 50
        

    
    bar_chart = generate_bar_chart(totalETHPerCollection, username)

    embed = discord.Embed(
        title="Combined Floor Price of {}'s NFTs".format(username),
        url="https://opensea.io/{}".format(wallet),
        description="Combined Floor Price: {} ETH".format(round(floorPrice, 4)),
        color=discord.Color.blue())

    file = discord.File(bar_chart, filename="image.png")
    embed.set_image(url="attachment://image.png")

    await ctx.send(file=file, embed=embed)
    
def generate_bar_chart(collection, username):
    plt.clf()
    plt.bar(collection.keys(), collection.values())
    plt.title("{}'s Total ETH Floor Value by Collection".format(username))
    plt.xticks(
        rotation=45, 
        horizontalalignment='right',
        fontweight='light',
        fontsize='small'  
)   
    chart_name = "chart_{}.png".format(username)
    plt.savefig(chart_name, bbox_inches="tight")
    
    return chart_name
    
    
client.run(config.keys['DISCORD_BOT_KEY'])
