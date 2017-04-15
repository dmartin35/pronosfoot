"""
- for next match day to come
- send reminder to users that have forecasts not submitted
"""
import datetime
import locale 

from django.contrib.auth.models import User

from season.models import Mailing
from admin.mailing.mailer import get_template
from admin.mailing.mailer import html_mail
from admin.mailing.mailer import send_mail
from season.models import Fixture
from season.models import Forecast
from season.templatetags.generic_tags import french_ordinal
from tools.html_accent import accent_to_html_code


def check_forecasts():
    """
    for next match day to come, send a reminder
    to any user that have missing forecasts 
    """
    locale.setlocale(locale.LC_ALL, 'fr_FR')
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    
    title = 'Rappel'
    subtitle_tpl = '%(week_loc)s journ&eacute;e'

    #load mail templates
    mail_tpl = get_template('base.html')
    reminder_tpl = get_template('reminder.html')
    
    #get the list of fixtures for the following day
    fixtures = Fixture.objects.filter(day=tomorrow).all()
    
    #handles matches of different weeks on the same day
    weeks = {}
    for fixture in fixtures:
        if fixture.week not in weeks:
            weeks[fixture.week] = []
        weeks[fixture.week].append(fixture.id)
    
    #for each week
    for week in list(weeks.keys()):
        week_localized = '%s' % french_ordinal(week, 'f')
        
        subtitle_week = subtitle_tpl % {'week_loc':week_localized}
    
        #for all users that still want the reminder
        mailinglist = Mailing.objects.filter(reminder=True)
        for user in mailinglist:
            user_auth = User.objects.get(pk=user.user_id)
            
            #skip user not active - do not spam
            if not user_auth.is_active:
                continue
            
            username = user_auth.username.title()
            email = user_auth.email
            user_news_key = user.news_key
            
            #check the user has matches without forecast
            #for the current week and tomrrow's date
            number_matches = 0
            for id in weeks[week]:
                res = Forecast.objects.filter(user=user.user_id, fixture=id)
                if len(res) == 0:
                    number_matches = number_matches + 1
                else:
                    #request returns only element
                    forecast = res[0]
                    if forecast.score_a is None and forecast.score_b is None:
                        number_matches = number_matches + 1
            
            if number_matches > 0:
                date_full = tomorrow.strftime('%A %%d %B %Y') % tomorrow.day
                date_full = accent_to_html_code(date_full)
                
                #handle the plural with tailing 'es'
                plural = 'es' if number_matches > 1 else ''
                    
                #insert the custom info for the user in the reminder template
                infos = {'num_matches':number_matches,
                         'plural_es':plural,
                         'date':date_full,
                         'week_loc':week_localized,
                         'week':week,
                         }
                reminder_content = reminder_tpl % infos

                user = username.capitalize()
                unsubscribeurl = 'unsubscribe/reminder/%s-%s-%s' % (username.lower(), email.lower(), user_news_key)
                html_content = html_mail(mail_tpl, 'reminder', title, 
                                         subtitle_week, username, 
                                         reminder_content, unsubscribeurl)
                         
                #send the mail - to the user- for the current week - for tomorrow
                send_mail(title, email, html_content)
