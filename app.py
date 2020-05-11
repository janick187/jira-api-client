# -*- coding: utf-8 -*-
'''
Author: Janick Spirig, janick.spirig@beecom.ch
Date: March 2020

This program's aim is to assign specific jira user groups to their related jira project roles for all projects of a jira instance

NOTE: Before this program can be executed some packages have to be installed first. To do so
- 1. Install pip
- 2. run the following command on the terminal: pip install -r /path/to/requirements.txt (adjust path)
'''

from resources import *
from sys import argv

def main():
    
    # assign user groups to project roles
    if argv[1] == 'EAD': 
        execution = UserDataExtractor()
        execution.extractProjectAdmins()
    
    # assign user groups to project roles
    if argv[1] == 'G2R':
        
        execution = GroupRoleAssigner()
        execution.assignGroupsToRoles()
    
    # extract target user-role memberships
    elif argv[1] == 'EUD':
        
        execution = UserDataExtractor()
        execution.printGroupMemberships()

    elif argv[1] == "UPS":
        execution = PermSchemeUpdater()
        execution.updatePermScheme()
    
if __name__ == '__main__':
    main()