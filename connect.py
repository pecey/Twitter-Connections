import tweepy
from configparser import SafeConfigParser
from neo4jrestclient.client import GraphDatabase

class TwitterConnector():
    def __init__(self, config_file):
        self.handler = None
        self.config_file = config_file
        self.twitter_configuration = dict()

    def fetch(self):
        parser = SafeConfigParser()
        parser.read(self.config_file)
        self.twitter_configuration['consumer_key'] = parser.get("twitter-consumer","public_key")
        self.twitter_configuration['consumer_secret'] = parser.get("twitter-consumer","secret_key")
        self.twitter_configuration['access_key'] = parser.get("twitter-access","public_key")
        self.twitter_configuration['access_secret'] = parser.get("twitter-access","secret_key")
        return self
        
    def connect(self):
        auth = tweepy.OAuthHandler(self.twitter_configuration['consumer_key'], self.twitter_configuration['consumer_secret'])
        auth.set_access_token(self.twitter_configuration['access_key'], self.twitter_configuration['access_secret'])
        self.handler = tweepy.API(auth)
        return self.handler

class Neo4jConnector():
    def __init__(self, config_file):
        self.handler = None
        self.config_file = config_file
        self.neo4j_configuration = dict()

    def fetch(self):
        parser = SafeConfigParser()
        parser.read(self.config_file)
        self.neo4j_configuration['host'] = parser.get("neo4j-credentials","host")
        self.neo4j_configuration['username'] = parser.get("neo4j-credentials","username")
        self.neo4j_configuration['password'] = parser.get("neo4j-credentials","password")
        return self
        
    def connect(self):
        host = self.neo4j_configuration['host']
        username = self.neo4j_configuration['username']
        password = self.neo4j_configuration['password']
        self.handler = GraphDatabase(host, username = username, password = password)
        return self.handler

#Deleting labels
#MATCH (n)
#DETACH DELETE n
