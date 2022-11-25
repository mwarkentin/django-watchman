from watchman.decorators import check

@check
def custom_check():
    raise Exception("The answer is 42")
