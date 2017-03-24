class TwitterGraph:
    def __init__(self, handlers, levels):
        self.api_handler = handlers["twitter"]
        self.neo4j_handler = handlers["neo4j"]
        self.levels = levels
        self.initial_users = {"pecey01"}
        self.visited_users = set()
        self.users = self.neo4j_handler.labels.create("User")

    def create_node(self,user):
        user_node = self.neo4j_handler.nodes.create(twitter_id = user.id, twitter_login = user.screen_name)
        self.users.add(user_node)
        self.visited_users.add(user.id)

    def create_relationship(self,source, destination, relation):
        source_node = self.users.get(twitter_id = source.id)[0]
        destination_node = self.users.get(twitter_id = destination.id)[0]
        source_node.relationships.create(relation, destination_node)

    def plot_self(self,user):
        self.create_node(user)

    def plot_followers(self,user):
        user_node = self.users.get(twitter_id = user.id)[0] 
        followers = user.followers()
        print "No of followers : {0}".format(len(followers))
        for follower in followers:
            if follower.id not in self.visited_users:
                self.create_node(follower)
            self.create_relationship(follower, user, "follower")

    def plot(self):
        current_level_users = set()
        for username in self.initial_users:
            user = self.api_handler.get_user(screen_name = username)
            self.plot_self(user)
            current_level_users.add(user)   
        while self.levels > 0:
            next_level_users = set()
            for user in current_level_users:
                for follower in user.followers():
                    next_level_users.add(follower)
                self.plot_followers(user)
            current_level_users = next_level_users
            self.levels = self.levels -1