import os
import sys
import django
import datetime
from api.ecs_api import EcsApi
from api.vpc_api import VpcApi
import log.log as log
from multiprocessing import Pool
from time import sleep
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hwcram.settings")

django.setup()
from django.db import transaction
from account.models import Account
from ecs.models import Ecs
from vpc.models import Createip
from api.ecs_api import EcsApi
from api.verify_api import VerifyApi

account_data = Account.objects.filter(account_name='hwcloudstam')
utc_time_now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
createip_data = Createip.objects.all()

def get_token():
    for i in account_data:
        return i.tokencn_north_1

def get_pid():
    for i in account_data:
        return i.pidcn_north_1

itoken = get_token()
ipid = get_pid()
mm = VerifyApi(itoken,'cn-north-1',ipid).get_status_code()
print(mm)
