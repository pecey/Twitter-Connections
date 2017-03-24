import tweepy
from configparser import SafeConfigParser
from neo4jrestclient.client import GraphDatabase

class TwitterGraph:
    def __init__(self, config, levels):
        twitter_configuration = config["twitter"]
        neo4j_configuration = config["neo4j"]
        self.api_handler = connect_to_twitter(twitter_configuration)
        self.neo4j_handler = connect_to_neo4j(neo4j_configuration)
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



def connect_to_neo4j(neo4j_configuration):
    host = neo4j_configuration['host']
    username = neo4j_configuration['username']
    password = neo4j_configuration['password']
    db_handler = GraphDatabase(host, username = username, password = password)
    return db_handler

def connect_to_twitter(twitter_configuration):
    auth = tweepy.OAuthHandler(twitter_configuration['consumer_key'], twitter_configuration['consumer_secret'])
    auth.set_access_token(twitter_configuration['access_key'], twitter_configuration['access_secret'])
    api = tweepy.API(auth)
    return api

def main():
    config_file = "access.conf"
    twitter_configuration = get_twitter_configuration(config_file)
    neo4j_configuration = get_neo4j_configuration(config_file)
    postgres_configuration =  get_postgres_configuration(config_file)
    config = dict()
    config["twitter"] = twitter_configuration
    config["neo4j"] = neo4j_configuration
    levels = 2
    twitter_graph = TwitterGraph(config, levels)
    twitter_graph.plot()


def get_twitter_configuration(config_file):
    parser = SafeConfigParser()
    parser.read(config_file)
    twitter_configuration = dict()
    twitter_configuration['consumer_key'] = parser.get("twitter-consumer","public_key")
    twitter_configuration['consumer_secret'] = parser.get("twitter-consumer","secret_key")
    twitter_configuration['access_key'] = parser.get("twitter-access","public_key")
    twitter_configuration['access_secret'] = parser.get("twitter-access","secret_key")
    return twitter_configuration


def get_neo4j_configuration(config_file):
    parser = SafeConfigParser()
    parser.read(config_file)
    neo4j_configuration = dict()
    neo4j_configuration['host'] = parser.get("neo4j-credentials","host")
    neo4j_configuration['username'] = parser.get("neo4j-credentials","username")
    neo4j_configuration['password'] = parser.get("neo4j-credentials","password")
    return neo4j_configuration


def get_postgres_configuration(config_file):
    parser = SafeConfigParser()
    parser.read(config_file)
    postgres_configuration = dict()
    postgres_configuration['host'] = parser.get("postgres-credentials","host")
    postgres_configuration['username'] = parser.get("postgres-credentials","username")
    postgres_configuration['password'] = parser.get("postgres-credentials","password")
    return postgres_configuration


if __name__ == "__main__":
    main()

#Deleting labels
#MATCH (n)
#DETACH DELETE n
