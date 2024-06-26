from django.db import models
from users.models import UserModel
from system.models import UUIDModel
from django.utils.translation import gettext_lazy as _
from main.variables import DECIMAL_PLACES_FIELD, MAX_DIGITS_FIELD, choices_status, StatusProductEnum
from main.helpers import photo_product_directory_path
from django_resized import ResizedImageField

class CategoryModel(UUIDModel):
    
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categorys')
    
    name = models.CharField(_("name"), max_length=50, unique=True)
    active = models.BooleanField(_("active"), default=True)
    
    def __str__(self) -> str:
        return f'{self.name}'
    
    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super().save(*args, **kwargs)

class ProductsActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status  = StatusProductEnum.APPROVED.value)

class ProductModel(UUIDModel):

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    user_owner  = models.ForeignKey(UserModel, on_delete=models.PROTECT, verbose_name=_("User Owner")) 
    name        = models.CharField(_("Name"), max_length=50)
    description = models.TextField(_("Description"))    
    category    = models.ForeignKey(CategoryModel, verbose_name=_('Categorias'), on_delete=models.PROTECT)
    price       = models.DecimalField(_('Price'), max_digits=MAX_DIGITS_FIELD, decimal_places=DECIMAL_PLACES_FIELD)
    model       = models.CharField(_('Model'), max_length=65)
    status      = models.CharField(_('Status'), choices=choices_status, default=StatusProductEnum.WAITING.value, max_length=2, blank=True, null=True)
    weight      = models.FloatField(_("Weight"), null=True, blank=True)
    dimension   = models.CharField(_("Dimension"), max_length=30, default='00x00x00', null=True, blank=True)
    
    #only_actives = ProductsActiveManager()

    def __str__(self) -> str:
        return f'{self.name} - {self.model} | {self.category}: {self.get_status_display()}'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.status = StatusProductEnum.WAITING.value
       
        return super().save(*args, **kwargs)

class PhotoProductModel(UUIDModel):
    
    class Meta:
        verbose_name = _("Photo Product")
        verbose_name_plural = _("Photo Products")

    photo   = ResizedImageField(_("photo"), size=[900, 700], upload_to=photo_product_directory_path)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    order   = models.IntegerField(default=0, blank=True, null=True)
    active  = models.BooleanField(_("active"), default=True)
    
    
    def __str__(self) -> str:
        return f'{self.product.name} | {self.photo.url[-15:]}'
    
    def save(self, *args, **kwargs):
        if not self.order:
            photos = PhotoProductModel.objects.filter(
                product=self.product
            ).order_by('order')
            if not photos:
                self.order = 0
                
            else:
                self.order = photos.last().order + 1
        
        return super().save(*args, **kwargs)       
        