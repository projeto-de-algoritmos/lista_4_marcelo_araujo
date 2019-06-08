from functions import *
import tkinter as tk

class Show:
    def __init__(self, show_id, name, rate=-1):
        self.id = show_id
        self.name = name
        self.rate = rate

class User:
    def __init__(self, idu, name, rated_shows=[]):
        self.id = idu
        self.name = name
        self.rated_shows = rated_shows

class Intersec:
    def __init__(self, show_id, user_rate, comp_rate):
        self.show_id = show_id
        self.user_rate = user_rate
        self.comp_rate = comp_rate

class ComparedUsers:
    def __init__(self, other_user, intersec_shows):
        self.other_user = other_user
        self.sorted_intersec = sorted(intersec_shows, key=lambda x: x.comp_rate)
        self.invertions = do_count_invert(self.sorted_intersec)
        max_inverts = get_max_inverts(len(self.sorted_intersec))
        
        if(max_inverts != 0):
            self.match_percentage = ((max_inverts-self.invertions)/float(max_inverts))*100
        else:
            self.match_percentage = 0

