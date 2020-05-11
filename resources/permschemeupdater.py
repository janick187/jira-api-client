# -*- coding: utf-8 -*-
from .ApiClient import ApiClient, ApiCallError
from .config import Config

class PermSchemeUpdater:
    def __init__(self):
        self.client = ApiClient()

    def updatePermScheme(self):
        # get all projects
        all_projects = self.client.getData("project")

        print("\nAll projects have been retrieved. There are {} projects.\n".format(len(all_projects)))
    
        # assign the new permission scheme to each project
        for element in all_projects:
            key = element['key']

            # assign new scheme
            try:
                path = "project/{}/permissionscheme".format(key)
                self.client.putData(path, {"id": Config.scheme_id})
                print("Assigned permission scheme {} to project {}".format(Config.scheme_id, key))
            except ApiCallError as e:
                print("ERROR: Could not update the permission scheme for Project Key {}\nMessage: {}".format(key, e.message))