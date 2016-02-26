import discord
import random
import sys

import Commands
import json


email = 'timbot99@mail.com'
password = input('Enter the password for ' + email + ': ')
client = discord.Client()
client.login(email, password)

botPrefix = Commands.botPrefix; #   Pull botprefix from Commands file

if len(botPrefix) != 1:
    print(' The botPrefix must be only 1 character long!')
    sys.exit()


restrict = False # if True this will make all commands restricted to Moderators only
    
@client.event
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
 
@client.event

def on_message(message): # when a message is recieved it is stored in the message object
    if message.author == client.user:        #so the bot doesnt respond to itself
        return
    
    with open('USERS.json') as file:    # reading users database into 'people' object
        people = json.load(file)
    author = str(message.author).lower()
    
    if author not in people['users']: # If the message author is not in the database
        people['users'][author] = {'level' : 0,'blacklist' : False} # create author in user database and write them to the file
        with open('USERS.json', 'w') as outfile:
            json.dump(people, outfile)
        print('Added ' + author + ' to database.')


    if message.content.startswith(botPrefix): # If message start with the botPrefix 
        userInput = message.content.split()
        if userInput[0][1:] in Commands.commandList : # if it matches a command in the commandList
            
            
            if restrict == False or (restrict and people['users'][author]['level'] >= 2): # If commands are restricted to ONLY moderators
                
                if people['users'][author]['blacklist']:    # if the user that send the message is on the blacklist
                    if userInput[0][1:] in Commands.commandList:    #if the user also has entered a command
                        response = 'You are blacklisted'
                else:

                    if userInput[0] == botPrefix + 'commands':
                        response = Commands.commands()
                        
                    if userInput[0] == botPrefix + "blacklist" and people['users'][author]['level'] >= 2:   # blacklist [view|add|remove] [_NAME_]
                        response = Commands.blacklist(userInput)
                        
                    if userInput[0] == botPrefix + 'fish':
                        response = Commands.fish(author,userInput)
                    
                    if userInput[0] == botPrefix + 'driveby':
                        client.send_message(message.channel,Commands.driveby(),'test', tts='True')

                    if userInput[0] == botPrefix + 'dice':
                        response = Commands.dice(userInput)

                    if userInput[0] == botPrefix + 'countdown':
                        response = Commands.countdown(userInput)
                        
                    if userInput[0] == botPrefix + 'islive':
                        response = Commands.islive(userInput)
                            
                    if userInput[0] == botPrefix + 'twitch':
                        response = Commands.twitch(userInput)

                    if userInput[0] == botPrefix + 'throw':
                        response = Commands.throw(userInput)

                    if userInput[0] == botPrefix + 'hug':
                        response = Commands.hug(userInput)

                    if userInput[0] == botPrefix + 'feat':
                        response = Commands.feat(userInput)
                        
                    if userInput[0] == botPrefix + 'joy':
                        response = Commands.joy(userInput)
                        
                    if userInput[0] == botPrefix + 'kidder':
                        response = Commands.kidder(userInput)

                    if userInput[0] == botPrefix + '8ball':
                        response = Commands.eightBall()
                        
                    if userInput[0] == botPrefix + 'lenny':
                        response = Commands.lenny(userInput)
                        
                    if userInput[0] == botPrefix + 'hayden':
                        response = Commands.hayden(userInput)

                    if userInput[0] == botPrefix + "shane":
                        response = Commands.shane()

                    if userInput[0] == botPrefix + 'hello':
                        response = Commands.hello(author,userInput)

                    if userInput[0] == botPrefix + "var":
                        response = Commands.var(userInput)

            else:
                response = 'Commands have been restricted to Moderaters only.'
                
            client.send_message(message.channel,response)            
            
client.run()
