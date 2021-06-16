import pytest

from tennis_match_lib import rules
from tennis_match_lib.score_format import ScoreFormat
from tennis_match_lib import validation
from tennis_match_lib.validator import Validator


@pytest.fixture
def match_rules():
    return rules.MatchRules.pro_tour()


@pytest.fixture
def score_format():
    return ScoreFormat.default()


@pytest.fixture
def validator(score_format, match_rules):
    return Validator(score_format, match_rules)


def test_re_pattern_creation_single_set():
    _rules = rules.MatchRules(
        max_sets=rules.SetsCount.ONE,
        games_count=rules.GamesCount.SIX,
        last_set_rule=rules.LastSet.TIEBREAK
    )
    fmt = ScoreFormat.default()
    validator = Validator(score_format=fmt, rules=_rules)
    assert validator.re_pattern_raw == r'[0-7]:[0-7](\(\d+\))?'


def test_re_pattern_creation_three_sets():
    _rules = rules.MatchRules(
        max_sets=rules.SetsCount.THREE,
        games_count=rules.GamesCount.SIX,
        last_set_rule=rules.LastSet.TIEBREAK
    )
    fmt = ScoreFormat.default()
    validator = Validator(score_format=fmt, rules=_rules)
    expected = r'[0-7]:[0-7](\(\d+\))? [0-7]:[0-7](\(\d+\))?( [0-7]:[0-7](\(\d+\))?)?'
    assert validator.re_pattern_raw == expected


def test_re_pattern_creation_five_sets():
    _rules = rules.MatchRules(
        max_sets=rules.SetsCount.FIVE,
        games_count=rules.GamesCount.SIX,
        last_set_rule=rules.LastSet.TIEBREAK
    )
    fmt = ScoreFormat.default()
    validator = Validator(score_format=fmt, rules=_rules)
    expected = (r'[0-7]:[0-7](\(\d+\))? [0-7]:[0-7](\(\d+\))? [0-7]:[0-7](\(\d+\))?'
                r'( [0-7]:[0-7](\(\d+\))?)?( [0-7]:[0-7](\(\d+\))?)?')
    assert validator.re_pattern_raw == expected


def test_re_pattern_creation_three_sets_last_tb_set():
    _rules = rules.MatchRules(
        max_sets=rules.SetsCount.THREE,
        games_count=rules.GamesCount.SIX,
        last_set_rule=rules.LastSet.TIEBREAK_SET
    )
    fmt = ScoreFormat.default()
    validator = Validator(score_format=fmt, rules=_rules)
    expected = r'[0-7]:[0-7](\(\d+\))? [0-7]:[0-7](\(\d+\))?( \d+:\d+)?'
    assert validator.re_pattern_raw == expected


@pytest.mark.parametrize(
    "score",
    [
        '6:4 6:2',
        '2:6 5:7',
        '6:0 6:7(8) 7:5',
        '6:7(0) 7:6(11) 6:7(100)'
    ]
)
def test_valid_score(validator, score):
    assert validator.validate(score) == validation.Valid(score)


@pytest.mark.parametrize(
    "score",
    [
        '6:-1 6:2',
        'just invalid',
        '6:0,6:0',
        '7:5 6:O',
        '8:3 6:2',
        '6:0'
    ]
)
def test_uno_invalid_score(validator, score):
    assert validator.validate(score) == validation.Invalid(
        value=['Score has invalid format']
    )


def test_invalid_score_too_many_sets(validator):
    score = '6:0 6:0 6:2 5:7'
    assert validator.validate(score) == validation.Invalid(
        value=['Number of sets is too large']
    )


def test_invalid_score_too_many_won_sets_one(validator):
    score = '6:0 6:0 6:2'
    assert validator.validate(score) == validation.Invalid(
        value=['Number of won sets is too large']
    )


def test_invalid_score_too_many_won_sets_two(validator):
    score = '4:6 3:6 4:6'
    assert validator.validate(score) == validation.Invalid(
        value=['Number of won sets is too large']
    )


def test_invalid_score_small_number_of_games_uno(validator):
    score = '4:5 6:7(8)'
    assert validator.validate(score) == validation.Invalid(
        value=['Set 1 has invalid number of games: value is too small']
    )


def test_invalid_score_small_number_of_games_dos(validator):
    score = '3:6 0:1'
    assert validator.validate(score) == validation.Invalid(
        value=['Set 2 has invalid number of games: value is too small']
    )


def test_invalid_score_small_number_of_games_tres(validator):
    score = '3:6 6:1 3:2'
    assert validator.validate(score) == validation.Invalid(
        value=['Set 3 has invalid number of games: value is too small']
    )


def test_invalid_score_small_number_of_games_for_no_tb_set():
    _rules = rules.MatchRules(
        max_sets=rules.SetsCount.THREE,
        games_count=rules.GamesCount.SIX,
        last_set_rule=rules.LastSet.TIEBREAK_SET
    )
    fmt = ScoreFormat.default()
    validator = Validator(score_format=fmt, rules=_rules)
    score = '3:6 6:1 4:6'
    assert validator.validate(score) == validation.Invalid(
        value=['Set 3 has invalid number of games: value is too small']
    )


def test_invalid_score_equal_games(validator):
    score = '3:6 6:6 6:2'
    assert validator.validate(score) == validation.Invalid(
        value=['Set 2 has invalid number of games: games cannot be equal']
    )
