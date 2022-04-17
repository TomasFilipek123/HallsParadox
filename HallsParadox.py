"""The Monty Hall Problem 
In the problem, you are on a game show, being asked to choose between three doors.
Behind each door, there is either a car or a goat. You choose a door. 
The host, Monty Hall, picks one of the other doors, which he knows has a goat behind it, and opens it, showing you the goat.
(You know, by the rules of the game, that Monty will always reveal a goat.)
Monty then asks whether you would like to switch your choice of door to the other remaining door.
Assuming you prefer having a car more than having a goat, do you choose to switch or not to switch?"""

import random, sys, time


NUM_OF_DOORS = 3
CLOSED = """
+--------------+
|              |
|    {}         |
|              |
|  *           |
|              |
|              |
|              |
+--------------+"""
CAR = r"""
+--------------+
|              |\
|              | \
|              |  \
|   ______     |  |
|  /|_||_\`.__ |  |
| (   _    _ _\| *| 
| =`-(_)--(_)-'|  |
+--------------+  |
                \ |
                 \|"""

GOAT = r'''
+--------------+
|              |\
|              | \ 
|              |  \
| (_(          |  |
| /_/'_____/)  |  |
| "  |      |  | *|
|    |""""""|  |  |
+______________+  |
                \ |
                 \|'''
strings = [GOAT, CAR, CLOSED]
doorsNums = ['1', '2', '3']

def main():
    wins = 0
    games = 0

    while True:
        doors = getNewDoors()
        displayTheDoors(doors)
        # Get index of the door player chooses
        guess = playerGuess()

        # Open random 'goat' door, not occupied by a player
        if random.randint(0, 1) == 0:
            for (doorIndex, behindDoor) in doors:
                if behindDoor == 'goat' and doorIndex != guess:
                    doors[doorIndex, behindDoor] = True
                    break
        else:
            for (doorIndex, behindDoor) in reversed(doors):
                if behindDoor == 'goat' and doorIndex != guess:
                    doors[doorIndex, behindDoor] = True
                    break
        displayTheDoors(doors)
        print()
        # Second round
        while True:
            # Monty hall asks if you want to change your guess
            print('Do you want to change your guess? (Y/N)')
            res = input('> ').upper().strip()
            if res.startswith('Y'):
                for (doorIndex, behindDoor) in doors:
                    if not doors[(doorIndex, behindDoor)]:
                        guess = doorIndex
                break
            elif res.startswith('N'):
                break
            continue

        # Opening the player's doors:
        for (doorIndex, behindDoor) in doors:
            if doorIndex == guess:
                doors[(doorIndex, behindDoor)] = True
                displayTheDoors(doors)
                if behindDoor == 'car':
                    print('Congratulations, You have won!')
                    wins += 1

                else:
                    print('You lose.')
        games += 1
        print(f'Your score: {wins}/{games}')
        print('Do You want to play again? (Y/N)')
        if input('> ').upper().startswith('N'):
            print('Thanks for playing!')
            print(f'Chance of winning the game with "changing door" technique: {changingDoors()}%')
            print(f'Chance of winning the game with "not-changing door" technique: {notChangingDoors()}%')
            time.sleep(5)
            sys.exit()

def getNewDoors():
    """Initialize the dictionary which represents the doors"""
    awardIndex = random.randint(0, 2)
    doors = {}
    for i in range(NUM_OF_DOORS):
        if i == awardIndex:
            doors[(i, 'car')] = False
        else:
            doors[(i, 'goat')] = False
    return doors

def displayTheDoors(doors):
    """Display the ASCII art representation of doors"""
    for (doorIndex, behindDoor) in doors:
        if doors[(doorIndex, behindDoor)] == False:
            print(CLOSED.format(doorIndex + 1))
        elif doors[(doorIndex, behindDoor)] == True:
            if behindDoor == 'car':
                print(CAR)
            elif behindDoor == 'goat':
                print(GOAT)
    print()

def playerGuess():
    """Get player's guess"""
    while True:
        print('Choose door number(1-3) or QUIT')
        res = input('> ').upper()
        if res == 'QUIT':
            print('Thanks for playing')
            sys.exit()
        if not res.isdecimal():
            print('Enter a number!')
            continue
        resIndex = int(res) - 1
        return resIndex

def notChangingDoors():
    """Simulation of 100_000 games 'not changing doors' technique"""
    wins = 0
    numOfSimulaitons = 100_000

    for i in range(numOfSimulaitons):
        doors = list('001')
        random.shuffle(doors)
        choice = random.randint(0, len(doors) - 1)
        if doors[choice] == '1':
            wins += 1
    winProbab = round(wins/numOfSimulaitons * 100, 2)
    return str(winProbab)

def changingDoors():
    """Simulation of 100_000 games 'changing doors' technique"""
    wins = 0
    numOfSimulations = 100_000
    for i in range(numOfSimulations):
        doors = list('001')
        random.shuffle(doors)
        choice = random.randint(0, len(doors) - 1)
        # Change guess - delete chosen doors
        del doors[choice]
        # open - delete remaining 'losing' door
        for doorNum in range(len(doors)):
            if doors[doorNum] == '0':
                del doors[doorNum]
                break
        # ultimately open the player's guess doors and check if player wins
        if doors[0] == '1':
            wins += 1
    winProbab = round(wins/numOfSimulations * 100, 2)
    return str(winProbab)

if __name__ == '__main__':
    main()