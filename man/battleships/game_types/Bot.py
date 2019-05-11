from abc import abstractmethod
from man.battleships.game_types import Ship, Point, Orientation, ShipType
from typing import List, Tuple, Dict, Union


class Bot:
    def __init__(self):
        self._last_shot_status = {'shot': None,
                                  'is_hit': None,
                                  'is_sunk': None,
                                  'ship_sunk': None,
                                  'error': None}

    @property
    def name(self):
        return str(type(self).__name__)

    @property
    def last_shot_status(self) -> Dict[str, Union[Point, bool, bool, ShipType, None]]:
        """
        This method returns the status of the last shot you made on the opponent's board as a dict

        Example response:

        {
            'shot': Point(4, 5),                                # type: Point
            'is_hit': True,                                     # type: bool
            'is_sunk' True,                                     # type: bool
            'ship_sunk': <ShipType.Battleship: 'Battleship'>,   # type: ShipType
            'error': None                                       # type: Union[None, Exception]
        }
        """
        return self._last_shot_status

    @last_shot_status.setter
    def last_shot_status(self, value: Dict[str, Union[Point, bool, bool, ShipType, None]]):
        self._last_shot_status = value

    @abstractmethod
    def get_ship_placements(self, ships: List[Ship]) -> List[Tuple[Ship, Point, Orientation]]:
        """ This method should return a list of valid ship placements. It is called once at the start of each game """
        pass

    @abstractmethod
    def get_shot(self) -> Point:
        """ This method should return a valid shot on the board as an Point(x, y). It is called by the game engine each round """
        pass
