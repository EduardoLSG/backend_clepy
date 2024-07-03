import base64
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from emails.enum_emails import EmailTypeEnum
from system.models import UUIDModel
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token
from main.helpers import photo_profile_directory_path
from emails.main import send_email
from email.mime.image import MIMEImage
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

# Create your models here.
class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        email = extra_fields.pop('email', None)
        password = extra_fields.pop('password', '123124')
        name     = extra_fields.pop('name', None)
        extra_fields['photo_profile'] = extra_fields.pop('picture', None)

        if not name:
            name = extra_fields.pop('fullname')

        if not email or not name:
            raise ValueError(_("The Email and Username must be set"))

        email = self.normalize_email(email)
        user = self.model(email=email, name = name, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, name, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        
        extra_fields['name'] = name
        extra_fields['email'] = email
        extra_fields['password'] = password
        
        return self.create_user(**extra_fields)


#USERS
class UserModel(UUIDModel, AbstractBaseUser, PermissionsMixin):
    """
    Class to substitute default base model
    With UUID
    """

    class Meta:
        verbose_name        = _("User")
        verbose_name_plural = _("Users")

    email           = models.EmailField(_("email"), unique=True)
    name            = models.CharField(_('name'), max_length=100)
    
    last_login      = models.DateTimeField(_("last login"), auto_now=True)
    date_joined     = models.DateTimeField(_("date joined"), auto_now_add=True)
    is_staff        = models.BooleanField(_("is staff"), default=False)
    is_active       = models.BooleanField(_("is active"), default=True)
    is_superuser    = models.BooleanField(_('is superuser'), default=False)
    
    phone           = models.CharField(_("Phone"), max_length=19)
    
    photo_profile   = models.FileField(_("Photo Profile"), upload_to=photo_profile_directory_path)
    
    
    document        = models.CharField(_("document"), max_length=17, unique=True, null=True, blank=True)
    type_doc        = models.CharField(_("type document"), max_length=1, choices=(("0", "CPF"), ("1", "CNPJ"), ("9", "--")), null=True, blank=True)
    
    terms_accept    = models.DateTimeField(_("terms_accept"), null=True, blank=True)
    token_firebase  = models.CharField(max_length=64, unique=True, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "phone", "document"]

    objects = CustomUserManager()

    ###DEFAULT
    def __str__(self):
        return f'{self.name} - {self.email}'

    def save(self, *args, **kwargs):
        if self.document == '' or not self.document:
            self.document = None
            self.type_doc = '9'
        
        else:
            ## Verificação de Documento para determinar seu tipo
            doc = self.document.replace('.', '').replace('-', '').replace('/', '')
            self.type_doc = '0' if len(doc) < 12 else '1'

        users = UserModel.objects.filter(id=self.pk)
        send_email_ = False if users.exists() else True
        super().save(*args, **kwargs)
        Token.objects.get_or_create(user=self)

        if send_email_:
            
            subject = 'Assunto do E-mail'
            from_email = settings.EMAIL_HOST_USER
            to_email = self.email
            body = 'Aqui está o PDF que você solicitou.'
            
            with open('./emails/templates/welcome/EMAIL_MARKETING_page-0001.jpg', 'rb') as f:
                image_data = f.read()
            
            # Renderizar o corpo do e-mail em HTML
            html_body = render_to_string('templates/welcome/index.html', {'body': body})

            # Criar o e-mail
            email = EmailMessage(subject, html_body, from_email, [to_email])
            email.content_subtype = 'html'

            # Anexar o PDF
            email.attach_file('./emails/templates/welcome/EMAIL_MARKETING.pdf')
            # Anexar a imagem embutida
            image = MIMEImage(image_data)
            image.add_header('Content-ID', '<imagem_embutida>')
            email.attach(image)

            # Enviar o e-mail
            email.send() 


class LocalizationUserModel(UUIDModel):
    
    class Meta:
        verbose_name = _("Endereço")
        verbose_name_plural = _("Endereços")
        
    user          = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    country       = models.CharField(_("Pais"),  max_length=50, default='BRASIL')
    state         = models.CharField(_("Estado"), max_length=50)
    city          = models.CharField(_("Cidade"), max_length=50)
    postal_code   = models.CharField(_("CEP"), max_length=10)
    district      = models.CharField(_("Bairro"), max_length=50, null=True, blank=True)
    street        = models.CharField(_("Endereço"), max_length=100, null=True, blank=True)
    number        = models.IntegerField(_("Numero"), null=True, blank=True)
    complement    = models.TextField(_("Complemento"), null=True, blank=True)
    reference     = models.TextField(_("Ponto de referência"), null=True, blank=True)
    main          = models.BooleanField(_("Principal"), default=True)