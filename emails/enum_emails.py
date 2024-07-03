from enum import Enum

from emails.configs_emails import email_welcome, email_not, email_passwd

class TypeEmail:
    PATH = ''
    METHOD = None
    """Method to config Email
    - email_wecolme
    - email_not
    - email_passwd
    """
    def __init__(self, path: str, method):
        self.PATH=path
        self.METHOD=method
        


class EmailTypeEnum(Enum):
    WELCOME = TypeEmail('welcome', email_welcome)
    NOTIFICATION = TypeEmail('notification', email_not)
    RESET_PASSWORD = TypeEmail('reset_password', email_passwd)
