class State:
    """Superclass for each state"""
    def __init__(self):
        self.done = False
        self.next = None
        self.quit = False
        self.previous = None
