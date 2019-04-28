from abc import abstractmethod
from man.battleships.game_types import Ship, Point, Orientation
from typing import List, Tuple, Union


class Bot:
    def __init__(self):
        self._last_shot_status = (None, None)

    @property
    def name(self):
        return str(type(self).__name__)

    @property
    def last_shot_status(self) -> Union[Tuple[None, None], Tuple[None, Exception], Tuple[Point, bool], Tuple[Point, Exception]]:
        """
        This method returns the status of the last shot you made on the opponent's board.

        Example responses you could receive:

        (None, None)                                    - no shot has yet been made (initial value)
        (None, MaxRetriesExceededException)             - no shot was made since your bot exceeded 3 retries
        (Point(4, 3), True)                             - you shot at (4, 3) and hit
        (Point(1, 4), False)                            - you shot at (1, 4) and missed
        (Point(1, 4), Exception)                        - your shot at (8, 2) failed with some exception
        """
        return self._last_shot_status

    @last_shot_status.setter
    def last_shot_status(self, value:  Union[Tuple[None, Exception], Tuple[Point, bool], Tuple[Point, Exception]]):
        self._last_shot_status = value

    @abstractmethod
    def get_ship_placements(self, ships: List[Ship]) -> List[Tuple[Ship, Point, Orientation]]:
        """ This method should return a list of valid ship placements. It is called once at the start of each game """
        pass

    @abstractmethod
    def get_shot(self) -> Point:
        """ This method should return a valid shot on the board as an (x,y) coordinate. It is called by the game engine each round """
        pass
