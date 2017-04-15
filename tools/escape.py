"""
latin-1 escaping module
"""

def escape_accent(mystr):
    """
    escape the following character(s): e acute -> e
    """

    mystr = mystr.replace('\xc3\xa9','e') # e acute
    mystr = mystr.replace('\xc3\x89','e') # capital e acute

    return mystr