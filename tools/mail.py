# coding: latin-1

##http://code.activestate.com/recipes/473810/ (r1)
# Send an HTML email with an embedded image and a plain text message for
# email clients that don't want to display the HTML.
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_html_mail(_server, _from, _to, _subject, _html_content, text_content):
    # Create the root message and fill in the from, to, and subject headers
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = _subject
    msgRoot['From'] = _from
    msgRoot['To'] = _to
    
    # Encapsulate the plain and HTML versions of the message body in an
    # 'alternative' part, so message agents can decide which they want to display.
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)
    
    msgText = MIMEText(text_content)
    msgAlternative.attach(msgText)
    
    msgText = MIMEText(_html_content, 'html')
    msgAlternative.attach(msgText)
    
    # Send the email 
    smtp = smtplib.SMTP(_server)
    smtp.sendmail(_from, _to, msgRoot.as_string())
    smtp.quit()


def send_text_mail(_server, _from, _to, _subject, _text_content):
    msg = MIMEText(_text_content)
    msg['Subject'] = _subject
    msg['From'] = _from
    msg['To'] = _to

    smtp = smtplib.SMTP(_server)
    smtp.sendmail(_from, [_to], msg.as_string())
    smtp.quit()



