"""Generating game levels and export them to the 'game_levels.pickle' file.
One level is a list with an enemy spaceships composition. Each element in a list is a tuple(x_pos, y_pos, enemy_style).
All levels are stored in one dictionary, where key is number of the level, and value is a list with tuples.
"""

import pickle


def level_gen() -> None:

    one_level = []  # List with tuples (x_pos, y_pos, enemy_style) which define enemy spaceships
    game_levels = {}  # Dictionary with one_level lists. Key is a level number.

    level = 1
    enemy_style = 1
    for y in range(1, 3):
        for x in range(6):
            one_level.append((x * 100, y * 75, enemy_style))
    game_levels[level] = one_level.copy()
    one_level.clear()

    level = 2
    enemy_style = 1
    for y in range(3):
        for x in range(8):
            one_level.append((x * 100, y * 75, enemy_style))
    game_levels[level] = one_level.copy()
    one_level.clear()

    level = 3
    enemy_style = 2
    for y in range(2):
        for x in range(3):
            one_level.append((x * 100, y * 75, enemy_style))
    game_levels[level] = one_level.copy()
    one_level.clear()

    level = 4
    enemy_style = 1
    for y in range(3):
        if y == 2:
            enemy_style = 2
        for x in range(8):
            one_level.append((x * 100, y * 75, enemy_style))
    game_levels[level] = one_level.copy()
    one_level.clear()

    level = 5
    enemy_style = 3
    for y in range(2):
        for x in range(1, 5):
            one_level.append((x * 100, y * 75, enemy_style))
    game_levels[level] = one_level.copy()
    one_level.clear()

    level = 6
    enemy_style = 3
    for y in range(4):
        if y >= 2:
            enemy_style = 2
        for x in range(6):
            one_level.append((x * 100, y * 75, enemy_style))
    game_levels[level] = one_level.copy()
    one_level.clear()

    level = 7
    for y in range(4):
        for x in range(8):
            if y <= 2:
                enemy_style = 3
            elif y > 2 and x in range(3, 5):
                enemy_style = 3
            else:
                enemy_style = 2
            one_level.append((x * 100, y * 75, enemy_style))
    game_levels[level] = one_level.copy()
    one_level.clear()

    level = 8
    enemy_style = 4
    one_level.append((1200/2, 170, enemy_style))
    game_levels[level] = one_level.copy()

    with open('game_levels.pickle', 'wb') as handle:  # Export dictionary to the 'game_levels.pickle' file
        pickle.dump(game_levels, handle, protocol=pickle.HIGHEST_PROTOCOL)
