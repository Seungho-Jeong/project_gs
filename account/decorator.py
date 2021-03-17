import jwt

from django.http import JsonResponse
from my_settings import SECRET_KEY, ALGORITHM
from .models     import Account

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token  = request.headers.get('Authorization', None)
            accounnt_info = jwt.decode(access_token, SECRET_KEY, algorithm = ALGORITHM)
            acccount_id   = Account.objects.get(id=accounnt_info['account_id'])

            if not acccount_id:
                raise Account.DoesNotExist('not_account_information', 400)

            if acccount_id['account_status'] is 1:
                request.is_master  = acccount_id['is_master']
                request.account_id = account_id['id']

            else:
                request.account_id = False

        except jwt.DecodeError:
            return JsonResponse({"message": "invalid_token"}, status=401)
        except Account.DoesNotExist:
            return JsonResponse({"message": "invaild_account"}, status=400)

        return func(self, request, *args, **kwargs)
    return wrapper()