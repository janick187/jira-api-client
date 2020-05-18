# -*- coding: utf-8 -*-
from .config import Config
import requests
from requests.auth import HTTPBasicAuth
import json

class ApiClient():
    def __init__(self):
        # load credentials for API uathentication from text file
        self.user = Config.username
        self.user_pass = Config.password
        self.url = Config.instance + '/rest/api/2'
        
    def processResponse(self, r):
        if r.status_code == 200:
            return r.json()
        elif r.status_code == 204:
            pass 
        else:
            exception = ApiCallError(r.json(), r.status_code)
            raise exception
    
    def getData(self, resource, params=None):
        if params == None: 
            return self.processResponse(requests.get("{}/{}".format(self.url,resource), auth=HTTPBasicAuth(self.user, self.user_pass)))
        else:
            return self.processResponse(requests.get("{}/{}".format(self.url,resource), auth=HTTPBasicAuth(self.user, self.user_pass), params=params))
        
    def postData(self, resource, data_dict):
        return self.processResponse(requests.post("{}/{}".format(self.url,resource), auth=HTTPBasicAuth(self.user, self.user_pass), json=data_dict))

    def deleteData(self, resource, params=None):
        if params == None:
            return self.processResponse(requests.delete("{}/{}".format(self.url,resource), auth=HTTPBasicAuth(self.user, self.user_pass)))
        else:
            return self.processResponse(requests.delete("{}/{}".format(self.url,resource), auth=HTTPBasicAuth(self.user, self.user_pass), params=params))

    def putData(self, resource, data_dict):
        return self.processResponse(requests.put("{}/{}".format(self.url,resource), auth=HTTPBasicAuth(self.user, self.user_pass), json=data_dict))
    
    def getDataFromUrl(self, url):
        return self.processResponse(requests.get(url, auth=HTTPBasicAuth(self.user, self.user_pass)))

class ApiCallError(Exception):
    def __init__(self, *args):
        self.body = args[0]
        self.message = self.body["errorMessages"][0]
        self.code = args[1]