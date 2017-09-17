#!/bin/bash
fun_uwsgi(){
    uwsgi_name=$(netstat -lnpt|grep uwsgi |awk  '{print $7 }'|awk -F '/' '{print $2}')
    if  [ "$uwsgi_name" = 'uwsgi' ];then
        exit 0
    else
        /usr/bin/uwsgi --ini /opt/hwcram/hwcram_uwsgi.ini -d /var/log/hwcram/uwsgi.log
    fi
}

for((i=1;i<=6;i++));do
    fun_uwsgi
    sleep 10
done
