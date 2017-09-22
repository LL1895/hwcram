#_!/usr/bin/python3
# coding: utf-8

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.packages.urllib3.exceptions import InsecurePlatformWarning
import log.log as log

class VpcApi(object):

    def __init__(self,token,region,project_id):
        self.region = region
        self.token = token
        self.project_id = project_id
        self.endpoint = ""
        self.region_list= ["cn-north-1","cn-east-2","cn-south-1","cn-northeast-1"]
        for i in self.region_list:
            if i == self.region:
                self.endpoint = "https://vpc." + i + ".myhwclouds.com"

    def get_public_ip(self):
        self.nozzle = "/v1/" + self.project_id + "/publicips"
        requestUrl = self.endpoint + self.nozzle

        headers = {
            "content-type": "application/json",
            "X-Auth-Token": self.token
        }

        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
        try:
            r = requests.get(requestUrl,headers=headers,verify=False,timeout=10)
            if r.status_code == 200:
                idict = {}
                ilist = r.json()['publicips']
                for i in ilist:
                    private_ip = i['private_ip_address']
                    public_ip = i['public_ip_address']
                    idict[public_ip] = private_ip
                return idict
            else:
                log.logging.error("status_code is " + str(r.status_code) + " not 200,get public ip failed")
        except Exception as e:
            log.logging.error(e)
