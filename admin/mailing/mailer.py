"""
MAILING BASE MODULE
"""
import os
import sys

from django.conf import settings

from tools.file import read_file
from tools.log import _log
from tools.mail import send_html_mail, send_text_mail

SERVER = settings.EMAIL_HOST
FROM = settings.EMAIL_HOST_USER

def get_template(filename):
    """
    return html mail template
    """
    current_dir = os.path.dirname(__file__)
    tpl = read_file(os.path.join(current_dir,'templates',filename))
    if not tpl:
        _log('Mailer error: could not load file "%s"'%filename)
        sys.exit(1)
    return tpl

def html_mail(tpl,type,title,subtitle,user,content,unsubscribeurl):
    """
    returns the entire html mail, from given template and infos
    """
    #stores all info to be inserted in the template, 
    #makes sure french accent are converted to their html equivalent
    infos = {'title': title,
             'subtitle': subtitle,
             'user': user,
             'content': content,
             'unsubscribeurl': unsubscribeurl,
             'mailtype': type 
             }
    
    return tpl % infos


def send_mail(object,dest,html_content):
    """
    send to the dest the email with object and html_content 
    """
    send_html_mail(SERVER, FROM, dest, object, html_content, '')
    

def send_mail_plain_text(object, dest, text_content):
    """
    send the plain text email to dest.
    """
    send_text_mail(SERVER, FROM, dest, object, text_content)
