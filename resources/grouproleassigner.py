# -*- coding: utf-8 -*-
from .ApiClient import ApiClient, ApiCallError
from .config import Config
import os.path
import csv

class GroupRoleAssigner:
    def __init__(self):
        self.client = ApiClient()
        
    def assignGroupsToRoles(self):
    
        # get the roles as dict and the project_keys as list
        roles, project_keys = self.getData()
    
        role_keys = list(roles.keys())
    
        # do assignment for all projects
        for project_key in project_keys:
        
            # assign all user groups to its role
            for group in Config.user_groups:
                
                group_index = Config.user_groups.index(group)
                role = roles[role_keys[group_index]]
                
                # check if project key is in group name
                if '<project-key>' in group:
                     group = group.replace('<project-key>', project_key)
                
                # assign group to role
                path = "project/{}/role/{}".format(project_key, role)
                
                try:
                    self.client.postData(path, {"group": [group]})
                    print("\nUser group {} has been added to Project Role ID {} for Project Key {}".format(group, role, project_key))
                except ApiCallError as e:
                    print("\nERROR: Could not add User group {} to Project Role ID {} for Project Key {}\nMessage: {}".format(group, role, project_key, e))
           
    def readFile(self):
        
        project_keys = []
        
        with open(os.path.join(os.path.dirname(__file__), os.pardir, 'projects.csv'), 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                
                # all data is in the same column
                if len(row) == 1:
                    project_keys.append(row[0].split(';')[1])
                
                # project key is in the second column
                else:
                   project_keys.append(row[1]) 
                
        print("\n{} projects that will be processed".format(len(project_keys)))
        
        return project_keys
    
    def getData(self):
        
        # get all existing roles
        all_roles = self.client.getData("role")
        
        # store items in dict, key:role_name; value:role_id
        roles = {}
        for x in all_roles:
            if x['name'] in Config.project_roles:
                roles[x['name']] = x['id']
        
        # extract the project keys
        project_keys = self.readFile()
        
        return roles, project_keys