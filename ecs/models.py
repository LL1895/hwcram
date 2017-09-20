from django.db import models
import datetime
from account.models import Account

# Create your models here.
class Ecs(models.Model):
    region_choices = (('cn-north-1','华北1'),('cn-south-1','华南1'),('cn-east-2','华东2'))
    ecs_name = models.CharField('主机名称', max_length=128, default='例：dwx411174_test')
    ecs_id = models.CharField('主机ID', max_length=40, unique=True, default='例：c90ab83a-6cdd-4404-8578-05fa965cfb12')
    region = models.CharField('区域', choices=region_choices, max_length=32, default='cn-north-1')
    ecs_shut_time = models.DateTimeField('关机时间',null=True)
    ecs_delete_time = models.DateTimeField('删除时间',null=True)
    ecs_status_tag = models.BooleanField('运行中', default=0)
    account_name = models.CharField('账户',max_length=20,null=True)
    #account_name = models.ForeignKey(Account,on_delete=models.CASCADE)

    class Meta:
        verbose_name = "云主机"
        verbose_name_plural = verbose_name
        db_table = "hw_ecs"

    def save(self,*args,**kargs):
        if self.ecs_delete_time <= self.ecs_shut_time:
            self.ecs_delete_time = self.ecs_shut_time + datetime.timedelta(days=7)
        super(Ecs,self).save(*args,**kargs)
