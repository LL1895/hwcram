from django.db import models
from account.models import Account
from api.vpc_api import VpcApi

# Create your models here.

class Vpc(models.Model):
    publicip_id = models.CharField('弹性IP-ID', max_length=40,null=True)
    publicip_status = models.CharField('状态', max_length=20,null=True)
    iptype_choices = (('5_bgp','动态'),('5_sbgp','静态'))
    publicip_type = models.CharField('IP类型',choices=iptype_choices,max_length=10,null=True)
    publicip = models.GenericIPAddressField('弹性IP',null=True)
    privateip = models.GenericIPAddressField('私有IP',null=True)
    project_id = models.CharField('项目ID', max_length=40,null=True)
    create_time = models.CharField('创建时间', max_length=40,null=True)
    bandwidth_id = models.CharField('带宽ID', max_length=40,null=True)
    bandtype_choices = (('WHOLE','共享'),('PER','独享'))
    bandwidth_type = models.CharField('带宽类型', choices=bandtype_choices,max_length=10,null=True)
    bandwidth_size = models.IntegerField('带宽大小',null=True)
    bandwidth_name = models.CharField('带宽名称', max_length=128,null=True)
    account = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    account_name = models.CharField('账户',max_length=20,null=True)
    region_choices = (('cn-north-1','华北1'),('cn-south-1','华南1'),('cn-east-2','华东2'))
    region = models.CharField('区域', choices=region_choices, max_length=32, default='cn-north-1')

    class Meta:
        verbose_name = "弹性IP"
        verbose_name_plural = verbose_name
        db_table = "hw_vpc"

#    def save(self,*args,**kargs):
#        self.tokencn_north_1 = TokenApi(self.account_name,self.user_name,self.password,'cn-north-1').get_token()
#        self.tokencn_east_2 = TokenApi(self.account_name,self.user_name,self.password,'cn-east-2').get_token()
#        self.tokencn_south_1 = TokenApi(self.account_name,self.user_name,self.password,'cn-south-1').get_token()
#        self.token_up_time = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc) + datetime.timedelta(hours=23)
#        super(Account,self).save(*args,**kargs)
