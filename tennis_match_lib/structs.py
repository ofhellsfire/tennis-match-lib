from dataclasses import dataclass


@dataclass
class SetScore:

    unit_one_games: int
    unit_two_games: int
    tiebreak: int = None
    duration = None


@dataclass
class BasicMatchStatsInfo:

    unit_one_sets_diff: int
    unit_two_sets_diff: int
    unit_one_games_diff: int
    unit_two_games_diff: int
