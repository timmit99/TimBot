userInput = input('Enter add or remove followd by a name: ')
userInput = userInput.split()
print(userInput)
blacklist = open('blacklist.txt', 'r+')


if userInput[0] == 'view':
    for line in blacklist:
        print(line)

elif userInput[0] == 'add':
    
    print('Adding User ' + userInput[1])
    location = blacklist.read().find(userInput[1])
    print('location = '+ str(location))
    if location >= 0: # if name is on the blacklist
        print('Name is already on the list.')

    else:
        print('Name is NOT in the blacklist')
        blacklist.close()
        open('blacklist.txt','a').write(userInput[1] + '\n')
        
        
elif userInput[0] == 'remove':
    lines = blacklist.readlines()
    blacklist.close()
    blacklist = open("blacklist.txt","w")
    for line in lines:
        if line != userInput[1]+"\n":
            blacklist.write(line)
    blacklist.close()
    
else:
    print('Invalid entry')
