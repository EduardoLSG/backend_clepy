from django.db import models
import uuid
# Create your models here.
class UUIDModel(models.Model):
    """
    Default Model with uuid as primary_key
    """
    
    id   = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4, editable=False)
    
    class Meta:
        abstract = True
        
        
class ConfigAccessModel(models.Model):
    type_var     = models.CharField('tipo variável', max_length=1, choices=(('0', 'Pagina'), ('1', 'Endpoint')), default=0)
    var          = models.CharField('Nome', max_length=255, unique=True)
    var_name     = models.CharField('Nome verificador', max_length=25)
    authorizated = models.BooleanField(verbose_name='Autorização', default=True)
    
    def __str__(self):
        return f'{self.var} -> {str(self.authorizated)}'
    

class ConfigSysModel(models.Model):
    class Meta:
        verbose_name = 'Variável de sistema'
        verbose_name_plural = 'Variáveis de sistema'
    
    name = models.CharField('nome váriavel',max_length=255, unique=True)
    value = models.TextField('valor')

    def __str__(self):
        return self.name