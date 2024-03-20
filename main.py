from typing import List
import itertools


# currently employing brute force, branch and bound would be best
class Pandora:
    def __init__(self, startingStamina, maxStamina):
        self.startingStamina = startingStamina
        self.maxStamina = maxStamina


class Collectable:
    def __init__(self, turn, value):
        self.turn = turn
        self.value = value


class Game:
    def __init__(self, numTurns, numDemons):
        self.demonList = None
        self.pandora = None
        self.numTurns = numTurns
        self.numDemons = numDemons

    def setPandora(self, pandora):
        self.pandora = pandora

    def setDemonList(self, demonList):
        self.demonList = demonList

    def simulateGame(self, order: list):  # type of order enforced to give IDE a hint
        currentScore = 0
        currentStamina = self.pandora.maxStamina

        staminaList: list[Collectable] = []  # done to enforce a type on this list, gives ide a hint for autocomplete
        fragmentList: list[Collectable] = []

        # this simulates all turns
        for turn in range(0, self.numTurns):
            if len(order) == 0: #in case it kills all demons before the end of the match
                break
            #print("turn : " + str(turn))
            # check if I can collect stamina in this turn, then discard the entry in the list
            for i in staminaList:
                if i.turn == turn:
                    # case in which i could replenish stamina
                    if currentStamina < self.pandora.maxStamina:
                        #print("gained " + str(i.value) + " stamina")
                        currentStamina += i.value
                    # done to avoid going over maxStamina (could be written more elegantly)
                    if currentStamina > self.pandora.maxStamina:
                        currentStamina = self.pandora.maxStamina

                    staminaList.pop(staminaList.index(i))

            # now select a demon and see if I can fight him
            #print(order)
            #print("current stamina " + str(currentStamina))
            selectedDemon: Demon = self.demonList[order[0]]
            if selectedDemon.consumedStamina <= currentStamina:
                #print("decision taken, killing " + str(order[0]))
                # drain energy
                currentStamina -= selectedDemon.consumedStamina
                # set staminaList and fragmentList
                staminaList.append(Collectable(selectedDemon.turnToRegainStamina + turn, selectedDemon.regainedStamina))

                dropList = selectedDemon.fragmentDrop
                for i in range(0, selectedDemon.turnsForFragments - 1):
                    fragmentList.append(Collectable(i + turn, dropList[i]))
                # then pop the defeat demon from list (ie pop first element of order)
                order.pop(0)

            # see if there are fragments to collect
            for i in fragmentList:
                if i.turn == turn:
                    currentScore += i.value
                    fragmentList.pop(fragmentList.index(i))

        return currentScore

    # currently brute force
    def optimize(self):

        bestScore = 0
        originalList = [item for item in range(0, len(self.demonList))]     # creates a list ranging from 0 to num of demons minus one
        allOrders = list(map(list, itertools.permutations(originalList)))   # creates all permutations of originalList (maps the tuple origination in iterTools to a list, then places them in a list)

        for order in allOrders:
            orderCopy = order.copy()
            score = self.simulateGame(order)
            if score > bestScore:
                bestOrder = orderCopy
                bestScore = score

        return bestOrder


class Demon:
    def __init__(self, consumedStamina, turnToRegainStamina, regainedStamina, turnsForFragments, fragmentDrop):
        self.consumedStamina = consumedStamina
        self.turnToRegainStamina = turnToRegainStamina
        self.regainedStamina = regainedStamina
        self.turnsForFragments = turnsForFragments  # num of turns for which fragments are dropped
        self.fragmentDrop = fragmentDrop  # list of dropped fragments in the sequent turns


def ingest():
    # This opens a handle to your file, in 'r' read mode
    file_handle = open('C:\\Users\\daniel\\Desktop\\test.txt', 'r')
    # Read in all the lines of your file into a list of lines
    lines_list = file_handle.readlines()
    # Do a double-nested list comprehension to get the rest of the data into your matrix
    my_data = [[int(val) for val in line.split()] for line in lines_list[0:]]

    pandora = Pandora(my_data[0][0], my_data[0][1])
    game = Game(my_data[0][2], my_data[0][3])

    game.setPandora(pandora)

    demonList = list()
    for i in range(1, len(my_data)):
        fragmentDrop = list()
        for j in range(4, 3 + my_data[i][3]):
            drop = my_data[i][j]
            fragmentDrop.append(drop)

        demon = Demon(my_data[i][0], my_data[i][1], my_data[i][2], my_data[i][3], fragmentDrop)
        demonList.append(demon)
    game.setDemonList(demonList)

    return game


def main():
    game = ingest()
    result = game.optimize()
    print(result)
    print(game.simulateGame(result)) #to print score


if __name__ == "__main__":
    main()
