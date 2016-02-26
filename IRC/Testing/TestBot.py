#!/usr/bin/env python3

import re
import socket
import Commands

# --------------------------------------------- Start Settings ----------------------------------------------------
HOST = "irc.twitch.tv"                          # Hostname of the IRC-Server in this case twitch's
PORT = 6667                                     # Default IRC-Port
CHAN = "#timmit99"                               # Channelname = #{Nickname}
NICK = "timbot99"                                # Nickname = Twitch username
PASS = "PRIVATE"   # www.twitchapps.com/tmi/ will help to retrieve the required authkey
botPrefix = '$'
commands = {'hello','test'}
# --------------------------------------------- End Settings -------------------------------------------------------


# --------------------------------------------- Start Functions ----------------------------------------------------

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
def get_sender(msg):
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
            line = line.split()

            if len(line) >= 1:
                if line[1] == 'PRIVMSG':
                    sender = get_sender(line[0])
                    message = get_message(line)
                    if sender != NICK and len(message) >= 1:
                        message = message.split()
                        if message[0].startswith(botPrefix):
                            command = message[0][1:]
                            if command in commands:
                                if command == 'hello':
                                    response = Commands.hello(sender,message)
                                if command == 'test':
                                    response = "test response"
                                

                                send_message(CHAN,response)

                    print(sender + ": " + ' '.join(message))

    except socket.error:
        print("Socket died")

    except socket.timeout:
        print("Socket timeout")
