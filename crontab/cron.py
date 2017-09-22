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
    retcode_nginx = subprocess.call("netstat -lnpt|grep nginx",shell=True)
    if retcode_nginx == 1:
        subprocess.call("/usr/sbin/nginx",shell=True)

def cron_uwsgi():
    retcode_uwsgi = subprocess.call("netstat -lnpt|grep uwsgi",shell=True)
    if retcode_uwsgi == 1:
        subprocess.call("/usr/bin/uwsgi --ini /opt/hwcram/hwcram_uwsgi.ini -d /var/log/hwcram/uwsgi.log",shell=True)

def cron_hwcram():
    retcode_hwcram = subprocess.call("ps -ef|grep hwcram.py|grep -v grep",shell=True)
    if retcode_hwcram == 1:
        subprocess.call("nohup /usr/bin/python3 /opt/hwcram/utils/hwcram.py > /dev/null 2>&1 &",shell=True)
