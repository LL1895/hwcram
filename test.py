'''ddd'''
import os
import sys
import datetime
import django
from api.rds_api import RdsApi
from api.verify_api import VerifyApi

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hwcram.settings")

django.setup()
from account.models import Account

#ACCOUNT_DATA = Account.objects.filter(account_name='zhangxuesu')
ACCOUNT_DATA = Account.objects.all()
#UTC_TIME_NOW = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)

#def get_token():
#    '''ddd'''
#    for i in ACCOUNT_DATA:
#        return i.tokencn_north_1
#
#def get_pid():
#    '''ddd'''
#    for i in ACCOUNT_DATA:
#        return i.pidcn_north_1
#
#ITOKEN = get_token()
#IPID = get_pid()
##mm = EcsApi(itoken,'cn-north-1',ipid).get_ecs_test()
##NNN = RdsApi(ITOKEN, 'cn-north-1', IPID).get_instances()
#NNN = VerifyApi(ITOKEN, 'cn-north-1', IPID).get_regions()
#print(type(NNN))
def token_verify():
    '''dd'''
    try:
        account_data = Account.objects.all()
        for account in account_data:
            ilist = {}
            resp_north = VerifyApi(
                account.tokencn_north_1,
                'cn-north-1',
                account.pidcn_north_1).get_projects()
            resp_east = VerifyApi(
                account.tokencn_east_2,
                'cn-east-2',
                account.pidcn_east_2).get_projects()
            resp_south = VerifyApi(
                account.tokencn_south_1,
                'cn-south-1',
                account.pidcn_south_1).get_projects()
            ilist = {resp_north, resp_east, resp_south}
            return ilist
            for i in ilist:
                print(i)
                    #account.save()
    except Exception as e:
        log.logging.error(e)
        log.logging.error("Failed to verify_token")
print(token_verify())
