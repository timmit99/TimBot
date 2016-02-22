import discord
import asyncio
import random
import sys
from urllib.request import urlopen
from urllib.error import URLError
import json


email = 'timbot99@mail.com'
password = input('Enter the password for ' + email + ': ')
client = discord.Client()
client.login(email, password)

commands = ['commands','id','8ball','lenny','hayden','hello','fish','driveby','dice','countdown','throw','hug','feat','joy','kidder','islive','twitch'];
botPrefix = '$';
Moderators = ['Timmit99']
mods = [x.lower() for x in Moderators]     # making all the names lowercase to make it easier to compare


if len(botPrefix) != 1:
    print(' The botPrefix must be only 1 character long!')
    sys.exit()

serverNames = [];
channelNames = [];
channelIds = [];
roleNames = [];
    
@client.event
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    for server in client.servers:
        serverNames.append(server.name)
        for role in server.roles:
            roleNames.append(role.name)
        for channel in server.channels:
            channelNames.append(channel.name)
            channelIds.append(channel.id)
    client.send_typing(discord.Object(id='150437222640910336'))



@client.event

def on_message(message):
    #blacklist = open('blacklist.txt', 'r+')
    listOfNames = open('blacklist.txt', 'r+').readlines()
    
    if message.author == client.user:        #so the bot doesnt respond to itself4
        return
    
    if str(message.author).lower() + "\n" in listOfNames:    # if the user that send the message is on the blacklist
        if message.content.split()[0][1:] in commands:    #if the user also has entered a command
            client.send_message(message.channel,'You are blacklisted')
    else:

        if message.content.startswith(botPrefix + 'commands'):
            response = 'Commands include: '
            for i in range(0,len(commands)-1):
                response = response + botPrefix + commands[i] + ', '
            response = response + 'and ' + botPrefix + commands[i+1]
            client.send_message(message.channel,response)

        if message.content.startswith(botPrefix + 'blacklist'):
            if str(message.author).lower() in mods:    # if the user has correct (mod) permissions
                userInput = message.content.split()
                userInput = userInput[1:]
                if len(userInput) > 0:
                    blacklist = open('blacklist.txt', 'r+')
                    if userInput[0] == 'view':
                        response = 'Blacklist: \n'
                        for line in blacklist:
                            response += line
                        client.send_message(message.channel,response)

                    elif userInput[0] == 'add':
                        location = blacklist.read().find(userInput[1])
                        if location >= 0: # if name is on the blacklist
                            client.send_message(message.channel,'User is already on the blacklist')

                        else:
                            blacklist.close()
                            open('blacklist.txt','a').write(userInput[1].lower() + '\n')
                            client.send_message(message.channel,'User added to blacklist')
                        
                        
                    elif userInput[0] == 'remove':
                        lines = blacklist.readlines()
                        blacklist.close()
                        blacklist = open("blacklist.txt","w")
                        for line in lines:
                            if line != userInput[1].lower()+"\n":
                                blacklist.write(line)
                        blacklist.close()
                        client.send_message(message.channel,'User removed from blacklist')
                    
                else:
                    client.send_message(message.channel,'Invalid entry. Use "view","add", ore "remove"')
            else:
                client.send_message(message.channel,'You are not a mod; You do not have permissions to use this command')
            
        if message.content.startswith(botPrefix + 'id'):
            try:
                if channelNames.index(str(message.content[len(botPrefix)+3:])) >= 0:
                    response = 'The ID for "' + str(message.content[len(botPrefix)+3:]) + '" is: ' + str(channelIds[channelNames.index(str(message.content[len(botPrefix)+3:]))])
                    client.send_message(message.channel,response)
                    print(channelNames.index(str(message.content[len(botPrefix)+3:])))
            except ValueError:
                client.send_message(message.channel,'Channel is not found')
                

            
        if message.content.startswith(botPrefix + 'fish'):
            fish = ['Snapper','Grouper','Cod','Red Herring','Clown Fish']
            adjective = ['large',' ','slimy','disabled','still flopping']
            response = str(message.author) + ' slaps ' + str(message.content[len(botPrefix)+5:]) + ' with a ' + adjective[random.randint(0, len(adjective)-1)] + ' ' + fish[random.randint(0, len(fish)-1)]
            client.send_message(message.channel,response)

        if message.content.startswith(botPrefix + 'driveby'):
            client.send_message(message.channel,'@@@@@@@@@@@@@@@@@@@@@@@@@@@@ ded','test', tts='True')

        if message.content.startswith(botPrefix + 'dice'):
            userInput = str(message.content)[len(botPrefix)+5:]
            firstNumber = userInput.split('d',1)[0]  #first number        
            secondNumber = userInput.split('d',1)[1]  #second number
            print(firstNumber + ' and ' + secondNumber)
            if firstNumber.isdigit() and secondNumber.isdigit():
                client.send_message(message.channel,'Rolling ' + firstNumber + ' of D'  + secondNumber + ' dice')
                response = 'Dice Rolls: '
                for i in range (0,int(firstNumber)-1):
                    response += str(random.randint(1,int(secondNumber))) + ', '
                response += str(random.randint(1,int(secondNumber)))
                client.send_message(message.channel,response)
            else:
                client.send_message(message.channel,'Invalid entry. Must be format \"' + botPrefix +'dice ###d###\"')          
            
        if message.content.startswith(botPrefix + 'countdown'):
            number = message.content.split()[1]
            if number.isdigit() and int(number)<=100:    # Check if the number is only 0-9 and under 20
                number = int(number)
                response = 'Countdown: ' + str(number)
                for i in range(0,number):
                    number -= 1
                    response += ', ' + str(number)
                response += ' BLAST OFF!'
                client.send_message(message.channel,response)
                    
            elif number.isdigit():
                client.send_message(message.channel,'Number entered is over 100, to big!')
            else:
                client.send_message(message.channel,'Invalid number entered')
                return
            
        if message.content.startswith(botPrefix + 'islive'):
            userInput = message.content.split()
            names = userInput[1:]
            index = 0
            for name in names:
                url = 'https://api.twitch.tv/kraken/streams/' + name
                try:
                    info = json.loads(urlopen(url, timeout = 15).read().decode('utf-8'))
                    if info['stream'] == None:
                        response = 'No, ' + str(names[index]) + ' is offline.'
                        client.send_message(message.channel, response)
                    else:
                        response = 'Yes, ' + str(names[index]) + ' is streaming "' + str(info['stream']['game']) + '" to ' + str(info['stream']['viewers']) + ' viewers.'
                        client.send_message(message.channel, response)
                except URLError as e:
                    if e.reason == 'Not Found' or e.reason == 'Unprocessable Entity':
                        response = 'I\'m sorry, ' + str(names[index]) + ' could not be found.'
                        client.send_message(message.channel, response)
                    else:
                        response = 'There was an error with your request'
                        client.send_message(message.channel, response)
                index += 1

        if message.content.startswith(botPrefix + 'throw'):
            response = '(╯°□°）╯彡 ' + str(message.content[len(botPrefix)+6:])
            client.send_message(message.channel,response)

        if message.content.startswith(botPrefix + 'hug'):
            response = '(>ಠ_ಠ)>  ' + str(message.content[len(botPrefix)+4:])
            client.send_message(message.channel,response)

        if message.content.startswith(botPrefix + 'feat'):
            response = "That's a feat, " + str(message.content[len(botPrefix)+5:]) + ", and I don't mean an arm." 
            client.send_message(message.channel,response)

        if message.content.startswith(botPrefix + 'joy'):
            response = "WHY DOESN'T " + str(message.content[len(botPrefix)+4:]).upper() + " RESONATE WITH JOY!?!?" 
            client.send_message(message.channel,response)
            
        if message.content.startswith(botPrefix + 'kidder'):
            response = "You were always sucha kidder, " + str(message.content[len(botPrefix)+7:]) 
            client.send_message(message.channel,response)

        if message.content.startswith(botPrefix + '8ball'):
            answers =  ['Yes!','No','It is a possibility','answer seems cloudy.','ask again later','it is unknown','never in a million years']
            client.send_message(message.channel,answers[random.randint(0, len(answers)-1)])
            
        if message.content.startswith(botPrefix + 'lenny'):
            response = '( ͡° ͜ʖ ͡°) ' + str(message.content[len(botPrefix)+6:])
            client.send_message(message.channel,response)
            
        if message.content.startswith(botPrefix + 'hayden'):
            response = 'ಠ_ಠ ' + str(message.content[len(botPrefix)+7:])
            client.send_message(message.channel,response)

        if message.content.startswith(botPrefix + 'hello'):
            if len(message.content) > len(botPrefix) + 5:
                response = 'Hello ' + str(message.content[len(botPrefix)+6:])
            else:
                response = 'Hello ' + str(message.author)
            client.send_message(message.channel,response)

        if message.content.startswith(botPrefix + 'twitch'):
            names = message.content.split()[1:]
            if len(names) == 0:
                response = 'Enter one or more names after ' + botPrefix + 'twitch in order to get the link(s)'
            elif len(names) == 1:
                response = 'http://twitch.tv/' + names[0]
            else:
                response = 'http://www.multitwitch.tv'
                for name in names:
                    response += '/' + name
            client.send_message(message.channel,response)
            
                
            
client.run()
