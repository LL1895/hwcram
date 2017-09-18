import os
import sys
import django
from datetime import datetime
from datetime import timezone

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hwcram.settings")

django.setup()
from account.models import Account
from ecs.models import Ecs

account_data = Account.objects.all()
utc_time_now = datetime.utcnow().replace(tzinfo=timezone.utc)

def update_token():
#    for i in account_data:
#        print(i.token_up_time)
#    for 
    pass

