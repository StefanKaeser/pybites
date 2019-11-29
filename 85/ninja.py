scores = [10, 50, 100, 175, 250, 400, 600, 800, 1000]
ranks = "white yellow orange green blue brown black paneled red".split()
BELTS = dict(zip(scores, ranks))


class NinjaBelt:
    def __init__(self, score=0):
        self._score = score
        self._last_earned_belt = None

    def _get_belt(self, new_score):
        """Might be a useful helper"""
        try:
            score_tier = max([score for score in scores if new_score >= score])
        except ValueError:
            return None
        belt = BELTS[score_tier]
        return belt

    def _get_score(self):
        return self._score

    def _set_score(self, new_score):
        if type(new_score) != int:
            raise ValueError("Only integers are allowed as scores.")
        if new_score < self.score:
            raise ValueError(
                f"Can not assign a lower score new_score={new_score}"
                f" than the current one curret_score={self.score}."
            )

        belt = self._get_belt(new_score)
        if belt != self._last_earned_belt:
            self._last_earned_belt = belt
            print(
                f"Congrats, you earned {new_score} points"
                f" obtaining the PyBites Ninja {belt.title()} Belt"
            )
        else:
            print(f"Set new score to {new_score}")
        self._score = new_score

    score = property(_get_score, _set_score)
