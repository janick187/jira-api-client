# -*- coding: utf-8 -*-
from .ApiClient import ApiClient, ApiCallError
from .config import Config
from .Role import Role
from .user import User
from .project import Project
from .Group import Group
import csv
import os.path

class UserDataExtractor:
    def __init__(self):
        self.client = ApiClient()
        self.usergroups = []
        
    def extractProjectAdmins(self):
        
        print("\nRetrieving all project data...\n")
        
        projects = []
        
        # get all the existing project
        try:
            all_projects = self.client.getData("project?expand=lead")
        except ApiCallError as e:            
            print("Error: Not able to retrieve project data: {}".format(e.message))
            exit()
            
        print("\nAll projects have been retrieved. There are {} projects.\n".format(len(all_projects)))
        
        for element in all_projects:
            # extract project admin of each project
            
            print("Processing projkect {}.\n".format(element['key']))
            
            project = Project(element['key'], element['name'])
            
            role1 = Role(999, 'administrators')
            role2 = Role(999, 'contributors')
            
            user = User(element['lead']['name'])
            
            role1.users.append(user)
            role2.users.append(user)
            
            project.addRole(role1)
            project.addRole(role2)
            
            # each project has a list with all roles. Each role has a list with all users which are part of this role.
            self.writeAdminFile(project)
    
    def printGroupMemberships(self):
        
        print("\nRetrieving all project data...\n")
        
        projects = []
        
        # get all the existing project
        try:
            all_projects = self.client.getData("project")
        except ApiCallError as e:            
            print("Error: Not able to retrieve project data: {}".format(e.message))
            exit()
            
        print("\nAll projects have been retrieved. There are {} projects.\n".format(len(all_projects)))
        
        for element in all_projects:
            project = Project(element['key'], element['name'])
            
            print("\nRetreiving user data for project {}\n".format(project.key))
            
            # get roles of project
            try:
                all_roles = self.client.getData("project/{}/role".format(project.key))
            except ApiCallError as e:
                if e.code == 404:
                    print("Error: Could not retrieve project {}: {}".format(project.name, e.message))
                    continue
                else:
                    print("Error: ".format(e.message))
                    break
                
            for key, value in all_roles.items():
                
                try:
                    role_data = self.client.getDataFromUrl(value)
                    
                    role = Role(role_data['id'], role_data['name'])
                    
                    self.addUsersToRole(role, role_data['actors'])
                    
                    project.addRole(role)
                
                except ApiCallError as e:
                    print("Error: Not able to retrieve single role data: {}".format(e.message))
                    break
                
            project.assignNewRoles()
            projects.append(project)
            # each project has a list with all roles. Each role has a list with all users which are part of this role.
            self.writeFile(project)
            
        # add last line to file with all users that are read-only
        d_role = Role(99, Config.target_roles[2])
        
        for p in projects:
            try:
                d_role.users += p.newroles[0].users
            # when project does not have any read-only users
            except IndexError:
                pass
        
        d_role.clearDuplicates()
        d_project = Project("dummy", "dummy_p")
        d_project.newroles = [d_role]
        self.writeFile(d_project)

    def addUsersToRole(self, role, data):
        
        for actor in data:
            # single user
            if actor['type'] == 'atlassian-user-role-actor':
                role.addUser(actor['name'])
            # user group
            else:
                
                if not any(x.name == actor['name'] for x in self.usergroups):
                    print("Group {} does not exist yet".format(actor['name']))
                    
                    print("Retrieving group data for group {}".format(actor['name']))
                    
                    try:
                        groupdata = self.client.getData("group/member", {"groupname":actor['name'], })
                        
                        group = Group(actor['name'])
                        for u in groupdata['values']:
                            if role.addUser(u['name']):
                                group.users.append(u['name'])
                        self.usergroups.append(group)
                                
                    except ApiCallError as e:
                        if e.code == 404:
                            print("Error: Could not retrieve user group {}: {}".format(actor['name'], e.message))
                            pass
                        else:
                            print("Error: ".format(e.message))
                            break
                else:
                    for group in self.usergroups:
                        if group.name == actor['name']:
                            print("Group {} exists already!".format(group.name))
                            for u in group.users:
                                role.addUser(u)
                            break
      
    def writeAdminFile(self, project):
        fname = 'group_admins.csv'
        
        if not os.path.isfile(fname):
            self.createAdminFile(fname)
        
        print("Writing to output file...\n")
        
        row_list = []
        
        for role in project.roles:
            
            user_string = ",".join([str(user.name) for user in role.users])
            
            row_list.append(["{};{}.{}.{};{}".format(project.name, "eng.jir", project.key, role.name, user_string)])
                    
        with open(fname, 'a+', newline='') as file:
            writer = csv.writer(file)
            for row in row_list:
                writer.writerow(row)
                
        print("Written to Output file\n")

    def writeFile(self, project):
        fname = 'groups_usernames.csv'
        
        if not os.path.isfile(fname):
            self.createFile(fname)
        
        print("Writing to output file...\n")
        
        row_list = []
        
        key = project.key
        for role in project.newroles:
            if "licensed" not in role.name:
                user_string = ",".join([str(user.name) for user in role.users])
                row_list.append(["{}.{}.{};{}".format("eng.jir", key, role.name, user_string)])
            else:
                if key == "dummy":
                    user_string = ",".join([str(user.name) for user in role.users])
                    row_list.append(["{}.{};{}".format("eng.jir", role.name, user_string)])
                    
        with open('groups_usernames.csv', 'a+', newline='') as file:
            writer = csv.writer(file)
            for row in row_list:
                writer.writerow(row)
                
        print("Written to Output file\n")
        
    def createFile(self, fname):
        print("\nCreating output file...\n".format(fname))
        
        row_list = [["ad_group_name;group_members_usernames"]]
        
        with open('groups_usernames.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for row in row_list:
                writer.writerow(row)  

        print("Output file created: {}\n".format(fname))
        
        
    def createAdminFile(self, fname):
        print("\nCreating output file...\n".format(fname))
        
        row_list = [["project_name;ad_group_name;lead"]]
        
        with open(fname, 'w', newline='') as file:
            writer = csv.writer(file)
            for row in row_list:
                writer.writerow(row)  

        print("Output file created: {}\n".format(fname))