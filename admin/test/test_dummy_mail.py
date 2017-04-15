"""
dummy/fake mail test
"""

from admin.mailing.mailer import send_mail_plain_text
from admin.mailing.mailer import FROM


def test_dummy_mail():

    title = 'Dummy'
    content = '*** FAKE CONTENT ***'

    # sends to sender himself
    send_mail_plain_text(title, FROM, content)


if __name__ == '__main__':
    test_dummy_mail()
