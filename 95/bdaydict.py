MSG = 'Hey {}, there are more people with your birthday!'


class BirthdayDict(dict):
    """Override dict to print a message every time a new person is added that has
       the same birthday (day+month) as somebody already in the dict"""

    @staticmethod
    def extract_month_day(dt):
        return (dt.month, dt.day)

    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

    def __setitem__(self, name, birthday):
        month_day = self.extract_month_day(birthday)
        has_birthday = any(month_day == self.extract_month_day(birthday) 
                        for birthday in self.values())
    
        if has_birthday:
            print(MSG.format(name))
        super().__setitem__(name, birthday)
