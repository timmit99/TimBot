import json

running = True;
botPrefix = "$";
blacklistOptions = ["view","add","remove"]

print("The syntax for this command is:")
print(botPrefix  + "blacklist [" + '|'.join(blacklistOptions) + "] [_NAME_] ")
print("The users.json file is able to be opened in any text editor.")

while running:

    userInput = input("enter command: ")

    if userInput.startswith(botPrefix + "blacklist"):   # blacklist [view|add|remove] [_NAME_]
        with open('USERS.json') as file:    
                users = json.load(file)
        userInput = userInput.lower().split()
        if len(userInput) > 1:    #if there is an action following blacklist
            if userInput[1] == 'view':
                response = "Blacklist: "
                for title in users:
                    for name in users[title]:
                        if users[title][name]['blacklist']:
                            response += name + ', '
                print(response[:-2])  #print to Discord

            if userInput[1] == "add":
                if userInput[2] in users['users'] and users['users'][userInput[2]]['blacklist'] == True:
                    response = 'User is already on the blacklist'
                else:
                    users['users'][userInput[2]] = {'blacklist' : True}
                    with open('USERS.json', 'w') as outfile:
                        json.dump(users, outfile)
                    response = 'Added ' + userInput[2] + ' to blacklist'
                print(response)

            if userInput[1] == "remove":
                if userInput[2] in users['users']:
                    #temp = {'level' : 0}
                    users['users'][userInput[2]] = {'level' : 1}
                    with open('USERS.json', 'w') as outfile:
                        json.dump(users, outfile)
                    response = 'Removed ' + userInput[2] + ' from blacklist. Set as regular user.'
                    print(response)

                else:
                    print(userInput[2] + ' is already on the blacklist!')

        else:
            print("Syntax is: var [" + '|'.join(blacklistOptions) + "] [_NAME_]")







    if userInput == "exit":
        running = False
                
