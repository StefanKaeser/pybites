class RecordScore():
    """Class to track a game's maximum score"""

    def __init__(self):
        self.scores = []

    def __call__(self, score):
        self.scores.append(score)
        return max(self.scores)
