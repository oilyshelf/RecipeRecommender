import RecommenderPackage.databaseConnection


class Recommender:
    def __init__(self):
        # TODO init the recommender
        self.db = RecommenderPackage.databaseConnection.DataBase()


    def knowledge_recom(self):
        # TODO
        return

    def contend_recom(self):
        # TODO
        return

    def create_userProfile(self):
        # TODO
        return

#testing

if __name__ == '__main__':
    r = Recommender()
