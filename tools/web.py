"""
WEB TOOLS
"""
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def get_url_content(url):
    """
    return the content of a URL from the web
    """
    headers = {'User-agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers, verify=False)
    return r.text


if __name__ == '__main__':
    #print get_url_content('http://lfp.fr/iCalendar/ligue1.ics')
    print(get_url_content('http://www.lfp.fr/ligue1/calendrier_resultat#sai=84&jour=1'))