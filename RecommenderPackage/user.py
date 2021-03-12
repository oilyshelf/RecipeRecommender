import pandas as pd


class User:
    theromix = None
    disliked_ing = None
    allergies = None
    prefered_tags = None
    profile = None
    gen = None

    def set_thermo(self, has):
        self.theromix = has

    def set_disliked_Ing(self, ingList):
        self.disliked_ing = ingList

    def set_allergies(self, alg):
        self.allergies = alg

    def set_tags(self, tags):
        self.prefered_tags = tags

    def set_userprofile(self, userprofile):
        self.profile = userprofile

    def set_gen(self, gen):
        self.gen = gen

    # user erstellung
    def is_user(self):
        return self.profile is not None
