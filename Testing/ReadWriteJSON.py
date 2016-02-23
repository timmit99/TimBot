import json

running = True;
botPrefix = "$";
varOptions = ["view","add","subtract","set","create","delete"]

print("The syntax for this command is:")
print("$var [" + '|'.join(varOptions) + "] [_NAME_] (optional_value)")
print("The VARIABLES.json file is able to be opened in any text editor.")
print("It contains 'count' to start with.")

while running:

    userInput = input("enter command: ")

    if userInput.startswith(botPrefix + "var "):   # var [view|add|subtract|set|create] [_NAME_] (optional_number)
        with open('VARIABLES.json') as var_file:    
                variables = json.load(var_file)
        userInput = userInput.split()
        if len(userInput) > 1:     # if there are values following "var"     var add, var sdf
            varAction = userInput[1].lower()
                        
            if varAction in varOptions and len(userInput) > 2:     # if there is a valid action and at least 2 paramaters
                varName = userInput[2].lower()
                if len(userInput) > 3:
                    if userInput[3].isdigit():
                        varValue = int(userInput[3])
                
                if varName in variables:     # if NAME is in the list of variables already
                        
                    if userInput[1] == "view":
                        print(varName + " = " + str(variables[varName]))
                        
                    elif userInput[1] == "add":
                        if len(userInput) >3:
                           variables[varName] += varValue
                           
                        else:
                            variables[varName] += 1
                        print(variables[varName])
                        with open('VARIABLES.json', 'w') as outfile:
                            json.dump(variables, outfile)
                            
                    elif userInput[1] == "subtract":
                        if len(userInput) >3:
                           variables[varName] -= varValue
                           
                        else:
                            variables[varName] -= 1
                        print(variables[varName])
                        with open('VARIABLES.json', 'w') as outfile:
                            json.dump(variables, outfile)
                            
                    elif userInput[1] == "set":
                        if len(userInput) >3:
                           variables[varName] = varValue
                           
                        else:
                            print("Value needed to set variable")
                        with open('VARIABLES.json', 'w') as outfile:
                            json.dump(variables, outfile)

                    if userInput[1] == "create":
                        print(varName + " already exists!. Use \"set\" to set a value.")

                    if userInput[1] == "delete":
                        del variables[varName]
                        
                elif varAction == "create":
                    if len(userInput) > 3:
                        variables[varName] = varValue
                    else:
                        variables[varName] = 0
                    print("Variable created with value of " + str(variables[varName]))
                    with open('VARIABLES.json', 'w') as outfile:
                        json.dump(variables, outfile)                
                elif varAction != "create" and varName not in variables:
                    print(" That variable doesn't exist. Use \"create\" to make a new variable")

                
            else: # if the action is not valid.
                print("Valid actions are: [" + '|'.join(varOptions) + "] [_NAME_] (optional_value)")
        else:
            print("Syntax is: var [" + '|'.join(varOptions) + "] [_NAME_] (optional_value)")
            
    if userInput == "exit":
        running = False
                
