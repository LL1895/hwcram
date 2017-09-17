#!/usr/bin/python3
# coding: utf-8

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.packages.urllib3.exceptions import InsecurePlatformWarning
import log.log as log

class TokenApi(object):

    def __init__(self,accountname,username,password,region):
        self.region = region
        self.nozzle = "/v3/auth/tokens"
        self.__username = username
        self.__password = password
        self.__accountname = accountname
        self.region_list= ["cn-north-1","cn-east-2","cn-south-1"]
        self.endpoint = ""
        self.project = ""
        for i in self.region_list:
            if i == self.region:
                self.project = i
                self.endpoint = "https://iam." + i + ".myhwclouds.com"

    def get_token(self):
        requestUrl = self.endpoint + self.nozzle
#        datas = {
#            "auth": {"identity": {"methods": ["password"],
#            "password": {"user": {"name": self.__username,
#            "password": self.__password,
#            "domain": {"name": self.__accountname}}}},
#            "scope": {"domain": {"name": self.__accountname}}}
#        }

        datas = {
            "auth": {"identity": {"methods": ["password"],
            "password": {"user": {"name": self.__username,
            "password": self.__password,
            "domain": {"name": self.__accountname}}}},
            "scope": {"project": {"name": self.project}}}
        }

        headers = {
            "content-type": "application/json",
        }

        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
        try:
            r = requests.post(requestUrl,json=datas,headers=headers,verify=False,timeout=5)
            if r.status_code == 201:
                return r.headers.get("X-Subject-Token")
            else:
                log.logging.error("status_code not 201,get token failed")
        except Exception as e:
            log.logging.error(e)
            log.logging.error("Failed,network problems or parameter errors")
