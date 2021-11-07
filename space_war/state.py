class State:
    """Superclass for each state"""
    def __init__(self) -> None:
        self.done = False  # When True 'control' class will change state to the another
        self.next = None  # Definied name of a next state
        self.quit = False  # When True 'control' class will close game window
        self.previous = None  # Name memory of a previous state
