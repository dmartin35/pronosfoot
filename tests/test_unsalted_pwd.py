import unittest
from django.test import TestCase
from django.contrib.auth import get_user_model
User = get_user_model()


@unittest.skip('Only for Dev purpose  - not to be executed on github/travis')
class UnsaltedPwdTestCase(TestCase):

    def test_unsalted_pwd_users(self):
        """Lists users with unsalted password"""

        # Unsalted MD5/SHA1:
        print(User.objects.filter(password__startswith='md5$$').count())
        print(User.objects.filter(password__startswith='sha1$$').count())
        # Salted MD5/SHA1:
        print(User.objects.filter(password__startswith='md5$').exclude(password__startswith='md5$$').count())
        print(User.objects.filter(password__startswith='sha1$').exclude(password__startswith='sha1$$').count())
        # Crypt hasher:
        print(User.objects.filter(password__startswith='crypt$$').count())

        from django.db.models import CharField
        from django.db.models.functions import Length
        CharField.register_lookup(Length)
        # Unsalted MD5 passwords might not have an 'md5$$' prefix:
        print(User.objects.filter(password__length=32).count())
