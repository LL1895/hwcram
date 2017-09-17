#_!/usr/bin/python3
# coding: utf-8

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.packages.urllib3.exceptions import InsecurePlatformWarning
import log.log as log

class EcsApi(object):

    def __init__(self,token,region,project_id):
        self.region = region
        self.token = token
        self.project_id = project_id
        self.endpoint = ""
        self.region_list= ["cn-north-1","cn-east-2","cn-south-1","cn-northeast-1"]
        for i in self.region_list:
            if i == self.region:
                self.endpoint = "https://ecs." + i + ".myhwclouds.com"

    def get_ecs_count(self):
        self.nozzle = "/v2/" + self.project_id + "/servers"
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
                return str(r.text).count("links")
            else:
                log.logging.error("status_code is " + str(r.status_code) + " not 200,get ecs count failed")
        except Exception as e:
            log.logging.error(e)

    def get_active_ecs_count(self):
        self.nozzle = "/v2/" + self.project_id + "/servers?status=ACTIVE"
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
                return str(r.text).count("links")
            else:
                log.logging.error("status_code is " + str(r.status_code) + " not 200,get active ecs count failed")
        except Exception as e:
            log.logging.error(e)

    def get_ecs(self,ecs_name=None):
        self.nozzle = "/v2/" + self.project_id + "/servers"
        self.ecs_name = ecs_name
        if self.ecs_name != None:
            self.nozzle = "/v2/" + self.project_id + "/servers?name=" + self.ecs_name
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
                ilist = r.json()['servers']
                for i in range(0,len(ilist)):
                    idict[ilist[i]['name']] = ilist[i]['id']
                return idict
            else:
                log.logging.error("status_code is " + str(r.status_code) + " not 200,get ecs failed")
        except Exception as e:
            log.logging.error(e)

    def get_active_ecs(self,ecs_name=None):
        self.nozzle = "/v2/" + self.project_id + "/servers?status=ACTIVE"
        self.ecs_name = ecs_name
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
                ilist = r.json()['servers']
                idict = {}
                idict_name = {}
                for i in range(0,len(ilist)):
                    idict[ilist[i]['name']] = ilist[i]['id']
                if self.ecs_name in idict.keys():
                    idict_name[self.ecs_name] = idict[self.ecs_name]
                    return idict_name
                else:
                    return idict
            else:
                log.logging.error("status_code is " + str(r.status_code) + " not 200,get active ecs failed")
        except Exception as e:
            log.logging.error(e)

    def get_shutoff_ecs(self,ecs_name=None):
        self.nozzle = "/v2/" + self.project_id + "/servers?status=SHUTOFF"
        self.ecs_name = ecs_name
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
                ilist = r.json()['servers']
                idict = {}
                idict_name = {}
                for i in range(0,len(ilist)):
                    idict[ilist[i]['name']] = ilist[i]['id']
                if self.ecs_name in idict.keys():
                    idict_name[self.ecs_name] = idict[self.ecs_name]
                    return idict_name
                else:
                    return idict
            else:
                log.logging.error("status_code is " + str(r.status_code) + " not 200,get shutoff ecs failed")
        except Exception as e:
            log.logging.error(e)

    def delete_ecs(self,ecs_id,delete_ip="true",delete_volume="true"):
        if isinstance(ecs_id,str):
            self.ecs_id = list(ecs_id.split(None))
        else:
            self.ecs_id = ecs_id
        self.nozzle = "/v1/" + self.project_id + "/cloudservers/delete"
        self.delete_ip = delete_ip
        self.delete_volume = delete_volume
        requestUrl = self.endpoint + self.nozzle

        datas_ecs_id_value = []
        for i in range(0,len(self.ecs_id)):
            locals()['tmpdict%s' %i] = {"id":self.ecs_id[i]}
            datas_ecs_id_value.append(locals()['tmpdict%s' %i])

        datas = {"servers":datas_ecs_id_value,"delete_publicip":self.delete_ip,"delete_volume":self.delete_volume}

        headers = {
            "content-type": "application/json",
            "X-Auth-Token": self.token
        }

        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
        try:
            r = requests.post(requestUrl,json=datas,headers=headers,verify=False,timeout=10)
            if r.status_code == 200:
                return r.json()
            else:
                log.logging.error("status_code is " + str(r.status_code) + " not 200,delete ecs failed")
        except Exception as e:
            log.logging.error(e)

    def shutoff_ecs(self,ecs_id,stop_type="HARD"):
        if isinstance(ecs_id,str):
            self.ecs_id = list(ecs_id.split(None))
        else:
            self.ecs_id = ecs_id

        self.stop_type = stop_type
        self.nozzle = "/v1/" + self.project_id + "/cloudservers/action"
        requestUrl = self.endpoint + self.nozzle

        datas_ecs_id_value = []
        for i in range(0,len(self.ecs_id)):
            locals()['tmpdict%s' %i] = {"id":self.ecs_id[i]}
            datas_ecs_id_value.append(locals()['tmpdict%s' %i])

        datas = {"os-stop":{"type":self.stop_type,"servers":datas_ecs_id_value}}

        headers = {
            "content-type": "application/json",
            "X-Auth-Token": self.token
        }

        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
        try:
            r = requests.post(requestUrl,json=datas,headers=headers,verify=False,timeout=10)
            if r.status_code == 200:
                return r.json()
            else:
                log.logging.error("status_code is " + str(r.status_code) + " not 200,shutoff ecs failed")
        except Exception as e:
            log.logging.error(e)

    def get_private_ip(self,server_id):
        self.server_id = server_id
        self.nozzle = "/v2/" + self.project_id + "/servers/" + self.server_id
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
                return r.json()
                #idict = {}
                #ilist = r.json()['servers']
                #for i in range(0,len(ilist)):
                #    idict[ilist[i]['name']] = ilist[i]['id']
                #return idict
            else:
                log.logging.error("status_code is " + str(r.status_code) + " not 200,get private ip failed")
        except Exception as e:
            log.logging.error(e)
