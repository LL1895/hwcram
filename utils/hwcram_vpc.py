import os
import sys
import django
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
from vpc.models import Vpc

account_data = Account.objects.all()

#@transaction.atomic
def sync_vpc_north():
    try:
        for account in account_data:

            vpc_all_n = VpcApi(account.tokencn_north_1,'cn-north-1',account.pidcn_north_1).get_public_ip()

            #add ips,update
            for i in vpc_all_n:
                Vpc.objects.get_or_create(
                    publicip_id=i['id'],
                    publicip_type=i['type'],
                    publicip=i['public_ip_address'],
                    project_id=i['tenant_id'],
                    create_time=i['create_time'],
                    bandwidth_id=i['bandwidth_id'],
                    bandwidth_type=i['bandwidth_share_type'],
                    region='cn-north-1',
                    account_name=account.account_name,
                    account_id=account.id,
                )

                if 'private_ip_address' in i.keys():
                    Vpc.objects.filter(publicip_id=i['id']).update(
                        publicip_status=i['status'],
                        privateip=i['private_ip_address'],
                        bandwidth_size=i['bandwidth_size'],
                        bandwidth_name = i['bandwidth_name'],
                    )
                else:
                    Vpc.objects.filter(publicip_id=i['id']).update(
                        publicip_status=i['status'],
                        bandwidth_size=i['bandwidth_size'],
                        bandwidth_name = i['bandwidth_name'],
                    )
    except Exception as e:
        log.logging.error(e)


#            #delete mysql_ecs
#            ecs_id_all_n = set(ecs_all_n.values())
#            ecs_id_all_mysql_n = set(list(map(lambda x: x.ecs_id,Ecs.objects.filter(account_name=account.account_name,region='cn-north-1'))))
#            delete_ecs_mysql_n = list(ecs_id_all_mysql_n - ecs_id_all_n)
#
#            for i in delete_ecs_mysql_n:
#                Ecs.objects.filter(ecs_id=i).delete()
#    except Exception as e:
#        log.logging.error(e)
#
#def is_active_north():
#    try:
#        for account in account_data:
#
#            ecs_active_n = EcsApi(account.tokencn_north_1,'cn-north-1',account.pidcn_north_1).get_active_ecs()
#            #add ecs_is_active
#            Ecs.objects.filter(account_name=account.account_name,region='cn-north-1').update(ecs_is_active=0)
#            for v in ecs_active_n.values():
#                Ecs.objects.filter(ecs_id=v).update(ecs_is_active=1)
#    except Exception as e:
#        log.logging.error(e)
#
#
#def deal_north():
#    try:
#        for account in account_data:
#            #shutoff ecs and delete hwclouds_ecs
#            ecs_id_shutoff_n = list(map(lambda x: x.ecs_id, Ecs.objects.filter(ecs_shut_time__lt=utc_time_now,account_name=account.account_name,region='cn-north-1')))
#            ecs_id_delete_n = list(map(lambda x: x.ecs_id, Ecs.objects.filter(ecs_delete_time__lt=utc_time_now,account_name=account.account_name,region='cn-north-1')))
#
#            if ecs_id_shutoff_n:
#                EcsApi(account.tokencn_north_1,'cn-north-1',account.pidcn_north_1).shutoff_ecs(ecs_id_shutoff_n)
#
#            if ecs_id_delete_n:
#                EcsApi(account.tokencn_north_1,'cn-north-1',account.pidcn_north_1).delete_ecs(ecs_id_delete_n)
#    except Exception as e:
#        log.logging.error(e)
#
#def private_ip_north():
#    try:
#        for account in account_data:
#            #add private_ip
#            private_ip_noexist_n = Ecs.objects.filter(private_ip__isnull=True,ecs_id__isnull=False,account_name=account.account_name,region='cn-north-1')
#            for i in private_ip_noexist_n:
#                ecs_private_ip_n = EcsApi(account.tokencn_north_1,'cn-north-1',account.pidcn_north_1).get_private_ip(i.ecs_id)
#                Ecs.objects.filter(ecs_id=i.ecs_id).update(private_ip=ecs_private_ip_n[i.ecs_id])
#    except Exception as e:
#        log.logging.error(e)
#
#def public_ip_north():
#    try:
#        for account in account_data:
#            #add public_ip
#            ecs_public_ip_n = VpcApi(account.tokencn_north_1,'cn-north-1',account.pidcn_north_1).get_public_ip()
#            for i in ecs_public_ip_n:
#                if 'private_ip_address' in i.keys():
#                    Ecs.objects.filter(private_ip=i['private_ip_address'],public_ip__isnull=True,account__pidcn_north_1__contains=i['tenant_id']).update(public_ip=i['public_ip_address'])
#    except Exception as e:
#        log.logging.error(e)
#
#def sync_ecs_east():
#    try:
#        for account in account_data:
#
#            ecs_all_e = EcsApi(account.tokencn_east_2,'cn-east-2',account.pidcn_east_2).get_ecs()
#
#            #add ecs,update ecs_name
#            for k,v in ecs_all_e.items():
#                Ecs.objects.get_or_create(ecs_id=v,region='cn-east-2',account_name=account.account_name,account_id=account.id)
#                Ecs.objects.filter(ecs_id=v).update(ecs_name=k)
#
#            #delete mysql_ecs
#            ecs_id_all_e = set(ecs_all_e.values())
#            ecs_id_all_mysql_e = set(list(map(lambda x: x.ecs_id,Ecs.objects.filter(account_name=account.account_name,region='cn-east-2'))))
#            delete_ecs_mysql_e = list(ecs_id_all_mysql_e - ecs_id_all_e)
#
#            for i in  delete_ecs_mysql_e:
#                Ecs.objects.filter(ecs_id=i).delete()
#    except Exception as e:
#        log.logging.error(e)
#
#def is_active_east():
#    try:
#        for account in account_data:
#
#            ecs_active_e = EcsApi(account.tokencn_east_2,'cn-east-2',account.pidcn_east_2).get_active_ecs()
#
#            #add ecs_is_active
#            Ecs.objects.filter(account_name=account.account_name,region='cn-east-2').update(ecs_is_active=0)
#            for v in ecs_active_e.values():
#                Ecs.objects.filter(ecs_id=v).update(ecs_is_active=1)
#    except Exception as e:
#        log.logging.error(e)
#
#
#def deal_east():
#    try:
#        for account in account_data:
#            #shutoff ecs and delete hwclouds_ecs
#            ecs_id_shutoff_e = list(map(lambda x: x.ecs_id, Ecs.objects.filter(ecs_shut_time__lt=utc_time_now,account_name=account.account_name,region='cn-east-2')))
#            ecs_id_delete_e = list(map(lambda x: x.ecs_id, Ecs.objects.filter(ecs_delete_time__lt=utc_time_now,account_name=account.account_name,region='cn-east-2')))
#
#            if ecs_id_shutoff_e:
#                EcsApi(account.tokencn_east_2,'cn-east-2',account.pidcn_east_2).shutoff_ecs(ecs_id_shutoff_e)
#
#            if ecs_id_delete_e:
#                EcsApi(account.tokencn_east_2,'cn-east-2',account.pidcn_east_2).delete_ecs(ecs_id_shutoff_e)
#    except Exception as e:
#        log.logging.error(e)
#
#def private_ip_east():
#    try:
#        for account in account_data:
#            #add private_ip
#            private_ip_noexist_e = Ecs.objects.filter(private_ip__isnull=True,ecs_id__isnull=False,account_name=account.account_name,region='cn-east-2')
#            for i in private_ip_noexist_e:
#                ecs_private_ip_e = EcsApi(account.tokencn_east_2,'cn-east-2',account.pidcn_east_2).get_private_ip(i.ecs_id)
#                Ecs.objects.filter(ecs_id=i.ecs_id).update(private_ip=ecs_private_ip_e[i.ecs_id])
#    except Exception as e:
#        log.logging.error(e)
#
#def public_ip_east():
#    try:
#        for account in account_data:
#            #add public_ip
#            ecs_public_ip_e = VpcApi(account.tokencn_east_2,'cn-east-2',account.pidcn_east_2).get_public_ip()
#            for i in ecs_public_ip_e:
#                if 'private_ip_address' in i.keys():
#                    Ecs.objects.filter(private_ip=i['private_ip_address'],public_ip__isnull=True,account__pidcn_east_2__contains=i['tenant_id']).update(public_ip=i['public_ip_address'])
#    except Exception as e:
#        log.logging.error(e)
#
#def sync_ecs_south():
#    try:
#        for account in account_data:
#
#            ecs_all_s = EcsApi(account.tokencn_south_1,'cn-south-1',account.pidcn_south_1).get_ecs()
#
#            #add ecs,update ecs_name
#            for k,v in ecs_all_s.items():
#                Ecs.objects.get_or_create(ecs_id=v,region='cn-south-1',account_name=account.account_name,account_id=account.id)
#                Ecs.objects.filter(ecs_id=v).update(ecs_name=k)
#
#            #delete mysql_ecs
#            ecs_id_all_s = set(ecs_all_s.values())
#            ecs_id_all_mysql_s = set(list(map(lambda x: x.ecs_id,Ecs.objects.filter(account_name=account.account_name,region='cn-south-1'))))
#            delete_ecs_mysql_s = list(ecs_id_all_mysql_s - ecs_id_all_s)
#
#            for i in  delete_ecs_mysql_s:
#                Ecs.objects.filter(ecs_id=i).delete()
#    except Exception as e:
#        log.logging.error(e)
#
#def is_active_south():
#    try:
#        for account in account_data:
#
#            ecs_active_s = EcsApi(account.tokencn_south_1,'cn-south-1',account.pidcn_south_1).get_active_ecs()
#            #add ecs_is_active
#            Ecs.objects.filter(account_name=account.account_name,region='cn-south-1').update(ecs_is_active=0)
#            for v in ecs_active_s.values():
#                Ecs.objects.filter(ecs_id=v).update(ecs_is_active=1)
#    except Exception as e:
#        log.logging.error(e)
#
#
#def deal_south():
#    try:
#        for account in account_data:
#            #shutoff ecs and delete hwclouds_ecs
#            ecs_id_shutoff_s = list(map(lambda x: x.ecs_id, Ecs.objects.filter(ecs_shut_time__lt=utc_time_now,account_name=account.account_name,region='cn-south-1')))
#            ecs_id_delete_s = list(map(lambda x: x.ecs_id, Ecs.objects.filter(ecs_delete_time__lt=utc_time_now,account_name=account.account_name,region='cn-south-1')))
#
#            if ecs_id_shutoff_s:
#                EcsApi(account.tokencn_south_1,'cn-south-1',account.pidcn_south_1).shutoff_ecs(ecs_id_shutoff_s)
#
#            if ecs_id_delete_s:
#                EcsApi(account.tokencn_south_1,'cn-south-1',account.pidcn_south_1).delete_ecs(ecs_id_shutoff_s)
#    except Exception as e:
#        log.logging.error(e)
#
#def private_ip_south():
#    try:
#        for account in account_data:
#            #add private_ip
#            private_ip_noexist_s = Ecs.objects.filter(private_ip__isnull=True,ecs_id__isnull=False,account_name=account.account_name,region='cn-south-1')
#            for i in private_ip_noexist_s:
#                ecs_private_ip_s = EcsApi(account.tokencn_south_1,'cn-south-1',account.pidcn_south_1).get_private_ip(i.ecs_id)
#                Ecs.objects.filter(ecs_id=i.ecs_id).update(private_ip=ecs_private_ip_s[i.ecs_id])
#    except Exception as e:
#        log.logging.error(e)
#
#def public_ip_south():
#    try:
#        for account in account_data:
#            #add public_ip
#            ecs_public_ip_s = VpcApi(account.tokencn_south_1,'cn-south-1',account.pidcn_south_1).get_public_ip()
#            for i in ecs_public_ip_s:
#                if 'private_ip_address' in i.keys():
#                    Ecs.objects.filter(private_ip=i['private_ip_address'],public_ip__isnull=True,account__pidcn_south_1__contains=i['tenant_id']).update(public_ip=i['public_ip_address'])
#    except Exception as e:
#        log.logging.error(e)
#
#def main():
#    func_list = [sync_ecs_north,is_active_north,deal_north,private_ip_north,public_ip_north,sync_ecs_east,is_active_east,deal_east,private_ip_east,public_ip_east,sync_ecs_south,is_active_south,deal_south,private_ip_south,public_ip_south]
#    p_count = len(func_list)
#    p = Pool(processes=p_count)
#    while True:
#        for i in func_list:
#            p.apply_async(i)
#        sleep(5)
#
#    p.close()
#    p.join()
#
#if __name__ == '__main__':
#    main()

sync_vpc_north()