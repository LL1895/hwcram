from django.db import models
import datetime
from account.models import Account

# Create your models here.

class Rds(models.Model):
    region_choices = (('cn-north-1','华北1'),('cn-south-1','华南1'),('cn-east-2','华东2'))
    rds_name = models.CharField('实例名称', max_length=128,null=True)
    rds_id = models.CharField('实例ID', max_length=40,null=True)
    rds_status = models.CharField('状态', max_length=20,null=True)
    region = models.CharField('区域', choices=region_choices, max_length=32, default='cn-north-1')
    rds_host = models.GenericIPAddressField('IP地址',null=True)
    rds_port = models.CharField('端口', max_length=10,null=True)
    type_choices = (('master','主实例'),('slave','备实例'),('readreplica','只读实例'))
    rds_type = models.CharField('类型',choices=type_choices,max_length=20,null=True)
    rds_delete_time = models.DateTimeField('删除时间',null=True)
    #master_id = models.CharField('主实例ID', max_length=40,null=True)
    account_name = models.CharField('账户',max_length=20,null=True)
    account = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)

    class Meta:
        verbose_name = "关系型数据库"
        verbose_name_plural = verbose_name
        db_table = "hw_rds"

    def save(self,*args,**kargs):
        utc_time_now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
        delete_time = utc_time_now + datetime.timedelta(hours=10)
        if not self.rds_delete_time:
            self.rds_delete_time = delete_time
        super(Rds,self).save(*args,**kargs)
