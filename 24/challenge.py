from abc import ABC, abstractmethod


class Challenge(ABC):
    def __init__(self, number, title):
        self.number = number
        self.title = title
    
    @abstractmethod
    def verify(self, value):
        pass

    @property
    def pretty_title(self):
        pass


class BlogChallenge(Challenge):
    def __init__(self, number, title, merged_prs):
        self.merged_prs = merged_prs
        super().__init__(number, title)

    def verify(self, number):
        return number in self.merged_prs

    @property
    def pretty_title(self):
        return f"PCC{self.number} - {self.title}"


class BiteChallenge(Challenge):
    def __init__(self, number, title, result):
        self.result = result
        super().__init__(number, title)

    def verify(self, my_result):
        return self.result == my_result

    @property
    def pretty_title(self):
        return f"Bite {self.number}. {self.title}"

