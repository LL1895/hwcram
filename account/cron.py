import os
import sys
import django
from datetime import datetime
from datetime import timezone
import log.log as log

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hwcram.settings")

django.setup()
from account.models import Account

account_data = Account.objects.all()
utc_time_now = datetime.utcnow().replace(tzinfo=timezone.utc)

def update_token():
    try:
        for i in account_data:
            if utc_time_now > i.token_up_time:
                i.save()
    except Exception as e:
        log.logging.error(e)
        log.logging.error("Failed to update_token")
