import requests
import json
import time
from discord_webhook import DiscordWebhook, DiscordEmbed
from bs4 import BeautifulSoup


print("\n------------------------------------------------------------------------------\nThis monitor will work with any CSGO item listed on the Steam Community Market\n------------------------------------------------------------------------------\n")

# gather user specifications
item = input("Enter the name of the item to monitor: ")
print('\n')
webHook = input("Paste your discord webhook here: ")
print('\n')
listing = input("Paste the link to the csgo item here: ")
print('\n')
monitorDelay = input("Enter monitor delay(seconds): ")
print('\n')
listing = listing.split("/")
listing = listing[-1]
URL = ("https://steamcommunity.com/market/priceoverview/?appid=730&currency=1&market_hash_name="+listing)

# uncomment and add block-comment above to hardcode instead of input
'''
item = "AK-47 | Redline"
webHook = "ENTER_WEBHOOK_HERE"
listing = "https://steamcommunity.com/market/listings/730/AK-47%20%7C%20Redline%20%28Field-Tested%29"
monitorDelay = "3000"
'''

# gets item image
r = requests.get("https://steamcommunity.com/market/listings/730/"+listing)
soup = BeautifulSoup(r.content, 'html.parser')
img = soup.findAll('img')
itemImage = ((img[7])['src'])

print("Starting Monitor...")

# checks current price of item
def priceCheck():
    r = requests.get(URL)
    jsonText = json.loads(r.text)
    price = (jsonText["lowest_price"])
    print("Current Price: ", price)
    sendNotif(price)

# sends notification to discord webhook
def sendNotif(price):
    webhook = DiscordWebhook(url=webHook)
    embed = DiscordEmbed(title=item, url="https://steamcommunity.com/market/listings/730/"+listing, color=0x5529d6)
    embed.set_thumbnail(url=itemImage)
    embed.add_embed_field(name="Current Price:", value=price, inline=False)
    embed.set_footer(text="Made by bard#1704")
    webhook.add_embed(embed)
    response = webhook.execute()
    time.sleep(int(monitorDelay))

while True:
    priceCheck()