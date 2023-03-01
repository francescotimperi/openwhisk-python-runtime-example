import uuid
import os
import time
import duckdb

# global conn object - we re-use this across function calls
con = None

def main(args):
    """
    Run a SQL query in a memory db as a serverless function
    """
    # debug
    print(args)
    is_warm = False
    # run a timer for info
    start = time.time()
    global con
    if not con:
        print("Cold start!")
        con = duckdb.connect(database=':memory:')
        con.execute("""
            INSTALL httpfs;
            LOAD httpfs;
            SET s3_region='us-east-1';
            SET s3_access_key_id='{}';
            SET s3_secret_access_key='{}';
        """.format(args['S3_USER'], args['S3_ACCESS'])
        )
    else:
        print("Warm start!")
        is_warm = True

    event_query =  args['q'] or None
    dump_to_storage = args['dump'] or False

    if not event_query:
        # debug
        print("No query received, returning a static response")
        # NOTE: this parquet pattern does NOT work on an AWS LAMBDA function with duck 0.7
        event_query = """
            SELECT COUNT(*) 
            FROM parquet_scan('s3://bauplan-qwak-reduce/data/2/*/*.parquet', HIVE_PARTITIONING=1)
            WHERE date BETWEEN '2022-01-01' AND '2022-01-02'
        """.strip()
    # get results
    results = con.execute(event_query).fetchall()
    # debug 
    if results:
        print("Total results: ", len(results))
    
    # return to client
    return {
        "metadata": {
            "timeMs": int((time.time() - start) * 1000.0),
            "epochMs": int(time.time() * 1000),
            "eventId": str(uuid.uuid4()),
            "query": event_query,
            "mock": event_query is None,
            "warm": is_warm
        },
        "data": {
            "results": results
        }
    }