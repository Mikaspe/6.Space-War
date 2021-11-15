from abc import ABC, abstractmethod


class State(ABC):
    """Superclass for each state"""
    def __init__(self) -> None:
        self.done = False  # When True, 'control' class will change state to the another
        self.next = None  # Name of a next state
        self.quit = False  # When True, 'control' class will close window
        self.previous = None  # Memory of a previous state name

    @abstractmethod
    def cleanup(self) -> None:
        """Called when state is done."""
        pass

    @abstractmethod
    def startup(self) -> None:
        """Called once when state is active."""
        pass

    @abstractmethod
    def get_event(self, event) -> None:
        """Gets and process events."""
        pass

    @abstractmethod
    def update(self, keys, dt) -> None:
        """Main method of the state."""
        pass

    @abstractmethod
    def draw(self, dt) -> None:
        """Draws on the screen."""
        pass
