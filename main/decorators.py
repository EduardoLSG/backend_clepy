from .helpers import get_access
from rest_framework.response import Response

def verif_access_page(name):
    def method_wrapper(view_method):
        def wrapper_func(request, *args, **kwargs):
            try:
                if name:
                    access = bool(get_access(name))
                    if not access:
                        raise Exception('Not Permited')

                return view_method(request, *args, **kwargs)
            except Exception as e:
                raise e
        
        return wrapper_func

    return method_wrapper


def allowed_users(allowed_roles=[]):
    
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            try:
                group = None
                print(request.user)
                #checking if user is part of a group
                if request.user.groups.exists():
                    group = request.user.groups.all()[0].name #set group value 
                    
                #checking if the group is in allowed role
                if group in allowed_roles:
                    return view_func(request, *args, **kwargs)
                else:
                    raise Exception('Not Permitted')
            
            except Exception as e:
                raise e
            
        return wrapper_func
    
    return decorator