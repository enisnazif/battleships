class InvalidOrientationError(ValueError):
    pass


class PointAlreadyShotException(Exception):
    pass


class ShotOffBoardException(Exception):
    pass


class InvalidShipPlacementException(Exception):
    pass


class MaxRetriesExceededException(Exception):
    pass


class NotAPointError(TypeError):
    pass
