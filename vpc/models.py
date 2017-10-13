from django.db import models
from account.models import Account
from api.vpc_api import VpcApi

# Create your models here.

class Vpc(models.Model):
    publicip_id = models.CharField('弹性IP-ID', max_length=40,null=True)
    publicip_status = models.CharField('状态', max_length=20,null=True)
    iptype_choices = (('5_bgp','动态BGP'),('5_sbgp','静态BGP'))
    publicip_type = models.CharField('IP类型',choices=iptype_choices,max_length=10,null=True)
    publicip = models.GenericIPAddressField('弹性IP',null=True)
    privateip = models.GenericIPAddressField('私有IP',null=True)
    project_id = models.CharField('项目ID', max_length=40,null=True)
    #create_time = models.CharField('创建时间(UTC)', max_length=40,null=True)
    create_time = models.DateTimeField('创建时间',null=True)
    bandwidth_id = models.CharField('带宽ID', max_length=40,null=True)
    bandtype_choices = (('WHOLE','共享'),('PER','独享'))
    bandwidth_type = models.CharField('带宽类型', choices=bandtype_choices,max_length=10,null=True)
    bandwidth_size = models.IntegerField('带宽大小',null=True)
    bandwidth_name = models.CharField('带宽名称', max_length=128,null=True)
    account = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    account_name = models.CharField('账户',max_length=20,null=True)
    region_choices = (('cn-north-1','华北1'),('cn-east-2','华东2'),('cn-south-1','华南1'))
    region = models.CharField('区域', choices=region_choices, max_length=32, default='cn-north-1')

    class Meta:
        verbose_name = "弹性IP"
        verbose_name_plural = verbose_name
        db_table = "hw_vpc"

class Createip(models.Model):
    publicip_id = models.CharField('弹性IP-ID', max_length=40,null=True)
    iptype_choices = (('5_bgp','动态BGP'),('5_sbgp','静态BGP'))
    publicip_type = models.CharField('IP类型',choices=iptype_choices,max_length=10,null=True,help_text="<font color='red'>* 为必填项</font>")
    publicip = models.GenericIPAddressField('弹性IP',null=True,blank=True,help_text='指定ip地址创建，留空则随机创建ip')
    #create_time = models.CharField('创建时间(UTC)', max_length=40,null=True)
    create_time = models.DateTimeField('创建时间',null=True)
    bandtype_choices = (('WHOLE','共享'),('PER','独享'))
    bandwidth_share_type = models.CharField('带宽类型', choices=bandtype_choices,max_length=10,null=True)
    bandwidth_share_id = models.CharField(
        '共享带宽ID',
        max_length=40,
        null=True,
        blank=True,
        help_text="<font color='blue'>独享带宽留空</font>，<font color='red'>共享带宽填写</font>",
    )
    bandwidth_size = models.IntegerField(
        '带宽大小',
        null=True,
        blank=True,
        help_text="<font color='blue'>独享带宽，填写数字，范围1~300M</font>，<font color='red'>共享带宽留空</font>",
    )
    bandwidth_name = models.CharField(
        '带宽名称',
        max_length=128,
        null=True,
        blank=True,
        help_text="<font color='blue'>独享带宽填写</font>，<font color='red'>共享带宽留空</font>",
    )
    bandwidth_charge_choices = (('traffic','按流量计费'),('bandwidth','按带宽计费'))
    bandwidth_charge_mode = models.CharField(
        '带宽计费方式',
        choices=bandwidth_charge_choices,
        blank=True,
        null=True,
        max_length=10,
        help_text="<font color='blue'>独享带宽填写</font>，<font color='red'>共享带宽留空</font>",
    )
    account = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    account_name = models.CharField('账户',max_length=20,null=True,help_text='填写云账户中已经配置的帐户名')
    region_choices = (('cn-north-1','华北1'),('cn-east-2','华东2'),('cn-south-1','华南1'))
    region = models.CharField('区域', choices=region_choices, max_length=32,null=True)
    result_choices = (('1','参数错误，带宽名称，大小，计费方式，必须填写，请修改'),('2','参数错误，共享带宽ID必须填写，请在弹性IP页面查找ID，请修改'),('200','IP创建成功，请验证IP及带宽'),('409','IP地址已被占用，创建失败'),('400','参数错误，请检查填写项'))
    result = models.CharField('创建结果', choices=result_choices, max_length=128,null=True)

    class Meta:
        verbose_name = "创建IP"
        verbose_name_plural = verbose_name
        db_table = "hw_createip"

#    def save(self,*args,**kargs):
#        account_data = Account.objects.filter(account_name=self.account_name)
#        iaccount_id = list(map(lambda x: x.id,account_data))
#        self.account_id = iaccount_id[0]
#
#        if self.region == 'cn-north-1':
#            iproject_id = list(map(lambda x: x.pidcn_north_1,account_data))
#            itoken = list(map(lambda x: x.tokencn_north_1,account_data))
#
#        if self.region == 'cn-east-2':
#            iproject_id = list(map(lambda x: x.pidcn_east_2,account_data))
#            itoken = list(map(lambda x: x.tokencn_east_2,account_data))
#
#        if self.region == 'cn-south-1':
#            iproject_id = list(map(lambda x: x.pidcn_south_1,account_data))
#            itoken = list(map(lambda x: x.tokencn_south_1,account_data))
#
#        r = VpcApi(itoken[0],self.region,iproject_id[0]).create_public_ip(self.publicip_type,self.bandwidth_share_type,self.publicip,self.bandwidth_name,self.bandwidth_size,self.bandwidth_share_id,self.bandwidth_charge_mode)
#
#        if r[1] == 200:
#            self.publicip_id = r[0]['id']
#            self.publicip_type = r[0]['type']
#            self.publicip = r[0]['public_ip_address']
#            self.create_time = r[0]['create_time']
#            self.bandwidth_size = r[0]['bandwidth_size']
#            self.result = str(r[1])
#        else:
#            self.result = str(r[1])
#
#        super(Createip,self).save(*args,**kargs)
