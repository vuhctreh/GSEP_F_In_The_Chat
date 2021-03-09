""" Functions regarding the users total points and level (used mainly for unlocking collectables) """


# william
def check_points_treshold(total_points):
    """ Calculates the users level based on his total points
    
    Args:
        total_points::int
            The total number of points that the user has gained

    Returns:
        level::int
            The users level calculated from his total points
    """

    # This is just a very easy function to mesure the level obtained, proof of
    # concept. to be changed later TODO

    # This will give an experience treshold
    level = total_points/50

    if level >= 9:
        level = 9

    return level


# william
def how_much_to_go(current_level):
    """ Calculates the number of points the user needs to obtain to advance levels 
        based on his current level

    Args:
        current_level::int 
            The users current level

    Returns:
        to_go_points::int
            The number of points the user needs to gain in order to move onto
            the next level
    """

    if current_level < 9:
        # transforming the current_level which is a float into an int
        int_value = int(current_level)

        # adding 1 to the int value to get the next threshold
        # take away from the next threshold the current level
        # this will give the level missing to go to the next threshold
        to_go_level = (int_value+1) - current_level

        # multiplying it by the 50 (this value has to be the same as the
        # divider in the function check_points_treshold)
        # this gives the number of points to go before the next treshold
        to_go_points = to_go_level*50

    else:
        to_go_points = 0

    return to_go_points
