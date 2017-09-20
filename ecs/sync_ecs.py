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

@transaction.atomic
def sync_ecs():
    try:
        for i in account_data:
            ecs_all = EcsApi(i.tokencn_north_1,'cn-north-1',i.pidcn_north_1).get_ecs()
            for k,v in ecs_all.iteritems():
                p = Ecs.objects.create(ecs_name=k,ecs_id=v,region='cn-north-1',account_name=i.account_name,ecs_shut_time=shut_time,ecs_delete_time=delete_time)
                #p.save()
    except Exception as e:
        log.logging.error(e)

sync_ecs()
