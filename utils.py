import textwrap

def get_int_attr(elm, name):
    return int(elm.get(name, 0))

def print_wrap(str):
    print(textwrap.fill(str, 70))

def print_result(*args):
    res = ''
    for i in range(0, len(args)):
        if i % 2:
            res += '{:<10} '
        else:
            res += '{:<14} '
    print_wrap(res.format(*args))
