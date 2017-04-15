#encoding:latin-1
"""
HTML FRENCH ACCENT MODULE
"""
import copy

def accent_to_html_code(str):
    """
    converts most common accented letter
    from french into corresponding html code
    """
    newstr = copy.copy(str)
    newstr = newstr.replace('û','&ucirc;')
    newstr = newstr.replace('ê','&ecirc;')
    newstr = newstr.replace('é','&eacute;')
    newstr = newstr.replace('è','&egrave;')
    newstr = newstr.replace('à','&agrave;')

    newstr = newstr.replace('\xfb','&ucirc;')
    newstr = newstr.replace('\xea','&ecirc;')
    newstr = newstr.replace('\xe9','&eacute;')
    newstr = newstr.replace('\xe8','&egrave;')
    newstr = newstr.replace('\xe0','&agrave;')

    return newstr

if __name__ == '__main__':
    mystr = '_é_è_û_à_ê'
    print(accent_to_html_code(mystr))