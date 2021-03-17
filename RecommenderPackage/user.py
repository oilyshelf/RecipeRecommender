# -*- coding: utf-8 -*-
"""User-module

holds the User class which safes all necessary user-related information´s

@authors Rostislav Iskandirov(oilyshelf), Ali Gökkaya(ScarxFace06)
"""


class User:
    theromix = None
    disliked_ing = None
    allergies = None
    preferred_tags = None
    profile = None
    gen = None
    last = None

    def set_thermo(self, has):
        self.theromix = has

    def set_disliked_ing(self, ing_list):
        self.disliked_ing = ing_list

    def set_allergies(self, alg):
        self.allergies = alg

    def set_tags(self, tags):
        self.preferred_tags = tags

    def set_userprofile(self, userprofile):
        self.profile = userprofile

    def set_gen(self, gen):
        self.gen = gen

    def is_user(self):
        """Function to see if this user has already a profile

        :return: boolean if user_profile was already created or not
        """
        return self.profile is not None
