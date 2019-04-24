import importlib
import random
from man.battleships.exceptions import (
    InvalidShipPlacementException,
    PointAlreadyShotException,
    ShotOffBoardException,
    MaxRetriesExceededException,
    NotAPointError
)
from man.battleships.types.Ship import ships_to_place
from man.battleships.types import Point, Board
from man.battleships.config import MAX_MOVE_TIME, MAX_RETRIES, BOARD_SIZE
import timeout_decorator
import logging

logger = logging.getLogger("game")


def competition_decorator():
    pass


def retry(exceptions, max_retries=MAX_RETRIES):
    """
    Retry decorator that retries the wrapped function a maximum of 'max_retries' times if 'exception' is raised

    :param exceptions: Tuple
    :param max_retries:
    :return:
    """

    def deco_retry(f):
        def f_retry(*args, **kwargs):
            n_retries = 0
            while n_retries < max_retries:
                try:
                    return f(*args, **kwargs)
                except exceptions as e:
                    logger.exception(e)
                    n_retries += 1
                    continue
            raise MaxRetriesExceededException

        return f_retry

    return deco_retry


class Game:
    def __init__(self, players, game_id):

        # Set game_id
        self.game_id = game_id

        # Create boards
        self.first_player_board = Board(BOARD_SIZE)
        self.second_player_board = Board(BOARD_SIZE)

        # Import the players
        bots_path = "man.battleships.bots"
        self.player_bots = [
            getattr(importlib.import_module(f"{bots_path}.{p}"), p)() for p in players
        ]

        # Flip a coin to decide who goes first
        self.first_player, self.second_player = random.sample(self.player_bots, k=2)

    def play_game(self):
        """
        Play a single game between two bots and return the winner, along with the game history

        :param player_1_bot:
        :param player_2_bot:
        :param game_id:
        :return:
        """

        # Perform ship placement (Keep retrying until we get a correct placement). If we don't, end the game here
        try:
            p1_placements = self._place_ships(self.first_player, self.first_player_board)
        except MaxRetriesExceededException:
            p1_placements = []

        try:
            p2_placements = self._place_ships(self.second_player, self.second_player_board)
        except MaxRetriesExceededException:
            p2_placements = []

        if not p1_placements or not p2_placements:
            return {
                "id": self.game_id,
                "p1_name": self.first_player.name,
                "p2_name": self.second_player.name,
                "p1_ship_placements": [],
                "p2_ship_placements": [],
                "p1_shots": [],
                "p2_shots": [],
                "winner": None,
            }

        p1_shots = []
        p2_shots = []

        # Game loop - get shots until a player wins
        while True:

            try:
                p1_shot, p1_is_hit = self._do_shot(
                    self.first_player, self.second_player_board
                )
            except (MaxRetriesExceededException, NotAPointError):
                p1_shot, p1_is_hit = None, None

            p1_shots.append(p1_shot)

            if self.second_player_board.is_board_lost():
                winner = self.first_player.name
                break

            try:
                p2_shot, p2_is_hit = self._do_shot(
                    self.second_player, self.first_player_board
                )
            except (MaxRetriesExceededException, NotAPointError):
                p2_shot, p2_is_hit = None, None

            p2_shots.append(p2_shot)

            if self.first_player_board.is_board_lost():
                winner = self.second_player.name
                break

            # Notify game bots of the status of their last shot
            self.first_player.last_shot_status = (p1_shot, p1_is_hit)
            self.second_player.last_shot_status = (p2_shot, p2_is_hit)

        return {
            "id": self.game_id,
            "p1_name": self.first_player.name,
            "p2_name": self.second_player.name,
            "p1_ship_placements": list(p1_placements),
            "p2_ship_placements": list(p2_placements),
            "p1_shots": list(p1_shots),
            "p2_shots": list(p2_shots),
            "winner": winner,
        }

    @retry((InvalidShipPlacementException, timeout_decorator.timeout_decorator.TimeoutError))
    @timeout_decorator.timeout(MAX_MOVE_TIME)
    def _place_ships(self, player, board):
        ship_placements = player.get_ship_placements(ships_to_place())

        # Ensure that the ship placements are of the correct format
        try:
            assert len(ship_placements) == len(ships_to_place())
        except AssertionError:
            raise InvalidShipPlacementException

        for ship, location, orientation in ship_placements:
            board.place_ship(ship, location, orientation)

        return board.ship_locations

    @retry((ShotOffBoardException, PointAlreadyShotException, timeout_decorator.timeout_decorator.TimeoutError))
    @timeout_decorator.timeout(MAX_MOVE_TIME)
    def _do_shot(self, player, board_to_shoot):
        player_shot = player.get_shot()

        # Ensure that the player is returning a point
        try:
            assert isinstance(player_shot, Point)
        except AssertionError:
            raise NotAPointError

        is_hit = board_to_shoot.shoot(player_shot)

        return player_shot, is_hit



