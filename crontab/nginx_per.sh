#!/bin/bash
fun_nginx(){
    nginx_name=$(netstat -lnpt |grep nginx|awk -F ' ' {'print $7'}|awk -F '/' {'print $2'})
    if  [ "$nginx_name" = 'nginx' ];then
        exit 0
    else
        /usr/sbin/nginx
    fi
}

for((i=1;i<=6;i++));do
    fun_nginx
    sleep 10
done
