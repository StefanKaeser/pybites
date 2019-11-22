class RecordScore():
    """Class to track a game's maximum score"""

    def __init__(self):
        self._maxscore = float('-inf')

    def __call__(self, score):
        self._maxscore = max(self._maxscore, score)
        return self._maxscore
