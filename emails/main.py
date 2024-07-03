from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from emails.enum_emails import EmailTypeEnum

def send_email(type: EmailTypeEnum, destinatary: str, context:dict = {}):
    """Function to management send emails on system

    Args:
        type (EmailTypeEnum): type of email sended
        destinatary (UserModel): user that will receive email
    """
    template = f"./templates/{type.value.PATH}/index.html"
    print(template)
    email_config = type.value.METHOD
    sub, body_html = email_config(context, template)
    
    message = EmailMultiAlternatives(
        subject=sub,
        body='Email',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[destinatary]
    )
    
    message.attach_alternative(body_html, "text/html")
    message.send(fail_silently=False)
    


from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse

from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    
    number_code = reset_password_token.key.zfill(6)
    
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.name,
        'email': reset_password_token.user.email,
        'code': "{}".format(number_code)
    }
    
    
    send_email(EmailTypeEnum.RESET_PASSWORD, reset_password_token.user.email, context)