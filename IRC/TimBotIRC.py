#!/usr/bin/env python3
### from https://www.sevadus.tv/forums/index.php?/topic/774-simple-python-irc-bot/ ###
import re
import socket
import Commands
import json
# --------------------------------------------- Start Settings ----------------------------------------------------
HOST = "irc.twitch.tv"                          # Hostname of the IRC-Server in this case twitch's
PORT = 6667                                     # Default IRC-Port
CHAN = '#' + input('Enter username of twitch channel to connect to: (no "#" needed) ') # "#timmit99"                               # Channelname = #{Nickname}
NICK = "timbot99"                                # Nickname = Twitch username
PASS = "PRIVATE"   # www.twitchapps.com/tmi/ will help to retrieve the required authkey
botPrefix = '$'
commands = Commands.commandList
# --------------------------------------------- End Settings -------------------------------------------------------


# --------------------------------------------- Start Functions ----------------------------------------------------
def send_pong(msg):
    con.send(bytes('PONG %s\r\n' % msg, 'UTF-8'))
    
def send_message(chan, msg):
    con.send(bytes('PRIVMSG %s :%s\r\n' % (chan, msg), 'UTF-8'))


def send_nick(nick):
    con.send(bytes('NICK %s\r\n' % nick, 'UTF-8'))


def send_pass(password):
    con.send(bytes('PASS %s\r\n' % password, 'UTF-8'))


def join_channel(chan):
    con.send(bytes('JOIN %s\r\n' % chan, 'UTF-8'))


def part_channel(chan):
    con.send(bytes('PART %s\r\n' % chan, 'UTF-8'))
# --------------------------------------------- End Functions ------------------------------------------------------


# --------------------------------------------- Start Helper Functions ---------------------------------------------
def get_author(msg):
    result = ""
    for char in msg:
        if char == "!":
            break
        if char != ":":
            result += char
    return result


def get_message(msg):
    result = ""
    i = 3
    length = len(msg)
    while i < length:
        result += msg[i] + " "
        i += 1
    result = result.lstrip(':')
    return result
# --------------------------------------------- End Helper Functions -----------------------------------------------

con = socket.socket()
con.connect((HOST, PORT))

send_pass(PASS)
send_nick(NICK)
join_channel(CHAN)

data = ""

while True:
    try:
        data = data+con.recv(1024).decode('UTF-8')
        data_split = re.split(r"[~\r\n]+", data)
        data = data_split.pop()

        for line in data_split:
            line = line.rstrip()
            line = line.split(' ')

            if len(line) >= 1:
                if line[0] == 'PING':
                    send_pong(line[1])
                    
                if line[1] == 'PRIVMSG':
                    author = get_author(line[0])
                    message = get_message(line)
                    with open('USERS.json') as file:    # reading users database into 'people' object
                        people = json.load(file)
                        
                    if CHAN not in people: # If the channel is not in the database
                        people[CHAN] = {} # create channel in user database and write them to the file
                        with open('USERS.json', 'w') as outfile:
                            json.dump(people, outfile)
                        print('Added ' + CHAN + ' to database.')


                    if author not in people[CHAN]: # If the message author is not in the database
                        people[CHAN][author] = {'level' : 0,'blacklist' : False} # create author in user database and write them to the file
                        with open('USERS.json', 'w') as outfile:
                            json.dump(people, outfile)
                        print('Added ' + author + ' to database.')

                    
                    if author != NICK and len(message) >= 1:
                        userInput = message.split()
                        if userInput[0].startswith(botPrefix):
                            command = userInput[0][1:]
                            if command in commands:
                                print(people[CHAN][author]['level'])
                              
                                if command == 'commands':
                                    response = Commands.commands()
                                    
                                if command == "blacklist" and people[CHAN][author]['level'] >= 2:   # blacklist [view|add|remove] [_NAME_]
                                    response = Commands.blacklist(userInput)
                                    
                                if command == 'fish':
                                    response = Commands.fish(author,userInput)
                                
                                if command == 'driveby':
                                    client.send_message(message.channel,Commands.driveby(),'test', tts='True')

                                if command == 'dice':
                                    response = Commands.dice(userInput)

                                if command == 'countdown':
                                    response = Commands.countdown(userInput)
                                    
                                if command == 'islive':
                                    response = Commands.islive(userInput)
                                        
                                if command == 'twitch':
                                    response = Commands.twitch(userInput)

                                if command == 'throw':
                                    response = Commands.throw(userInput)

                                if command == 'hug':
                                    response = Commands.hug(userInput)

                                if command == 'feat':
                                    response = Commands.feat(userInput)
                                    
                                if command == 'joy':
                                    response = Commands.joy(userInput)
                                    
                                if command == 'kidder':
                                    response = Commands.kidder(userInput)

                                if command == '8ball':
                                    response = Commands.eightBall()
                                    
                                if command == 'lenny':
                                    response = Commands.lenny(userInput)
                                    
                                if command == 'hayden':
                                    response = Commands.hayden(userInput)

                                if command == "shane":
                                    response = Commands.shane()

                                if command == 'hello':
                                    response = Commands.hello(author,userInput)

                                if command == "var":
                                    response = Commands.var(userInput)

                                            
                                print(response)
                                print(CHAN)
                                send_message(CHAN,response)

                    print(author + ": " + ''.join(message))

    except socket.error:
        print("Socket died")

    except socket.timeout:
        print("Socket timeout")
