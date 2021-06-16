import pytest

from tennis_match_lib.errors import GameValueError, TiebreakValueError
from tennis_match_lib.score_format import ScoreFormat
from tennis_match_lib.parser import Parser, ParseResult
from tennis_match_lib.rules import MatchRules
from tennis_match_lib.structs import SetScore, BasicMatchStatsInfo


@pytest.fixture
def score_format():
    return ScoreFormat.default()


@pytest.fixture
def parser(score_format):
    return Parser(score_format=score_format, rules=MatchRules.pro_tour())


@pytest.fixture
def parser_club_rules(score_format):
    return Parser(score_format=score_format, rules=MatchRules.club())


def test_positive_uno_without_tiebreak(parser):
    score = '6:4 6:2'
    actual = parser.parse(score)
    expected = ParseResult(
        sets=[
            SetScore(unit_one_games=6, unit_two_games=4),
            SetScore(unit_one_games=6, unit_two_games=2),
        ],
        stats_info=BasicMatchStatsInfo(
            unit_one_sets_diff=2,
            unit_two_sets_diff=-2,
            unit_one_games_diff=6,
            unit_two_games_diff=-6
        )
    )
    assert actual == expected


def test_positive_dos_without_tiebreak(parser):
    score = '5:7 0:6'
    actual = parser.parse(score)
    expected = ParseResult(
        sets=[
            SetScore(unit_one_games=5, unit_two_games=7),
            SetScore(unit_one_games=0, unit_two_games=6),
        ],
        stats_info=BasicMatchStatsInfo(
            unit_one_sets_diff=-2,
            unit_two_sets_diff=2,
            unit_one_games_diff=-8,
            unit_two_games_diff=8
        )
    )
    assert actual == expected


def test_positive_tres_without_tiebreak(parser):
    score = '5:7 6:4 6:2'
    actual = parser.parse(score)
    expected = ParseResult(
        sets=[
            SetScore(unit_one_games=5, unit_two_games=7),
            SetScore(unit_one_games=6, unit_two_games=4),
            SetScore(unit_one_games=6, unit_two_games=2),
        ],
        stats_info=BasicMatchStatsInfo(
            unit_one_sets_diff=1,
            unit_two_sets_diff=-1,
            unit_one_games_diff=4,
            unit_two_games_diff=-4
        )
    )
    assert actual == expected


def test_positive_uno_with_tiebreak(parser):
    score = '6:0 7:6(5)'
    actual = parser.parse(score)
    expected = ParseResult(
        sets=[
            SetScore(unit_one_games=6, unit_two_games=0),
            SetScore(unit_one_games=7, unit_two_games=6, tiebreak=5),
        ],
        stats_info=BasicMatchStatsInfo(
            unit_one_sets_diff=2,
            unit_two_sets_diff=-2,
            unit_one_games_diff=7,
            unit_two_games_diff=-7
        )
    )
    assert actual == expected


def test_positive_dos_with_tiebreak(parser):
    score = '6:7(0) 7:6(10) 6:7(20)'
    actual = parser.parse(score)
    expected = ParseResult(
        sets=[
            SetScore(unit_one_games=6, unit_two_games=7, tiebreak=0),
            SetScore(unit_one_games=7, unit_two_games=6, tiebreak=10),
            SetScore(unit_one_games=6, unit_two_games=7, tiebreak=20),
        ],
        stats_info=BasicMatchStatsInfo(
            unit_one_sets_diff=-1,
            unit_two_sets_diff=1,
            unit_one_games_diff=-1,
            unit_two_games_diff=1
        )
    )
    assert actual == expected


def test_positive_uno_with_tiebreak_set(parser_club_rules):
    score = '6:7(5) 7:5 6:10'
    actual = parser_club_rules.parse(score)
    expected = ParseResult(
        sets=[
            SetScore(unit_one_games=6, unit_two_games=7, tiebreak=5),
            SetScore(unit_one_games=7, unit_two_games=5),
            SetScore(unit_one_games=6, unit_two_games=10),
        ],
        stats_info=BasicMatchStatsInfo(
            unit_one_sets_diff=-1,
            unit_two_sets_diff=1,
            unit_one_games_diff=0,
            unit_two_games_diff=0
        )
    )
    assert actual == expected


def test_positive_dos_with_tiebreak_set(parser_club_rules):
    score = '6:3 1:6 10:2'
    actual = parser_club_rules.parse(score)
    expected = ParseResult(
        sets=[
            SetScore(unit_one_games=6, unit_two_games=3),
            SetScore(unit_one_games=1, unit_two_games=6),
            SetScore(unit_one_games=10, unit_two_games=2),
        ],
        stats_info=BasicMatchStatsInfo(
            unit_one_sets_diff=1,
            unit_two_sets_diff=-1,
            unit_one_games_diff=-1,
            unit_two_games_diff=1
        )
    )
    assert actual == expected


def test_neg_uno_wrong_tiebreak_value(parser):
    score = '6:7(r) 2:6'
    with pytest.raises(GameValueError):
        parser.parse(score)


def test_neg_dos_wrong_game_value(parser):
    score = '6:F 2:6'
    with pytest.raises(GameValueError):
        parser.parse(score)


def test_neg_tres_wrong_game_value(parser):
    score = 'justwrongscore'
    with pytest.raises(GameValueError):
        parser.parse(score)
