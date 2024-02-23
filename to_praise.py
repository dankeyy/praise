"""extract a user-displayable hash from a raise-failable-entrypoint"""

import os
import sys
import json
import typing
import traceback


def _codepoint_from_exception() -> typing.Optional[tuple]:
    _, _, exc_tb = sys.exc_info()
    stack = traceback.extract_tb(exc_tb)

    if not stack:
        return None

    last_call = stack[-1]
    filename = "./" + os.path.relpath(last_call.filename)
    lineno = str(last_call.lineno)

    scope = ".".join(
        frame.name
        for frame in stack
        if frame.name != "<module>"
        and frame.filename == last_call.filename
    )
    return filename, scope, lineno


def hash_from_exception() -> str:
    """to be used as a library function to get the hash from an exception"""
    codepoint = _codepoint_from_exception()
    try:
        with open("praise.json") as jpraise:
            existing_mapping = json.load(jpraise)
    except FileNotFoundError:
        return "no praise.json found"

    if not codepoint:
        return "no traceback was available, could not extract codepoint"

    codepoint_repr = ':'.join(codepoint)
    return next(
        (k for k,v in existing_mapping.items() if v == codepoint_repr),
        "no match found"
    )


def _test():
    try:
        from example.kapibara import f
        f()
    except Exception:
        print(hash_from_exception())


if __name__ == '__main__':
    _test()
