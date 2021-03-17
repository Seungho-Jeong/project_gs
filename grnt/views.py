import json

from django.shortcuts   import render
from django.views       import View
from django.http        import JsonResponse
from django.db          import transaction

from datetime           import datetime, timedelta
from dateutil.relativedelta import relativedelta

from account.decorator  import login_decorator
from account.models     import Account
from .models            import (
    MNFCTCompany,
    ModelGroup,
    ModelCategory,
    ModelInformation,
    GRNTImage,
    ReceiptImage,
    SVCInformation
)
# Create your views here.

class GRNTInformation(View):

    @login_decorator
    def post(self, request):

        try:
            data = json.loads(request.body)

            if not Account.objects.filter(id=request.account.id):
                return JsonResponse({"message": "no_information_account"}, stauts=401)

            guarantee_start_date = datetime.strptime(data['purchase_date'], '%Y-%m-%d')
            guarantee_end_date   = guarantee_start_date + relativedelta(years=2) + timedelta(days=-1)
            data['grnt_period']  = guarantee_end_date

            with transaction.atomic():
                ModelInformation.objects.create(
                    account_id        = request.account.id,
                    model_category_id = data['model_category_id'],
                    model_name_ko     = data['model_name_ko'],
                    model_name_en     = data['model_name_en'],
                    purchase_paid     = data['purchase_paid'],
                    purchase_date     = data['purchase_date'],
                    purchase_location = data['purchase_location'],
                    grnt_period       = data['grnt_period'],
                    serial_number     = data['serial_number']
                )
                return JsonResponse({"message": "success"}, status=201)

        except KeyError as e:
            return JsonResponse({"message": "key_error: {}".format(e)}, status=400)
        except Exception as e:
            return JsonResponse({"message": "error: {}".format(e)}, status=400)

    @login_decorator
    def get(self, request, model_information_id):

        try:
            this_model = ModelInformation.objects.get(id=model_information_id)

            if request.account is False:
                return JsonResponse({"message": "unauthorization"}, status=401)

            if request.account.is_master is True:
                request.account.id = this_model.account_id

            if request.account.id is not this_model.account_id:
                return JsonResponse({"message": "unauthorization"}, status=401)

            information_detail = {
                "model_category_id": this_model.model_category_id,
                "model_name_ko"    : this_model.model_name_ko,
                "model_name_en"    : this_model.model_name_en,
                "purchase_paid"    : this_model.purchase_paid,
                "purchase_location": this_model.purchase_location,
                "purchase_date"    : this_model.purchase_date,
                "grnt_period"      : this_model.grnt_period,
                "serial_number"    : this_model.serial_number,
                "created_at"       : this_model.created_at,
                "updated_at"       : this_model.updated_at
            }
            return JsonResponse({"message": "success", "detail": information_detail}, status=200)

        except ModelInformation.DoesNotExist:
            return JsonResponse({"message": "no_exist_information"}, status=400)
        except KeyError as e:
            return JsonResponse({"message": "keyerror: {}".format(e)}, status=400)
        except Exception as e:
            return JsonResponse({"message": "error: {}".format(e)}, status=400)

    @login_decorator
    def put(self, request, model_information_id):

        try:
            data = json.loads(request.body)
            this_model = ModelInformation.objects.get(id=model_information_id)

            if request.account is False:
                return JsonResponse({"message": "unauthorization"}, status=401)

            if request.account.is_master is True:
                request.account.id = this_model.account_id

            if request.account.id is not this_model.account_id:
                return JsonResponse({"message": "unauthorization"}, status=401)

            guarantee_start_date = datetime.strptime(data['purchase_date'], '%Y-%m-%d')
            guarantee_end_date   = guarantee_start_date + relativedelta(years=2) + timedelta(days=-1)
            data['grnt_period']  = guarantee_end_date

            with transaction.atomic():
                ModelInformation.objects.filter(id = model_information_id).update(
                    model_category_id=data['model_category_id'],
                    model_name_ko=data['model_name_ko'],
                    model_name_en=data['model_name_en'],
                    purchase_paid=data['purchase_paid'],
                    purchase_date=data['purchase_date'],
                    purchase_location=data['purchase_location'],
                    grnt_period=data['grnt_period'],
                    serial_number=data['serial_number']
                )
                return JsonResponse({"message": "success"}, status=200)

        except KeyError as e:
            return JsonResponse({"message": "key_error: {}".format(e)}, status=400)
        except Exception as e:
            return JsonResponse({"message": "error: {}".format(e)}, status=400)