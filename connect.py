import tweepy
from configparser import SafeConfigParser
from neo4jrestclient.client import GraphDatabase

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
    api = connect_to_twitter(twitter_configuration)
    db = connect_to_neo4j(neo4j_configuration)
    levels = 2
    user_set = set()
    users = db.labels.create("User")
    initial_users = {"pecey01"}
    plot(initial_users,user_set, users,db,api, levels)

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



def plot(user_set, users,db, api, levels):
    user = api.me()
    plot_self(user, user_set, users, db)
    current_level_users = {user}
    while levels > 0:
        next_level_users = set()
        for user in current_level_users:
            for follower in user.followers():
                next_level_users.add(follower)
            plot_followers(user, user_set, users, db)
        current_level_users = next_level_users
        levels = levels -1
            

def plot_self(user, user_set, users, db):
    create_node(user, users, user_set, db)

def plot_followers(user, user_set, users,db):
    user_node = users.get(twitter_id = user.id)[0] 
    followers = user.followers()
    print "No of followers : {0}".format(len(followers))
    for follower in followers:
        if follower.id not in user_set:
            create_node(follower, users, user_set, db)
        create_relationship(follower, user, "follower", users)

def create_node(user, users, user_set, db):
    user_node = db.nodes.create(twitter_id = user.id, twitter_login = user.screen_name)
    users.add(user_node)
    user_set.add(user.id)

def create_relationship(source, destination, relation,users):
    source_node = users.get(twitter_id = source.id)[0]
    destination_node = users.get(twitter_id = destination.id)[0]
    source_node.relationships.create(relation, destination_node)    

if __name__ == "__main__":
    main()

#Deleting labels
#MATCH (n)
#DETACH DELETE n
