"""
newsletter test
"""
import sys
import locale
import datetime

from admin.mailing.mailer import get_template
from admin.mailing.mailer import html_mail
from admin.mailing.mailer import send_mail
from admin.mailing.mailer import FROM

def test_newsletter(newsfile):
    """
    test fake newsletter
    """
    locale.setlocale(locale.LC_ALL, 'fr_FR')
    now = datetime.datetime.now()
    
    title = 'Newsletter'
    subtitle = '%(month)s %(year)s' % {'month':now.strftime('%B'),'year':now.year}
    
    mail_tpl = get_template('base.html')
    news = get_template(newsfile)

    username = 'Test'
    unsubscribeurl = '#' 
    html_content = html_mail(mail_tpl, 'newsletter', title, subtitle, username, news, unsubscribeurl)
    send_mail(title, FROM, html_content)
    
def usage():
    print('Usage:')
    print(('%s <news_tpl_file>' % sys.argv[0]))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)
        
    test_newsletter(sys.argv[1])
