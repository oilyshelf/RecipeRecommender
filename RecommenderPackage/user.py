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
        if self.disliked_ing is None:
            self.disliked_ing = more
        else:
            self.disliked_ing.extend(more)
        print(self.disliked_ing)

    def update_df(self, in_it):
        self.dataframe = self.dataframe[self.dataframe[self.last_ing] == in_it]

    def update_ing(self, ing):
        self.last_ing = ing

    def is_user(self):
        """Function to see if this user has already a profile

        :return: boolean if user_profile was already created or not
        """
        return self.profile is not None

    def get_session_p(self):
        if self.session_profile is None:
            self.session_profile = self.profile.copy()
        return self.session_profile

    """def closest(lst, K):
        l = np.array([i[1] for i in lst])
        # print(l) 
        idx = (np.abs(l - K)).argmin()
        return lst[idx]

    def dynamic(df, l=5):
       for i in range(l):
            size = df.shape[0]
            percentage_list = [(str(i), df[df[i] == True].shape[0] / size) for i in df.columns]
            temp = closest(percentage_list, 0.5)
            print("Magst du",
                  cur.execute("Select familyName from IngFamily where familyID = ?", (temp[0],)).fetchone()[0], " ?")
            # some input = True , no input = False
            user = bool(input())  # to google api
            # here we need to save result into user class
            df = df[df[temp[0]] == user] 

    """
