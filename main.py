from connect import TwitterConnector, Neo4jConnector
from twitter_graph import TwitterGraph

def main():
    config_file = "access.conf"
    twitter_handler = TwitterConnector(config_file).fetch().connect()
    neo4j_handler = Neo4jConnector(config_file).fetch().connect()
    levels = 2
    handlers = dict()
    handlers["twitter"] = twitter_handler
    handlers["neo4j"] = neo4j_handler
    twitter_graph = TwitterGraph(handlers,levels)
    twitter_graph.plot()

if __name__ == "__main__":
    main()
