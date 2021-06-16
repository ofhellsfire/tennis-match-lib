import enum


class SetsCount(enum.IntEnum):

    ONE = 1
    THREE = 2
    FIVE = 3


class GamesCount(enum.IntEnum):

    FOUR = 1
    SIX = 2


class LastSet(enum.IntEnum):

    TIEBREAK = 1
    TIEBREAK_SET = 2
    NO_TIEBREAK = 3


TIEBREAK_SET_POINTS_TO_WIN = 10


class MatchRules:
    def __init__(
        self,
        max_sets: SetsCount,
        games_count: GamesCount,
        last_set_rule: LastSet,
        tb_set_points_to_win=TIEBREAK_SET_POINTS_TO_WIN,
    ):
        MatchRules._check_max_sets(max_sets)
        MatchRules._check_games_count(games_count)
        self._sets = max_sets
        self._games = games_count
        self.last_set = last_set_rule
        self.tb_set_points_to_win = tb_set_points_to_win

    @classmethod
    def pro_tour(cls):
        return cls(
            max_sets=SetsCount.THREE, games_count=GamesCount.SIX, last_set_rule=LastSet.TIEBREAK
        )

    @classmethod
    def club(cls):
        return cls(
            max_sets=SetsCount.THREE,
            games_count=GamesCount.SIX,
            last_set_rule=LastSet.TIEBREAK_SET,
        )

    @classmethod
    def club_short(cls):
        return cls(
            max_sets=SetsCount.ONE, games_count=GamesCount.SIX, last_set_rule=LastSet.TIEBREAK
        )

    @classmethod
    def grand_slam(cls):
        return cls(
            max_sets=SetsCount.FIVE, games_count=GamesCount.SIX, last_set_rule=LastSet.TIEBREAK
        )

    @property
    def sets(self):
        if self._sets == SetsCount.ONE:
            return 1
        elif self._sets == SetsCount.THREE:
            return 3
        elif self._sets == SetsCount.FIVE:
            return 5
        else:
            raise ValueError(f'Unexpected sets value: {self._max_sets}')

    @property
    def games(self):
        if self._games == GamesCount.FOUR:
            return 4
        elif self._games == GamesCount.SIX:
            return 6
        else:
            raise ValueError(f'Unexpected games value: {self._max_sets}')

    @staticmethod
    def _check_max_sets(sets):
        if sets not in (SetsCount.ONE, SetsCount.THREE, SetsCount.FIVE):
            raise ValueError(f'Invalid sets value: {sets}')

    @staticmethod
    def _check_games_count(games):
        if games not in (GamesCount.FOUR, GamesCount.SIX):
            raise ValueError(f'Invalid games value: {games}')
