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
    session_profile = None
    gen = None
    last = None
    last_ing = None
    counter = 0

    def __init__(self, dataframe):
        self.dataframe = dataframe

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

    def extend_disliked(self, more):
        """
        adds items to disliked list and creates one if its not init
        """
        if self.disliked_ing is None:
            self.disliked_ing = more
        else:
            self.disliked_ing.extend(more)
        print(self.disliked_ing)

    def update_df(self, in_it):
        """ updates dataframe on the fact if user liked the last item or not"""
        self.dataframe = self.dataframe[self.dataframe[self.last_ing] == in_it]

    def update_ing(self, ing):
        self.last_ing = ing

    def is_user(self):
        """Function to see if this user has already a profile

        :return: boolean if user_profile was already created or not
        """
        return self.profile is not None

    def get_session_p(self):
        """returns users session_profile if it exist if not copys the user_profile 
        :return: users session_profile<pandas:series>
        """
        if self.session_profile is None:
            self.session_profile = self.profile.copy()
        return self.session_profile

   
