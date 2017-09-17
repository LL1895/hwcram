import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hwcram.settings")

django.setup()
from account.models import Account

#p = Account.save(account_name='dwxoiiaiiisd',user_name='asdsad',password='pas',pidcn_north_1='sadasa',pidcn_east_2='asdaad',pidcn_south_1='adsad')
#p.save()

def sync_token():
    print('i love you')
