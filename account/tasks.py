from __future__ import absolute_import
from celery import shared_task
import log.log as log
from account.models import Account
import datetime

@shared_task
def token_task():
    try:
        account_data = Account.objects.all()
        utc_time_now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
        for account in account_data:
            if utc_time_now > account.token_up_time:
                account.save()
    except Exception as e:
        log.logging.error(e)
        log.logging.error("Failed to update_token")
