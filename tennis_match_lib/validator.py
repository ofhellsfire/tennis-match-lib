from collections import Counter
import re

from tennis_match_lib import common
from tennis_match_lib.rules import LastSet
from tennis_match_lib import validation


class Validator:
    def __init__(self, score_format, rules):
        self.score_format = score_format
        self.rules = rules
        self.re_pattern_raw = self._generate_re_pattern()
        self.re_pattern = re.compile(self.re_pattern_raw)
        self.sets = []

    def validate(self, score):
        return (
            validation.validate_into(str, self._validate_by_regexp(score))
            .and_then(self._validate_number_of_sets)
            .and_then(self._parse_score)
            .and_then(self._validate_number_of_won_sets)
            .and_then(self._validate_games_have_too_small_numbers)
            .and_then(self._validate_games_equality)
        )
        # 1. validate score according to regexp for given format and rules

        # Failure Set Cases:
        # 1. number of sets are in the expected range according to rules
        # 2. number of won sets exceeds number defined in rules

        # Failure Game Cases:
        # 1. both games are less than 6
        # 2. at least one game more than 7 (if not NO_TIEBREAK and TB_SET in last set)
        # 3. both games are equal
        # 4. if one game is 6, then two game is not in range 0..4
        # 5. if two game is 6, then one game is not in range 0..4
        # 6. if one game is 7, then two game is not in range 5..6
        # 7. if two game is 7, then one game is not in range 5..6
        # 8. if one game is 7, two game is 6 and no tiebreak score
        # 9. if two game is 7, one game is 6 and no tiebreak score
        # 10. if tiebreak score can't be parsed to int

    def _generate_re_pattern(self):
        _games = self.rules.games + 1
        _sep = self.score_format.game_sep
        req_set_pattern = f'[0-{_games}]{_sep}[0-{_games}](\\(\\d+\\))?'
        aux_set_pattern = f'( {req_set_pattern})?'
        tb_set_pattern = r'( \d+:\d+)?'
        req_sets = []
        aux_sets = []
        for i in range(self.rules.sets):
            if i <= self.rules.sets // 2:
                req_sets.append(req_set_pattern)
            else:
                aux_sets.append(aux_set_pattern)
        if self.rules.last_set == LastSet.TIEBREAK_SET:
            if aux_sets:
                aux_sets[-1] = tb_set_pattern
            else:
                aux_sets.append(tb_set_pattern)
        return f"{' '.join(req_sets)}{''.join(aux_sets)}"

    def _validate_by_regexp(self, score):
        if not isinstance(score, str) or not self.re_pattern.match(score):
            return validation.Invalid(['Score has invalid format'])
        else:
            return validation.Valid(score)

    def _validate_number_of_sets(self, score):
        sets = score.split(self.score_format.set_sep)
        if len(sets) > self.rules.sets:
            return validation.Invalid(['Number of sets is too large'])
        elif len(sets) < self.rules.sets // 2 + 1:
            return validation.Invalid(['Number of sets is too small'])
        else:
            return validation.Valid(score)

    def _parse_score(self, score):
        try:
            self.sets = common.parse_score(score)
        except Exception:
            return validation.Invalid(['Unable to parse the score'])
        return validation.Valid(score)

    def _validate_number_of_won_sets(self, score):
        won_sets = Counter([s.unit_one_games > s.unit_two_games for s in self.sets])
        required_number_of_sets_to_win = self.rules.sets // 2 + 1
        if (
            won_sets[0] > required_number_of_sets_to_win
            or won_sets[1] > required_number_of_sets_to_win
        ):
            return validation.Invalid(['Number of won sets is too large'])
        else:
            return validation.Valid(score)

    def _validate_games_have_too_small_numbers(self, score):
        for i, s in enumerate(self.sets, 1):
            if (
                self.rules.last_set == LastSet.TIEBREAK_SET
                and i == len(self.sets)
                and s.unit_one_games < self.rules.tb_set_points_to_win
                and s.unit_two_games < self.rules.tb_set_points_to_win
            ) or (s.unit_one_games < self.rules.games and s.unit_two_games < self.rules.games):
                return validation.Invalid(
                    [f'Set {i} has invalid number of games: value is too small']
                )
        return validation.Valid(score)

    def _validate_games_equality(self, score):
        for i, s in enumerate(self.sets, 1):
            if s.unit_one_games == s.unit_two_games:
                return validation.Invalid(
                    [f'Set {i} has invalid number of games: games cannot be equal']
                )
        return validation.Valid(score)

    def _validate_games_have_too_large_numbers(self, score):  ####### incomplete yet
        for i, s in enumerate(self.sets, 1):
            if (
                self.rules.last_set not in (LastSet.TIEBREAK_SET, LastSet.NO_TIEBREAK)
                and i == len(self.sets)
                and s.unit_one_games > self.rules.tb_set_points_to_win + 1
                and s.unit_two_games < self.rules.tb_set_points_to_win + 1
            ) or (
                s.unit_one_games > self.rules.games + 1 or s.unit_two_games > self.rules.games + 1
            ):
                return validation.Invalid(
                    [f'Set {i} has invalid number of games: value is too small']
                )
        return validation.Valid(score)
