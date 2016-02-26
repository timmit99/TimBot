import re
import random

userInput = input('Enter add or remove followd by a name: ')
userInput = userInput.split()
botPrefix = '$'

dicePattern = re.compile('(\d*)[d|D](\d)+$') # '[1-9](\d*)d[\d+'
def dice(userInput):
     if len(userInput)>1:
          if dicePattern.match(userInput[1]):
               numbers = list(map(int,re.split("[d|D]",userInput[1])[0:2]))
               print(numbers)
               if numbers[0] == 0:  #  0 dice condition
                    response = 'You cannot roll 0 dice...'
               elif numbers[0] > 100: #  Over 100 dice condition
                    response = 'You can only roll up to 100 dice'
               elif numbers[1] > 1000: #  Dice with over 1000 sides condition
                    response = 'Dice are limited to under 100 sides.'
               else:
                    rolls = []
                    print(rolls)
                    response = 'Rolling ' + str(numbers[0]) + ' of D'  + str(numbers[1]) + ' dice'
                    print(response)
                    for i in range (0,numbers[0]):
                         roll = random.randint(1,numbers[1])
                         print(str(roll))
                         rolls.append(str(roll))
                    response = 'Dice Rolls: ' + ', '.join(rolls)
          else:
               response = 'Invalid entry. Must be format \"' + botPrefix +'dice ###d###\"'
     else:
          response = 'Syntax is \"' + botPrefix +'dice ###d###\"'
     return response

response = dice(userInput)

print(response)

