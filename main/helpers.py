import uuid
from system.models import ConfigAccessModel, ConfigSysModel


def photo_product_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    filename = f"{uuid.uuid4()}.{filename.split('.')[1]}"
    return f'products/{instance.product.pk}/{filename}'

def photo_profile_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    filename = f"{uuid.uuid4()}.{filename.split('.')[1]}"
    return f'profiles/{instance.pk}/{filename}'



def get_config(name):
    try:
        config = ConfigSysModel.objects.get(name = name)
        return config.value
    
    except:
        return 0


def get_access(name):
    try: 
        access = ConfigAccessModel.objects.get(var=name)
        return access.authorizated

    except:
        return True