import os
import sys
import django
import datetime
from api.ecs_api import EcsApi
from api.vpc_api import VpcApi
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

#@transaction.atomic
def sync_north():
    try:
        for account in account_data:

            ecs_all_n = EcsApi(account.tokencn_north_1,'cn-north-1',account.pidcn_north_1).get_ecs()

            #add ecs,update ecs_name
            for k,v in ecs_all_n.items():
                Ecs.objects.get_or_create(ecs_id=v,region='cn-north-1',account_name=account.account_name,account_id=account.id)
                Ecs.objects.filter(ecs_id=v).update(ecs_name=k)

            #delete mysql_ecs
            ecs_id_all_n = set(ecs_all_n.values())
            ecs_id_all_mysql_n = set(list(map(lambda x: x.ecs_id,Ecs.objects.filter(account_name=account.account_name,region='cn-north-1'))))
            delete_ecs_mysql_n = list(ecs_id_all_mysql_n - ecs_id_all_n)

            for i in delete_ecs_mysql_n:
                Ecs.objects.filter(ecs_id=i).delete()
    except Exception as e:
        log.logging.error(e)

def is_active_north():
    try:
        for account in account_data:

            ecs_active_n = EcsApi(account.tokencn_north_1,'cn-north-1',account.pidcn_north_1).get_active_ecs()
            #add ecs_is_active
            Ecs.objects.filter(account_name=account.account_name,region='cn-north-1').update(ecs_is_active=0)
            for v in ecs_active_n.values():
                Ecs.objects.filter(ecs_id=v).update(ecs_is_active=1)
    except Exception as e:
        log.logging.error(e)


def deal_north():
    try:
        for account in account_data:
            #shutoff ecs and delete hwclouds_ecs
            ecs_id_shutoff_n = list(map(lambda x: x.ecs_id, Ecs.objects.filter(ecs_shut_time__lt=utc_time_now,account_name=account.account_name,region='cn-north-1')))
            ecs_id_delete_n = list(map(lambda x: x.ecs_id, Ecs.objects.filter(ecs_delete_time__lt=utc_time_now,account_name=account.account_name,region='cn-north-1')))

            if ecs_id_shutoff_n:
                EcsApi(account.tokencn_north_1,'cn-north-1',account.pidcn_north_1).shutoff_ecs(ecs_id_shutoff_n)

            if ecs_id_delete_n:
                EcsApi(account.tokencn_north_1,'cn-north-1',account.pidcn_north_1).delete_ecs(ecs_id_delete_n)
    except Exception as e:
        log.logging.error(e)

def private_ip_north():
    try:
        for account in account_data:
            #add private_ip
            private_ip_noexist_n = Ecs.objects.filter(private_ip__isnull=True,ecs_id__isnull=False,account_name=account.account_name,region='cn-north-1')
            for i in private_ip_noexist_n:
                ecs_private_ip_n = EcsApi(account.tokencn_north_1,'cn-north-1',account.pidcn_north_1).get_private_ip(i.ecs_id)
                Ecs.objects.filter(ecs_id=i.ecs_id).update(private_ip=ecs_private_ip_n[i.ecs_id])
    except Exception as e:
        log.logging.error(e)

def public_ip_north():
    try:
        for account in account_data:
            #add public_ip
            public_ip_noexist_n = Ecs.objects.filter(public_ip__isnull=True,ecs_id__isnull=False,account_name=account.account_name,region='cn-north-1')
            ecs_public_ip_n = VpcApi(account.tokencn_north_1,'cn-north-1',account.pidcn_north_1).get_public_ip()
            print(ecs_public_ip_n)
            #for i in public_ip_noexist_n:
            #    pass
            #    #Ecs.objects.filter(ecs_id=i.ecs_id).update(private_ip=ecs_private_ip_n[i.ecs_id])
    except Exception as e:
        log.logging.error(e)

def sync_east():
    try:
        for account in account_data:

            ecs_all_e = EcsApi(account.tokencn_east_2,'cn-east-2',account.pidcn_east_2).get_ecs()

            #add ecs,update ecs_name
            for k,v in ecs_all_e.items():
                Ecs.objects.get_or_create(ecs_id=v,region='cn-east-2',account_name=account.account_name,account_id=account.id)
                Ecs.objects.filter(ecs_id=v).update(ecs_name=k)

            #delete mysql_ecs
            ecs_id_all_e = set(ecs_all_e.values())
            ecs_id_all_mysql_e = set(list(map(lambda x: x.ecs_id,Ecs.objects.filter(account_name=account.account_name,region='cn-east-2'))))
            delete_ecs_mysql_e = list(ecs_id_all_mysql_e - ecs_id_all_e)

            for i in  delete_ecs_mysql_e:
                Ecs.objects.filter(ecs_id=i).delete()
    except Exception as e:
        log.logging.error(e)

def is_active_east():
    try:
        for account in account_data:

            ecs_active_e = EcsApi(account.tokencn_east_2,'cn-east-2',account.pidcn_east_2).get_active_ecs()

            #add ecs_is_active
            Ecs.objects.filter(account_name=account.account_name,region='cn-east-2').update(ecs_is_active=0)
            for v in ecs_active_e.values():
                Ecs.objects.filter(ecs_id=v).update(ecs_is_active=1)
    except Exception as e:
        log.logging.error(e)


def deal_east():
    try:
        for account in account_data:
            #shutoff ecs and delete hwclouds_ecs
            ecs_id_shutoff_e = list(map(lambda x: x.ecs_id, Ecs.objects.filter(ecs_shut_time__lt=utc_time_now,account_name=account.account_name,region='cn-east-2')))
            ecs_id_delete_e = list(map(lambda x: x.ecs_id, Ecs.objects.filter(ecs_delete_time__lt=utc_time_now,account_name=account.account_name,region='cn-east-2')))

            if ecs_id_shutoff_e:
                EcsApi(account.tokencn_east_2,'cn-east-2',account.pidcn_east_2).shutoff_ecs(ecs_id_shutoff_e)

            if ecs_id_delete_e:
                EcsApi(account.tokencn_east_2,'cn-east-2',account.pidcn_east_2).delete_ecs(ecs_id_shutoff_e)
    except Exception as e:
        log.logging.error(e)

def private_ip_east():
    try:
        for account in account_data:
            #add private_ip
            private_ip_noexist_e = Ecs.objects.filter(private_ip__isnull=True,ecs_id__isnull=False,account_name=account.account_name,region='cn-east-2')
            for i in private_ip_noexist_e:
                ecs_private_ip_e = EcsApi(account.tokencn_east_2,'cn-east-2',account.pidcn_east_2).get_private_ip(i.ecs_id)
                Ecs.objects.filter(ecs_id=i.ecs_id).update(private_ip=ecs_private_ip_e[i.ecs_id])
    except Exception as e:
        log.logging.error(e)

def sync_south():
    try:
        for account in account_data:

            ecs_all_s = EcsApi(account.tokencn_south_1,'cn-south-1',account.pidcn_south_1).get_ecs()

            #add ecs,update ecs_name
            for k,v in ecs_all_s.items():
                Ecs.objects.get_or_create(ecs_id=v,region='cn-south-1',account_name=account.account_name,account_id=account.id)
                Ecs.objects.filter(ecs_id=v).update(ecs_name=k)

            #delete mysql_ecs
            ecs_id_all_s = set(ecs_all_s.values())
            ecs_id_all_mysql_s = set(list(map(lambda x: x.ecs_id,Ecs.objects.filter(account_name=account.account_name,region='cn-south-1'))))
            delete_ecs_mysql_s = list(ecs_id_all_mysql_s - ecs_id_all_s)

            for i in  delete_ecs_mysql_s:
                Ecs.objects.filter(ecs_id=i).delete()
    except Exception as e:
        log.logging.error(e)

def is_active_south():
    try:
        for account in account_data:

            ecs_active_s = EcsApi(account.tokencn_south_1,'cn-south-1',account.pidcn_south_1).get_active_ecs()
            #add ecs_is_active
            Ecs.objects.filter(account_name=account.account_name,region='cn-south-1').update(ecs_is_active=0)
            for v in ecs_active_s.values():
                Ecs.objects.filter(ecs_id=v).update(ecs_is_active=1)
    except Exception as e:
        log.logging.error(e)


def deal_south():
    try:
        for account in account_data:
            #shutoff ecs and delete hwclouds_ecs
            ecs_id_shutoff_s = list(map(lambda x: x.ecs_id, Ecs.objects.filter(ecs_shut_time__lt=utc_time_now,account_name=account.account_name,region='cn-south-1')))
            ecs_id_delete_s = list(map(lambda x: x.ecs_id, Ecs.objects.filter(ecs_delete_time__lt=utc_time_now,account_name=account.account_name,region='cn-south-1')))

            if ecs_id_shutoff_s:
                EcsApi(account.tokencn_south_1,'cn-south-1',account.pidcn_south_1).shutoff_ecs(ecs_id_shutoff_s)

            if ecs_id_delete_s:
                EcsApi(account.tokencn_south_1,'cn-south-1',account.pidcn_south_1).delete_ecs(ecs_id_shutoff_s)
    except Exception as e:
        log.logging.error(e)

def private_ip_south():
    try:
        for account in account_data:
            #add private_ip
            private_ip_noexist_s = Ecs.objects.filter(private_ip__isnull=True,ecs_id__isnull=False,account_name=account.account_name,region='cn-south-1')
            for i in private_ip_noexist_s:
                ecs_private_ip_s = EcsApi(account.tokencn_south_1,'cn-south-1',account.pidcn_south_1).get_private_ip(i.ecs_id)
                Ecs.objects.filter(ecs_id=i.ecs_id).update(private_ip=ecs_private_ip_s[i.ecs_id])
    except Exception as e:
        log.logging.error(e)

#def main():
#    func_list = [sync_north,is_active_north,deal_north,ip_north,sync_east,is_active_east,deal_east,ip_east,sync_south,is_active_south,deal_south,ip_south]
#    p = Pool(processes=12)
#    #while True:
#    #    for i in func_list:
#    #        p.apply_async(i)
#    for i in func_list:
#        p.apply_async(i)
#
#    p.close()
#    p.join()
#
#if __name__ == '__main__':
#    main()

public_ip_north()
