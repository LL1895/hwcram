from django.db import models
import datetime
from account.models import Account
from api.ecs_api import EcsApi

# Create your models here.

class Ecs(models.Model):
    region_choices = (('cn-north-1','华北1'),('cn-south-1','华南1'),('cn-east-2','华东2'))
    ecs_name = models.CharField('主机名称', max_length=128,null=True)
    ecs_id = models.CharField('主机ID', max_length=40, default='c90ab83a-6cdd-4404-8578-05fa965cfb12')
    region = models.CharField('区域', choices=region_choices, max_length=32, default='cn-north-1')
    ecs_shut_time = models.DateTimeField('关机时间',null=True)
    ecs_delete_time = models.DateTimeField('删除时间',null=True)
    ecs_is_active = models.BooleanField('运行中', default=0)
    account_name = models.CharField('账户',max_length=20,null=True)
    account = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    private_ip = models.GenericIPAddressField('私网地址',null=True)
    public_ip = models.GenericIPAddressField('公网地址',null=True)

    class Meta:
        verbose_name = "云主机"
        verbose_name_plural = verbose_name
        db_table = "hw_ecs"

    def save(self,*args,**kargs):
        utc_time_now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
        shut_time = utc_time_now + datetime.timedelta(hours=10)
        delete_time = shut_time + datetime.timedelta(days=7)
        if not (self.ecs_shut_time and self.ecs_delete_time):
            self.ecs_shut_time,self.ecs_delete_time = shut_time,delete_time

        if self.ecs_delete_time <= self.ecs_shut_time:
            self.ecs_delete_time = self.ecs_shut_time + datetime.timedelta(days=7)
        super(Ecs,self).save(*args,**kargs)
