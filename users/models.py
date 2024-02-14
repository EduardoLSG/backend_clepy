from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from system.models import UUIDModel
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token
from main.helpers import photo_profile_directory_path

# Create your models here.
class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, name, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
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
        
        return self.create_user(name, email, password, **extra_fields)


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
    
    photo_profile   = models.ImageField(_("Photo Profile"), upload_to=photo_profile_directory_path)
    
    
    document        = models.CharField(_("document"), max_length=17, unique=True)
    type_doc        = models.CharField(_("type document"), max_length=1, choices=(("0", "CPF"), ("1", "CNPJ")), null=True, blank=True)
    
    terms_accept    = models.DateTimeField(_("terms_accept"), null=True, blank=True)
    token_firebase  = models.CharField(max_length=64, unique=True, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "phone", "document"]

    objects = CustomUserManager()

    ###DEFAULT
    def __str__(self):
        return f'{self.name} - {self.email}'

    def save(self, *args, **kwargs):
        
        ## Verificação de Documento para determinar seu tipo
        doc = self.document.replace('.', '').replace('-', '').replace('/', '')
        self.type_doc = '0' if len(doc) < 12 else '1'
        
        super().save(*args, **kwargs)
        Token.objects.get_or_create(user=self)
        
        
        
class LocalizationUserModel(UUIDModel):
    
    class Meta:
        verbose_name = _("Endereço")
        verbose_name_plural = _("Endereços")
        
    user          = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    country       = models.CharField(_("Pais"),  max_length=50)
    state         = models.CharField(_("Estado"), max_length=50)
    city          = models.CharField(_("Cidade"), max_length=50)
    district      = models.CharField(_("Bairro"), max_length=50)
    street        = models.CharField(_("Endereço"), max_length=100)
    number        = models.IntegerField(_("Numero"))
    complement    = models.TextField(_("Complemento"), null=True, blank=True)
    reference     = models.TextField(_("Ponto de referência"), null=True, blank=True)
    postal_code   = models.CharField(_("CEP"), max_length=10)
    main          = models.BooleanField(_("Principal"), default=True)