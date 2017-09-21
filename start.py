import os
import sys
import django
import datetime
from api.ecs_api import EcsApi
import log.log as log

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hwcram.settings")

django.setup()
from django.db import transaction
from account.models import Account
from ecs.models import Ecs

account_data = Account.objects.all()
utc_time_now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
shut_time = utc_time_now + datetime.timedelta(hours=10)
delete_time = shut_time + datetime.timedelta(days=7)

def update_token():
    try:
        for i in account_data:
            if utc_time_now > i.token_up_time:
                i.save()
    except Exception as e:
        log.logging.error(e)
        log.logging.error("Failed to update_token")

#@transaction.atomic
def sync_ecs():
    try:
        for account in account_data:
            #cn-north-1
            ecs_all_n = EcsApi(account.tokencn_north_1,'cn-north-1',account.pidcn_north_1).get_ecs()
            ecs_active_n = EcsApi(account.tokencn_north_1,'cn-north-1',account.pidcn_north_1).get_active_ecs()

            for k,v in ecs_all_n.items():
                Ecs.objects.get_or_create(ecs_id=v,region='cn-north-1',account_name=account.account_name,account_id=account.id)
                Ecs.objects.filter(ecs_id=v).update(ecs_name=k)

            for v in ecs_active_n.values():
                Ecs.objects.filter(ecs_id=v).update(ecs_is_active=1)

            ecs_id_all_n = set(ecs_all_n.values())
            ecs_id_all_mysql_n = set(list(map(lambda x: x.ecs_id,Ecs.objects.filter(account_name=account.account_name,region='cn-north-1'))))
            delete_ecs_mysql_n = list(ecs_id_all_mysql_n - ecs_id_all_n)

            for i in  delete_ecs_mysql_n:
                Ecs.objects.filter(ecs_id=i).delete()

            #cn-east-2
            ecs_all_e = EcsApi(account.tokencn_east_2,'cn-east-2',account.pidcn_east_2).get_ecs()
            ecs_active_e = EcsApi(account.tokencn_east_2,'cn-east-2',account.pidcn_east_2).get_active_ecs()

            for k,v in ecs_all_e.items():
                Ecs.objects.get_or_create(ecs_id=v,region='cn-east-2',account_name=account.account_name,account_id=account.id)
                Ecs.objects.filter(ecs_id=v).update(ecs_name=k)

            for v in ecs_active_e.values():
                Ecs.objects.filter(ecs_id=v).update(ecs_is_active=1)

            ecs_id_all_e = set(ecs_all_n.values())
            ecs_id_all_mysql_e = set(list(map(lambda x: x.ecs_id,Ecs.objects.filter(account_name=account.account_name,region='cn-east-2'))))
            delete_ecs_mysql_e = list(ecs_id_all_mysql_n - ecs_id_all_n)

            for i in  delete_ecs_mysql_e:
                Ecs.objects.filter(ecs_id=i).delete()

            #cn-south-1
            ecs_all_s = EcsApi(account.tokencn_south_1,'cn-south-1',account.pidcn_south_1).get_ecs()
            ecs_active_s = EcsApi(account.tokencn_south_1,'cn-south-1',account.pidcn_south_1).get_active_ecs()

            for k,v in ecs_all_s.items():
                Ecs.objects.get_or_create(ecs_id=v,region='cn-south-1',account_name=account.account_name,account_id=account.id)
                Ecs.objects.filter(ecs_id=v).update(ecs_name=k)

            for v in ecs_active_s.values():
                Ecs.objects.filter(ecs_id=v).update(ecs_is_active=1)

            ecs_id_all_s = set(ecs_all_s.values())
            ecs_id_all_mysql_s = set(list(map(lambda x: x.ecs_id,Ecs.objects.filter(account_name=account.account_name,region='cn-south-1'))))
            delete_ecs_mysql_s = list(ecs_id_all_mysql_s - ecs_id_all_s)

            for i in  delete_ecs_mysql_s:
                Ecs.objects.filter(ecs_id=i).delete()
    except Exception as e:
        log.logging.error(e)

update_token()
sync_ecs()
