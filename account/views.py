import json
import jwt
import re
import bcrypt
import my_settings

from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.views import View

from .models import AccountStatus, Account

# Create your views here.

class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if Account.objects.filter(email=data['email']).exists():
                return JsonResponse({"message": "exists_email"}, status=400)

            if Account.objects.filter(phone_number=data['phone_number']).exists():
                return JsonResponse({"message": "exists_phone_number"})

            if not re.match('^01([016789])([0-9]{3,4})([0-9]{4})$', data['phone_number']):
                return JsonResponse({"MESSAGE": "not_in_form(phone_number)"}, status=400)

            if not re.match('^[a-zA-Z0-9]([-_.]?[a-zA-Z0-9])*@[a-zA-Z0-9]([-_.]?[a-zA-Z0-9])*.[a-zA-Z]{2,}$',
                            data['email']):
                return JsonResponse({"MESSAGE": "not_in_form(email)"}, status=400)

            with transaction.atomic():
                hashed_password = bcrypt.hashpw(data['password'].encode('UTF-8'), bcrypt.gensalt())
                Account.objects.create(
                    email=data['email'],
                    password=hashed_password.decode('UTF-8'),
                    phone_number=data['phone_number'],
                    address=data['address'],
                    profile_image=data['profile_image'],
                    is_master=data['is_master'],
                    account_status_id=data['account_status_id']
                )
                return JsonResponse({"message": "success"}, status=201)
        except KeyError as e:
            return JsonResponse({"message": "key_error: {}".format(e)}, status=400)
        except Exception as e:
            return JsonResponse({"message": "error: {}".format(e)}, status=400)

class SignInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            account = Account.objects.get(email=data['email'])
            user_id = account.id
            is_master = account.is_master

            if not bcrypt.checkpw(data['password'].encode('UTF-8'), account.password.encode('UTF-8')):
                return JsonResponse({"message": "wrong_password"}, status=401)

            access_token = jwt.encode({
                'user_id'  : user_id,
                'is_master': is_master
            }, my_settings.SECRET_KEY, algorithm=my_settings.ALGORITHM)

            return JsonResponse({"message": "success", "Authorization": access_token}, status=200)
        except Account.DoesNotExist:
            return JsonResponse({"message": "no_account_information"}, status=400)
        except KeyError as e:
            return JsonResponse({"message": "key_error: {}".format(e)}, status=400)
        except Exception as e:
            return JsonResponse({"message": "error: {}".format(e)}, status=400)