class generic:
    pass    #this makes me able to



def main():
    ingest()


def ingest():

    # This opens a handle to your file, in 'r' read mode
    file_handle = open('C:\\Users\\daniel\\Desktop\\test.txt', 'r')
    # Read in all the lines of your file into a list of lines
    lines_list = file_handle.readlines()
    # Do a double-nested list comprehension to get the rest of the data into your matrix
    my_data = [[int(val) for val in line.split()] for line in lines_list[0:]]

    pandora = generic()
    game = generic()

    pandora.startingStamina = my_data[0][0]
    pandora.maxStamina = my_data[0][1]

    game.numTurns = my_data[0][2]
    game.numDemons = my_data[0][3]

    demonList = list()
    for i in range (1, len(my_data)):
        demon = generic()

        demon.consumedStamina = my_data[i][0]
        demon.turnToRegainStamina = my_data[i][1]





if __name__ == "__main__":
    main()
