from django.db      import models

from account.views  import Account


class MNFCTCompany(models.Model):
    mnfct_company = models.CharField(max_length=30)

    class Meta:
        db_table = 'MNFCT_company'


class ModelGroup(models.Model):
    mnfct_company = models.ForeignKey(MNFCTCompany, on_delete=models.CASCADE)
    model_group   = models.CharField(max_length=30)

    class Meta:
        db_table = 'model_group_TYPE'


class ModelCategory(models.Model):
    model_group = models.ForeignKey(ModelGroup, on_delete=models.CASCADE)
    model_category = models.CharField(max_length=30)

    class Meta:
        db_table = 'model_category_TYPE'


class ModelInformation(models.Model):
    model_categoty    = models.ForeignKey(ModelCategory, on_delete=models.CASCADE)
    account_id        = models.ForeignKey(Account, on_delete=models.CASCADE)
    model_name_ko     = models.CharField(max_length=30, null=True)
    model_name_en     = models.CharField(max_length=30)
    purchase_paid     = models.IntegerField(default=0, null=True)
    purchase_date     = models.DateField(null=True)
    purchase_location = models.CharField(max_length=30, null=True)
    grnt_period       = models.DateField(null=True)
    serial_number     = models.CharField(max_length=30)
    created_at        = models.DateTimeField(auto_now_add=True)
    updated_ad        = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'model_information'


class GRNTImage(models.Model):
    model_information = models.ForeignKey(ModelInformation, on_delete=models.CASCADE)
    grnt_image        = models.URLField(max_length=200)

    class Meta:
        db_table = 'grnt_image'


class ReceiptImage(models.Model):
    model_information = models.ForeignKey(ModelInformation, on_delete=models.CASCADE)
    receipt_image     = models.URLField(max_length=200)

    class Meta:
        db_table = 'receipt_image'
        

class SVCInformation(models.Model):
    mnfct_company = models.ForeignKey(MNFCTCompany, on_delete=models.CASCADE)
    svc_name      = models.CharField(max_length=30)
    svc_contact   = models.CharField(max_length=30)
    svc_address   = models.CharField(max_length=100)
    svc_image     = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'svc_information'
