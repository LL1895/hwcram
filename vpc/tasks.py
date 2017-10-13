from __future__ import absolute_import
from celery import shared_task
from api.vpc_api import VpcApi
import log.log as log
from account.models import Account
from vpc.models import Createip
from vpc.models import Vpc
import datetime

account_data = Account.objects.all()

@shared_task
def createip_task(
    createip_id,
    account_name,
    account_id,
    token,
    region,
    projectid,
    publicip_type,
    bandwidth_share_type,
    publicip,
    bandwidth_name,
    bandwidth_size,
    bandwidth_share_id,
    bandwidth_charge_mode,
):
    try:
        createip_data = Createip.objects.filter(id=createip_id)
        if bandwidth_share_type == 'PER':
            if bandwidth_name and bandwidth_size and bandwidth_charge_mode:
                r = VpcApi(
                    token,
                    region,
                    projectid,
                ).create_public_ip(
                    publicip_type,
                    bandwidth_share_type,
                    publicip,
                    bandwidth_name,
                    bandwidth_size,
                    bandwidth_share_id,
                    bandwidth_charge_mode,
                )

                if r[1] == 200:
                    createip_data.update(publicip_id = r[0]['id'])
                    createip_data.update(publicip = r[0]['public_ip_address'])
                    create_time = datetime.datetime.strptime(r[0]['create_time'],'%Y-%m-%d %H:%M:%S').replace(tzinfo=datetime.timezone.utc)
                    createip_data.update(create_time = create_time)
                    createip_data.update(result = str(r[1]))
                    createip_data.update(account_id = account_id)
                    return r
                else:
                    createip_data.update(result = str(r[1]))
                    createip_data.update(account_id = account_id)
                    return r
            else:
                createip_data.update(result = '1')

        if bandwidth_share_type == 'WHOLE':
            if bandwidth_share_id:
                r = VpcApi(
                    token,
                    region,
                    projectid,
                ).create_public_ip(
                    publicip_type,
                    bandwidth_share_type,
                    publicip,
                    bandwidth_name,
                    bandwidth_size,
                    bandwidth_share_id,
                    bandwidth_charge_mode,
                )

                if r[1] == 200:
                    createip_data.update(publicip_id = r[0]['id'])
                    createip_data.update(publicip = r[0]['public_ip_address'])
                    create_time = datetime.datetime.strptime(r[0]['create_time'],'%Y-%m-%d %H:%M:%S').replace(tzinfo=datetime.timezone.utc)
                    createip_data.update(create_time = create_time)
                    createip_data.update(result = str(r[1]))
                    createip_data.update(account_id = account_id)
                    return r
                else:
                    createip_data.update(result = str(r[1]))
                    createip_data.update(account_id = account_id)
                    return r
            else:
                createip_data.update(result = '2')
    except Exception as e:
        log.logging.error(e)

def delete_createip_all():
    utc_time_now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
    delete_time = utc_time_now - datetime.timedelta(hours=24)
    Createip.objects.filter(create_time__lt=delete_time).delete()

def sync_publicip_north():
    try:
        for account in account_data:

            publicip_all_n = VpcApi(account.tokencn_north_1,'cn-north-1',account.pidcn_north_1).get_public_ip()
            publicip_id_all_n = set()

            #add ips,update
            for pubip in publicip_all_n:
                create_time = datetime.datetime.strptime(pubip['create_time'],'%Y-%m-%d %H:%M:%S').replace(tzinfo=datetime.timezone.utc)
                Vpc.objects.get_or_create(
                    publicip_id=pubip['id'],
                    publicip_type=pubip['type'],
                    publicip=pubip['public_ip_address'],
                    project_id=pubip['tenant_id'],
                    #create_time=pubip['create_time'],
                    create_time=create_time,
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
                create_time = datetime.datetime.strptime(pubip['create_time'],'%Y-%m-%d %H:%M:%S').replace(tzinfo=datetime.timezone.utc)
                Vpc.objects.get_or_create(
                    publicip_id=pubip['id'],
                    publicip_type=pubip['type'],
                    publicip=pubip['public_ip_address'],
                    project_id=pubip['tenant_id'],
                    #create_time=pubip['create_time'],
                    create_time=create_time,
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
                create_time = datetime.datetime.strptime(pubip['create_time'],'%Y-%m-%d %H:%M:%S').replace(tzinfo=datetime.timezone.utc)
                Vpc.objects.get_or_create(
                    publicip_id=pubip['id'],
                    publicip_type=pubip['type'],
                    publicip=pubip['public_ip_address'],
                    project_id=pubip['tenant_id'],
                    #create_time=pubip['create_time'],
                    create_time=create_time,
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

@shared_task
def ip_task():
    sync_publicip_north()
    sync_publicip_east()
    sync_publicip_south()
    delete_createip_all()
