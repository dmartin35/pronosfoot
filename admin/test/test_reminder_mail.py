"""
reminder mail test
"""
import sys
import locale
import datetime

from admin.mailing.mailer import get_template
from admin.mailing.mailer import send_mail_plain_text
from admin.mailing.mailer import FROM


def test_reminder():
    locale.setlocale(locale.LC_ALL, 'fr_FR')
    now = datetime.datetime.now()

    title = 'Rappel'
    subtitle = '1ere journee'
    mail_tpl = get_template('reminder.txt')

    username = 'Test'
    unsubscribeurl = '#'

    infos = {
        'num_matches': 3,
        'plural_es': 'es',
        'date': str(now),
        'week_loc': '1ere',
        'week': 1,
        'title': title,
        'subtitle': subtitle,
        'user': username,
        'unsubscribeurl': unsubscribeurl,
    }

    content = mail_tpl % infos

    # sends to sender himself
    send_mail_plain_text(title, FROM, content)


if __name__ == '__main__':
    test_reminder()
