#!/bin/bash
kill -9 $(netstat -lantp|grep uwsgi|awk '{print $7}'|awk -F '/' '{print $1}')
