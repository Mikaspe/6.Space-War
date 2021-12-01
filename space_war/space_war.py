import sys

import pygame

from .control import Control


def main() -> None:
    """Game initialization."""
    pygame.init()
    app = Control()
    app.main_game_loop()

    pygame.quit()
    sys.exit()


main()
