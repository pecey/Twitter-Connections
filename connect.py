import tweepy
from configparser import SafeConfigParser
from neo4jrestclient.client import GraphDatabase
def connect(consumer_key, consumer_secret, access_key, access_secret):
    print "CKey : {0} CSecret : {1} AKey : {2} ASecret : {3}".format(consumer_key, consumer_secret, access_key, access_secret)
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
    levels = 1
    user_set = set()
    users = db.labels.create("User")
    plot(user_set, users,db,api)

def plot(user_set, users,db, api):
    me = api.me()
    user_set.add(me.id) 
    root_node = db.nodes.create(twitter_id = me.id)
    users.add(root_node)
    plot_followers(me, user_set, users,db,root_node)
                
def plot_followers(user, user_set, users,db,user_node):
    followers = user.followers()
    print "No of followers : {0}".format(len(followers))
    dir(user_node)
    for follower in followers:
        if follower.id not in user_set:
            follower_node = db.nodes.create(twitter_id = follower.id)
            follower_node.relationships.create("followers", user_node)
            users.add(follower_node)
        else:
            follower_node = users.get(twitter_id = follower.id)
            follower_node.relationships.create("followers", user_node)

if __name__ == "__main__":
    main()

#Deleting labels
#MATCH (n)
#DETACH DELETE n
