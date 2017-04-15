"""
NEWSLETTER
"""
import datetime
import locale
import sys

from django.contrib.auth.models import User

from season.models import Mailing
from admin.mailing.mailer import get_template
from admin.mailing.mailer import html_mail
from admin.mailing.mailer import send_mail
from tools.html_accent import accent_to_html_code

def newsletter(newsfile):
    locale.setlocale(locale.LC_ALL, 'fr_FR')
    now = datetime.datetime.now()
    
    title = 'Newsletter'
    subtitle = '%(month)s %(year)s' % {'month':now.strftime('%B'),'year':now.year}
    subtitle = accent_to_html_code(subtitle)
    
    mail_tpl = get_template('base.html')
    news = get_template(newsfile)

    mailinglist = Mailing.objects.filter(newsletter=True)
    for user in mailinglist:
        user_auth = User.objects.get(pk=user.user_id)
        username = user_auth.username.title()
        email = user_auth.email
        user_news_key = user.news_key
        unsubscribeurl = 'unsubscribe/newsletter/%s-%s-%s' % (username.lower(), email.lower(), user_news_key)
        html_content = html_mail(mail_tpl, 'newsletter', title, subtitle, username, news, unsubscribeurl)
        send_mail(title, email, html_content)
        
def usage():
    print('Usage:')
    print('%s <news_tpl_file>' % sys.argv[0])

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)
        
    newsletter(sys.argv[1])
