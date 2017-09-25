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
                ilist = r.json()['publicips']
                return ilist
            else:
                log.logging.error("status_code is " + str(r.status_code) + " not 200,get public ip failed")
        except Exception as e:
            log.logging.error(e)

    def create_public_ip(self,ip_type,bandwidth_share_type,ip_address=None,bandwidth_name=None,bandwidth_size=None,bandwidth_share_id=None,bandwidth_charge_mode=None):
        self.ip_type = ip_type
        self.bandwidth_share_type = bandwidth_share_type
        self.ip_address = ip_address
        self.bandwidth_name = bandwidth_name
        self.bandwidth_size = bandwidth_size
        self.bandwidth_share_id = bandwidth_share_id
        self.bandwidth_charge_mode = bandwidth_charge_mode
        self.nozzle = "/v1/" + self.project_id + "/publicips"
        requestUrl = self.endpoint + self.nozzle
        if self.bandwidth_share_type == 'WHOLE':
            if self.ip_address:
                datas = {
                    "publicip":{
                        "type":self.ip_type,
                        "ip_address":self.ip_address,
                    },
                    "bandwidth":{
                        "size":self.bandwidth_size,
                        "id":self.bandwidth_share_id,
                        "share_type":self.bandwidth_share_type,
                    }
                }
            else:
                datas = {
                    "publicip":{
                        "type":self.ip_type,
                    },
                    "bandwidth":{
                        "size":self.bandwidth_size,
                        "id":self.bandwidth_share_id,
                        "share_type":self.bandwidth_share_type,
                    }
                }

        if self.bandwidth_share_type == 'PER':
            if self.ip_address:
                datas = {
                    "publicip":{
                        "type":self.ip_type,
                        "ip_address":self.ip_address,
                    },
                    "bandwidth":{
                        "name":self.bandwidth_name,
                        "size":self.bandwidth_size,
                        "share_type":self.bandwidth_share_type,
                        "charge_mode":self.bandwidth_charge_mode,
                    }
                }
            else:
                datas = {
                    "publicip":{
                        "type":self.ip_type,
                    },
                    "bandwidth":{
                        "name":self.bandwidth_name,
                        "size":self.bandwidth_size,
                        "share_type":self.bandwidth_share_type,
                        "charge_mode":self.bandwidth_charge_mode,
                    }
                }

        headers = {
            "content-type": "application/json",
            "X-Auth-Token": self.token
        }

        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
        try:
            r = requests.post(requestUrl,json=datas,headers=headers,verify=False,timeout=30)
            if r.status_code == 200:
                return r.json()['publicip'],r.status_code
            else:
                return r.json(),r.status_code
                log.logging.error("status_code is " + str(r.status_code) + " not 200,create publicip failed")
        except Exception as e:
            log.logging.error(e)
