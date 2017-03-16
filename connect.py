import tweepy
from configparser import SafeConfigParser
from neo4jrestclient.client import GraphDatabase
def connect(consumer_key, consumer_secret, access_key, access_secret):
    db = GraphDatabase("http://localhost:7474", username="neo4j", password="lionking")
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    return api,db

def main():
    parser = SafeConfigParser()
    parser.read("access.conf")
    consumer_key = parser.get("twitter-consumer","public_key")
    consumer_secret = parser.get("twitter-consumer","secret_key")
    access_key = parser.get("twitter-access","public_key")
    access_secret = parser.get("twitter-access","secret_key")
    api,db = connect(consumer_key, consumer_secret, access_key, access_secret)
    levels = 2
    user_set = set()
    users = db.labels.create("User")
    plot(user_set, users,db,api, levels)

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
