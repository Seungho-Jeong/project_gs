from django.db import models

# Create your models here.
class AccountStatus(models.Model):
    account_status = models.CharField(max_length=30)

    class Meta:
        db_table = 'account_status_TYPE'


class Account(models.Model):
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=30)
    address = models.CharField(max_length=100, null=True)
    profile_image = models.URLField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_master = models.BooleanField(default=False)
    account_status = models.ForeignKey(AccountStatus, on_delete=models.CASCADE, default=1)

    class Meta:
        db_table = 'account'
