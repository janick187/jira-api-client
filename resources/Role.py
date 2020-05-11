# -*- coding: utf-8 -*-
from .ApiClient import ApiClient, ApiCallError
from .user import User

class Role:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.users = []
        self.client = ApiClient()
        
    def addUser(self, name):
        user_ok = True
        
        # check if username starts with e, E, h or H
        if name.startswith('e') or name.startswith('E') or name.startswith('h') or name.startswith('H'):
            # check if first letter is followed by 6 digits
            try:
                int(name[1:7])
                user_ok = False
            except ValueError:
                pass
        if user_ok:
            user = User(name)
            self.users.append(user)
            print("Done with user {}".format(user.name))
            return True
        else:
            print("User {} will be ignored as the usersname starts with e, E, h or H followed by 6 digits".format(name))
        
                
    def clearDuplicates(self):
        self.users = list({tuple(user.name): user  for user in self.users}.values())