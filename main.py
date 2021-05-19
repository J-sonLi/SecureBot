import requests
import discord
import os

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  if message.embeds:
    # Prevents infinite loops of message
    if message.author.bot:
        return
    else:
      url = 'https://www.virustotal.com/vtapi/v2/url/report'
      params = {
        'apikey': os.environ.get('VIRUS_TOTAL_API'),
        'resource': message.content
        }
      response = requests.get(url=url, params=params)
      check_positive = response.json()
      if check_positive['positives'] <= 0:
        check_mark = '\N{White Heavy Check Mark}'
        await message.add_reaction(check_mark)
      elif check_positive['positives'] <= 4:
        warning_mark = '\N{Double Exclamation Mark}'
        await message.add_reaction(warning_mark)
      else:
          error_mark = '\N{Cross Mark}'
          await message.add_reaction(error_mark)
            
client.run(os.environ.get('TOKEN'))
