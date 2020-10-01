def get_attack():
    words = "this is a test to test something".split(' ')
    for word in words:
        yield word


def get_defend():
    words = "thou shalt not muzzle the ox".split(' ')
    for word in words:
        yield word


def get_rival():
    words = "as it turns out kili is not wifi enabled".split(' ')
    for word in words:
        yield word
