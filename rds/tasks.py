from __future__ import absolute_import
from celery import shared_task
import datetime
from api.rds_api import RdsApi
import log.log as log
from account.models import Account
from .models import Rds

def sync_rds_north():
    try:
        account_data = Account.objects.all()
        for account in account_data:
            rds_all_n = RdsApi(account.tokencn_north_1,'cn-north-1',account.pidcn_north_1).get_instances()
            ilist = []
            #add rds
            for ins in rds_all_n:
                Rds.objects.get_or_create(
                    rds_name=ins['name'],
                    region='cn-north-1',
                    rds_id=ins['id'],
                    rds_host=ins['hostname'],
                    rds_type=ins['type'],
                    account_name=account.account_name,
                    account_id=account.id
                )
                ilist.append(ins['id'])
            #update status,port
                Rds.objects.filter(rds_id=ins['id']).update(rds_status=ins['status'])
                Rds.objects.filter(rds_id=ins['id']).update(rds_port=ins['dbPort'])
            #delete mysql_rds
            rds_id_all_n = set(ilist)
            rds_id_all_mysql_n = set(list(map(lambda x: x.rds_id,Rds.objects.filter(account_name=account.account_name,region='cn-north-1'))))
            delete_rds_mysql_n = list(rds_id_all_mysql_n - rds_id_all_n)

            for i in delete_rds_mysql_n:
                Rds.objects.filter(rds_id=i).delete()
    except Exception as e:
        log.logging.error(e)

def deal_north():
    try:
        account_data = Account.objects.all()
        utc_time_now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
        for account in account_data:
            #delete rds
            rds_id_delete_n = list(map(lambda x: x.rds_id, Rds.objects.filter(rds_delete_time__lt=utc_time_now,account_name=account.account_name,region='cn-north-1')))

            for ins in rds_id_delete_n:
                RdsApi(account.tokencn_north_1,'cn-north-1',account.pidcn_north_1).delete_instances(ins)
    except Exception as e:
        log.logging.error(e)


def sync_rds_east():
    try:
        account_data = Account.objects.all()
        for account in account_data:
            rds_all_e = RdsApi(account.tokencn_east_2,'cn-east-2',account.pidcn_east_2).get_instances()
            ilist = []
            #add rds
            for ins in rds_all_e:
                Rds.objects.get_or_create(
                    rds_name=ins['name'],
                    region='cn-east-2',
                    rds_id=ins['id'],
                    rds_host=ins['hostname'],
                    rds_type=ins['type'],
                    account_name=account.account_name,
                    account_id=account.id
                )
                ilist.append(ins['id'])
            #update status,port
                Rds.objects.filter(rds_id=ins['id']).update(rds_status=ins['status'])
                Rds.objects.filter(rds_id=ins['id']).update(rds_port=ins['dbPort'])
            #delete mysql_rds
            rds_id_all_e = set(ilist)
            rds_id_all_mysql_e = set(list(map(lambda x: x.rds_id,Rds.objects.filter(account_name=account.account_name,region='cn-east-2'))))
            delete_rds_mysql_e = list(rds_id_all_mysql_e - rds_id_all_e)

            for i in delete_rds_mysql_e:
                Rds.objects.filter(rds_id=i).delete()
    except Exception as e:
        log.logging.error(e)

def deal_east():
    try:
        account_data = Account.objects.all()
        utc_time_now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
        for account in account_data:
            #delete rds
            rds_id_delete_e = list(map(lambda x: x.rds_id, Rds.objects.filter(rds_delete_time__lt=utc_time_now,account_name=account.account_name,region='cn-east-2')))

            for ins in rds_id_delete_e:
                RdsApi(account.tokencn_east_2,'cn-east-2',account.pidcn_east_2).delete_instances(ins)
    except Exception as e:
        log.logging.error(e)

def sync_rds_south():
    try:
        account_data = Account.objects.all()
        for account in account_data:
            rds_all_s = RdsApi(account.tokencn_south_1,'cn-south-1',account.pidcn_south_1).get_instances()
            ilist = []
            #add rds
            for ins in rds_all_s:
                Rds.objects.get_or_create(
                    rds_name=ins['name'],
                    region='cn-south-1',
                    rds_id=ins['id'],
                    rds_host=ins['hostname'],
                    rds_type=ins['type'],
                    account_name=account.account_name,
                    account_id=account.id
                )
                ilist.append(ins['id'])
            #update status,port
                Rds.objects.filter(rds_id=ins['id']).update(rds_status=ins['status'])
                Rds.objects.filter(rds_id=ins['id']).update(rds_port=ins['dbPort'])
            #delete mysql_rds
            rds_id_all_s = set(ilist)
            rds_id_all_mysql_s = set(list(map(lambda x: x.rds_id,Rds.objects.filter(account_name=account.account_name,region='cn-south-1'))))
            delete_rds_mysql_s = list(rds_id_all_mysql_s - rds_id_all_s)

            for i in delete_rds_mysql_s:
                Rds.objects.filter(rds_id=i).delete()
    except Exception as e:
        log.logging.error(e)

def deal_south():
    try:
        account_data = Account.objects.all()
        utc_time_now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
        for account in account_data:
            #delete rds
            rds_id_delete_s = list(map(lambda x: x.rds_id, Rds.objects.filter(rds_delete_time__lt=utc_time_now,account_name=account.account_name,region='cn-south-1')))

            for ins in rds_id_delete_s:
                RdsApi(account.tokencn_south_1,'cn-south-1',account.pidcn_south_1).delete_instances(ins)
    except Exception as e:
        log.logging.error(e)

@shared_task
def rds_task():
    sync_rds_north()
#    deal_north()
#    sync_rds_east()
#    deal_east()
#    sync_rds_south()
#    deal_south()
