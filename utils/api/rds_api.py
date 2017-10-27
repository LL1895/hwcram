#_!/usr/bin/python3
# coding: utf-8

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.packages.urllib3.exceptions import InsecurePlatformWarning
import log.log as log

class RdsApi(object):

    def __init__(self,token,region,project_id):
        self.region = region
        self.token = token
        self.project_id = project_id
        self.endpoint = ""
        self.region_list= ["cn-north-1","cn-east-2","cn-south-1","cn-northeast-1"]
        for i in self.region_list:
            if i == self.region:
                self.endpoint = "https://rds." + i + ".myhwclouds.com"

    def get_versions(self):
        self.nozzle = "/rds/"
        requestUrl = self.endpoint + self.nozzle

        headers = {
            "content-type": "application/json",
            "X-Auth-Token": self.token
        }

        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
        try:
            r = requests.get(requestUrl,headers=headers,verify=False,timeout=20)
            if r.status_code == 200:
                #ilist = r.json()['publicips']
                return r.json()
            else:
                log.logging.error("status_code is " + str(r.status_code) + " not 200,get rds versions failed")
        except Exception as e:
            log.logging.error(e)

    def get_instances(self):
        self.nozzle = "/rds/v1/" + self.project_id + "/instances"
        requestUrl = self.endpoint + self.nozzle

        headers = {
            "content-type": "application/json",
            "X-Auth-Token": self.token,
            "X-Language": "en-us",
        }

        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
        try:
            r = requests.get(requestUrl,headers=headers,verify=False,timeout=20)
            if r.status_code == 200:
                ilist = r.json()['instances']
                for i in ilist:
                    i.pop('nics')
                    i.pop('vpc')
                    i.pop('securityGroup')
                    i.pop('flavor')
                    i.pop('volume')
                    i.pop('dataStoreInfo')
                    i.pop('updated')
                    i.pop('availabilityZone')
                    i.pop('created')
                    i.pop('region')
                return ilist
            else:
                log.logging.error("status_code is " + str(r.status_code) + " not 200,get rds instances failed")
        except Exception as e:
            log.logging.error(e)

    def delete_instances(self,instanceid):
        self.instanceid = instanceid
        self.nozzle = "/rds/v1/" + self.project_id + "/instances/" + self.instanceid
        requestUrl = self.endpoint + self.nozzle

        headers = {
            "content-type": "application/json",
            "X-Auth-Token": self.token,
            "X-Language": "en-us",
        }

        datas = {"keepLastManualBackup": "0"}

        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
        try:
            r = requests.delete(requestUrl,json=datas,headers=headers,verify=False,timeout=20)
            if r.status_code == 200 or r.status_code == 202:
                return r.json()
            else:
                log.logging.error("status_code is " + str(r.status_code) + " not 200,delete rds instances failed")
        except Exception as e:
            log.logging.error(e)
