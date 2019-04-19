from abc import abstractmethod
from man.battleships.types import Ship
from typing import List


class Bot:

    def __init__(self):
        self._last_shot_status = (None, None)

    @property
    def name(self):
        return str(type(self).__name__)

    @property
    def last_shot_status(self):
        return self._last_shot_status

    @last_shot_status.setter
    def last_shot_status(self, value):
        self._last_shot_status = value

    @abstractmethod
    def place_ships(self, ships: List[Ship]):
        """ This method should return a valid ship placement on the board of the opponent. It is called once """
        pass

    @abstractmethod
    def get_shot(self):
        """ This method should return a valid shot on the board as an (x,y) coordinate. It is called by the game engine each round """
        pass
