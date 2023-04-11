import logging
import os
from datetime import time
import time
import yaml
import pandas

from hate_tweet_map.database import DataBase


def main():
    global db,db1, query
    start = time.time()
    logging.basicConfig()

    with open("edge_list_script.config", "r") as ymlfile:
        cfg = yaml.safe_load(ymlfile)
        source_field = cfg['criteria']['source']
        target_field = cfg['criteria']['target']


    if (source_field == "author_username" and target_field == "user_mentioned") or (source_field == "author_username" and target_field == "hashtag") or (source_field == "author_username" and target_field == "user_retweeted") or (source_field == "hashtag" and target_field == "user_mentioned"):
        print(" ")
    else:
        print("Non è possibile creare una edge list con questi parametri. \n")
        print("Le edge list possibili sono: \n")
        print("author_username --> MENZIONA --> user_mentioned \n")
        print("author_username --> UTILIZZA --> hashtag \n")
        print("author_username --> RITWITTA --> user_retweeted \n")
        print("hashtag --> UTILIZZATO NEL CONTESTO DI --> user_mentioned \n")


    log = logging.getLogger("CONVERTER EDGE LIST")
    log.setLevel(logging.INFO)

    db = DataBase('edge_list_script.config')
    db1 = DataBase('edge_list_script.config')

    """
    Inserting as source field "author_username" and inserting as target field "user_mentioned", a csv file will be created 
    with these specified parameters
    """
    if source_field == "author_username":
        if target_field == "user_mentioned":
            df1 = pandas.DataFrame(db.extract_all_tweets())
            df1.to_csv('dict', index=False)
            log.info("EXTRACT [MENTIONS]...")
            db.pipeline_mentions()
            db.pipeline_mentions1()
            db.pipeline_mentions2()
            db.pipeline_mentions3()
            db.pipeline_mentions4()
            result=db.pipeline_mentions5()
            log.info("UPDATE: {} TWEETS".format((result)))
            query = {"source": {"$exists": "true"}}
            db.extract(query)
            df = pandas.DataFrame(db.extract(query))
            newdf = df.explode('target')
            newdf.to_csv('data.csv', index=False)
            log.info("TWEETS SAVED ON: {}".format(os.path.abspath('../../data.csv')))
            db.delete_collection()
            name = cfg['mongodb']['collection']
            db1 = db.create_collection(name)
            data = df1.to_dict(orient="records")
            db1.insert_many(data)
            ABSOLUTE_PATH = os.path.abspath("dict")
            os.remove(ABSOLUTE_PATH)

    """
    Inserting as source field "author_username" and inserting as target field "hashtag", a csv file will be created 
    with these specified parameters
    """
    if source_field == "author_username":
        if target_field == "hashtag":
            df1 = pandas.DataFrame(db.extract_all_tweets())
            df1.to_csv('dict', index=False)
            log.info("EXTRACT [HASHTAG]...")
            result = db.pipeline_hashtags()
            log.info("UPDATE: {} TWEETS".format((result)))
            query = {"source":{"$exists":"true"}}
            db.extract(query)
            df = pandas.DataFrame(db.extract(query))
            newdf=df.explode('target')
            newdf.to_csv('prova.csv', index=False)
            log.info("TWEETS SAVED ON: {}".format(os.path.abspath('../../data.csv')))
            db.delete_collection()
            name = cfg['mongodb']['collection']
            db1 = db.create_collection(name)
            data = df1.to_dict(orient="records")
            db1.insert_many(data)
            ABSOLUTE_PATH=os.path.abspath("dict")
            os.remove(ABSOLUTE_PATH)
    """
    Inserting as source field "hashtag" and inserting as target field "user_mentioned", a csv file will be created 
    with these specified parameters
    """
    if source_field == "hashtag":
        if target_field == "user_mentioned":
            df1 = pandas.DataFrame(db.extract_all_tweets())
            df1.to_csv('dict', index=False)
            log.info("EXTRACT [MENTIONS]...")
            db.pipeline_hashtags1()
            db.pipeline_hashtags2()
            db.pipeline_hashtags3()
            db.pipeline_hashtags4()
            db.pipeline_hashtags5()
            result=db.pipeline_hashtags6()
            log.info("UPDATE: {} TWEETS".format((result)))
            query = {"source": {"$exists": "true"}}
            db.extract(query)
            df = pandas.DataFrame(db.extract(query))
            newdf=df.explode('target')
            newdf1=newdf.explode("source")
            newdf1.to_csv('data.csv', index=False)
            log.info("TWEETS SAVED ON: {}".format(os.path.abspath('../../data.csv')))
            db.delete_collection()
            name = cfg['mongodb']['collection']
            db1 = db.create_collection(name)
            data = df1.to_dict(orient="records")
            db1.insert_many(data)
            ABSOLUTE_PATH = os.path.abspath("dict")
            os.remove(ABSOLUTE_PATH)

    """
    Inserting as source field "author_username" and inserting as target field "user_retweeted", a csv file will be created 
    with these specified parameters
    """
    if source_field == "author_username":
        if target_field == "user_retweeted":
            df1 = pandas.DataFrame(db.extract_all_tweets())
            df1.to_csv('dict', index=False)
            log.info("EXTRACT [RETWEET]...")
            db.pipeline_retweets1()
            result=db.pipeline_retweets()
            log.info("UPDATE: {} TWEETS".format((result)))
            query = {"source":{"$exists":"true"}}
            db.extract(query)
            df = pandas.DataFrame(db.extract(query))
            newdf = df.explode('target')
            newdf.to_csv('data2.csv', index=False)
            log.info("TWEETS SAVED ON: {}".format(os.path.abspath('../../data.csv')))
            db.delete_collection()
            name = cfg['mongodb']['collection']
            db1 = db.create_collection(name)
            data = df1.to_dict(orient="records")
            db1.insert_many(data)
            ABSOLUTE_PATH = os.path.abspath("dict")
            os.remove(ABSOLUTE_PATH)

    end = time.time()
    log.info("DONE IN: {}".format(end - start))


if __name__ == "__main__":
    main()
