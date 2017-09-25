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
def sync_publicip_north():
    try:
        for account in account_data:

            publicip_all_n = VpcApi(account.tokencn_north_1,'cn-north-1',account.pidcn_north_1).get_public_ip()
            publicip_id_all_n = set()

            #add ips,update
            for pubip in publicip_all_n:
                Vpc.objects.get_or_create(
                    publicip_id=pubip['id'],
                    publicip_type=pubip['type'],
                    publicip=pubip['public_ip_address'],
                    project_id=pubip['tenant_id'],
                    create_time=pubip['create_time'],
                    bandwidth_id=pubip['bandwidth_id'],
                    bandwidth_type=pubip['bandwidth_share_type'],
                    region='cn-north-1',
                    account_name=account.account_name,
                    account_id=account.id,
                )

                if 'private_ip_address' in pubip.keys():
                    Vpc.objects.filter(publicip_id=pubip['id']).update(
                        publicip_status=pubip['status'],
                        privateip=pubip['private_ip_address'],
                        bandwidth_size=pubip['bandwidth_size'],
                        bandwidth_name = pubip['bandwidth_name'],
                    )
                else:
                    Vpc.objects.filter(publicip_id=pubip['id']).update(
                        publicip_status=pubip['status'],
                        bandwidth_size=pubip['bandwidth_size'],
                        bandwidth_name = pubip['bandwidth_name'],
                    )

            #delete mysql_publicip
                publicip_id_all_n.add(pubip['id'])
            publicip_id_all_mysql_n = set(list(map(lambda x: x.publicip_id,Vpc.objects.filter(account_name=account.account_name,region='cn-north-1'))))
            delete_publicip_mysql_n = list(publicip_id_all_mysql_n - publicip_id_all_n)

            for pubip_id in delete_publicip_mysql_n:
                Vpc.objects.filter(publicip_id=pubip_id).delete()
    except Exception as e:
        log.logging.error(e)

def sync_publicip_east():
    try:
        for account in account_data:

            publicip_all_e = VpcApi(account.tokencn_east_2,'cn-east-2',account.pidcn_east_2).get_public_ip()
            publicip_id_all_e = set()

            #add ips,update
            for pubip in publicip_all_e:
                Vpc.objects.get_or_create(
                    publicip_id=pubip['id'],
                    publicip_type=pubip['type'],
                    publicip=pubip['public_ip_address'],
                    project_id=pubip['tenant_id'],
                    create_time=pubip['create_time'],
                    bandwidth_id=pubip['bandwidth_id'],
                    bandwidth_type=pubip['bandwidth_share_type'],
                    region='cn-east-2',
                    account_name=account.account_name,
                    account_id=account.id,
                )

                if 'private_ip_address' in pubip.keys():
                    Vpc.objects.filter(publicip_id=pubip['id']).update(
                        publicip_status=pubip['status'],
                        privateip=pubip['private_ip_address'],
                        bandwidth_size=pubip['bandwidth_size'],
                        bandwidth_name = pubip['bandwidth_name'],
                    )
                else:
                    Vpc.objects.filter(publicip_id=pubip['id']).update(
                        publicip_status=pubip['status'],
                        bandwidth_size=pubip['bandwidth_size'],
                        bandwidth_name = pubip['bandwidth_name'],
                    )

            #delete mysql_publicip
                publicip_id_all_e.add(pubip['id'])
            publicip_id_all_mysql_e = set(list(map(lambda x: x.publicip_id,Vpc.objects.filter(account_name=account.account_name,region='cn-east-2'))))
            delete_publicip_mysql_e = list(publicip_id_all_mysql_e - publicip_id_all_e)

            for pubip_id in delete_publicip_mysql_e:
                Vpc.objects.filter(publicip_id=pubip_id).delete()
    except Exception as e:
        log.logging.error(e)

def sync_publicip_south():
    try:
        for account in account_data:

            publicip_all_s = VpcApi(account.tokencn_south_1,'cn-south-1',account.pidcn_south_1).get_public_ip()
            publicip_id_all_s = set()

            #add ips,update
            for pubip in publicip_all_s:
                Vpc.objects.get_or_create(
                    publicip_id=pubip['id'],
                    publicip_type=pubip['type'],
                    publicip=pubip['public_ip_address'],
                    project_id=pubip['tenant_id'],
                    create_time=pubip['create_time'],
                    bandwidth_id=pubip['bandwidth_id'],
                    bandwidth_type=pubip['bandwidth_share_type'],
                    region='cn-south-1',
                    account_name=account.account_name,
                    account_id=account.id,
                )

                if 'private_ip_address' in pubip.keys():
                    Vpc.objects.filter(publicip_id=pubip['id']).update(
                        publicip_status=pubip['status'],
                        privateip=pubip['private_ip_address'],
                        bandwidth_size=pubip['bandwidth_size'],
                        bandwidth_name = pubip['bandwidth_name'],
                    )
                else:
                    Vpc.objects.filter(publicip_id=pubip['id']).update(
                        publicip_status=pubip['status'],
                        bandwidth_size=pubip['bandwidth_size'],
                        bandwidth_name = pubip['bandwidth_name'],
                    )

            #delete mysql_publicip
                publicip_id_all_s.add(pubip['id'])
            publicip_id_all_mysql_s = set(list(map(lambda x: x.publicip_id,Vpc.objects.filter(account_name=account.account_name,region='cn-south-1'))))
            delete_publicip_mysql_s = list(publicip_id_all_mysql_s - publicip_id_all_s)

            for pubip_id in delete_publicip_mysql_s:
                Vpc.objects.filter(publicip_id=pubip_id).delete()
    except Exception as e:
        log.logging.error(e)

def main():
    func_list = [sync_publicip_north,sync_publicip_east,sync_publicip_south]
    p_count = len(func_list)
    p = Pool(processes=p_count)
    while True:
        for i in func_list:
            p.apply_async(i)
        sleep(5)

    p.close()
    p.join()

if __name__ == '__main__':
    main()
