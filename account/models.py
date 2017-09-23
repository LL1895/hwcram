from django.db import models
from api.token_api import TokenApi
import datetime

# Create your models here.

class Account(models.Model):
    account_name = models.CharField('账户名', max_length=20, unique=True)
    user_name = models.CharField('用户名', max_length=20,default='若使用帐户名登录，此项填写账户名')
    password = models.CharField('密码', max_length=20)
    pidcn_north_1 = models.CharField('项目ID-华北1', max_length=40,default='在我的凭证中查看项目列表获取')
    pidcn_east_2 = models.CharField('项目ID-华东2', max_length=40)
    pidcn_south_1 = models.CharField('项目ID-华南1', max_length=40)
    tokencn_north_1 = models.TextField('token-华北1',null=True)
    tokencn_east_2 = models.TextField('Token-华东2',null=True)
    tokencn_south_1 = models.TextField('Token-华南1',null=True)
    token_up_time = models.DateTimeField('Token-有效(UTC)',null=True)

    class Meta:
        verbose_name = "云账户"
        verbose_name_plural = verbose_name
        db_table = "hw_account"

    def save(self,*args,**kargs):
        self.tokencn_north_1 = TokenApi(self.account_name,self.user_name,self.password,'cn-north-1').get_token()
        self.tokencn_east_2 = TokenApi(self.account_name,self.user_name,self.password,'cn-east-2').get_token()
        self.tokencn_south_1 = TokenApi(self.account_name,self.user_name,self.password,'cn-south-1').get_token()
        self.token_up_time = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc) + datetime.timedelta(hours=23)
        super(Account,self).save(*args,**kargs)
