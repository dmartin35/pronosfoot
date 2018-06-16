"""
latin-1 escaping module
"""

def escape_accent(mystr):
    """
    escape the following accented character(s) (e/i) into non-accented equivalent
    """

    mystr = mystr.replace('\xc3\xa9','e') # e acute
    mystr = mystr.replace('\xc3\x89','e') # capital e acute

    mystr = mystr.replace('\xc3\xae', 'i')  # i circumflex

    return mystr