import base64
import os
import re
import time

import util.cryptography
from linkr import db


def _generate_api_key():
    """
    Generate a random API key.

    :return: A random alphanumeric string.
    """
    return re.sub('(\W\D)+', '', base64.b64encode(os.urandom(32)))


class User(db.Model):
    """
    Model representing a registered user.
    """

    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    is_admin = db.Column(db.Boolean, index=True, default=False)
    signup_time = db.Column(db.Integer)
    signup_ip = db.Column(db.Text)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.Text)
    api_key = db.Column(db.String(64), index=True)

    def __init__(
        self,
        username,
        password,
        signup_ip,
        is_admin=False,
    ):
        self.signup_time = int(time.time())
        self.signup_ip = signup_ip
        self.username = username
        self.password_hash = util.cryptography.secure_hash(password)
        self.generate_new_api_key()
        self.is_admin = is_admin

    def validate_password(self, password):
        """
        Validate that the supplied password is correct for this user account.

        :param password: The supplied password.
        :return: True if the supplied password matches the user's password; False otherwise.
        """
        return util.cryptography.secure_hash(password) == self.password_hash

    def update_password(self, new_password):
        """
        Set a new password for the user.

        :param new_password: The new plain-text password.
        """
        self.password_hash = util.cryptography.secure_hash(new_password)

    def generate_new_api_key(self):
        """
        Generate a new API key for this user.
        """
        self.api_key = _generate_api_key()

    def as_dict(self):
        """
        Represent this user as a API-friendly, JSON-formatted dictionary.

        :return: A representation of this user's data as a dictionary.
        """
        return {
            'user_id': self.user_id,
            'is_admin': self.is_admin,
            'signup_time': self.signup_time,
            'signup_ip': self.signup_ip,
            'username': self.username,
            'api_key': self.api_key,
        }

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_anonymous():
        return False

    @staticmethod
    def is_active():
        return True

    def get_id(self):
        return unicode(self.user_id)
