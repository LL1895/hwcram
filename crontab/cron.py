import subprocess

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
