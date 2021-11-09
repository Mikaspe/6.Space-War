class State:
    """Superclass for each state"""
    def __init__(self) -> None:
        self.done = False  # When True 'control' class will change state to the another
        self.next = None  # Name of a next state
        self.quit = False  # When True 'control' class will close window
        self.previous = None  # Memory of a previous state name
