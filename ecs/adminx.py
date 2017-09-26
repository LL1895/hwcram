import xadmin
from xadmin import views
from import_export import resources
from .models import Ecs
# Register your models here.

class GlobalSetting(object):
    site_title = '云资源自动管理V1.2.0'
    site_footer = 'V1.2.0'

class EcsImportResource(resources.ModelResource):
    class Meta:
        model = Ecs
        #fields = ('name', 'description',)
        exclude = ('account')

class EcsExportResource(resources.ModelResource):
    class Meta:
        model = Ecs
        #fields = ('name', 'description',)
        exclude = ('account')

@xadmin.sites.register(Ecs)
class EcsAdmin(object):
    readonly_fields = ('ecs_name','ecs_id','region','ecs_is_active','account_name','private_ip','public_ip','account')
    list_display =  ['ecs_name', 'private_ip','public_ip','region', 'account_name', 'ecs_shut_time', 'ecs_delete_time', 'ecs_is_active']
    list_filter = ['account_name', 'region']
    search_fields = ['ecs_name','ecs_id','account_name','region','private_ip','public_ip']
    list_per_page = 10
    #list_export = []
    refresh_times = (20,40,60)
    show_detail_fields = []
    #list_editable = ['ecs_shut_time','ecs_delete_time']
    #import_export_args = {'export_resource_class': EcsExportResource}

xadmin.site.register(views.CommAdminView, GlobalSetting)
