import os
import sys
import django
import datetime
from api.ecs_api import EcsApi
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

account_data = Account.objects.all()
utc_time_now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)

def update_token():
    try:
        for i in account_data:
            if utc_time_now > i.token_up_time:
                i.save()
    except Exception as e:
        log.logging.error(e)
        log.logging.error("Failed to update_token")

def cron_nginx():
    retcode_nginx = subprocess.call("netstat -lnpt|grep nginx|grep -v grep",shell=True)
    if retcode_nginx == 1:
        subprocess.call("/usr/sbin/nginx",shell=True)

def cron_uwsgi():
    retcode_uwsgi = subprocess.call("netstat -lnpt|grep uwsgi|grep -v grep",shell=True)
    if retcode_uwsgi == 1:
        subprocess.call("/usr/bin/uwsgi --ini /opt/hwcram/hwcram_uwsgi.ini -d /var/log/hwcram/uwsgi.log",shell=True)

def cron_celery():
    retcode_celery = subprocess.call("ps -ef|grep '/usr/local/python3/bin/python3.6 -m celery worker'|grep -v grep",shell=True)
    if retcode_celery == 1:
        subprocess.call("/etc/init.d/celeryd start",shell=True)

def cron_celerybeat():
    retcode_celerybeat = subprocess.call("ps -ef|grep '/usr/local/bin/celery beat'|grep -v grep",shell=True)
    if retcode_celerybeat == 1:
        subprocess.call("/etc/init.d/celerybeat start",shell=True)
