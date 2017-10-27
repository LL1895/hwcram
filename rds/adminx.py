import xadmin
from import_export import resources
from .models import Rds
from account.models import Account
# Register your models here.
class RdsImportResource(resources.ModelResource):
    class Meta:
        model = Rds
        #fields = ('name', 'description',)
        #exclude = ('tokencn_north_1','tokencn_east_2','tokencn_south_1','token_up_time')

class RdsExportResource(resources.ModelResource):
    class Meta:
        model = Rds
        #fields = ('name', 'description',)
        exclude = ('account')

@xadmin.sites.register(Rds)
class RdsAdmin(object):
    readonly_fields = (
        'rds_name',
        'rds_id',
        'rds_host',
        'rds_port',
        'rds_type',
        'account',
        'account_name',
        'region',
        'rds_status',
    )

    list_display =  [
        'rds_name',
        'rds_status',
        'rds_host',
        'rds_port',
        'rds_delete_time',
        'rds_type',
        'region',
        'account_name',
    ]

    list_filter = [
        'account_name',
        'region',
        'rds_status',
    ]

    search_fields = [
        'rds_id',
        'region',
        'rds_name',
        'rds_status',
        'rds_host',
        'rds_port',
        'account_name'
    ]
    #list_editable =  ['account_name', 'user_name', 'password', 'pidcn_north_1', 'pidcn_east_2', 'pidcn_south_1']
    list_per_page = 10
    #list_export = []
    show_detail_fields = []
    refresh_times = (20,40,60)
    model_icon = 'fa fa-database'
    #import_export_args = {'export_resource_class': VpcExportResource}
