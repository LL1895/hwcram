import xadmin
from import_export import resources
from .models import Vpc
from .models import Createip
from account.models import Account
from .action import CreateipAction
# Register your models here.
class VpcImportResource(resources.ModelResource):
    class Meta:
        model = Vpc
        #fields = ('name', 'description',)
        #exclude = ('tokencn_north_1','tokencn_east_2','tokencn_south_1','token_up_time')

class VpcExportResource(resources.ModelResource):
    class Meta:
        model = Vpc
        #fields = ('name', 'description',)
        exclude = ('account')

class CreateipImportResource(resources.ModelResource):
    class Meta:
        model = Createip
        #fields = ('name', 'description',)
        exclude = ('publicip_id','create_time','account','result')

class CreateipExportResource(resources.ModelResource):
    class Meta:
        model = Createip
        #fields = ('name', 'description',)
        exclude = ('account')

@xadmin.sites.register(Vpc)
class VpcAdmin(object):
    readonly_fields = (
        'publicip_id',
        'publicip_status',
        'publicip_type',
        'publicip',
        'privateip',
        'project_id',
        'create_time',
        'bandwidth_id',
        'bandwidth_type',
        'bandwidth_size',
        'bandwidth_name',
        'account',
        'account_name',
        'region',
    )

    list_display =  [
        'publicip',
        'publicip_type',
        'publicip_status',
        'privateip',
        'account_name',
        'region',
        'bandwidth_type',
        'bandwidth_size',
        'bandwidth_name',
        'create_time',
    ]

    list_filter = [
        'account_name',
        'region',
        'publicip_type',
        'publicip_status',
        'bandwidth_type',
    ]

    search_fields = [
        'publicip_id',
        'region',
        'publicip',
        'project_id',
        'bandwidth_id',
        'bandwidth_name',
        'account_name'
    ]

    #list_editable =  ['account_name', 'user_name', 'password', 'pidcn_north_1', 'pidcn_east_2', 'pidcn_south_1']

    list_per_page = 10

    #list_export = []

    show_detail_fields = []

    refresh_times = (20,40,60)

    #import_export_args = {'export_resource_class': VpcExportResource}

@xadmin.sites.register(Createip)
class CreateipAdmin(object):
    exclude = (
        'publicip_id',
        'create_time',
        'account',
        'result',
    )

    list_display =  [
        'publicip',
        'publicip_type',
        'result',
        'account_name',
        'region',
        'create_time',
    ]

    list_filter = [
        'account_name',
        'region',
        'publicip_type',
        'bandwidth_share_type',
    ]

    search_fields = [
        'bandwidth_share_type',
        'region',
        'publicip',
        'bandwidth_share_id',
        'bandwidth_name',
        'bandwidth_size',
        'account_name'
    ]

    #list_editable =  ['account_name', 'user_name', 'password', 'pidcn_north_1', 'pidcn_east_2', 'pidcn_south_1']
    list_per_page = 10
    #list_export = []
    show_detail_fields = []
    #refresh_times = (20,40,60)
    import_export_args = {'import_resource_class':CreateipImportResource}
    model_icon = 'fa fa-plus'
    actions = [CreateipAction,]
