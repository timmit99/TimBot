import discord
import asyncio
import random
import sys

email = 'timbot99@mail.com'
password = input('Enter the password for ' + email + ': ')
client = discord.Client()
client.login(email, password)

commands = ['commands','id','8ball','lenny','hayden','hello','fish','driveby','dice','countdown','throw','hug','feat','joy'];
botPrefix = '$';

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
##    client.change_status(game='Minecraft',idle='false')
    client.send_typing(discord.Object(id='150437222640910336'))
##    print(str(channelNames))
##    print(str(roleNames))
##    print(str(client.servers[0].roles))
##    name = str(client.user.name)
##    name += ' is now connected to chat. Use \'' + botPrefix + '\' to prefix all the commands.'
##    client.send_message(discord.Object(id='150437222640910336'),name)


@client.event

def on_message(message):
    if message.author == client.user:
        return
    
    
    if message.content.startswith(botPrefix + 'commands'):
        response = 'Commands include: '
        for i in range(0,len(commands)-1):
            response = response + botPrefix + commands[i] + ', '
        response = response + 'and ' + botPrefix + commands[i+1]
        client.send_message(message.channel,response)
        
    if message.content.startswith(botPrefix + 'id'):
        try:
            if channelNames.index(str(message.content[len(botPrefix)+3:])) >= 0:
                response = 'The ID for "' + str(message.content[len(botPrefix)+3:]) + '" is: ' + str(channelIds[channelNames.index(str(message.content[len(botPrefix)+3:]))])
                client.send_message(message.channel,response)
                print(channelNames.index(str(message.content[len(botPrefix)+3:])))
        except ValueError:
            client.send_message(message.channel,'Channel is not found')
            
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
        
    if message.content.startswith(botPrefix + 'fish'):
        fish = ['Snapper','Grouper','Cod','Red Herring','Clown Fish']
        adjective = ['large',' ','slimy','disabled','still flopping']
        response = str(message.author) + ' slaps ' + str(message.content[len(botPrefix)+5:]) + ' with a ' + adjective[random.randint(0, len(adjective)-1)] + ' ' + fish[random.randint(0, len(fish)-1)]
        client.send_message(message.channel,response)

    if message.content.startswith(botPrefix + 'driveby'):
        client.send_message(message.channel,'testing','test', tts=True)

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
        number = message.content[len(botPrefix)+ 10:]
        number = number.partition(' ')[0]
        print(number)
        if number.isdigit() and int(number)<=100:    # Check if the number is only 0-9 and under 20
            #client.send_message(message.channel,'Valid number entered')
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
        

        
@client.event
def on_member_join(member):
    server = member.server
    fmt = 'Welcome {0.mention} to {1.name}!'
    client.send_message(server, fmt.format(member, server))

client.run()
