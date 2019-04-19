import importlib
from man.battleships.types.Board import (
    Board,
    InvalidShipPlacementException,
    PointAlreadyShotException,
    ShotOffBoardException,
)
from man.battleships.types.Ship import ships_to_place
from man.battleships.types.AntiCheatContainer import AntiCheatContainer
from man.battleships.config import BOARD_SIZE


def retry(exception, max_retries=3):
    """
    Retry decorator that retries the wrapped function a maximum of 'max_retries' times if 'exception' is raised

    :param exception:
    :param max_retries:
    :return:
    """

    def deco_retry(f):
        def f_retry(*args, **kwargs):
            n_retries = 0
            while n_retries < max_retries:
                try:
                    return f(*args, **kwargs)
                except exception:
                    n_retries += 1
                    continue
            return [], []  # All retries failed :( #TODO: Raise a MaxRetriesExceeded exception?

        return f_retry

    return deco_retry


class Game:
    def __init__(self, player_1, player_2, game_id):

        bots_path = "man.battleships.bots"
        player_1_bot = importlib.import_module(f"{bots_path}.{player_1}")
        player_2_bot = importlib.import_module(f"{bots_path}.{player_2}")

        self.player_1_bot = getattr(player_1_bot, player_1)()
        self.player_2_bot = getattr(player_2_bot, player_2)()
        self.game_id = game_id

        # Define boards
        self.player_1_board = Board(BOARD_SIZE)
        self.player_2_board = Board(BOARD_SIZE)

    def play_game(self):
        """
        Play a single game between two bots and return the winner, along with the game history

        :param player_1_bot:
        :param player_2_bot:
        :param game_id:
        :return:
        """

        # Load the players
        player_1 = AntiCheatContainer(self.player_1_bot)
        player_2 = AntiCheatContainer(self.player_2_bot)

        # Perform ship placement (Keep retrying until we get a correct placement)
        p1_placements = self._place_ships(player_1.bot, self.player_1_board)
        p2_placements = self._place_ships(player_2.bot, self.player_2_board)

        p1_shots = []
        p2_shots = []

        # Game loop - get shots until a player wins
        while True:
            p1_shot, p1_is_hit = self._do_shot(
                player_1.bot, self.player_2_board
            )
            p2_shot, p2_is_hit = self._do_shot(
                player_2.bot, self.player_1_board
            )

            p1_shots.append(p1_shot)
            p2_shots.append(p2_shot)

            # Notify game bots of the status of their last shot
            player_1.bot.last_shot_status = (p1_shot, p1_is_hit)
            player_2.bot.last_shot_status = (p2_shot, p2_is_hit)

            if self.player_1_board.is_game_won():
                winner = player_2.bot.name
                break

            if self.player_2_board.is_game_won():
                winner = player_1.bot.name
                break

        return {
            "id": self.game_id,
            "p1_name": player_1.bot.name,
            "p2_name": player_2.bot.name,
            "winner": winner,
            "p1_shots": [shot for shot in p1_shots if shot],
            "p1_ship_placements": [p for p in p1_placements],
            "p2_shots": [shot for shot in p2_shots if shot],
            "p2_ship_placements": [p for p in p2_placements],
        }


    @retry(InvalidShipPlacementException)
    def _place_ships(self, player, board):
        player_ship_placements = player.place_ships(ships_to_place())

        for ship, point, orientation in player_ship_placements:
            board.place_ship(ship, point, orientation)

        return board.get_ship_locations()

    @retry(ShotOffBoardException)
    @retry(PointAlreadyShotException)
    def _do_shot(self, player, board_to_shoot):
        player_shot = player.get_shot()
        is_hit = board_to_shoot.shoot(player_shot)
        return player_shot, is_hit
