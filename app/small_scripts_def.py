def check_points_treshold(total_points):

    #this will give an experience treshold
    level = total_points/50

    if (level >= 10):
        return 10

    else:
        return level

# This is just a very easy function to mesure the level obtained, proof of concept. to be changed later TODO
