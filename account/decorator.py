import jwt

from django.http import JsonResponse
from my_settings import SECRET_KEY, ALGORITHM
from .models     import Account

def login_decorator(func):

    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)

            if access_token:
                payload = jwt.decode(access_token, SECRET_KEY, algorithms=ALGORITHM)
                request.account   = Account.objects.get(id=payload['user_id'])
                request.is_master = payload['is_master']

            else:
                request.account = False

        except jwt.exceptions.DecodeError:
            return JsonResponse({'MESSAGE': 'INVALID_TOKEN'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=400)

        return func(self, request, *args, **kwargs)
    return wrapper