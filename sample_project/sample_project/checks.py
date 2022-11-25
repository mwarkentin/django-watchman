from watchman.decorators import check


def fail_custom_check():
    return {"fail_custom_check": _fail_custom_check()}

@check
def _fail_custom_check():
    raise Exception("The answer is 42")

def ok_custom_check():
    return {"ok_custom_check": _ok_custom_check()}

@check
def _ok_custom_check():
    return {"ok": True}
