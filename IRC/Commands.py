import random
import json
import re
from urllib.request import urlopen
from urllib.error import URLError

commandList = ['commands','8ball','lenny','hayden','hello','fish','driveby','shane','dice','countdown','throw','hug','feat','joy','kidder','islive','twitch','var','blacklist'];

dicePattern = re.compile('(\d*)[d|D](\d)+$') # '[1-9](\d*)d[\d+'

botPrefix = '$'

def commands():
        response = 'Commands include: ' + botPrefix + (', '+botPrefix).join(commandList)
        return response

def hug(userInput):
        response = '(>ಠ_ಠ)>  ' + ' '.join(userInput[1:])
        return response

def lenny(userInput):
        response = '( ͡° ͜ʖ ͡°) ' + ' '.join(userInput[1:])
        return response

def feat(userInput):
        response = "That's a feat, " + ' '.join(userInput[1:]) + ", and I don't mean an arm." 

        return response   

def joy(userInput):
        response = 'WHY DOESN\'T ' + ' '.join(userInput[1:]).upper() + " RESONATE WITH JOY!?!?" 
        return response   

def kidder(userInput):
        response = "You were always sucha kidder, " + ' '.join(userInput[1:])
        return response

def throw(userInput):
        response = '(╯°□°）╯彡 ' + ' '.join(userInput[1:])
        return response

def eightBall():
        answers =  ['Yes!','No','It is a possibility','answer seems cloudy.','ask again later','it is unknown','never in a million years']
        response = answers[random.randint(0, len(answers)-1)]
        return response

def hello(author,userInput):
        response = 'Hello ' + author
        if len(userInput) > 1:
                response = 'Hello ' + ' '.join(userInput[1:])
        return response

def hayden(userInput):
        response = 'ಠ_ಠ ' + ' '.join(userInput[1:])
        return response

def driveby():
        response = '@@@@@@@@@@@@@@@@@@@@@@@@@@@@ ded'
        return response

def shane():
	response = "JAYSOOOON"
	return response

def throw(userInput):
        response = '(╯°□°）╯彡 ' + ' '.join(userInput[1:])
        return response

def fish(author,userInput):
        fish = ['Snapper','Grouper','Cod','Red Herring','Clown Fish','blue marlin','whale shark','yellowfin tuna','striped bass']
        adjective = [' ','large','slimy','disabled','still flopping','fluorescent','abnormal','well-groomed','godly']
        if len(userInput) > 1:
                response = author + ' slaps ' +' '.join(userInput[1:]) + ' with a ' + adjective[random.randint(0, len(adjective)-1)] + ' ' + fish[random.randint(0, len(fish)-1)]
        else:
                response = 'Enter a name after ' + botPrefix + 'fish.'
        return response

def blacklist(userInput):
        import json
        with open('USERS.json') as file:    # Load database into dictionary "people"
                people = json.load(file)
                
        blacklistActions = ["view","add","remove"]
        if len(userInput) == 3 and userInput[1] in blacklistActions: # If the command is 3 terms long and the action is a valid one from blacklistOptions     
                target = userInput[2]
                if target not in people['users']: # if the target is not in the database, add them
                        people['users'][target] = {'blacklist' : False,"level":0}
                if userInput[1] == 'view' and len(userInput) == 3: #if command is "blacklist view [_NAME_]"
                        if people['users'][target]['blacklist']:
                                response = target + ' is on the blacklist.'                           
                        else: # If the 'blacklist' tag is False
                                response = target + ' is not on the blacklist.'                           

                if userInput[1] == "add" and len(userInput) == 3:     #if command is "blacklist add [_NAME_]"
                    if people['users'][target]['blacklist']:
                        response = target + ' is already on the blacklist.'                           
                    else: # If the 'blacklist' tag is False
                        people['users'][target]['blacklist'] = True
                        response = target + ' has been added to the blacklist.' 

                if userInput[1] == "remove" and len(userInput) == 3:     #if command is "blacklist remove [_NAME_]"
                    if people['users'][target]['blacklist']:
                        people['users'][target]['blacklist'] = False
                        response = target + ' has been removed from the blacklist.'                           
                    else: # If the 'blacklist' tag is True
                        response = target + ' is on the blacklist.' 
                        
                with open('USERS.json', 'w') as outfile:
                    json.dump(people, outfile)
                
        else:
                response = "Syntax is: " +botPrefix + "blacklist [" + ' | '.join(blacklistActions) + "] [_NAME_]"

        return response

def var(userInput):    # var [view|add|subtract|set|create] [_NAME_] (optional_number)
        varOptions = ["view","add","subtract","set","create","delete",'list']
        with open('VARIABLES.json') as var_file:    
                variables = json.load(var_file)
        if len(userInput) > 1:     # if there are values following "var"     var add, var sdf
                varAction = userInput[1].lower()
                if varAction == "list":
                        response = "Variables: "
                        for name in variables:
                                response  += name + "=" + str(variables[name]) + ", "
                        response = response[:-2]
                elif varAction in varOptions and len(userInput) > 2:     # if there is a valid action and at least 2 paramaters
                        varName = userInput[2].lower()
                        varValueTest = True
                        if len(userInput) > 3 and userInput[3].isdigit():
                                varValue = int(userInput[3])
                                varValueTest = True
                        elif len(userInput) > 3:
                                varValueTest = False
                                response = "The last value MUST be blank or numbers"
             
                        if varName in variables:     # if NAME is in the list of variables already
                            
                                if userInput[1] == "view":
                                    response = varName + " = " + str(variables[varName])
                                    
                                elif userInput[1] == "add" and varValueTest:
                                    if len(userInput) > 3:
                                       variables[varName] += varValue
                                       
                                    else:
                                        variables[varName] += 1
                                    response = varName + " = " + str(variables[varName])
                                    with open('VARIABLES.json', 'w') as outfile:
                                        json.dump(variables, outfile)
                                        
                                elif userInput[1] == "subtract" and varValueTest:
                                    if len(userInput) >3:
                                       variables[varName] -= varValue
                                       
                                    else:
                                        variables[varName] -= 1
                                    response = varName + " = " + str(variables[varName])
                                    with open('VARIABLES.json', 'w') as outfile:
                                        json.dump(variables, outfile)
                                        
                                elif userInput[1] == "set" and varValueTest:
                                    if len(userInput) >3:
                                       variables[varName] = varValue
                                       response = varName + " = " + str(variables[varName])
                                    else:
                                        presponse = "Value needed to set variable"
                                    with open('VARIABLES.json', 'w') as outfile:
                                        json.dump(variables, outfile)

                                if userInput[1] == "create":
                                    response = varName + " already exists!. Use \"set\" to set a value."
                                    
                                if userInput[1] == "delete":
                                    del variables[varName]
                                    response = varName + " succesfully deleted."
                                    with open('VARIABLES.json', 'w') as outfile:
                                        json.dump(variables, outfile)
                                    
                        elif varAction == "create":
                                if len(userInput) > 3:
                                    variables[varName] = varValue
                                else:
                                    variables[varName] = 0
                                response = "Variable created with value of " + str(variables[varName])
                                with open('VARIABLES.json', 'w') as outfile:
                                    json.dump(variables, outfile)                
                        elif varAction != "create" and varName not in variables:
                                response = " That variable doesn't exist. Use \"create\" to make a new variable"

                    
                else: # if the action is not valid.
                    response = "Valid actions are: [" + ' | '.join(varOptions) + "]   [\_NAME\_]   (optional_value)"
        else:
                response = "Syntax is: " +botPrefix + "var  [ " + ' | '.join(varOptions) + " ]   [\_NAME\_]   (optional_value)"
        return response

def dice(userInput):
        if len(userInput)>1:
                if dicePattern.match(userInput[1]):
                        numbers = list(map(int,re.split("[d|D]",userInput[1])[0:2]))
                        if numbers[0] <= 0:  #  0 dice condition
                                response = 'You cannot roll 0 dice...'
                        elif numbers[0] > 100: #  Over 100 dice condition
                                response = 'You can only roll up to 100 dice'
                        elif numbers[1] <= 1: #  Dice with over 1000 sides condition
                                response = 'You cannot roll a dice with 1 or fewer sides...'
                        elif numbers[1] > 1000: #  Dice with over 1000 sides condition
                                response = 'Dice are limited to under 100 sides.'
                        else:
                                rolls = []
                                for i in range (0,numbers[0]):
                                        roll = random.randint(1,numbers[1])
                                        rolls.append(str(roll))
                                response = 'Dice Rolls: ' + ', '.join(rolls)
                else:
                        response = 'Invalid entry. Must be format \"' + botPrefix +'dice ###d###\"'
        else:
                response = 'Syntax is \"' + botPrefix +'dice ###d###\"'
        return response

def twitch(userInput):
        names = userInput[1:]
        if len(names) == 0:
            response = 'Enter one or more names after ' + botPrefix + 'twitch in order to get the link(s)'
        elif len(names) == 1:
            response = 'http://twitch.tv/' + names[0]
        else:
            response = 'http://www.multitwitch.tv'
            for name in names:
                response += '/' + name
        return response


def islive(userInput):
        names = userInput[1:]
        index = 0
        response = ''
        if len(names) == 0:
            response = 'Enter a name to view that channels status on twitch.'
        else:
            for name in names:
                url = 'https://api.twitch.tv/kraken/streams/' + name
                try:
                    info = json.loads(urlopen(url, timeout = 15).read().decode('utf-8'))
                    if info['stream'] == None:
                        response += 'No, ' + str(names[index]) + ' is offline.' + '\n'
                    else:
                        response += 'Yes, ' + str(names[index]) + ' is streaming "' + str(info['stream']['game']) + '" to ' + str(info['stream']['viewers']) + ' viewers.' + '\n'
                except URLError as e:
                    if e.reason == 'Not Found' or e.reason == 'Unprocessable Entity':
                        response += 'I\'m sorry, ' + str(names[index]) + ' could not be found.' + '\n'
                    else:
                        response += 'There was an error with your request' + '\n'
                index += 1
        return response
def countdown(userInput):
        number = userInput[1]
        if number.isdigit() and int(number)<=100:    # Check if the number is only 0-9 and under 100
            number = int(number)
            response = 'Countdown: ' + str(number)
            for i in range(0,number):
                number -= 1
                response += ', ' + str(number)
            response += ' BLAST OFF!'
                
        elif number.isdigit():
            response = 'Number entered is over 100, to big!'
        else:
            response = 'Invalid number entered'
        return response
