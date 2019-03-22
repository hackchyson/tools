#!/usr/bin/env python
"""
This module provdies a few string manipulation functions.

>>> is_balanced("(Python (is (not (lisp))))")
True
>>> shorten("The Crossing", 10)
'The Cro...'
>>> simplify(" some    text   with   spurious  whitespace  ")
'some text with spurious whitespace'
"""

import string


def shorten(text, length=25, indicator="..."):
    if len(text) > length:
        text = text[:length - len(indicator)] + indicator
    return text


def simplify(text, whitespace=string.whitespace, delete=""):
    r"""Return the text with muliple spaces reduced to single spaces

    The whitespace parameter is a string of characters, each of which
    is considered to be a space.
    If delete is noe empty it should be a string, in which case any
    characters in the delete string are excluded from the resultant
    string.

    :param text:
    :param whitespace:
    :param delete:
    :return:

    >>> simplify(" this   and\n that\t too")
    'this and that too'
    >>> simplify("  Washington   D.C.\n")
    'Washington D.C.'
    >>> simplify("Washington  D.C.\n", delete=",;:.")
    'Washington DC'
    >>> simplify(" disemvoweled ", delete="aeiou")
    'dsmvwld'
    """

    result = []
    word = ""
    for char in text:
        if char in delete:
            continue
        elif char in whitespace:
            if word:
                result.append(word)
                word = ""
        else:
            word += char
    if word:
        result.append(word)
    return " ".join(result)


def is_balanced(text, brackets="()[]{}<>"):
    """

    :param text:
    :param brackets:
    :return:
    """
    counts = {}
    left_for_right = {}
    for left, right in zip(brackets[::2], brackets[1::2]):
        assert left != right, "the bracket characters must differ"
        counts[left] = 0
        left_for_right[right] = left
    for c in text:
        if c in counts:
            counts[c] += 1
        elif c in left_for_right:
            left = left_for_right[c]
            if counts[left] == 0:
                return False
            counts[left] -= 1
    return not any(counts.values())


if __name__ == "__main__":
    import doctest

    doctest.testmod()
