import xadmin
from xadmin import views
from .models import Ecs
# Register your models here.

class GlobalSetting(object):
    site_title = '云资源自动管理V1.2.0'
    site_footer = 'V1.2.0'

class EcsAdmin(object):
    readonly_fields = ('ecs_name','ecs_id','region','delete_ecs_tag','shut_ecs_tag','ecs_status_tag','account_name')
    list_display =  ['ecs_name', 'region', 'account_name', 'ecs_shut_time', 'ecs_delete_time', 'ecs_status_tag']
    list_filter = ['account_name', 'region']
    search_fields = ['ecs_name','ecs_id','account_name','region']
    list_per_page = 10
    list_export = []
    refresh_times = (20,40,60)

#class Ecs_allAdmin(admin.ModelAdmin):
#    list_disply = ['ecs_name', 'ecs_id', 'regoin', 'shut_time', 'delete_time']
#    list_filter = ['region', 'shut_time','delete_time']
#    search_fields = ['ecs_name','ecs_id']
#    list_per_page = 10
#
#    actions = ['make_published']
#
#    def make_published(modeladmin, request, queryset):
#        queryset.update(operate=0)
#        n = queryset.count()
#        if n:
#            modeladmin.message_user(request,"Successfully deleted %s." % n)
#    make_published.short_description = "Mark selected stories as published"

xadmin.site.register(Ecs,EcsAdmin)
xadmin.site.register(views.CommAdminView, GlobalSetting)
#xadmin.site.register(Ecs_all,Ecs_allAdmin)
