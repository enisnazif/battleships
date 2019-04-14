from abc import abstractmethod


class Bot:

    def get_bot_name(self):
        return str(type(self).__name__)

    @abstractmethod
    def place_ships(self, ships):
        """ This method should return a valid ship placement on the board of the opponent. It is called once """
        pass

    @abstractmethod
    def get_shot(self, board):
        """ This method should return a valid shot on the board as an (x,y) coordinate. It is called by the game engine each round """
        pass
