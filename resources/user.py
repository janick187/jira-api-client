# -*- coding: utf-8 -*-
class User:
    def __init__(self, name):
        self.name = name
        
    def __hash__(self):
        return hash(self.name)