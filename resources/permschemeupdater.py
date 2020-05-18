# -*- coding: utf-8 -*-
from .ApiClient import ApiClient, ApiCallError
from .config import Config
from .grouproleassigner import GroupRoleAssigner

class PermSchemeUpdater:
    def __init__(self):
        self.client = ApiClient()
        self.fileReader = GroupRoleAssigner()

    def updatePermScheme(self):
        # get all projects
        project_keys = self.fileReader.readFile()

        print("\nAll projects have been retrieved. There are {} projects.\n".format(len(project_keys)))
    
        # assign the new permission scheme to each project
        for key in project_keys:

            # assign new scheme
            try:
                path = "project/{}/permissionscheme".format(key)
                self.client.putData(path, {"id": Config.scheme_id})
                print("Assigned permission scheme {} to project {}".format(Config.scheme_id, key))
            except ApiCallError as e:
                print("ERROR: Could not update the permission scheme for Project Key {}\nMessage: {}".format(key, e.message))