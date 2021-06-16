import pytest

from tennis_match_lib.score_format import ScoreFormat


def test_create_arbitrary_score_format():
    sf = ScoreFormat(' ', '-')
    assert sf.set_sep == ' '
    assert sf.game_sep == '-'


def test_create_with_invalid_set_separator():
    with pytest.raises(ValueError):
        sf = ScoreFormat('_', ':')


def test_create_with_invalid_game_separator():
    with pytest.raises(ValueError):
        sf = ScoreFormat(' ', '\\')
