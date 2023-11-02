import random 

# Creates random range of 3 defined colors
def three_color_palette(pcd, c1_min, c1_max, c2_min, c2_max, c3_min, c3_max):
    # Create a list of colors
    colors = []
    for _ in range(len(pcd.points)):
        color_range = random.randint(0, 2)  # Randomly select 0, 1, or 2
        if color_range == 0:
            color = [random.randint(c1_min[0], c1_max[0]),
                     random.randint(c1_min[1], c1_max[1]),
                     random.randint(c1_min[2], c1_max[2])]
        elif color_range == 1:
            color = [random.randint(c2_min[0], c2_max[0]),
                     random.randint(c2_min[1], c2_max[1]),
                     random.randint(c2_min[2], c2_max[2])]
        else:
            color = [random.randint(c3_min[0], c3_max[0]),
                     random.randint(c3_min[1], c3_max[1]),
                     random.randint(c3_min[2], c3_max[2])]
        colors.append(color)

    return colors

# Creates random range of 2 defined colors
def two_color_palette(pcd, c1_min, c1_max, c2_min, c2_max):
    colors = []
    for _ in range(len(pcd.points)):
        color_range = random.randint(0, 1)  # Randomly select 0, 1
        if color_range == 0:
            color = [random.randint(c1_min[0], c1_max[0]),
                     random.randint(c1_min[1], c1_max[1]),
                     random.randint(c1_min[2], c1_max[2])]
        else:
            color = [random.randint(c2_min[0], c2_max[0]),
                     random.randint(c2_min[1], c2_max[1]),
                     random.randint(c2_min[2], c2_max[2])]
        colors.append(color)

    return colors

# Creates random range of 3 defined colors
def one_color_palette(pcd, c1_min, c1_max):
    # Create a list of colors
    colors = []
    for _ in range(len(pcd.points)):
        color = [random.randint(c1_min[0], c1_max[0]),
                 random.randint(c1_min[1], c1_max[1]),
                 random.randint(c1_min[2], c1_max[2])]
        colors.append(color)

    return colors