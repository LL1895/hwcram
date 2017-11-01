#_!/usr/bin/python3
# coding: utf-8

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.packages.urllib3.exceptions import InsecurePlatformWarning
import log.log as log

class VerifyApi(object):

    def __init__(self,token,region,project_id):
        self.region = region
        self.token = token
        self.project_id = project_id
        self.endpoint = ""
        self.region_list= ["cn-north-1","cn-east-2","cn-south-1","cn-northeast-1"]
        for i in self.region_list:
            if i == self.region:
                self.endpoint = "https://ecs." + i + ".myhwclouds.com"

    def get_status_code(self):
        self.nozzle = "/v2/" + self.project_id + "/servers"
        requestUrl = self.endpoint + self.nozzle

        headers = {
            "content-type": "application/json",
            "X-Auth-Token": self.token
        }

        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
        try:
            r = requests.get(requestUrl,headers=headers,verify=False,timeout=20)
            return r.status_code
        except Exception as e:
            log.logging.error(e)
