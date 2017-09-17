import xadmin
from import_export import resources
from .models import Account
# Register your models here.
class AccountImportResource(resources.ModelResource):
    class Meta:
        model = Account
        #fields = ('name', 'description',)
        exclude = ('tokencn_north_1','tokencn_east_2','tokencn_south_1','token_up_time')

class AccountExportResource(resources.ModelResource):
    class Meta:
        model = Account
        #fields = ('name', 'description',)
        #exclude = ('tokencn_north_1','tokencn_east_2','tokencn_south_1','token_up_time')

@xadmin.sites.register(Account)
class AccountAdmin(object):
    exclude = ('tokencn_north_1','tokencn_east_2','tokencn_south_1','token_up_time')
    list_display =  ['account_name', 'user_name', 'pidcn_north_1', 'pidcn_east_2', 'pidcn_south_1']
    list_filter = ['account_name', 'user_name']
    search_fields = ['account_name','user_name']
    #list_editable =  ['account_name', 'user_name', 'password', 'pidcn_north_1', 'pidcn_east_2', 'pidcn_south_1']
    list_per_page = 10
    list_export = []
    #refresh_times = (5,10,20)                                                   
    import_export_args = {'import_resource_class': AccountImportResource, 'export_resource_class': AccountExportResource}
