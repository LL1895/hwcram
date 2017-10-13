from xadmin.plugins.actions import BaseActionView
from account.models import Account
from vpc.tasks import createip_task

#class CreateipAction(BaseActionView):
class CreateipAction(BaseActionView):
    action_name = 'create_ip' #相当于这个 Action 的唯一标示, 尽量用比较针对性的名字
    description = '创建所选的 创建IP' #描述, 出现在 Action 菜单中, 可以使用 ``%(verbose_name_plural)s`` 代替 Model 的名字.

    model_perm = 'change' #该 Action 所需权限
    icon = 'fa fa-tasks' #图标:tasks

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

                if obj.region == 'cn-north-1':
                    iproject_id = list(map(lambda x: x.pidcn_north_1,account_data))
                    itoken = list(map(lambda x: x.tokencn_north_1,account_data))

                if obj.region == 'cn-east-2':
                    iproject_id = list(map(lambda x: x.pidcn_east_2,account_data))
                    itoken = list(map(lambda x: x.tokencn_east_2,account_data))

                if obj.region == 'cn-south-1':
                    iproject_id = list(map(lambda x: x.pidcn_south_1,account_data))
                    itoken = list(map(lambda x: x.tokencn_south_1,account_data))

                createip_task.delay(obj.id,obj.account_name,iaccount_id[0],itoken[0],obj.region,iproject_id[0],obj.publicip_type,obj.bandwidth_share_type,obj.publicip,obj.bandwidth_name,obj.bandwidth_size,obj.bandwidth_share_id,obj.bandwidth_charge_mode)

            self.message_user("成功执行 %s 个创建IP的动作，请多次刷新查看创建结果，每条目保留24小时，如需留存，请导出" % n,'success')
