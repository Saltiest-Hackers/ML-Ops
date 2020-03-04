import requests
import psycopg2
from .config import Config
import utils

with psycopg2.connect(CONN_ARGS) as conn:
    with conn.cursor() as curs:
        
        # Collect id of most recent post in DB
        query = """
            SELECT id
            FROM comments
            ORDER BY time desc
            LIMIT 1"""
        curs.execute(query)
        response = curs.fetchone()
        
        # collect recent posts from Hacker News API
        
        min_id = response[0] + 1
        max_id = requests.get(LATEST).json()
        
        new_items = list(range(min_id, max_id + 1))
        
        comments = []
        
        for uri in new_items:
            uri = HNAPI + f'item/{item}.json'
            item = requests.get(uri).json()            

            if item is None:
                continue
            
            comment = True if item['type'] == 'comment' else False
            if not comment:
                continue
            
            comments.append(pd.Series(item))
        
        df = pd.DataFrame(comments)
        
        # TODO: Use vader to score new values
        
        # TODO: Insert new values to DB
        
    
            
        
        
        
        

        
        
        
        

        


        
        
    
