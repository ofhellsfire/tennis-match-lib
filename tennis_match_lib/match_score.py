from collections import OrderedDict
from dataclasses import dataclass

from rules import MatchRules
from score_format import ScoreFormat


class TennisMatchScore2:

    # general given
    unit_one: any
    unit_two: any
    score: str

    # general calculated
    winner: any
    loser: any

    # additional given
    duration: any
    datetime: any
    court_name: any

    # score calculated/parsed
    sets: NSetsMatchScore

    # stats info calculated
    stats_info: TennisMatchBasicStatsInfo

    # aux stats info

    # match rules given: needed only for validation
    rules: MatchRules

    # score format given: needed only for parsing
    score_format: ScoreFormat


class TennisMatchScore:
    def __init__(
        self,
        unit_one,
        unit_two,
        score,
        rules=MatchRules.pro_tour(),
        score_format=ScoreFormat.default(),
        duration=None,
        datetime=None,
        court_name=None,
    ):
        self.unit_one = unit_one
        self.unit_two = unit_two
        self.score = score
        self.rules = rules
        self.score_format = score_format
        self.duration = duration
        self.datetime = datetime
        self.court_name = court_name
        self.sets = None  # TODO
        self.stats_info = None  # TODO

    def _validate(self):
        pass

    def is_unit_one_winner(self):
        pass

    def is_unit_two_winner(self):
        pass


# TODO: case when someone get retired, or walkover
