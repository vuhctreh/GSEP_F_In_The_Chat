#william
def check_points_treshold(total_points):

    # This is just a very easy function to mesure the level obtained, proof of concept. to be changed later TODO

    #this will give an experience treshold
    level = total_points/50

    if (level >= 9):
        return 9

    else:
        return level

#william
def how_much_to_go(current_level):

    if (current_level<9):
        # transforming the current_level which is a float into an int
        int_value = int(current_level)

        # adding 1 to the int value to get the next threshold
        # take away from the next threshold the current level
        # this will give the level missing to go to the next threshold
        to_go_level = (int_value+1) - current_level

        # multiplying it by the 50 (this value has to be the same as the divider in the function check_points_treshold)
        # this gives the number of points to go before the next treshold
        to_go_points = to_go_level*50

        return to_go_points

    else:
        return 0
