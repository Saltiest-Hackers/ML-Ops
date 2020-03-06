# Saltiest Hackers Data Endpoints 

## 1. Top 100 Saltiest Comments
Returns: 
`{"author": string, "comment_text": string, "id": int, "parent_id": int, "saltiness": float, "time": int}`

Endpoint: hn-saltiness.herokuapp.com/topcomments

## 2. Top 100 Saltiest Users
Returns:
`{"author": string, "avg_salt": float, "n_comments": int}`

Endpoint: hn-saltiness.herokuapp.com/topusers

## 3. User's Saltiest Comments
Returns: 
`{"author": string, "comment_text": string, "id": int, "parent_id": int, "saltiness": float, "time": int}`

Endpoint: https://hn-saltiness.herokuapp.com/user/username

## 4. Single Comment Endpoint
Returns: 
`{"author": string, "comment_text": string, "id": int, "parent_id": int, "saltiness": float, "time": int}`

Endpoint: https://hn-saltiness.herokuapp.com/comment/comment_id