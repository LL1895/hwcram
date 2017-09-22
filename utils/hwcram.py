import os
import sys
import django
import datetime
from api.ecs_api import EcsApi
import log.log as log
from multiprocessing import Pool
from time import sleep

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

            #add ecs,update ecs_name,update private_ip
            for k,v in ecs_all_n.items():
                Ecs.objects.get_or_create(ecs_id=v,region='cn-north-1',account_name=account.account_name,account_id=account.id)
                Ecs.objects.filter(ecs_id=v).update(ecs_name=k)
                ecs_private_ip_n = EcsApi(account.tokencn_north_1,'cn-north-1',account.pidcn_north_1).get_private_ip(v)
                Ecs.objects.filter(ecs_id=v).update(private_ip=ecs_private_ip_n[v])

            #add ecs_is_active
            Ecs.objects.filter(account_name=account.account_name,region='cn-north-1').update(ecs_is_active=0)
            for v in ecs_active_n.values():
                Ecs.objects.filter(ecs_id=v).update(ecs_is_active=1)

            #delete mysql_ecs
            ecs_id_all_n = set(ecs_all_n.values())
            ecs_id_all_mysql_n = set(list(map(lambda x: x.ecs_id,Ecs.objects.filter(account_name=account.account_name,region='cn-north-1'))))
            delete_ecs_mysql_n = list(ecs_id_all_mysql_n - ecs_id_all_n)

            for i in delete_ecs_mysql_n:
                Ecs.objects.filter(ecs_id=i).delete()

            #shutoff ecs and delete hwclouds_ecs
            ecs_id_shutoff_n = list(map(lambda x: x.ecs_id, Ecs.objects.filter(ecs_shut_time__lt=utc_time_now,account_name=account.account_name,region='cn-north-1')))
            ecs_id_delete_n = list(map(lambda x: x.ecs_id, Ecs.objects.filter(ecs_delete_time__lt=utc_time_now,account_name=account.account_name,region='cn-north-1')))

            if ecs_id_shutoff_n:
                EcsApi(account.tokencn_north_1,'cn-north-1',account.pidcn_north_1).shutoff_ecs(ecs_id_shutoff_n)

            if ecs_id_delete_n:
                EcsApi(account.tokencn_north_1,'cn-north-1',account.pidcn_north_1).delete_ecs(ecs_id_delete_n)

            #cn-east-2
            ecs_all_e = EcsApi(account.tokencn_east_2,'cn-east-2',account.pidcn_east_2).get_ecs()
            ecs_active_e = EcsApi(account.tokencn_east_2,'cn-east-2',account.pidcn_east_2).get_active_ecs()

            #add ecs,update ecs_name,update private_ip
            for k,v in ecs_all_e.items():
                Ecs.objects.get_or_create(ecs_id=v,region='cn-east-2',account_name=account.account_name,account_id=account.id)
                Ecs.objects.filter(ecs_id=v).update(ecs_name=k)
                ecs_private_ip_e = EcsApi(account.tokencn_east_2,'cn-east-2',account.pidcn_east_2).get_private_ip(v)
                Ecs.objects.filter(ecs_id=v).update(private_ip=ecs_private_ip_e[v])

            #add ecs_is_active
            Ecs.objects.filter(account_name=account.account_name,region='cn-east-2').update(ecs_is_active=0)
            for v in ecs_active_e.values():
                Ecs.objects.filter(ecs_id=v).update(ecs_is_active=1)

            #delete mysql_ecs
            ecs_id_all_e = set(ecs_all_n.values())
            ecs_id_all_mysql_e = set(list(map(lambda x: x.ecs_id,Ecs.objects.filter(account_name=account.account_name,region='cn-east-2'))))
            delete_ecs_mysql_e = list(ecs_id_all_mysql_n - ecs_id_all_n)

            for i in  delete_ecs_mysql_e:
                Ecs.objects.filter(ecs_id=i).delete()

            #shutoff ecs and delete hwclouds_ecs
            ecs_id_shutoff_e = list(map(lambda x: x.ecs_id, Ecs.objects.filter(ecs_shut_time__lt=utc_time_now,account_name=account.account_name,region='cn-east-2')))
            ecs_id_delete_e = list(map(lambda x: x.ecs_id, Ecs.objects.filter(ecs_delete_time__lt=utc_time_now,account_name=account.account_name,region='cn-east-2')))

            if ecs_id_shutoff_e:
                EcsApi(account.tokencn_east_2,'cn-east-2',account.pidcn_east_2).shutoff_ecs(ecs_id_shutoff_e)

            if ecs_id_delete_e:
                EcsApi(account.tokencn_east_2,'cn-east-2',account.pidcn_east_2).delete_ecs(ecs_id_shutoff_e)

            #cn-south-1
            ecs_all_s = EcsApi(account.tokencn_south_1,'cn-south-1',account.pidcn_south_1).get_ecs()
            ecs_active_s = EcsApi(account.tokencn_south_1,'cn-south-1',account.pidcn_south_1).get_active_ecs()

            #add ecs,update ecs_name,update private_ip
            for k,v in ecs_all_s.items():
                Ecs.objects.get_or_create(ecs_id=v,region='cn-south-1',account_name=account.account_name,account_id=account.id)
                Ecs.objects.filter(ecs_id=v).update(ecs_name=k)
                ecs_private_ip_s = EcsApi(account.tokencn_south_1,'cn-south-1',account.pidcn_south_1).get_private_ip(v)
                Ecs.objects.filter(ecs_id=v).update(private_ip=ecs_private_ip_s[v])

            #add ecs_is_active
            Ecs.objects.filter(account_name=account.account_name,region='cn-south-1').update(ecs_is_active=0)
            for v in ecs_active_s.values():
                Ecs.objects.filter(ecs_id=v).update(ecs_is_active=1)

            #delete mysql_ecs
            ecs_id_all_s = set(ecs_all_s.values())
            ecs_id_all_mysql_s = set(list(map(lambda x: x.ecs_id,Ecs.objects.filter(account_name=account.account_name,region='cn-south-1'))))
            delete_ecs_mysql_s = list(ecs_id_all_mysql_s - ecs_id_all_s)

            for i in  delete_ecs_mysql_s:
                Ecs.objects.filter(ecs_id=i).delete()

            #shutoff ecs and delete hwclouds_ecs
            ecs_id_shutoff_s = list(map(lambda x: x.ecs_id, Ecs.objects.filter(ecs_shut_time__lt=utc_time_now,account_name=account.account_name,region='cn-south-1')))
            ecs_id_delete_s = list(map(lambda x: x.ecs_id, Ecs.objects.filter(ecs_delete_time__lt=utc_time_now,account_name=account.account_name,region='cn-south-1')))

            if ecs_id_shutoff_s:
                EcsApi(account.tokencn_south_1,'cn-south-1',account.pidcn_south_1).shutoff_ecs(ecs_id_shutoff_s)

            if ecs_id_delete_s:
                EcsApi(account.tokencn_south_1,'cn-south-1',account.pidcn_south_1).delete_ecs(ecs_id_shutoff_s)
    except Exception as e:
        log.logging.error(e)

def main():
    func_list = [update_token,sync_ecs]
    p = Pool(processes=2)
    while True:
        for i in func_list:
            p.apply_async(i)
    p.close()
    p.join()

if __name__ == '__main__':
    main()
