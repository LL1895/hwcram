from xadmin.plugins.actions import BaseActionView
from vpc.models import VpcApi
from account.models import Account

#class CreateipAction(BaseActionView):
class CreateipAction(BaseActionView):
    action_name = 'create_ip' #相当于这个 Action 的唯一标示, 尽量用比较针对性的名字
    description = '创建所选的 创建IP' #描述, 出现在 Action 菜单中, 可以使用 ``%(verbose_name_plural)s`` 代替 Model 的名字.

    model_perm = 'change' #该 Action 所需权限
    icon = 'fa fa-times' #图标:黑色X

    # 而后实现 do_action 方法
    def do_action(self, queryset):
        # queryset 是包含了已经选择的数据的 queryset
        if not self.has_change_permission:
            raise PermissionDenied

        n = queryset.count()

        if n:
            for obj in queryset:
                account_data = Account.objects.filter(account_name=obj.account_name)
                iaccount_id = list(map(lambda x: x.id,account_data))
                obj.account_id = iaccount_id[0]

                if obj.region == 'cn-north-1':
                    iproject_id = list(map(lambda x: x.pidcn_north_1,account_data))
                    itoken = list(map(lambda x: x.tokencn_north_1,account_data))

                if obj.region == 'cn-east-2':
                    iproject_id = list(map(lambda x: x.pidcn_east_2,account_data))
                    itoken = list(map(lambda x: x.tokencn_east_2,account_data))

                if obj.region == 'cn-south-1':
                    iproject_id = list(map(lambda x: x.pidcn_south_1,account_data))
                    itoken = list(map(lambda x: x.tokencn_south_1,account_data))

                r = VpcApi(itoken[0],obj.region,iproject_id[0]).create_public_ip(obj.publicip_type,obj.bandwidth_share_type,obj.publicip,obj.bandwidth_name,obj.bandwidth_size,obj.bandwidth_share_id,obj.bandwidth_charge_mode)

                if r[1] == 200:
                    obj.publicip_id = r[0]['id']
                    obj.publicip_type = r[0]['type']
                    obj.publicip = r[0]['public_ip_address']
                    obj.create_time = r[0]['create_time']
                    obj.bandwidth_size = r[0]['bandwidth_size']
                    obj.result = str(r[1])
                else:
                    obj.result = str(r[1])

                obj.save()
            self.message_user("成功发送 %s 个创建IP的请求，创建成功后清除条目，创建失败后保留条目" % n,'success')
