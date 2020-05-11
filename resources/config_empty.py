# -*- coding: utf-8 -*-
class Config:
    
    #### JIRA INSTANCE CONFIG ####
    username = ''
    password = ''
    instance = ''
    
    ##### ASSIGN GROUPS TO ROLES ##### 
    
    # existing project roles
    project_roles = []

    # existing user groups -> group in user_groups at index position x will be associated to role at index position x in project_roles
    user_groups = []
    
    ##### EXTRACT TARGET USER-ROLE MEMBERSHIPS ##### 
    
    # JIRA roles to be marked as read-only
    readonly_roles = []
    
    # JIRA roles to be marked as admin -> all other roles will be assigned to group "Contributors"
    admin_roles = []
    
    # JIRA target roles, the roles under which the users will be listed in the output file
    target_roles = []

    ##### UPDATE PROJECT PERMISSION SCHEME #####
    # id of the permission scheme that should be assigned to all projects
    scheme_id = 