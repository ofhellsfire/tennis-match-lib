# -*- coding: utf-8 -*-
"""Parser module provides Parser class and structs to parse tennis match scores.
"""

# pylint: disable=too-few-public-methods


class ScoreFormat:
    """Score format struct with validation.

    Args:
        set_sep (str): Set separator.
        game_sep (str): Game separator.
    """

    ALLOWED_SET_SEP = (' ',)
    ALLOWED_GAME_SEP = (':', '-', r'/')

    def __init__(self, set_sep, game_sep):
        ScoreFormat._check_set_sep(set_sep)
        ScoreFormat._check_game_sep(game_sep)
        self.set_sep = set_sep
        self.game_sep = game_sep

    @classmethod
    def default(cls):
        """Returns default ScoreFormat instance with ' ' as set separator
        and ':' as game separator.

        Returns:
            ScoreFormat: default score format.
        """
        return cls(set_sep=' ', game_sep=':')

    @staticmethod
    def _check_set_sep(sep):
        if sep not in ScoreFormat.ALLOWED_SET_SEP:
            raise ValueError(f'Invalid set separator: {sep}')

    @staticmethod
    def _check_game_sep(sep):
        if sep not in ScoreFormat.ALLOWED_GAME_SEP:
            raise ValueError(f'Invalid game separator: {sep}')
