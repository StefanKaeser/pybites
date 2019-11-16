from functools import singledispatch

@singledispatch
def count_down(data_type):
    raise ValueError
    
@count_down.register(int)
@count_down.register(float)
@count_down.register(str)
def _(data_type):
    data_type = str(data_type)
    for _ in data_type[:]:
        print(data_type)
        data_type = data_type[:-1]

@count_down.register(list)
@count_down.register(tuple)
@count_down.register(dict)
@count_down.register(set)
@count_down.register(range)
def _(data_type):
    data_type = [str(ele) for ele in data_type]
    for _ in data_type[:]:
        print("".join(data_type))
        data_type = data_type[:-1]
