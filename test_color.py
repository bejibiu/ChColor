from chcolor import convert_to_RJB


def test_change_color_with_sharp():
    color = convert_to_RJB("#000000")
    assert color == [0, 0, 0]


def test_change_colot_without_sharp():
    color = convert_to_RJB("000000")
    assert color == [0, 0, 0]


def test_change_colot_as_list():
    color = convert_to_RJB("(0,0,0)")
    assert color == [0, 0, 0]
