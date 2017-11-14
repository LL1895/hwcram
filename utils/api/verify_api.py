#!/usr/bin/python3
# coding: utf-8

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.packages.urllib3.exceptions import InsecurePlatformWarning
import log.log as log

class VerifyApi(object):
    '''dd'''
    def __init__(self, token, region, project_id):
        self.region = region
        self.token = token
        self.project_id = project_id
        self.endpoint = ""
        self.region_list= ["cn-north-1", "cn-east-2", "cn-south-1", "cn-northeast-1"]
        for i in self.region_list:
            if i == self.region:
                self.endpoint = "https://iam." + i + ".myhwclouds.com"

    def get_regions(self):
        '''dd'''
        self.nozzle = "/v3/" + "regions"
        request_url = self.endpoint + self.nozzle

        headers = {
            "content-type": "application/json",
            "X-Auth-Token": self.token
        }

        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
        try:
            resp = requests.get(request_url, headers=headers, verify=False, timeout=20)
            return resp.status_code
        except Exception as e:
            log.logging.error(e)

    def get_projects(self):
        '''dd'''
        self.nozzle = "/v3/" + "projects"
        request_url = self.endpoint + self.nozzle

        headers = {
            "content-type": "application/json",
            "X-Auth-Token": self.token
        }

        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
        try:
            resp = requests.get(request_url, headers=headers, verify=False, timeout=20)
            return resp.status_code
        except Exception as e:
            log.logging.error(e)
