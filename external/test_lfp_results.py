import logging
logging.basicConfig()

from external.lfp_results import parse_results_page
from external.lfp_api import get_score

#html = open('lfp_84_01.html', 'r').read()
#res = parse_results_page(html)
#print(res)
# Test: OK

print(get_score(1,'Bastia', 'Paris'))
print(get_score(1,'Monaco', 'Guimgamp'))
print(get_score(1,'Montpellier', 'Angers'))