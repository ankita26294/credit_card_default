import pymongo
import pandas as pd
import json
# from default.config import mongo_client

# Provide the mongodb localhost url to connect python to mongodb.
client = pymongo.MongoClient("mongodb://localhost:27017/neurolabDB")
DATA_FILE_PATH ="/config/workspace/UCI_Credit_Card.csv"
DATABASE_NAME="default"
COLLECTION_NAME="credit"

if __name__=="__main__":
    df=pd.read_csv(DATA_FILE_PATH)
    print(f"Rows and columns :{df.shape}")
    df.reset_index(drop=True,inplace=True)
    json_record=list(json.loads(df.T.to_json()).values())
    print(json_record[0])

    # all data insert into mongodb
    client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)