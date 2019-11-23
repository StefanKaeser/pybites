class Animal:
    
    _count = 10000
    _animals = []

    def __init__(self, name):
        self.name = name

        # Explicitly access class variable to increase (re-set)
        type(self)._count += 1
        self.number = self._count

        self._animals.append(self)

    def __str__(self):
        return f"{self.number}. {self.name.capitalize()}"

    @classmethod
    def zoo(cls):
        return "\n".join([str(animal) for animal in cls._animals])
