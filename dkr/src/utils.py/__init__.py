import pandas as pd
import requests
import .Config



def retrieve_posts(start: int, stop: int):
    """Collects new posts from hacker news api
    
    Args:
    -----
    start - int - id of first post to collect
    stop - int - id of last post to collect
    
    Returns:
    -------
    posts - pd.Dataframe
    """
    if start > stop:
        raise ValueError("Value mismatch: Start must be less than stop")
    
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
        
    return pd.DataFrame(comments)