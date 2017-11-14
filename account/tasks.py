from __future__ import absolute_import
import datetime
from celery import shared_task
import log.log as log
from account.models import Account
from api.verify_api import VerifyApi

@shared_task
def token_task():
    '''dd'''
    try:
        account_data = Account.objects.all()
        utc_time_now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
        for account in account_data:
            if utc_time_now > account.token_up_time:
                account.save()
    except Exception as e:
        log.logging.error(e)
        log.logging.error("Failed to update_token")

@shared_task
def token_verify():
    '''dd'''
    try:
        account_data = Account.objects.all()
        for account in account_data:
            iset = {}
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
            iset = {resp_north, resp_east, resp_south}
            for i in iset:
                if i != 200:
                    account.save()
    except Exception as e:
        log.logging.error(e)
        log.logging.error("Failed to verify_token")
