from man.battleships.types.Point import Point


def test_point():
    p = Point(5, 3)

    assert p.x == 5
    assert p.y == 3
