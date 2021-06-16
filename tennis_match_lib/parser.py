# -*- coding: utf-8 -*-
"""Parser module provides Parser class and structs to parse tennis match scores.
"""

# pylint: disable=too-few-public-methods

from collections import namedtuple

from tennis_match_lib import common
from tennis_match_lib.constants import TIEBREAK_SCORE_PATTERN
from tennis_match_lib.errors import GameValueError
from tennis_match_lib.rules import LastSet
from tennis_match_lib.structs import BasicMatchStatsInfo, SetScore


ParseResult = namedtuple('ParseResult', ['sets', 'stats_info'])


class Parser:
    """Parser to parse tennis match scores.

    Args:
        score_format (tennis_match_lib.score_format.ScoreFormat): Score format.
        rules (tennis_match_lib.rules.MatchRules): Match rules.
    """

    def __init__(self, score_format, rules):
        self.score_format = score_format
        self.rules = rules

    def parse(self, score):
        """Returns parsed sets and stats info for the given score.

        Args:
            score (str): Tennis match score.

        Returns:
            namedtuple: Parse result with sets and stats info.
        """
        try:
            sets = common.parse_score(score)
        except (TypeError, ValueError) as ex:
            raise GameValueError(f'Invalid game value: {score}: {ex}') from ex
        stats_info = self._calculate_stats_info(sets)
        parse_result = ParseResult(sets=sets, stats_info=stats_info)
        return parse_result

    def _calculate_stats_info(self, sets):
        unit_one_sets, unit_two_sets = self._calculate_sets_count(sets)
        unit_one_games_diff, unit_two_games_diff = self._calculate_games_count(sets)
        return BasicMatchStatsInfo(
            unit_one_sets_diff=(unit_one_sets - unit_two_sets),
            unit_two_sets_diff=(unit_two_sets - unit_one_sets),
            unit_one_games_diff=unit_one_games_diff,
            unit_two_games_diff=unit_two_games_diff,
        )

    @staticmethod
    def _calculate_sets_count(sets):
        sets_winner = [s.unit_one_games > s.unit_two_games for s in sets]
        unit_one_sets = len([x for x in sets_winner if x is True])
        unit_two_sets = len(sets_winner) - unit_one_sets
        return unit_one_sets, unit_two_sets

    def _calculate_games_count(self, sets):
        if len(sets) == self.rules.sets and self.rules.last_set == LastSet.TIEBREAK_SET:
            return self._get_games_diff_when_last_tiebreak_set(sets)
        unit_one_games_diff = self._get_games_diff(sets)
        return unit_one_games_diff, unit_one_games_diff * (-1)

    @staticmethod
    def _get_games_diff(sets):
        return sum(x.unit_one_games for x in sets) - sum(x.unit_two_games for x in sets)

    def _get_games_diff_when_last_tiebreak_set(self, sets):
        unit_one_games_diff = self._get_games_diff(sets[:-1])
        if sets[-1].unit_one_games > sets[-1].unit_two_games:
            unit_one_games_diff += 1
        else:
            unit_one_games_diff -= 1
        return unit_one_games_diff, unit_one_games_diff * (-1)
