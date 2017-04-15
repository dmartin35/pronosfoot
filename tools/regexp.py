"""
REGULAR EXPRESSION TOOLS
"""
import re

def extract_regexp_groups(regexp,string):
    """
    returns all matched groups from string usign given regular expression
    NB: regexp must be provided with group names (?P<group>) 
    """
    valid = re.match(regexp, string)
    if valid:
        return valid.groupdict()