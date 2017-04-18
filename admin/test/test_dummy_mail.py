"""
dummy/fake mail test
"""
import pytest
from admin.mailing.mailer import send_mail_plain_text
from admin.mailing.mailer import FROM


@pytest.mark.skip(reason='Not valid for pytest')
def test_dummy_mail():

    title = 'Dummy'
    content = '*** FAKE CONTENT ***'

    # sends to sender himself
    send_mail_plain_text(title, FROM, content)


if __name__ == '__main__':
    test_dummy_mail()
