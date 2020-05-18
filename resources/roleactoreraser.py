# -*- coding: utf-8 -*-
from .ApiClient import ApiClient, ApiCallError
from .config import Config
from .grouproleassigner import GroupRoleAssigner

class RoleActorEraser:
    def __init__(self):
        self.client = ApiClient()
        self.fileReader = GroupRoleAssigner()

    def deleteRoleActors(self):
        # get all projects
        project_keys = self.fileReader.readFile()

        print("\nAll projects have been retrieved. There are {} projects.\n".format(len(project_keys)))
    
        # delete role actor for each project
        for key in project_keys:

            role_id = Config.role_id
            path = "project/{}/role/{}".format(key, role_id)

            # get all actors of role
            try:
                print("Get role data of role {} for project {}".format(role_id, key))
                data = self.client.getData(path)
            except ApiCallError as e:
                print("ERROR: Could not get role data for Project Key {}\nMessage: {}".format(key, e.message))

            if len(data['actors']) > 0:
                for actor in data['actors']:
                    if actor['type'] == 'atlassian-group-role-actor':
                        # actor is a group, delete group from role
                        try:
                            self.client.deleteData(path, {'group' : actor['name']})
                            print("Group {} has been deleted from role {} in project {}".format(actor['name'], role_id, key))
                        except ApiCallError as e:
                            print("ERROR: Could not delete group {} from role {} in project {}\nMessage: {}".format(actor['name'], role_id, key, e.message))
                    else: 
                        # actor is a single user
                        try:
                            user_key = self.client.getData("user", {'username': actor['name']})['key']
                            print(user_key)
                            self.client.deleteData(path, {'user' : user_key})
                            print("User {} with key {} has been deleted from role {} in project {}".format(actor['name'], user_key, role_id, key))
                        except ApiCallError as e:
                            print("ERROR: Could not delete user {} from role {} in project {}\nMessage: {}".format(actor['name'], role_id, key, e.message))
            else:
                print("No actors in role {} for project {}".format(role_id, key))