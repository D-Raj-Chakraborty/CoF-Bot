import discord
import os
import requests
import json
import random  #random module used for random choosing
from replit import db
from keep_alive import alive_always

#creating a instance of cient
client = discord.Client()

sad_words = ["sad","depressed","unhappy","angry","miserable","depressing"]

starter_encouragements = [
  "Cheer up!",
  "Hang in there.",
  "You are a great person / bot!"
]

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)

  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def update_encouragements(encourageing_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encourageing_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encourageing_message]


def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] =  encouragements


@client.event
async def on_ready():
    print('we have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
  
    msg = message.content
  
    if message.content.startswith('$inspire'):
      quote = get_quote()
      await message.channel.send(quote)

    if db["responding"]:
      options = starter_encouragements
      if "encouragements" in db.keys():
         options.extend(db["encouragements"])
        
      if any(word in msg for word in sad_words):
        await message.channel.send(random.choice(options))

      
    if msg.startswith("$new"):
      encourageing_message = msg.split("$new ",1)[1]
      update_encouragements(encourageing_message)
      await message.channel.send("New encouraging  Message Added..") 

    if msg.startswith("$del"):
      encouragements = []
      if "encouragements" in db.keys():
        index = int(msg.split("$del",1)[1])
        delete_encouragement(index)
        encouragements = db["encouragements"]
      await message.channel.send(encouragements) 


    if msg.startswith("$list"):
      encouragements = []
      if "encouragements" in db.keys():
        encouragements = db["encouragements"]
      await message.channel.send(encouragements)
      
    if msg.startswith("$responding"):
      value = msg.split("$responding ",1)[1]
       
      if value.lower() == "true":
        db["responding"] = True
        await message.channel.send("Responding is on.")
      else:
        db["responding"] = False
        await message.channel.send("Responding is off.")


alive_always()
client.run(os.getenv('TOKEN'))
my_secret = os.environ['TOKEN']
