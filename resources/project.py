# -*- coding: utf-8 -*-
from .config import Config
from .Role import Role

class Project:
    def __init__(self, key, name):
        self.key = key
        self.name = name
        self.roles = []
        
    def addRole(self, role):
        self.roles.append(role)
        
    def assignNewRoles(self):
        read_only = Role(0, Config.target_roles[2])
        admins = Role(1, Config.target_roles[0])
        contributors = Role(2, Config.target_roles[1])
 
        for role in self.roles:
            if role.name in Config.readonly_roles:
                read_only.users += role.users
                
            elif role.name in Config.admin_roles:
                admins.users += role.users
            else:
                contributors.users += role.users
        
        # remove duplicates
        read_only.clearDuplicates()
        admins.clearDuplicates()
        contributors.clearDuplicates()
        
        self.newroles = [read_only, admins, contributors]