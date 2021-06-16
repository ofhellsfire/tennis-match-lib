import re

from tennis_match_lib.structs import SetScore


DEFAULT_SET_SEPARATOR = ' '
DEFAULT_GAME_SEPARATOR = ':'
TIEBREAK_SCORE_PATTERN = re.compile(r'([(]\d+[)])')


def reverse_score(
    score, set_separator=DEFAULT_SET_SEPARATOR, game_separator=DEFAULT_GAME_SEPARATOR
):
    def _reverse(score):
        a, b = score.split(game_separator)
        return f'{b}{game_separator}{a}'

    split = score.split(set_separator)
    tiebreaks = []
    for _set in split:
        if '(' in _set:
            tiebreaks.append(_set[3:])
        else:
            tiebreaks.append('')
    tbless_score = TIEBREAK_SCORE_PATTERN.sub('', score).split(set_separator)
    return set_separator.join([f'{_reverse(s)}{t}' for s, t in zip(tbless_score, tiebreaks)])


def parse_score(
    score, set_separator=DEFAULT_SET_SEPARATOR, game_separator=DEFAULT_GAME_SEPARATOR
):
    sets = score.split(set_separator)
    return [parse_set(s, game_separator) for s in sets]


def parse_set(
    set_score, set_separator=DEFAULT_SET_SEPARATOR, game_separator=DEFAULT_GAME_SEPARATOR
):
    tb_score = None
    score = set_score
    if TIEBREAK_SCORE_PATTERN.search(set_score):
        tb_score = int(set_score[4:-1])
        score = TIEBREAK_SCORE_PATTERN.sub('', set_score)
    unit_one_games, unit_two_games = [int(game) for game in score.split(game_separator)]
    return SetScore(
        unit_one_games=unit_one_games, unit_two_games=unit_two_games, tiebreak=tb_score
    )
