from django.template import Library
import contextlib

register = Library()

@register.filter(name='get_range')
def get_range(value, startidx=0):
    """
      Filter - returns a list containing range made from given value
      Usage (in template):
    
      <ul>{% for i in 3|get_range %}
        <li>{{ i }}. Do something</li>
      {% endfor %}</ul>
    
      Results with the HTML:
      <ul>
        <li>0. Do something</li>
        <li>1. Do something</li>
        <li>2. Do something</li>
      </ul>
    
      Instead of 3 one may use the variable set in the views
    """
    return list(range(startidx, value))

@register.filter(name='toint')
def toint(val):
    return int(val)

@register.filter(name='listvalue')
def listvalue(inputlist, valueidx):
    if valueidx < len(inputlist):
        return inputlist[valueidx]
    return None

@register.filter(name='haserrors')
def haserrors(formseterrors):
    if formseterrors:
        for subdict in formseterrors:
            if subdict != {}:
                return True
    return False

@register.filter(name='can_submit_formset')
def can_submit_formset(formset):
    for form in formset:
        if not form.readonly:
            return True
    return False

@register.filter(name='can_submit_form')
def can_submit_form(form):
    return form.readonly == False

@register.filter(name='french_ordinal')
def french_ordinal(value, inflection):
    if value==1:
        if inflection=='m': 
            return '1er'
        elif inflection=='f': 
            return '1re'
        else:
            raise Exception("unknown inflection", inflection)
    else:
        return str(value)+'e'
    
#@register.filter(name='tableline_class')
#def tableline_class(index):
#    if int(index)%2==0:
#        return 'tableline_even'
#    else:
#        return 'tableline_odd'
    
def _listToStr(list):
    str = ''
    if len(list)>0:
        str += '(' 
    for elem in list:
        str += '%s, '%elem
    str += ')'
    #remove last comma
    str = str.replace(', )',')')
    return str

#def _usersForBestStat(users_stats, value, statidx):
#    users = []
#    for tuple in (users_stats):
#        if tuple[statidx] and int(tuple[statidx]) == int(value):
#            user = tuple[0].title()
#            users.append(user)
#    return _listToStr(users)
#
#@register.filter(name='usersForBestTotal')
#def usersForBestTotal(users_stats, stats):
#    return _usersForBestStat(users_stats, stats[0], 1)
#
#@register.filter(name='usersForBestScores')
#def usersForBestScores(users_stats, stats):
#    return _usersForBestStat(users_stats, stats[1], 2)
#
#@register.filter(name='usersForBestIssues')
#def usersForBestIssues(users_stats, stats):
#    return _usersForBestStat(users_stats, stats[2], 3)

@register.filter(name='hasUserForecastForFixture')
def hasUserForecastForFixture(results, fixtureid):
    """
    return True if a result object matches the 
    required fixture id, 
    return False if no forecast is found for the fixture id
    """
    for result in results:
        if result.fixture_id == fixtureid:
            return True
    return False

@register.filter(name='winner')
def winner(fixture, winner):
    """
    returns the bold class name if the winner (home/away)
    is the winner in the fixture result
    """
    iswinner = 'winner'
    isnotwinner = ''
    
    if winner == 'home':
        if ( (fixture.score_a is not None) and 
             (fixture.score_b is not None) and
             (fixture.score_a > fixture.score_b) ):
            return iswinner
    elif winner == 'away':
        if ( (fixture.score_a is not None) and 
             (fixture.score_b is not None) and
             (fixture.score_a < fixture.score_b) ):
            return iswinner
    return isnotwinner

@register.filter(name='getdictvalue')
def getdictvalue(mydict,key):
    if key in mydict:
        return mydict[key]
    else:
        return ''
    
@register.filter(name='has_key')
def has_key(dict,key):
    if key in dict:
        return True
    else:
        return False
    
#@register.filter(name='get_calendar_class')
#def get_calendar_class(dict,key):
#    cal_class = ''
#    if dict.has_key(key):
#        cal_class = dict[key]
#        if cal_class in ['empty', 'half']:
#            cal_class = '%s has_event' % cal_class
#    return cal_class

@register.filter(name='avg_table_line')
def avg_table_line(line):
    pts = line['pts']
    matches = line['matches']
    return '%0.2f' % (float(pts)/float(matches))
    
@register.filter(name='goal_diff')
def goal_diff(value):
    intvalue = int(value)
    if intvalue > 0:
        return '+%d'%intvalue
    return '%d'%intvalue

@register.filter(name='listToComaSepStr')
def listToComaSepStr(list):
    str = ''
    for elem in list:
        str += '%s, '%elem
    #remove last comma and whitespace
    return str[:-2]

@register.filter(name='capFirstAll')
def capFirstAll(list):
    return [val.capitalize() for val in list]

@register.filter(name='notIsNone')
def notIsNone(val):
    return not val is None

@register.filter(name='evoClass')
def evoClass(value):
    try:
        intvalue = int(value)
        if intvalue > 0:
            return 'up'
        elif intvalue == 0:
            return 'same'
        elif intvalue < 0:
            return 'down'
        else:
            return ''
    except:
        return ''

@register.filter(name='movement')
def movement(value):
    """ returns the movement css class"""
    with contextlib.suppress(ValueError, TypeError):
        intvalue = int(value)
        if intvalue > 0:
            return 'up'
        elif intvalue < 0:
            return 'down'
    # any other case
    return 'none'

@register.filter(name='boolToInt')
def boolToInt(val):
    return 1 if val else 0

@register.filter(name='teamTitle')
def teamTitle(title):
    titles = {'winner_midseason':'champion d\'Automne',
              'winner':'champion',
              'second':'dauphin',
              'third':'troisi&egrave;me',
              'fourth':'quatri&egrave;me',
              'fifth': 'cinqui&egrave;me',
              'looser1':'rel&eacute;gu&eacute;s',
              'looser2':'rel&eacute;gu&eacute;s',
              'looser3':'rel&eacute;gu&eacute;s',
              'looser4': 'rel&eacute;gu&eacute;s',
              }
    return titles[title]

@register.filter(name='float_dbledigit')
def float_dbledigit(var):
    try:
        return '%0.2f' % float(var)
    except:
        return var
    
@register.filter(name='int_list')
def int_list(mylist):
    try:
        return [int(x) for x in mylist]
    except:
        return mylist

@register.filter('WDL')
def wdl(value):
    """
    convert win/draw/lose into single char - french localized
    :param value: string
    :return: single char string
    """
    return {'win': 'G', 'draw': 'N', 'lose': 'P'}.get(value)

@register.filter('slice_str')
def slice_string(value, count):
    return str(value)[:int(count)]

@register.filter('is_finished')
def fixture_is_finished(fixture):
    return fixture.score_a is not None and fixture.score_b is not None
